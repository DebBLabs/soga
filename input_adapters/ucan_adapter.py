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
    return f"req-{uuid.uuid4().hex[:12]}"


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


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


def ucan_to_runtime_envelope_v0_1(payload: Dict[str, Any]) -> RuntimeEnvelope:
    """
    Convert a UCAN-shaped capability token payload into the SOGA v0.1
    canonical RuntimeEnvelope model.

    This adapter does not verify UCAN signatures.
    It normalizes UCAN-shaped authority evidence for the unchanged Governance PDP.
    """

    ucan = payload.get("ucan", payload)

    facts = ucan.get("fct") or ucan.get("facts") or payload.get("facts") or {}
    attenuations = ucan.get("att") or ucan.get("attenuations") or payload.get("attenuations") or []

    first_att = attenuations[0] if attenuations and isinstance(attenuations[0], dict) else {}

    resource = (
        first_att.get("with")
        or first_att.get("resource")
        or payload.get("resource")
        or "resource://demo/step1"
    )

    actions = _as_list(
        first_att.get("can")
        or first_att.get("actions")
        or payload.get("actions")
        or payload.get("allowed_actions")
        or "step1"
    )

    action_type = payload.get("action_type") or payload.get("action") or (actions[0] if actions else "step1")

    subject_id = (
        payload.get("subject_id")
        or facts.get("subject_id")
        or ucan.get("iss")
        or ucan.get("issuer")
        or "subject-unknown"
    )

    subject_state_raw = (
        payload.get("subject_agency_state")
        or facts.get("subject_agency_state")
        or "ACTIVE"
    )

    mission_id = (
        payload.get("mission_id")
        or facts.get("mission_id")
        or ucan.get("jti")
        or "mission-ucan-soga-001"
    )

    authority_id = (
        payload.get("delegation_id")
        or ucan.get("jti")
        or ucan.get("cid")
        or mission_id
    )

    mission = MissionTemplate(
        mission_id=str(mission_id),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(subject_id),
        objective=str(
            facts.get("objective")
            or payload.get("objective")
            or f"Invoke UCAN resource {resource} for action {action_type}"
        ),
        allowed_actions=actions or [str(action_type)],
        forbidden_actions=[],
        bounds={
            "capability_type": "ucan",
            "resource": resource,
            "attenuations": attenuations,
        },
        references={
            "ucan_id": ucan.get("jti") or ucan.get("cid"),
            "issuer": ucan.get("iss") or ucan.get("issuer"),
            "audience": ucan.get("aud") or ucan.get("audience"),
            "resource": resource,
        },
        metadata={
            "source": payload.get("source", "ucan_adapter"),
        },
    )

    authority = AuthorityEvidence(
        authority_id=str(authority_id),
        authority_type="ucan",
        allowed_actions=actions or [str(action_type)],
        source_protocol="ucan",
        references={
            "issuer": ucan.get("iss") or ucan.get("issuer"),
            "audience": ucan.get("aud") or ucan.get("audience"),
            "resource": resource,
            "expiration": ucan.get("exp") or payload.get("expires_at"),
        },
        raw_evidence={
            "ucan": payload,
        },
    )

    subject = SubjectState(
        subject_id=str(subject_id),
        governance_state=_soga_subject_state(str(subject_state_raw)),
        reachability=Reachability.REACHABLE,
        context={
            "subject_agency_state_raw": subject_state_raw,
        },
    )

    return RuntimeEnvelope(
        request_id=str(payload.get("request_id") or generate_request_id()),
        mission=mission,
        authority=authority,
        subject=subject,
        execution_context={
            "requested_action": str(action_type),
            "source": payload.get("source", "ucan_adapter"),
        },
        policy={
            "profile": "soga-baseline-v0.1",
        },
        metadata={
            "adapter": "ucan_adapter",
            "source_protocol": "ucan",
        },
    )
