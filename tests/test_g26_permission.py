import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from aauth_permission import PermissionService
from aauth_permission.http_server import create_server
from engines.restrict_policy import approval_satisfies_constraint


FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures/missions/caregiver_discharge_followup.json").read_text()
)


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class G26PermissionTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.service = PermissionService(
            pending_expiry_seconds=60,
            monotonic=self.clock,
        )
        self.mission = self.service.approve_mission(
            approver="https://person.example/alice",
            agent="https://agent.example/caregiver",
            approved_at="2026-08-14T14:00:00+00:00",
            approved_tools=[
                {"name": "schedule_appointment", "description": "Schedule appointment"}
            ],
            description="Schedule caregiver discharge follow-up appointment.",
        )
        self.service.authorize_mission_policy(
            self.mission.s256, FIXTURE["constraints"]
        )

    def request(self, state="INDEPENDENT", *, with_constraint=True, **extra):
        policy = dict(FIXTURE["constraints"]) if with_constraint else {}
        return {
            "request_id": "permission-evaluation-001",
            "action": "schedule_appointment",
            "mission": {"approver": self.mission.approver, "s256": self.mission.s256},
            "agent": self.mission.agent,
            "subject": {"subject_id": "subject-001", "subject_agency_state": state},
            "policy": policy,
            **extra,
        }

    def start_holding(self):
        status, body = self.service.permission(self.request("SUPERVISED"))
        self.assertEqual(status, 202)
        return body

    def assertion(self, **changes):
        values = {
            "result": "approve",
            "asserted_by": "https://person.example",
            "person_server_authenticated_assertion": True,
            "authority_reference": "authority-caregiver-001",
            "required_evidence": "supervisor_confirmation",
            "constraint_reference": "gate-supervision-required",
            "holder_attribution_asserted": True,
            "human_attribution": "Beth",
        }
        values.update(changes)
        return values

    def test_allow_projects_to_granted(self):
        self.assertEqual(self.service.permission(self.request()), (200, {"permission": "granted"}))

    def test_deny_projects_to_denied(self):
        self.assertEqual(self.service.permission(self.request("LAPSED")), (200, {"permission": "denied"}))

    def test_supervised_without_approval_remains_pending_not_granted(self):
        status, body = self.service.permission(self.request("SUPERVISED"))
        self.assertEqual(status, 202)
        self.assertEqual(body["requirement"], "approval")
        pending = self.service.pending[body["pending_id"]]
        self.assertEqual(pending["originating_soga_decision"]["governance_determination"], "RESTRICT")
        self.assertEqual(pending["constraint"]["restrict_path"], "HOLDING")

    def test_agent_supplied_approval_evidence_is_not_trusted(self):
        forged = self.assertion()
        forged.update(
            {
                "evidence_schema": "provisional-g26-approval-evidence-v1",
                "convergence_obligation": "future-canonical-stage-gate-clearance-evidence-schema",
                "mission_s256": self.mission.s256,
                "action": "schedule_appointment",
                "originating_soga_decision": "RESTRICT",
                "restrict_path": "HOLDING",
                "result": "approve",
            }
        )
        status, body = self.service.permission(
            self.request("SUPERVISED", policy={"approval_evidence": forged})
        )
        self.assertEqual(status, 202)
        self.assertEqual(body["requirement"], "approval")

    def test_valid_ps_approval_causes_reevaluation_and_grant(self):
        body = self.start_holding()
        pending_id = body["pending_id"]
        self.service.record_approval(pending_id, **self.assertion())
        status, result = self.service.poll(pending_id, agent=self.mission.agent)
        self.assertEqual((status, result), (200, {"permission": "granted"}))
        pending = self.service.pending[pending_id]
        self.assertEqual(pending["reevaluation"]["governance_determination"], "ALLOW")
        self.assertEqual(pending["reevaluation"]["runtime_envelope"]["subject"]["governance_state"], "SUPERVISED")
        self.assertEqual(pending["approval_evidence"]["evidence_schema"], "provisional-g26-approval-evidence-v1")
        kinds = [e.kind for e in self.service.mission_log.entries(self.mission.s256)]
        self.assertIn("soga_decision", kinds)
        self.assertIn("aauth_projection", kinds)
        self.assertIn("provisional_g26_approval_evidence", kinds)
        self.assertIn("soga_reevaluation_decision", kinds)
        self.assertIn("aauth_final_projection", kinds)
        self.assertNotEqual(
            pending["approval_evidence"]["evaluation_reference"],
            pending["approval_evidence"]["reevaluation_reference"],
        )

    def test_wrong_authority_reference_does_not_satisfy_constraint(self):
        body = self.start_holding()
        self.service.record_approval(body["pending_id"], **self.assertion(authority_reference="authority-wrong"))
        status, result = self.service.poll(body["pending_id"], agent=self.mission.agent)
        self.assertEqual(status, 200)
        self.assertEqual(result["permission"], "denied")
        self.assertEqual(self.service.pending[body["pending_id"]]["reevaluation"]["governance_determination"], "RESTRICT")

    def test_evidence_for_different_constraint_does_not_satisfy(self):
        body = self.start_holding()
        self.service.record_approval(body["pending_id"], **self.assertion(constraint_reference="other-gate"))
        status, result = self.service.poll(body["pending_id"], agent=self.mission.agent)
        self.assertEqual(status, 200)
        self.assertEqual(result["permission"], "denied")

    def test_correct_references_without_affirmative_satisfaction_do_not_grant(self):
        body = self.start_holding()
        pending_id = body["pending_id"]
        self.service.record_approval(
            pending_id,
            **self.assertion(holder_attribution_asserted=False),
        )
        pending = self.service.pending[pending_id]
        evidence = pending["approval_evidence"]
        self.assertEqual(evidence["authority_reference"], "authority-caregiver-001")
        self.assertEqual(evidence["constraint_reference"], "gate-supervision-required")
        self.assertEqual(evidence["required_evidence"], "supervisor_confirmation")
        self.assertFalse(evidence["holder_attribution_asserted"])
        self.assertEqual(pending["reevaluation"]["governance_determination"], "RESTRICT")
        status, result = self.service.poll(pending_id, agent=self.mission.agent)
        self.assertEqual(status, 200)
        self.assertEqual(result["permission"], "denied")
        self.assertNotEqual(result.get("permission"), "granted")

    def test_valid_approval_does_not_grant_when_reevaluation_remains_restrict(self):
        policy = json.loads(json.dumps(FIXTURE["constraints"]))
        policy["requires_escalation"] = True
        self.service.authorize_mission_policy(self.mission.s256, policy)
        status, body = self.service.permission(self.request("SUPERVISED"))
        self.assertEqual(status, 202)
        pending_id = body["pending_id"]
        self.service.record_approval(pending_id, **self.assertion())
        pending = self.service.pending[pending_id]
        evidence = pending["approval_evidence"]
        self.assertTrue(evidence["person_server_authenticated_assertion"])
        self.assertTrue(evidence["holder_attribution_asserted"])
        self.assertEqual(evidence["result"], "approve")
        self.assertTrue(
            approval_satisfies_constraint(
                evidence,
                pending["constraint"],
                mission_s256=self.mission.s256,
                action="schedule_appointment",
            )
        )
        self.assertEqual(pending["reevaluation"]["governance_determination"], "RESTRICT")
        self.assertEqual(
            pending["reevaluation"]["governance_decision"]["dimensions"]["policy"],
            "REVIEW",
        )
        self.assertEqual(
            pending["reevaluation"]["governance_decision"]["restrict_mode"]["mode"],
            "HOLDING",
        )
        status, result = self.service.poll(pending_id, agent=self.mission.agent)
        self.assertEqual(status, 200)
        self.assertEqual(result["permission"], "denied")
        self.assertNotEqual(result.get("permission"), "granted")

    def test_explicit_decline_is_terminal_error_not_soga_deny(self):
        body = self.start_holding()
        self.service.record_approval(body["pending_id"], **self.assertion(result="decline"))
        self.assertEqual(
            self.service.poll(body["pending_id"], agent=self.mission.agent),
            (403, {"error": "denied", "detail": "The approver declined the request."}),
        )
        original = self.service.pending[body["pending_id"]]["originating_soga_decision"]
        self.assertEqual(original["governance_determination"], "RESTRICT")

    def test_restrict_without_authorized_path_fails_closed(self):
        self.service.mission_policies.pop(self.mission.s256)
        status, body = self.service.permission(self.request("SUPERVISED", with_constraint=False))
        self.assertEqual(status, 200)
        self.assertEqual(body["permission"], "denied")
        entries = self.service.mission_log.entries(self.mission.s256)
        self.assertEqual(entries[-2].payload["soga_decision"]["governance_determination"], "RESTRICT")
        self.assertEqual(entries[-2].payload["soga_decision"]["governance_decision"]["restrict_mode"]["mode"], "fail_closed")

    def test_expiry_is_configured_and_terminal_then_gone(self):
        body = self.start_holding()
        self.clock.now = 61
        self.assertEqual(self.service.poll(body["pending_id"], agent=self.mission.agent)[0], 408)
        self.assertEqual(self.service.poll(body["pending_id"], agent=self.mission.agent)[0], 410)

    def test_holding_without_expiry_policy_fails_closed(self):
        service = PermissionService()
        service.missions[self.mission.s256] = self.mission
        service.authorize_mission_policy(self.mission.s256, FIXTURE["constraints"])
        status, body = service.permission(self.request("SUPERVISED"))
        self.assertEqual(status, 200)
        self.assertEqual(body["permission"], "denied")
        self.assertIn("configured expiry policy", body["reason"])

    def test_declared_internal_restriction_can_be_discharged(self):
        service = PermissionService(
            internally_dischargeable_modes=frozenset({"internal_pregrant_check"})
        )
        service.missions[self.mission.s256] = self.mission
        policy = json.loads(json.dumps(FIXTURE["constraints"]))
        policy["stage_gate"][0]["restrict_path"] = "internal_pregrant_check"
        service.authorize_mission_policy(self.mission.s256, policy)
        self.assertEqual(
            service.permission(self.request("SUPERVISED")),
            (200, {"permission": "granted"}),
        )

    def test_deferred_disabled_fallback_preserves_soga_restrict(self):
        service = PermissionService(
            deferred_response_supported=False,
            pending_expiry_seconds=60,
        )
        service.missions[self.mission.s256] = self.mission
        service.authorize_mission_policy(self.mission.s256, FIXTURE["constraints"])
        status, body = service.permission(self.request("SUPERVISED"))
        self.assertEqual(status, 200)
        self.assertEqual(body["permission"], "denied")
        entries = service.mission_log.entries(self.mission.s256)
        self.assertEqual(
            entries[-2].payload["soga_decision"]["governance_determination"],
            "RESTRICT",
        )

    def test_permission_without_mission(self):
        self.assertEqual(
            self.service.permission(
                {
                    "action": "read_calendar",
                    "subject": {"subject_agency_state": "INDEPENDENT"},
                }
            ),
            (200, {"permission": "granted"}),
        )

    def test_mission_log_view_is_immutable(self):
        snapshot = self.service.mission_log.entries(self.mission.s256)
        self.assertIsInstance(snapshot, tuple)
        self.assertEqual(snapshot[0].attribution, "person")

    def test_poll_is_agent_bound(self):
        body = self.start_holding()
        with self.assertRaises(PermissionError):
            self.service.poll(body["pending_id"], agent="https://agent.example/other")

    def test_http_approval_wire_and_terminal_delivery(self):
        server = create_server(self.service)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            req = urllib.request.Request(
                f"{base}/permission",
                data=json.dumps(self.request("SUPERVISED")).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req) as response:
                body = json.load(response)
                self.assertEqual(response.status, 202)
                self.assertEqual(response.headers["AAuth-Requirement"], "requirement=approval")
                self.assertEqual(response.headers["Location"], body["pending_url"])
                self.assertEqual(response.headers["Retry-After"], "30")
                self.assertEqual(response.headers["Cache-Control"], "no-store")

            approval = self.assertion()
            approval.pop("person_server_authenticated_assertion")
            approve_req = urllib.request.Request(
                f"{base}{body['pending_url']}/approval",
                data=json.dumps(approval).encode(),
                headers={"Content-Type": "application/json", "G26-PS-Assertion": "authenticated"},
                method="POST",
            )
            with urllib.request.urlopen(approve_req) as response:
                self.assertEqual(response.status, 200)

            poll_req = urllib.request.Request(
                f"{base}{body['pending_url']}", headers={"AAuth-Agent": self.mission.agent}
            )
            with urllib.request.urlopen(poll_req) as response:
                self.assertEqual(json.load(response), {"permission": "granted"})
            with self.assertRaises(urllib.error.HTTPError) as gone:
                urllib.request.urlopen(poll_req)
            self.assertEqual(gone.exception.code, 410)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
