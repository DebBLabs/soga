from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests
from flask import Flask, jsonify, request

from execution.mock_adapter import execute_command
from verify.gateway_router import build_gate_and_logger

app = Flask(__name__)

gate, logger = build_gate_and_logger()

MISTY = os.environ.get("MISTY", "http://192.168.10.214/api")

STATE_FILE = "/app/authority_state.json"


def get_authority_state() -> str:
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("state", "GuestsRestricted")
    except Exception:
        return "GuestsRestricted"


def set_authority_state(state: str) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump({"state": state}, f)


def safe_misty_led(red: int, green: int, blue: int) -> None:
    try:
        requests.post(
            f"{MISTY}/led",
            json={"red": red, "green": green, "blue": blue},
            timeout=2,
        )
    except Exception:
        pass


def effective_input_from_decision(payload: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use the normalized/flattened runtime input produced by PolicyGate when available.

    This avoids mismatches when callers submit a canonical envelope instead of
    the legacy flat payload shape.
    """
    return decision.get("input") or payload


def build_runtime_summary(
    payload: Dict[str, Any],
    decision: Dict[str, Any],
    authority_state: str,
    runtime_status: str,
    execution_mode: str,
) -> Dict[str, Any]:
    decision_body = decision.get("decision", {})
    runtime_refs = decision.get("runtime_refs", {})
    effective_input = effective_input_from_decision(payload, decision)

    return {
        "request_id": runtime_refs.get("request_id"),
        "subject_id": runtime_refs.get("subject_id"),
        "subject_agency_state": effective_input.get("subject_agency_state"),
        "authority_state": authority_state,
        "decision": decision_body.get("status"),
        "execution": execution_mode,
        "runtime_status": runtime_status,
        "rule": decision_body.get("rule"),
        "reason": decision_body.get("reason"),
    }


def emit_runtime_receipt(
    payload: Dict[str, Any],
    decision: Dict[str, Any],
    authority_state: str,
    runtime_status: str,
    execution_mode: str,
    outcome_reason: str,
) -> Dict[str, Any]:
    decision_body = decision.get("decision", {})
    runtime_refs = decision.get("runtime_refs", {})
    effective_input = effective_input_from_decision(payload, decision)

    runtime_summary = build_runtime_summary(
        payload=payload,
        decision=decision,
        authority_state=authority_state,
        runtime_status=runtime_status,
        execution_mode=execution_mode,
    )

    logger(
        {
            "component": "verify",
            "action": "execute",
            "request_id": runtime_refs.get("request_id"),
            "runtime_refs": runtime_refs,
            "runtime_summary": runtime_summary,
            "request": payload,
            "effective_input": effective_input,
            "decision": decision,
            "runtime_receipt": {
                "request_id": runtime_refs.get("request_id"),
                "runtime_refs": runtime_refs,
                "runtime_summary": runtime_summary,
                "runtime_status": runtime_status,
                "execution_mode": execution_mode,
                "authority_state": authority_state,
                "subject_agency_state": effective_input.get("subject_agency_state"),
                "decision_status": decision_body.get("status"),
                "allow": decision_body.get("allow"),
                "rule": decision_body.get("rule"),
                "reason": decision_body.get("reason"),
                "outcome_reason": outcome_reason,
            },
        }
    )

    return runtime_summary


@app.get("/health")
def health() -> Any:
    return jsonify({"status": "ok"})


@app.post("/set-state")
def set_state() -> Any:
    payload: Dict[str, Any] = request.get_json(force=True) or {}
    state = payload.get("state", "GuestsRestricted")

    set_authority_state(state)

    return jsonify({"status": "OK", "state": state})


@app.post("/execute")
def execute() -> Any:
    payload: Dict[str, Any] = request.get_json(force=True) or {}

    decision = gate.evaluate(payload)
    effective_input = effective_input_from_decision(payload, decision)

    state = get_authority_state()
    decision_body = decision.get("decision", {})
    decision_status = decision_body.get("status")
    allow = bool(decision_body.get("allow", False))
    runtime_refs = decision.get("runtime_refs", {})

    if state == "OperatorAway":
        safe_misty_led(255, 255, 255)

        response = {
            "status": "NEUTRAL",
            "authority_state": state,
            "execution": "held",
            "subject_agency_state": effective_input.get("subject_agency_state"),
            "request_id": runtime_refs.get("request_id"),
            "runtime_refs": runtime_refs,
            "effective_input": effective_input,
            "decision": decision,
            "reason": f"state={state}",
        }

        response["runtime_summary"] = emit_runtime_receipt(
            payload=payload,
            decision=decision,
            authority_state=state,
            runtime_status="NEUTRAL",
            execution_mode="held",
            outcome_reason=response["reason"],
        )

        return jsonify(response)

    if decision_status == "RESTRICT":
        safe_misty_led(255, 255, 0)

        decision_package = {
            "request_id": runtime_refs.get("request_id"),
            "receipt_id": runtime_refs.get("request_id"),
            "decision": decision_status,
            "runtime_status": "RESTRICTED",
            "execution_mode": {
                "action": "hold",
                "buffer_action": "HOLD_AND_NOTIFY",
            },
            "rule": decision_body.get("rule"),
            "reason": decision_body.get("reason", "Execution restricted"),
        }
        execution_result = execute_command(decision_package)

        response = {
            "status": "RESTRICTED",
            "authority_state": state,
            "execution": "bounded",
            "subject_agency_state": effective_input.get("subject_agency_state"),
            "request_id": runtime_refs.get("request_id"),
            "runtime_refs": runtime_refs,
            "allowed_autofunctions": [
                "led_yellow",
                "hold",
                "log",
                "notify_or_escalate_stub",
            ],
            "blocked_action": effective_input,
            "effective_input": effective_input,
            "decision_package": decision_package,
            "execution_result": execution_result,
            "decision": decision,
            "reason": decision_body.get("reason", "Execution restricted"),
        }

        response["runtime_summary"] = emit_runtime_receipt(
            payload=payload,
            decision=decision,
            authority_state=state,
            runtime_status="RESTRICTED",
            execution_mode="bounded",
            outcome_reason=response["reason"],
        )

        return jsonify(response)

    if state == "GuestsRestricted":
        safe_misty_led(255, 0, 0)

        response = {
            "status": "DENIED",
            "authority_state": state,
            "execution": "blocked",
            "subject_agency_state": effective_input.get("subject_agency_state"),
            "request_id": runtime_refs.get("request_id"),
            "runtime_refs": runtime_refs,
            "effective_input": effective_input,
            "decision": decision,
            "reason": f"state={state}",
        }

        response["runtime_summary"] = emit_runtime_receipt(
            payload=payload,
            decision=decision,
            authority_state=state,
            runtime_status="DENIED",
            execution_mode="blocked",
            outcome_reason=response["reason"],
        )

        return jsonify(response)

    if decision_status == "DENY" or not allow:
        safe_misty_led(255, 0, 0)

        response = {
            "status": "DENIED",
            "authority_state": state,
            "execution": "blocked",
            "subject_agency_state": effective_input.get("subject_agency_state"),
            "request_id": runtime_refs.get("request_id"),
            "runtime_refs": runtime_refs,
            "effective_input": effective_input,
            "decision": decision,
            "reason": decision_body.get("reason", "Execution denied"),
        }

        response["runtime_summary"] = emit_runtime_receipt(
            payload=payload,
            decision=decision,
            authority_state=state,
            runtime_status="DENIED",
            execution_mode="blocked",
            outcome_reason=response["reason"],
        )

        return jsonify(response)

    try:
        misty_response = requests.post(
            f"{MISTY}/led",
            json={"red": 0, "green": 0, "blue": 255},
            timeout=2,
        )

        response = {
            "status": "EXECUTED",
            "authority_state": state,
            "execution": "completed",
            "subject_agency_state": effective_input.get("subject_agency_state"),
            "request_id": runtime_refs.get("request_id"),
            "runtime_refs": runtime_refs,
            "effective_input": effective_input,
            "decision": decision,
            "misty_status_code": misty_response.status_code,
            "misty_response": misty_response.json()
            if misty_response.headers.get("content-type", "").startswith("application/json")
            else misty_response.text,
        }

        response["runtime_summary"] = emit_runtime_receipt(
            payload=payload,
            decision=decision,
            authority_state=state,
            runtime_status="EXECUTED",
            execution_mode="completed",
            outcome_reason="Execution completed",
        )

        return jsonify(response)

    except Exception as e:
        response = {
            "status": "ERROR",
            "authority_state": state,
            "execution": "failed",
            "subject_agency_state": effective_input.get("subject_agency_state"),
            "request_id": runtime_refs.get("request_id"),
            "runtime_refs": runtime_refs,
            "effective_input": effective_input,
            "decision": decision,
            "error": str(e),
        }

        response["runtime_summary"] = emit_runtime_receipt(
            payload=payload,
            decision=decision,
            authority_state=state,
            runtime_status="ERROR",
            execution_mode="failed",
            outcome_reason=str(e),
        )

        return jsonify(response), 500


if __name__ == "__main__":
    env = (os.environ.get("ENVIRONMENT") or "dev").lower()
    debug = env != "prod"
    app.run(host="0.0.0.0", port=8088, debug=debug)