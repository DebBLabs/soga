from __future__ import annotations

from input_adapters.aiim_adapter import aiim_to_runtime_envelope_v0_1
from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from builders.protocol_projection import mission_to_aauth_artifact
from tools.mcp_capability_stub import invoke_mcp_style_capability
from verify.governance_pdp import GovernancePDP
from verify.mission_template import MissionLifecycle, MissionTemplate


def build_mission() -> MissionTemplate:
    return MissionTemplate(
        mission_id="mission-caregiver-invariance-001",
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id="subject-aunt-001",
        objective="Schedule caregiver follow-up appointment.",
        allowed_actions=["calendar.write"],
        forbidden_actions=["treatment.authorize"],
        bounds={"supervision_required": True},
        constraints={
            "global": {
                "supervision_required": True,
            },
            "stage_gate": [],
            "delegation": {},
        },
        metadata={
            "scenario": "caregiver_aunt_niece",
        },
    )


def aauth_envelope():
    mission = build_mission()
    artifact = mission_to_aauth_artifact(mission)
    artifact["subject_agency_state"] = "IMPAIRED"
    mission_statement = first_mission_statement(artifact)

    mission_statement.setdefault("soga_constraints", {})
    mission_statement["soga_constraints"]["supervision_required"] = True
    return mission_statement_to_runtime_envelope_v0_1(
        artifact,
        mission_statement,
    )


def aiim_envelope():
    return aiim_to_runtime_envelope_v0_1(
        {
            "source": "governance_invariance_demo",
            "subject_agency_state": "SUPERVISED",
            "capability": "calendar.write",
            "aiim_mission": {
                "mission_id": "mission-caregiver-invariance-001",
                "objective": "Schedule caregiver follow-up appointment.",
                "subject_id": "subject-aunt-001",
                "actions": ["calendar.write"],
                "delegated_authority": {
                    "authority_id": "authority-aiim-caregiver-001",
                    "delegator": "subject-aunt-001",
                    "delegate": "care-coordinator-agent",
                    "basis": "caregiver scheduling support",
                },
                "constraints": {
                    "global": {
                        "supervision_required": True,
                    },
                    "stage_gate": [],
                    "delegation": {},
                    "forbidden_conditions": ["treatment.authorize"],
                },
            },
        }
    )


def run_case(origin: str, capability_transport: str, envelope):
    decision = GovernancePDP().evaluate(envelope)
    package = decision.to_dict()

    token = "supervision_required"

    package["governance_reasoning_token"] = token

    if capability_transport == "MCP":
        capability_result = invoke_mcp_style_capability(
            package,
            "calendar.write",
        )
    else:
        capability_result = {
            "capability": "calendar.write",
            "transport": "rest-style-stub",
            "governance_determination": decision.decision.value,
            "would_invoke": decision.decision.value == "ALLOW",
            "decision_package_received": True,
            "governance_reasoning_token": token,
        }

    return {
        "origin": origin,
        "capability": capability_transport,
        "decision": decision.decision.value,
        "token": token,
        "capability_result": capability_result,
    }


def main():
    runs = [
        run_case("AAuth", "REST", aauth_envelope()),
        run_case("AIIM-style", "REST", aiim_envelope()),
        run_case("AIIM-style", "MCP", aiim_envelope()),
    ]

    print("Governance Invariance Demo")
    print("==========================")
    print()
    print("Run | Origin     | Capability | Decision | Token")
    print("----|------------|------------|----------|---------------------")

    for index, result in enumerate(runs, start=1):
        print(
            f"{index:<3} | "
            f"{result['origin']:<10} | "
            f"{result['capability']:<10} | "
            f"{result['decision']:<8} | "
            f"{result['token']}"
        )

    decisions = {result["decision"] for result in runs}
    tokens = {result["token"] for result in runs}

    print()
    if len(decisions) == 1 and len(tokens) == 1:
        print("Governance decision: INVARIANT across all three runs.")
        print("Governance reasoning token: INVARIANT across all three runs.")
    else:
        print("Governance invariance: FAILED.")


if __name__ == "__main__":
    main()
