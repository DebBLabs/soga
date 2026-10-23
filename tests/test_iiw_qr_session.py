"""Focused tests for the standalone IIW QR participant-session package."""

import http.client
import hashlib
import json
from contextlib import ExitStack
from pathlib import Path
import socket
import tempfile
import threading
import unittest
from unittest import mock

from iiw_qr_session.gateway import (
    GatewayConfigurationError, handler_for, participant_url, server_for,
)
from iiw_qr_session.package import (
    PackageValidationError, validate_bind_configuration, validate_manifest,
    validate_private_ipv4,
)
from iiw_qr_session.session import (
    ALLOW_DIRECTED_RESPONSE, DECLINE_DIRECTED_RESPONSE, FIXTURE_ACTION,
    FIXTURE_MISSION, FIXTURE_PARTICIPANT, ParticipantSession,
    SessionUnavailable,
)


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def fixed_entropy(size):
    return bytes(range(size))


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.session = ParticipantSession(
            gateway_instance="fixture-gateway", clock=self.clock,
            capability_factory=fixed_entropy)

    def submit(self, **changes):
        values = dict(
            capability=self.session.capability,
            choice=ALLOW_DIRECTED_RESPONSE, mission=FIXTURE_MISSION,
            action=FIXTURE_ACTION, participant=FIXTURE_PARTICIPANT,
            gateway_instance="fixture-gateway")
        values.update(changes)
        return self.session.submit(**values)

    def test_exact_allow_and_decline_choices(self):
        self.assertEqual(self.submit().choice, ALLOW_DIRECTED_RESPONSE)
        other = ParticipantSession(gateway_instance="fixture-gateway", clock=self.clock,
                                   capability_factory=fixed_entropy)
        self.assertEqual(other.submit(
            capability=other.capability, choice=DECLINE_DIRECTED_RESPONSE,
            mission=FIXTURE_MISSION, action=FIXTURE_ACTION,
            participant=FIXTURE_PARTICIPANT,
            gateway_instance="fixture-gateway").choice, DECLINE_DIRECTED_RESPONSE)

    def test_replay_and_cancel_fail_indistinguishably(self):
        capability = self.session.capability
        self.submit()
        with self.assertRaisesRegex(SessionUnavailable, "session unavailable"):
            self.session.submit(capability=capability, choice=ALLOW_DIRECTED_RESPONSE,
                mission=FIXTURE_MISSION, action=FIXTURE_ACTION,
                participant=FIXTURE_PARTICIPANT, gateway_instance="fixture-gateway")
        cancelled = ParticipantSession(gateway_instance="fixture-gateway", clock=self.clock,
                                       capability_factory=fixed_entropy)
        capability = cancelled.capability
        cancelled.cancel()
        with self.assertRaisesRegex(SessionUnavailable, "session unavailable"):
            cancelled.submit(capability=capability, choice=ALLOW_DIRECTED_RESPONSE,
                mission=FIXTURE_MISSION, action=FIXTURE_ACTION,
                participant=FIXTURE_PARTICIPANT, gateway_instance="fixture-gateway")

    def test_expiry_boundary(self):
        capability = self.session.capability
        self.clock.now = 220.0
        with self.assertRaises(SessionUnavailable):
            self.session.submit(capability=capability, choice=ALLOW_DIRECTED_RESPONSE,
                mission=FIXTURE_MISSION, action=FIXTURE_ACTION,
                participant=FIXTURE_PARTICIPANT, gateway_instance="fixture-gateway")
        with self.assertRaises(SessionUnavailable):
            _ = self.session.capability

    def test_every_binding_and_unknown_choice_fail(self):
        for field, value in (
            ("capability", "00" * 32), ("choice", "MAYBE"),
            ("mission", "other"), ("action", "other"),
            ("participant", "other"), ("gateway_instance", "other")):
            session = ParticipantSession(gateway_instance="fixture-gateway", clock=self.clock,
                                         capability_factory=fixed_entropy)
            self.session = session
            with self.assertRaisesRegex(SessionUnavailable, "session unavailable"):
                self.submit(**{field: value})

    def test_default_entropy_and_constructor_refusals(self):
        session = ParticipantSession(gateway_instance="fixture-gateway", clock=self.clock)
        capability = session.capability
        self.assertEqual(len(capability), 64)
        self.assertTrue(all(value in "0123456789abcdef" for value in capability))
        for changes in (
            {"gateway_instance": ""}, {"gateway_instance": "é"},
            {"lifetime_seconds": True}, {"lifetime_seconds": 121},
            {"capability_factory": lambda _size: b"short"},
        ):
            values = dict(gateway_instance="fixture-gateway", clock=self.clock,
                          capability_factory=fixed_entropy)
            values.update(changes)
            with self.assertRaises((TypeError, ValueError)):
                ParticipantSession(**values)

    def test_concurrent_submission_consumes_once(self):
        capability = self.session.capability
        barrier = threading.Barrier(8)
        accepted = []
        refused = []

        def submit():
            barrier.wait()
            try:
                accepted.append(self.session.submit(
                    capability=capability, choice=ALLOW_DIRECTED_RESPONSE,
                    mission=FIXTURE_MISSION, action=FIXTURE_ACTION,
                    participant=FIXTURE_PARTICIPANT,
                    gateway_instance="fixture-gateway"))
            except SessionUnavailable:
                refused.append(True)

        workers = [threading.Thread(target=submit) for _ in range(8)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=2)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(refused), 7)


class AddressTests(unittest.TestCase):
    def test_private_ipv4_only(self):
        self.assertEqual(validate_private_ipv4("192.168.10.4"), "192.168.10.4")
        for value in ("127.0.0.1", "0.0.0.0", "169.254.1.1", "224.0.0.1",
                      "8.8.8.8", "::1", "host.local", "192.168.010.4"):
            with self.assertRaises(PackageValidationError, msg=value):
                validate_private_ipv4(value)

    def test_bind_configuration_refuses_multiple_and_unassigned_addresses(self):
        valid = validate_bind_configuration(
            bind_addresses=["192.168.10.4"],
            interface_addresses={"192.168.10.4"})
        self.assertEqual(valid.address, "192.168.10.4")
        loopback = validate_bind_configuration(
            bind_addresses=["127.0.0.1"], interface_addresses={"127.0.0.1"},
            synthetic_loopback=True)
        self.assertTrue(loopback.synthetic_loopback)
        for addresses, observed, synthetic in (
            (["0.0.0.0"], {"0.0.0.0"}, False),
            (["host.local"], {"host.local"}, False),
            (["127.0.0.1"], {"127.0.0.1"}, False),
            (["192.168.10.4", "127.0.0.1"], {"192.168.10.4", "127.0.0.1"}, False),
            (["192.168.10.4"], {"192.168.10.5"}, False),
            (["192.168.10.4"], {"192.168.10.4"}, True),
        ):
            with self.assertRaises(PackageValidationError):
                validate_bind_configuration(
                    bind_addresses=addresses, interface_addresses=observed,
                    synthetic_loopback=synthetic)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="iiw-qr-manifest-")
        self.root = Path(self.temporary.name) / "bundle"
        self.root.mkdir()
        self.payload = self.root / "runtime.bin"
        self.payload.write_bytes(b"fixture-runtime")
        self.manifest_path = Path(self.temporary.name) / "manifest.json"

    def tearDown(self):
        self.temporary.cleanup()

    def manifest(self, **changes):
        value = {
            "schema": 1, "system": "FixtureOS", "machine": "fixture-machine",
            "python": "3.fixture",
            "files": {"runtime.bin": hashlib.sha256(b"fixture-runtime").hexdigest()},
        }
        value.update(changes)
        self.manifest_path.write_text(json.dumps(value), encoding="utf-8")
        return value

    def validate(self):
        with ExitStack() as stack:
            stack.enter_context(mock.patch(
                "iiw_qr_session.package.platform.system", return_value="FixtureOS"))
            stack.enter_context(mock.patch(
                "iiw_qr_session.package.platform.machine", return_value="fixture-machine"))
            stack.enter_context(mock.patch(
                "iiw_qr_session.package.platform.python_version", return_value="3.fixture"))
            return validate_manifest(self.root, self.manifest_path)

    def test_manifest_acceptance_and_identity_mismatches(self):
        expected = self.manifest()
        self.assertEqual(self.validate(), expected)
        self.manifest_path.write_text("{", encoding="utf-8")
        with self.assertRaises(PackageValidationError):
            self.validate()
        for changes in (
            {"schema": 2}, {"system": "OtherOS"}, {"machine": "other"},
            {"python": "other"}, {"files": {}},
            {"files": {"runtime.bin": "0" * 64}},
            {"extra": "field"}, {"files": None},
        ):
            self.manifest(**changes)
            with self.assertRaises(PackageValidationError):
                self.validate()

    def test_manifest_refuses_noncanonical_and_symlink_paths(self):
        outside = Path(self.temporary.name) / "outside.bin"
        outside.write_bytes(b"fixture-runtime")
        link = self.root / "linked"
        link.symlink_to(outside.parent, target_is_directory=True)
        for relative in ("../outside.bin", str(outside), "linked/outside.bin", "./runtime.bin"):
            self.manifest(files={relative: hashlib.sha256(b"fixture-runtime").hexdigest()})
            with self.assertRaises(PackageValidationError):
                self.validate()
        root_link = Path(self.temporary.name) / "bundle-link"
        root_link.symlink_to(self.root, target_is_directory=True)
        self.manifest()
        with self.assertRaises(PackageValidationError):
            with ExitStack() as stack:
                stack.enter_context(mock.patch(
                    "iiw_qr_session.package.platform.system", return_value="FixtureOS"))
                stack.enter_context(mock.patch(
                    "iiw_qr_session.package.platform.machine", return_value="fixture-machine"))
                stack.enter_context(mock.patch(
                    "iiw_qr_session.package.platform.python_version", return_value="3.fixture"))
                validate_manifest(root_link, self.manifest_path)
        manifest_link = Path(self.temporary.name) / "manifest-link.json"
        manifest_link.symlink_to(self.manifest_path)
        with self.assertRaises(PackageValidationError):
            with ExitStack() as stack:
                stack.enter_context(mock.patch(
                    "iiw_qr_session.package.platform.system", return_value="FixtureOS"))
                stack.enter_context(mock.patch(
                    "iiw_qr_session.package.platform.machine", return_value="fixture-machine"))
                stack.enter_context(mock.patch(
                    "iiw_qr_session.package.platform.python_version", return_value="3.fixture"))
                validate_manifest(self.root, manifest_link)


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.session = ParticipantSession(gateway_instance="fixture-gateway", clock=self.clock,
                                          capability_factory=fixed_entropy)
        self.events = []
        configuration = validate_bind_configuration(
            bind_addresses=["127.0.0.1"], interface_addresses={"127.0.0.1"},
            synthetic_loopback=True)
        placeholder = handler_for(session=self.session, gateway_instance="fixture-gateway",
                                  exact_host="127.0.0.1:1", callback=self.events.append)
        self.server = server_for(configuration=configuration, port=0,
                                 handler_class=placeholder)
        self.port = self.server.server_address[1]
        handler = handler_for(session=self.session, gateway_instance="fixture-gateway",
                              exact_host=f"127.0.0.1:{self.port}", callback=self.events.append)
        self.server.RequestHandlerClass = handler
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.closed = False

    def tearDown(self):
        if not self.closed:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=2)

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        value = response.read()
        result = response.status, dict(response.headers), value
        connection.close()
        return result

    def test_page_scrubs_fragment_and_sets_security_headers(self):
        status, headers, body = self.request(
            "GET", "/participant", headers={"Host": f"127.0.0.1:{self.port}"})
        self.assertEqual(status, 200)
        notice = body.index(b"unverified adult demo input")
        leave = body.index(b"choose nothing and leave")
        first_button = body.index(b"<button")
        self.assertLess(notice, first_button)
        self.assertLess(leave, first_button)
        self.assertIn(b"<button disabled", body)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertEqual(headers["Referrer-Policy"], "no-referrer")
        status, _, script = self.request(
            "GET", "/participant.js", headers={"Host": f"127.0.0.1:{self.port}"})
        self.assertEqual(status, 200)
        self.assertIn(b"history.replaceState", script)
        self.assertIn(b"requestAnimationFrame", script)
        self.assertNotIn(self.session.capability.encode(), body + script)

    def test_valid_choice_invokes_callback_once(self):
        body = json.dumps({
            "capability": self.session.capability,
            "choice": ALLOW_DIRECTED_RESPONSE, "mission": FIXTURE_MISSION,
            "action": FIXTURE_ACTION, "participant": FIXTURE_PARTICIPANT,
        })
        status, _, response = self.request("POST", "/choice", body=body, headers={
            "Host": f"127.0.0.1:{self.port}", "Content-Type": "application/json"})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(response), {"status": "choice recorded"})
        for forbidden in (b"eyJ", b"policy", b"127.0.0.1", b"adult-demo-participant"):
            self.assertNotIn(forbidden, response)
        self.assertEqual(len(self.events), 1)
        event = self.events[0]
        self.assertEqual((event.choice, event.mission, event.action,
                          event.participant, event.gateway_instance),
                         (ALLOW_DIRECTED_RESPONSE, FIXTURE_MISSION, FIXTURE_ACTION,
                          FIXTURE_PARTICIPANT, "fixture-gateway"))
        status, _, response = self.request("POST", "/choice", body=body, headers={
            "Host": f"127.0.0.1:{self.port}", "Content-Type": "application/json"})
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(response), {"status": "session unavailable"})
        self.assertEqual(len(self.events), 1)

    def test_invalid_requests_are_bounded(self):
        host = {"Host": f"127.0.0.1:{self.port}"}
        cases = (("GET", "/unknown", None, host, 404),
                 ("PUT", "/choice", b"x" * 2048, host, 405),
                 ("POST", "/choice", b"{}", host, 400),
                 ("POST", "/choice", b"{}", {**host, "Content-Type": "text/plain"}, 400))
        for method, path, body, headers, expected in cases:
            status, response_headers, _ = self.request(method, path, body, headers)
            self.assertEqual(status, expected)
            self.assertEqual(response_headers["Cache-Control"], "no-store")
        self.assertEqual(self.events, [])

    def test_framing_host_size_and_shape_refusals(self):
        host = f"127.0.0.1:{self.port}"
        invalid_json = (
            b"not-json", b"[]", b'{"unknown":true}',
            json.dumps({"capability": "00" * 32, "choice": "MAYBE",
                        "mission": FIXTURE_MISSION, "action": FIXTURE_ACTION,
                        "participant": FIXTURE_PARTICIPANT}).encode("utf-8"),
        )
        for body in invalid_json:
            status, headers, response = self.request("POST", "/choice", body=body,
                headers={"Host": host, "Content-Type": "application/json"})
            self.assertEqual(status, 404 if body.startswith(b'{"capability"') else 400)
            self.assertEqual(headers["Connection"], "close")
            self.assertNotIn(b"token", response)
        status, headers, _ = self.request("POST", "/choice", body=b"x" * 1025,
            headers={"Host": host, "Content-Type": "application/json"})
        self.assertEqual((status, headers["Connection"]), (400, "close"))
        for bad_host in ("localhost", "127.0.0.1:1"):
            status, _, _ = self.request("GET", "/participant", headers={"Host": bad_host})
            self.assertEqual(status, 400)
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.putrequest("GET", "/participant", skip_host=True)
        connection.putheader("Host", host)
        connection.putheader("Content-Length", "1")
        connection.endheaders(b"x")
        response = connection.getresponse()
        self.assertEqual(response.status, 400)
        response.read()
        connection.close()
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.putrequest("POST", "/choice", skip_host=True)
        connection.putheader("Host", host)
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Content-Length", "2")
        connection.endheaders(b"{}")
        response = connection.getresponse()
        self.assertEqual((response.status, response.getheader("Connection")), (400, "close"))
        response.read()
        connection.close()

    def test_transfer_encoding_and_duplicate_host_are_rejected(self):
        host = f"127.0.0.1:{self.port}"
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.putrequest("POST", "/choice", skip_host=True)
        connection.putheader("Host", host)
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Transfer-Encoding", "chunked")
        connection.endheaders(b"0\r\n\r\n")
        response = connection.getresponse()
        self.assertEqual((response.status, response.getheader("Connection")), (400, "close"))
        response.read()
        connection.close()
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.putrequest("GET", "/participant", skip_host=True)
        connection.putheader("Host", host)
        connection.putheader("Host", host)
        connection.endheaders()
        response = connection.getresponse()
        self.assertEqual((response.status, response.getheader("Connection")), (400, "close"))
        response.read()
        connection.close()
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.putrequest("POST", "/choice", skip_host=True)
        connection.putheader("Host", host)
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Content-Length", "2")
        connection.putheader("Content-Length", "2")
        connection.endheaders(b"{}")
        response = connection.getresponse()
        self.assertEqual(response.status, 400)
        response.read()
        connection.close()

    def test_expired_cancelled_and_cleanup_are_terminal(self):
        capability = self.session.capability
        self.clock.now = 220.0
        body = json.dumps({"capability": capability,
            "choice": ALLOW_DIRECTED_RESPONSE, "mission": FIXTURE_MISSION,
            "action": FIXTURE_ACTION, "participant": FIXTURE_PARTICIPANT})
        status, _, _ = self.request("POST", "/choice", body=body, headers={
            "Host": f"127.0.0.1:{self.port}", "Content-Type": "application/json"})
        self.assertEqual(status, 404)
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.assertFalse(self.thread.is_alive())
        self.session.cancel()
        self.closed = True
        with self.assertRaises(SessionUnavailable):
            _ = self.session.capability
        probe = socket.socket()
        probe.settimeout(1)
        with self.assertRaises(OSError):
            probe.connect(("127.0.0.1", self.port))
        probe.close()

    def test_participant_url_uses_fragment(self):
        url = participant_url(literal_ipv4="192.168.10.4", port=4317,
                              capability="ab" * 32)
        self.assertEqual(url, "http://192.168.10.4:4317/participant#" + "ab" * 32)
        for address, port, capability in (
            ("127.0.0.1", 4317, "ab" * 32),
            ("host.local", 4317, "ab" * 32),
            ("192.168.10.4", True, "ab" * 32),
            ("192.168.10.4", 4317, "AB" * 32),
            ("192.168.10.4", 4317, "z" * 64),
        ):
            with self.assertRaises((GatewayConfigurationError, PackageValidationError)):
                participant_url(literal_ipv4=address, port=port, capability=capability)


if __name__ == "__main__":
    raise SystemExit("run only through the separately reviewed controller")

