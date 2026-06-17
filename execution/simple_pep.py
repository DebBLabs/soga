from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from verify.decision_package import DecisionPackage, GovernanceOutcome
from verify.execution_status import ExecutionState, ExecutionStatus


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_execution_reference() -> str:
    return f"exec-{uuid4().hex[:12]}"


class SimplePEP:
    """
    Minimal Policy Enforcement Point.

    The PEP consumes a Decision Package and produces Execution Status.
    It does not re-evaluate governance, authority, mission, or subject state.
    """

    def enforce(self, decision_package: DecisionPackage) -> ExecutionStatus:
        if decision_package.decision == GovernanceOutcome.ALLOW:
            execution_state = ExecutionState.EXECUTING
            notes = "Execution permitted by Decision Package."

        elif decision_package.decision == GovernanceOutcome.RESTRICT:
            execution_state = ExecutionState.HOLDING
            notes = "Execution held or constrained by Decision Package."

        elif decision_package.decision == GovernanceOutcome.DENY:
            execution_state = ExecutionState.ABORTED
            notes = "Execution rejected by Decision Package."

        else:
            execution_state = ExecutionState.FAILED
            notes = "Unknown governance outcome."

        timestamp = now_iso()

        return ExecutionStatus(
            execution_status=execution_state,
            execution_reference=new_execution_reference(),
            request_id=decision_package.request_id,
            receipt_id=decision_package.receipt_id,
            execution_started_at=timestamp,
            execution_updated_at=timestamp,
            execution_notes=notes,
            metadata={
                "pep": "simple_pep",
                "decision": decision_package.decision.value,
                "directives": decision_package.directives,
                "constraints": decision_package.constraints,
            },
        )
