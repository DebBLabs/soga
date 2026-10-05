"""Tests for the sanitized local demo-operator adapter."""

import hashlib
from pathlib import Path
import threading
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from m02_aauth_fcf656d import jose
from m02_aauth_fcf656d.approval_pending import (
    ApprovalPendingClient, ApprovalPendingStore, ApprovalPendingSurface,
    create_approval_pending_server, signed_poll,
)
from m02_aauth_fcf656d.demo_operator import (
    MAX_RECEIPT_IDS, DemoOperatorAdapter, DemoOperatorError,
)
from m02_aauth_fcf656d.exchange import Mission, PersonServer, signed_post
from m02_aauth_fcf656d.localhost import (
    LocalAgentClient, PersonServerSurface, TransportMap, create_server,
)
from m02_aauth_fcf656d.other_party_approval import (
    DIRECTED_SCOPE, ApprovalGovernedResource, OtherPartyApprovalPolicy,
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
REPO = Path(__file__).resolve().parents[1]


class Clock:
    def __init__(self, value=NOW):
        self.value = value
        self.lock = threading.Lock()

    def __call__(self):
        with self.lock:
            return self.value


def supervision_profile():
    return SogaSupervisionProfile.create(
        verified_authority_state={
            "revoked": False, "expired": False, "delegation_hops": 0,
            "max_delegation_hops": 0, "elapsed_seconds": 0,
            "max_elapsed_seconds": 1800, "attenuated": False,
            "source": "m02-demo-operator-reviewed-test-profile",
            "observed_at": NOW, "unavailable": ["revoked", "attenuated"],
        },
        required_authority_facts=(), subject_governance_state="INDEPENDENT",
        reachability="REACHABLE",
        subject_state_source="declared-test-profile-policy",
        reachability_source="declared-test-profile-policy")


class DemoOperatorTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.pending_sequence = 0
        self.receipt_sequence = 0

        def pending_identifier():
            self.pending_sequence += 1
            return format(self.pending_sequence, "032d")

        def receipt_identifier():
            self.receipt_sequence += 1
            return ("r" + format(self.receipt_sequence, "031d"))

        self.receipt_identifier = receipt_identifier
        self.ap = Issuer(AP, "aauth-agent.json", "ap-key", Ed25519PrivateKey.generate())
        self.ps = Issuer(PS, "aauth-person.json", "ps-key", Ed25519PrivateKey.generate())
        self.resource_issuer = Issuer(
            RESOURCE, "aauth-resource.json", "resource-key",
            Ed25519PrivateKey.generate())
        self.agent_private = Ed25519PrivateKey.generate()
        self.agent_jwk = jose.public_jwk(self.agent_private.public_key(), "agent-key")
        self.agent_token = issue_agent_token(
            self.ap, agent_id=AGENT, ps=PS, agent_jwk=self.agent_jwk,
            now=NOW, expires=NOW + 7200, jti="agent-1")
        self.person_server = PersonServer(
            issuer=self.ps, agent_provider=self.ap, resource=self.resource_issuer,
            directed_subject=SUBJECT,
            missions={MISSION: Mission(MISSION, AGENT, NOW + 1800)},
            supervisor=SogaSupervisor(supervision_profile()), now=NOW)
        self.policy = OtherPartyApprovalPolicy()
        self.resource = ApprovalGovernedResource(
            issuer=self.resource_issuer, person_server=self.ps, now=NOW,
            approval_policy=self.policy)
        self.store = ApprovalPendingStore(
            clock=self.clock, id_factory=pending_identifier)
        self.adapter = DemoOperatorAdapter(
            store=self.store, policy=self.policy, participant=PARTICIPANT,
            mission_s256=MISSION, scope=DIRECTED_SCOPE, clock=self.clock,
            receipt_id_factory=self.receipt_identifier)
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
                      RESOURCE: "http://127.0.0.1:" +
                      str(self.resource_server.server_port)})
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

    def auth_token(self):
        status, _, person = self.send(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        self.assertEqual(status, 200)
        status, _, resource = self.send(
            RESOURCE, "/authorize", {"scope": DIRECTED_SCOPE},
            person["person_token"])
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

    def poll(self, path, token):
        request = signed_poll(
            self.mapping.authority(RESOURCE), path, token,
            self.agent_private, self.clock())
        return self.poll_client.poll(role=RESOURCE, path=path, request=request)

    def test_01_exact_held_approved_receipt_and_event(self):
        _, status, headers, _ = self.begin()
        self.assertEqual(status, 202)
        event = self.adapter.record_held_input(headers["Location"], "APPROVED")
        self.assertEqual(event.event, "held_other_party_input_recorded")
        self.assertEqual(event.state, "APPROVED")
        self.assertEqual(event.asserted_role, "parent")
        self.assertEqual(event.assurance, "unverified-demo-input")
        self.assertEqual(event.expires_at - event.observed_at, 120)
        self.assertNotIn("pending", event.as_dict())

    def test_02_exact_held_withdrawn_receipt_and_event(self):
        _, _, headers, _ = self.begin()
        event = self.adapter.record_held_input(headers["Location"], "WITHDRAWN")
        self.assertEqual(event.state, "WITHDRAWN")
        self.assertEqual(event.source, "local-operator-demo-control")
        self.assertEqual(len(event.receipt_id), 32)

    def test_03_standing_approved_returns_immediate_200(self):
        event = self.adapter.replace_standing_input("APPROVED")
        _, status, _, body = self.begin()
        self.assertEqual(status, 200)
        self.assertEqual(body["decision"]["reason"], "approval_active")
        self.assertEqual(event.event, "standing_other_party_input_recorded")

    def test_04_standing_withdrawn_returns_202_pending(self):
        self.adapter.replace_standing_input("WITHDRAWN")
        _, status, headers, body = self.begin()
        self.assertEqual((status, body), (202, {"status": "pending"}))
        self.assertTrue(headers["Location"].startswith("/pending/"))

    def test_05_standing_cleared_returns_202_pending(self):
        self.adapter.replace_standing_input("APPROVED")
        event = self.adapter.replace_standing_input("CLEARED")
        _, status, _, body = self.begin()
        self.assertEqual((status, body), (202, {"status": "pending"}))
        self.assertIsNone(event.receipt_id)
        self.assertIsNone(event.expires_at)

    def test_06_held_approved_poll_allows_once(self):
        token, _, headers, _ = self.begin()
        self.adapter.record_held_input(headers["Location"], "APPROVED")
        status, _, body = self.poll(headers["Location"], token)
        self.assertEqual(status, 200)
        self.assertEqual(body["decision"]["reason"], "approval_active")

    def test_07_held_withdrawn_poll_is_terminal_denial(self):
        token, _, headers, _ = self.begin()
        self.adapter.record_held_input(headers["Location"], "WITHDRAWN")
        status, _, body = self.poll(headers["Location"], token)
        self.assertEqual(status, 403)
        self.assertEqual(body["decision"]["reason"], "approval_withdrawn")

    def test_08_binding_mismatch_is_reported_only_by_signed_poll(self):
        token, _, headers, _ = self.begin(participant="participant-test-2")
        event = self.adapter.record_held_input(headers["Location"], "APPROVED")
        self.assertEqual(event.state, "APPROVED")
        status, _, body = self.poll(headers["Location"], token)
        self.assertEqual(status, 403)
        self.assertEqual(body["decision"]["reason"], "participant_mismatch")

    def test_09_withdrawal_replaces_approval_before_poll(self):
        token, _, headers, _ = self.begin()
        self.adapter.record_held_input(headers["Location"], "APPROVED")
        self.adapter.record_held_input(headers["Location"], "WITHDRAWN")
        status, _, body = self.poll(headers["Location"], token)
        self.assertEqual(status, 403)
        self.assertEqual(body["decision"]["reason"], "approval_withdrawn")

    def test_10_terminal_unknown_and_malformed_fail_with_fixed_codes(self):
        token, _, headers, _ = self.begin()
        self.adapter.record_held_input(headers["Location"], "APPROVED")
        self.assertEqual(self.poll(headers["Location"], token)[0], 200)
        cases = ((headers["Location"], "pending_not_live"),
                 ("/pending/short", "invalid_input"),
                 ("/wrong/" + "1" * 32, "invalid_input"))
        for path, code in cases:
            with self.subTest(path=path), self.assertRaises(DemoOperatorError) as raised:
                self.adapter.record_held_input(path, "APPROVED")
            self.assertEqual(raised.exception.code, code)

    def test_11_invalid_duplicate_capacity_and_concurrency_fail_closed(self):
        with self.assertRaises(DemoOperatorError) as invalid:
            self.adapter.replace_standing_input("UNKNOWN")
        self.assertEqual(invalid.exception.code, "invalid_input")

        bad_clock = Clock()
        bad_store = ApprovalPendingStore(
            clock=bad_clock, id_factory=lambda: "p" * 32)
        bad_clock_adapter = DemoOperatorAdapter(
            store=bad_store, policy=OtherPartyApprovalPolicy(),
            participant=PARTICIPANT, mission_s256=MISSION,
            scope=DIRECTED_SCOPE, clock=bad_clock,
            receipt_id_factory=lambda: "t" * 32)
        bad_clock.value = -1
        with self.assertRaises(DemoOperatorError) as clock_error:
            bad_clock_adapter.replace_standing_input("APPROVED")
        self.assertEqual(clock_error.exception.code, "invalid_input")

        malformed_identifier = DemoOperatorAdapter(
            store=self.store, policy=self.policy, participant=PARTICIPANT,
            mission_s256=MISSION, scope=DIRECTED_SCOPE, clock=self.clock,
            receipt_id_factory=lambda: "not-url-safe-or-32-characters!")
        with self.assertRaises(DemoOperatorError) as identifier_error:
            malformed_identifier.replace_standing_input("APPROVED")
        self.assertEqual(identifier_error.exception.code, "invalid_input")

        duplicate = DemoOperatorAdapter(
            store=self.store, policy=self.policy, participant=PARTICIPANT,
            mission_s256=MISSION, scope=DIRECTED_SCOPE, clock=self.clock,
            receipt_id_factory=lambda: "d" * 32)
        duplicate.replace_standing_input("APPROVED")
        with self.assertRaises(DemoOperatorError) as repeated:
            duplicate.replace_standing_input("WITHDRAWN")
        self.assertEqual(repeated.exception.code, "invalid_input")

        counter = iter("c" + format(value, "031d")
                       for value in range(MAX_RECEIPT_IDS + 1))
        bounded = DemoOperatorAdapter(
            store=self.store, policy=self.policy, participant=PARTICIPANT,
            mission_s256=MISSION, scope=DIRECTED_SCOPE, clock=self.clock,
            receipt_id_factory=lambda: next(counter))
        for _ in range(MAX_RECEIPT_IDS):
            bounded.replace_standing_input("APPROVED")
        with self.assertRaises(DemoOperatorError) as full:
            bounded.replace_standing_input("APPROVED")
        self.assertEqual(full.exception.code, "operator_capacity")

        events = []
        failures = []
        concurrent = DemoOperatorAdapter(
            store=self.store, policy=self.policy, participant=PARTICIPANT,
            mission_s256=MISSION, scope=DIRECTED_SCOPE, clock=self.clock,
            receipt_id_factory=self.receipt_identifier)

        def change(state):
            try:
                events.append(concurrent.replace_standing_input(state))
            except Exception as error:
                failures.append(type(error).__name__)

        threads = [threading.Thread(target=change, args=(state,))
                   for state in ("APPROVED", "WITHDRAWN") * 8]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=2)
        self.assertEqual(failures, [])
        self.assertEqual(len({event.receipt_id for event in events}), 16)
        self.assertNotIn("eyJ", repr(events))

    def test_12_d140_sources_remain_byte_identical(self):
        expected = {
            "m02_aauth_fcf656d/approval_pending.py":
                "18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b",
            "tests/test_m02_aauth_approval_pending.py":
                "b0936449de6a143102ac012f7783ef138a5fe743a56fae41093b53d2eda37c69",
            "tools/m02_aauth_fcf656d/run_approval_pending_tests.py":
                "fb76b2135042178a6915ddca03f409e85981ddf40df49937839355540aab0ee7",
        }
        for relative, digest in expected.items():
            with self.subTest(relative=relative):
                self.assertEqual(
                    hashlib.sha256((REPO / relative).read_bytes()).hexdigest(), digest)
