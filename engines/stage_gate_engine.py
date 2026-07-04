from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


class StageGateState:
    EXECUTE_DIRECTLY = "EXECUTE_DIRECTLY"
    GOVERNANCE_REQUIRED = "GOVERNANCE_REQUIRED"
    RESTRICTED = "RESTRICTED"
    RESUBMIT_FOR_GOVERNANCE = "RESUBMIT_FOR_GOVERNANCE"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_interruption_instance_id() -> str:
    return f"sgi-{uuid4().hex[:12]}"


class StageGateEngine:
    """
    Evaluates stage gate declarations for mission execution steps.

    Stage Gates determine when governance must be invoked.

    They do not make governance decisions.
    They do not modify GovernancePDP behavior.
    They do not modify RuntimeEnvelope structure.
    """

    def evaluate_step(
        self,
        mission: Dict[str, Any],
        step_id: str,
        runtime_evidence: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        runtime_evidence = runtime_evidence or {}

        gate = self._find_gate_for_step(
            mission,
            step_id,
        )

        if gate is None:
            return {
                "state": StageGateState.EXECUTE_DIRECTLY,
                "step_id": step_id,
                "gate": None,
                "reason": "No stage gate declared for this mission step.",
            }

        if self._has_clearance(
            gate,
            runtime_evidence,
        ):
            return {
                "state": StageGateState.RESUBMIT_FOR_GOVERNANCE,
                "step_id": step_id,
                "gate": gate,
                "reason": "Clearance evidence present; resubmit through governance.",
                "clearance_evidence": runtime_evidence.get("clearance_evidence"),
            }

        if runtime_evidence.get("governance_decision") == "RESTRICT":
            return {
                "state": StageGateState.RESTRICTED,
                "step_id": step_id,
                "gate": gate,
                "reason": "Governance returned RESTRICT for this stage gate.",
                "interruption_record": self._build_interruption_record(
                    mission,
                    step_id,
                    gate,
                    runtime_evidence,
                ),
            }

        return {
            "state": StageGateState.GOVERNANCE_REQUIRED,
            "step_id": step_id,
            "gate": gate,
            "reason": "Stage gate declared; governance evaluation required.",
        }

    def _find_gate_for_step(
        self,
        mission: Dict[str, Any],
        step_id: str,
    ) -> Optional[Dict[str, Any]]:
        constraints = mission.get("constraints", {}) or {}
        stage_gates: List[Dict[str, Any]] = constraints.get("stage_gate", []) or []

        for gate in stage_gates:
            if not isinstance(gate, dict):
                continue

            gate_step = (
                gate.get("step_id")
                or gate.get("applies_to")
                or gate.get("mission_step")
            )

            if gate_step == step_id:
                return gate

        return None

    def _has_clearance(
        self,
        gate: Dict[str, Any],
        runtime_evidence: Dict[str, Any],
    ) -> bool:
        clearance_evidence = runtime_evidence.get("clearance_evidence")

        if not isinstance(clearance_evidence, dict):
            return False

        required_evidence = gate.get("required_evidence")

        if required_evidence is None:
            return bool(clearance_evidence.get("satisfied"))

        return clearance_evidence.get("type") == required_evidence

    def _build_interruption_record(
        self,
        mission: Dict[str, Any],
        step_id: str,
        gate: Dict[str, Any],
        runtime_evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Execution Interruption Record — Sprint C in-memory only.
        # Durable implementation belongs in Sprint E (Mission Execution Engine).

        return {
            "interruption_instance_id": new_interruption_instance_id(),
            "created_at": now_iso(),
            "mission_id": mission.get("mission_id"),
            "step_id": step_id,
            "gate_id": gate.get("gate_id"),
            "gate_name": gate.get("name"),
            "pending_reason": gate.get("governance_reasoning_token"),
            "restrict_path": gate.get("restrict_path", "HOLDING"),
            "clearance_state": "PENDING",
            "triggering_cdp_reference": runtime_evidence.get("cdp_reference"),
        }
