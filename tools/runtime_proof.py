from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from policy_gate.policy_gate import PolicyGate


def run_case(name, payload):
    gate = PolicyGate(policy_id="test", policy_version="0.1")
    result = gate.evaluate(payload)
    decision = result["decision"]
    runtime_refs = result.get("runtime_refs", {})

    print(f"\n{name}")
    print("-" * len(name))
    print(f"status: {decision['status']}")
    print(f"allow: {decision['allow']}")
    print(f"rule: {decision['rule']}")
    print(f"reason: {decision['reason']}")
    print(f"request_id: {runtime_refs.get('request_id')}")
    print(f"mission_id: {runtime_refs.get('mission_id')}")
    print(f"subject_id: {runtime_refs.get('subject_id')}")
    print(f"delegation_id: {runtime_refs.get('delegation_id')}")


run_case(
    "FLAT: ACTIVE subject allows clean supervised request",
    {
        "action_type": "step1",
        "allowed_actions": ["step1"],
        "supervision_required": True,
        "guest_present": False,
        "operator_present": True,
        "subject_agency_state": "INDEPENDENT",
    },
)

run_case(
    "FLAT: IMPAIRED subject restricts supervised request",
    {
        "action_type": "step1",
        "allowed_actions": ["step1"],
        "supervision_required": True,
        "guest_present": False,
        "operator_present": True,
        "subject_agency_state": "SUPERVISED",
    },
)

run_case(
    "FLAT: Out-of-scope action denies request",
    {
        "action_type": "step9",
        "allowed_actions": ["step1"],
        "supervision_required": False,
        "guest_present": False,
        "operator_present": True,
        "subject_agency_state": "INDEPENDENT",
    },
)

run_case(
    "ENVELOPE: IMPAIRED subject restricts supervised request",
    {
        "mission": {
            "mission_id": "mission-test-001",
            "action_type": "step1",
            "allowed_actions": ["step1"],
            "supervision_required": True,
            "forbidden_conditions": [],
        },
        "subject": {
            "subject_id": "subject-001",
            "subject_agency_state": "SUPERVISED",
        },
        "delegation": {
            "delegation_id": "del-test-001",
            "credential_refs": [],
            "parent_request_id": None,
            "revoked": False,
            "expires_at": "2026-12-31T12:00:00Z",
        },
        "execution_context": {
            "guest_present": False,
            "operator_present": True,
            "source": "runtime_proof_envelope",
        },
    },
)

run_case(
    "ENVELOPE: Out-of-scope action denies request",
    {
        "mission": {
            "mission_id": "mission-test-002",
            "action_type": "step9",
            "allowed_actions": ["step1"],
            "supervision_required": False,
            "forbidden_conditions": [],
        },
        "subject": {
            "subject_id": "subject-001",
            "subject_agency_state": "INDEPENDENT",
        },
        "delegation": {
            "delegation_id": "del-test-002",
            "credential_refs": [],
            "parent_request_id": None,
            "revoked": False,
            "expires_at": "2026-12-31T12:00:00Z",
        },
        "execution_context": {
            "guest_present": False,
            "operator_present": True,
            "source": "runtime_proof_envelope",
        },
    },
)

run_case(
    "RAR: Mission Statement restricts via SOGA constraints",
    {
        "authorization_details": [
            {
                "type": "aauth_mission_statement",
                "mission_id": "mission-rar-001",
                "subject_id": "subject-001",
                "delegation_id": "del-rar-001",
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
        "source": "runtime_proof_rar_mission_statement",
    },
)