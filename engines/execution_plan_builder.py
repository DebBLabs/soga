class ExecutionPlanBuilder:
    """
    Builds executable mission steps from a CMR.

    This does not execute anything.
    It identifies steps that must later be
    checked against authority requirements
    and evidence resolution.
    """

    def build(
        self,
        cmr,
    ):

        steps = []

        for action in cmr.get("allowed_actions", []):

            steps.append(
                {
                    "step_id": f"step-{action}",
                    "action": action,
                    "status": "PLANNED",
                    "execution_type": "allowed_action",
                    "requires_authority_check": True,
                    "resources": cmr.get("resources", []),
                    "constraints": cmr.get("bounds", {}),
                }
            )

        for action in cmr.get("forbidden_actions", []):

            steps.append(
                {
                    "step_id": f"step-{action}",
                    "action": action,
                    "status": "PROHIBITED",
                    "execution_type": "forbidden_action",
                    "requires_authority_check": False,
                    "resources": [],
                    "constraints": {
                        "reason": "Forbidden by mission constraint",
                    },
                }
            )

        return {
            "mission_id": cmr["mission_id"],
            "objective": cmr.get("objective"),
            "steps": steps,
        }
