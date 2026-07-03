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
    return f"req-mcp-{uuid.uuid4().hex[:12]}"


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


def mcp_to_runtime_envelope_v0_1(
    payload: Dict[str, Any],
    governance_context: Dict[str, Any],
) -> RuntimeEnvelope:
    """
    Convert representative MCP-style capability invocation data into the
    canonical SOGA RuntimeEnvelope.

    Adapter boundary:
    - passive data transformer only
    - static mocked payloads only
    - no MCP transport
    - no MCP SDK
    - no socket connection
    - no tool execution
    - no governance decision logic

    Appended governance context must be static configuration or deterministic
    lookup supplied at adapter initialization.
    """

    tool_call = payload.get("tool_call", payload)

    capability = (
        tool_call.get("name")
        or tool_call.get("tool")
        or payload.get("capability")
        or governance_context.get("capability")
        or "step1"
    )

    actions = _as_list(
        governance_context.get("allowed_actions")
        or payload.get("allowed_actions")
        or capability
    )

    subject_id = (
        governance_context.get("subject_id")
        or payload.get("subject_id")
        or "subject-mcp-unknown"
    )

    subject_state_raw = governance_context.get("subject_agency_state", "ACTIVE")

    mission_constraints = governance_context.get("mission_constraints", {})

    mission_id = (
        governance_context.get("mission_id")
        or payload.get("mission_id")
        or "mission-mcp-stub-001"
    )

    mission = MissionTemplate(
        mission_id=str(mission_id),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(subject_id),
        objective=str(
            governance_context.get("objective")
            or f"Representative MCP capability request for {capability}"
        ),
        allowed_actions=actions or [str(capability)],
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
            "server": payload.get("server"),
            "tool": capability,
            "tool_call_id": tool_call.get("id"),
        },
        metadata={
            "source": payload.get("source", "mcp_adapter"),
            "adapter": "mcp_adapter",
            "source_protocol": "mcp-style",
            "stub": True,
        },
    )

    authority = AuthorityEvidence(
        authority_id=str(
            governance_context.get("authority_id")
            or payload.get("authority_id")
            or f"authority-mcp-{capability}"
        ),
        authority_type="mcp-style-capability",
        allowed_actions=actions or [str(capability)],
        source_protocol="mcp-style",
        references={
            "server": payload.get("server"),
            "tool": capability,
            "tool_call_id": tool_call.get("id"),
        },
        raw_evidence={
            "mcp_payload": payload,
            "governance_context": governance_context,
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
            "requested_action": str(capability),
            "capability": str(capability),
            "evaluated_at": payload.get("evaluated_at"),
            "source": payload.get("source", "mcp_adapter"),
            "governance_reasoning_token": governance_context.get(
                "governance_reasoning_token"
            ),
        },
        policy={
            "profile": "soga-baseline-v0.1",
        },
        metadata={
            "adapter": "mcp_adapter",
            "source_protocol": "mcp-style",
            "stub": True,
        },
    )
