class RuntimeAcquisitionPlanner:
    """
    Determines what runtime actions are needed
    before each mission step may execute.

    It does not choose protocols or vendors.
    It simply identifies the governance actions
    required to satisfy the mission.
    """

    def plan(self, gap_report):

        runtime_plan = []

        for step in gap_report["steps"]:

            if step["verdict"] == "READY":

                runtime_plan.append(
                    {
                        "step_id": step["step_id"],
                        "action": step["action"],
                        "runtime_action": "PROCEED",
                        "reason": "All required capability and evidence are available.",
                    }
                )

            elif step["verdict"] == "PROHIBITED":

                runtime_plan.append(
                    {
                        "step_id": step["step_id"],
                        "action": step["action"],
                        "runtime_action": "DENY",
                        "reason": "Mission policy prohibits execution.",
                    }
                )

            else:

                runtime_plan.append(
                    {
                        "step_id": step["step_id"],
                        "action": step["action"],
                        "runtime_action": "ACQUIRE_EVIDENCE",
                        "required_capability": step["required_capability"],
                        "reason": (
                            "Execution must pause until sufficient "
                            "authority evidence is obtained."
                        ),
                    }
                )

        return runtime_plan
