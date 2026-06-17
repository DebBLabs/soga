from __future__ import annotations

from typing import Any, Dict

from input_adapters.aauth_adapter import first_mission_statement, mission_statement_to_envelope
from input_adapters.sample_adapter import sample_artifact_to_envelope
from policy_gate.policy_gate import PolicyGate


def print_result(label: str, result: Dict[str, Any]) -> str:
    decision = result.get("decision", {})
    status = decision.get("status")
    rule = decision.get("rule")
    reason = decision.get("reason")

    print(f"\n{label}")
    print("-" * len(label))
    print(f"status: {status}")
    print(f"rule: {rule}")
    print(f"reason: {reason}")

    return str(status)


def main() -> None:
    gate = PolicyGate(policy_id="P03-delex-stub", policy_version="0.1.0")

    aauth_payload = {
        "authorization_details": [
            {
                "type": "aauth_mission_statement",
                "mission_id": "mission-aauth-interop-001",
                "subject_id": "subject-001",
                "delegation_id": "del-aauth-interop-001",
                "actions": ["step1"],
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
        "subject_agency_state": "SUPERVISED",
        "guest_present": False,
        "operator_present": True,
        "source": "input_adapter_proof_aauth",
    }

    mission_statement = first_mission_statement(aauth_payload)
    if mission_statement is None:
        raise RuntimeError("No AAuth mission statement found")

    aauth_envelope = mission_statement_to_envelope(
        aauth_payload,
        mission_statement,
    )

    sample_payload = {
        "mission_id": "mission-sample-interop-001",
        "subject_id": "subject-001",
        "delegation_id": "del-sample-interop-001",
        "action": "step1",
        "allowed_actions": ["step1"],
        "supervision_required": True,
        "subject_agency_state": "SUPERVISED",
        "source": "input_adapter_proof_sample",
    }

    sample_envelope = sample_artifact_to_envelope(sample_payload)

    aauth_result = gate.evaluate(aauth_envelope)
    sample_result = gate.evaluate(sample_envelope)

    aauth_status = print_result("AAUTH INPUT ADAPTER RESULT", aauth_result)
    sample_status = print_result("SAMPLE INPUT ADAPTER RESULT", sample_result)

    print("\nINTEROP CHECK")
    print("-------------")
    print(f"same_status: {aauth_status == sample_status}")
    print(f"expected_status: RESTRICT")


if __name__ == "__main__":
    main()