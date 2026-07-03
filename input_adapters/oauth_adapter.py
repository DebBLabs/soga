from __future__ import annotations
import uuid
from typing import Any, Dict, List
from verify.mission_template import MissionLifecycle, MissionTemplate
from verify.runtime_envelope_model import (
    AuthorityEvidence,
    Reachability,
    RuntimeEnvelope,
    SubjectGovernanceState,
    SubjectState,
)
def generate_request_id() -> str:
    return f"req-oauth-{uuid.uuid4().hex[:12]}"
def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]
def _subject_state(value: str) -> SubjectGovernanceState:
    mapping = {
        "ACTIVE": SubjectGovernanceState.INDEPENDENT,
        "INDEPENDENT": SubjectGovernanceState.INDEPENDENT,
        "IMPAIRED": SubjectGovernanceState.SUPERVISED,
        "SUPERVISED": SubjectGovernanceState.SUPERVISED,
        "MANAGED": SubjectGovernanceState.MANAGED,
        "DELEGATED": SubjectGovernanceState.DELEGATED,
        "LAPSED": SubjectGovernanceState.LAPSED,
        "UNREACHABLE": SubjectGovernanceState.SUPERVISED,
    }
    return mapping.get(str(value).upper(), SubjectGovernanceState.INDEPENDENT)
def oauth_gnap_to_runtime_envelope_v0_1(
    payload: Dict[str, Any],
    governance_context: Dict[str, Any],
) -> RuntimeEnvelope:
    """
    Convert representative OAuth/GNAP-style authority data into the canonical
    SOGA RuntimeEnvelope.
    Adapter boundary:
    - passive data transformer only
    - static mocked payloads only
    - no live OAuth server
    - no live GNAP server
    - no socket connection
    - no token library
    - no a2a-gateway integration
    - no governance decision logic
    Appended governance context must be static configuration or deterministic
    lookup supplied at adapter initialization.
    """
    grant = payload.get("grant", payload)
    access_token = payload.get("access_token", {})
    authorization_details = grant.get("authorization_details", [])
    first_detail = (
        authorization_details[0]
        if authorization_details and isinstance(authorization_details[0], dict)
        else {}
    )
    actions = _as_list(
        first_detail.get("actions")
        or first_detail.get("allowed_actions")
        or access_token.get("scope")
        or payload.get("actions")
        or "step1"
    )
    action_type = (
        payload.get("action_type")
        or first_detail.get("action_type")
        or first_detail.get("action")
        or (actions[0] if actions else "step1")
    )
    subject_id = (
        governance_context.get("subject_id")
        or payload.get("subject_id")
        or access_token.get("sub")
        or grant.get("subject")
        or "subject-oauth-unknown"
    )
    subject_state_raw = governance_context.get("subject_agency_state", "ACTIVE")
    mission_constraints = governance_context.get("mission_constraints", {})
    mission_id = (
        first_detail.get("mission_id")
        or governance_context.get("mission_id")
        or payload.get("mission_id")
        or "mission-oauth-gnap-stub-001"
    )
    mission = MissionTemplate(
        mission_id=str(mission_id),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(subject_id),
        objective=str(
            first_detail.get("objective")
            or governance_context.get("objective")
            or "Representative OAuth/GNAP delegated mission"
        ),
        allowed_actions=actions or [str(action_type)],
        forbidden_actions=list(
            mission_constraints.get("forbidden_conditions", [])
        ),
        bounds=dict(mission_constraints),
        constraints={
            "global": dict(mission_constraints.get("global", {})),
            "stage_gate": list(mission_constraints.get("stage_gate", [])),
            "delegation": dict(mission_constraints.get("delegation", {})),
        },
        references={
            "client_id": grant.get("client_id") or payload.get("client_id"),
            "grant_id": grant.get("grant_id") or payload.get("grant_id"),
            "token_id": access_token.get("jti"),
            "resource": first_detail.get("resource"),
        },
        metadata={
            "source": payload.get("source", "oauth_adapter"),
            "adapter": "oauth_adapter",
            "source_protocol": payload.get("source_protocol", "oauth-gnap-style"),
            "stub": True,
        },
    )
    authority = AuthorityEvidence(
        authority_id=str(
            grant.get("grant_id")
            or access_token.get("jti")
            or payload.get("delegation_id")
            or mission_id
        ),
        authority_type="oauth-gnap-style",
        allowed_actions=actions or [str(action_type)],
        source_protocol="oauth-gnap-style",
        references={
            "client_id": grant.get("client_id") or payload.get("client_id"),
            "resource": first_detail.get("resource"),
            "scope": access_token.get("scope"),
            "issuer": access_token.get("iss"),
            "audience": access_token.get("aud"),
        },
        raw_evidence={
            "oauth_gnap_payload": payload,
        },
    )
    subject = SubjectState(
        subject_id=str(subject_id),
        governance_state=_subject_state(str(subject_state_raw)),
        reachability=Reachability.REACHABLE,
        context={
            "subject_agency_state_raw": subject_state_raw,
            "governance_context_source": governance_context.get(
                "source",
                "static_configuration",
            ),
        },
    )
    return RuntimeEnvelope(
        request_id=str(payload.get("request_id") or generate_request_id()),
        mission=mission,
        authority=authority,
        subject=subject,
        execution_context={
            "requested_action": str(action_type),
            "capability": governance_context.get("capability"),
            "evaluated_at": payload.get("evaluated_at"),
            "source": payload.get("source", "oauth_adapter"),
            "governance_reasoning_token": governance_context.get(
                "governance_reasoning_token"
            ),
        },
        policy={
            "profile": "soga-baseline-v0.1",
        },
        metadata={
            "adapter": "oauth_adapter",
            "source_protocol": "oauth-gnap-style",
            "stub": True,
        },
    )
