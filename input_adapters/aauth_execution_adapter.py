from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from verify.mission_template import MissionLifecycle, MissionTemplate
from verify.runtime_envelope_model import (
    AuthorityEvidence,
    Reachability,
    RuntimeEnvelope,
    SubjectGovernanceState,
    SubjectState,
)


def _new_request_id() -> str:
    return f"req-aauth-exec-{uuid.uuid4().hex[:12]}"


def _string(value: Any, default: str) -> str:
    if value is None:
        return default
    return str(value)


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if isinstance(value, set):
        return [str(item) for item in value]
    return [str(value)]


def _subject_governance_state(value: Any) -> SubjectGovernanceState:
    normalized = str(value or "INDEPENDENT").upper()

    mapping = {
        "ACTIVE": SubjectGovernanceState.INDEPENDENT,
        "INDEPENDENT": SubjectGovernanceState.INDEPENDENT,
        "IMPAIRED": SubjectGovernanceState.SUPERVISED,
        "SUPERVISED": SubjectGovernanceState.SUPERVISED,
        "HELD": SubjectGovernanceState.MANAGED,
        "MANAGED": SubjectGovernanceState.MANAGED,
        "DELEGATED": SubjectGovernanceState.DELEGATED,
        "LAPSED": SubjectGovernanceState.LAPSED,
        # UNREACHABLE is primarily a reachability signal, not a
        # governance state. Mapping it to SUPERVISED here preserves
        # conservative behavior for legacy payloads that place
        # reachability in the wrong field. The canonical reachability
        # axis remains separate in _reachability().
        "UNREACHABLE": SubjectGovernanceState.SUPERVISED,
    }

    return mapping.get(normalized, SubjectGovernanceState.INDEPENDENT)


def _reachability(value: Any) -> Reachability:
    normalized = str(value or "UNKNOWN").upper()

    mapping = {
        "REACHABLE": Reachability.REACHABLE,
        "UNREACHABLE": Reachability.UNREACHABLE,
        "UNKNOWN": Reachability.UNKNOWN,
    }

    return mapping.get(normalized, Reachability.UNKNOWN)


class AAuthExecutionAdapter:
    """
    Translate an AAuth-shaped execution request into SOGA canonical
    runtime inputs.

    This adapter is protocol projection.

    It receives AAuth-shaped evidence and execution context.
    It produces a protocol-independent RuntimeEnvelope.

    It does not:
    - evaluate governance
    - decide ALLOW / RESTRICT / DENY
    - call the Runtime Governance Engine
    - produce a Canonical Decision Package

    AAuth remains evidence.
    SOGA remains the governance evaluator.
    """

    source_protocol = "aauth"

    def to_runtime_envelope(
        self,
        execution_request: Dict[str, Any],
    ) -> RuntimeEnvelope:

        mission_block = dict(execution_request.get("mission", {}))
        authority_block = dict(execution_request.get("authority", {}))
        subject_block = dict(execution_request.get("subject", {}))
        runtime_block = dict(execution_request.get("runtime", {}))

        request_id = _string(
            execution_request.get("request_id")
            or runtime_block.get("request_id"),
            _new_request_id(),
        )

        user_id = _string(
            execution_request.get("user_id")
            or subject_block.get("subject_id")
            or mission_block.get("subject_id"),
            "guest",
        )

        message = _string(
            execution_request.get("message")
            or mission_block.get("objective")
            or mission_block.get("description"),
            "AAuth delegated execution request",
        )

        requested_action = _string(
            execution_request.get("action")
            or execution_request.get("requested_action")
            or runtime_block.get("requested_action")
            or mission_block.get("action")
            or mission_block.get("action_type"),
            "supply_chain_optimization",
        )

        allowed_actions = _as_list(
            authority_block.get("allowed_actions")
            or mission_block.get("allowed_actions")
            or execution_request.get("allowed_actions")
            or requested_action
        )

        mission = MissionTemplate(
            mission_id=_string(
                mission_block.get("mission_id")
                or execution_request.get("mission_id"),
                "mission-aauth-execution",
            ),
            lifecycle=MissionLifecycle.ACTIVE,
            subject_id=user_id,
            objective=message,
            allowed_actions=allowed_actions,
            forbidden_actions=_as_list(
                mission_block.get("forbidden_actions")
                or execution_request.get("forbidden_actions")
            ),
            bounds=dict(
                mission_block.get("bounds")
                or execution_request.get("constraints")
                or {}
            ),
            references={
                "agent_url": execution_request.get("agent_url"),
                "source": "aauth_execution_adapter",
                **dict(mission_block.get("references", {})),
            },
            metadata={
                "adapter": "aauth_execution_adapter",
                "source_protocol": self.source_protocol,
            },
        )

        authority = AuthorityEvidence(
            authority_id=_string(
                authority_block.get("authority_id")
                or execution_request.get("delegation_id")
                or execution_request.get("token_id"),
                "authority-aauth-execution",
            ),
            authority_type=_string(
                authority_block.get("authority_type"),
                "aauth",
            ),
            allowed_actions=allowed_actions,
            source_protocol=self.source_protocol,
            references=dict(authority_block.get("references", {})),
            raw_evidence={
                "aauth_execution_request": execution_request,
                "authority": authority_block,
            },
        )

        subject = SubjectState(
            subject_id=user_id,
            governance_state=_subject_governance_state(
                subject_block.get("governance_state")
                or subject_block.get("subject_agency_state")
                or execution_request.get("subject_agency_state")
                or runtime_block.get("subject_agency_state")
            ),
            reachability=_reachability(
                subject_block.get("reachability")
                or execution_request.get("reachability")
                or runtime_block.get("reachability")
            ),
            context={
                "user_id": user_id,
                **dict(subject_block.get("context", {})),
            },
        )

        return RuntimeEnvelope(
            request_id=request_id,
            mission=mission,
            authority=authority,
            subject=subject,
            execution_context={
                "requested_action": requested_action,
                "agent_url": execution_request.get("agent_url"),
                "message": message,
                "source": "aauth_execution_boundary",
                **dict(execution_request.get("execution_context", {})),
            },
            policy=dict(
                execution_request.get("policy")
                or {
                    "profile": "soga-baseline-v0.1",
                }
            ),
            metadata={
                "adapter": "aauth_execution_adapter",
                "source_protocol": self.source_protocol,
            },
        )


def adapt_aauth_execution_request(
    execution_request: Dict[str, Any],
) -> RuntimeEnvelope:
    """
    Convenience function for callers that do not need to instantiate
    the adapter class directly.
    """
    return AAuthExecutionAdapter().to_runtime_envelope(
        execution_request
    )


def adapt_aauth_execution_request_to_dict(
    execution_request: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Return canonical runtime inputs as a dictionary for logging,
    tests, and integration boundaries that are not dataclass-aware.
    """
    return adapt_aauth_execution_request(
        execution_request
    ).to_dict()
