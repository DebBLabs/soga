"""Tests for the bounded localhost AAuth transport and SOGA gateway."""

import hashlib
import http.client
import json
from pathlib import Path
import threading
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from m02_aauth_fcf656d import jose
from m02_aauth_fcf656d.exchange import Mission, PersonServer, Resource, signed_post
from m02_aauth_fcf656d.localhost import (
    LocalAgentClient, LocalhostProfileError, PersonServerSurface, ResourceSurface,
    TransportMap, create_server,
)
from m02_aauth_fcf656d.soga_supervision import (
    SogaSupervisionProfile, SogaSupervisor, SupervisionAdapterError,
)
from m02_aauth_fcf656d.tokens import Issuer, issue_agent_token


NOW = 1_000_000
AP = "https://agent.example"
PS = "https://ps.example"
RESOURCE = "https://resource.example"
AGENT = "aauth:misty-tipjar@agent.example"
MISSION = "mission-sha256"
SUBJECT = "directed-person-1"
SCOPE = "misty.interact"


def authority_state(**changes):
    value = {
        "revoked": False,
        "expired": False,
        "delegation_hops": 0,
        "max_delegation_hops": 0,
        "elapsed_seconds": 0,
        "max_elapsed_seconds": 1800,
        "attenuated": False,
        "source": "m02-localhost-reviewed-test-profile",
        "observed_at": NOW,
        "unavailable": ["revoked", "attenuated"],
    }
    value.update(changes)
    return value


def explicit_profile(*, required_authority_facts):
    return SogaSupervisionProfile.create(
        verified_authority_state=authority_state(),
        required_authority_facts=required_authority_facts,
        subject_governance_state="INDEPENDENT",
        reachability="REACHABLE",
        subject_state_source="declared-test-profile-policy",
        reachability_source="declared-test-profile-policy")


class TransportMapTests(unittest.TestCase):
    def test_exact_mapping_and_bare_role_authority(self):
        mapping = TransportMap(
            person_server=PS, resource=RESOURCE,
            mappings={PS: "http://127.0.0.1:12001",
                      RESOURCE: "http://127.0.0.1:12002"})
        self.assertEqual(mapping.destination(PS), ("127.0.0.1", 12001))
        self.assertEqual(mapping.authority(PS), "ps.example")
        self.assertEqual(mapping.authority(RESOURCE), "resource.example")

    def test_invalid_transport_spellings_fail_closed(self):
        invalid = (
            "HTTP://127.0.0.1:80", "http://localhost:80", "http://0.0.0.0:80",
            "http://127.0.0.2:80", "http://[::1]:80", "http://127.0.0.1",
            "http://127.0.0.1:0", "http://127.0.0.1:00080",
            "http://user@127.0.0.1:80", "http://127.0.0.1:80/path",
            "http://127.0.0.1:80?query", "http://127.0.0.1:80#fragment",
            "http://127.0.0.1:65536",
        )
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(LocalhostProfileError):
                TransportMap(person_server=PS, resource=RESOURCE,
                             mappings={PS: value, RESOURCE: "http://127.0.0.1:12002"})

    def test_mapping_rejects_missing_unknown_and_noncanonical_roles(self):
        cases = (
            {PS: "http://127.0.0.1:12001"},
            {PS: "http://127.0.0.1:12001", RESOURCE: "http://127.0.0.1:12002",
             "https://other.example": "http://127.0.0.1:12003"},
        )
        for mappings in cases:
            with self.subTest(mappings=mappings), self.assertRaises(LocalhostProfileError):
                TransportMap(person_server=PS, resource=RESOURCE, mappings=mappings)
        with self.assertRaises(LocalhostProfileError):
            TransportMap(person_server="http://ps.example", resource=RESOURCE,
                         mappings={"http://ps.example": "http://127.0.0.1:12001",
                                   RESOURCE: "http://127.0.0.1:12002"})


class SogaSupervisionTests(unittest.TestCase):
    def separated_input(self):
        return {
            "resource_asserted": {
                "resource": RESOURCE, "scope": SCOPE,
                "resource_jti": "resource-1", "expires_at": NOW + 300,
            },
            "person_server_verified": {
                "person_server": PS, "sub": SUBJECT, "agent_jkt": "thumbprint",
                "mission_s256": MISSION, "mission_active": True,
                "mission_expires_at": NOW + 1800,
            },
            "agent_asserted": {"agent_id": AGENT, "justification": "bounded greeting"},
        }

    def test_exact_state_and_unavailable_required_fact_fail_closed(self):
        profile = explicit_profile(required_authority_facts=("revoked",))
        seen = []

        def evaluator(request, *, verified_authority_state):
            seen.append((request, verified_authority_state))
            raise ValueError("required verified authority facts are unavailable")

        supervisor = SogaSupervisor(profile, evaluator=evaluator)
        decision = supervisor(self.separated_input())
        self.assertEqual((decision.determination, decision.reason_code),
                         ("DENY", "soga-error"))
        self.assertEqual(supervisor.calls, 1)
        self.assertEqual(seen[0][1]["unavailable"], ("revoked", "attenuated"))

    def test_only_complete_soga_allow_becomes_allow(self):
        profile = explicit_profile(required_authority_facts=())

        def result(determination):
            return {
                "governance_determination": determination,
                "governance_decision": {"step_id": "decision-1"},
                "canonical_decision_package": {"decision": determination},
            }

        for determination, expected in (("ALLOW", "ALLOW"), ("RESTRICT", "DENY"),
                                         ("DENY", "DENY")):
            with self.subTest(determination=determination):
                supervisor = SogaSupervisor(
                    profile, evaluator=lambda request, verified_authority_state,
                    value=result(determination): value)
                self.assertEqual(supervisor(self.separated_input()).determination, expected)
        malformed = SogaSupervisor(profile, evaluator=lambda *args, **kwargs: {})
        self.assertEqual(malformed(self.separated_input()).determination, "DENY")

    def test_invalid_authority_state_is_rejected_before_bridge(self):
        for changes in ({"revoked": "false"}, {"delegation_hops": -1},
                        {"unavailable": ["unknown"]}, {"source": ""}):
            with self.subTest(changes=changes), self.assertRaises(SupervisionAdapterError):
                SogaSupervisionProfile.create(
                    verified_authority_state=authority_state(**changes),
                    required_authority_facts=(),
                    subject_governance_state="INDEPENDENT",
                    reachability="REACHABLE",
                    subject_state_source="declared-test-profile-policy",
                    reachability_source="declared-test-profile-policy")

    def test_subject_state_and_sources_are_explicit_and_exact(self):
        base = dict(
            verified_authority_state=authority_state(),
            required_authority_facts=(),
            subject_governance_state="INDEPENDENT",
            reachability="REACHABLE",
            subject_state_source="declared-test-profile-policy",
            reachability_source="declared-test-profile-policy")
        for name, value in (
                ("subject_governance_state", "typo"),
                ("reachability", "typo"),
                ("subject_state_source", ""),
                ("reachability_source", "")):
            changed = dict(base)
            changed[name] = value
            with self.subTest(name=name), self.assertRaises(SupervisionAdapterError):
                SogaSupervisionProfile.create(**changed)


class LocalhostGatewayTests(unittest.TestCase):
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
        self.supervisor = SogaSupervisor(explicit_profile(required_authority_facts=()))
        self.person_server = PersonServer(
            issuer=self.ps, agent_provider=self.ap, resource=self.resource_issuer,
            directed_subject=SUBJECT,
            missions={MISSION: Mission(MISSION, AGENT, NOW + 1800)},
            supervisor=self.supervisor, now=NOW)
        self.resource = Resource(
            issuer=self.resource_issuer, person_server=self.ps, now=NOW)
        self.ps_server = create_server(PersonServerSurface(person_server=self.person_server))
        self.resource_server = create_server(ResourceSurface(
            resource=self.resource, subject=SUBJECT, mission_s256=MISSION,
            required_scope=SCOPE))
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

    def exchange_to_resource_token(self):
        status, _, person = self.send(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        self.assertEqual(status, 200)
        person_token = person["person_token"]
        status, _, resource = self.send(
            RESOURCE, "/authorize", {"scope": SCOPE}, person_token)
        self.assertEqual(status, 200)
        return person_token, resource["resource_token"]

    def complete_exchange(self):
        person_token, resource_token = self.exchange_to_resource_token()
        status, _, auth = self.send(
            PS, "/auth-token",
            {"resource_token": resource_token, "presented_token": person_token,
             "justification": "Run one bounded interaction"})
        self.assertEqual(status, 200)
        auth_token = auth["auth_token"]
        status, headers, receipt = self.send(
            RESOURCE, "/enforce", {"action": "greet"}, auth_token)
        return person_token, resource_token, auth_token, status, headers, receipt

    def test_real_soga_supervised_four_hop_exchange_and_gateway(self):
        person, resource, auth, status, headers, receipt = self.complete_exchange()
        self.assertEqual(status, 200)
        self.assertEqual(receipt, {
            "authorization": "allowed", "mission_s256": MISSION,
            "scope": SCOPE, "subject": SUBJECT,
        })
        self.assertEqual(self.supervisor.calls, 1)
        claims = [jose.verify_compact(person, "aa-person+jwt", self.ps.jwks),
                  jose.verify_compact(resource, "aa-resource+jwt", self.resource_issuer.jwks),
                  jose.verify_compact(auth, "aa-auth+jwt", self.ps.jwks)]
        self.assertEqual([item["mission_s256"] for item in claims], [MISSION] * 3)
        self.assertEqual(headers["Cache-Control"], "no-store")

    def test_person_token_at_gateway_returns_exact_auth_requirement(self):
        person_token, resource_token = self.exchange_to_resource_token()
        status, headers, body = self.send(
            RESOURCE, "/enforce", {"action": "greet"}, person_token)
        self.assertEqual((status, body), (401, {"error": "auth_token_required"}))
        self.assertIn('requirement=auth-token', headers["AAuth-Requirement"])
        self.assertIn(resource_token, headers["AAuth-Requirement"])

    def test_body_cannot_supply_method_path_or_authority(self):
        request = self.signed(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        envelope = {"headers": request.headers, "body": request.body.decode(),
                    "authority": "attacker.example"}
        raw = json.dumps(envelope).encode()
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.ps_server.server_port, timeout=2)
        try:
            connection.request("POST", "/person-token", raw,
                               {"Content-Type": "application/json",
                                "Content-Length": str(len(raw))})
            response = connection.getresponse()
            self.assertEqual(response.status, 400)
            response.read()
        finally:
            connection.close()

    def test_signature_failure_returns_signature_error(self):
        request = self.signed(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        request.headers["signature"] = "sig=:AAAA:"
        status, headers, body = self.client.send(
            role=PS, path="/person-token", request=request)
        self.assertEqual((status, body), (401, {"error": "signature_error"}))
        self.assertIn("error=invalid_signature", headers["Signature-Error"])

    def test_soga_restrict_deny_malformed_and_exception_issue_no_auth_token(self):
        outcomes = (
            {"governance_determination": "RESTRICT",
             "governance_decision": {"step_id": "restrict-1"},
             "canonical_decision_package": {"decision": "RESTRICT"}},
            {"governance_determination": "DENY",
             "governance_decision": {"step_id": "deny-1"},
             "canonical_decision_package": {"decision": "DENY"}},
            {},
            RuntimeError("governance unavailable"),
        )
        for outcome in outcomes:
            with self.subTest(outcome=type(outcome).__name__):
                def evaluator(request, *, verified_authority_state, selected=outcome):
                    if isinstance(selected, Exception):
                        raise selected
                    return selected
                self.person_server.supervisor = SogaSupervisor(
                    explicit_profile(required_authority_facts=()), evaluator=evaluator)
                person, resource = self.exchange_to_resource_token()
                status, _, body = self.send(
                    PS, "/auth-token",
                    {"resource_token": resource, "presented_token": person,
                     "justification": "bounded greeting"})
                self.assertEqual(status, 403)
                self.assertNotIn("auth_token", body)

    def test_transport_input_errors_routes_and_methods_fail_closed(self):
        host, port = self.mapping.destination(PS)
        cases = (
            (b"{bad", "application/json", 400),
            (b"[]", "application/json", 400),
            (b"{}", "text/plain", 400),
            (json.dumps({"headers": {}, "body": "{}", "path": "/person-token"}).encode(),
             "application/json", 400),
        )
        for body, content_type, expected in cases:
            with self.subTest(body=body, content_type=content_type):
                connection = http.client.HTTPConnection(host, port, timeout=2)
                try:
                    connection.request("POST", "/person-token", body,
                                       {"Content-Type": content_type,
                                        "Content-Length": str(len(body))})
                    response = connection.getresponse()
                    self.assertEqual(response.status, expected)
                    rendered = response.read().decode()
                    self.assertNotIn("eyJ", rendered)
                finally:
                    connection.close()
        connection = http.client.HTTPConnection(host, port, timeout=2)
        try:
            connection.request("PUT", "/person-token", b"{}",
                               {"Content-Type": "application/json"})
            response = connection.getresponse()
            self.assertEqual(response.status, 405)
            response.read()
            connection.request("GET", "/unknown")
            response = connection.getresponse()
            self.assertEqual(response.status, 404)
            response.read()
        finally:
            connection.close()

    def test_missing_and_oversized_content_length_fail_without_body_read(self):
        host, port = self.mapping.destination(PS)
        for raw_length in (None, "65537", "+1", "-1", "not-a-number"):
            with self.subTest(raw_length=raw_length):
                connection = http.client.HTTPConnection(host, port, timeout=2)
                try:
                    connection.putrequest("POST", "/person-token")
                    connection.putheader("Content-Type", "application/json")
                    if raw_length is not None:
                        connection.putheader("Content-Length", raw_length)
                    connection.endheaders()
                    response = connection.getresponse()
                    self.assertEqual(response.status, 400)
                    response.read()
                finally:
                    connection.close()

    def test_client_rejects_cross_role_authority_before_connection(self):
        request = self.signed(
            PS, "/person-token", {"resource": RESOURCE, "mission_s256": MISSION})
        with self.assertRaises(LocalhostProfileError):
            self.client.send(role=RESOURCE, path="/person-token", request=request)

    def test_server_factory_rejects_every_nonprofile_bind(self):
        surface = PersonServerSurface(person_server=self.person_server)
        for host, port in (("localhost", 0), ("0.0.0.0", 0), ("::1", 0),
                           ("192.0.2.1", 0), ("127.0.0.1", -1),
                           ("127.0.0.1", 65536)):
            with self.subTest(host=host, port=port), self.assertRaises(LocalhostProfileError):
                create_server(surface, host=host, port=port)

    def test_metadata_routes_preserve_https_identity_without_discovery_claim(self):
        for server, path, issuer, role in (
            (self.ps_server, "/.well-known/aauth-person.json", PS, "person-server"),
            (self.resource_server, "/.well-known/aauth-resource.json", RESOURCE, "resource"),
        ):
            connection = http.client.HTTPConnection(
                "127.0.0.1", server.server_port, timeout=2)
            try:
                connection.request("GET", path)
                response = connection.getresponse()
                value = json.loads(response.read())
                self.assertEqual((response.status, value["issuer"], value["fixture_role"]),
                                 (200, issuer, role))
                self.assertTrue(value["test_only"])
            finally:
                connection.close()

    def test_d113_sources_remain_byte_identical(self):
        expected = {
            "identifiers.py": "54c495785fc5fc26d24e3c406bb334d0022410faff37696d40220e1b83759579",
            "tokens.py": "34f705123acb83772f9f2428409593233f004384c46b2cf96f0358615cf2dd04",
            "exchange.py": "ed82a97873f7c535917dd0ecbecf81e31287015c3dfbc77396cb3dc8675fdf0f",
            "metadata.py": "c1a473ee3f21ed4832668fadb87e9db72dbade4278f99aa35efff868db225a5a",
        }
        root = Path(__file__).parents[1] / "m02_aauth_fcf656d"
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
