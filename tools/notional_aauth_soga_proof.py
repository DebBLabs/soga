from __future__ import annotations

import json

from input_adapters.notional_aauth_adapter import from_notional_aauth
from verify.governance_pdp import GovernancePDP


def build_payload(governance_state: str) -> dict:
    return {
        "request": {
            "request_id": f"req-aauth-{governance_state.lower()}",
            "requested_action": "step1",
        },
        "mission": {
            "mission_id": "mission-aauth-notional-001",
            "lifecycle": "ACTIVE",
            "subject_id": "subject-001",
            "description": "Demonstrate AAuth-shaped input into SOGA Runtime Envelope.",
            "allowed_actions": ["step1"],
        },
        "authority": {
            "authority_id": "authority-aauth-notional-001",
            "authority_type": "aauth",
            "allowed_actions": ["step1"],
            "references": {
                "notional_token": "aa-auth+jwt-placeholder"
            },
        },
        "subject": {
            "subject_id": "subject-001",
            "governance_state": governance_state,
            "reachability": "REACHABLE",
        },
        "policy": {
            "profile": "soga-baseline-v0.1"
        },
    }


def print_case(title: str, payload: dict) -> None:
    envelope = from_notional_aauth(payload)
    decision = GovernancePDP().evaluate(envelope)

    print(title)
    print("-" * len(title))
    print("source_protocol:", envelope.authority.source_protocol)
    print("mission_id:", envelope.mission.mission_id)
    print("subject_state:", envelope.subject.governance_state.value)
    print(json.dumps(decision.to_dict(), indent=2))
    print()


def main() -> None:
    print("Notional AAuth -> SOGA Proof")
    print("============================")
    print("Same AAuth-shaped mission.")
    print("Same AAuth-shaped authority.")
    print("Same requested action.")
    print("Different Subject Governance State.")
    print("Same Governance PDP.")
    print("Different Decision Package.")
    print()

    print_case("CASE 1: INDEPENDENT subject", build_payload("INDEPENDENT"))
    print_case("CASE 2: SUPERVISED subject", build_payload("SUPERVISED"))
    print_case("CASE 3: LAPSED subject", build_payload("LAPSED"))


if __name__ == "__main__":
    main()
