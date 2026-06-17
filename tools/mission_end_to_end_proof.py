from __future__ import annotations

import argparse
import json

from builders.mission_builder import mission_file_to_template
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


def run_case(label: str, envelope):
    decision = GovernancePDP().evaluate(envelope)
    status = SimplePEP().enforce(decision)

    print(label)
    print("-" * len(label))
    print("source_protocol:", envelope.authority.source_protocol)
    print("mission_id:", envelope.mission.mission_id)
    print("decision:", decision.decision.value)
    print("execution_status:", status.execution_status.value)
    print(json.dumps(status.to_dict(), indent=2))
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run end-to-end proof for a mission."
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
    mission_statement = first_mission_statement(aauth_artifact)
    if mission_statement is None:
        raise RuntimeError("No AAuth mission statement found")

    aauth_envelope = mission_statement_to_runtime_envelope_v0_1(
        aauth_artifact,
        mission_statement,
    )

    ucan_artifact = mission_to_ucan_artifact(mission)
    ucan_envelope = ucan_to_runtime_envelope_v0_1(ucan_artifact)

    zcap_artifact = mission_to_zcap_artifact(mission)
    zcap_envelope = zcap_to_runtime_envelope_v0_1(zcap_artifact)

    print("Mission End-to-End Proof")
    print("========================")
    print(
        "Mission JSON -> MissionTemplate -> Protocol Projections "
        "-> Adapters -> RuntimeEnvelope -> GovernancePDP -> PEP"
    )
    print()

    run_case("AAuth path", aauth_envelope)
    run_case("UCAN path", ucan_envelope)
    run_case("ZCAP path", zcap_envelope)


if __name__ == "__main__":
    main()
