from __future__ import annotations

import argparse
import json
from copy import deepcopy

from builders.mission_builder import (
    build_mission_template,
    load_mission_file,
)
from builders.protocol_projection import (
    mission_to_aauth_artifact,
)
from execution.simple_pep import SimplePEP
from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from verify.governance_pdp import GovernancePDP


def run_state(mission_file: str, subject_agency_state: str):
    data = deepcopy(load_mission_file(mission_file))
    data.setdefault("governance", {})
    data["governance"][
        "subject_agency_state"
    ] = subject_agency_state

    mission = build_mission_template(data)
    artifact = mission_to_aauth_artifact(mission)

    mission_statement = first_mission_statement(
        artifact
    )
    if mission_statement is None:
        raise RuntimeError(
            "No AAuth mission statement found"
        )

    envelope = mission_statement_to_runtime_envelope_v0_1(
        artifact,
        mission_statement,
    )

    decision = GovernancePDP().evaluate(envelope)
    status = SimplePEP().enforce(decision)

    return {
        "subject_agency_state":
            subject_agency_state,
        "source_protocol":
            envelope.authority.source_protocol,
        "mission_id":
            envelope.mission.mission_id,
        "governance_determination":
            decision.decision.value,
        "restrict_mode":
            decision.constraints.get("restrict_mode"),
        "execution_status":
            status.execution_status.value,
        "execution_receipt":
            status.to_dict(),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Show governance outcome changes across subject agency states."
    )
    parser.add_argument(
        "mission_file",
        nargs="?",
        default="missions/gift_purchase_mission.json",
        help="Mission JSON file",
    )
    args = parser.parse_args()

    results = [
        run_state(args.mission_file, "INDEPENDENT"),
        run_state(args.mission_file, "SUPERVISED"),
        run_state(args.mission_file, "LAPSED"),
    ]

    print("SOGA SUBJECT AGENCY STATE DEMO")
    print("==============================")
    print()
    print(
        "Same mission + same protocol + different "
        "Subject Agency State -> different governance outcome"
    )
    print()
    print(
        json.dumps(
            results,
            indent=2,
            default=str,
        )
    )

    expected = {
        "INDEPENDENT": "ALLOW",
        "SUPERVISED": "RESTRICT",
        "LAPSED": "DENY",
    }

    for result in results:
        state = result["subject_agency_state"]
        if (
            result["governance_determination"]
            != expected[state]
        ):
            raise AssertionError(
                f"{state} expected {expected[state]} "
                f"but got {result['governance_determination']}"
            )

    restrict = [
        result
        for result in results
        if result["governance_determination"]
        == "RESTRICT"
    ][0]

    if not restrict["restrict_mode"]:
        raise AssertionError(
            "RESTRICT missing named restrict_mode"
        )

    print()
    print(
        "PASS: subject state changed; "
        "governance outcome changed."
    )


if __name__ == "__main__":
    main()
