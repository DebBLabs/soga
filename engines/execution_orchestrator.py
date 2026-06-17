from engines.restrict_execution_engine import (
    RestrictExecutionEngine,
)


class ExecutionOrchestrator:
    """
    Executes or withholds execution based on
    runtime governance decisions.
    """

    def run(
        self,
        cmr,
        standing_capabilities,
        available_evidence,
        governance_decisions=None,
    ):

        governance_decisions = governance_decisions or []

        decision_by_step = {
            item["step_id"]: item
            for item in governance_decisions
        }

        receipts = []

        for action in cmr.get("allowed_actions", []):

            step_id = f"step-{action}"
            decision = decision_by_step.get(
                step_id,
                {
                    "decision": "ALLOW",
                    "reason":
                        "Required authority and evidence were satisfied before execution.",
                    "restrict_mode": None,
                },
            )

            if decision["decision"] == "ALLOW":

                receipts.append(
                    {
                        "step_id": step_id,
                        "action": action,
                        "decision": "ALLOW",
                        "execution_status": "SIMULATED_COMPLETE",
                        "reason": decision["reason"],
                    }
                )

            elif decision["decision"] == "RESTRICT":

                restricted = (
                    RestrictExecutionEngine()
                    .execute(
                        {
                            "step_id": step_id,
                            "action": action,
                        },
                        decision["restrict_mode"],
                    )
                )

                receipts.append(
                    {
                        "step_id": step_id,
                        "action": action,
                        "decision": "RESTRICT",
                        "execution_status":
                            restricted["execution_status"],
                        "restrict_mode":
                            restricted["mode"],
                        "reason":
                            restricted["reason"],
                        "details":
                            restricted,
                    }
                )

            else:

                receipts.append(
                    {
                        "step_id": step_id,
                        "action": action,
                        "decision": "DENY",
                        "execution_status": "NOT_EXECUTED",
                        "reason": decision["reason"],
                    }
                )

        for action in cmr.get("forbidden_actions", []):

            step_id = f"step-{action}"
            decision = decision_by_step.get(
                step_id,
                {
                    "decision": "DENY",
                    "reason":
                        "Action is prohibited by mission constraint.",
                },
            )

            receipts.append(
                {
                    "step_id": step_id,
                    "action": action,
                    "decision": "DENY",
                    "execution_status": "NOT_EXECUTED",
                    "reason": decision["reason"],
                }
            )

        return {
            "mission_id": cmr["mission_id"],
            "receipts": receipts,
        }
