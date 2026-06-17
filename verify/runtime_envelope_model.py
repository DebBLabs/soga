from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict

from verify.mission_template import MissionTemplate


class SubjectGovernanceState(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    SUPERVISED = "SUPERVISED"
    MANAGED = "MANAGED"
    DELEGATED = "DELEGATED"
    LAPSED = "LAPSED"


class Reachability(str, Enum):
    REACHABLE = "REACHABLE"
    UNREACHABLE = "UNREACHABLE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class AuthorityEvidence:
    """
    Normalized authority evidence carried into the Runtime Envelope.

    This object records what authority is available.
    It does not determine whether execution remains legitimate.
    """

    authority_id: str
    authority_type: str
    allowed_actions: list[str] = field(default_factory=list)
    source_protocol: str = "unknown"
    references: Dict[str, Any] = field(default_factory=dict)
    raw_evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authority_id": self.authority_id,
            "authority_type": self.authority_type,
            "allowed_actions": self.allowed_actions,
            "source_protocol": self.source_protocol,
            "references": self.references,
            "raw_evidence": self.raw_evidence,
        }


@dataclass(frozen=True)
class SubjectState:
    """
    Subject governance and reachability state evaluated at T-execution.
    """

    subject_id: str
    governance_state: SubjectGovernanceState
    reachability: Reachability
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "governance_state": self.governance_state.value,
            "reachability": self.reachability.value,
            "context": self.context,
        }


@dataclass(frozen=True)
class RuntimeEnvelope:
    """
    Protocol-independent governance input evaluated by the SOGA Governance PDP.

    The Runtime Envelope composes Mission, Authority, Subject Governance State,
    Reachability, Execution Context, and Policy.
    """

    request_id: str
    mission: MissionTemplate
    authority: AuthorityEvidence
    subject: SubjectState
    execution_context: Dict[str, Any] = field(default_factory=dict)
    policy: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "mission": self.mission.to_dict(),
            "authority": self.authority.to_dict(),
            "subject": self.subject.to_dict(),
            "execution_context": self.execution_context,
            "policy": self.policy,
            "metadata": self.metadata,
        }
