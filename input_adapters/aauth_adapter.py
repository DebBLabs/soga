from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


MISSION_STATEMENT_TYPES = {
    "aauth_mission_statement",
    "soga_mission_statement",
}


def generate_request_id() -> str:
    return f"req-{uuid.uuid4().hex[:12]}"


def first_mission_statement(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Extract the first AAuth/SOGA Mission Statement from an OAuth/RAR-style
    authorization_details array.

    This adapter treats the incoming object as frozen evidence. It does not
    evaluate authority, apply policy, or make runtime decisions.
    """
    authorization_details = payload.get("authorization_details", [])

    if not isinstance(authorization_details, list):
        return None

    for item in authorization_details:
        if not isinstance(item, dict):
            continue

        if item.get("type") in MISSION_STATEMENT_TYPES:
            return item

    return None


def actions_from_mission_statement(mission_statement: Dict[str, Any]) -> List[str]:
    actions = mission_statement.get("actions") or mission_statement.get("allowed_actions") or []

    if isinstance(actions, str):
        return [actions]

    if isinstance(actions, list):
        return [str(action) for action in actions]

    return []


def mission_statement_to_envelope(
    payload: Dict[str, Any],
    mission_statement: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an AAuth/RAR-style Mission Statement into the canonical SOGA
    Runtime Envelope.

    Adapter boundary:
    - Parses protocol-shaped input.
    - Preserves frozen evidence.
    - Does not evaluate.
    - Does not decide ALLOW / RESTRICT / DENY.
    """
    soga_constraints = mission_statement.get("soga_constraints", {}) or {}

    actions = actions_from_mission_statement(mission_statement)
    action_type = (
        payload.get("action_type")
        or mission_statement.get("action_type")
        or mission_statement.get("action")
        or (actions[0] if actions else "step1")
    )

    subject_agency_state = (
        payload.get("subject_agency_state")
        or soga_constraints.get("subject_agency_state")
        or "ACTIVE"
    )

    subject_id = (
        payload.get("subject_id")
        or mission_statement.get("subject_id")
        or mission_statement.get("principal_id")
    )

    delegation_id = (
        payload.get("delegation_id")
        or mission_statement.get("delegation_id")
        or mission_statement.get("mission_id")
    )

    return {
        "mission": {
            "mission_id": mission_statement.get("mission_id"),
            "action_type": action_type,
            "allowed_actions": actions or [action_type],
            "supervision_required": bool(
                soga_constraints.get(
                    "supervision_required",
                    mission_statement.get("supervision_required", False),
                )
            ),
            "forbidden_conditions": soga_constraints.get(
                "forbidden_conditions",
                mission_statement.get("forbidden_conditions", []),
            ),
            "soga_constraints": soga_constraints,
            "mission_statement": mission_statement,
        },
        "subject": {
            "subject_id": subject_id,
            "subject_agency_state": subject_agency_state,
        },
        "delegation": {
            "delegation_id": delegation_id,
            "credential_refs": payload.get("credential_refs", []),
            "parent_request_id": payload.get("parent_request_id"),
            "revoked": bool(payload.get("revoked", mission_statement.get("revoked", False))),
            "expires_at": payload.get(
                "expires_at",
                mission_statement.get("expires_at", "2026-12-31T12:00:00Z"),
            ),
            "frozen_evidence": {
                "authorization_details": payload.get("authorization_details", []),
            },
        },
        "execution_context": {
            "request_id": payload.get("request_id") or generate_request_id(),
            "guest_present": bool(payload.get("guest_present", False)),
            "operator_present": bool(payload.get("operator_present", False)),
            "evaluated_at": payload.get("evaluated_at"),
            "source": payload.get("source", "aauth_mission_statement"),
        },
    }


# --- SOGA v0.1 canonical model adapter ------------------------------------

from verify.mission_template import MissionLifecycle, MissionTemplate
from verify.runtime_envelope_model import (
    AuthorityEvidence,
    Reachability,
    RuntimeEnvelope,
    SubjectGovernanceState,
    SubjectState,
)


def _soga_subject_state(value: str) -> SubjectGovernanceState:
    mapping = {
        "ACTIVE": SubjectGovernanceState.INDEPENDENT,
        "INDEPENDENT": SubjectGovernanceState.INDEPENDENT,
        "IMPAIRED": SubjectGovernanceState.SUPERVISED,
        "SUPERVISED": SubjectGovernanceState.SUPERVISED,
        "HELD": SubjectGovernanceState.MANAGED,
        "MANAGED": SubjectGovernanceState.MANAGED,
        "DELEGATED": SubjectGovernanceState.DELEGATED,
        "UNREACHABLE": SubjectGovernanceState.SUPERVISED,
        "LAPSED": SubjectGovernanceState.LAPSED,
    }
    return mapping.get(str(value).upper(), SubjectGovernanceState.INDEPENDENT)


def mission_statement_to_runtime_envelope_v0_1(
    payload: Dict[str, Any],
    mission_statement: Dict[str, Any],
) -> RuntimeEnvelope:
    """
    Convert an AAuth/RAR-style Mission Statement into the SOGA v0.1
    canonical RuntimeEnvelope model.

    This is the real bridge from older AAuth-shaped evidence into the
    new protocol-independent Governance PDP.
    """

    actions = actions_from_mission_statement(mission_statement)
    action_type = (
        payload.get("action_type")
        or mission_statement.get("action_type")
        or mission_statement.get("action")
        or (actions[0] if actions else "step1")
    )

    subject_id = (
        payload.get("subject_id")
        or mission_statement.get("subject_id")
        or mission_statement.get("principal_id")
        or "subject-unknown"
    )

    subject_state_raw = (
        payload.get("subject_agency_state")
        or mission_statement.get("subject_agency_state")
        or mission_statement.get("soga_constraints", {}).get("subject_agency_state")
        or "ACTIVE"
    )

    mission = MissionTemplate(
        mission_id=str(mission_statement.get("mission_id", "mission-aauth-unknown")),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(subject_id),
        objective=str(
            mission_statement.get("objective")
            or mission_statement.get("description")
            or "AAuth mission statement"
        ),
        allowed_actions=actions or [str(action_type)],
        forbidden_actions=list(
            mission_statement.get("soga_constraints", {}).get(
                "forbidden_conditions",
                mission_statement.get("forbidden_conditions", []),
            )
        ),
        bounds=dict(mission_statement.get("soga_constraints", {})),
        references={
            "delegation_id": mission_statement.get("delegation_id"),
            "resource_id": mission_statement.get("resource_id"),
            "resource_ref": mission_statement.get("resource_ref"),
            "agent_id": mission_statement.get("agent_id"),
            "person_server_id": mission_statement.get("person_server_id"),
            "r3_refs": mission_statement.get("r3_refs"),
        },
        metadata={
            "source": payload.get("source", "aauth_adapter"),
            "mission_statement_type": mission_statement.get("type"),
        },
    )

    authority = AuthorityEvidence(
        authority_id=str(
            payload.get("delegation_id")
            or mission_statement.get("delegation_id")
            or mission_statement.get("mission_id")
            or "authority-aauth-unknown"
        ),
        authority_type="aauth",
        allowed_actions=actions or [str(action_type)],
        source_protocol="aauth",
        references={
            "credential_refs": payload.get("credential_refs", []),
            "r3_granted": mission_statement.get("r3_granted"),
            "r3_conditional": mission_statement.get("r3_conditional"),
        },
        raw_evidence={
            "authorization_details": payload.get("authorization_details", []),
        },
    )

    subject = SubjectState(
        subject_id=str(subject_id),
        governance_state=_soga_subject_state(str(subject_state_raw)),
        reachability=Reachability.REACHABLE,
        context={
            "subject_agency_state_raw": subject_state_raw,
            "guest_present": payload.get("guest_present"),
            "operator_present": payload.get("operator_present"),
        },
    )

    return RuntimeEnvelope(
        request_id=str(payload.get("request_id") or generate_request_id()),
        mission=mission,
        authority=authority,
        subject=subject,
        execution_context={
            "requested_action": str(action_type),
            "evaluated_at": payload.get("evaluated_at"),
            "source": payload.get("source", "aauth_adapter"),
        },
        policy={
            "profile": "soga-baseline-v0.1",
        },
        metadata={
            "adapter": "aauth_adapter",
            "source_protocol": "aauth",
        },
    )
