from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class AgentEvidence:
    """
    Advisory agent evidence.

    Evidence only. Not a governance determination.
    """

    agent_id: str
    evidence_type: str
    evidence_content: Dict[str, Any]
    provenance: Dict[str, Any]
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "evidence_type": self.evidence_type,
            "evidence_content": self.evidence_content,
            "provenance": self.provenance,
            "confidence": self.confidence,
        }
