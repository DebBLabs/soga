"""Unexecuted deterministic synthetic integration tests."""
import unittest
from threading import RLock
from dataclasses import replace
from unittest.mock import Mock

from g27_tip_jar.adapter import Invocation
from robot_gateway.misty_invitation import MISTY_B_PLATFORM_ID, MistyInvitationAdapter, ACTION, CATALOG_VERSION
from robot_gateway.unavailable_mbot2 import MBOT2_UNAVAILABLE_PLATFORM_ID, UnavailableMbot2Adapter
from robot_gateway.switching import RobotObservation
from robot_gateway.operator_runtime import Binding, OperatorRuntime


class Repository:
    def __init__(self, grants):
        self.grants = dict(grants)
        self.invalidations = []
        self.lock = RLock()

    def consume(self, platform_id, session_id, decision_reference, boot_id):
        with self.lock:
            key = (session_id, decision_reference)
            grant = self.grants.get(key)
            if grant is None or grant.platform_id != platform_id or boot_id != "boot":
                raise RuntimeError("invalid_grant")
            del self.grants[key]
            return grant

    def invalidate(self, session_id, reason):
        with self.lock:
            self.invalidations.append((session_id, reason))
            self.grants = {key: value for key, value in self.grants.items() if key[0] != session_id}

    def invalidate_selection(self, platform_id):
        with self.lock:
            self.grants = {key: value for key, value in self.grants.items() if value.platform_id != platform_id}


class HostLocks:
    def __init__(self):
        self.held = set()

    def acquire(self, platform, endpoint):
        if endpoint in self.held:
            return None
        self.held.add(endpoint)
        return type("Lease", (), {"release": lambda lease: self.held.discard(endpoint)})()


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.now = 0.0
        self.records = []
        self.fail_persist = False
        self.misty = MISTY_B_PLATFORM_ID
        self.mbot = MBOT2_UNAVAILABLE_PLATFORM_ID
        self.grant = Invocation(
            request_id="r1", decision_reference="d1", mission_s256="a" * 64,
            session_id="s1", platform_id=self.misty, agent_id="operator",
            action=ACTION, catalog_version=CATALOG_VERSION,
        )
        self.repository = Repository({("s1", "d1"): self.grant})
        self.locks = HostLocks()
        self.bindings = [
            Binding(self.misty, "misty-b:192.168.8.219:80", MistyInvitationAdapter(lambda *args: {"result": True}), 5.5),
            Binding(self.mbot, "mbot-placeholder", UnavailableMbot2Adapter(), 0.1),
        ]
        def persist(record):
            if self.fail_persist:
                raise OSError("disk")
            self.records.append(record)
        self.options = dict(
            repository=self.repository, completion_verifiers={key: lambda *args: True for key in (self.misty, self.mbot)},
            neutral_verifiers={key: lambda *args: True for key in (self.misty, self.mbot)},
            host_locks=self.locks, persist=persist, boot_id="boot", monotonic=lambda: self.now,
        )
        self.runtime = OperatorRuntime(self.bindings, **self.options)
        # Deterministic supervisor seam; no background timer is started here.
        self.runtime._mode = "RUNNING"
        self.runtime.supervise_once()
        self.runtime.startup_neutral(self.startup(self.misty, "initial"))
        self.runtime.startup_neutral(self.startup(self.mbot, "initial"))
        self.runtime.select(self.misty)

    def startup(self, platform, proof):
        return RobotObservation("boot", platform, "startup", "startup", "startup", "neutral", proof)

    def active(self, kind, proof):
        record = self.runtime._owner.state["record"]
        return RobotObservation("boot", record["platform_id"], record["request_id"],
                                record["session_id"], record["decision_reference"], kind, proof)

    def start(self):
        self.runtime.allow_open(session_id="s1", decision_reference="d1")

    def test_duplicate_endpoint_and_host_owner_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate_physical_endpoint"):
            OperatorRuntime([self.bindings[0], replace(self.bindings[1], endpoint=self.bindings[0].endpoint)], **self.options)
        with self.assertRaisesRegex(RuntimeError, "physical_target_busy"):
            OperatorRuntime(self.bindings, **self.options)

    def test_live_mode_and_missing_repository_refused(self):
        with self.assertRaisesRegex(ValueError, "live_wiring"):
            OperatorRuntime(self.bindings, **(self.options | {"physical_mode": True}))
        with self.assertRaisesRegex(ValueError, "repository_and_persistence"):
            OperatorRuntime(self.bindings, **(self.options | {"repository": None}))

    def test_stale_heartbeat_refuses_before_consumption(self):
        self.now = 0.3
        with self.assertRaisesRegex(RuntimeError, "supervisor_unhealthy"):
            self.start()
        self.assertIn(("s1", "d1"), self.repository.grants)

    def test_predispatch_decline_invalidates_without_stop(self):
        self.runtime.lifecycle("DECLINE", "s1")
        self.assertEqual(self.runtime._owner.state["phase"], "IDLE")
        with self.assertRaises(RuntimeError):
            self.start()

    def test_selection_invalidates_old_grant(self):
        self.runtime.select(self.mbot)
        self.assertNotIn(("s1", "d1"), self.repository.grants)

    def test_normal_neutral_is_persisted(self):
        self.start()
        self.runtime.completed(self.active("completed", "done"))
        self.runtime.lifecycle("FINISH", "s1")
        self.runtime.neutral(self.active("neutral", "neutral"))
        self.assertTrue(self.records[0]["neutral_verified"])

    def test_persistence_failure_blocks_new_selection(self):
        self.start()
        self.runtime.lifecycle("FINISH", "s1")
        self.fail_persist = True
        with self.assertRaises(OSError):
            self.runtime.neutral(self.active("neutral", "neutral"))
        self.assertEqual(self.runtime._mode, "PERSISTENCE_LOCKED")
        with self.assertRaisesRegex(RuntimeError, "runtime_locked"):
            self.runtime.select(self.mbot)
        self.assertIsNotNone(self.runtime._persist_pending)

    def test_placeholder_persistence_failure_is_latched(self):
        self.runtime.select(self.mbot)
        self.repository.grants[("s2", "d2")] = replace(self.grant, platform_id=self.mbot, session_id="s2", decision_reference="d2", request_id="r2")
        self.fail_persist = True
        with self.assertRaises(OSError):
            self.runtime.allow_open(session_id="s2", decision_reference="d2")
        self.assertEqual(self.runtime._mode, "PERSISTENCE_LOCKED")
        self.assertTrue(self.runtime._persist_pending["neutral_inferred_from_zero_io"])

    def test_slow_stop_is_not_false_health_failure(self):
        self.runtime._job_started = 0.0
        self.runtime._queued_at = None
        self.runtime._job_stopping = True
        self.now = 1.0
        self.runtime.supervise_once()
        self.assertEqual(self.runtime._mode, "RUNNING")
        self.now = 5.6
        self.runtime.supervise_once()
        self.assertEqual(self.runtime._mode, "HEALTH_LOCKED")

    def test_nonstop_stalled_worker_latches_health(self):
        self.runtime._job_started = 0.0
        self.runtime._queued_at = None
        self.runtime._job_stopping = False
        self.now = 0.3
        self.runtime.supervise_once()
        self.assertEqual(self.runtime._mode, "HEALTH_LOCKED")
        self.assertTrue(self.runtime._revoke_done.wait(1.0))
        self.assertNotIn(("s1", "d1"), self.repository.grants)

    def test_closed_idle_sends_no_stop_and_never_dispatches(self):
        self.runtime.shutdown()
        self.assertEqual(self.runtime._mode, "CLOSED")
        with self.assertRaisesRegex(RuntimeError, "runtime_locked"):
            self.start()
        self.runtime.release_after_poweroff(True)
        self.assertEqual(self.locks.held, set())

    def test_boot_replay_rejected(self):
        observation = replace(self.startup(self.misty, "fresh"), run_id="old")
        from robot_gateway.gateway import RobotGatewayError
        with self.assertRaisesRegex(RobotGatewayError, "observation_binding_mismatch"):
            self.runtime.startup_neutral(observation)

    def test_incarnation_limit_refuses_new_grant(self):
        while not self.runtime._jobs.empty():
            self.runtime._jobs.get_nowait()
            self.runtime._jobs.task_done()
        self.runtime._queued_at = None
        self.now = 1800.0
        self.runtime.supervise_once()
        self.assertEqual(self.runtime._mode, "CLOSED")
        with self.assertRaisesRegex(RuntimeError, "runtime_locked"):
            self.start()


    def test_health_revokes_all_unconsumed_platform_grants(self):
        self.runtime._latch_health()
        self.assertTrue(self.runtime._revoke_done.wait(1.0))
        self.assertEqual(self.repository.grants, {})

    def test_worker_death_and_queued_age_latch(self):
        self.runtime._driver_armed = True
        self.runtime._worker = Mock()
        self.runtime._worker.is_alive.return_value = False
        self.runtime.supervise_once()
        self.assertEqual(self.runtime._mode, "HEALTH_LOCKED")
        self.runtime._driver_armed = False
        self.runtime._mode = "RUNNING"
        self.runtime._queued_at = 0.0
        self.now = 0.3
        self.runtime.supervise_once()
        self.assertEqual(self.runtime._mode, "HEALTH_LOCKED")

    def test_failed_allow_refreshes_phase_and_shutdown_always_stops_driver(self):
        self.repository.grants.clear()
        with self.assertRaisesRegex(RuntimeError, "invalid_grant"):
            self.start()
        self.assertEqual(self.runtime._phase, "IDLE")
        self.runtime._latch_health()
        result = self.runtime.shutdown()
        self.assertEqual(result["mode"], "CLOSED")
        self.assertTrue(self.runtime._stop_event.is_set())

    def test_health_latch_does_not_erase_pending_persistence(self):
        self.start()
        self.runtime.lifecycle("FINISH", "s1")
        self.fail_persist = True
        with self.assertRaises(OSError):
            self.runtime.neutral(self.active("neutral", "neutral"))
        self.runtime._latch_health()
        self.assertTrue(self.runtime._revoke_done.wait(1.0))
        self.fail_persist = False
        self.runtime.recover(startup_observations=[self.startup(self.misty, "recovered")])
        self.assertIsNone(self.runtime._persist_pending)
        self.assertEqual(self.runtime._mode, "RUNNING")

    def test_wrong_session_or_decision_cannot_end_active_interaction(self):
        self.start()
        self.runtime.lifecycle("WITHDRAW", "other", "d1")
        self.runtime.lifecycle("LEAVE", "s1", "other")
        self.assertEqual(self.runtime._owner.state["phase"], "WAIT_COMPLETION")
        self.runtime.lifecycle("ERROR", "s1", "d1")
        self.assertEqual(self.runtime._owner.state["record"]["terminal_event"], "ERROR")

    def test_placeholder_startup_record_is_explicit_inference(self):
        records = [record for record in self.runtime._startup_records if record["platform_id"] == self.mbot]
        self.assertEqual(records[0]["kind"], "zero_io_inference")

    def test_recover_release_persistence_failure_is_retained(self):
        self.start()
        self.runtime.lifecycle("ERROR", "s1", "d1")
        self.fail_persist = True
        with self.assertRaises(OSError):
            self.runtime.recover(self.active("neutral", "recover"),
                                 startup_observations=[self.startup(self.misty, "fresh")])
        self.assertIsNotNone(self.runtime._persist_pending)
        self.assertEqual(self.runtime._mode, "PERSISTENCE_LOCKED")

    def test_operator_stop_wait_has_stop_budget(self):
        self.start()
        request = self.runtime._owner.state["record"]["request_id"]
        self.runtime._stop_started(request)
        self.runtime._job_started = 0.0
        self.runtime._queued_at = None
        self.runtime._job_request_id = request
        self.runtime._job_stopping = False
        self.now = 0.5
        self.runtime.supervise_once()
        self.assertEqual(self.runtime._mode, "RUNNING")


    def test_latch_during_consume_prevents_dispatch(self):
        original = self.repository.consume
        transport = Mock(return_value={"result": True})
        self.bindings[0].adapter._transport = transport
        def latch_then_consume(*args):
            self.runtime._latch_health()
            return original(*args)
        self.repository.consume = latch_then_consume
        with self.assertRaises(RuntimeError):
            self.start()
        transport.assert_not_called()
        self.assertEqual(self.runtime._phase, "IDLE")
        self.assertTrue(self.runtime._revoke_done.wait(1.0))

    def test_real_worker_timer_expire_with_slow_stop(self):
        from threading import Event
        from robot_gateway.strict_json_post import SPEAK_URL
        entered, resume, settled = Event(), Event(), Event()
        original_accept = self.runtime._accept_state
        def transport(url, payload):
            if url != SPEAK_URL:
                entered.set()
                if not resume.wait(3.0):
                    raise RuntimeError("test_stop_wait")
            return {"result": True}
        def accept(state):
            value = original_accept(state)
            if state["phase"] == "WAIT_NEUTRAL":
                settled.set()
            return value
        self.bindings[0].adapter._transport = transport
        self.runtime._accept_state = accept
        while not self.runtime._jobs.empty():
            self.runtime._jobs.get_nowait()
            self.runtime._jobs.task_done()
        self.runtime._queued_at = None
        # Preserve the real worker, but let this test drive supervision at
        # exact clock boundaries rather than racing an automatic supervisor.
        self.runtime._supervise_loop = lambda: self.runtime._stop_event.wait()
        self.runtime.start()
        try:
            self.start()
            self.runtime.completed(self.active("completed", "done"))
            self.now = 5.0
            self.runtime.supervise_once()
            self.assertTrue(entered.wait(1.0))
            self.now = 5.5
            self.runtime.supervise_once()
            self.assertEqual(self.runtime._mode, "RUNNING")
            resume.set()
            self.assertTrue(settled.wait(2.0))
        finally:
            resume.set()
            self.runtime.shutdown()
        self.assertFalse(self.runtime._worker.is_alive())

    def test_start_and_shutdown_active_uses_existing_one_stop(self):
        self.runtime.start()
        self.start()
        state = self.runtime.shutdown()
        self.assertEqual(state["mode"], "CLOSED")
        self.assertTrue(self.runtime._stop_event.is_set())
        self.assertIsNotNone(self.runtime._owner.state["record"]["stop_receipt"])


    def test_health_locked_neutral_deadline_recovers_through_owner_lock(self):
        self.start()
        self.runtime.lifecycle("FINISH", "s1", "d1")
        neutral = self.active("neutral", "neutral-after-timeout")
        self.runtime._latch_health()
        self.assertTrue(self.runtime._revoke_done.wait(1.0))
        self.now = 4.0
        self.runtime._heartbeat = self.now
        self.runtime.recover(neutral, startup_observations=[self.startup(self.misty, "recovered-startup")])
        self.assertEqual(self.runtime._owner.state["phase"], "IDLE")
        self.assertEqual(self.runtime._mode, "RUNNING")

    def test_shutdown_persistence_failure_cannot_reopen_closed_runtime(self):
        self.start()
        self.runtime.shutdown()
        self.fail_persist = True
        with self.assertRaises(OSError):
            self.runtime.neutral(self.active("neutral", "closed-neutral"))
        self.assertEqual(self.runtime._mode, "CLOSED")
        with self.assertRaisesRegex(RuntimeError, "runtime_closed"):
            self.runtime.recover(startup_observations=[self.startup(self.misty, "no-reopen")])
