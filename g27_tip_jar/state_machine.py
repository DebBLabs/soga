from __future__ import annotations

from enum import Enum
from threading import RLock


class OperatingState(str, Enum):
    NEUTRAL = "neutral"
    PENDING = "pending"
    DEGRADED = "degraded"
    EXECUTING = "executing"
    SAFETY_STOPPED = "safety_stopped"


class StateTransitionError(RuntimeError):
    pass


class SafetyStateMachine:
    """Per-platform state priority; physical behavior is neither simulated nor claimed."""

    def __init__(self, platform_id: str) -> None:
        self.platform_id = platform_id
        self._lock = RLock()
        self.state = OperatingState.NEUTRAL
        self.request_id: str | None = None
        self.request_current = False
        self.safety_latched = False
        self.phone_status = "neutral"

    def enter_pending(self, request_id: str) -> None:
        with self._lock:
            if self.safety_latched:
                raise StateTransitionError("safety_stop_has_precedence")
            if not request_id:
                raise StateTransitionError("missing_request_id")
            self.state = OperatingState.PENDING
            self.request_id = request_id
            self.request_current = True
            self.phone_status = "pending"

    def resolve_pending(self, *, request_id: str, allow: bool, common_gate_satisfied: bool) -> OperatingState:
        with self._lock:
            if self.safety_latched:
                self.state = OperatingState.SAFETY_STOPPED
                self.phone_status = "safety_stopped"
                return self.state
            if self.state != OperatingState.PENDING or self.request_id != request_id:
                raise StateTransitionError("wrong_pending_request")
            if not self.request_current:
                self._degrade()
                return self.state
            if allow and common_gate_satisfied:
                self.state = OperatingState.EXECUTING
                self.phone_status = "executing"
            else:
                self._degrade()
            return self.state

    def make_request_stale(self, request_id: str) -> None:
        with self._lock:
            if self.request_id != request_id:
                raise StateTransitionError("wrong_pending_request")
            self.request_current = False
            if self.safety_latched:
                self.state = OperatingState.SAFETY_STOPPED
                self.phone_status = "safety_stopped"
            else:
                self._degrade()

    def terminate_session(self) -> None:
        with self._lock:
            self.request_current = False
            self.request_id = None
            if self.safety_latched:
                self.state = OperatingState.SAFETY_STOPPED
                self.phone_status = "safety_stopped"
            else:
                self.state = OperatingState.NEUTRAL
                self.phone_status = "terminal"

    def safety_stop(self) -> None:
        with self._lock:
            self.safety_latched = True
            self.request_current = False
            self.state = OperatingState.SAFETY_STOPPED
            self.phone_status = "safety_stopped"

    def attempt_automatic_release(self, _cause: str) -> bool:
        with self._lock:
            return False

    def operator_release(self, *, platform_id: str, conditions_verified: bool, neutral_established: bool) -> bool:
        with self._lock:
            if platform_id != self.platform_id or not conditions_verified or not neutral_established:
                return False
            self.safety_latched = False
            self.request_id = None
            self.request_current = False
            self.state = OperatingState.NEUTRAL
            self.phone_status = "neutral"
            return True

    def action_finished(self, *, observed: bool) -> str:
        with self._lock:
            if self.safety_latched:
                return "interrupted"
            self.state = OperatingState.NEUTRAL
            self.request_current = False
            self.request_id = None
            outcome = "completed" if observed else "unknown"
            self.phone_status = outcome
            return outcome

    def finish_degraded_presentation(self) -> None:
        with self._lock:
            if self.state != OperatingState.DEGRADED:
                raise StateTransitionError("not_degraded")
            self.state = OperatingState.NEUTRAL
            # The participant-visible request outcome survives the physical
            # presentation's return to neutral.
            self.phone_status = "degraded"

    def _degrade(self) -> None:
        self.state = OperatingState.DEGRADED
        self.phone_status = "degraded"
