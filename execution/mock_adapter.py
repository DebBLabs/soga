from __future__ import annotations

from typing import Any, Dict, List


def _base_receipt(decision_package: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "request_id": decision_package.get("request_id"),
        "receipt_id": decision_package.get("receipt_id"),
        "decision": decision_package.get("decision"),
        "rule": decision_package.get("rule"),
        "adapter": "mock_adapter",
        "runtime_log": [],
    }


def execute_command(decision_package: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a simulated hardware outcome based only on the finalized
    Verify decision package.

    Boundary rule:
    - The adapter does not receive the Runtime Envelope.
    - The adapter does not receive the Mission Statement.
    - The adapter does not receive subject state or governance context.
    - The adapter does not re-evaluate.
    """
    decision = str(decision_package.get("decision", "DENY")).upper()
    execution_mode = decision_package.get("execution_mode", {}) or {}

    action = execution_mode.get("action", "hold")
    receipt = _base_receipt(decision_package)
    runtime_log: List[str] = receipt["runtime_log"]

    if decision == "ALLOW":
        runtime_log.append(f"MOCK_HW: Action '{action}' executed at full authority.")
        receipt.update(
            {
                "status": "EXECUTED_FULL",
                "hardware_action_executed": action,
                "bounded": False,
            }
        )
        return receipt

    if decision == "RESTRICT":
        buffer_action = execution_mode.get("buffer_action", "HOLD")
        runtime_log.append(f"MOCK_HW: Action '{action}' did not proceed at full authority.")
        runtime_log.append(f"MOCK_HW: Restriction applied by decision package: {buffer_action}.")
        receipt.update(
            {
                "status": "EXECUTED_WITH_CONSTRAINTS",
                "hardware_action_executed": buffer_action,
                "bounded": True,
            }
        )
        return receipt

    runtime_log.append("MOCK_HW: Execution aborted. Standby mode active.")
    receipt.update(
        {
            "status": "ABORTED",
            "hardware_action_executed": None,
            "bounded": False,
        }
    )
    return receipt
