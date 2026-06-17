from __future__ import annotations

import json
from copy import deepcopy

from input_adapters.ucan_adapter import ucan_to_runtime_envelope_v0_1
from verify.governance_pdp import GovernancePDP


def build_ucan_payload(subject_agency_state: str) -> dict:
    return {
        "ucan": {
            "iss": "did:key:subject-001",
            "aud": "did:key:agent-001",
            "jti": "ucan-demo-step1",
            "att": [
                {
                    "with": "resource://demo/step1",
                    "can": "step1",
                }
            ],
            "fct": {
                "mission_id": "mission-ucan-soga-001",
                "subject_id": "subject-001",
                "objective": "Demonstrate UCAN-shaped input into SOGA Runtime Envelope.",
                "subject_agency_state": subject_agency_state,
            },
            "exp": 1798718400,
        },
        "source": "ucan_runtime_envelope_v0_1_proof",
    }


def evaluate_payload(payload: dict) -> dict:
    envelope = ucan_to_runtime_envelope_v0_1(payload)
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
    print("authority_id:", envelope["authority"]["authority_id"])
    print("subject_id:", envelope["subject"]["subject_id"])
    print("subject_agency_state:", envelope["subject"]["governance_state"])
    print("raw_subject_agency_state:", envelope["subject"]["context"]["subject_agency_state_raw"])
    print(json.dumps(decision, indent=2))
    print()


def main() -> None:
    active_payload = build_ucan_payload("ACTIVE")

    impaired_payload = deepcopy(active_payload)
    impaired_payload["ucan"]["fct"]["subject_agency_state"] = "IMPAIRED"

    lapsed_payload = deepcopy(active_payload)
    lapsed_payload["ucan"]["fct"]["subject_agency_state"] = "LAPSED"

    print("UCAN Capability Token -> SOGA v0.1 Runtime Envelope Proof")
    print("=========================================================")
    print("Same UCAN-shaped capability token.")
    print("Same resource, audience, issuer, and allowed action.")
    print("Different subject_agency_state assertion.")
    print("Same canonical Governance PDP.")
    print("Different Decision Package.")
    print()

    print_case("CASE 1: ACTIVE subject agency state", active_payload)
    print_case("CASE 2: IMPAIRED subject agency state", impaired_payload)
    print_case("CASE 3: LAPSED subject agency state", lapsed_payload)


if __name__ == "__main__":
    main()
