from __future__ import annotations

import json
from pathlib import Path

from engines.capability_registry import CapabilityRegistry
from engines.governed_execution_loop import GovernedExecutionLoop
from verify.runtime_envelope_model import SubjectGovernanceState


FIXTURE_DIR = Path("tests/fixtures/capabilities")


def load_registry():
    registry = CapabilityRegistry()

    for fixture_path in sorted(FIXTURE_DIR.glob("*.json")):
        with fixture_path.open("r", encoding="utf-8") as fixture_file:
            capability = json.load(fixture_file)

        registry.register(
            canonical_name=capability["canonical_name"],
            implementations=capability["implementations"],
            required_authority_scope=capability["required_authority_scope"],
            governance_dimensions_affected=(
                capability["governance_dimensions_affected"]
            ),
        )

    return registry


def build_mission():
    return {
        "mission_id": "caregiver-discharge-follow-up",
        "subject_id": "subject-001",
        "authority_id": "authority-caregiver-001",
        "objective": "Schedule caregiver discharge follow-up appointment.",
        "scenario": "caregiver_discharge_follow_up",
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


def build_steps():
    return [
        {
            "step_id": "schedule_appointment",
            "action": "schedule_appointment",
            "required_capability": "appointment.schedule",
            "governance_reasoning_token": "supervision_required",
        }
    ]


def print_record(record):
    print(f"stage_gate_state: {record['stage_gate_state']}")
    print(f"route: {record['route']}")

    if "governance_decision" in record:
        print(f"governance_decision: {record['governance_decision']}")

    if "interruption" in record:
        print("interruption_record:")
        print(f"  step_id: {record['interruption']['step_id']}")
        print(f"  reason: {record['interruption']['reason']}")

    if "capability_resolution" in record:
        resolution = record["capability_resolution"]
        print(f"capability: {resolution['canonical_name']}")
        print("available_implementations:")
        for implementation in resolution["implementations"]:
            print(
                f"  - {implementation['type']}: "
                f"{implementation['stub_endpoint']}"
            )


def main():
    mission = build_mission()
    steps = build_steps()
    loop = GovernedExecutionLoop(
        capability_registry=load_registry(),
    )

    print("=== Governed Execution Loop Demo ===")
    print("Scenario: caregiver discharge follow-up")
    print()

    print("Phase 1 — Stage Gate fires")
    phase_1 = loop.run(
        mission,
        steps,
        SubjectGovernanceState.SUPERVISED,
        {},
    )
    print_record(phase_1["records"][0])
    print()

    print("Phase 2 — Interruption record created")
    print(f"interruptions: {len(loop.interruptions)}")
    print()

    print("Phase 3 — Clearance provided")
    clearance_evidence = {
        "supervisor_confirmation": True,
        "governance_reasoning_token": "supervision_required",
    }
    print(f"runtime_evidence: {clearance_evidence}")
    print()

    print("Phase 4 — Resubmission and capability resolution")
    phase_4 = loop.run(
        mission,
        steps,
        SubjectGovernanceState.INDEPENDENT,
        clearance_evidence,
    )
    print_record(phase_4["records"][0])
    print()

    print("Governance Boundary")
    print("-------------------")
    print("StageGateEngine determines when governance is invoked.")
    print("GovernancePDP determines the governance decision.")
    print("CapabilityRegistry resolves implementation options only.")


if __name__ == "__main__":
    main()
