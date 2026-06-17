from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ExecutionState(str, Enum):
    PENDING = "PENDING"
    HOLDING = "HOLDING"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    ESCALATED = "ESCALATED"
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ExecutionStatus:
    """
    Operational representation of execution after a Decision Package is consumed.

    This object records what execution is doing.
    It does not represent governance evaluation or delegated authority.
    """

    execution_status: ExecutionState
    execution_reference: str
    request_id: Optional[str] = None
    receipt_id: Optional[str] = None
    execution_started_at: Optional[str] = None
    execution_updated_at: Optional[str] = None
    execution_notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_status": self.execution_status.value,
            "execution_reference": self.execution_reference,
            "request_id": self.request_id,
            "receipt_id": self.receipt_id,
            "execution_started_at": self.execution_started_at,
            "execution_updated_at": self.execution_updated_at,
            "execution_notes": self.execution_notes,
            "metadata": self.metadata,
        }
