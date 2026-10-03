"""Tests for the additive, explicitly unverified other-party approval policy."""

import http.client
import json
import threading
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from m02_aauth_fcf656d import jose
from m02_aauth_fcf656d.exchange import Mission, PersonServer, SupervisionDecision, signed_post
from m02_aauth_fcf656d.localhost import (
    LocalAgentClient, PersonServerSurface, TransportMap, create_server,
)
from m02_aauth_fcf656d.other_party_approval import (
    AMBIENT_SCOPE, DIRECTED_SCOPE, POLICY_VERSION, ApprovalGovernedResource,
    ApprovalResourceSurface, OtherPartyApprovalError, OtherPartyApprovalPolicy,
    OtherPartyApprovalReceipt,
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


def authority_state():
    return {
        "revoked": False, "expired": False, "delegation_hops": 0,
        "max_delegation_hops": 0, "elapsed_seconds": 0,
        "max_elapsed_seconds": 1800, "attenuated": False,
        "source": "m02-other-party-reviewed-test-profile", "observed_at": NOW,
        "unavailable": ["revoked", "attenuated"],
    }


def supervision_profile():
    return SogaSupervisionProfile.create(
        verified_authority_state=authority_state(), required_authority_facts=(),
        subject_governance_state="INDEPENDENT", reachability="REACHABLE",
        subject_state_source="declared-test-profile-policy",
        reachability_source="declared-test-profile-policy")


def receipt(**changes):
    value = {
        "receipt_id": "receipt-test-1", "asserted_role": "parent",
        "assurance": "unverified-demo-input", "participant": PARTICIPANT,
        "mission_s256": MISSION, "scope": DIRECTED_SCOPE, "state": "APPROVED",
        "observed_at": NOW - 1, "expires_at": NOW + 300,
        "source": "local-test-fixture",
    }
    value.update(changes)
    return OtherPartyApprovalReceipt.create(value)


class ExplodingPolicy(OtherPartyApprovalPolicy):
    def evaluate(self, **_kwargs):
        raise AssertionError("ambient action consulted approval policy")


class OtherPartyApprovalTests(unittest.TestCase):
    def setUp(self):
        self.ap = Issuer(AP, "aauth-agent.json", "ap-key", Ed25519PrivateKey.generate())
        self.ps = Issuer(PS, "aauth-person.json", "ps-key", Ed25519PrivateKey.generate())
        self.resource_issuer = Issuer(
            RESOURCE, "aauth-resource.json", "resource-key", Ed25519PrivateKey.generate())
        self.agent_private = Ed25519PrivateKey.generate()
        self.agent_jwk = jose.public_jwk(self.agent_private.public_key(), "agent-key")
        self.agent_token = issue_agent_token(
            self.ap, agent_id=AGENT, ps=PS, agent_jwk=self.agent_jwk,
            now=NOW, expires=NOW + 7200, jti="agent-1")
        self.policy = OtherPartyApprovalPolicy()
        self.supervisor = SogaSupervisor(supervision_profile())
        self.person_server = PersonServer(
            issuer=self.ps, agent_provider=self.ap, resource=self.resource_issuer,
            directed_subject=SUBJECT,
            missions={MISSION: Mission(MISSION, AGENT, NOW + 1800)},
            supervisor=self.supervisor, now=NOW)
        self.resource = ApprovalGovernedResource(
            issuer=self.resource_issuer, person_server=self.ps, now=NOW,
            approval_policy=self.policy)
        self.ps_server = create_server(PersonServerSurface(person_server=self.person_server))
        self.resource_server = create_server(ApprovalResourceSurface(
            resource=self.resource, subject=SUBJECT, mission_s256=MISSION))
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

    def tearDown(self):
        for server in (self.ps_server, self.resource_server):
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join(timeout=2)
            self.assertFalse(thread.is_alive())

    def signed(self, role, path, body, token=None):
        return signed_post(self.mapping.authority(role), path, body,
                           token or self.agent_token, self.agent_private, NOW)

    def send(self, role, path, body, token=None):
        return self.client.send(
            role=role, path=path, request=self.signed(role, path, body, token))

    def resource_token(self, scope):
        status, _, person = self.send(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        self.assertEqual(status, 200)
        status, _, resource = self.send(
            RESOURCE, "/authorize", {"scope": scope}, person["person_token"])
        self.assertEqual(status, 200)
        return person["person_token"], resource["resource_token"]

    def auth_token(self, scope):
        person, resource = self.resource_token(scope)
        status, _, auth = self.send(
            PS, "/auth-token",
            {"resource_token": resource, "presented_token": person,
             "justification": "bounded participant response"})
        self.assertEqual(status, 200)
        return auth["auth_token"]

    def enforce(self, token, scope=DIRECTED_SCOPE, participant=PARTICIPANT):
        return self.send(
            RESOURCE, "/enforce", {"participant": participant, "scope": scope}, token)

    def test_receipt_requires_exact_schema_and_types(self):
        base = receipt().__dict__
        cases = (
            {name: value for name, value in base.items() if name != "source"},
            {**base, "extra": "value"}, {**base, "asserted_role": "guardian"},
            {**base, "assurance": "verified"}, {**base, "state": "UNKNOWN"},
            {**base, "observed_at": True}, {**base, "expires_at": NOW - 2},
            {**base, "source": ""},
        )
        for value in cases:
            with self.subTest(value=value), self.assertRaises(OtherPartyApprovalError):
                OtherPartyApprovalReceipt.create(value)

    def test_unknown_scope_fails_closed(self):
        token = self.auth_token("misty.unknown")
        status, _, body = self.enforce(token, scope="misty.unknown")
        self.assertEqual(status, 403)
        self.assertEqual(body["authorization"], "denied")

    def test_ambient_action_never_consults_approval_policy(self):
        self.resource.approval_policy = ExplodingPolicy()
        token = self.auth_token(AMBIENT_SCOPE)
        status, _, body = self.enforce(token, scope=AMBIENT_SCOPE)
        self.assertEqual(status, 200)
        self.assertEqual(body["scope"], AMBIENT_SCOPE)
        self.assertIsNone(body["decision"])

    def test_directed_action_without_receipt_is_denied(self):
        token = self.auth_token(DIRECTED_SCOPE)
        status, _, body = self.enforce(token)
        self.assertEqual(status, 403)
        self.assertEqual(body["reason"], "other_party_approval_required")
        self.assertEqual(body["decision"]["reason"], "approval_absent")

    def test_wrong_participant_mission_and_scope_do_not_satisfy_policy(self):
        for changed, reason in (
                ({"participant": "participant-test-2"}, "participant_mismatch"),
                ({"mission_s256": "other-mission"}, "mission_mismatch")):
            candidate = receipt(**changed)
            self.policy.replace(candidate)
            decision = self.policy.evaluate(
                participant=PARTICIPANT, mission_s256=MISSION,
                scope=DIRECTED_SCOPE, now=NOW)
            self.assertEqual(decision.reason, reason)
            self.assertEqual(decision.outcome, "DENY")
        self.policy.replace(receipt())
        with self.assertRaises(OtherPartyApprovalError):
            self.policy.evaluate(
                participant=PARTICIPANT, mission_s256=MISSION,
                scope=AMBIENT_SCOPE, now=NOW)

    def test_active_exact_approval_and_soga_allow_complete_exchange(self):
        self.policy.replace(receipt())
        token = self.auth_token(DIRECTED_SCOPE)
        status, _, body = self.enforce(token)
        self.assertEqual(status, 200)
        self.assertEqual(body["decision"]["outcome"], "ALLOW")
        self.assertEqual(body["decision"]["policy_version"], POLICY_VERSION)
        self.assertEqual(body["decision"]["approval_assurance"],
                         "unverified-demo-input")
        self.assertEqual(body["decision"]["participant_source"],
                         "agent-asserted-signed-action-body")

    def test_active_approval_never_overrides_soga_denial_or_failure(self):
        self.policy.replace(receipt())

        def evaluator_for(value):
            if isinstance(value, Exception):
                def raise_error(*_args, **_kwargs):
                    raise value
                return raise_error
            if value == "MALFORMED":
                return lambda *_args, **_kwargs: {}
            return lambda *_args, **_kwargs: {
                "governance_determination": value,
                "governance_decision": {"step_id": "decision-test"},
                "canonical_decision_package": {"decision": value},
            }

        for outcome in ("DENY", "RESTRICT", "MALFORMED", ValueError("failure")):
            with self.subTest(outcome=str(outcome)):
                self.person_server.supervisor = SogaSupervisor(
                    supervision_profile(), evaluator=evaluator_for(outcome))
                person, resource = self.resource_token(DIRECTED_SCOPE)
                status, _, body = self.send(
                    PS, "/auth-token",
                    {"resource_token": resource, "presented_token": person,
                     "justification": "bounded participant response"})
                self.assertEqual(status, 403)
                self.assertNotIn("auth_token", body)
                self.assertEqual(self.policy.calls, 0)

    def test_withdrawal_denies_the_next_directed_enforcement(self):
        self.policy.replace(receipt())
        token = self.auth_token(DIRECTED_SCOPE)
        self.assertEqual(self.enforce(token)[0], 200)
        self.policy.replace(receipt(state="WITHDRAWN", observed_at=NOW))
        status, _, body = self.enforce(token)
        self.assertEqual(status, 403)
        self.assertEqual(body["decision"]["reason"], "approval_withdrawn")

    def test_previously_issued_token_remains_valid_but_policy_denies_action(self):
        self.policy.replace(receipt())
        token = self.auth_token(DIRECTED_SCOPE)
        request = self.signed(
            RESOURCE, "/enforce",
            {"participant": PARTICIPANT, "scope": DIRECTED_SCOPE}, token)
        self.resource.enforce(
            request, subject=SUBJECT, mission_s256=MISSION,
            required_scope=DIRECTED_SCOPE)
        self.policy.replace(receipt(state="WITHDRAWN", observed_at=NOW))
        self.resource.enforce(
            request, subject=SUBJECT, mission_s256=MISSION,
            required_scope=DIRECTED_SCOPE)
        status, _, body = self.enforce(token)
        self.assertEqual(status, 403)
        self.assertEqual(body["decision"]["reason"], "approval_withdrawn")

    def test_cross_participant_action_is_denied(self):
        self.policy.replace(receipt())
        token = self.auth_token(DIRECTED_SCOPE)
        status, _, body = self.enforce(token, participant="participant-test-2")
        self.assertEqual(status, 403)
        self.assertEqual(body["decision"]["reason"], "participant_mismatch")

    def test_expired_and_future_observed_receipts_fail_closed(self):
        for candidate, reason in (
                (receipt(observed_at=NOW - 10, expires_at=NOW), "approval_expired"),
                (receipt(observed_at=NOW + 1, expires_at=NOW + 10),
                 "approval_not_yet_observed")):
            with self.subTest(reason=reason):
                self.policy.replace(candidate)
                decision = self.policy.evaluate(
                    participant=PARTICIPANT, mission_s256=MISSION,
                    scope=DIRECTED_SCOPE, now=NOW)
                self.assertEqual((decision.outcome, decision.reason), ("DENY", reason))

    def test_single_variable_receipt_state_changes_directed_outcome(self):
        token = self.auth_token(DIRECTED_SCOPE)
        request_body = {"participant": PARTICIPANT, "scope": DIRECTED_SCOPE}
        before = {
            "agent": AGENT, "agent_jwk": self.agent_jwk,
            "mission_s256": MISSION, "resource": RESOURCE,
            "participant": PARTICIPANT, "scope": DIRECTED_SCOPE,
            "subject": SUBJECT, "clock": NOW,
            "justification": "bounded participant response",
        }
        absent = self.send(RESOURCE, "/enforce", request_body, token)
        self.policy.replace(receipt())
        approved = self.send(RESOURCE, "/enforce", request_body, token)
        after = {
            "agent": AGENT, "agent_jwk": self.agent_jwk,
            "mission_s256": MISSION, "resource": RESOURCE,
            "participant": PARTICIPANT, "scope": DIRECTED_SCOPE,
            "subject": SUBJECT, "clock": NOW,
            "justification": "bounded participant response",
        }
        self.assertEqual(absent[0], 403)
        self.assertEqual(approved[0], 200)
        self.assertEqual(before, after)
        self.assertEqual(absent[2]["decision"]["approval_assurance"],
                         "unverified-demo-input")


if __name__ == "__main__":
    unittest.main()
