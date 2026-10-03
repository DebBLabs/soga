"""Tests for the additive AAuth requirement=approval pending lifecycle."""

import hashlib
import http.client
import json
from pathlib import Path
import threading
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from m02_aauth_fcf656d import jose
from m02_aauth_fcf656d.approval_pending import (
    MAX_PENDING_RECORDS, PENDING_LIFETIME_SECONDS, ApprovalPendingClient,
    ApprovalPendingStore, ApprovalPendingSurface, create_approval_pending_server,
    signed_poll,
)
from m02_aauth_fcf656d.exchange import Mission, PersonServer, signed_post
from m02_aauth_fcf656d.localhost import (
    LocalAgentClient, PersonServerSurface, TransportMap, create_server,
)
from m02_aauth_fcf656d.other_party_approval import (
    AMBIENT_SCOPE, DIRECTED_SCOPE, ApprovalGovernedResource,
    OtherPartyApprovalPolicy, OtherPartyApprovalReceipt,
)
from m02_aauth_fcf656d.soga_supervision import SogaSupervisionProfile, SogaSupervisor
from m02_aauth_fcf656d.tokens import Issuer, issue_agent_token


NOW = 1_000_000
AP = "https://agent.example"
PS = "https://ps.example"
RESOURCE = "https://resource.example"
AGENT = "aauth:misty-tipjar@agent.example"
MISSION = "mission-sha256"
SUBJECT = "directed-person-1"
PARTICIPANT = "participant-test-1"


class Clock:
    def __init__(self, value=NOW):
        self.value = value
        self.lock = threading.Lock()

    def __call__(self):
        with self.lock:
            return self.value

    def advance(self, seconds=1):
        with self.lock:
            self.value += seconds
            return self.value


def authority_state():
    return {
        "revoked": False, "expired": False, "delegation_hops": 0,
        "max_delegation_hops": 0, "elapsed_seconds": 0,
        "max_elapsed_seconds": 1800, "attenuated": False,
        "source": "m02-approval-pending-reviewed-test-profile",
        "observed_at": NOW, "unavailable": ["revoked", "attenuated"],
    }


def supervision_profile():
    return SogaSupervisionProfile.create(
        verified_authority_state=authority_state(), required_authority_facts=(),
        subject_governance_state="INDEPENDENT", reachability="REACHABLE",
        subject_state_source="declared-test-profile-policy",
        reachability_source="declared-test-profile-policy")


class ApprovalPendingTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.next_id = 0

        def identifier():
            self.next_id += 1
            return format(self.next_id, "032d")

        self.ap = Issuer(AP, "aauth-agent.json", "ap-key", Ed25519PrivateKey.generate())
        self.ps = Issuer(PS, "aauth-person.json", "ps-key", Ed25519PrivateKey.generate())
        self.resource_issuer = Issuer(
            RESOURCE, "aauth-resource.json", "resource-key", Ed25519PrivateKey.generate())
        self.agent_private = Ed25519PrivateKey.generate()
        self.agent_jwk = jose.public_jwk(self.agent_private.public_key(), "agent-key")
        self.agent_token = issue_agent_token(
            self.ap, agent_id=AGENT, ps=PS, agent_jwk=self.agent_jwk,
            now=NOW, expires=NOW + 7200, jti="agent-1")
        self.supervisor = SogaSupervisor(supervision_profile())
        self.person_server = PersonServer(
            issuer=self.ps, agent_provider=self.ap, resource=self.resource_issuer,
            directed_subject=SUBJECT,
            missions={MISSION: Mission(MISSION, AGENT, NOW + 1800)},
            supervisor=self.supervisor, now=NOW)
        self.policy = OtherPartyApprovalPolicy()
        self.resource = ApprovalGovernedResource(
            issuer=self.resource_issuer, person_server=self.ps, now=NOW,
            approval_policy=self.policy)
        self.store = ApprovalPendingStore(clock=self.clock, id_factory=identifier)
        self.ps_server = create_server(PersonServerSurface(person_server=self.person_server))
        self.resource_server = create_approval_pending_server(ApprovalPendingSurface(
            resource=self.resource, subject=SUBJECT, mission_s256=MISSION,
            store=self.store))
        self.threads = [
            threading.Thread(target=self.ps_server.serve_forever),
            threading.Thread(target=self.resource_server.serve_forever),
        ]
        for thread in self.threads:
            thread.start()
        self.mapping = TransportMap(
            person_server=PS, resource=RESOURCE,
            mappings={PS: "http://127.0.0.1:" + str(self.ps_server.server_port),
                      RESOURCE: "http://127.0.0.1:" + str(self.resource_server.server_port)})
        self.client = LocalAgentClient(self.mapping)
        self.poll_client = ApprovalPendingClient(self.mapping)

    def tearDown(self):
        for server in (self.ps_server, self.resource_server):
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join(timeout=2)
            self.assertFalse(thread.is_alive())

    def signed(self, role, path, body, token=None):
        return signed_post(
            self.mapping.authority(role), path, body, token or self.agent_token,
            self.agent_private, self.clock())

    def send(self, role, path, body, token=None):
        return self.client.send(
            role=role, path=path, request=self.signed(role, path, body, token))

    def auth_token(self, scope=DIRECTED_SCOPE):
        status, _, person = self.send(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        self.assertEqual(status, 200)
        status, _, resource = self.send(
            RESOURCE, "/authorize", {"scope": scope}, person["person_token"])
        self.assertEqual(status, 200)
        status, _, auth = self.send(
            PS, "/auth-token",
            {"resource_token": resource["resource_token"],
             "presented_token": person["person_token"],
             "justification": "bounded participant response"})
        self.assertEqual(status, 200)
        return auth["auth_token"]

    def begin(self, token=None, participant=PARTICIPANT):
        active = token or self.auth_token()
        status, headers, body = self.send(
            RESOURCE, "/enforce",
            {"participant": participant, "scope": DIRECTED_SCOPE}, active)
        return active, status, headers, body

    def poll(self, path, token, *, created=None, private_key=None):
        when = self.clock() if created is None else created
        request = signed_poll(
            self.mapping.authority(RESOURCE), path, token,
            private_key or self.agent_private, when)
        return self.poll_client.poll(role=RESOURCE, path=path, request=request)

    def receipt(self, *, participant=PARTICIPANT, mission=MISSION,
                state="APPROVED", observed=None, expires=None):
        now = self.clock()
        return OtherPartyApprovalReceipt.create({
            "receipt_id": "receipt-test-1", "asserted_role": "parent",
            "assurance": "unverified-demo-input", "participant": participant,
            "mission_s256": mission, "scope": DIRECTED_SCOPE, "state": state,
            "observed_at": now - 1 if observed is None else observed,
            "expires_at": now + 60 if expires is None else expires,
            "source": "local-out-of-band-test-fixture",
        })

    def pending_id(self, location):
        return location.rsplit("/", 1)[1]

    def test_01_initial_response_has_exact_approval_contract(self):
        _, status, headers, body = self.begin()
        self.assertEqual(status, 202)
        self.assertEqual(body, {"status": "pending"})
        self.assertEqual(headers["AAuth-Requirement"], "requirement=approval")
        self.assertRegex(headers["Location"], r"^/pending/[A-Za-z0-9_-]{32}$")
        self.assertEqual(headers["Retry-After"], "0")
        self.assertEqual(headers["Cache-Control"], "no-store")

        status, _, person = self.send(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        self.assertEqual(status, 200)
        status, _, resource = self.send(
            RESOURCE, "/authorize", {"scope": DIRECTED_SCOPE}, person["person_token"])
        self.assertEqual(status, 200)
        status, challenge_headers, challenge = self.send(
            RESOURCE, "/enforce",
            {"participant": PARTICIPANT, "scope": DIRECTED_SCOPE},
            person["person_token"])
        self.assertEqual((status, challenge), (401, {"error": "auth_token_required"}))
        self.assertIn("requirement=auth-token", challenge_headers["AAuth-Requirement"])
        self.assertIn(resource["resource_token"], challenge_headers["AAuth-Requirement"])

    def test_02_ambient_action_creates_no_pending_record(self):
        token = self.auth_token(AMBIENT_SCOPE)
        status, _, body = self.send(
            RESOURCE, "/enforce",
            {"participant": PARTICIPANT, "scope": AMBIENT_SCOPE}, token)
        self.assertEqual(status, 200)
        self.assertIsNone(body["decision"])
        self.assertEqual(self.store.count, 0)
        self.assertEqual(self.policy.calls, 0)

    def test_03_same_token_and_key_observe_pending(self):
        token, _, headers, _ = self.begin()
        status, polled_headers, body = self.poll(headers["Location"], token)
        self.assertEqual((status, body), (202, {"status": "pending"}))
        self.assertEqual(polled_headers["Location"], headers["Location"])
        self.assertEqual(polled_headers["Retry-After"], "0")

    def test_04_poll_is_bodyless_real_get(self):
        token, _, headers, _ = self.begin()
        request = signed_poll(
            self.mapping.authority(RESOURCE), headers["Location"], token,
            self.agent_private, self.clock())
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.body, b"")
        self.assertNotIn("content-length", request.headers)
        self.assertNotIn("content-type", request.headers)
        self.assertEqual(self.poll_client.poll(
            role=RESOURCE, path=headers["Location"], request=request)[0], 202)

        host, port = self.mapping.destination(RESOURCE)
        connection = http.client.HTTPConnection(host, port, timeout=2)
        connection.request("GET", headers["Location"], body=b"x", headers={
            "Content-Length": "1", "Signature-Key": "x",
            "Signature-Input": "x", "Signature": "x",
        })
        response = connection.getresponse()
        self.assertEqual(response.status, 400)
        self.assertEqual(response.getheader("Connection"), "close")
        response.read()
        self.assertIsNone(connection.sock)
        connection.close()

    def test_05_active_exact_approval_completes_once(self):
        self.policy.replace(self.receipt())
        _, status, _, body = self.begin()
        self.assertEqual(status, 200)
        self.assertEqual(body["decision"]["reason"], "approval_active")
        self.assertEqual(self.store.count, 0)
        self.policy.replace(None)
        token, _, headers, _ = self.begin()
        self.store.resolve(self.pending_id(headers["Location"]), self.receipt())
        status, _, body = self.poll(headers["Location"], token)
        self.assertEqual(status, 200)
        self.assertEqual(body["authorization"], "allowed")
        self.assertEqual(body["decision"]["approval_assurance"],
                         "unverified-demo-input")

    def test_06_withdrawn_decision_is_terminal_denial(self):
        token, _, headers, _ = self.begin()
        self.store.resolve(
            self.pending_id(headers["Location"]), self.receipt(state="WITHDRAWN"))
        status, _, body = self.poll(headers["Location"], token)
        self.assertEqual(status, 403)
        self.assertEqual(body["decision"]["reason"], "approval_withdrawn")

    def test_07_pending_expiry_returns_408_before_auth_expiry(self):
        token, _, headers, _ = self.begin()
        self.clock.advance(PENDING_LIFETIME_SECONDS)
        status, _, body = self.poll(headers["Location"], token)
        self.assertEqual((status, body), (408, {"error": "expired"}))

    def test_08_terminal_poll_returns_410_without_recompletion(self):
        token, _, headers, _ = self.begin()
        self.store.resolve(self.pending_id(headers["Location"]), self.receipt())
        self.assertEqual(self.poll(headers["Location"], token)[0], 200)
        self.clock.advance()
        self.assertEqual(self.poll(headers["Location"], token)[0], 410)

    def test_09_unknown_and_wrong_key_are_indistinguishable(self):
        token, _, headers, _ = self.begin()
        unknown = "/pending/" + "9" * 32
        unknown_result = self.poll(unknown, token)
        wrong_request = signed_poll(
            self.mapping.authority(RESOURCE), headers["Location"], token,
            Ed25519PrivateKey.generate(), self.clock())
        wrong_result = self.poll_client.poll(
            role=RESOURCE, path=headers["Location"], request=wrong_request)
        self.assertEqual(unknown_result[0], 404)
        self.assertEqual(wrong_result[0], 404)
        self.assertEqual(unknown_result[2], wrong_result[2])
        for name in ("Content-Type", "Cache-Control", "Content-Length"):
            self.assertEqual(unknown_result[1][name], wrong_result[1][name])

    def test_10_signature_failures_and_fresh_later_poll(self):
        token, _, headers, _ = self.begin()
        path = headers["Location"]
        request = signed_poll(
            self.mapping.authority(RESOURCE), path, token,
            self.agent_private, self.clock())
        self.assertEqual(self.poll_client.poll(
            role=RESOURCE, path=path, request=request)[0], 202)
        self.assertEqual(self.poll_client.poll(
            role=RESOURCE, path=path, request=request)[0], 404)
        self.clock.advance()
        self.assertEqual(self.poll(path, token)[0], 202)
        self.assertEqual(self.poll(path, token, created=NOW - 1000)[0], 404)

        host, port = self.mapping.destination(RESOURCE)
        cases = (
            {},
            {"Signature-Key": "malformed", "Signature-Input": "malformed",
             "Signature": "malformed"},
            {"Signature-Key": "x" * 16385, "Signature-Input": "x",
             "Signature": "x"},
        )
        for headers_to_send in cases:
            with self.subTest(headers=headers_to_send):
                connection = http.client.HTTPConnection(host, port, timeout=2)
                connection.request("GET", path, headers=headers_to_send)
                response = connection.getresponse()
                self.assertIn(response.status, {400, 401})
                self.assertEqual(response.getheader("Connection"), "close")
                response.read()
                connection.close()

        raw = ("GET " + path + " HTTP/1.1\r\nHost: resource.example\r\n"
               "Signature-Key: x\r\nSignature-Key: y\r\n"
               "Signature-Input: x\r\nSignature: x\r\nConnection: close\r\n\r\n")
        import socket
        with socket.create_connection((host, port), timeout=2) as duplicate:
            duplicate.sendall(raw.encode("ascii"))
            self.assertIn(b" 401 ", duplicate.recv(4096))

    def test_11_receipt_binding_and_time_mismatches_deny(self):
        cases = (
            self.receipt(participant="participant-test-2"),
            self.receipt(mission="other-mission"),
            self.receipt(observed=NOW + 10),
            self.receipt(expires=NOW),
        )
        for candidate in cases:
            with self.subTest(candidate=candidate):
                token, _, headers, _ = self.begin()
                self.store.resolve(self.pending_id(headers["Location"]), candidate)
                self.assertEqual(self.poll(headers["Location"], token)[0], 403)

    def test_12_concurrency_atomicity_isolation_and_capacity(self):
        token = self.auth_token()
        records = [self.begin(token)[2]["Location"] for _ in range(MAX_PENDING_RECORDS)]
        self.assertEqual(self.begin(token)[1], 503)
        self.store.resolve(self.pending_id(records[0]), self.receipt())
        results = []

        def poll_once(created):
            results.append(self.poll(records[0], token, created=created)[0])

        workers = [threading.Thread(target=poll_once, args=(NOW + offset,))
                   for offset in (1, 2)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=2)
            self.assertFalse(worker.is_alive())
        self.assertEqual(sorted(results), [200, 410])
        self.assertEqual(self.poll(records[1], token, created=NOW + 3)[0], 202)

    def test_13_soga_failure_prevents_pending_lifecycle(self):
        for outcome in ("DENY", "RESTRICT", "MALFORMED", ValueError("failure")):
            def evaluator(*_args, selected=outcome, **_kwargs):
                if isinstance(selected, Exception):
                    raise selected
                if selected == "MALFORMED":
                    return {}
                return {
                    "governance_determination": selected,
                    "governance_decision": {"step_id": "decision-test"},
                    "canonical_decision_package": {"decision": selected},
                }
            self.person_server.supervisor = SogaSupervisor(
                supervision_profile(), evaluator=evaluator)
            status, _, person = self.send(
                PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
            self.assertEqual(status, 200)
            status, _, resource = self.send(
                RESOURCE, "/authorize", {"scope": DIRECTED_SCOPE},
                person["person_token"])
            self.assertEqual(status, 200)
            status, _, body = self.send(
                PS, "/auth-token",
                {"resource_token": resource["resource_token"],
                 "presented_token": person["person_token"], "justification": "test"})
            self.assertEqual(status, 403)
            self.assertNotIn("auth_token", body)
            self.assertEqual(self.store.count, 0)

    def test_14_agent_has_no_decision_route(self):
        before = self.store.count
        status, _, _ = self.send(
            RESOURCE, "/approval", {"pending_id": "1" * 32, "state": "APPROVED"})
        self.assertEqual(status, 404)
        self.assertEqual(self.store.count, before)

    def test_15_d132_sources_remain_byte_identical(self):
        root = Path(__file__).resolve().parents[1]
        expected = {
            "m02_aauth_fcf656d/other_party_approval.py":
                "c5a244da3ef5e6694df663af2ff0fb5cd83cdf928fa49c1ab708b197c35d78b0",
            "tests/test_m02_aauth_other_party_approval.py":
                "a24e5f76832a5b8df7e9ed67409c18b03ce4a2b773103d813285048019e30a66",
            "tools/m02_aauth_fcf656d/run_other_party_approval_tests.py":
                "b0fa483f3ab0ea343de847b8b4acb78096afc81bd81d3f69b0206ef579a3bdc1",
        }
        for relative, digest in expected.items():
            self.assertEqual(hashlib.sha256((root / relative).read_bytes()).hexdigest(), digest)

    def test_16_pending_lifetime_is_bounded_by_auth_token_and_clock(self):
        status, _, person = self.send(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        self.assertEqual(status, 200)
        token, _, headers, _ = self.begin()
        record = self.store._record(headers["Location"])
        claims = jose.verify_compact(token, "aa-auth+jwt", self.ps.jwks)
        self.assertEqual(record.created_at, self.clock())
        self.assertEqual(record.expires_at - record.created_at,
                         PENDING_LIFETIME_SECONDS)
        self.assertLess(record.expires_at, claims["exp"])

        self.clock.advance(61)
        status, _, resource = self.send(
            RESOURCE, "/authorize", {"scope": DIRECTED_SCOPE}, person["person_token"])
        self.assertEqual(status, 200)
        resource_claims = jose.verify_compact(
            resource["resource_token"], "aa-resource+jwt", self.resource_issuer.jwks)
        self.assertEqual(resource_claims["iat"], self.clock())
        status, _, body = self.send(
            RESOURCE, "/enforce",
            {"participant": "participant-clock", "scope": DIRECTED_SCOPE}, token)
        self.assertEqual((status, body), (202, {"status": "pending"}))


if __name__ == "__main__":
    unittest.main()
