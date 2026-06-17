from __future__ import annotations

import json
from copy import deepcopy

from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from tools.aauth_test_payloads import build_aauth_mission_payload
from verify.governance_pdp import GovernancePDP


def evaluate_payload(payload: dict) -> dict:
    mission_statement = first_mission_statement(payload)

    if mission_statement is None:
        raise RuntimeError("No AAuth mission statement found")

    envelope = mission_statement_to_runtime_envelope_v0_1(
        payload,
        mission_statement,
    )

    decision = GovernancePDP().evaluate(envelope)

    return {
        "envelope": envelope.to_dict(),
        "decision": decision.to_dict(),
    }


def print_case(label: str, payload: dict) -> None:
    result = evaluate_payload(payload)
    envelope = result["envelope"]
    decision = result["decision"]

    print(label)
    print("-" * len(label))
    print("source_protocol:", envelope["authority"]["source_protocol"])
    print("mission_id:", envelope["mission"]["mission_id"])
    print("subject_id:", envelope["subject"]["subject_id"])
    print("subject_agency_state:", envelope["subject"]["governance_state"])
    print("raw_subject_agency_state:", envelope["subject"]["context"]["subject_agency_state_raw"])
    print(json.dumps(decision, indent=2))
    print()


def main() -> None:
    active_payload = build_aauth_mission_payload("ACTIVE")

    impaired_payload = deepcopy(active_payload)
    impaired_payload["subject_agency_state"] = "IMPAIRED"

    lapsed_payload = deepcopy(active_payload)
    lapsed_payload["subject_agency_state"] = "LAPSED"

    print("AAuth Mission Statement -> SOGA v0.1 Runtime Envelope Proof")
    print("==========================================================")
    print("Same AAuth/RAR-style mission statement.")
    print("Same authority evidence.")
    print("Same requested action.")
    print("Different subject_agency_state assertion.")
    print("Same canonical Governance PDP.")
    print("Different Decision Package.")
    print()

    print_case("CASE 1: ACTIVE subject agency state", active_payload)
    print_case("CASE 2: IMPAIRED subject agency state", impaired_payload)
    print_case("CASE 3: LAPSED subject agency state", lapsed_payload)


if __name__ == "__main__":
    main()
