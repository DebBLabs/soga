from __future__ import annotations

import uuid
from typing import Any, Dict

from input_adapters.aauth_adapter import first_mission_statement, generate_request_id, mission_statement_to_envelope
from verify.phase1b_core import now_iso



def normalize_runtime_envelope(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize incoming requests into a canonical runtime envelope.

    Accepted input shapes:
    - legacy flat runtime payload
    - canonical runtime envelope
    - OAuth/RAR-style authorization_details containing an AAuth/SOGA Mission Statement
    """
    if all(key in payload for key in ("mission", "subject", "delegation", "execution_context")):
        envelope = dict(payload)
    else:
        mission_statement = first_mission_statement(payload)

        if mission_statement is not None:
            envelope = mission_statement_to_envelope(payload, mission_statement)
        else:
            envelope = {
                "mission": {
                    "mission_id": payload.get("mission_id"),
                    "action_type": payload.get("action_type")
                    or payload.get("action")
                    or payload.get("operation")
                    or "step1",
                    "allowed_actions": payload.get("allowed_actions"),
                    "supervision_required": payload.get("supervision_required", False),
                    "forbidden_conditions": payload.get("forbidden_conditions", []),
                },
                "subject": {
                    "subject_id": payload.get("subject_id") or payload.get("principal_id"),
                    "subject_agency_state": payload.get("subject_agency_state", "ACTIVE"),
                },
                "delegation": {
                    "delegation_id": payload.get("delegation_id"),
                    "credential_refs": payload.get("credential_refs", []),
                    "parent_request_id": payload.get("parent_request_id"),
                    "revoked": payload.get("revoked", False),
                    "expires_at": payload.get("expires_at", "2026-12-31T12:00:00Z"),
                },
                "execution_context": {
                    "request_id": payload.get("request_id") or generate_request_id(),
                    "guest_present": payload.get("guest_present", False),
                    "operator_present": payload.get("operator_present", False),
                    "evaluated_at": payload.get("evaluated_at"),
                    "source": payload.get("source", "runtime_envelope"),
                },
            }

    envelope.setdefault("mission", {})
    envelope.setdefault("subject", {})
    envelope.setdefault("delegation", {})
    envelope.setdefault("execution_context", {})
    envelope.setdefault(
        "advisory_inputs",
        {
            "advisory_agents": [],
        },
    )

    envelope["execution_context"].setdefault("request_id", generate_request_id())
    envelope["execution_context"].setdefault("evaluated_at", now_iso())
    envelope["execution_context"].setdefault("source", "runtime_envelope")

    if envelope["execution_context"].get("evaluated_at") is None:
        envelope["execution_context"]["evaluated_at"] = now_iso()

    envelope["mission"].setdefault("mission_id", None)
    envelope["mission"].setdefault("forbidden_conditions", [])
    envelope["mission"].setdefault("soga_constraints", {})

    envelope["delegation"].setdefault("delegation_id", None)
    envelope["delegation"].setdefault("credential_refs", [])
    envelope["delegation"].setdefault("parent_request_id", None)
    envelope["delegation"].setdefault("expires_at", "2026-12-31T12:00:00Z")
    envelope["delegation"].setdefault("revoked", False)

    envelope["subject"].setdefault("subject_id", None)
    envelope["subject"].setdefault("subject_agency_state", "ACTIVE")

    return envelope


def flatten_runtime_envelope(envelope: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten a canonical runtime envelope back into the current Phase 1B evaluator shape.

    This keeps the existing PolicyGate/evaluator stable while introducing
    mission/subject/delegation/execution_context boundaries.
    """
    mission = envelope.get("mission", {})
    subject = envelope.get("subject", {})
    delegation = envelope.get("delegation", {})
    execution_context = envelope.get("execution_context", {})

    action_type = (
        mission.get("action_type")
        or mission.get("action")
        or mission.get("operation")
        or "step1"
    )

    allowed_actions = mission.get("allowed_actions")
    if allowed_actions is None:
        allowed_actions = [action_type]

    evaluated_at = execution_context.get("evaluated_at") or now_iso()

    return {
        "request_id": execution_context.get("request_id"),
        "mission_id": mission.get("mission_id"),
        "delegation_id": delegation.get("delegation_id"),
        "subject_id": subject.get("subject_id"),
        "credential_refs": delegation.get("credential_refs", []),
        "parent_request_id": delegation.get("parent_request_id"),
        "action_type": action_type,
        "allowed_actions": allowed_actions,
        "supervision_required": bool(mission.get("supervision_required", False)),
        "forbidden_conditions": mission.get("forbidden_conditions", []),
        "soga_constraints": mission.get("soga_constraints", {}),
        "subject_agency_state": subject.get("subject_agency_state", "ACTIVE"),
        "guest_present": bool(execution_context.get("guest_present", False)),
        "operator_present": bool(execution_context.get("operator_present", False)),
        "revoked": bool(delegation.get("revoked", False)),
        "expires_at": delegation.get("expires_at", "2026-12-31T12:00:00Z"),
        "evaluated_at": evaluated_at,
        "source": execution_context.get("source", "runtime_envelope"),
        "runtime_envelope": envelope,
    }