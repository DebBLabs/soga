"""
SOGA Canonical Decision Package Adapter

Packages runtime governance decisions into the normative
Canonical Decision Package artifact.

This adapter performs packaging only.
It does not perform governance evaluation.
"""

from typing import Any, Dict, List, Optional

from verify.decision_package_builder import build_decision_package


def _normalize_dimensions(dimensions: Dict[str, str]) -> Dict[str, str]:
    return {
        "mission": dimensions.get("mission", "PASS"),
        "authority": dimensions.get("authority", "PASS"),
        "subject_agency_state": dimensions.get(
            "subject_agency_state",
            dimensions.get(
                "subject_agency_state",
                dimensions.get("subject", "PASS"),
            ),
        ),
        "reachability": dimensions.get("reachability", "PASS"),
        "execution_context": dimensions.get(
            "execution_context",
            "PASS",
        ),
        "policy": dimensions.get("policy", "PASS"),
    }


def _restrict_mode_value(
    restrict_mode: Any,
) -> Optional[str]:

    if not restrict_mode:
        return None

    if isinstance(restrict_mode, dict):
        return (
            restrict_mode.get("mode")
            or restrict_mode.get("name")
            or restrict_mode.get("type")
            or restrict_mode.get("decision")
            or "RESTRICT"
        )

    return str(restrict_mode)


class CanonicalDecisionPackageAdapter:

    def build_for_step(
        self,
        *,
        decision: Dict[str, Any],
        cmr: Dict[str, Any],
        runtime: Dict[str, Any],
        receipt: Optional[Dict[str, Any]] = None,
    ):

        runtime = runtime or {}
        receipt = receipt or {}

        dimensions = _normalize_dimensions(
            decision.get("dimensions", {})
        )

        authority_inputs = runtime.get(
            "authority",
            {},
        )

        subject_agency_state = runtime.get(
            "subject_agency_state",
            "Independent",
        )

        reachability = runtime.get(
            "reachability",
            "Reachable",
        )

        execution_context = runtime.get(
            "execution_context",
            {
                "step_id": decision.get("step_id"),
                "action": decision.get("action"),
            },
        )

        policy = runtime.get(
            "policy",
            {},
        )

        execution_receipt = (
            receipt.get("receipt_id")
            or receipt.get("step_id")
            or decision.get("step_id")
            or "generated"
        )

        provenance = runtime.get(
            "provenance",
            "SOGA-RuntimeGovernanceEngine",
        )

        return build_decision_package(
            determination=decision["decision"],
            dimensions=dimensions,
            authority_inputs=authority_inputs,
            subject_agency_state=subject_agency_state,
            reachability=reachability,
            mission=cmr,
            execution_context=execution_context,
            policy=policy,
            execution_receipt=execution_receipt,
            provenance=provenance,
            restrict_mode=_restrict_mode_value(
                decision.get("restrict_mode")
            ),
        )

    def build_many(
        self,
        *,
        decisions: List[Dict[str, Any]],
        cmr: Dict[str, Any],
        runtime: Dict[str, Any],
        receipts: Optional[List[Dict[str, Any]]] = None,
    ):

        receipts = receipts or []

        receipts_by_step = {
            r.get("step_id"): r
            for r in receipts
        }

        return [
            self.build_for_step(
                decision=d,
                cmr=cmr,
                runtime=runtime,
                receipt=receipts_by_step.get(
                    d.get("step_id"),
                    {},
                ),
            )
            for d in decisions
        ]
