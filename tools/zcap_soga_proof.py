from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from input_adapters.zcap_adapter import zcap_to_envelope
from policy_gate.policy_gate import PolicyGate


def build_zcap_payload(subject_agency_state: str) -> Dict[str, Any]:
    return {
        "capability": {
            "@context": "https://w3id.org/security/v2",
            "id": "urn:zcap:demo:step1",
            "type": "Capability",
            "controller": "subject-001",
            "parentCapability": "urn:zcap:root:demo",
            "invocationTarget": "resource://demo/step1",
            "allowedAction": ["step1"],
            "caveat": [
                {
                    "type": "SOGARuntimeGovernanceCaveat",
                    "restrict_if_subject_agency_state": [
                        "IMPAIRED",
                        "HELD",
                        "UNREACHABLE",
                    ],
                }
            ],
            "expirationDate": "2026-12-31T12:00:00Z",
        },
        "mission_id": "mission-zcap-soga-001",
        "subject_agency_state": subject_agency_state,
        "supervision_required": True,
        "source": "zcap_soga_proof",
    }


def print_case(label: str, payload: Dict[str, Any], result: Dict[str, Any]) -> None:
    capability = payload.get("capability", {})
    decision = result.get("decision", {})
    runtime_refs = result.get("runtime_refs", {})

    print(f"\n{label}")
    print("-" * len(label))
    print(f"subject_agency_state: {payload.get('subject_agency_state')}")
    print(f"status: {decision.get('status')}")
    print(f"allow: {decision.get('allow')}")
    print(f"rule: {decision.get('rule')}")
    print(f"reason: {decision.get('reason')}")
    print(f"mission_id: {runtime_refs.get('mission_id')}")
    print(f"subject_id: {runtime_refs.get('subject_id')}")
    print(f"delegation_id: {runtime_refs.get('delegation_id')}")
    print(f"capability_id: {capability.get('id')}")
    print(f"parent_capability: {capability.get('parentCapability')}")
    print(f"invocation_target: {capability.get('invocationTarget')}")
    print(f"allowed_action: {capability.get('allowedAction')}")
    print(f"caveat: {capability.get('caveat')}")


def main() -> None:
    gate = PolicyGate(policy_id="P03-delex-stub", policy_version="0.1.0")

    active_payload = build_zcap_payload("ACTIVE")
    impaired_payload = deepcopy(active_payload)
    impaired_payload["subject_agency_state"] = "IMPAIRED"

    active_envelope = zcap_to_envelope(active_payload)
    impaired_envelope = zcap_to_envelope(impaired_payload)

    active_result = gate.evaluate(active_envelope)
    impaired_result = gate.evaluate(impaired_envelope)

    print("ZCAP + SOGA Proof")
    print("=================")
    print("Same ZCAP-shaped capability artifact.")
    print("Same parent capability, invocation target, and allowed action.")
    print("Different subject_agency_state.")
    print("Different execution-time governance outcome.")

    print_case("CASE 1: ACTIVE subject", active_payload, active_result)
    print_case("CASE 2: IMPAIRED subject", impaired_payload, impaired_result)


if __name__ == "__main__":
    main()
