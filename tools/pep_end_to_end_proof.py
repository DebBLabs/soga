from __future__ import annotations

import json
from copy import deepcopy

from execution.simple_pep import SimplePEP
from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from tools.aauth_test_payloads import build_aauth_mission_payload
from verify.governance_pdp import GovernancePDP


def evaluate_and_enforce(payload: dict) -> dict:
    mission_statement = first_mission_statement(payload)

    if mission_statement is None:
        raise RuntimeError("No AAuth mission statement found")

    envelope = mission_statement_to_runtime_envelope_v0_1(
        payload,
        mission_statement,
    )

    decision_package = GovernancePDP().evaluate(envelope)
    execution_status = SimplePEP().enforce(decision_package)

    return {
        "envelope": envelope.to_dict(),
        "decision_package": decision_package.to_dict(),
        "execution_status": execution_status.to_dict(),
    }


def print_case(label: str, payload: dict) -> None:
    result = evaluate_and_enforce(payload)

    decision = result["decision_package"]
    status = result["execution_status"]

    print(label)
    print("-" * len(label))
    print("source_protocol:", result["envelope"]["authority"]["source_protocol"])
    print("subject_agency_state:", result["envelope"]["subject"]["governance_state"])
    print("decision:", decision["decision"])
    print("rule:", decision["rule"])
    print("directives:", decision["directives"])
    print("execution_status:", status["execution_status"])
    print(json.dumps(status, indent=2))
    print()


def main() -> None:
    active_payload = build_aauth_mission_payload("ACTIVE")

    impaired_payload = deepcopy(active_payload)
    impaired_payload["subject_agency_state"] = "IMPAIRED"

    lapsed_payload = deepcopy(active_payload)
    lapsed_payload["subject_agency_state"] = "LAPSED"

    print("SOGA End-to-End PEP Proof")
    print("=========================")
    print("AAuth-shaped mission evidence.")
    print("Adapter normalizes to RuntimeEnvelope.")
    print("GovernancePDP produces DecisionPackage.")
    print("SimplePEP produces ExecutionStatus.")
    print()

    print_case("CASE 1: ACTIVE subject agency state", active_payload)
    print_case("CASE 2: IMPAIRED subject agency state", impaired_payload)
    print_case("CASE 3: LAPSED subject agency state", lapsed_payload)


if __name__ == "__main__":
    main()
