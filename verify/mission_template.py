from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class MissionLifecycle(str, Enum):
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


@dataclass(frozen=True)
class MissionTemplate:
    """
    Protocol-independent representation of delegated intent.

    This object records why delegated authority is being exercised.
    It does not represent authority itself, execution status, or enforcement behavior.
    """

    mission_id: str
    lifecycle: MissionLifecycle
    subject_id: str
    objective: str
    allowed_actions: List[str] = field(default_factory=list)
    forbidden_actions: List[str] = field(default_factory=list)
    bounds: Dict[str, Any] = field(default_factory=dict)
    references: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "lifecycle": self.lifecycle.value,
            "subject_id": self.subject_id,
            "objective": self.objective,
            "allowed_actions": self.allowed_actions,
            "forbidden_actions": self.forbidden_actions,
            "bounds": self.bounds,
            "references": self.references,
            "metadata": self.metadata,
        }
