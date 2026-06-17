from advisory.advisory_dimension_evidence import (
    advisory_dimension_review_signals,
)
from advisory.advisory_dimension_evidence import (
    advisory_dimension_review_signals,
)
from engines.restrict_mode_selector import (
    RestrictModeSelector,
)
from engines.runtime_dimension_evaluator import (
    RuntimeDimensionEvaluator,
)


class RuntimeGovernanceEngine:
    """
    Makes the final governance decision at
    execution time using the six SOGA
    governance dimensions.

    The PDP decides ALLOW, RESTRICT, or DENY.

    If RESTRICT applies, the PDP selects the
    restriction mode. The execution layer
    implements that mode.
    """

    def evaluate(
        self,
        runtime_plan,
        evidence_selection=None,
        runtime=None,
    ):

        evidence_selection = evidence_selection or []
        runtime = runtime or {}

        selection_by_step = {
            item["step_id"]: item
            for item in evidence_selection
        }

        decisions = []

        for item in runtime_plan:

            selection = selection_by_step.get(
                item["step_id"],
                {},
            )

            step = {
                "step_id": item["step_id"],
                "action": item["action"],
                "status": selection.get(
                    "status",
                    item["runtime_action"],
                ),
                "selected_evidence": selection.get(
                    "selected_evidence",
                ),
            }

            review_signals = (
                advisory_dimension_review_signals(
                    runtime
                )
            )

            dimensions = (
                RuntimeDimensionEvaluator()
                .evaluate(
                    step,
                    runtime,
                    review_signals,
                )
            )

            restrict_mode = None

            if "FAIL" in dimensions.values():

                decision = "DENY"
                reason = (
                    "One or more governance dimensions "
                    "failed at execution time."
                )

            elif "REVIEW" in dimensions.values():

                decision = "RESTRICT"
                restrict_mode = (
                    RestrictModeSelector()
                    .select(dimensions)
                )
                reason = restrict_mode["reason"]

            else:

                decision = "ALLOW"
                reason = (
                    "All governance dimensions passed "
                    "at execution time."
                )

            decisions.append(
                {
                    "step_id": item["step_id"],
                    "action": item["action"],
                    "decision": decision,
                    "reason": reason,
                    "dimensions": dimensions,
                    "restrict_mode": restrict_mode,
                }
            )

        return decisions
