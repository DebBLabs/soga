from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class GovernanceOutcome(str, Enum):
    ALLOW = "ALLOW"
    RESTRICT = "RESTRICT"
    DENY = "DENY"


@dataclass(frozen=True)
class DecisionPackage:
    """
    Protocol-independent governance output produced by the SOGA Governance PDP.

    This object records what governance decided.
    It does not represent execution status or enforcement behavior.
    """

    request_id: str
    receipt_id: str
    decision: GovernanceOutcome
    reason_class: str
    rule: str
    explanation: str
    constraints: Dict[str, Any] = field(default_factory=dict)
    directives: List[str] = field(default_factory=list)
    runtime_references: Dict[str, Any] = field(default_factory=dict)
    audit_references: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "receipt_id": self.receipt_id,
            "decision": self.decision.value,
            "reason_class": self.reason_class,
            "rule": self.rule,
            "explanation": self.explanation,
            "constraints": self.constraints,
            "directives": self.directives,
            "runtime_references": self.runtime_references,
            "audit_references": self.audit_references,
        }
