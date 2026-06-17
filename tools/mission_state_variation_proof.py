from __future__ import annotations

import argparse
from copy import deepcopy

from builders.mission_builder import (
    build_mission_template,
    load_mission_file,
)
from builders.protocol_projection import mission_to_aauth_artifact
from execution.simple_pep import SimplePEP
from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from verify.governance_pdp import GovernancePDP


def run_state(
    mission_file: str,
    subject_agency_state: str,
) -> None:
    data = deepcopy(load_mission_file(mission_file))
    data.setdefault("governance", {})
    data["governance"]["subject_agency_state"] = subject_agency_state

    mission = build_mission_template(data)
    artifact = mission_to_aauth_artifact(mission)

    mission_statement = first_mission_statement(artifact)
    if mission_statement is None:
        raise RuntimeError("No AAuth mission statement found")

    envelope = mission_statement_to_runtime_envelope_v0_1(
        artifact,
        mission_statement,
    )

    decision = GovernancePDP().evaluate(envelope)
    status = SimplePEP().enforce(decision)

    print(
        f"{subject_agency_state} "
        f"-> {decision.decision.value} "
        f"-> {status.execution_status.value}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run governance state variation proof."
    )
    parser.add_argument(
        "mission_file",
        nargs="?",
        default="missions/gift_purchase_mission.json",
        help="Mission JSON file",
    )
    args = parser.parse_args()

    print("Mission State Variation Proof")
    print("=============================")
    print("Same mission. Same protocol path. Different governance state.")
    print()

    run_state(args.mission_file, "ACTIVE")
    run_state(args.mission_file, "IMPAIRED")
    run_state(args.mission_file, "LAPSED")


if __name__ == "__main__":
    main()
