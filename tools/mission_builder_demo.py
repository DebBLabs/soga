from __future__ import annotations

import json
from pathlib import Path

from builders.mission_builder import (
    build_governed_mission,
    load_mission_file,
)
from engines.capability_registry import CapabilityRegistry
from engines.governed_execution_loop import GovernedExecutionLoop
from verify.runtime_envelope_model import SubjectGovernanceState


MISSION_FIXTURE = Path(
    "tests/fixtures/missions/caregiver_discharge_followup.json"
)
CAPABILITY_FIXTURES = Path("tests/fixtures/capabilities")


def load_registry():
    registry = CapabilityRegistry()

    for fixture_path in sorted(CAPABILITY_FIXTURES.glob("*.json")):
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


def print_record(record):
    print(f"stage_gate_state: {record['stage_gate_state']}")
    print(f"route: {record['route']}")

    if "governance_decision" in record:
        print(f"cdp_decision: {record['governance_decision']}")

    if "interruption" in record:
        print("interruption_record:")
        print(f"  step_id: {record['interruption']['step_id']}")
        print(f"  reason: {record['interruption']['reason']}")

    if "capability_resolution" in record:
        resolution = record["capability_resolution"]
        print(f"capability: {resolution['canonical_name']}")
        print("implementations:")
        for implementation in resolution["implementations"]:
            print(
                f"  - {implementation['type']}: "
                f"{implementation['stub_endpoint']}"
            )


def main():
    source = load_mission_file(MISSION_FIXTURE)
    mission = build_governed_mission(source)
    steps = source["steps"]

    loop = GovernedExecutionLoop(
        capability_registry=load_registry(),
    )

    print("=== Mission Builder Demo ===")
    print("Mission loaded from fixture.")
    print(f"mission_id: {mission['mission_id']}")
    print(f"objective: {mission['objective']}")
    print()

    print("Phase 1 — Authored mission enters governed execution")
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

    print("Phase 3 — Supervisor clearance provided")
    clearance_evidence = {
        "supervisor_confirmation": True,
        "governance_reasoning_token": "supervision_required",
    }
    print(f"runtime_evidence: {clearance_evidence}")
    print()

    print("Phase 4 — Resubmission, CDP trail, capability resolution")
    phase_4 = loop.run(
        mission,
        steps,
        SubjectGovernanceState.INDEPENDENT,
        clearance_evidence,
    )
    print_record(phase_4["records"][0])
    print()

    print("Boundary")
    print("--------")
    print("MissionBuilder authors the mission package.")
    print("GovernedExecutionLoop routes execution.")
    print("GovernancePDP emits CDP decisions.")
    print("CapabilityRegistry describes implementation options.")


if __name__ == "__main__":
    main()
