from __future__ import annotations

import uuid
from typing import Any, Dict, List


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


def zcap_to_envelope(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a ZCAP-shaped capability artifact into the canonical SOGA
    Runtime Envelope.

    Adapter boundary:
    - Parses ZCAP-shaped input.
    - Preserves frozen evidence.
    - Does not verify cryptographic proofs.
    - Does not evaluate caveats.
    - Does not decide ALLOW / RESTRICT / DENY.
    """
    capability = payload.get("capability", payload)

    invocation_target = (
        capability.get("invocationTarget")
        or capability.get("invocation_target")
        or capability.get("resource")
        or payload.get("resource")
    )

    allowed_actions = (
        capability.get("allowedAction")
        or capability.get("allowedActions")
        or capability.get("actions")
        or payload.get("allowed_actions")
        or payload.get("actions")
        or []
    )

    actions = _as_list(allowed_actions)
    action_type = payload.get("action_type") or payload.get("action") or (actions[0] if actions else "step1")

    caveats = capability.get("caveat") or capability.get("caveats") or payload.get("caveats") or []

    subject_agency_state = payload.get("subject_agency_state", "ACTIVE")

    subject_id = (
        payload.get("subject_id")
        or payload.get("controller")
        or capability.get("controller")
        or capability.get("invoker")
    )

    delegation_id = (
        payload.get("delegation_id")
        or capability.get("id")
        or capability.get("@id")
    )

    expires_at = (
        payload.get("expires_at")
        or capability.get("expires")
        or capability.get("expirationDate")
        or "2026-12-31T12:00:00Z"
    )

    return {
        "mission": {
            "mission_id": payload.get("mission_id") or delegation_id,
            "action_type": action_type,
            "allowed_actions": actions or [action_type],
            "supervision_required": bool(payload.get("supervision_required", False)),
            "forbidden_conditions": payload.get("forbidden_conditions", []),
            "soga_constraints": {
                "capability_type": "zcap",
                "invocation_target": invocation_target,
                "caveats": caveats,
                "restrict_if_subject_agency_state": payload.get(
                    "restrict_if_subject_agency_state",
                    ["IMPAIRED", "HELD", "UNREACHABLE"],
                ),
                "supervision_required": bool(payload.get("supervision_required", False)),
            },
            "capability": capability,
        },
        "subject": {
            "subject_id": subject_id,
            "subject_agency_state": subject_agency_state,
        },
        "delegation": {
            "delegation_id": delegation_id,
            "credential_refs": _as_list(
                payload.get("credential_refs")
                or payload.get("proof_chain")
                or capability.get("parentCapability")
                or capability.get("parent_capability")
            ),
            "parent_request_id": payload.get("parent_request_id"),
            "revoked": bool(payload.get("revoked", False)),
            "expires_at": expires_at,
            "frozen_evidence": {
                "zcap": payload,
            },
        },
        "execution_context": {
            "request_id": payload.get("request_id") or generate_request_id(),
            "guest_present": bool(payload.get("guest_present", False)),
            "operator_present": bool(payload.get("operator_present", True)),
            "evaluated_at": payload.get("evaluated_at"),
            "source": payload.get("source", "zcap_adapter"),
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


def zcap_to_runtime_envelope_v0_1(payload: Dict[str, Any]) -> RuntimeEnvelope:
    """
    Convert a ZCAP-shaped capability artifact into the SOGA v0.1
    canonical RuntimeEnvelope model.

    This adapter preserves the ZCAP-shaped authority evidence and normalizes it
    for the protocol-independent Governance PDP.
    """

    capability = payload.get("capability", payload)

    invocation_target = (
        capability.get("invocationTarget")
        or capability.get("invocation_target")
        or capability.get("resource")
        or payload.get("resource")
    )

    allowed_actions = (
        capability.get("allowedAction")
        or capability.get("allowedActions")
        or capability.get("actions")
        or payload.get("allowed_actions")
        or payload.get("actions")
        or []
    )

    actions = _as_list(allowed_actions)
    action_type = payload.get("action_type") or payload.get("action") or (actions[0] if actions else "step1")

    subject_id = (
        payload.get("subject_id")
        or payload.get("controller")
        or capability.get("controller")
        or capability.get("invoker")
        or "subject-unknown"
    )

    delegation_id = (
        payload.get("delegation_id")
        or capability.get("id")
        or capability.get("@id")
        or "authority-zcap-unknown"
    )

    subject_state_raw = payload.get("subject_agency_state", "ACTIVE")

    caveats = capability.get("caveat") or capability.get("caveats") or payload.get("caveats") or []

    mission = MissionTemplate(
        mission_id=str(payload.get("mission_id") or delegation_id),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(subject_id),
        objective=str(
            payload.get("objective")
            or f"Invoke ZCAP target {invocation_target} for action {action_type}"
        ),
        allowed_actions=actions or [str(action_type)],
        forbidden_actions=list(payload.get("forbidden_conditions", [])),
        bounds={
            "capability_type": "zcap",
            "invocation_target": invocation_target,
            "caveats": caveats,
            "supervision_required": bool(payload.get("supervision_required", False)),
        },
        references={
            "capability_id": capability.get("id") or capability.get("@id"),
            "parent_capability": capability.get("parentCapability") or capability.get("parent_capability"),
            "invocation_target": invocation_target,
        },
        metadata={
            "source": payload.get("source", "zcap_adapter"),
            "capability_type": capability.get("type"),
        },
    )

    authority = AuthorityEvidence(
        authority_id=str(delegation_id),
        authority_type="zcap",
        allowed_actions=actions or [str(action_type)],
        source_protocol="zcap",
        references={
            "parent_capability": capability.get("parentCapability") or capability.get("parent_capability"),
            "invocation_target": invocation_target,
            "expiration": capability.get("expires") or capability.get("expirationDate"),
        },
        raw_evidence={
            "zcap": payload,
        },
    )

    subject = SubjectState(
        subject_id=str(subject_id),
        governance_state=_soga_subject_state(str(subject_state_raw)),
        reachability=Reachability.REACHABLE,
        context={
            "subject_agency_state_raw": subject_state_raw,
            "operator_present": payload.get("operator_present"),
            "guest_present": payload.get("guest_present"),
        },
    )

    return RuntimeEnvelope(
        request_id=str(payload.get("request_id") or generate_request_id()),
        mission=mission,
        authority=authority,
        subject=subject,
        execution_context={
            "requested_action": str(action_type),
            "source": payload.get("source", "zcap_adapter"),
        },
        policy={
            "profile": "soga-baseline-v0.1",
        },
        metadata={
            "adapter": "zcap_adapter",
            "source_protocol": "zcap",
        },
    )
