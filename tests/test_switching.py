"""Unexecuted integration cases for the staged gateway and lifecycle owner."""
import threading
import unittest
from dataclasses import replace

from g27_tip_jar.adapter import Invocation
from robot_gateway.gateway import RobotGatewayError
from robot_gateway.owned_gateway import OwnedRobotGateway as RobotGateway
from robot_gateway.misty_invitation import ACTION, CATALOG_VERSION, MISTY_B_PLATFORM_ID, MistyInvitationAdapter
from robot_gateway.strict_json_post import SPEAK_URL
from robot_gateway.unavailable_mbot2 import MBOT2_UNAVAILABLE_PLATFORM_ID, UnavailableMbot2Adapter
from robot_gateway.switching import RobotObservation, RobotSwitcher

MISTY = MISTY_B_PLATFORM_ID
MBOT = MBOT2_UNAVAILABLE_PLATFORM_ID


class SwitchingTests(unittest.TestCase):
    def setUp(self):
        self.now = 0.0
        self.count = 0
        self.transport_mode = "ok"
        self.entered = threading.Event()
        self.resume = threading.Event()

        def transport(url, payload):
            if url == SPEAK_URL:
                if self.transport_mode == "blocked":
                    self.entered.set()
                    if not self.resume.wait(1.0):
                        raise RuntimeError("test_dispatch_deadline")
                if self.transport_mode == "error":
                    raise RuntimeError("transport_failure")
            return {"status": "Success", "result": True}

        self.adapters = {MISTY: MistyInvitationAdapter(transport), MBOT: UnavailableMbot2Adapter()}
        self.owner = RobotSwitcher(
            self.adapters,
            completion_verifiers={key: self.verify for key in self.adapters},
            neutral_verifiers={key: self.verify for key in self.adapters},
            authorize=self.authorize, monotonic=lambda: self.now, run_id="boot-1",
        )
        for key in self.adapters:
            self.owner.startup_neutral(self.observation(key, "startup", "startup", "startup", "neutral", "boot-" + key))
        self.owner.select(MISTY)

    def verify(self, observation, invocation):
        if invocation is not None:
            self.assertEqual(observation.session_id, invocation.session_id)
            self.assertEqual(observation.decision_reference, invocation.decision_reference)
        return observation.proof != "invalid"

    def authorize(self, platform, session, decision):
        self.count += 1
        return Invocation(
            request_id="r" + str(self.count), decision_reference=decision,
            mission_s256="a" * 64, session_id=session, platform_id=platform,
            agent_id="operator", action=ACTION, catalog_version=CATALOG_VERSION,
        )

    def observation(self, platform, request, session, decision, kind, proof):
        return RobotObservation("boot-1", platform, request, session, decision, kind, proof)

    def active_observation(self, kind, proof="proof"):
        record = self.owner.state["record"]
        return self.observation(record["platform_id"], record["request_id"], record["session_id"],
                                record["decision_reference"], kind, proof)

    def start(self):
        return self.owner.allow_open(session_id="s1", decision_reference="d1")

    def normal_finish(self):
        self.owner.completed(self.active_observation("completed", "done"))
        self.owner.finish()
        self.owner.neutral(self.active_observation("neutral", "neutral"))

    def test_verified_neutral_then_switch(self):
        self.start()
        self.owner.completed(self.active_observation("completed", "done"))
        self.owner.finish()
        self.assertEqual(self.owner.state["phase"], "WAIT_NEUTRAL")
        with self.assertRaises(RobotGatewayError):
            self.owner.select(MBOT)
        self.owner.neutral(self.active_observation("neutral", "neutral"))
        self.owner.select(MBOT)
        self.assertTrue(self.owner.state["record"]["completion_verified"])
        self.assertTrue(self.owner.state["record"]["neutral_verified"])

    def test_startup_and_direct_gateway_bypass_refused(self):
        token = object()
        gateway = RobotGateway(self.adapters, access_token=token)
        invocation = self.authorize(MISTY, "s", "d")
        with self.assertRaisesRegex(RobotGatewayError, "exclusive_owner_required"):
            gateway.reserve(invocation, bound_platform_id=MISTY)
        with self.assertRaisesRegex(RobotGatewayError, "target_not_selected"):
            gateway.reserve(invocation, bound_platform_id=MISTY, access_token=token)
        gateway.select_target(MISTY, access_token=token)
        with self.assertRaisesRegex(RobotGatewayError, "target_not_selected"):
            gateway.reserve(replace(invocation, platform_id=MBOT), bound_platform_id=MBOT, access_token=token)

    def test_session_cannot_be_reused_after_switch(self):
        self.start()
        self.normal_finish()
        self.owner.select(MBOT)
        with self.assertRaisesRegex(RobotGatewayError, "authorization_consumed"):
            self.owner.allow_open(session_id="s1", decision_reference="new")

    def test_unavailable_placeholder_does_not_lock(self):
        self.owner.select(MBOT)
        result = self.start()
        self.assertEqual(result["phase"], "IDLE")
        self.assertEqual(result["record"]["terminal_event"], "UNAVAILABLE")
        self.owner.select(MISTY)

    def test_bad_observation_and_replay(self):
        self.start()
        good = self.active_observation("completed", "one-proof")
        for bad in (replace(good, platform_id=MBOT), replace(good, session_id="other"),
                    replace(good, run_id="old"), replace(good, proof="invalid")):
            with self.assertRaises(RobotGatewayError):
                self.owner.completed(bad)
        self.owner.completed(good)
        self.owner.finish()
        with self.assertRaisesRegex(RobotGatewayError, "observation_replay"):
            self.owner.neutral(self.active_observation("neutral", "one-proof"))

    def test_missing_completion_stop_lock_and_recovery(self):
        self.start()
        self.now = 10.0
        self.owner.tick()
        state = self.owner.state
        self.assertEqual(state["phase"], "LOCKED")
        self.assertEqual(state["record"]["terminal_event"], "COMPLETION_MISSING")
        self.assertIsNotNone(state["record"]["stop_receipt"])
        self.owner.recover(self.active_observation("neutral", "recovery"))
        self.owner.select(MBOT)

    def test_neutral_wait_deadline_locks(self):
        self.start()
        self.owner.finish()
        self.now = 3.0
        self.owner.tick()
        self.assertEqual(self.owner.state["phase"], "LOCKED")
        self.owner.recover(self.active_observation("neutral", "recovery"))
        self.assertEqual(self.owner.state["phase"], "IDLE")

    def test_dispatch_failure_attempts_stop_before_recovery(self):
        self.transport_mode = "error"
        state = self.start()
        self.assertEqual(state["phase"], "LOCKED")
        self.assertIsNotNone(state["record"]["dispatch_receipt"])
        self.assertIsNotNone(state["record"]["stop_receipt"])
        self.owner.recover(self.active_observation("neutral", "recovery"))

    def test_dispatch_stop_race_preserves_both_receipts(self):
        self.transport_mode = "blocked"
        results, failures = [], []
        def dispatch():
            try:
                results.append(self.start())
            except Exception as error:
                failures.append(error)
        thread = threading.Thread(target=dispatch, daemon=True)
        thread.start()
        try:
            self.assertTrue(self.entered.wait(1.0))
            stopped = self.owner.finish()
            self.assertEqual(stopped["phase"], "LOCKED")
            with self.assertRaisesRegex(RobotGatewayError, "dispatch_still_in_flight"):
                self.owner.recover(self.active_observation("neutral", "early"))
        finally:
            self.resume.set()
            thread.join(2.0)
        self.assertFalse(thread.is_alive())
        self.assertEqual(failures, [])
        record = self.owner.state["record"]
        self.assertIsNotNone(record["stop_receipt"])
        self.assertIsNotNone(record["dispatch_receipt"])
        self.assertEqual(results[0]["phase"], "LOCKED")
        self.owner.recover(self.active_observation("neutral", "recovery"))

    def test_direct_gateway_selection_refusals(self):
        token = object()
        gateway = RobotGateway(self.adapters, access_token=token)
        gateway.select_target(MISTY, access_token=token)
        invocation = self.authorize(MISTY, "s", "d")
        gateway.reserve(invocation, bound_platform_id=MISTY, access_token=token)
        with self.assertRaisesRegex(RobotGatewayError, "invitation_already_active"):
            gateway.select_target(MBOT, access_token=token)
        gateway.release(invocation.request_id, access_token=token)
        with self.assertRaisesRegex(RobotGatewayError, "dispatch_still_in_flight"):
            gateway.select_target(MBOT, access_token=token)
        gateway.lock_for_operator_reset(access_token=token)
        with self.assertRaisesRegex(RobotGatewayError, "operator_reset_required"):
            gateway.select_target(MBOT, access_token=token)


    def test_recovery_waits_for_owner_dispatch_postprocessing(self):
        original = self.owner._gateway.dispatch_reserved
        post_ready, post_resume = threading.Event(), threading.Event()
        errors = []
        def delayed(*args, **kwargs):
            receipt = original(*args, **kwargs)
            post_ready.set()
            if not post_resume.wait(3.0):
                raise RuntimeError("test_post_deadline")
            return receipt
        self.owner._gateway.dispatch_reserved = delayed
        def dispatch():
            try:
                self.start()
            except Exception as error:
                errors.append(error)
        thread = threading.Thread(target=dispatch, daemon=True)
        thread.start()
        try:
            self.assertTrue(post_ready.wait(1.0))
            self.owner.finish()
            with self.assertRaisesRegex(RobotGatewayError, "dispatch_still_in_flight"):
                self.owner.recover(self.active_observation("neutral", "too-early"))
        finally:
            post_resume.set()
            thread.join(4.0)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        self.owner.recover(self.active_observation("neutral", "recovery"))

    def test_stop_timeout_cannot_recover_while_adapter_stop_runs(self):
        self.start()
        original = self.owner._gateway.stop
        stop_ready, stop_resume = threading.Event(), threading.Event()
        results = []
        def delayed(*args, **kwargs):
            stop_ready.set()
            if not stop_resume.wait(3.0):
                raise RuntimeError("test_stop_deadline")
            return original(*args, **kwargs)
        self.owner._gateway.stop = delayed
        thread = threading.Thread(target=lambda: results.append(self.owner.finish()), daemon=True)
        thread.start()
        try:
            self.assertTrue(stop_ready.wait(1.0))
            self.now = 3.0
            self.owner.tick()
            with self.assertRaisesRegex(RobotGatewayError, "dispatch_still_in_flight"):
                self.owner.recover(self.active_observation("neutral", "too-early"))
        finally:
            stop_resume.set()
            thread.join(4.0)
        self.assertFalse(thread.is_alive())
        self.assertEqual(results[0]["phase"], "LOCKED")
        self.owner.recover(self.active_observation("neutral", "recovery"))

    def test_terminal_record_survives_next_interaction(self):
        self.start()
        request = self.owner.state["record"]["request_id"]
        self.normal_finish()
        self.owner.select(MBOT)
        self.owner.allow_open(session_id="s2", decision_reference="d2")
        self.assertTrue(self.owner.terminal_receipt(request)["neutral_verified"])
