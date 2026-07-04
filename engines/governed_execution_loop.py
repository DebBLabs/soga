from __future__ import annotations

from engines.stage_gate_engine import (
    StageGateEngine,
    StageGateState,
)
from engines.capability_registry import CapabilityRegistry
from verify.governance_pdp import GovernancePDP
from verify.mission_template import MissionLifecycle, MissionTemplate
from verify.runtime_envelope_model import (
    AuthorityEvidence,
    Reachability,
    RuntimeEnvelope,
    SubjectGovernanceState,
    SubjectState,
)


class GovernedExecutionLoop:
    """
    Routes mission steps through stage gate evaluation,
    governance evaluation, and capability resolution.

    This loop contains no policy logic and no execution logic.
    It composes existing components only.
    """

    def __init__(
        self,
        stage_gate_engine=None,
        governance_pdp=None,
        capability_registry=None,
    ):
        self.stage_gate_engine = stage_gate_engine or StageGateEngine()
        self.governance_pdp = governance_pdp or GovernancePDP()
        self.capability_registry = (
            capability_registry or CapabilityRegistry()
        )
        self.interruptions = []

    def run(
        self,
        mission,
        steps,
        subject_state,
        runtime_evidence=None,
    ):
        runtime_evidence = runtime_evidence or {}
        records = []

        for step in steps:
            records.append(
                self._route_step(
                    mission,
                    step,
                    subject_state,
                    runtime_evidence,
                )
            )

        return {
            "mission_id": mission["mission_id"],
            "records": records,
            "interruptions": self.interruptions,
        }

    def _route_step(
        self,
        mission,
        step,
        subject_state,
        runtime_evidence,
    ):
        gate = self.stage_gate_engine.evaluate_step(
            mission,
            step["step_id"],
            runtime_evidence,
        )

        state = gate["state"]

        if state == StageGateState.EXECUTE_DIRECTLY:
            capability = self.capability_registry.resolve(
                step["required_capability"]
            )

            return {
                "step_id": step["step_id"],
                "stage_gate_state": state,
                "route": "EXECUTE_DIRECTLY",
                "capability_resolution": capability,
            }

        if state == StageGateState.GOVERNANCE_REQUIRED:
            return self._submit_for_governance(
                mission,
                step,
                subject_state,
                gate,
                runtime_evidence,
                "GOVERNANCE_REQUIRED",
            )

        if state == StageGateState.RESUBMIT_FOR_GOVERNANCE:
            return self._submit_for_governance(
                mission,
                step,
                subject_state,
                gate,
                runtime_evidence,
                "RESUBMIT_FOR_GOVERNANCE",
            )

        interruption = self._create_interruption(
            step,
            state,
            "Stage gate restricted execution.",
        )

        return {
            "step_id": step["step_id"],
            "stage_gate_state": state,
            "route": "INTERRUPTED",
            "interruption": interruption,
        }

    def _submit_for_governance(
        self,
        mission,
        step,
        subject_state,
        gate,
        runtime_evidence,
        route,
    ):
        token = (
            gate.get("governance_reasoning_token")
            or runtime_evidence.get("governance_reasoning_token")
            or step.get("governance_reasoning_token")
            or "supervision_required"
        )

        envelope = self._build_envelope(
            mission,
            step,
            subject_state,
            token,
        )

        cdp = self.governance_pdp.evaluate(envelope)
        decision = getattr(cdp.decision, "value", str(cdp.decision))

        if decision == "ALLOW":
            capability = self.capability_registry.resolve(
                step["required_capability"]
            )

            return {
                "step_id": step["step_id"],
                "stage_gate_state": gate["state"],
                "route": route,
                "governance_decision": decision,
                "capability_resolution": capability,
            }

        if decision == "RESTRICT":
            interruption = self._create_interruption(
                step,
                gate["state"],
                "Governance decision restricted execution.",
            )

            return {
                "step_id": step["step_id"],
                "stage_gate_state": gate["state"],
                "route": "INTERRUPTED",
                "governance_decision": decision,
                "interruption": interruption,
            }

        return {
            "step_id": step["step_id"],
            "stage_gate_state": gate["state"],
            "route": route,
            "governance_decision": decision,
        }

    def _create_interruption(
        self,
        step,
        stage_gate_state,
        reason,
    ):
        interruption = {
            "step_id": step["step_id"],
            "required_capability": step["required_capability"],
            "stage_gate_state": stage_gate_state,
            "reason": reason,
        }

        self.interruptions.append(interruption)
        return interruption

    def _build_envelope(
        self,
        mission,
        step,
        subject_state,
        token,
    ):
        mission_template = MissionTemplate(
            mission_id=mission["mission_id"],
            lifecycle=MissionLifecycle.ACTIVE,
            subject_id=mission["subject_id"],
            objective=mission["objective"],
            allowed_actions=[step["action"]],
            constraints=mission["constraints"],
        )

        authority = AuthorityEvidence(
            authority_id=mission["authority_id"],
            authority_type="delegated",
            allowed_actions=[step["action"]],
            source_protocol="governed_execution_loop",
            references={},
            raw_evidence={},
        )

        subject = SubjectState(
            subject_id=mission["subject_id"],
            governance_state=subject_state,
            reachability=Reachability.REACHABLE,
            context={
                "scenario": mission.get("scenario"),
            },
        )

        return RuntimeEnvelope(
            request_id=f"req-{mission['mission_id']}-{step['step_id']}",
            mission=mission_template,
            authority=authority,
            subject=subject,
            execution_context={
                "requested_action": step["action"],
                "governance_reasoning_token": token,
            },
            policy={
                "profile": "soga-governed-execution-loop-v0.1",
            },
            metadata={
                "engine": "governed_execution_loop",
            },
        )
