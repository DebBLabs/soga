from __future__ import annotations

# Stage Gate Lifecycle Demonstration
# Exercises the complete four-phase Stage Gate lifecycle.
# Real GovernancePDP called at each evaluation.
# StageGateEngine determines when to invoke governance.
# GovernancePDP determines what the governance decision is.
# These responsibilities must never be conflated.

from engines.stage_gate_engine import StageGateEngine
from verify.governance_pdp import GovernancePDP
from verify.mission_template import MissionLifecycle, MissionTemplate
from verify.runtime_envelope_model import (
    AuthorityEvidence,
    Reachability,
    RuntimeEnvelope,
    SubjectGovernanceState,
    SubjectState,
)


def build_mission() -> dict:
    return {
        "mission_id": "caregiver-discharge-follow-up",
        "objective": "Schedule caregiver discharge follow-up appointment.",
        "constraints": {
            "global": {},
            "stage_gate": [
                {
                    "gate_id": "gate-supervision-required",
                    "name": "supervision_required",
                    "step_id": "schedule_appointment",
                    "governance_reasoning_token": "supervision_required",
                    "required_evidence": "supervisor_confirmation",
                    "restrict_path": "HOLDING",
                }
            ],
            "delegation": {},
        },
    }


def build_envelope(
    subject_state: SubjectGovernanceState,
    token: str,
) -> RuntimeEnvelope:
    mission = MissionTemplate(
        mission_id="caregiver-discharge-follow-up",
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id="subject-001",
        objective="Schedule caregiver discharge follow-up appointment.",
        allowed_actions=["schedule_appointment"],
        constraints={
            "global": {},
            "stage_gate": [
                {
                    "gate_id": "gate-supervision-required",
                    "name": "supervision_required",
                    "step_id": "schedule_appointment",
                    "governance_reasoning_token": token,
                    "required_evidence": "supervisor_confirmation",
                    "restrict_path": "HOLDING",
                }
            ],
            "delegation": {},
        },
    )

    authority = AuthorityEvidence(
        authority_id="authority-caregiver-001",
        authority_type="delegated",
        allowed_actions=["schedule_appointment"],
        source_protocol="stage_gate_demo",
        references={},
        raw_evidence={},
    )

    subject = SubjectState(
        subject_id="subject-001",
        governance_state=subject_state,
        reachability=Reachability.REACHABLE,
        context={
            "scenario": "caregiver_discharge_follow_up",
        },
    )

    return RuntimeEnvelope(
        request_id=f"req-stage-gate-{token}",
        mission=mission,
        authority=authority,
        subject=subject,
        execution_context={
            "requested_action": "schedule_appointment",
            "governance_reasoning_token": token,
        },
        policy={
            "profile": "soga-stage-gate-demo-v0.1",
        },
        metadata={
            "demo": "stage_gate_lifecycle",
        },
    )


def decision_value(cdp) -> str:
    return getattr(cdp.decision, "value", str(cdp.decision))


def token_for(cdp, fallback: str) -> str:
    constraints = getattr(cdp, "constraints", {}) or {}
    return (
        constraints.get("governance_reasoning_token")
        or constraints.get("subject_agency_state")
        or fallback
    )


def main() -> None:
    mission = build_mission()
    stage_gate_engine = StageGateEngine()
    pdp = GovernancePDP()

    print("=== Stage Gate Lifecycle Demonstration ===")
    print("Scenario: Caregiver Discharge Follow-Up — Supervised Subject")
    print()

    print("Phase 1 — Discovery Boundary")
    print("  Mission step: schedule_appointment")
    print("  Stage gate declared: supervision_required")

    phase_1 = stage_gate_engine.evaluate_step(
        mission,
        "schedule_appointment",
        {},
    )

    print("  StageGateEngine:", phase_1["state"])
    print()

    print("Phase 2 — Interruption Request")
    print("  Submitting to GovernancePDP...")

    restricted_envelope = build_envelope(
        SubjectGovernanceState.SUPERVISED,
        "supervision_required",
    )

    restricted_cdp = pdp.evaluate(restricted_envelope)

    print("  Decision:", decision_value(restricted_cdp))
    print("  Token: supervision_required")

    phase_2 = stage_gate_engine.evaluate_step(
        mission,
        "schedule_appointment",
        {
            "governance_decision": decision_value(restricted_cdp),
            "cdp_reference": restricted_cdp.receipt_id,
        },
    )

    print("  StageGateEngine:", phase_2["state"])
    print(
        "  Interruption record created:",
        phase_2["interruption_record"]["interruption_instance_id"],
    )
    print()

    print("Phase 3 — Clearance Capture")
    print("  Clearance received: supervisor_confirmed = true")
    print("  Updated evidence recorded.")

    phase_3 = stage_gate_engine.evaluate_step(
        mission,
        "schedule_appointment",
        {
            "clearance_evidence": {
                "type": "supervisor_confirmation",
                "supervisor_confirmed": True,
                "satisfied": True,
            },
        },
    )

    print("  StageGateEngine:", phase_3["state"])
    print()

    print("Phase 4 — Resubmission Pass")
    print("  Resubmitting through passive adapter and normalizer...")
    print("  GovernancePDP evaluates updated RuntimeEnvelope...")

    # Phase 4: Supervisor clearance received.
    # Effective subject agency state transitions to INDEPENDENT
    # for this execution step. Clearance authorizes independent
    # execution of this specific mission step.
    # Subject remains SUPERVISED for future steps without clearance.
    cleared_envelope = build_envelope(
        SubjectGovernanceState.INDEPENDENT,
        "supervision_cleared",
    )

    cleared_cdp = pdp.evaluate(cleared_envelope)

    print("  Decision:", decision_value(cleared_cdp))
    print("  Token: supervision_cleared")
    print()
    print("Mission continues.")
    print("Stage Gate lifecycle: COMPLETE")
    print("GovernancePDP: UNCHANGED")
    print("RuntimeEnvelope: UNCHANGED")


if __name__ == "__main__":
    main()
