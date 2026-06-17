from __future__ import annotations

import argparse
import json

from builders.mission_builder import mission_file_to_template
from builders.protocol_projection import (
    mission_to_aauth_artifact,
    mission_to_ucan_artifact,
    mission_to_zcap_artifact,
)
from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from input_adapters.ucan_adapter import (
    ucan_to_runtime_envelope_v0_1,
)
from input_adapters.zcap_adapter import (
    zcap_to_runtime_envelope_v0_1,
)
from verify.governance_pdp import GovernancePDP


def cdp_summary(label, envelope):
    decision = GovernancePDP().evaluate(envelope)

    return {
        "path": label,
        "source_protocol": envelope.authority.source_protocol,
        "mission_id": envelope.mission.mission_id,
        "subject_agency_state": envelope.subject.governance_state.value,
        "governance_determination": decision.decision.value,
        "reason_class": decision.reason_class,
        "rule": decision.rule,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Show protocol independence for one mission."
    )
    parser.add_argument(
        "mission_file",
        nargs="?",
        default="missions/gift_purchase_mission.json",
        help="Mission JSON file",
    )
    args = parser.parse_args()

    mission = mission_file_to_template(args.mission_file)

    aauth_artifact = mission_to_aauth_artifact(mission)
    mission_statement = first_mission_statement(
        aauth_artifact
    )
    if mission_statement is None:
        raise RuntimeError("No AAuth mission statement found")

    cases = [
        (
            "AAuth",
            mission_statement_to_runtime_envelope_v0_1(
                aauth_artifact,
                mission_statement,
            ),
        ),
        (
            "UCAN",
            ucan_to_runtime_envelope_v0_1(
                mission_to_ucan_artifact(mission)
            ),
        ),
        (
            "ZCAP",
            zcap_to_runtime_envelope_v0_1(
                mission_to_zcap_artifact(mission)
            ),
        ),
    ]

    results = [
        cdp_summary(label, envelope)
        for label, envelope in cases
    ]

    print(
        "SOGA PROTOCOL INDEPENDENCE DEMO"
    )
    print(
        "==============================="
    )
    print()
    print(
        "Same mission + same Subject Agency State "
        "+ different protocol -> same governance outcome"
    )
    print()
    print(
        json.dumps(
            results,
            indent=2,
            default=str,
        )
    )

    outcomes = {
        result["governance_determination"]
        for result in results
    }

    if len(outcomes) != 1:
        raise AssertionError(
            "Protocol switch changed governance outcome"
        )

    print()
    print(
        "PASS: protocol changed; governance outcome did not."
    )


if __name__ == "__main__":
    main()
