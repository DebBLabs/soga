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
    return f"req-aiim-{uuid.uuid4().hex[:12]}"


def _actions(value: Any) -> List[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _subject_state(value: str) -> SubjectGovernanceState:
    mapping = {
        "ACTIVE": SubjectGovernanceState.INDEPENDENT,
        "INDEPENDENT": SubjectGovernanceState.INDEPENDENT,
        "IMPAIRED": SubjectGovernanceState.SUPERVISED,
        "SUPERVISED": SubjectGovernanceState.SUPERVISED,
        "MANAGED": SubjectGovernanceState.MANAGED,
        "DELEGATED": SubjectGovernanceState.DELEGATED,
        "LAPSED": SubjectGovernanceState.LAPSED,
    }
    return mapping.get(str(value).upper(), SubjectGovernanceState.INDEPENDENT)


def aiim_to_runtime_envelope_v0_1(payload: Dict[str, Any]) -> RuntimeEnvelope:
    """
    Convert representative AIIM-shaped mission data into the canonical
    SOGA RuntimeEnvelope.

    Adapter boundary:
    - passive data transformer only
    - no AIIM schema implementation
    - no protocol coupling
    - no governance decision logic
    """

    mission_data = payload.get("aiim_mission", {})
    authority_data = mission_data.get("delegated_authority", {})
    constraints = mission_data.get("constraints", {})
    actions = _actions(mission_data.get("actions") or mission_data.get("allowed_actions"))

    action_type = (
        payload.get("action_type")
        or mission_data.get("action_type")
        or (actions[0] if actions else "step1")
    )

    subject_id = (
        payload.get("subject_id")
        or mission_data.get("subject_id")
        or authority_data.get("subject_id")
        or "subject-aiim-unknown"
    )

    subject_state_raw = (
        payload.get("subject_agency_state")
        or mission_data.get("subject_agency_state")
        or "SUPERVISED"
    )

    mission = MissionTemplate(
        mission_id=str(mission_data.get("mission_id", "mission-aiim-stub-001")),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(subject_id),
        objective=str(
            mission_data.get("objective")
            or "Representative AIIM mission"
        ),
        allowed_actions=actions or [str(action_type)],
        forbidden_actions=list(
            constraints.get("forbidden_conditions", [])
        ),
        bounds=dict(constraints),
        constraints={
            "global": dict(constraints.get("global", {})),
            "stage_gate": list(constraints.get("stage_gate", [])),
            "delegation": dict(constraints.get("delegation", {})),
        },
        references={
            "origin": "aiim-style-stub",
            "care_team_id": mission_data.get("care_team_id"),
            "workflow_id": mission_data.get("workflow_id"),
        },
        metadata={
            "source": payload.get("source", "aiim_adapter"),
            "adapter": "aiim_adapter",
            "stub": True,
        },
    )

    authority = AuthorityEvidence(
        authority_id=str(
            authority_data.get("authority_id")
            or authority_data.get("delegation_id")
            or mission_data.get("mission_id")
            or "authority-aiim-stub-001"
        ),
        authority_type="aiim-style",
        allowed_actions=actions or [str(action_type)],
        source_protocol="aiim-style-stub",
        references={
            "delegator": authority_data.get("delegator"),
            "delegate": authority_data.get("delegate"),
            "basis": authority_data.get("basis"),
        },
        raw_evidence={
            "aiim_mission": mission_data,
        },
    )

    subject = SubjectState(
        subject_id=str(subject_id),
        governance_state=_subject_state(str(subject_state_raw)),
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
            "capability": payload.get("capability"),
            "evaluated_at": payload.get("evaluated_at"),
            "source": payload.get("source", "aiim_adapter"),
        },
        policy={
            "profile": "soga-baseline-v0.1",
        },
        metadata={
            "adapter": "aiim_adapter",
            "source_protocol": "aiim-style-stub",
            "stub": True,
        },
    )
