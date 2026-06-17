from __future__ import annotations

import argparse
import json
from copy import deepcopy

from builders.mission_builder import build_mission_template, load_mission_file
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


def envelope_from_protocol(protocol: str, mission):
    protocol = protocol.lower()

    if protocol == "aauth":
        artifact = mission_to_aauth_artifact(mission)
        mission_statement = first_mission_statement(artifact)
        if mission_statement is None:
            raise RuntimeError("No AAuth mission statement found")
        return mission_statement_to_runtime_envelope_v0_1(artifact, mission_statement)

    if protocol == "ucan":
        artifact = mission_to_ucan_artifact(mission)
        return ucan_to_runtime_envelope_v0_1(artifact)

    if protocol == "zcap":
        artifact = mission_to_zcap_artifact(mission)
        return zcap_to_runtime_envelope_v0_1(artifact)

    raise ValueError(f"Unsupported protocol: {protocol}")


def run_mission(path: str, protocol: str, state: str) -> dict:
    data = deepcopy(load_mission_file(path))
    data.setdefault("governance", {})
    data["governance"]["subject_agency_state"] = state

    mission = build_mission_template(data)
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
        description="Run a SOGA mission through protocol projection, adapter, Governance PDP, and PEP."
    )
    parser.add_argument("mission_file", help="Path to mission JSON file")
    parser.add_argument(
        "--protocol",
        choices=["aauth", "ucan", "zcap"],
        default="aauth",
        help="Protocol projection path to use",
    )
    parser.add_argument(
        "--state",
        default="ACTIVE",
        help="Subject agency/governance state assertion, e.g. ACTIVE, IMPAIRED, LAPSED",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print only a compact summary",
    )

    args = parser.parse_args()

    result = run_mission(args.mission_file, args.protocol, args.state)

    if args.summary:
        envelope = result["runtime_envelope"]
        decision = result["decision_package"]
        status = result["execution_status"]

        print("SOGA Mission Run")
        print("================")
        print(f"mission_id: {envelope['mission']['mission_id']}")
        print(f"protocol: {envelope['authority']['source_protocol']}")
        print(f"subject_state: {envelope['subject']['governance_state']}")
        print(f"decision: {decision['decision']}")
        print(f"execution_status: {status['execution_status']}")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
