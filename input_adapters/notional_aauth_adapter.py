from __future__ import annotations

from typing import Any, Dict

from verify.mission_template import MissionLifecycle, MissionTemplate
from verify.runtime_envelope_model import (
    AuthorityEvidence,
    Reachability,
    RuntimeEnvelope,
    SubjectGovernanceState,
    SubjectState,
)


def _mission_lifecycle(value: str) -> MissionLifecycle:
    try:
        return MissionLifecycle(value.upper())
    except ValueError:
        return MissionLifecycle.ACTIVE


def _subject_governance_state(value: str) -> SubjectGovernanceState:
    try:
        return SubjectGovernanceState(value.upper())
    except ValueError:
        return SubjectGovernanceState.INDEPENDENT


def _reachability(value: str) -> Reachability:
    try:
        return Reachability(value.upper())
    except ValueError:
        return Reachability.UNKNOWN


def from_notional_aauth(payload: Dict[str, Any]) -> RuntimeEnvelope:
    """
    Convert an AAuth-shaped payload into a SOGA Runtime Envelope.

    This adapter is intentionally not a full AAuth implementation.
    It demonstrates the adapter boundary:

        AAuth-shaped input -> RuntimeEnvelope

    The Governance PDP does not need to know that the input came from AAuth.
    """

    mission_block = payload.get("mission", {})
    authority_block = payload.get("authority", {})
    subject_block = payload.get("subject", {})
    request_block = payload.get("request", {})

    subject_id = str(
        subject_block.get("subject_id")
        or payload.get("subject_id")
        or mission_block.get("subject_id")
        or "subject-unknown"
    )

    mission = MissionTemplate(
        mission_id=str(mission_block.get("mission_id", "mission-aauth-notional-001")),
        lifecycle=_mission_lifecycle(str(mission_block.get("lifecycle", "ACTIVE"))),
        subject_id=subject_id,
        objective=str(
            mission_block.get(
                "objective",
                mission_block.get("description", "Notional AAuth delegated mission."),
            )
        ),
        allowed_actions=list(
            mission_block.get(
                "allowed_actions",
                authority_block.get("allowed_actions", []),
            )
        ),
        forbidden_actions=list(mission_block.get("forbidden_actions", [])),
        bounds=dict(mission_block.get("bounds", {})),
        references=dict(mission_block.get("references", {})),
        metadata={
            "source": "notional_aauth_adapter",
            "aauth_mission_description": mission_block.get("description"),
        },
    )

    authority = AuthorityEvidence(
        authority_id=str(authority_block.get("authority_id", "authority-aauth-notional-001")),
        authority_type=str(authority_block.get("authority_type", "aauth")),
        allowed_actions=list(authority_block.get("allowed_actions", mission.allowed_actions)),
        source_protocol="aauth",
        references=dict(authority_block.get("references", {})),
        raw_evidence=dict(authority_block.get("raw_evidence", {})),
    )

    subject = SubjectState(
        subject_id=subject_id,
        governance_state=_subject_governance_state(
            str(subject_block.get("governance_state", "INDEPENDENT"))
        ),
        reachability=_reachability(str(subject_block.get("reachability", "UNKNOWN"))),
        context=dict(subject_block.get("context", {})),
    )

    return RuntimeEnvelope(
        request_id=str(request_block.get("request_id", payload.get("request_id", "req-aauth-notional"))),
        mission=mission,
        authority=authority,
        subject=subject,
        execution_context={
            "requested_action": request_block.get("requested_action"),
            **dict(payload.get("execution_context", {})),
        },
        policy=dict(payload.get("policy", {"profile": "soga-baseline-v0.1"})),
        metadata={
            "adapter": "notional_aauth_adapter",
            "source_protocol": "aauth",
        },
    )
