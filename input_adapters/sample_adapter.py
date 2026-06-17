from typing import Any, Dict


def sample_artifact_to_envelope(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mission": {
            "mission_id": payload.get("mission_id"),
            "action_type": payload.get("action"),
            "allowed_actions": payload.get("allowed_actions", []),
            "supervision_required": payload.get("supervision_required", False),
            "forbidden_conditions": [],
            "soga_constraints": {},
        },
        "subject": {
            "subject_id": payload.get("subject_id"),
            "subject_agency_state": payload.get(
                "subject_agency_state",
                "ACTIVE",
            ),
        },
        "delegation": {
            "delegation_id": payload.get("delegation_id"),
            "credential_refs": [],
            "parent_request_id": None,
            "revoked": False,
            "expires_at": "2026-12-31T12:00:00Z",
        },
        "execution_context": {
            "request_id": payload.get("request_id"),
            "guest_present": False,
            "operator_present": False,
            "evaluated_at": None,
            "source": "sample_adapter",
        },
    }