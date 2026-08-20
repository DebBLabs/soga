from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Mapping

from .adapter import Invocation, TargetBoundAdapter
from .lifecycle import LifecycleError, SessionGrantService, SessionState
from .state_machine import OperatingState, SafetyStateMachine


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

    def submit(self, decision: ActionDecision, *, channel_key: str) -> dict:
        with self._lock:
            machine = self.state_machines.get(decision.platform_id)
            if machine is None:
                raise RuntimeErrorAtStage("target_resolution", "unknown_platform")
            request_key = (decision.session_id, decision.request_id)
            prior = self.sessions.prior_action_receipt(decision.session_id, decision.request_id)
            if prior is not None:
                if self._decisions[request_key] != decision:
                    raise RuntimeErrorAtStage("idempotency", "request_binding_conflict")
                return prior
            try:
                session = self.sessions.validate_session(
                    decision.session_id,
                    channel_key=channel_key,
                    platform_id=decision.platform_id,
                    participant_activity=True,
                )
            except LifecycleError as exc:
                raise RuntimeErrorAtStage(exc.stage, exc.code) from exc
            if session.mission_s256 != decision.mission_s256:
                raise RuntimeErrorAtStage("decision_binding", "wrong_mission")

            machine.enter_pending(decision.request_id)
            if decision.decision != Decision.ALLOW:
                machine.resolve_pending(
                    request_id=decision.request_id,
                    allow=False,
                    common_gate_satisfied=False,
                )
                receipt = {
                    "request_id": decision.request_id,
                    "platform_id": decision.platform_id,
                    "decision": decision.decision.value,
                    "adapter_status": "not_dispatched",
                    "physical_outcome": "not_started",
                    "phone_status": "degraded",
                }
                machine.finish_degraded_presentation()
                stored = self.sessions.record_action_receipt(
                    decision.session_id, decision.request_id, receipt
                )
                self._decisions[request_key] = decision
                return stored

            state = machine.resolve_pending(
                request_id=decision.request_id,
                allow=True,
                common_gate_satisfied=True,
            )
            if state != OperatingState.EXECUTING:
                raise RuntimeErrorAtStage("state_gate", state.value)
            invocation = Invocation(
                request_id=decision.request_id,
                decision_reference=decision.decision_reference,
                mission_s256=decision.mission_s256,
                session_id=decision.session_id,
                platform_id=decision.platform_id,
                agent_id=decision.agent_id,
                action=decision.action,
                catalog_version=decision.catalog_version,
            )
            adapter_receipt = self.adapter.dispatch(
                invocation, bound_platform_id=decision.platform_id
            )
            outcome = machine.action_finished(observed=False)
            receipt = {
                **adapter_receipt,
                "decision": decision.decision.value,
                "decision_reference": decision.decision_reference,
                "mission_s256": decision.mission_s256,
                "session_id": decision.session_id,
                "action": decision.action,
                "catalog_version": decision.catalog_version,
                "phone_status": outcome,
            }
            stored = self.sessions.record_action_receipt(
                decision.session_id, decision.request_id, receipt
            )
            self._decisions[request_key] = decision
            return stored

    def safety_stop(self, platform_id: str) -> None:
        with self._lock:
            try:
                self.state_machines[platform_id].safety_stop()
            except KeyError as exc:
                raise RuntimeErrorAtStage("target_resolution", "unknown_platform") from exc
            session = self.sessions.live_session_for_platform(platform_id)
            if session is not None:
                self.sessions.terminate(session.session_id, SessionState.SAFETY_STOPPED)
