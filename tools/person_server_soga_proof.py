from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from policy_gate.policy_gate import PolicyGate


def build_aauth_mission_payload(subject_agency_state: str) -> Dict[str, Any]:
    return {
        "authorization_details": [
            {
                "type": "aauth_mission_statement",
                "mission_id": "mission-person-server-soga-001",
                "subject_id": "subject-001",
                "delegation_id": "del-person-server-soga-001",
                "agent_id": "agent-001",
                "person_server_id": "ps-001",
                "resource_id": "resource-001",
                "resource_ref": "resource://demo/step1",
                "actions": ["step1"],
                "r3_refs": ["r3-demo-step1"],
                "r3_granted": {
                    "actions": ["step1"],
                    "resource": "resource://demo/step1",
                },
                "r3_conditional": {
                    "requires_runtime_governance": True,
                },
                "soga_constraints": {
                    "supervision_required": True,
                    "restrict_if_subject_agency_state": [
                        "IMPAIRED",
                        "HELD",
                        "UNREACHABLE",
                    ],
                },
                "expires_at": "2026-12-31T12:00:00Z",
            }
        ],
        "subject_agency_state": subject_agency_state,
        "guest_present": False,
        "operator_present": True,
        "source": "person_server_soga_proof",
    }


def mission_statement_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    authorization_details = payload.get("authorization_details", [])

    if not authorization_details:
        raise RuntimeError("No authorization_details found")

    mission_statement = authorization_details[0]

    if not isinstance(mission_statement, dict):
        raise RuntimeError("Mission statement is not a dictionary")

    return mission_statement


def print_case(label: str, payload: Dict[str, Any], result: Dict[str, Any]) -> None:
    mission_statement = mission_statement_from_payload(payload)
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
    print(f"agent_id: {mission_statement.get('agent_id')}")
    print(f"person_server_id: {mission_statement.get('person_server_id')}")
    print(f"resource_id: {mission_statement.get('resource_id')}")
    print(f"resource_ref: {mission_statement.get('resource_ref')}")
    print(f"r3_refs: {mission_statement.get('r3_refs')}")
    print(f"r3_granted: {mission_statement.get('r3_granted')}")
    print(f"r3_conditional: {mission_statement.get('r3_conditional')}")


def main() -> None:
    gate = PolicyGate(policy_id="P03-delex-stub", policy_version="0.1.0")

    active_payload = build_aauth_mission_payload("ACTIVE")
    impaired_payload = deepcopy(active_payload)
    impaired_payload["subject_agency_state"] = "IMPAIRED"

    active_result = gate.evaluate(active_payload)
    impaired_result = gate.evaluate(impaired_payload)

    print("AAuth Person Server + SOGA Proof")
    print("================================")
    print("Same AAuth-shaped mission and delegation.")
    print("Same agent, person server, resource, and R3 context.")
    print("Different subject_agency_state.")
    print("Different execution-time governance outcome.")

    print_case("CASE 1: ACTIVE subject", active_payload, active_result)
    print_case("CASE 2: IMPAIRED subject", impaired_payload, impaired_result)


if __name__ == "__main__":
    main()
