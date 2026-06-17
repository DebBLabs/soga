from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from builders.protocol_projection import (
    mission_to_aauth_artifact,
    mission_to_ucan_artifact,
    mission_to_zcap_artifact,
)
from execution.simple_pep import SimplePEP
from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from input_adapters.ucan_adapter import ucan_to_runtime_envelope_v0_1
from input_adapters.zcap_adapter import zcap_to_runtime_envelope_v0_1
from verify.governance_pdp import GovernancePDP
from verify.mission_template import MissionLifecycle, MissionTemplate


def load_generated_mission(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def generated_to_mission_template(data: dict) -> MissionTemplate:
    actions = data.get("allowed_actions") or ["execute_mission"]

    return MissionTemplate(
        mission_id=str(data["mission_id"]),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(data.get("subject", {}).get("subject_id", "subject-001")),
        objective=str(data.get("objective", "")),
        allowed_actions=list(actions),
        forbidden_actions=list(data.get("hard_constraints", [])),
        bounds={
            "preferences": data.get("preferences", []),
            "hard_constraints": data.get("hard_constraints", []),
            "fallback_behaviors": data.get("fallback_behaviors", []),
        },
        references={
            "title": data.get("title"),
            "source_reference_mission": data.get("source_reference_mission"),
            "governance_questions": data.get("governance_questions", []),
        },
        metadata={
            "builder": "run_generated_mission",
            "subject_agency_state": data.get("governance", {}).get("subject_agency_state", "ACTIVE"),
            "evaluate_at_execution": data.get("governance", {}).get("evaluate_at_execution", True),
        },
    )


def envelope_from_protocol(protocol: str, mission: MissionTemplate):
    protocol = protocol.lower()

    if protocol == "aauth":
        artifact = mission_to_aauth_artifact(mission)
        mission_statement = first_mission_statement(artifact)
        if mission_statement is None:
            raise RuntimeError("No AAuth mission statement found")
        return mission_statement_to_runtime_envelope_v0_1(artifact, mission_statement)

    if protocol == "ucan":
        return ucan_to_runtime_envelope_v0_1(mission_to_ucan_artifact(mission))

    if protocol == "zcap":
        return zcap_to_runtime_envelope_v0_1(mission_to_zcap_artifact(mission))

    raise ValueError(f"Unsupported protocol: {protocol}")


def run(path: str, protocol: str, state: str) -> dict:
    data = deepcopy(load_generated_mission(path))
    data.setdefault("governance", {})
    data["governance"]["subject_agency_state"] = state

    mission = generated_to_mission_template(data)
    envelope = envelope_from_protocol(protocol, mission)
    decision = GovernancePDP().evaluate(envelope)
    execution_status = SimplePEP().enforce(decision)

    return {
        "mission": mission.to_dict(),
        "runtime_envelope": envelope.to_dict(),
        "decision_package": decision.to_dict(),
        "execution_status": execution_status.to_dict(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a generated canonical mission through SOGA."
    )
    parser.add_argument("generated_mission_file")
    parser.add_argument("--protocol", choices=["aauth", "ucan", "zcap"], default="aauth")
    parser.add_argument("--state", default="ACTIVE")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    result = run(args.generated_mission_file, args.protocol, args.state)

    if args.summary:
        envelope = result["runtime_envelope"]
        decision = result["decision_package"]
        status = result["execution_status"]

        print("SOGA Generated Mission Run")
        print("==========================")
        print(f"mission_id: {envelope['mission']['mission_id']}")
        print(f"protocol: {envelope['authority']['source_protocol']}")
        print(f"subject_state: {envelope['subject']['governance_state']}")
        print(f"decision: {decision['decision']}")
        print(f"execution_status: {status['execution_status']}")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
