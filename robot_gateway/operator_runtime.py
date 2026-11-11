"""Internal synthetic integration runtime. No live transport construction."""
from copy import deepcopy
from dataclasses import dataclass
from queue import Empty, Queue
from threading import Event, RLock, Thread, get_ident
import time
from typing import Protocol, runtime_checkable

from .switching import RobotSwitcher
from .unavailable_mbot2 import MBOT2_UNAVAILABLE_PLATFORM_ID, UnavailableMbot2Adapter


@runtime_checkable
class IssuedAllowRepository(Protocol):
    def consume(self, platform_id, session_id, decision_reference, boot_id): ...
    def invalidate(self, session_id, reason): ...
    def invalidate_selection(self, platform_id): ...


@dataclass(frozen=True)
class Binding:
    platform_id: str
    endpoint: str
    adapter: object
    stop_bound: float


class _ObservedAdapter:
    def __init__(self, adapter, on_stop, after_stop):
        self._adapter = adapter
        self._on_stop = on_stop
        self._after_stop = after_stop
        self.platform_id = adapter.platform_id

    def dispatch(self, *args, **kwargs):
        return self._adapter.dispatch(*args, **kwargs)

    def stop_to_neutral(self, *args, **kwargs):
        request_id = args[0].request_id
        self._on_stop(request_id)
        try:
            return self._adapter.stop_to_neutral(*args, **kwargs)
        finally:
            self._after_stop(request_id)


class OperatorRuntime:
    """Use injected fake dependencies only until a live wiring package is reviewed."""
    def __init__(self, bindings, *, repository, completion_verifiers, neutral_verifiers,
                 host_locks, persist, boot_id, monotonic=time.monotonic, physical_mode=False):
        if physical_mode:
            raise ValueError("live_wiring_not_implemented")
        if not isinstance(repository, IssuedAllowRepository) or not callable(persist):
            raise ValueError("repository_and_persistence_required")
        if not bindings or len({binding.endpoint for binding in bindings}) != len(bindings):
            raise ValueError("duplicate_physical_endpoint")
        if len({binding.platform_id for binding in bindings}) != len(bindings):
            raise ValueError("duplicate_platform")
        if any(type(binding.endpoint) is not str or not binding.endpoint or
               binding.adapter.platform_id != binding.platform_id or
               type(binding.stop_bound) not in (int, float) or not 0 < binding.stop_bound <= 5.5
               for binding in bindings):
            raise ValueError("invalid_binding")
        self._clock = monotonic
        self._started = monotonic()
        self._mutex = RLock()
        self._mode = "HEALTH_LOCKED"
        self._phase = "IDLE"
        self._heartbeat = None
        self._selected = None
        self._runtime_ready = set()
        self._jobs = Queue(maxsize=1)
        self._stop_event = Event()
        self._worker = self._supervisor = None
        self._job_started = None
        self._job_stopping = False
        self._health_stop_scheduled = False
        self._active_calls = 0
        self._persist_pending = None
        self._persisted = set()
        self._consumed = 0
        self._sessions = set()
        self._repository = repository
        self._persist = persist
        self._boot_id = boot_id
        self._leases = []
        self._platforms = tuple(binding.platform_id for binding in bindings)
        self._placeholder = {binding.platform_id for binding in bindings
                             if binding.platform_id == MBOT2_UNAVAILABLE_PLATFORM_ID
                             and isinstance(binding.adapter, UnavailableMbot2Adapter)}
        self._startup_records = []
        self._driver_armed = False
        self._queued_at = None
        self._stops_active = set()
        self._job_request_id = None
        self._active_binding = None
        self._recovering = False
        self._revoke_done = Event()
        self._revoke_done.set()
        self._revocation_failed = False
        self._revoker = None
        self._stop_bounds = {binding.platform_id: binding.stop_bound for binding in bindings}
        adapters = {}
        try:
            for binding in bindings:
                lease = host_locks.acquire(binding.platform_id, binding.endpoint)
                if lease is None:
                    raise RuntimeError("physical_target_busy")
                self._leases.append(lease)
                adapter = binding.adapter
                if not (binding.platform_id == MBOT2_UNAVAILABLE_PLATFORM_ID and isinstance(adapter, UnavailableMbot2Adapter)):
                    adapter = _ObservedAdapter(adapter, self._stop_started, self._stop_finished)
                adapters[binding.platform_id] = adapter
            self._owner = RobotSwitcher(adapters, completion_verifiers=completion_verifiers,
                                        neutral_verifiers=neutral_verifiers, authorize=self._consume,
                                        monotonic=monotonic, run_id=boot_id)
        except BaseException:
            for lease in reversed(self._leases):
                lease.release()
            raise

    def _stop_started(self, request_id):
        with self._mutex:
            self._phase = "STOPPING"
            self._stops_active.add(request_id)
            if self._job_request_id == request_id:
                self._job_stopping = True

    def _stop_finished(self, request_id):
        with self._mutex:
            self._stops_active.discard(request_id)

    def _healthy(self):
        if self._heartbeat is None or not 0 <= self._clock() - self._heartbeat <= 0.25:
            raise RuntimeError("supervisor_unhealthy")
        if self._mode != "RUNNING" or self._recovering:
            raise RuntimeError("runtime_locked")
        if self._driver_armed and (self._worker is None or not self._worker.is_alive()):
            raise RuntimeError("worker_not_alive")
        if self._clock() - self._started >= 1800 or self._consumed >= 100:
            raise RuntimeError("incarnation_exhausted")

    def _consume(self, platform, session, decision):
        # RobotSwitcher holds its owner lock while calling this callback.
        with self._mutex:
            self._healthy()
            if platform not in self._runtime_ready:
                raise RuntimeError("startup_neutral_required")
            invocation = self._repository.consume(platform, session, decision, self._boot_id)
            self._healthy()
            self._consumed += 1
            self._sessions.add(session)
            return invocation

    def start(self):
        with self._mutex:
            if self._worker is not None:
                raise RuntimeError("already_started")
            self._worker = Thread(target=self._work_loop, daemon=True)
            self._supervisor = Thread(target=self._supervise_loop, daemon=True)
            self._heartbeat = self._clock()
            self._mode = "RUNNING"
            self._driver_armed = True
            self._worker.start()
            self._supervisor.start()

    def _work_loop(self):
        while not self._stop_event.is_set():
            try:
                job = self._jobs.get(timeout=0.05)
            except Empty:
                continue
            with self._mutex:
                self._job_started = self._clock()
                self._queued_at = None
                self._job_request_id = None if self._active_binding is None else self._active_binding.get("request_id")
                self._job_stopping = self._phase == "STOPPING" or self._job_request_id in self._stops_active
            try:
                state = self._owner.tick() if job == "tick" else self._owner.finish(event=job)
                self._accept_state(state)
            except BaseException:
                self._latch_health()
            finally:
                with self._mutex:
                    self._job_started = None
                    self._job_request_id = None
                    self._jobs.task_done()

    def _supervise_loop(self):
        while not self._stop_event.wait(0.05):
            self.supervise_once()

    def supervise_once(self):
        failed, exhausted = False, False
        with self._mutex:
            now = self._clock()
            self._heartbeat = now
            exhausted = self._mode == "RUNNING" and (now - self._started >= 1800 or self._consumed >= 100)
            if self._driver_armed and (self._worker is None or not self._worker.is_alive()):
                failed = True
            if self._queued_at is not None and now - self._queued_at > 0.25:
                failed = True
            if self._job_started is not None:
                stopping = self._job_stopping or self._phase == "STOPPING" and (
                    self._job_request_id is None or self._job_request_id in self._stops_active)
                bound = self._stop_bounds.get(self._selected, 5.5) if stopping else 0.25
                failed = failed or now - self._job_started > bound
            if self._mode == "RUNNING" and not failed and not exhausted and self._job_started is None and self._jobs.empty():
                self._queued_at = now
                self._jobs.put_nowait("tick")
        if failed:
            self._latch_health()
        elif exhausted:
            self.shutdown()

    def _revoke_all(self):
        failed = False
        for platform in self._platforms:
            try:
                self._repository.invalidate_selection(platform)
            except BaseException:
                failed = True
        with self._mutex:
            self._revocation_failed = failed
            self._revoke_done.set()

    def _schedule_revocation(self):
        with self._mutex:
            if not self._revoke_done.is_set():
                return
            self._revoke_done.clear()
            self._revocation_failed = False
            self._revoker = Thread(target=self._revoke_all, daemon=True)
            revoker = self._revoker
        revoker.start()

    def _latch_health(self):
        with self._mutex:
            if self._mode == "CLOSED":
                return
            self._mode = "HEALTH_LOCKED"
            self._runtime_ready.clear()
            need_stop = self._phase in ("DISPATCHING", "WAIT_COMPLETION", "RESPONSE_WINDOW")
            launch = need_stop and not self._health_stop_scheduled
            if launch:
                self._health_stop_scheduled = True
        self._schedule_revocation()
        if launch:
            Thread(target=self._rescue_stop, daemon=True).start()

    def _rescue_stop(self):
        try:
            state = self._owner.finish(event="ERROR")
            self._accept_state(state)
        except BaseException:
            pass
        # If the owner callback holds its lock, this thread may be blocked.
        # HEALTH_LOCKED is already visible; operator must use physical stop.

    def _accept_state(self, state):
        with self._mutex:
            self._phase = state["phase"]
            self._active_binding = None if state["phase"] == "IDLE" else deepcopy(state["record"])
            self._selected = state["selected_platform_id"]
            record = state["record"]
            terminal = state["phase"] == "IDLE" and bool(record.get("terminal_event"))
            if not terminal or record["request_id"] in self._persisted:
                return state
            if self._persist_pending is not None:
                return state
            self._persist_pending = deepcopy(record)
        try:
            self._persist(deepcopy(record))
        except BaseException:
            with self._mutex:
                if self._mode != "CLOSED":
                    self._mode = "PERSISTENCE_LOCKED"
            raise
        with self._mutex:
            self._persisted.add(record["request_id"])
            self._persist_pending = None
        return state

    def _call(self, method, *args, require_health=False, **kwargs):
        with self._mutex:
            if require_health:
                self._healthy()
                if self._active_calls or self._persist_pending is not None:
                    raise RuntimeError("operation_pending")
            self._active_calls += 1
            if method == "allow_open":
                self._phase = "DISPATCHING"
                self._active_binding = {"session_id": kwargs["session_id"],
                                        "decision_reference": kwargs["decision_reference"]}
        try:
            state = getattr(self._owner, method)(*args, **kwargs)
            return self._accept_state(self._owner.state if state is None else state)
        except BaseException:
            # Refresh the mirror after owner-lock unwinding, without holding the
            # supervisor mutex while acquiring the owner lock.
            state = self._owner.state
            with self._mutex:
                self._phase = state["phase"]
                self._selected = state["selected_platform_id"]
                self._active_binding = None if state["phase"] == "IDLE" else deepcopy(state["record"])
            raise
        finally:
            with self._mutex:
                self._active_calls -= 1

    def startup_neutral(self, observation):
        state = self._call("startup_neutral", observation)
        with self._mutex:
            self._runtime_ready.add(observation.platform_id)
            self._startup_records.append({
                "platform_id": observation.platform_id, "run_id": observation.run_id,
                "proof": observation.proof,
                "kind": "zero_io_inference" if observation.platform_id in self._placeholder else "verified_observation",
            })
        return state

    def select(self, platform_id):
        with self._mutex:
            self._healthy()
            if self._active_calls:
                raise RuntimeError("operation_pending")
            if platform_id not in self._runtime_ready:
                raise RuntimeError("startup_neutral_required")
            if self._selected is not None:
                self._repository.invalidate_selection(self._selected)
        state = self._call("select", platform_id, require_health=True)
        with self._mutex:
            self._selected = platform_id
        return state

    def allow_open(self, *, session_id, decision_reference):
        return self._call("allow_open", session_id=session_id,
                          decision_reference=decision_reference, require_health=True)

    def lifecycle(self, event, session_id, decision_reference=None):
        if event not in ("DECLINE", "WITHDRAW", "LEAVE", "FINISH", "ERROR"):
            raise ValueError("invalid_lifecycle")
        self._repository.invalidate(session_id, event)
        with self._mutex:
            phase = self._phase
            binding = deepcopy(self._active_binding)
        matches = binding is not None and binding.get("session_id") == session_id and (
            decision_reference is None or binding.get("decision_reference") == decision_reference)
        if not matches or event == "DECLINE" or phase in ("IDLE", "STOPPING", "WAIT_NEUTRAL", "LOCKED"):
            return None
        return self._call("finish", event=event)

    def completed(self, observation):
        return self._call("completed", observation)

    def neutral(self, observation):
        return self._call("neutral", observation)

    def recover(self, observation=None, *, startup_observations=()):
        with self._mutex:
            if self._mode == "CLOSED":
                raise RuntimeError("runtime_closed")
            if self._active_calls or self._recovering:
                raise RuntimeError("operation_pending")
            if not self._revoke_done.is_set() or self._revocation_failed:
                raise RuntimeError("grant_revocation_unconfirmed")
            self._recovering = True
            pending = deepcopy(self._persist_pending)
            phase = self._phase
        try:
            if pending is not None:
                self._persist(deepcopy(pending))
                with self._mutex:
                    self._persisted.add(pending["request_id"])
                    self._persist_pending = None
            if phase == "LOCKED":
                self._call("recover", observation)
            elif phase == "WAIT_NEUTRAL":
                # A latched health gate pauses scheduled ticks. Drive this
                # no-new-dispatch deadline before choosing the recovery seam.
                state = self._call("tick")
                if state["phase"] == "LOCKED":
                    self._call("recover", observation)
                else:
                    self._call("neutral", observation)
            elif phase != "IDLE":
                raise RuntimeError("recovery_wait_for_stop")
            if not startup_observations:
                raise RuntimeError("fresh_startup_neutral_required")
            for startup in startup_observations:
                self.startup_neutral(startup)
            with self._mutex:
                if self._mode == "CLOSED":
                    raise RuntimeError("runtime_closed")
                if self._heartbeat is None or self._clock() - self._heartbeat > 0.25:
                    raise RuntimeError("supervisor_unhealthy")
                if self._driver_armed and (self._worker is None or not self._worker.is_alive()):
                    raise RuntimeError("worker_not_alive")
                if self._selected is not None and self._selected not in self._runtime_ready:
                    raise RuntimeError("selected_neutral_unconfirmed")
                self._mode = "RUNNING"
                self._health_stop_scheduled = False
        finally:
            with self._mutex:
                self._recovering = False

    def shutdown(self):
        with self._mutex:
            self._mode = "CLOSED"
            phase = self._phase
        self._schedule_revocation()
        failure = None
        try:
            if phase in ("DISPATCHING", "WAIT_COMPLETION", "RESPONSE_WINDOW"):
                self._call("finish", event="SHUTDOWN")
        except BaseException as error:
            failure = type(error).__name__
        finally:
            self._stop_event.set()
            for thread in (self._worker, self._supervisor):
                if thread is not None and thread.ident != get_ident():
                    thread.join(1.0)
        return {"mode": "CLOSED", "operator_power_confirmation": "required", "cleanup_error": failure}

    def release_after_poweroff(self, confirmed):
        with self._mutex:
            if self._mode != "CLOSED" or confirmed is not True or self._active_calls or (
                self._worker is not None and self._worker.is_alive()
            ):
                raise RuntimeError("poweroff_or_operations_unconfirmed")
            for lease in reversed(self._leases):
                lease.release()
            self._leases.clear()
