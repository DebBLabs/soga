import contextlib
import io
import unittest
from unittest import mock

from g27_tip_jar.adapter import AdapterError, Invocation
from g27_tip_jar.demo import main
from g27_tip_jar.localhost import (
    LocalhostStack,
    LocalhostTransportError,
    LoopbackRecordingAdapter,
)


class G27LocalhostTests(unittest.TestCase):
    def setUp(self):
        self.stack = LocalhostStack()
        self.client = self.stack.client

    def tearDown(self):
        self.stack.close()

    def open_session(self, platform_id="misty-a"):
        grant = self.client.runtime_post("/offer", {"platform_id": platform_id})
        session = self.client.runtime_post(
            "/scan", {**grant, "channel_key": f"channel-{platform_id}"}
        )
        return grant, session

    def begin(self, session, request_id="request-1"):
        return self.client.runtime_post(
            "/request",
            {
                "request_id": request_id,
                "mission_s256": session["mission_s256"],
                "session_id": session["session_id"],
                "platform_id": session["platform_id"],
                "channel_key": session["channel_key"],
                "agent_id": "tip-jar-agent",
                "action": "greet_participant",
                "catalog_version": "catalog-v1",
            },
        )

    def deliver(self, session, request_id="request-1", decision="ALLOW"):
        return self.client.deliver(
            {
                "session_id": session["session_id"],
                "request_id": request_id,
                "decision_reference": f"decision-{request_id}",
                "decision": decision,
            }
        )

    def test_positive_cross_service_flow_preserves_pending_and_unknown_outcome(self):
        _grant, session = self.open_session()
        self.assertEqual(self.begin(session), {"request_id": "request-1", "state": "pending"})
        pending = self.client.status()
        self.assertEqual(pending["pending_request_ids"], ["request-1"])
        self.assertEqual(pending["fake_receipts"], {"misty-a": 0, "misty-b": 0})

        receipt = self.deliver(session)
        self.assertEqual(receipt["physical_outcome"], "unknown")
        self.assertEqual(receipt["phone_status"], "unknown")
        self.assertEqual(receipt["adapter_status"], "received_by_loopback_recording_surface")
        final = self.client.status()
        self.assertEqual(final["fake_receipts"], {"misty-a": 1, "misty-b": 0})
        self.assertEqual(
            [event["kind"] for event in final["events"]],
            ["request_received", "decision_received", "dispatch_recorded", "outcome_recorded"],
        )

    def test_late_allow_crossing_governance_service_loses_to_safety_stop(self):
        _grant, session = self.open_session()
        self.begin(session)
        self.client.runtime_post("/stop", {"platform_id": "misty-a"})
        with self.assertRaises(LocalhostTransportError) as caught:
            self.deliver(session)
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("session_validation", "terminal_safety_stopped"),
        )
        status = self.client.status()
        self.assertEqual(status["fake_receipts"], {"misty-a": 0, "misty-b": 0})
        self.assertEqual(
            [event["kind"] for event in status["events"]],
            ["request_received", "safety_halt", "decision_received", "decision_rejected"],
        )

    def test_wrong_target_scan_fails_without_consuming_grant(self):
        grant = self.client.runtime_post("/offer", {"platform_id": "misty-a"})
        with self.assertRaises(LocalhostTransportError) as caught:
            self.client.runtime_post(
                "/scan",
                {**grant, "platform_id": "misty-b", "channel_key": "channel-b"},
            )
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("grant_binding", "binding_mismatch"),
        )
        self.assertEqual(self.client.status()["grants"][grant["grant_id"]]["state"], "issued")

    def test_a_session_request_naming_b_fails_at_session_binding_over_http(self):
        _grant, session = self.open_session("misty-a")
        with self.assertRaises(LocalhostTransportError) as caught:
            self.client.runtime_post(
                "/request",
                {
                    "request_id": "cross-target-http-request",
                    "mission_s256": session["mission_s256"],
                    "session_id": session["session_id"],
                    "platform_id": "misty-b",
                    "channel_key": session["channel_key"],
                    "agent_id": "tip-jar-agent",
                    "action": "greet_participant",
                    "catalog_version": "catalog-v1",
                },
            )
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("session_binding", "wrong_platform"),
        )
        status = self.client.status()
        self.assertEqual(status["pending_request_ids"], [])
        self.assertEqual(status["fake_receipts"], {"misty-a": 0, "misty-b": 0})

    def test_safety_latched_platform_rejects_new_session_without_consuming_grant(self):
        _first_grant, first_session = self.open_session()
        self.client.runtime_post("/stop", {"platform_id": "misty-a"})
        next_grant = self.client.runtime_post("/offer", {"platform_id": "misty-a"})
        with self.assertRaises(LocalhostTransportError) as caught:
            self.client.runtime_post(
                "/scan",
                {**next_grant, "channel_key": "channel-misty-a-next"},
            )
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("session_admission", "safety_stopped"),
        )
        status = self.client.status()
        self.assertEqual(status["grants"][next_grant["grant_id"]]["state"], "issued")
        self.assertEqual(status["sessions"][first_session["session_id"]]["state"], "safety_stopped")
        self.assertEqual(len(status["sessions"]), 1)
        self.assertEqual(status["fake_receipts"], {"misty-a": 0, "misty-b": 0})

    def test_recording_adapter_rejects_non_loopback_configuration(self):
        with self.assertRaises(LocalhostTransportError) as caught:
            LoopbackRecordingAdapter({"misty-a": "http://192.0.2.10:8080"})
        self.assertEqual(caught.exception.code, "non_loopback_url")

    def test_missing_target_does_not_fall_back_to_other_service(self):
        adapter = LoopbackRecordingAdapter({"misty-b": self.stack.recording_urls["misty-b"]})
        invocation = Invocation(
            request_id="missing-target-request",
            decision_reference="decision-missing-target",
            mission_s256="mission-sha",
            session_id="session-missing-target",
            platform_id="misty-a",
            agent_id="tip-jar-agent",
            action="greet_participant",
            catalog_version="catalog-v1",
        )
        with self.assertRaises(AdapterError) as caught:
            adapter.dispatch(invocation, bound_platform_id="misty-a")
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("target_resolution", "unavailable_platform"),
        )
        self.assertEqual(len(self.stack.recording_services["misty-b"].received), 0)


class G27LocalhostDemoTests(unittest.TestCase):
    def test_interactive_localhost_flow_is_visible_end_to_end(self):
        output = io.StringIO()
        commands = iter(
            ["offer a", "scan", "request greet_participant", "status", "events", "allow", "events", "quit"]
        )
        with contextlib.redirect_stdout(output), mock.patch(
            "builtins.input", side_effect=lambda _prompt: next(commands)
        ):
            result = main(["localhost"])
        self.assertEqual(result, 0)
        rendered = output.getvalue()
        self.assertIn("Real loopback HTTP between local services", rendered)
        self.assertIn("request crossed localhost; state=pending", rendered)
        self.assertIn("fake A receipts: 0", rendered)
        self.assertIn("governance crossed separate service=ALLOW", rendered)
        self.assertIn("physical=unknown", rendered)
        self.assertIn("04 outcome_recorded", rendered)


if __name__ == "__main__":
    unittest.main()
