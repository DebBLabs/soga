from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from threading import Condition, RLock
from typing import Callable

from g27_tip_jar.adapter import Invocation

from .gateway import RobotGateway, RobotGatewayError
from .misty_invitation import ACTION, CATALOG_VERSION, utterance_id_for


LIFECYCLE_EVENTS = frozenset(("LEAVE", "FINISH", "WITHDRAW", "EXPIRE", "ERROR", "SHUTDOWN"))
SPEECH_COMPLETION_SECONDS = 10.0
RESPONSE_WINDOW_SECONDS = 5.0


@dataclass
class _Active:
    invocation: Invocation
    phase: str
    started_at: float
    completion_deadline: float
    response_deadline: float | None = None
    release_at: float | None = None
    stop_event: str | None = None
    terminal: dict[str, object] | None = None
    dispatch_receipt: dict[str, object] | None = None
    stop_receipt: dict[str, object] | None = None
    late_completion_recorded: bool = False


class RobotInvitationCoordinator:
    """Internal lifecycle seam; it exposes no participant-facing endpoint."""

    def __init__(
        self,
        *,
        gateway: RobotGateway,
        platform_id: str,
        agent_id: str,
        mission_s256: str,
        new_request_id: Callable[[], str],
        monotonic: Callable[[], float],
    ) -> None:
        if not platform_id or not agent_id or not mission_s256:
            raise ValueError("missing_fixed_binding")
        self._gateway = gateway
        self._platform_id = platform_id
        self._agent_id = agent_id
        self._mission_s256 = mission_s256
        self._new_request_id = new_request_id
        self._monotonic = monotonic
        self._lock = RLock()
        self._condition = Condition(self._lock)
        self._active: _Active | None = None
        self._consumed_sessions: set[str] = set()
        self._consumed_decisions: set[str] = set()
        self._terminals: dict[tuple[str, str], dict[str, object]] = {}

    def allow_open(self, *, decision_reference: str, session_id: str) -> dict[str, object]:
        if not decision_reference or not session_id:
            raise RobotGatewayError("missing_allow_binding")
        now = self._monotonic()
        request_id = self._new_request_id()
        invocation = Invocation(
            request_id=request_id,
            decision_reference=decision_reference,
            mission_s256=self._mission_s256,
            session_id=session_id,
            platform_id=self._platform_id,
            agent_id=self._agent_id,
            action=ACTION,
            catalog_version=CATALOG_VERSION,
        )
        with self._condition:
            if session_id in self._consumed_sessions or decision_reference in self._consumed_decisions:
                raise RobotGatewayError("allow_binding_consumed")
            if self._active is not None:
                raise RobotGatewayError("invitation_already_active")
            try:
                owner = self._gateway.reserve(invocation, bound_platform_id=self._platform_id)
            except Exception:
                self._consumed_sessions.add(session_id)
                self._consumed_decisions.add(decision_reference)
                terminal = self._rejected_terminal(invocation)
                self._store_terminal(invocation, terminal)
                return deepcopy(terminal)
            if not owner:
                raise RobotGatewayError("request_id_not_fresh")
            active = _Active(
                invocation=invocation,
                phase="DISPATCHING",
                started_at=now,
                completion_deadline=now + SPEECH_COMPLETION_SECONDS,
            )
            self._active = active
            self._consumed_sessions.add(session_id)
            self._consumed_decisions.add(decision_reference)

        try:
            dispatch_receipt = self._gateway.dispatch_reserved(
                invocation, bound_platform_id=self._platform_id, owner=True
            )
        except Exception:
            terminal = self._terminal(invocation, "DISPATCH_REJECTED", None, None)
            terminal["dispatch_status"] = "NOT_DISPATCHED"
            terminal["delivery"] = "not_dispatched"
            with self._condition:
                if self._active is active:
                    active.phase = "TERMINAL"
                    active.terminal = terminal
                    self._store_terminal(invocation, terminal)
                    self._gateway.release(invocation.request_id)
                    self._gateway.lock_for_operator_reset()
                    self._active = None
                    self._condition.notify_all()
            return deepcopy(terminal)

        now = self._monotonic()
        with self._condition:
            active.dispatch_receipt = deepcopy(dispatch_receipt)
            if self._active is not active:
                stored = self._terminals.get(self._key(session_id, decision_reference))
                return deepcopy(stored if stored is not None else dispatch_receipt)
            if active.phase in ("STOPPING", "TERMINAL"):
                self._condition.notify_all()
                completed = self._condition.wait_for(lambda: active.phase == "TERMINAL", timeout=3.0)
                if completed and active.terminal is not None:
                    return deepcopy(active.terminal)
                return self._stop_pending_terminal(invocation, active.stop_event or "STOP")
            if dispatch_receipt.get("command_acknowledgement") == "ACKNOWLEDGED":
                active.phase = "SPEECH_PENDING"
                active.completion_deadline = now + SPEECH_COMPLETION_SECONDS
                return deepcopy(dispatch_receipt)
            active.phase = "STOPPING"
            active.stop_event = "DISPATCH_FAILED"

        stop_receipt = self._gateway.stop(invocation)
        terminal = self._terminal(invocation, "DISPATCH_FAILED", dispatch_receipt, stop_receipt)
        terminal["delivery"] = dispatch_receipt.get("delivery", "unknown")
        if dispatch_receipt.get("command_acknowledgement") == "NOT_DISPATCHED":
            terminal["dispatch_status"] = "NOT_DISPATCHED"
        with self._condition:
            terminal["late_completion_recorded"] = active.late_completion_recorded
            if self._active is active:
                active.phase = "TERMINAL"
                active.terminal = terminal
                self._store_terminal(invocation, terminal)
                self._gateway.release(invocation.request_id)
                self._gateway.lock_for_operator_reset()
                self._active = None
                self._condition.notify_all()
        return deepcopy(terminal)

    def speech_complete(self, *, utterance_id: str, session_id: str, decision_reference: str) -> dict[str, object]:
        now = self._monotonic()
        key = self._key(session_id, decision_reference)
        with self._condition:
            active = self._active
            if active is None:
                terminal = self._terminals.get(key)
                if terminal is not None and terminal.get("utterance_id") == utterance_id:
                    terminal["late_completion_recorded"] = True
                    return deepcopy(terminal)
                raise RobotGatewayError("stale_completion")
            invocation = active.invocation
            if session_id != invocation.session_id or decision_reference != invocation.decision_reference:
                raise RobotGatewayError("completion_binding_mismatch")
            if utterance_id != utterance_id_for(invocation.request_id):
                raise RobotGatewayError("completion_binding_mismatch")
            if active.phase in ("STOPPING", "TERMINAL"):
                if active.terminal is not None:
                    active.terminal["late_completion_recorded"] = True
                    self._store_terminal(invocation, active.terminal)
                    return deepcopy(active.terminal)
                active.late_completion_recorded = True
                return self._stop_pending_terminal(invocation, active.stop_event or "STOP")
            if active.phase != "SPEECH_PENDING":
                raise RobotGatewayError("stale_completion")
            if now > active.completion_deadline:
                raise RobotGatewayError("completion_deadline_elapsed")
            active.phase = "RESPONSE_WINDOW"
            active.response_deadline = now + RESPONSE_WINDOW_SECONDS
            return {"phase": active.phase, "physical_outcome": "unknown"}

    def lifecycle(self, event: str, *, session_id: str, decision_reference: str | None) -> dict[str, object]:
        if event not in LIFECYCLE_EVENTS:
            raise RobotGatewayError("unknown_lifecycle_event")
        if not session_id:
            raise RobotGatewayError("missing_session_binding")
        key = self._key(session_id, decision_reference)
        with self._condition:
            existing = self._terminals.get(key)
            if existing is not None:
                return deepcopy(existing)
            active = self._active
            if active is None:
                if session_id in self._consumed_sessions or (
                    decision_reference and decision_reference in self._consumed_decisions
                ):
                    raise RobotGatewayError("stale_lifecycle_event")
                if event == "LEAVE":
                    if decision_reference is not None:
                        raise RobotGatewayError("leave_has_decision")
                elif not decision_reference:
                    raise RobotGatewayError("missing_decision_binding")
                self._consumed_sessions.add(session_id)
                if decision_reference:
                    self._consumed_decisions.add(decision_reference)
                terminal = self._predispatch_terminal(event, session_id, decision_reference)
                self._terminals[key] = terminal
                return deepcopy(terminal)
            invocation = active.invocation
            if session_id != invocation.session_id or decision_reference != invocation.decision_reference:
                self._consumed_sessions.add(session_id)
                if decision_reference:
                    self._consumed_decisions.add(decision_reference)
                raise RobotGatewayError("lifecycle_binding_mismatch")
            if active.phase == "TERMINAL":
                return deepcopy(active.terminal)
            if active.phase == "STOPPING":
                completed = self._condition.wait_for(lambda: active.phase == "TERMINAL", timeout=3.0)
                if completed and active.terminal is not None:
                    return deepcopy(active.terminal)
                return self._stop_pending_terminal(invocation, event)
            prior_phase = active.phase
            active.phase = "STOPPING"
            active.stop_event = event
            release_at = active.completion_deadline if prior_phase in ("DISPATCHING", "SPEECH_PENDING") else self._monotonic()

        stop_receipt = self._gateway.stop(invocation)
        with self._condition:
            active.stop_receipt = deepcopy(stop_receipt)
            if prior_phase == "DISPATCHING" and active.dispatch_receipt is None:
                self._condition.wait_for(lambda: active.dispatch_receipt is not None, timeout=3.0)
            dispatch_receipt = active.dispatch_receipt
            terminal = self._terminal(invocation, event, dispatch_receipt, stop_receipt)
            if event == "WITHDRAW":
                terminal["presentation_outcome"] = "STOPPED"
            terminal["late_completion_recorded"] = active.late_completion_recorded
            terminal["speak_outstanding_at_stop"] = bool(
                stop_receipt.get("speak_outstanding_at_stop") or prior_phase == "DISPATCHING"
            )
            acknowledgement = None if dispatch_receipt is None else dispatch_receipt.get("command_acknowledgement")
            if acknowledgement == "NOT_DISPATCHED":
                terminal["dispatch_status"] = "NOT_DISPATCHED"
                terminal["speak_outstanding_at_stop"] = False
            ambiguous = (
                prior_phase == "DISPATCHING"
                or acknowledgement != "ACKNOWLEDGED"
                or stop_receipt.get("stop_status") != "ACKNOWLEDGED"
            )
            if prior_phase == "DISPATCHING" and acknowledgement == "ACKNOWLEDGED":
                terminal["delivery"] = "acknowledged_after_stop"
            active.phase = "TERMINAL"
            active.terminal = terminal
            self._store_terminal(invocation, terminal)
            if ambiguous:
                self._gateway.release(invocation.request_id)
                self._gateway.lock_for_operator_reset()
                self._active = None
            else:
                active.release_at = release_at
                if release_at <= self._monotonic():
                    self._gateway.release(invocation.request_id)
                    self._active = None
            self._condition.notify_all()
        return deepcopy(terminal)

    def tick(self) -> dict[str, object] | None:
        now = self._monotonic()
        with self._condition:
            active = self._active
            if active is None or active.phase == "STOPPING":
                return None
            invocation = active.invocation
            if active.phase == "TERMINAL":
                if active.release_at is not None and now >= active.release_at:
                    terminal = deepcopy(active.terminal)
                    self._gateway.release(invocation.request_id)
                    self._active = None
                    self._condition.notify_all()
                    return terminal
                return None
            if active.phase == "RESPONSE_WINDOW" and active.response_deadline is not None:
                if now < active.response_deadline:
                    return None
                terminal = self._terminal(invocation, "EXPIRE", active.dispatch_receipt, None)
                terminal["late_completion_recorded"] = active.late_completion_recorded
                active.phase = "TERMINAL"
                active.terminal = terminal
                self._store_terminal(invocation, terminal)
                self._gateway.release(invocation.request_id)
                self._active = None
                self._condition.notify_all()
                return deepcopy(terminal)
            if active.phase != "SPEECH_PENDING" or now < active.completion_deadline:
                return None
            active.phase = "STOPPING"
            active.stop_event = "COMPLETION_MISSING"

        stop_receipt = self._gateway.stop(invocation)
        terminal = self._terminal(invocation, "COMPLETION_MISSING", active.dispatch_receipt, stop_receipt)
        terminal["completion"] = "missing"
        with self._condition:
            terminal["late_completion_recorded"] = active.late_completion_recorded
            if self._active is active:
                active.phase = "TERMINAL"
                active.terminal = terminal
                self._store_terminal(invocation, terminal)
                self._gateway.release(invocation.request_id)
                self._gateway.lock_for_operator_reset()
                self._active = None
                self._condition.notify_all()
        return deepcopy(terminal)

    def terminal_receipt(self, *, session_id: str, decision_reference: str | None) -> dict[str, object] | None:
        with self._lock:
            receipt = self._terminals.get(self._key(session_id, decision_reference))
            return None if receipt is None else deepcopy(receipt)

    def _store_terminal(self, invocation: Invocation, terminal: dict[str, object]) -> None:
        self._terminals[self._key(invocation.session_id, invocation.decision_reference)] = terminal

    @staticmethod
    def _key(session_id: str, decision_reference: str | None) -> tuple[str, str]:
        return session_id, decision_reference or ""

    @staticmethod
    def _predispatch_terminal(event: str, session_id: str, decision_reference: str | None) -> dict[str, object]:
        return {
            "session_id": session_id,
            "decision_reference": decision_reference,
            "terminal_event": event,
            "presentation_outcome": "STOPPED" if event == "WITHDRAW" else "CANCELLED",
            "dispatch_status": "NOT_DISPATCHED",
            "stop_status": "NOT_APPLICABLE",
            "delivery": "not_dispatched",
            "physical_outcome": "unknown",
            "execution_surface": "robot_invitation_coordinator",
        }

    @staticmethod
    def _rejected_terminal(invocation: Invocation) -> dict[str, object]:
        result = RobotInvitationCoordinator._terminal(invocation, "DISPATCH_REJECTED", None, None)
        result["dispatch_status"] = "NOT_DISPATCHED"
        result["delivery"] = "not_dispatched"
        return result

    @staticmethod
    def _terminal(
        invocation: Invocation,
        event: str,
        dispatch_receipt: dict[str, object] | None,
        stop_receipt: dict[str, object] | None,
    ) -> dict[str, object]:
        result = {
            "request_id": invocation.request_id,
            "session_id": invocation.session_id,
            "decision_reference": invocation.decision_reference,
            "platform_id": invocation.platform_id,
            "action": invocation.action,
            "utterance_id": utterance_id_for(invocation.request_id),
            "terminal_event": event,
            "presentation_outcome": "NONE",
            "adapter_status": "unknown",
            "command_acknowledgement": "unknown",
            "dispatch_status": "DISPATCH_ATTEMPTED",
            "stop_status": "NOT_APPLICABLE",
            "delivery": "unknown",
            "physical_outcome": "unknown",
            "late_completion_recorded": False,
            "execution_surface": "robot_invitation_coordinator",
        }
        if dispatch_receipt:
            for field in ("adapter_status", "command_acknowledgement", "delivery"):
                result[field] = dispatch_receipt.get(field, result[field])
        if stop_receipt:
            result["stop_status"] = stop_receipt.get("stop_status", "FAILED")
            result["speak_outstanding_at_stop"] = bool(stop_receipt.get("speak_outstanding_at_stop"))
        return result

    @staticmethod
    def _stop_pending_terminal(invocation: Invocation, event: str) -> dict[str, object]:
        result = RobotInvitationCoordinator._terminal(invocation, event, None, None)
        result["stop_status"] = "PENDING"
        return result

