"""Specification tests for the transport-free minimal AAuth exchange."""

import json
from pathlib import Path
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from m02_aauth_fcf656d import jose
from m02_aauth_fcf656d.exchange import (
    ExchangeError, Mission, PersonServer, Resource, SupervisionDecision,
    signed_post,
)
from m02_aauth_fcf656d.identifiers import (
    IdentifierError, OutOfProfileIdentifier, validate_agent_identifier,
)
from m02_aauth_fcf656d.metadata import (
    agent_provider_fixture_metadata, assert_interim_metadata,
    interim_person_server_metadata, person_server_fixture_metadata,
    resource_fixture_metadata,
)
from m02_aauth_fcf656d.tokens import (
    Issuer, TokenProfileError, issue_agent_token, issue_auth_token,
    issue_person_token, issue_resource_token, verify_auth_token,
)


NOW = 1_000_000
AP = "https://agent.example"
PS = "https://ps.example"
RESOURCE = "https://resource.example"
AGENT = "aauth:misty-tipjar@agent.example"
MISSION = "mission-sha256"
SUBJECT = "directed-person-1"


class Recorder:
    def __init__(self, decision=None, error=None):
        self.decision = decision or SupervisionDecision("ALLOW", "decision-1", "mission-policy")
        self.error = error
        self.calls = []

    def __call__(self, value):
        self.calls.append(value)
        if self.error:
            raise self.error
        return self.decision


class ExchangeFixture(unittest.TestCase):
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
        self.supervisor = Recorder()
        missions = {MISSION: Mission(MISSION, AGENT, NOW + 1800)}
        self.person_server = PersonServer(
            issuer=self.ps, agent_provider=self.ap, resource=self.resource_issuer,
            directed_subject=SUBJECT, missions=missions,
            supervisor=self.supervisor, now=NOW)
        self.resource = Resource(issuer=self.resource_issuer, person_server=self.ps, now=NOW)

    def agent_request(self, authority, path, body, token=None):
        return signed_post(authority, path, body, token or self.agent_token,
                           self.agent_private, NOW)

    def complete_exchange(self):
        person_request = self.agent_request(
            "ps.example", "/person", {"resource": RESOURCE, "mission_s256": MISSION})
        person_token = self.person_server.person_token(person_request)
        resource_request = self.agent_request(
            "resource.example", "/authorize", {"scope": "misty.interact"}, person_token)
        resource_token = self.resource.authorize(resource_request)
        auth_request = self.agent_request(
            "ps.example", "/token",
            {"resource_token": resource_token, "presented_token": person_token,
             "justification": "Run one bounded interaction"})
        auth_token = self.person_server.auth_token(auth_request)
        return person_token, resource_token, auth_token


class IdentifierAndMetadataTests(ExchangeFixture):
    def test_identifier_syntax_case_and_subagent_profile_boundary(self):
        self.assertEqual(validate_agent_identifier(AGENT, top_level_only=True), AGENT)
        self.assertEqual(validate_agent_identifier("aauth:Agent@agent.example"),
                         "aauth:Agent@agent.example")
        self.assertEqual(validate_agent_identifier("aauth:agent+child@agent.example"),
                         "aauth:agent+child@agent.example")
        with self.assertRaises(OutOfProfileIdentifier):
            validate_agent_identifier("aauth:agent+child@agent.example", top_level_only=True)
        for invalid in ("aauth:@agent.example", "aauth:space here@agent.example",
                        "aauth:agent@https://agent.example", "AAUTH:agent@agent.example"):
            with self.subTest(invalid=invalid), self.assertRaises(IdentifierError):
                validate_agent_identifier(invalid)

    def test_fixture_metadata_is_separate_from_interim_metadata(self):
        interim = interim_person_server_metadata(PS, PS + "/jwks")
        self.assertEqual(assert_interim_metadata(interim), interim)
        ps = person_server_fixture_metadata(PS, PS + "/jwks", PS + "/person", PS + "/token")
        self.assertEqual(set(ps).intersection({"issuer", "jwks_uri", "person_token_endpoint",
                                               "auth_token_endpoint"}),
                         {"issuer", "jwks_uri", "person_token_endpoint", "auth_token_endpoint"})
        with self.assertRaises(ValueError):
            assert_interim_metadata(ps)
        self.assertEqual(agent_provider_fixture_metadata(AP, AP + "/jwks")["fixture_role"],
                         "agent-provider")
        self.assertEqual(resource_fixture_metadata(
            RESOURCE, RESOURCE + "/jwks", RESOURCE + "/authorize")["access_mode"],
            "auth-token")
        for issuer in (self.ap, self.ps, self.resource_issuer):
            self.assertTrue(all("d" not in key and key["alg"] == "Ed25519"
                                for key in issuer.jwks["keys"]))


class LiveExchangeTests(ExchangeFixture):
    def test_complete_exchange_and_mission_continuity(self):
        person_token, resource_token, auth_token = self.complete_exchange()
        person = jose.verify_compact(person_token, "aa-person+jwt", self.ps.jwks)
        resource = jose.verify_compact(
            resource_token, "aa-resource+jwt", self.resource_issuer.jwks)
        auth = jose.verify_compact(auth_token, "aa-auth+jwt", self.ps.jwks)
        self.assertEqual([person["mission_s256"], resource["mission_s256"],
                          auth["mission_s256"]], [MISSION, MISSION, MISSION])
        self.assertEqual([person["sub"], resource["sub"], auth["sub"]],
                         [SUBJECT, SUBJECT, SUBJECT])
        self.assertEqual(resource["presented_jti"], person["jti"])
        self.assertEqual(len(self.supervisor.calls), 1)
        call = self.supervisor.calls[0]
        self.assertEqual(set(call), {"resource_asserted", "person_server_verified",
                                     "agent_asserted"})
        final = self.agent_request(
            "resource.example", "/interact", {"action": "greet"}, auth_token)
        enforced = self.resource.enforce(
            final, subject=SUBJECT, mission_s256=MISSION,
            required_scope="misty.interact")
        self.assertEqual(enforced["jti"], "auth-1")

    def test_person_token_is_rejected_where_auth_token_required(self):
        person_token, _, _ = self.complete_exchange()
        wrong = self.agent_request(
            "resource.example", "/interact", {"action": "greet"}, person_token)
        with self.assertRaisesRegex(Exception, "wrong AAuth token type"):
            self.resource.enforce(
                wrong, subject=SUBJECT, mission_s256=MISSION,
                required_scope="misty.interact")

    def test_confirmation_key_binding_is_enforced(self):
        _, _, auth = self.complete_exchange()
        other_private = Ed25519PrivateKey.generate()
        request = signed_post(
            "resource.example", "/interact", {"action": "greet"},
            auth, other_private, NOW)
        with self.assertRaises(Exception):
            self.resource.enforce(
                request, subject=SUBJECT, mission_s256=MISSION,
                required_scope="misty.interact")

    def test_person_token_requires_active_retained_owned_mission(self):
        cases = (
            {},
            {MISSION: Mission(MISSION, AGENT, NOW + 1800, active=False)},
            {MISSION: Mission(MISSION, AGENT, NOW)},
            {MISSION: Mission(MISSION, "aauth:other@agent.example", NOW + 1800)},
        )
        for missions in cases:
            with self.subTest(missions=missions):
                self.person_server.missions = missions
                request = self.agent_request(
                    "ps.example", "/person",
                    {"resource": RESOURCE, "mission_s256": MISSION})
                with self.assertRaises(ExchangeError):
                    self.person_server.person_token(request)

    def test_supervision_deny_malformed_and_exception_fail_closed(self):
        for supervisor in (
            Recorder(SupervisionDecision("DENY", "decision-2", "policy-deny")),
            Recorder(decision="not-a-decision"),
            Recorder(error=RuntimeError("unavailable")),
        ):
            with self.subTest(supervisor=supervisor):
                self.person_server.supervisor = supervisor
                person_request = self.agent_request(
                    "ps.example", "/person", {"resource": RESOURCE,
                                                "mission_s256": MISSION})
                person = self.person_server.person_token(person_request)
                resource_request = self.agent_request(
                    "resource.example", "/authorize", {"scope": "misty.interact"}, person)
                resource = self.resource.authorize(resource_request)
                request = self.agent_request(
                    "ps.example", "/token",
                    {"resource_token": resource, "presented_token": person,
                     "justification": "test"})
                with self.assertRaises(ExchangeError):
                    self.person_server.auth_token(request)
                self.assertEqual(len(supervisor.calls), 1)

    def test_invalid_chain_bindings_fail_before_supervision(self):
        person, resource, _ = self.complete_exchange()
        base_claims = jose.verify_compact(resource, "aa-resource+jwt", self.resource_issuer.jwks)
        variants = {
            "aud": "https://other.example",
            "ps": "https://other.example",
            "sub": "other-subject",
            "presented_jti": "other-jti",
            "agent_jkt": "other-thumbprint",
            "mission_s256": "other-mission",
            "exp": NOW,
        }
        for name, value in variants.items():
            with self.subTest(name=name):
                changed = self.resource_issuer.sign({**base_claims, name: value},
                                                    "aa-resource+jwt")
                request = self.agent_request(
                    "ps.example", "/token",
                    {"resource_token": changed, "presented_token": person,
                     "justification": "test"})
                calls = len(self.supervisor.calls)
                with self.assertRaises((ExchangeError, TokenProfileError)):
                    self.person_server.auth_token(request)
                self.assertEqual(len(self.supervisor.calls), calls)

    def test_tampered_presented_token_and_wrong_scope_fail(self):
        person, _, auth = self.complete_exchange()
        parts = person.split(".")
        tampered = parts[0] + "." + parts[1] + "." + (
            "A" if parts[2][0] != "A" else "B") + parts[2][1:]
        resource_claims = {
            "iss": RESOURCE, "dwk": "aauth-resource.json", "aud": PS, "ps": PS,
            "sub": SUBJECT, "presented_jti": "person-1",
            "agent_jkt": jose.jwk_thumbprint(self.agent_jwk),
            "mission_s256": MISSION, "scope": "misty.interact",
            "jti": "resource-2", "iat": NOW, "exp": NOW + 300,
        }
        resource = self.resource_issuer.sign(resource_claims, "aa-resource+jwt")
        request = self.agent_request(
            "ps.example", "/token",
            {"resource_token": resource, "presented_token": tampered,
             "justification": "test"})
        with self.assertRaises(TokenProfileError):
            self.person_server.auth_token(request)
        final = self.agent_request(
            "resource.example", "/interact", {"action": "greet"}, auth)
        with self.assertRaisesRegex(TokenProfileError, "scope"):
            self.resource.enforce(final, subject=SUBJECT, mission_s256=MISSION,
                                  required_scope="misty.admin")
        for subject, mission in (("wrong-subject", MISSION),
                                 (SUBJECT, "wrong-mission")):
            with self.subTest(subject=subject, mission=mission), \
                    self.assertRaisesRegex(TokenProfileError, "context"):
                self.resource.enforce(final, subject=subject, mission_s256=mission,
                                      required_scope="misty.interact")

    def test_lifetime_ceilings_and_governing_expiry(self):
        with self.assertRaisesRegex(TokenProfileError, "one hour"):
            issue_person_token(
                self.ps, resource=RESOURCE, subject=SUBJECT, agent_jwk=self.agent_jwk,
                mission_s256=MISSION, now=NOW, expires=NOW + 3601, jti="person-long",
                agent_expires=NOW + 7200, mission_expires=NOW + 7200)
        with self.assertRaisesRegex(TokenProfileError, "five minutes"):
            issue_resource_token(
                self.resource_issuer, ps=PS, subject=SUBJECT,
                presented_jti="person-1", agent_jwk=self.agent_jwk,
                mission_s256=MISSION, scope="misty.interact", now=NOW,
                expires=NOW + 301, jti="resource-long")
        with self.assertRaisesRegex(TokenProfileError, "governing"):
            issue_auth_token(
                self.ps, resource=RESOURCE, ps=PS, subject=SUBJECT,
                agent_jwk=self.agent_jwk, mission_s256=MISSION,
                scope="misty.interact", now=NOW, expires=NOW + 601,
                jti="auth-long", agent_expires=NOW + 600,
                presented_expires=NOW + 700, mission_expires=NOW + 800)

    def test_accepted_frozen_packages_are_unchanged(self):
        root = Path(__file__).resolve().parents[1]
        expected = {
            "m02_person_server/__init__.py": "1590a304fe8181b6fe7c9e2819e61a5799afb31d827e9cdf596e5cfb97c084b5",
            "m02_person_server/crypto.py": "df1c28318ab44b2c23a957a5aecd23f4bcda2e6068f4616786aaa1916bfac6f9",
            "m02_person_server/http_server.py": "51d11c9a928ecc432efe8d86a342200b9d6666da78acfaa77042e0bfe922c74b",
            "m02_person_server/service.py": "0b7c0d503ef347c568fc6f6e5ece690d41b1fbc5885f2805b36819d261127043",
            "m02_person_server/store.py": "0c60b7f8e2539a7da7ccae7c301c5366b269974c15a29c4dc029e4bc647fc590",
            "m02_person_server/walkthrough.py": "0e69bcfc8edb9655020d4733af25de473e1a1488a333ae779a252ecfac34528d",
            "m02_aauth_fcf656d/__init__.py": "c480bf75ecea51a368627cb00dabdd96ed9e48df784497ce9b7efee80f8f58e8",
            "m02_aauth_fcf656d/http_signatures.py": "f6ae4f4463852b310d09608d4a60084a566733e857098bcd42f2bc1a659cab65",
            "m02_aauth_fcf656d/jose.py": "cda9b577746116e65c34977706593475a8637a3ec6823375dda7baffa961cdd4",
            "m02_aauth_fcf656d/profile.py": "fb7b9b51ada64c7e45f61eb24991078cbe5d172cdf781887bf6843c27fb7afbf",
            "m02_aauth_fcf656d/structured_fields.py": "9d774a03dd096577a9ce917b40f4c3693e30758319fa05f455feb3b734c78a71",
            "tests/test_m02_aauth_fcf656d.py": "89b71359c6c071453fab289aa85443aa4f7156e4a2d263d8ac12f85bee4deaad",
            "m02_was_composition/__init__.py": "62e10c1f9bee9b3f27d1f0acb17f71a34ea89fcf30e39f93b83bb620de3d5f97",
            "m02_was_composition/adapter.py": "28bcbaeda80c7436353e6872e3fa2f35390e4089ae1ea7d5c64ced93afe071e7",
            "m02_was_composition/controller.py": "559a9397e610a7f60cdf34db1b96874ad60509d609a069e2c0bf2e5b78727f2e",
            "m02_was_composition/diagnostic_tests.py": "794a1b961d976abeaad044221e031358922016e9817c891e2403663337719403",
            "m02_was_composition/worker.mjs": "f3f58b1d603228c057d9a5af99045cd5783ea5a92ffaa0e550fc0cc1ce2d5b60",
            "tools/m02_stage3lib/README.md": "cb65726039cce6d8178139ebd5ccdeacc8c0142b011741bca65f235df8cf64af",
            "tools/m02_stage3lib/harness.mjs": "17d053cd3d644fdc782c14ccb23dcf8e8d6d5de66a7e200a0c0623d28e7c6b4c",
            "tools/m02_stage3lib/source_contract.test.mjs": "85a712693a1a6584958ae90dc517b8108ff5c4922abbc7c23c310ed0ec5d602d",
        }
        import hashlib
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest)
