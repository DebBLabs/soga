import unittest

from g27_tip_jar.runtime import RuntimeErrorAtStage

from m01_qr import (
    ACTION,
    AGENT_ID,
    APPROVER_ID,
    M01Flow,
    M01FlowError,
    MistySignalLightAdapter,
    build_mission,
)
from m01_qr.flow import PLATFORM_ID


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class M01QRTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.flow = M01Flow(monotonic=self.clock)

    def test_authorized_native_mission_is_deterministic_and_single_action(self):
        mission = build_mission()
        self.assertEqual(mission.approver, APPROVER_ID)
        self.assertEqual(mission.agent, AGENT_ID)
        self.assertEqual([tool.name for tool in mission.approved_tools], [ACTION])
        self.assertEqual(mission.s256, build_mission().s256)

    def test_positive_qr_path_reaches_soga_and_records_one_unknown_outcome(self):
        offer = self.flow.offer(grant_id="grant-positive")
        receipt = self.flow.scan_and_request(
            offer.qr_payload,
            channel_key="channel-positive",
            request_id="request-positive",
        )
        self.assertEqual(receipt["governance_projection"], "granted")
        self.assertEqual(receipt["execution_surface"], "recording_only")
        self.assertEqual(receipt["physical_outcome"], "unknown")
        self.assertEqual(len(self.flow.surface.received), 1)
        self.assertEqual(self.flow.surface.received[0]["platform_id"], PLATFORM_ID)
        self.assertEqual(self.flow.surface.received[0]["action"], ACTION)
        self.assertEqual(
            self.flow.surface.received[0]["decision_reference"],
            "receipt-request-positive",
        )
        self.assertEqual(
            [
                entry.kind
                for entry in self.flow.person_server.mission_log.entries(
                    self.flow.mission.s256
                )
            ],
            ["mission_approved", "soga_decision", "aauth_projection"],
        )
        soga_entry = self.flow.person_server.mission_log.entries(
            self.flow.mission.s256
        )[1]
        subject = soga_entry.payload["soga_decision"]["runtime_envelope"]["subject"]
        self.assertEqual(subject["subject_id"], "m01-anonymous-participant-session")
        self.assertEqual(subject["context"]["identity_status"], "UNKNOWN")
        self.assertEqual(subject["context"]["age_status"], "UNKNOWN")
        self.assertEqual(
            soga_entry.payload["soga_decision"]["runtime_envelope"]["policy"],
            {"mission_s256": self.flow.mission.s256},
        )

    def test_qr_contains_no_action_target_or_network_address(self):
        payload = self.flow.offer(grant_id="opaque-reference-1").qr_payload
        self.assertEqual(payload, "m01-grant:opaque-reference-1")
        self.assertNotIn(ACTION, payload)
        self.assertNotIn(PLATFORM_ID, payload)
        self.assertNotIn("http", payload)

    def test_replay_does_not_create_second_session_or_dispatch(self):
        offer = self.flow.offer(grant_id="grant-replay")
        self.flow.scan_and_request(
            offer.qr_payload,
            channel_key="channel-replay",
            request_id="request-replay",
        )
        with self.assertRaises(RuntimeErrorAtStage) as caught:
            self.flow.scan_and_request(
                offer.qr_payload,
                channel_key="channel-replay-2",
                request_id="request-replay-2",
            )
        self.assertEqual((caught.exception.stage, caught.exception.code),
                         ("grant_consumption", "reused_or_invalid"))
        self.assertEqual(len(self.flow.surface.received), 1)

    def test_wrong_action_fails_before_grant_consumption_or_dispatch(self):
        offer = self.flow.offer(grant_id="grant-wrong-action")
        with self.assertRaises(M01FlowError) as caught:
            self.flow.scan_and_request(
                offer.qr_payload,
                channel_key="channel-wrong-action",
                request_id="request-wrong-action",
                requested_action="m01.speak_phrase",
            )
        self.assertEqual((caught.exception.stage, caught.exception.code),
                         ("catalog", "action_not_authorized"))
        self.assertEqual(self.flow.sessions.inspect("grant-wrong-action")["state"], "issued")
        self.assertEqual(self.flow.surface.received, ())

    def test_invalid_qr_fails_without_session_or_dispatch(self):
        with self.assertRaises(M01FlowError) as caught:
            self.flow.scan_and_request(
                "https://192.168.1.183/api/led",
                channel_key="channel-invalid",
                request_id="request-invalid",
            )
        self.assertEqual((caught.exception.stage, caught.exception.code),
                         ("qr", "invalid_format"))
        self.assertEqual(self.flow.sessions.sessions, {})
        self.assertEqual(self.flow.surface.received, ())

    def test_safety_latch_blocks_session_without_consuming_grant(self):
        offer = self.flow.offer(grant_id="grant-safety")
        self.flow.runtime.safety_stop(PLATFORM_ID)
        with self.assertRaises(Exception) as caught:
            self.flow.scan_and_request(
                offer.qr_payload,
                channel_key="channel-safety",
                request_id="request-safety",
            )
        self.assertIn("session_admission: safety_stopped", str(caught.exception))
        self.assertEqual(self.flow.sessions.inspect("grant-safety")["state"], "issued")
        self.assertEqual(self.flow.surface.received, ())

    def test_prepared_misty_adapter_runs_governed_path_with_fake_transport(self):
        calls = []

        def fake_transport(url, payload):
            calls.append((url, dict(payload)))
            return {"status": "Success"}

        platform_id = "m01-misty-a-explicit-test-fixture"
        adapter = MistySignalLightAdapter(
            platform_id=platform_id,
            api_base_url="http://127.0.0.1:30001/api",
            transport=fake_transport,
            wait=lambda seconds: calls.append(("wait", seconds)),
            duration_seconds=1.0,
        )
        flow = M01Flow(
            monotonic=self.clock,
            platform_id=platform_id,
            execution_adapter=adapter,
        )
        receipt = flow.scan_and_request(
            flow.offer(grant_id="grant-prepared-adapter").qr_payload,
            channel_key="channel-prepared-adapter",
            request_id="request-prepared-adapter",
        )
        self.assertEqual(
            calls,
            [
                ("http://127.0.0.1:30001/api/led", {"red": 255, "green": 105, "blue": 180}),
                ("wait", 1.0),
                ("http://127.0.0.1:30001/api/led", {"red": 255, "green": 255, "blue": 0}),
            ],
        )
        self.assertEqual(receipt["adapter_status"], "robot_api_acknowledged")
        self.assertEqual(receipt["signal_adapter_status"], "robot_api_acknowledged")
        self.assertEqual(receipt["wait_status"], "completed")
        self.assertEqual(receipt["execution_surface"], "misty_api_transport")
        self.assertEqual(receipt["physical_outcome"], "unknown")
        self.assertEqual(receipt["neutral_outcome"], "unknown")
        self.assertEqual(receipt["neutral_adapter_status"], "robot_api_acknowledged")

    def test_prepared_misty_adapter_has_no_default_target(self):
        with self.assertRaises(Exception):
            MistySignalLightAdapter(
                platform_id="m01-misty-a",
                api_base_url="",
                transport=lambda _url, _payload: {"status": "Success"},
                wait=lambda _seconds: None,
                duration_seconds=1.0,
            )

    def test_signal_transport_error_still_attempts_neutral_and_seals_replay(self):
        calls = []

        def uncertain_signal_transport(url, payload):
            calls.append((url, dict(payload)))
            if len(calls) == 1:
                raise TimeoutError("response timeout after possible delivery")
            return {"status": "Success"}

        platform_id = "m01-misty-a-error-fixture"
        adapter = MistySignalLightAdapter(
            platform_id=platform_id,
            api_base_url="http://127.0.0.1:30002/api",
            transport=uncertain_signal_transport,
            wait=lambda _seconds: None,
            duration_seconds=1.0,
        )
        flow = M01Flow(
            monotonic=self.clock,
            platform_id=platform_id,
            execution_adapter=adapter,
        )
        receipt = flow.scan_and_request(
            flow.offer(grant_id="grant-uncertain-signal").qr_payload,
            channel_key="channel-uncertain-signal",
            request_id="request-uncertain-signal",
        )
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[1][1], {"red": 255, "green": 255, "blue": 0})
        self.assertEqual(receipt["adapter_status"], "robot_api_incomplete")
        self.assertEqual(receipt["signal_adapter_status"], "transport_error")
        self.assertEqual(receipt["neutral_adapter_status"], "robot_api_acknowledged")
        self.assertEqual(receipt["physical_outcome"], "unknown")
        self.assertEqual(receipt["neutral_outcome"], "unknown")

        replay_receipt = adapter.dispatch(
            adapter._invocations["request-uncertain-signal"],
            bound_platform_id=platform_id,
        )
        self.assertEqual(replay_receipt, {
            key: receipt[key]
            for key in replay_receipt
        })
        self.assertEqual(len(calls), 2)

    def test_duration_must_be_positive_and_at_most_five_seconds(self):
        for duration in (0, -1, 5.1):
            with self.assertRaises(Exception):
                MistySignalLightAdapter(
                    platform_id="m01-misty-a-duration-fixture",
                    api_base_url="http://127.0.0.1:30003/api",
                    transport=lambda _url, _payload: {"status": "Success"},
                    wait=lambda _seconds: None,
                    duration_seconds=duration,
                )


if __name__ == "__main__":
    unittest.main()
