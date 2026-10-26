"""Focused real-seam tests for the fictional-parent role-play package."""

import hashlib
import http.client
import json
from pathlib import Path
import threading
import unittest

import m02_demo_operator_tests
from iiw_qr_session.package import BindConfiguration
from iiw_fictional_parent import connection, gateway, session

REPO = Path(__file__).resolve().parents[1]


class FictionalParentTests(unittest.TestCase):
    def setUp(self):
        self.base = m02_demo_operator_tests.DemoOperatorTests(methodName="runTest")
        self.base.setUp()
        self.receipt_sequence = 0
        self.capability = bytes(range(32))

    def tearDown(self):
        self.base.tearDown()

    def receipt_id(self):
        self.receipt_sequence += 1
        return "q" + format(self.receipt_sequence, "031d")

    def begin_encounter(self, *, held_participant=session.PARTICIPANT,
                        pending_path=None):
        token, status, headers, body = self.base.begin(participant=held_participant)
        self.assertEqual((status, body), (202, {"status": "pending"}))
        qr_session, connected = connection.create_encounter(
            gateway_instance="table-1", capability_factory=lambda size: self.capability,
            store=self.base.store, policy=self.base.policy,
            pending_path=pending_path or headers["Location"], clock=self.base.clock,
            receipt_id_factory=self.receipt_id)
        return token, headers["Location"], qr_session, connected

    def submit(self, qr_session, choice=session.APPROVE, **changes):
        fields = {"capability": self.capability.hex(), "choice": choice,
                  "scenario": session.SCENARIO, "action": session.ACTION_LABEL,
                  "participant": session.PARTICIPANT, "roleplay": session.ROLEPLAY,
                  "gateway_instance": "table-1"}
        fields.update(changes)
        return qr_session.submit(**fields)

    def test_01_exact_disclosure_buttons_and_fixed_meaning(self):
        text = gateway._HTML.decode()
        for value in (gateway.DISCLOSURE, gateway.SOURCE_DISCLOSURE,
                      gateway.SCOPE_DISCLOSURE,
                      "Approve the directed response in this fictional scenario",
                      "Decline the directed response in this fictional scenario"):
            self.assertIn(value, text)
        self.assertIn("does not identify or authenticate you", gateway.SOURCE_DISCLOSURE)

    def test_02_fragment_removed_before_controls_enable(self):
        text = gateway._SCRIPT.decode()
        self.assertLess(text.index("history.replaceState"), text.index("b.disabled=false"))

    def test_03_approve_real_seam_polls_200(self):
        token, path, qr, connected = self.begin_encounter()
        event = connected.record(self.submit(qr))
        status, _, body = self.base.poll(path, token)
        self.assertEqual((status, body["decision"]["reason"]), (200, "approval_active"))
        self.assertEqual(body["decision"]["approval_source"],
                         "local-operator-demo-control")
        self.assertEqual(event.assurance, "unverified-demo-input")

    def test_04_decline_real_seam_polls_403(self):
        token, path, qr, connected = self.begin_encounter()
        connected.record(self.submit(qr, session.DECLINE))
        status, _, body = self.base.poll(path, token)
        self.assertEqual((status, body["decision"]["reason"]),
                         (403, "approval_withdrawn"))

    def test_05_no_standing_policy_mutation(self):
        before = self.base.policy.calls
        _, _, qr, connected = self.begin_encounter()
        connected.record(self.submit(qr))
        self.assertEqual(self.base.policy.calls, before)
        self.assertNotIn("replace_standing_input",
                         (REPO / "iiw_fictional_parent/connection.py").read_text())

    def test_06_no_choice_stays_pending_then_expires(self):
        token, path, _, _ = self.begin_encounter()
        self.assertEqual(self.base.poll(path, token)[0], 202)
        self.base.clock.value += 120
        self.assertEqual(self.base.poll(path, token)[0], 408)

    def test_07_expiry_cancel_replay_and_duplicate_are_one_use(self):
        _, _, qr, _ = self.begin_encounter()
        self.submit(qr)
        with self.assertRaises(session.FictionalParentSessionUnavailable): self.submit(qr)
        _, _, qr2, _ = self.begin_encounter()
        qr2.cancel()
        with self.assertRaises(session.FictionalParentSessionUnavailable): self.submit(qr2)
        _, _, qr3, _ = self.begin_encounter()
        self.base.clock.value += 30
        with self.assertRaises(session.FictionalParentSessionUnavailable): self.submit(qr3)
        with self.assertRaises(session.FictionalParentSessionUnavailable): _ = qr3.capability

    def test_08_binding_mismatches_and_unknown_choice_fail_closed(self):
        for key in ("capability", "choice", "scenario", "action", "participant",
                    "roleplay", "gateway_instance"):
            _, _, qr, _ = self.begin_encounter()
            with self.assertRaises(session.FictionalParentSessionUnavailable):
                self.submit(qr, **{key: "wrong"})

    def test_09_concurrent_session_submissions_accept_at_most_one(self):
        _, _, qr, _ = self.begin_encounter(); results = []
        def submit_once():
            try: self.submit(qr); results.append("ok")
            except session.FictionalParentSessionUnavailable: results.append("refused")
        threads = [threading.Thread(target=submit_once) for _ in range(12)]
        for item in threads: item.start()
        for item in threads: item.join(2)
        self.assertEqual(results.count("ok"), 1)

    def test_10_second_connection_for_same_path_is_refused(self):
        _, path, _, _ = self.begin_encounter()
        with self.assertRaises(connection.FictionalParentConnectionUnavailable):
            connection.create_connection(
                store=self.base.store, policy=self.base.policy, pending_path=path,
                clock=self.base.clock, encounter_started_at=self.base.clock(),
                receipt_id_factory=self.receipt_id)

    def test_11_real_adapter_refusal_consumes_connection(self):
        # Unknown live-record identifier.
        _, _, qr, connected = self.begin_encounter(
            pending_path="/pending/" + "z" * 32)
        event = self.submit(qr)
        with self.assertRaises(connection.FictionalParentConnectionUnavailable):
            connected.record(event)
        # Malformed pending path.
        _, _, qr2, malformed = self.begin_encounter(pending_path="/not-pending")
        event2 = self.submit(qr2)
        with self.assertRaises(connection.FictionalParentConnectionUnavailable):
            malformed.record(event2)
        # Already-terminal record through the public accepted seams.
        token3, path3, qr3, terminal = self.begin_encounter()
        self.base.adapter.record_held_input(path3, "APPROVED")
        self.base.poll(path3, token3)
        event3 = self.submit(qr3)
        with self.assertRaises(connection.FictionalParentConnectionUnavailable):
            terminal.record(event3)
        # Expired held record; the shorter QR session is already unavailable too.
        _, _, qr4, expired = self.begin_encounter()
        self.base.clock.value += 120
        with self.assertRaises(session.FictionalParentSessionUnavailable): self.submit(qr4)
        with self.assertRaises(connection.FictionalParentConnectionUnavailable):
            expired.record(session.FictionalParentChoice(
                session.APPROVE, session.SCENARIO, session.ACTION_LABEL,
                session.PARTICIPANT, session.ROLEPLAY, "table-1"))
        with self.assertRaises(connection.FictionalParentConnectionUnavailable):
            connected.record(event)

    def test_12_signed_poll_outcome_set(self):
        token, path, qr, connected = self.begin_encounter()
        connected.record(self.submit(qr))
        self.assertEqual(self.base.poll(path, token)[0], 200)
        self.assertEqual(self.base.poll(path, token)[0], 410)
        self.assertEqual(self.base.poll("/pending/" + "x" * 32, token)[0], 404)
        token2, path2, _, _ = self.begin_encounter()
        self.assertEqual(self.base.poll(path2, token2)[0], 202)

    def test_13_deliberate_participant_mismatch_is_named(self):
        token, path, qr, connected = self.begin_encounter(
            held_participant="different-fictional-child")
        connected.record(self.submit(qr))
        status, _, body = self.base.poll(path, token)
        self.assertEqual((status, body["decision"]["reason"]),
                         (403, "participant_mismatch"))

    def live_gateway(self, *, pending_path=None):
        _, _, qr, connected = self.begin_encounter(pending_path=pending_path)
        config = BindConfiguration(address="127.0.0.1",
                                   interface_addresses=("127.0.0.1",),
                                   synthetic_loopback=True)
        host = "fictional.test"
        handler = gateway.handler_for(session=qr, gateway_instance="table-1",
                                      exact_host=host, connection=connected)
        server = gateway.server_for(configuration=config, port=0, handler_class=handler)
        thread = threading.Thread(target=server.serve_forever); thread.start()
        return server, thread, host, qr

    def request(self, server, method, path, host, body=None, headers=None):
        client = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
        values = {"Host": host}; values.update(headers or {})
        client.request(method, path, body=body, headers=values)
        response = client.getresponse(); payload = response.read()
        result = response.status, dict(response.getheaders()), payload
        client.close(); return result

    def test_14_live_http_headers_host_framing_and_uniform_refusal(self):
        server, thread, host, _ = self.live_gateway()
        try:
            status, headers, _ = self.request(server, "GET", gateway.PARTICIPANT_PATH, host)
            self.assertEqual(status, 200)
            for name in gateway.SECURITY_HEADERS: self.assertIn(name, headers)
            self.assertEqual(self.request(server, "GET", gateway.PARTICIPANT_PATH,
                                          "wrong.test")[0], 400)
            self.assertEqual(self.request(server, "PUT", gateway.PARTICIPANT_PATH,
                                          host, body=b"untrusted")[0], 405)
            self.assertEqual(self.request(server, "POST", gateway.CHOICE_PATH, host,
                                          body=b"{}", headers={"Content-Type": "text/plain"})[0], 400)
            self.assertEqual(self.request(server, "POST", gateway.CHOICE_PATH, host,
                                          body=b"{" * 1025, headers={"Content-Type": "application/json"})[0], 400)
        finally:
            server.shutdown(); server.server_close(); thread.join(2)

    def test_15_bind_configuration_refuses_non_exact_addresses(self):
        for address in ("0.0.0.0", "localhost", "127.0.0.2", "192.0.2.1"):
            config = BindConfiguration(address=address,
                                       interface_addresses=("127.0.0.1",),
                                       synthetic_loopback=True)
            with self.assertRaises(ValueError):
                gateway.server_for(configuration=config, port=0,
                                   handler_class=gateway.BaseHTTPRequestHandler)

    def test_16_responses_and_errors_do_not_leak_secret_values(self):
        server, thread, host, _ = self.live_gateway()
        try:
            status, _, body = self.request(
                server, "POST", gateway.CHOICE_PATH, host,
                body=json.dumps({"capability": "wrong"}).encode(),
                headers={"Content-Type": "application/json"})
            self.assertEqual(status, 404)
            for secret in (self.capability.hex(), "q" * 32, "eyJ"):
                self.assertNotIn(secret.encode(), body)
        finally:
            server.shutdown(); server.server_close(); thread.join(2)
        # A real adapter refusal is a uniform public 404 and consumes the session.
        server, thread, host, refused_qr = self.live_gateway(
            pending_path="/pending/" + "y" * 32)
        try:
            body = json.dumps({
                "capability": self.capability.hex(), "choice": session.APPROVE,
                "scenario": session.SCENARIO, "action": session.ACTION_LABEL,
                "participant": session.PARTICIPANT, "roleplay": session.ROLEPLAY,
            }).encode()
            status, _, response = self.request(
                server, "POST", gateway.CHOICE_PATH, host, body=body,
                headers={"Content-Type": "application/json"})
            self.assertEqual((status, json.loads(response)),
                             (404, {"status": "session unavailable"}))
            with self.assertRaises(session.FictionalParentSessionUnavailable):
                _ = refused_qr.capability
            status2, _, _ = self.request(
                server, "POST", gateway.CHOICE_PATH, host, body=body,
                headers={"Content-Type": "application/json"})
            self.assertEqual(status2, 404)
        finally:
            server.shutdown(); server.server_close(); thread.join(2)

    def test_17_gateway_shutdown_closes_listener(self):
        server, thread, _, _ = self.live_gateway(); port = server.server_port
        server.shutdown(); server.server_close(); thread.join(2)
        self.assertFalse(thread.is_alive())
        with self.assertRaises(OSError):
            http.client.HTTPConnection("127.0.0.1", port, timeout=.2).connect()

    def test_18_same_tick_timer_precedence_and_frozen_sources(self):
        _, _, qr, connected = self.begin_encounter()
        self.assertIs(qr.clock, connected.clock)
        self.assertEqual(qr.encounter_started_at, connected.encounter_started_at)
        self.assertEqual(qr.expires_at - qr.encounter_started_at, 30)
        expected = {
            "m02_aauth_fcf656d/approval_pending.py": "18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b",
            "m02_aauth_fcf656d/demo_operator.py": "b65160deffccf80220a0f466384a98ad1c3d21101dc44a1ee3b5d8099bf238a3",
            "m02_aauth_fcf656d/other_party_approval.py": "c5a244da3ef5e6694df663af2ff0fb5cd83cdf928fa49c1ab708b197c35d78b0",
            "iiw_qr_session/package.py": "3f079c3bd7c834758a1062926f5083d556497ab8013a2426ea5bef95584495c9"}
        for relative, digest in expected.items():
            self.assertEqual(hashlib.sha256((REPO / relative).read_bytes()).hexdigest(), digest)
        for path in (REPO / "iiw_fictional_parent").glob("*.py"):
            self.assertNotIn("iiw_qr_session.session", path.read_text())
