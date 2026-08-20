import threading
import unittest

from g27_tip_jar.adapter import AdapterError, FakeSurface, Invocation, TargetBoundAdapter
from g27_tip_jar.lifecycle import GrantState, LifecycleError, SessionGrantService, SessionState
from g27_tip_jar.runtime import ActionDecision, Decision, PrototypeRuntime, RuntimeErrorAtStage
from g27_tip_jar.state_machine import OperatingState, SafetyStateMachine, StateTransitionError


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class G27TipJarTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.service = SessionGrantService(monotonic=self.clock)
        self.surface_a = FakeSurface("misty-a")
        self.surface_b = FakeSurface("misty-b")
        self.adapter = TargetBoundAdapter(
            {"misty-a": self.surface_a, "misty-b": self.surface_b}
        )
        self.machine_a = SafetyStateMachine("misty-a")
        self.machine_b = SafetyStateMachine("misty-b")
        self.runtime = PrototypeRuntime(
            sessions=self.service,
            adapter=self.adapter,
            state_machines={"misty-a": self.machine_a, "misty-b": self.machine_b},
        )

    def issue(self, platform_id="misty-a", grant_id=None):
        return self.service.issue_grant(
            mission_s256="mission-sha",
            platform_id=platform_id,
            notice_version="notice-v1",
            policy_version="policy-v1",
            issuer="person-server",
            grant_id=grant_id,
        )

    def consume(self, grant, channel_key="channel-a"):
        return self.service.initiate_and_consume(
            grant.grant_id,
            platform_id=grant.platform_id,
            mission_s256=grant.mission_s256,
            notice_version=grant.notice_version,
            policy_version=grant.policy_version,
            channel_key=channel_key,
        )

    def invocation(self, session, request_id="request-1", platform_id=None):
        return Invocation(
            request_id=request_id,
            decision_reference="decision-1",
            mission_s256=session.mission_s256,
            session_id=session.session_id,
            platform_id=platform_id or session.platform_id,
            agent_id="tip-jar-agent",
            action="greet_participant",
            catalog_version="catalog-v1",
        )

    def decision(self, session, request_id="request-1", decision=Decision.ALLOW, **changes):
        values = {
            "request_id": request_id,
            "decision_reference": "decision-1",
            "decision": decision,
            "mission_s256": session.mission_s256,
            "session_id": session.session_id,
            "platform_id": session.platform_id,
            "agent_id": "tip-jar-agent",
            "action": "greet_participant",
            "catalog_version": "catalog-v1",
        }
        values.update(changes)
        return ActionDecision(**values)

    def assert_lifecycle_error(self, stage, code, call):
        with self.assertRaises(LifecycleError) as caught:
            call()
        self.assertEqual((caught.exception.stage, caught.exception.code), (stage, code))

    def assert_adapter_error(self, stage, code, call):
        with self.assertRaises(AdapterError) as caught:
            call()
        self.assertEqual((caught.exception.stage, caught.exception.code), (stage, code))

    def test_positive_control_a_records_once_b_unchanged_and_outcome_unknown(self):
        session = self.consume(self.issue())
        receipt = self.runtime.submit(self.decision(session), channel_key=session.channel_key)
        self.assertEqual(receipt["adapter_status"], "received_by_recording_surface")
        self.assertEqual(receipt["physical_outcome"], "unknown")
        self.assertEqual(receipt["phone_status"], "unknown")
        self.assertEqual(len(self.surface_a.received), 1)
        self.assertEqual(self.surface_b.received, ())

    def test_negative_a_credential_presented_to_b_fails_at_grant_binding_without_consumption(self):
        grant = self.issue("misty-a")
        self.assert_lifecycle_error(
            "grant_binding",
            "binding_mismatch",
            lambda: self.service.initiate_and_consume(
                grant.grant_id,
                platform_id="misty-b",
                mission_s256=grant.mission_s256,
                notice_version=grant.notice_version,
                policy_version=grant.policy_version,
                channel_key="channel-b",
            ),
        )
        self.assertEqual(grant.state, GrantState.ISSUED)

    def test_negative_a_session_request_to_b_fails_at_session_binding(self):
        session = self.consume(self.issue())
        self.assert_lifecycle_error(
            "session_binding",
            "wrong_platform",
            lambda: self.service.validate_session(
                session.session_id,
                channel_key=session.channel_key,
                platform_id="misty-b",
            ),
        )

    def test_negative_a_decision_to_b_adapter_fails_at_target_binding(self):
        session = self.consume(self.issue())
        self.assert_adapter_error(
            "target_binding",
            "wrong_platform",
            lambda: self.adapter.dispatch(
                self.invocation(session), bound_platform_id="misty-b"
            ),
        )
        self.assertEqual(self.surface_a.received, ())
        self.assertEqual(self.surface_b.received, ())

    def test_negative_missing_a_surface_does_not_fall_back_to_b(self):
        adapter = TargetBoundAdapter({"misty-b": self.surface_b})
        session = self.consume(self.issue())
        self.assert_adapter_error(
            "target_resolution",
            "unavailable_platform",
            lambda: adapter.dispatch(self.invocation(session), bound_platform_id="misty-a"),
        )
        self.assertEqual(self.surface_b.received, ())

    def test_negative_concurrent_replay_consumes_grant_once_at_grant_consumption(self):
        grant = self.issue(grant_id="collision-grant")
        barrier = threading.Barrier(3)
        results = []

        def scan(channel):
            barrier.wait()
            try:
                self.consume(grant, channel)
                results.append(("created", None))
            except LifecycleError as exc:
                results.append((exc.stage, exc.code))

        threads = [threading.Thread(target=scan, args=(f"channel-{i}",)) for i in range(2)]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join()
        self.assertEqual(results.count(("created", None)), 1)
        self.assertEqual(results.count(("grant_consumption", "reused_or_invalid")), 1)
        self.assertEqual(len(self.service.sessions), 1)

    def test_negative_second_live_session_fails_at_session_concurrency_without_consuming_grant(self):
        self.consume(self.issue("misty-a"))
        second = self.issue("misty-b")
        self.assert_lifecycle_error(
            "session_concurrency", "active_session_exists", lambda: self.consume(second, "channel-b")
        )
        self.assertEqual(second.state, GrantState.ISSUED)

    def test_negative_two_different_grants_race_for_one_live_session_slot(self):
        grants = [
            self.issue("misty-a", grant_id="slot-race-a"),
            self.issue("misty-b", grant_id="slot-race-b"),
        ]
        barrier = threading.Barrier(3)
        results = []

        def scan(grant):
            barrier.wait()
            try:
                session = self.consume(grant, f"channel-{grant.platform_id}")
                results.append((grant.grant_id, "created", session.session_id))
            except LifecycleError as exc:
                results.append((grant.grant_id, exc.stage, exc.code))

        threads = [threading.Thread(target=scan, args=(grant,)) for grant in grants]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join()

        created = [result for result in results if result[1] == "created"]
        rejected = [
            result
            for result in results
            if result[1:] == ("session_concurrency", "active_session_exists")
        ]
        self.assertEqual(len(created), 1)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(len(self.service.sessions), 1)
        states = {grant.grant_id: grant.state for grant in grants}
        self.assertEqual(states[created[0][0]], GrantState.CONSUMED)
        self.assertEqual(states[rejected[0][0]], GrantState.ISSUED)

    def test_negative_duplicate_action_request_returns_prior_receipt_without_second_invocation(self):
        session = self.consume(self.issue())
        invocation = self.invocation(session)
        first = self.adapter.dispatch(invocation, bound_platform_id="misty-a")
        second = self.adapter.dispatch(invocation, bound_platform_id="misty-a")
        self.assertEqual(first, second)
        self.assertEqual(len(self.surface_a.received), 1)

    def test_negative_duplicate_request_id_with_changed_binding_fails_at_idempotency(self):
        session = self.consume(self.issue())
        original = self.invocation(session)
        self.adapter.dispatch(original, bound_platform_id="misty-a")
        changed = self.invocation(session, platform_id="misty-b")
        self.assert_adapter_error(
            "idempotency",
            "request_binding_conflict",
            lambda: self.adapter.dispatch(changed, bound_platform_id="misty-b"),
        )
        self.assertEqual(len(self.surface_a.received), 1)
        self.assertEqual(self.surface_b.received, ())

    def test_negative_deny_stops_at_decision_without_adapter_invocation(self):
        session = self.consume(self.issue())
        receipt = self.runtime.submit(
            self.decision(session, decision=Decision.DENY),
            channel_key=session.channel_key,
        )
        self.assertEqual(receipt["adapter_status"], "not_dispatched")
        self.assertEqual(receipt["phone_status"], "degraded")
        self.assertEqual(self.machine_a.state, OperatingState.NEUTRAL)
        self.assertEqual(self.surface_a.received, ())

    def test_negative_runtime_duplicate_request_with_changed_decision_fails_at_idempotency(self):
        session = self.consume(self.issue())
        original = self.runtime.submit(
            self.decision(session, decision=Decision.DENY),
            channel_key=session.channel_key,
        )
        self.assertEqual(original["decision"], "DENY")
        with self.assertRaises(RuntimeErrorAtStage) as caught:
            self.runtime.submit(
                self.decision(session, decision=Decision.ALLOW),
                channel_key=session.channel_key,
            )
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("idempotency", "request_binding_conflict"),
        )
        self.assertEqual(self.surface_a.received, ())

    def test_negative_wrong_mission_stops_at_decision_binding(self):
        session = self.consume(self.issue())
        with self.assertRaises(RuntimeErrorAtStage) as caught:
            self.runtime.submit(
                self.decision(session, mission_s256="other-mission"),
                channel_key=session.channel_key,
            )
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("decision_binding", "wrong_mission"),
        )
        self.assertEqual(self.surface_a.received, ())

    def test_audit_receipts_do_not_retain_presented_grant_handle(self):
        grant = self.issue(grant_id="presented-bearer-handle")
        self.consume(grant)
        serialized = repr(self.service.receipts)
        self.assertNotIn("presented-bearer-handle", serialized)
        self.assertIn("grant_digest", serialized)

    def test_invalidated_grant_is_terminal_for_initiation(self):
        grant = self.issue()
        self.service.invalidate_grant(grant.grant_id)
        self.assertEqual(grant.state, GrantState.INVALIDATED)
        self.assert_lifecycle_error(
            "grant_consumption", "reused_or_invalid", lambda: self.consume(grant)
        )

    def test_negative_expired_grant_fails_at_grant_validation(self):
        grant = self.issue()
        self.clock.now = 600
        self.assert_lifecycle_error(
            "grant_validation", "expired", lambda: self.consume(grant)
        )
        self.assertEqual(grant.state, GrantState.EXPIRED)

    def test_negative_idle_timeout_fails_at_session_validation_and_cannot_revive(self):
        session = self.consume(self.issue())
        self.clock.now = 60
        self.assert_lifecycle_error(
            "session_validation",
            "terminal_expired",
            lambda: self.service.validate_session(
                session.session_id,
                channel_key=session.channel_key,
                platform_id=session.platform_id,
                participant_activity=True,
            ),
        )
        self.assertEqual(session.state, SessionState.EXPIRED)

    def test_negative_internal_polling_does_not_extend_idle_timeout(self):
        session = self.consume(self.issue())
        self.clock.now = 59
        self.service.validate_session(
            session.session_id,
            channel_key=session.channel_key,
            platform_id=session.platform_id,
            participant_activity=False,
        )
        self.assertEqual(session.idle_expires_at, 60)

    def test_negative_participant_activity_never_extends_hard_maximum(self):
        session = self.consume(self.issue())
        self.clock.now = 290
        session.idle_expires_at = 295
        self.service.validate_session(
            session.session_id,
            channel_key=session.channel_key,
            platform_id=session.platform_id,
            participant_activity=True,
        )
        self.assertEqual(session.idle_expires_at, session.hard_expires_at)

    def test_negative_wrong_channel_fails_at_channel_binding(self):
        session = self.consume(self.issue())
        self.assert_lifecycle_error(
            "channel_binding",
            "wrong_channel",
            lambda: self.service.validate_session(
                session.session_id, channel_key="other", platform_id=session.platform_id
            ),
        )

    def test_negative_terminal_session_cannot_be_revived(self):
        session = self.consume(self.issue())
        self.service.terminate(session.session_id, SessionState.WITHDRAWN)
        self.assert_lifecycle_error(
            "session_validation",
            "terminal_withdrawn",
            lambda: self.service.validate_session(
                session.session_id,
                channel_key=session.channel_key,
                platform_id=session.platform_id,
                participant_activity=True,
            ),
        )

    def test_negative_missing_adapter_binding_fails_at_decision_binding(self):
        session = self.consume(self.issue())
        bad = Invocation(
            request_id="request-bad",
            decision_reference="",
            mission_s256=session.mission_s256,
            session_id=session.session_id,
            platform_id="misty-a",
            agent_id="tip-jar-agent",
            action="greet_participant",
            catalog_version="catalog-v1",
        )
        self.assert_adapter_error(
            "decision_binding",
            "missing_binding",
            lambda: self.adapter.dispatch(bad, bound_platform_id="misty-a"),
        )

    def test_negative_pending_stale_request_cannot_accept_late_allow(self):
        machine = SafetyStateMachine("misty-a")
        machine.enter_pending("request-1")
        machine.make_request_stale("request-1")
        self.assertEqual(machine.state, OperatingState.DEGRADED)
        with self.assertRaises(StateTransitionError) as caught:
            machine.resolve_pending(
                request_id="request-1", allow=True, common_gate_satisfied=True
            )
        self.assertEqual(str(caught.exception), "wrong_pending_request")

    def test_negative_safety_halt_wins_race_with_allow(self):
        machine = SafetyStateMachine("misty-a")
        machine.enter_pending("request-1")
        machine.safety_stop()
        state = machine.resolve_pending(
            request_id="request-1", allow=True, common_gate_satisfied=True
        )
        self.assertEqual(state, OperatingState.SAFETY_STOPPED)
        self.assertTrue(machine.safety_latched)

    def test_negative_runtime_safety_stop_terminates_session_and_blocks_later_action(self):
        session = self.consume(self.issue())
        self.runtime.safety_stop("misty-a")
        self.assertEqual(session.state, SessionState.SAFETY_STOPPED)
        with self.assertRaises(RuntimeErrorAtStage) as caught:
            self.runtime.submit(self.decision(session), channel_key=session.channel_key)
        self.assertEqual(
            (caught.exception.stage, caught.exception.code),
            ("session_validation", "terminal_safety_stopped"),
        )
        self.assertEqual(self.surface_a.received, ())

    def test_negative_safety_stop_release_rejects_all_five_automatic_clear_paths(self):
        machine = SafetyStateMachine("misty-a")
        machine.safety_stop()
        for cause in (
            "network_restoration",
            "late_allow",
            "adapter_process_restart",
            "participant_retry",
            "release_of_misty_b",
        ):
            with self.subTest(cause=cause):
                self.assertFalse(machine.attempt_automatic_release(cause))
                self.assertEqual(machine.state, OperatingState.SAFETY_STOPPED)
                self.assertTrue(machine.safety_latched)

    def test_negative_operator_release_requires_correct_platform_and_verified_neutral(self):
        machine = SafetyStateMachine("misty-a")
        machine.safety_stop()
        self.assertFalse(
            machine.operator_release(
                platform_id="misty-b", conditions_verified=True, neutral_established=True
            )
        )
        self.assertFalse(
            machine.operator_release(
                platform_id="misty-a", conditions_verified=True, neutral_established=False
            )
        )
        self.assertTrue(machine.safety_latched)

    def test_operator_release_enters_neutral_without_resuming_request(self):
        machine = SafetyStateMachine("misty-a")
        machine.enter_pending("request-1")
        machine.safety_stop()
        self.assertTrue(
            machine.operator_release(
                platform_id="misty-a", conditions_verified=True, neutral_established=True
            )
        )
        self.assertEqual(machine.state, OperatingState.NEUTRAL)
        self.assertIsNone(machine.request_id)

    def test_degraded_status_remains_phone_visible_after_neutral_presentation(self):
        machine = SafetyStateMachine("misty-a")
        machine.enter_pending("request-1")
        machine.resolve_pending(
            request_id="request-1", allow=False, common_gate_satisfied=False
        )
        machine.finish_degraded_presentation()
        self.assertEqual(machine.state, OperatingState.NEUTRAL)
        self.assertEqual(machine.phone_status, "degraded")

    def test_unknown_physical_outcome_is_not_promoted_to_completed(self):
        machine = SafetyStateMachine("misty-a")
        machine.enter_pending("request-1")
        machine.resolve_pending(
            request_id="request-1", allow=True, common_gate_satisfied=True
        )
        self.assertEqual(machine.action_finished(observed=False), "unknown")
        self.assertEqual(machine.phone_status, "unknown")


if __name__ == "__main__":
    unittest.main()
