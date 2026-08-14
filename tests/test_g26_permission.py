import unittest
import json
import threading
import urllib.request

from aauth_permission import PermissionService
from aauth_permission.http_server import create_server


class G26PermissionTests(unittest.TestCase):
    def setUp(self):
        self.service = PermissionService()
        self.mission = self.service.approve_mission(
            approver="https://person.example/alice",
            agent="https://agent.example/caregiver",
            approved_at="2026-08-14T14:00:00+00:00",
            approved_tools=[{"name": "schedule_visit", "description": "Schedule visit"}],
            description="Arrange an approved caregiver visit.",
        )

    def request(self, state="INDEPENDENT", **extra):
        return {
            "action": "schedule_visit",
            "mission": {"approver": self.mission.approver, "s256": self.mission.s256},
            "subject": {"subject_id": "subject-001", "subject_agency_state": state},
            **extra,
        }

    def last_decision(self):
        return self.service.mission_log.entries(self.mission.s256)[-1].payload

    def test_allow_projects_to_granted(self):
        self.assertEqual(self.service.permission(self.request()), (200, {"permission": "granted"}))
        self.assertEqual(self.last_decision()["soga_decision"]["governance_determination"], "ALLOW")

    def test_deny_projects_to_denied(self):
        status, body = self.service.permission(self.request("LAPSED"))
        self.assertEqual((status, body), (200, {"permission": "denied"}))
        self.assertEqual(self.last_decision()["soga_decision"]["governance_determination"], "DENY")

    def test_internally_discharged_restrict_projects_to_granted(self):
        service = PermissionService(
            internally_dischargeable_modes=frozenset({"supervised_execution"})
        )
        service.missions[self.mission.s256] = self.mission
        status, body = service.permission(self.request("SUPERVISED"))
        self.assertEqual((status, body), (200, {"permission": "granted"}))
        log = service.mission_log.entries(self.mission.s256)[-1].payload
        self.assertEqual(log["soga_decision"]["governance_determination"], "RESTRICT")
        self.assertEqual(log["aauth_projection"], "granted_after_internal_discharge")

    def test_agent_participation_restrict_is_deferred_without_timeout(self):
        status, body = self.service.permission(self.request("SUPERVISED"))
        self.assertEqual(status, 202)
        self.assertEqual(body["requirement"], "interaction")
        self.assertNotIn("timeout", body)
        self.assertEqual(self.last_decision()["soga_decision"]["governance_determination"], "RESTRICT")

    def test_denied_fallback_does_not_rewrite_restrict_as_deny(self):
        service = PermissionService(deferred_response_supported=False)
        service.missions[self.mission.s256] = self.mission
        status, body = service.permission(self.request("SUPERVISED"))
        self.assertEqual(status, 200)
        self.assertEqual(body["permission"], "denied")
        entry = service.mission_log.entries(self.mission.s256)[-1].payload
        self.assertEqual(entry["soga_decision"]["governance_determination"], "RESTRICT")
        self.assertEqual(entry["aauth_projection"], "denied_with_reason_fallback")

    def test_permission_without_mission(self):
        status, body = self.service.permission({"action": "read_calendar", "subject": {"subject_agency_state": "INDEPENDENT"}})
        self.assertEqual((status, body), (200, {"permission": "granted"}))

    def test_mission_log_view_is_immutable(self):
        snapshot = self.service.mission_log.entries(self.mission.s256)
        self.assertIsInstance(snapshot, tuple)
        self.assertEqual(snapshot[0].attribution, "person")

    def test_running_http_permission_endpoint(self):
        server = create_server(self.service)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/permission"
            req = urllib.request.Request(
                url,
                data=json.dumps(self.request()).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(json.load(response), {"permission": "granted"})
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
