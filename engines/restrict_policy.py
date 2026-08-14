from __future__ import annotations

from typing import Any, Mapping


def authorized_restrict_constraint(
    policy: Mapping[str, Any], action: str
) -> dict[str, Any] | None:
    """Return the authorized Stage Gate constraint for an action, if declared."""
    for constraint in policy.get("stage_gate", []):
        if constraint.get("step_id") == action and constraint.get("restrict_path"):
            return dict(constraint)
    return None


def approval_satisfies_constraint(
    evidence: Mapping[str, Any] | None,
    constraint: Mapping[str, Any] | None,
    *,
    mission_s256: str,
    action: str,
) -> bool:
    """Validate provisional G26 approval evidence against its exact constraint."""
    if not evidence or not constraint:
        return False
    return all(
        (
            evidence.get("evidence_schema")
            == "provisional-g26-approval-evidence-v1",
            evidence.get("convergence_obligation")
            == "future-canonical-stage-gate-clearance-evidence-schema",
            evidence.get("result") == "approve",
            evidence.get("person_server_authenticated_assertion") is True,
            evidence.get("holder_attribution_asserted") is True,
            evidence.get("mission_s256") == mission_s256,
            evidence.get("action") == action,
            evidence.get("originating_soga_decision") == "RESTRICT",
            evidence.get("restrict_path") == "HOLDING",
            evidence.get("constraint_reference") == constraint.get("gate_id"),
            evidence.get("required_evidence") == constraint.get("required_evidence"),
            evidence.get("authority_reference") == constraint.get("authority_reference"),
        )
    )
