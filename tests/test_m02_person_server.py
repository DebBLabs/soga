import json
import http.client
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from m02_person_server import (
    LocalPersonServer,
    PersonServerError,
    SQLitePersonServerStore,
    TokenRejected,
    create_server,
)
from m02_person_server.crypto import encode_hs256
from engines.aauth_execution_runtime_bridge import evaluate_aauth_execution_request


class Clock:
    def __init__(self, now=1_000):
        self.now = now

    def __call__(self):
        return self.now


class M02PersonServerCoreTests(unittest.TestCase):
    issuer = "http://127.0.0.1:38465"
    agent_id = "agent-local-test"
    agent_secret = b"agent-test-secret-material-32-bytes"
    ps_secret = b"person-server-test-secret-32-bytes"
    operator_secret = "operator-test-secret"
    mission_s256 = "mission-s256-local-test"

    def setUp(self):
        self.clock = Clock()
        self.store = SQLitePersonServerStore(":memory:")
        self.service = LocalPersonServer.create_for_local_test(
            store=self.store,
            issuer=self.issuer,
            now=self.clock,
            secret=self.ps_secret,
            operator_secret=self.operator_secret,
        )
        self.service.register_test_agent(
            agent_id=self.agent_id, secret=self.agent_secret
        )
        self.mission = {
            "s256": self.mission_s256,
            "description": "Bounded local M02 test mission",
            "approved_tools": [
                {"name": "greet_participant", "description": "Greet locally"}
            ],
        }
        self.service.retain_mission(
            mission_s256=self.mission_s256, mission=self.mission
        )
        self.token = self.service.issue_person_token(
            subject="person-local-test",
            audience=self.issuer,
            mission_s256=self.mission_s256,
            confirmation={"kid": self.agent_id},
        )

    def tearDown(self):
        self.store.close()

    def request(self, request_id="request-1", **changes):
        value = {
            "request_id": request_id,
            "mission_s256": self.mission_s256,
            "action": "greet_participant",
            "subject": {
                "person_id": "person-local-test",
                "subject_agency_state": "INDEPENDENT",
            },
            "reachability": "REACHABLE",
        }
        value.update(changes)
        return value

    def permission(self, request=None, **changes):
        request = request or self.request()
        values = {
            "request": request,
            "agent_id": self.agent_id,
            "signature": self.service.sign_test_request(
                request=request, secret=self.agent_secret
            ),
            "person_token": self.token,
        }
        values.update(changes)
        return self.service.permission(**values)

    def token_claims(self):
        return self.service.verify_person_token(
            self.token,
            audience=self.issuer,
            mission_s256=self.mission_s256,
            expected_confirmation={"kid": self.agent_id},
        )

    def test_positive_signed_current_bound_request_reaches_soga(self):
        self.assertEqual(
            self.permission(), (200, {"permission": "granted"})
        )
        events = self.store.events()
        decisions = [event for event in events if event["kind"] == "soga_decision"]
        projections = [event for event in events if event["kind"] == "aauth_projection"]
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["payload"]["governance_determination"], "ALLOW")
        self.assertEqual(projections[-1]["payload"]["projection"], "granted")
        self.assertIn("canonical_decision_package", decisions[0]["payload"])

    def test_unsigned_request_is_rejected_before_governance(self):
        with self.assertRaises(TokenRejected):
            self.permission(signature="")
        self.assertFalse(any(e["kind"] == "soga_decision" for e in self.store.events()))

    def test_altered_request_is_rejected_by_signature(self):
        signed = self.request()
        signature = self.service.sign_test_request(
            request=signed, secret=self.agent_secret
        )
        altered = dict(signed, action="different_action")
        with self.assertRaises(TokenRejected):
            self.service.permission(
                request=altered,
                agent_id=self.agent_id,
                signature=signature,
                person_token=self.token,
            )

    def test_wrong_agent_key_is_rejected(self):
        with self.assertRaises(TokenRejected):
            self.permission(
                signature=self.service.sign_test_request(
                    request=self.request(), secret=b"wrong-agent-key-material-32-bytes"
                )
            )

    def test_wrong_token_signature_is_rejected(self):
        claims = self.token_claims()
        forged = encode_hs256(
            claims,
            key_id="m02-local-hs256-1",
            secret=b"wrong-person-server-key-32-bytes",
        )
        with self.assertRaises(TokenRejected):
            self.permission(person_token=forged)

    def test_wrong_issuer_is_rejected(self):
        claims = dict(self.token_claims(), iss="http://127.0.0.1:1")
        forged = encode_hs256(
            claims, key_id="m02-local-hs256-1", secret=self.ps_secret
        )
        with self.assertRaisesRegex(TokenRejected, "issuer"):
            self.permission(person_token=forged)

    def test_wrong_audience_is_rejected(self):
        wrong_audience_token = self.service.issue_person_token(
            subject="person-local-test",
            audience="http://127.0.0.1:38466",
            mission_s256=self.mission_s256,
            confirmation={"kid": self.agent_id},
        )
        with self.assertRaisesRegex(TokenRejected, "audience"):
            self.permission(person_token=wrong_audience_token)

    def test_wrong_agent_confirmation_is_rejected(self):
        self.service.register_test_agent(
            agent_id="agent-other", secret=b"other-agent-secret-material-32bytes"
        )
        request = self.request()
        with self.assertRaisesRegex(TokenRejected, "confirmation"):
            self.service.permission(
                request=request,
                agent_id="agent-other",
                signature=self.service.sign_test_request(
                    request=request,
                    secret=b"other-agent-secret-material-32bytes",
                ),
                person_token=self.token,
            )

    def test_subject_must_match_retained_person_token(self):
        request = self.request(
            subject={
                "person_id": "person-other",
                "subject_agency_state": "INDEPENDENT",
            }
        )
        with self.assertRaisesRegex(TokenRejected, "subject"):
            self.permission(request)

    def test_wrong_mission_binding_is_rejected(self):
        self.service.retain_mission(
            mission_s256="mission-other",
            mission={
                "s256": "mission-other",
                "description": "Different mission",
                "approved_tools": [{"name": "greet_participant"}],
            },
        )
        request = self.request(mission_s256="mission-other")
        with self.assertRaisesRegex(TokenRejected, "mission binding"):
            self.permission(request=request)

    def test_unapproved_action_does_not_receive_permission(self):
        with self.assertRaisesRegex(TokenRejected, "not approved"):
            self.permission(self.request(action="not_in_approved_tools"))

    def test_identical_authenticated_request_retry_is_idempotent(self):
        request = self.request()
        first = self.permission(request)
        self.assertEqual(self.permission(request), first)
        self.assertEqual(
            sum(e["kind"] == "soga_decision" for e in self.store.events()), 1
        )

    def test_conflicting_request_id_reuse_is_rejected(self):
        self.permission(self.request())
        with self.assertRaisesRegex(TokenRejected, "different authenticated content"):
            self.permission(self.request(action="not_in_approved_tools"))

    def test_expired_token_is_rejected_before_governance(self):
        self.clock.now += 301
        with self.assertRaisesRegex(TokenRejected, "expired"):
            self.permission()
        self.assertFalse(any(e["kind"] == "soga_decision" for e in self.store.events()))

    def test_future_issued_token_is_rejected(self):
        claims = dict(self.token_claims(), iat=self.clock.now + 1)
        forged = encode_hs256(
            claims, key_id="m02-local-hs256-1", secret=self.ps_secret
        )
        with self.assertRaisesRegex(TokenRejected, "not yet valid"):
            self.permission(person_token=forged)

    def test_revoked_token_is_rejected_before_governance(self):
        self.service.revoke_person_token(
            token_id=self.token_claims()["jti"], reason="local negative control"
        )
        with self.assertRaisesRegex(TokenRejected, "revoked"):
            self.permission()
        self.assertFalse(any(e["kind"] == "soga_decision" for e in self.store.events()))

    def test_policy_requiring_unavailable_authority_fact_fails_closed(self):
        mission = dict(self.mission)
        mission["policy"] = {"required_authority_facts": ["attenuated"]}
        self.store.close()
        self.store = SQLitePersonServerStore(":memory:")
        self.service = LocalPersonServer.create_for_local_test(
            store=self.store,
            issuer=self.issuer,
            now=self.clock,
            secret=self.ps_secret,
            operator_secret=self.operator_secret,
        )
        self.service.register_test_agent(agent_id=self.agent_id, secret=self.agent_secret)
        self.service.retain_mission(mission_s256=self.mission_s256, mission=mission)
        self.token = self.service.issue_person_token(
            subject="person-local-test", audience=self.issuer,
            mission_s256=self.mission_s256, confirmation={"kid": self.agent_id}
        )
        with self.assertRaisesRegex(TokenRejected, "unavailable"):
            self.permission()

    def test_verified_retained_state_reaches_b038_runtime_input(self):
        self.permission()
        decision = next(
            event["payload"]
            for event in self.store.events()
            if event["kind"] == "soga_decision"
        )
        runtime_authority = decision["canonical_decision_package"]["authority_inputs"]
        self.assertEqual(
            runtime_authority["additional_inputs"]["live_input_source"],
            "retained-person-token",
        )
        self.assertEqual(
            runtime_authority["additional_inputs"]["authority_id"],
            self.token_claims()["jti"],
        )

    def approval_evidence(self, pending_id):
        pending = self.store.pending(pending_id)
        evidence = {
            "pending_id": pending["pending_id"],
            "request_id": pending["request_id"],
            "mission_s256": pending["mission_s256"],
            "action": pending["action"],
            "agent_id": pending["agent_id"],
            "holder_attribution_asserted": True,
        }
        restrict_mode = pending["decision"]["governance_decision"].get("restrict_mode")
        constraint = restrict_mode.get("constraint", {}) if isinstance(restrict_mode, dict) else {}
        for name in ("constraint_reference", "required_evidence"):
            if constraint.get(name) is not None:
                evidence[name] = constraint[name]
        return evidence

    def test_approval_requires_exact_pending_binding(self):
        status, body = self.permission(
            self.request(
                subject={
                    "person_id": "person-local-test",
                    "subject_agency_state": "SUPERVISED",
                }
            )
        )
        self.assertEqual(status, 202)
        evidence = self.approval_evidence(body["pending_id"])
        evidence["mission_s256"] = "mission-wrong"
        with self.assertRaisesRegex(TokenRejected, "wrong mission_s256 binding"):
            self.service.resolve_pending(
                pending_id=body["pending_id"], result="approve",
                approval_evidence=evidence,
            )

    def test_approval_evidence_causes_reevaluation_not_direct_grant(self):
        status, body = self.permission(
            self.request(
                subject={
                    "person_id": "person-local-test",
                    "subject_agency_state": "SUPERVISED",
                }
            )
        )
        self.assertEqual(status, 202)
        result = self.service.resolve_pending(
            pending_id=body["pending_id"], result="approve",
            approval_evidence=self.approval_evidence(body["pending_id"]),
        )
        self.assertIn(result[1]["permission"], {"granted", "denied"})
        decisions = [e for e in self.store.events() if e["kind"] == "soga_decision"]
        self.assertEqual(len(decisions), 2)
        self.assertTrue(
            decisions[-1]["payload"]["runtime_envelope"]["request_id"].endswith(
                "-reevaluation"
            )
        )

    def test_reevaluation_rejects_subject_changed_in_retained_authority(self):
        status, body = self.permission(
            self.request(
                subject={
                    "person_id": "person-local-test",
                    "subject_agency_state": "SUPERVISED",
                }
            )
        )
        self.assertEqual(status, 202)
        token_id = self.token_claims()["jti"]
        with self.store.transaction() as connection:
            connection.execute(
                "UPDATE tokens SET subject = ? WHERE token_id = ?",
                ("different-retained-subject", token_id),
            )
        with self.assertRaisesRegex(
            TokenRejected, "pending subject no longer matches retained authority"
        ):
            self.service.resolve_pending(
                pending_id=body["pending_id"],
                result="approve",
                approval_evidence=self.approval_evidence(body["pending_id"]),
            )

    def test_terminal_poll_delivers_exact_final_permission_once_then_gone(self):
        status, body = self.permission(
            self.request(
                subject={
                    "person_id": "person-local-test",
                    "subject_agency_state": "SUPERVISED",
                }
            )
        )
        self.assertEqual(status, 202)
        final = self.service.resolve_pending(
            pending_id=body["pending_id"], result="decline"
        )
        first_poll = {
            "request_id": "poll-terminal-1",
            "pending_id": body["pending_id"],
        }
        self.assertEqual(
            self.service.poll_pending(
                pending_id=body["pending_id"],
                request=first_poll,
                agent_id=self.agent_id,
                signature=self.service.sign_test_request(
                    request=first_poll, secret=self.agent_secret
                ),
            ),
            final,
        )
        second_poll = {
            "request_id": "poll-terminal-2",
            "pending_id": body["pending_id"],
        }
        self.assertEqual(
            self.service.poll_pending(
                pending_id=body["pending_id"],
                request=second_poll,
                agent_id=self.agent_id,
                signature=self.service.sign_test_request(
                    request=second_poll, secret=self.agent_secret
                ),
            ),
            (410, {"error": "gone"}),
        )

    def test_expired_pending_poll_delivers_408_once_then_gone(self):
        status, body = self.permission(
            self.request(
                subject={
                    "person_id": "person-local-test",
                    "subject_agency_state": "SUPERVISED",
                }
            )
        )
        self.assertEqual(status, 202)
        self.clock.now += 61
        first_poll = {
            "request_id": "poll-expired-1",
            "pending_id": body["pending_id"],
        }
        self.assertEqual(
            self.service.poll_pending(
                pending_id=body["pending_id"], request=first_poll,
                agent_id=self.agent_id,
                signature=self.service.sign_test_request(
                    request=first_poll, secret=self.agent_secret
                ),
            ),
            (408, {"error": "expired"}),
        )
        second_poll = {
            "request_id": "poll-expired-2",
            "pending_id": body["pending_id"],
        }
        self.assertEqual(
            self.service.poll_pending(
                pending_id=body["pending_id"], request=second_poll,
                agent_id=self.agent_id,
                signature=self.service.sign_test_request(
                    request=second_poll, secret=self.agent_secret
                ),
            ),
            (410, {"error": "gone"}),
        )

    def test_bridge_centrally_fails_closed_for_required_unavailable_authority_fact(self):
        execution_request = {
            "request_id": "bridge-unavailable-1",
            "action": "greet_participant",
            "mission": {
                "mission_id": self.mission_s256,
                "allowed_actions": ["greet_participant"],
            },
            "authority": {
                "authority_id": self.token_claims()["jti"],
                "allowed_actions": ["greet_participant"],
            },
            "subject": {
                "subject_id": "person-local-test",
                "subject_agency_state": "INDEPENDENT",
                "reachability": "REACHABLE",
            },
            "policy": {"required_authority_facts": ["attenuated"]},
        }
        verified = {
            "revoked": False,
            "expired": False,
            "delegation_hops": 0,
            "max_delegation_hops": 0,
            "elapsed_seconds": 0,
            "max_elapsed_seconds": 3600,
            "attenuated": False,
            "unavailable": ["attenuated"],
            "source": "direct-test-verified-state",
            "observed_at": self.clock.now,
        }
        with self.assertRaisesRegex(
            ValueError, "required verified authority facts are unavailable: attenuated"
        ):
            evaluate_aauth_execution_request(
                execution_request, verified_authority_state=verified
            )

    def test_late_approval_cannot_revive_revoked_authority(self):
        request = self.request(
            subject={
                "person_id": "person-local-test",
                "subject_agency_state": "SUPERVISED",
            }
        )
        status, body = self.permission(request)
        self.assertEqual(status, 202)
        self.service.revoke_person_token(
            token_id=self.token_claims()["jti"], reason="revoked while pending"
        )
        with self.assertRaisesRegex(TokenRejected, "revoked while permission was pending"):
            self.service.resolve_pending(
                pending_id=body["pending_id"],
                result="approve",
                approval_evidence=self.approval_evidence(body["pending_id"]),
            )
        self.assertNotEqual(self.store.pending(body["pending_id"])["state"], "granted")

    def test_late_approval_cannot_revive_expired_pending(self):
        request = self.request(
            subject={
                "person_id": "person-local-test",
                "subject_agency_state": "SUPERVISED",
            }
        )
        status, body = self.permission(request)
        self.assertEqual(status, 202)
        self.clock.now += 61
        self.assertEqual(
            self.service.resolve_pending(
                pending_id=body["pending_id"],
                result="approve",
                approval_evidence={"holder_attribution_asserted": True},
            ),
            (408, {"error": "expired"}),
        )

    def test_sqlite_state_survives_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "person-server.sqlite3"
            first_store = SQLitePersonServerStore(path)
            first = LocalPersonServer.create_for_local_test(
                store=first_store,
                issuer=self.issuer,
                now=self.clock,
                secret=self.ps_secret,
                operator_secret=self.operator_secret,
            )
            first.register_test_agent(agent_id=self.agent_id, secret=self.agent_secret)
            first.retain_mission(mission_s256=self.mission_s256, mission=self.mission)
            token = first.issue_person_token(
                subject="person-local-test", audience=self.issuer,
                mission_s256=self.mission_s256, confirmation={"kid": self.agent_id}
            )
            first_store.close()
            reopened_store = SQLitePersonServerStore(path)
            try:
                reopened = LocalPersonServer(
                    store=reopened_store,
                    issuer=self.issuer,
                    now=self.clock,
                    operator_secret=self.operator_secret,
                )
                self.assertEqual(
                    reopened.store.mission(self.mission_s256)["s256"],
                    self.mission_s256,
                )
                self.assertEqual(
                    reopened.verify_person_token(
                        token, audience=self.issuer,
                        mission_s256=self.mission_s256,
                        expected_confirmation={"kid": self.agent_id},
                    )["sub"],
                    "person-local-test",
                )
            finally:
                reopened_store.close()

    def test_concurrent_revocation_has_one_authoritative_winner(self):
        token_id = self.token_claims()["jti"]
        barrier = threading.Barrier(8)
        results = []
        lock = threading.Lock()

        def revoke(index):
            barrier.wait()
            changed = self.service.revoke_person_token(
                token_id=token_id, reason=f"concurrent-{index}"
            )
            with lock:
                results.append(changed)

        threads = [threading.Thread(target=revoke, args=(index,)) for index in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(results.count(True), 1)
        self.assertEqual(
            sum(e["kind"] == "person_token_revoked" for e in self.store.events()), 1
        )

    def test_concurrent_identical_permission_has_one_soga_decision(self):
        request = self.request()
        signature = self.service.sign_test_request(
            request=request, secret=self.agent_secret
        )
        barrier = threading.Barrier(8)
        responses = []
        errors = []
        lock = threading.Lock()

        def submit():
            barrier.wait()
            try:
                result = self.service.permission(
                    request=request,
                    agent_id=self.agent_id,
                    signature=signature,
                    person_token=self.token,
                )
                with lock:
                    responses.append(result)
            except Exception as error:  # retained for an actionable assertion
                with lock:
                    errors.append(error)

        threads = [threading.Thread(target=submit) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(responses) + len(errors), 8)
        self.assertGreaterEqual(len(responses), 1)
        self.assertTrue(
            all(response == (200, {"permission": "granted"}) for response in responses)
        )
        self.assertTrue(
            all(
                isinstance(error, PersonServerError)
                and str(error) == "identical request is still being evaluated"
                for error in errors
            )
        )
        self.assertEqual(
            self.permission(request), (200, {"permission": "granted"})
        )
        self.assertEqual(
            sum(e["kind"] == "soga_decision" for e in self.store.events()), 1
        )

    def test_audit_excludes_raw_token_and_test_secrets(self):
        self.permission()
        rendered = json.dumps(self.store.events(), sort_keys=True)
        self.assertNotIn(self.token, rendered)
        self.assertNotIn(self.ps_secret.decode(), rendered)
        self.assertNotIn(self.agent_secret.decode(), rendered)
        self.assertNotIn(self.operator_secret, rendered)

    def test_package_has_no_wallet_misty_or_physical_execution_import(self):
        package = Path(__file__).parents[1] / "m02_person_server"
        source = "\n".join(path.read_text() for path in package.glob("*.py")).lower()
        for forbidden in (
            "freewallet", "wallet_attached", "was-teaching", "misty",
            "physical_outcome", "g27_tip_jar", "m01_",
        ):
            self.assertNotIn(forbidden, source)


class M02PersonServerHTTPTests(unittest.TestCase):
    agent_id = "agent-http-test"
    agent_secret = b"agent-http-test-secret-32-bytes"
    operator_secret = "operator-http-test-secret"
    mission_s256 = "mission-http-test"

    def setUp(self):
        self.clock = Clock()
        self.store = SQLitePersonServerStore(":memory:")
        self.service = LocalPersonServer.create_for_local_test(
            store=self.store,
            issuer="http://127.0.0.1",
            now=self.clock,
            secret=b"person-http-test-secret-32bytes",
            operator_secret=self.operator_secret,
        )
        self.service.register_test_agent(agent_id=self.agent_id, secret=self.agent_secret)
        self.service.retain_mission(
            mission_s256=self.mission_s256,
            mission={
                "s256": self.mission_s256,
                "description": "HTTP boundary test",
                "approved_tools": [{"name": "greet_participant"}],
            },
        )
        self.token = self.service.issue_person_token(
            subject="person-http-test",
            audience=self.service.issuer,
            mission_s256=self.mission_s256,
            confirmation={"kid": self.agent_id},
        )
        self.server = create_server(self.service, host="127.0.0.1", port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.store.close()

    def request(self, request_id="http-request-1", state="INDEPENDENT", **changes):
        request = {
            "request_id": request_id,
            "mission_s256": self.mission_s256,
            "action": "greet_participant",
            "subject": {
                "person_id": "person-http-test",
                "subject_agency_state": state,
            },
            "reachability": "REACHABLE",
        }
        request.update(changes)
        return request

    def permission_body(self, request=None):
        request = request or self.request()
        return {
            "request": request,
            "agent_id": self.agent_id,
            "signature": self.service.sign_test_request(
                request=request, secret=self.agent_secret
            ),
            "person_token": self.token,
        }

    def http(self, method, path, body=None, headers=None):
        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(
            f"{self.base}{path}", data=data, method=method,
            headers=headers or ({"Content-Type": "application/json"} if data else {}),
        )
        try:
            with urllib.request.urlopen(request, timeout=2) as response:
                return response.status, dict(response.headers), json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, dict(error.headers), json.load(error)

    def test_http_positive_request_crosses_real_loopback_into_soga(self):
        status, headers, body = self.http(
            "POST", "/permission", self.permission_body()
        )
        self.assertEqual((status, body), (200, {"permission": "granted"}))
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertTrue(any(e["kind"] == "soga_decision" for e in self.store.events()))

    def test_http_magic_header_authenticates_nothing(self):
        body = self.permission_body()
        body["signature"] = "invalid"
        status, _, response = self.http(
            "POST", "/permission", body,
            {"Content-Type": "application/json", "G26-PS-Assertion": "authenticated"},
        )
        self.assertEqual(status, 401)
        self.assertEqual(response["error"], "invalid_token")

    def test_http_pending_poll_requires_signed_agent_binding(self):
        status, _, pending = self.http(
            "POST", "/permission",
            self.permission_body(self.request(state="SUPERVISED")),
        )
        self.assertEqual(status, 202)
        poll = {"request_id": "poll-request-1", "pending_id": pending["pending_id"]}
        unsigned = {
            "request": poll, "agent_id": self.agent_id, "signature": "invalid"
        }
        self.assertEqual(
            self.http("POST", f"{pending['pending_url']}/poll", unsigned)[0], 401
        )
        signed = dict(
            unsigned,
            signature=self.service.sign_test_request(
                request=poll, secret=self.agent_secret
            ),
        )
        status, _, response = self.http(
            "POST", f"{pending['pending_url']}/poll", signed
        )
        self.assertEqual((status, response["status"]), (202, "pending"))

    def test_http_terminal_poll_delivers_final_permission_once_then_gone(self):
        status, _, pending = self.http(
            "POST", "/permission",
            self.permission_body(self.request(state="SUPERVISED")),
        )
        self.assertEqual(status, 202)
        status, _, final = self.http(
            "POST",
            f"/_test/pending/{pending['pending_id']}/approval",
            {"result": "decline"},
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.operator_secret}",
            },
        )
        self.assertEqual((status, final), (200, {"permission": "denied", "reason": "approval declined"}))

        first = {"request_id": "http-terminal-poll-1", "pending_id": pending["pending_id"]}
        first_body = {
            "request": first,
            "agent_id": self.agent_id,
            "signature": self.service.sign_test_request(
                request=first, secret=self.agent_secret
            ),
        }
        status, _, delivered = self.http(
            "POST", f"{pending['pending_url']}/poll", first_body
        )
        self.assertEqual((status, delivered), (200, final))

        second = {"request_id": "http-terminal-poll-2", "pending_id": pending["pending_id"]}
        second_body = {
            "request": second,
            "agent_id": self.agent_id,
            "signature": self.service.sign_test_request(
                request=second, secret=self.agent_secret
            ),
        }
        status, _, gone = self.http(
            "POST", f"{pending['pending_url']}/poll", second_body
        )
        self.assertEqual((status, gone), (410, {"error": "gone"}))

    def test_http_operator_routes_require_operator_bearer(self):
        status, _, body = self.http(
            "POST", "/_test/tokens/revoke", {"token_id": "anything", "reason": "test"}
        )
        self.assertEqual(status, 401)
        self.assertEqual(body["error"], "invalid_token")

    def test_http_setup_and_mutation_routes_are_test_namespaced(self):
        payload = {"agent_id": "new-agent", "secret": "new-agent-secret-32-bytes"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.operator_secret}",
        }
        self.assertEqual(self.http("POST", "/agents", payload, headers)[0], 404)
        self.assertEqual(self.http("POST", "/_test/agents", payload, headers)[0], 201)

    def test_http_wrong_content_type_is_rejected(self):
        status, _, body = self.http(
            "POST", "/permission", self.permission_body(), {"Content-Type": "text/plain"}
        )
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "invalid_request")

    def test_http_malformed_json_is_rejected(self):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        connection.request(
            "POST", "/permission", body=b"{bad", headers={"Content-Type": "application/json"}
        )
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
        self.assertEqual(response.status, 400)
        self.assertEqual(payload["error"], "invalid_request")

    def test_http_non_object_json_is_rejected(self):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        connection.request(
            "POST", "/permission", body=b"[]", headers={"Content-Type": "application/json"}
        )
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
        self.assertEqual(response.status, 400)
        self.assertEqual(payload["error"], "invalid_request")

    def test_http_oversized_declared_body_is_rejected_without_read(self):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        connection.putrequest("POST", "/permission")
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Content-Length", "1000001")
        connection.endheaders()
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
        self.assertEqual(response.status, 400)
        self.assertEqual(payload["error"], "invalid_request")

    def test_http_unknown_security_field_is_rejected(self):
        request = self.request(representative_authority={"claim": "unverified"})
        status, _, body = self.http(
            "POST", "/permission", self.permission_body(request)
        )
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "invalid_request")

    def test_http_unsupported_method_and_route_have_no_redirect_or_fallback(self):
        self.assertEqual(self.http("GET", "/permission")[0], 404)
        status, headers, _ = self.http("GET", "/not-a-route")
        self.assertEqual(status, 404)
        self.assertNotIn("Location", headers)

    def test_create_server_rejects_hostname_and_nonloopback_without_binding(self):
        for host in ("localhost", "0.0.0.0", "192.0.2.10"):
            with self.subTest(host=host), self.assertRaises(ValueError):
                create_server(self.service, host=host, port=0)


if __name__ == "__main__":
    unittest.main()
