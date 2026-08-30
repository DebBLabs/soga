from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Mapping

from .adapter import Invocation, TargetBoundAdapter
from .lifecycle import LifecycleError, SessionGrantService, SessionState
from .state_machine import OperatingState, SafetyStateMachine, StateTransitionError


class Decision(str, Enum):
    ALLOW = "ALLOW"
    RESTRICT = "RESTRICT"
    DENY = "DENY"


class RuntimeErrorAtStage(RuntimeError):
    def __init__(self, stage: str, code: str):
        super().__init__(f"{stage}: {code}")
        self.stage = stage
        self.code = code


@dataclass(frozen=True)
class ActionDecision:
    request_id: str
    decision_reference: str
    decision: Decision
    mission_s256: str
    session_id: str
    platform_id: str
    agent_id: str
    action: str
    catalog_version: str


@dataclass(frozen=True)
class ActionRequest:
    request_id: str
    mission_s256: str
    session_id: str
    platform_id: str
    agent_id: str
    action: str
    catalog_version: str


@dataclass(frozen=True)
class PendingAction:
    request: ActionRequest
    channel_key: str


class PrototypeRuntime:
    """Coordinates current session truth, state priority, and recording-only dispatch."""

    def __init__(
        self,
        *,
        sessions: SessionGrantService,
        adapter: TargetBoundAdapter,
        state_machines: Mapping[str, SafetyStateMachine],
    ) -> None:
        self.sessions = sessions
        self.adapter = adapter
        self.state_machines = dict(state_machines)
        self._lock = RLock()
        self._decisions: dict[tuple[str, str], ActionDecision] = {}
        self._pending: dict[tuple[str, str], PendingAction] = {}
        self._events: list[dict] = []

    @property
    def events(self) -> tuple[dict, ...]:
        with self._lock:
            return tuple(dict(event) for event in self._events)

    @property
    def pending_request_ids(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(key[1] for key in self._pending)

    def initiate_session(
        self,
        grant_id: str,
        *,
        platform_id: str,
        mission_s256: str,
        notice_version: str,
        policy_version: str,
        channel_key: str,
    ):
        """Admit and consume a grant atomically with the platform safety gate."""
        with self._lock:
            machine = self.state_machines.get(platform_id)
            if machine is None:
                raise RuntimeErrorAtStage("target_resolution", "unknown_platform")
            if machine.safety_latched:
                raise RuntimeErrorAtStage("session_admission", "safety_stopped")
            try:
                return self.sessions.initiate_and_consume(
                    grant_id,
                    platform_id=platform_id,
                    mission_s256=mission_s256,
                    notice_version=notice_version,
                    policy_version=policy_version,
                    channel_key=channel_key,
                )
            except LifecycleError as exc:
                raise RuntimeErrorAtStage(exc.stage, exc.code) from exc

    def begin_request(self, request: ActionRequest, *, channel_key: str) -> dict:
        with self._lock:
            machine = self.state_machines.get(request.platform_id)
            if machine is None:
                raise RuntimeErrorAtStage("target_resolution", "unknown_platform")
            request_key = (request.session_id, request.request_id)
            if request_key in self._pending:
                prior = self._pending[request_key]
                if prior != PendingAction(request, channel_key):
                    raise RuntimeErrorAtStage("idempotency", "request_binding_conflict")
                return {"request_id": request.request_id, "state": "pending"}
            if self.sessions.prior_action_receipt(request.session_id, request.request_id) is not None:
                raise RuntimeErrorAtStage("idempotency", "request_already_resolved")
            try:
                session = self.sessions.validate_session(
                    request.session_id,
                    channel_key=channel_key,
                    platform_id=request.platform_id,
                    participant_activity=True,
                )
            except LifecycleError as exc:
                raise RuntimeErrorAtStage(exc.stage, exc.code) from exc
            if session.mission_s256 != request.mission_s256:
                raise RuntimeErrorAtStage("request_binding", "wrong_mission")
            try:
                machine.enter_pending(request.request_id)
            except StateTransitionError as exc:
                raise RuntimeErrorAtStage("state_gate", str(exc)) from exc
            self._pending[request_key] = PendingAction(request, channel_key)
            self._record_event(
                "request_received",
                request_id=request.request_id,
                session_id=request.session_id,
                platform_id=request.platform_id,
                action=request.action,
                state="pending",
            )
            return {"request_id": request.request_id, "state": "pending"}

    def resolve_request(
        self,
        *,
        session_id: str,
        request_id: str,
        decision_reference: str,
        outcome: Decision,
    ) -> dict:
        with self._lock:
            request_key = (session_id, request_id)
            try:
                pending = self._pending[request_key]
            except KeyError as exc:
                raise RuntimeErrorAtStage("pending_lookup", "unknown_request") from exc
            request = pending.request
            decision = ActionDecision(
                request_id=request.request_id,
                decision_reference=decision_reference,
                decision=outcome,
                mission_s256=request.mission_s256,
                session_id=request.session_id,
                platform_id=request.platform_id,
                agent_id=request.agent_id,
                action=request.action,
                catalog_version=request.catalog_version,
            )
            self._record_event(
                "decision_received",
                request_id=request_id,
                session_id=session_id,
                platform_id=request.platform_id,
                decision=outcome.value,
                decision_reference=decision_reference,
            )
            machine = self.state_machines[request.platform_id]
            try:
                self.sessions.validate_session(
                    session_id,
                    channel_key=pending.channel_key,
                    platform_id=request.platform_id,
                    participant_activity=False,
                )
            except LifecycleError as exc:
                self._record_event(
                    "decision_rejected",
                    request_id=request_id,
                    session_id=session_id,
                    platform_id=request.platform_id,
                    reason=f"{exc.stage}:{exc.code}",
                )
                self._pending.pop(request_key, None)
                if not machine.safety_latched:
                    machine.terminate_session()
                raise RuntimeErrorAtStage(exc.stage, exc.code) from exc
            if machine.safety_latched:
                self._record_event(
                    "decision_rejected",
                    request_id=request_id,
                    session_id=session_id,
                    platform_id=request.platform_id,
                    reason="state_gate:safety_stopped",
                )
                self._pending.pop(request_key, None)
                raise RuntimeErrorAtStage("state_gate", "safety_stopped")

            if outcome != Decision.ALLOW:
                machine.resolve_pending(
                    request_id=request_id,
                    allow=False,
                    common_gate_satisfied=False,
                )
                self._record_event(
                    "dispatch_skipped",
                    request_id=request_id,
                    session_id=session_id,
                    platform_id=request.platform_id,
                    reason=outcome.value,
                )
                receipt = {
                    "request_id": request_id,
                    "platform_id": request.platform_id,
                    "decision": outcome.value,
                    "adapter_status": "not_dispatched",
                    "physical_outcome": "not_started",
                    "phone_status": "degraded",
                }
                machine.finish_degraded_presentation()
                self._record_event(
                    "outcome_recorded",
                    request_id=request_id,
                    session_id=session_id,
                    platform_id=request.platform_id,
                    physical_outcome="not_started",
                    phone_status="degraded",
                )
            else:
                state = machine.resolve_pending(
                    request_id=request_id,
                    allow=True,
                    common_gate_satisfied=True,
                )
                if state != OperatingState.EXECUTING:
                    raise RuntimeErrorAtStage("state_gate", state.value)
                invocation = Invocation(
                    request_id=request.request_id,
                    decision_reference=decision_reference,
                    mission_s256=request.mission_s256,
                    session_id=request.session_id,
                    platform_id=request.platform_id,
                    agent_id=request.agent_id,
                    action=request.action,
                    catalog_version=request.catalog_version,
                )
                adapter_receipt = self.adapter.dispatch(
                    invocation, bound_platform_id=request.platform_id
                )
                self._record_event(
                    "dispatch_recorded",
                    request_id=request_id,
                    session_id=session_id,
                    platform_id=request.platform_id,
                    adapter_status=adapter_receipt["adapter_status"],
                )
                physical_outcome = machine.action_finished(observed=False)
                receipt = {
                    **adapter_receipt,
                    "decision": outcome.value,
                    "decision_reference": decision_reference,
                    "mission_s256": request.mission_s256,
                    "session_id": session_id,
                    "action": request.action,
                    "catalog_version": request.catalog_version,
                    "phone_status": physical_outcome,
                }
                self._record_event(
                    "outcome_recorded",
                    request_id=request_id,
                    session_id=session_id,
                    platform_id=request.platform_id,
                    physical_outcome=adapter_receipt["physical_outcome"],
                    phone_status=physical_outcome,
                )
            stored = self.sessions.record_action_receipt(session_id, request_id, receipt)
            self._decisions[request_key] = decision
            self._pending.pop(request_key, None)
            return stored

    def submit(self, decision: ActionDecision, *, channel_key: str) -> dict:
        with self._lock:
            request_key = (decision.session_id, decision.request_id)
            prior = self.sessions.prior_action_receipt(decision.session_id, decision.request_id)
            if prior is not None:
                if self._decisions[request_key] != decision:
                    raise RuntimeErrorAtStage("idempotency", "request_binding_conflict")
                return prior
            self.begin_request(
                ActionRequest(
                    request_id=decision.request_id,
                    mission_s256=decision.mission_s256,
                    session_id=decision.session_id,
                    platform_id=decision.platform_id,
                    agent_id=decision.agent_id,
                    action=decision.action,
                    catalog_version=decision.catalog_version,
                ),
                channel_key=channel_key,
            )
            return self.resolve_request(
                session_id=decision.session_id,
                request_id=decision.request_id,
                decision_reference=decision.decision_reference,
                outcome=decision.decision,
            )

    def safety_stop(self, platform_id: str) -> None:
        with self._lock:
            try:
                self.state_machines[platform_id].safety_stop()
            except KeyError as exc:
                raise RuntimeErrorAtStage("target_resolution", "unknown_platform") from exc
            session = self.sessions.live_session_for_platform(platform_id)
            if session is not None:
                self.sessions.terminate(session.session_id, SessionState.SAFETY_STOPPED)
            self._record_event(
                "safety_halt",
                platform_id=platform_id,
                session_id=None if session is None else session.session_id,
                state="safety_stopped",
            )

    def _record_event(self, kind: str, **details) -> None:
        self._events.append({"sequence": len(self._events) + 1, "kind": kind, **details})
