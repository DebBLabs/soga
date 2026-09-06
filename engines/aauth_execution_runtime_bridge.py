from __future__ import annotations

from typing import Any, Dict

from engines.canonical_decision_package_adapter import (
    CanonicalDecisionPackageAdapter,
)
from engines.runtime_governance_engine import RuntimeGovernanceEngine
from input_adapters.aauth_execution_adapter import (
    adapt_aauth_execution_request,
)


def _title_case_enum(value: str, default: str) -> str:
    if not value:
        return default

    normalized = str(value).strip().upper()

    mapping = {
        "INDEPENDENT": "Independent",
        "SUPERVISED": "Supervised",
        "MANAGED": "Managed",
        "DELEGATED": "Delegated",
        "LAPSED": "Lapsed",
        "REACHABLE": "Reachable",
        "UNREACHABLE": "Unreachable",
        "UNKNOWN": "Unknown",
    }

    return mapping.get(normalized, default)


def evaluate_aauth_execution_request(
    execution_request: Dict[str, Any],
    *,
    verified_authority_state: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Evaluate an AAuth execution request through SOGA runtime governance.

    This bridge preserves the Sprint 8 architecture:

    AAuth-shaped request
        -> AAuthExecutionAdapter
        -> RuntimeEnvelope
        -> RuntimeGovernanceEngine
        -> Canonical Decision Package

    The adapter remains projection-only.
    The Runtime Governance Engine produces the governance decision.
    The CDP adapter packages the decision.
    """

    envelope = adapt_aauth_execution_request(execution_request)
    envelope_dict = envelope.to_dict()

    requested_action = (
        envelope.execution_context.get("requested_action")
        or "execution"
    )

    runtime_plan = [
        {
            "step_id": envelope.request_id,
            "action": requested_action,
            "runtime_action": "PROCEED",
            "reason": "AAuth execution request projected into SOGA runtime plan.",
        }
    ]

    selected_evidence = [
        {
            "step_id": envelope.request_id,
            "status": "PROCEED",
            "selected_evidence": envelope.authority.to_dict(),
        }
    ]

    subject_agency_state = _title_case_enum(
        envelope.subject.governance_state.value,
        "Independent",
    )

    reachability = _title_case_enum(
        envelope.subject.reachability.value,
        "Reachable",
    )

    # AAuth execution requests may omit live reachability.
    # For the initial ALLOW path, absent reachability is treated
    # as Reachable at the runtime bridge layer. Explicit UNKNOWN
    # or UNREACHABLE values still flow through and may produce
    # REVIEW / RESTRICT or FAIL according to RuntimeGovernanceEngine.
    if reachability == "Unknown" and not (
        execution_request.get("reachability")
        or execution_request.get("runtime", {}).get("reachability")
        or execution_request.get("subject", {}).get("reachability")
    ):
        reachability = "Reachable"

    if verified_authority_state is None:
        # Compatibility-only path for the pre-M02 callers. New Person Server
        # code must pass state derived from verified retained authority.
        authority_runtime = {
            "revoked": False,
            "expired": False,
            "delegation_hops": 0,
            "max_delegation_hops": 3,
            "elapsed_seconds": 0,
            "max_elapsed_seconds": 86400,
            "attenuated": False,
            "additional_inputs": {
                "source_protocol": envelope.authority.source_protocol,
                "authority_id": envelope.authority.authority_id,
            },
        }
    else:
        required_authority_inputs = {
            "revoked",
            "expired",
            "delegation_hops",
            "max_delegation_hops",
            "elapsed_seconds",
            "max_elapsed_seconds",
            "attenuated",
        }
        missing = required_authority_inputs.difference(verified_authority_state)
        if missing:
            raise ValueError(
                "verified_authority_state is missing required live inputs: "
                + ", ".join(sorted(missing))
            )
        boolean_fields = {"revoked", "expired", "attenuated"}
        integer_fields = {
            "delegation_hops",
            "max_delegation_hops",
            "elapsed_seconds",
            "max_elapsed_seconds",
        }
        if any(type(verified_authority_state[name]) is not bool for name in boolean_fields):
            raise TypeError("verified authority flags must be booleans")
        if any(
            type(verified_authority_state[name]) is not int
            or verified_authority_state[name] < 0
            for name in integer_fields
        ):
            raise TypeError("verified authority counts and limits must be non-negative integers")
        authority_runtime = {
            name: verified_authority_state[name] for name in required_authority_inputs
        }
        authority_runtime["additional_inputs"] = {
            "source_protocol": envelope.authority.source_protocol,
            "authority_id": envelope.authority.authority_id,
            "live_input_source": verified_authority_state.get("source"),
            "observed_at": verified_authority_state.get("observed_at"),
            "unavailable": list(verified_authority_state.get("unavailable", ())),
        }
        required_authority_facts = set(
            envelope.policy.get("required_authority_facts", ())
        )
        unavailable_authority_facts = set(
            verified_authority_state.get("unavailable", ())
        )
        unavailable_required = required_authority_facts.intersection(
            unavailable_authority_facts
        )
        if unavailable_required:
            raise ValueError(
                "required verified authority facts are unavailable: "
                + ", ".join(sorted(unavailable_required))
            )

    runtime = {
        "authority": authority_runtime,
        "subject_agency_state": subject_agency_state,
        "reachability": reachability,
        "execution_context": envelope.execution_context,
        "execution_context_valid": True,
        "policy": envelope.policy,
        "provenance": "AAuthExecutionRuntimeBridge",
    }

    decisions = RuntimeGovernanceEngine().evaluate(
        runtime_plan,
        evidence_selection=selected_evidence,
        runtime=runtime,
    )

    decision = decisions[0]

    cdp = CanonicalDecisionPackageAdapter().build_for_step(
        decision=decision,
        cmr=envelope.mission.to_dict(),
        runtime=runtime,
        receipt={
            "receipt_id": f"receipt-{envelope.request_id}",
            "step_id": envelope.request_id,
        },
    )

    return {
        "governance_determination": decision["decision"],
        "reason": decision["reason"],
        "runtime_envelope": envelope_dict,
        "governance_decision": decision,
        "canonical_decision_package": cdp.to_dict(),
    }
