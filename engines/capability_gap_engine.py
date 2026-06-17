class CapabilityGapEngine:
    """
    Produces a gap report from capability discovery,
    evidence resolution, and step verdicts.

    This does not pick protocols.
    It identifies what is ready, blocked,
    prohibited, or must be acquired.
    """

    def analyze(
        self,
        execution_result,
        acquisition_plan,
    ):

        capability_by_step = {
            item["step_id"]: item
            for item in execution_result.get(
                "capability_discovery",
                []
            )
        }

        evidence_by_step = {
            item["step_id"]: item
            for item in execution_result.get(
                "evidence_resolution",
                []
            )
        }

        acquisition_by_step = {
            item["step_id"]: item
            for item in acquisition_plan
        }

        report = {
            "mission_id":
                execution_result["mission_id"],
            "steps":
                [],
            "summary": {
                "ready": 0,
                "blocked": 0,
                "prohibited": 0,
                "capabilities_to_acquire": [],
            },
        }

        for verdict in execution_result.get(
            "step_verdicts",
            [],
        ):

            step_id = verdict["step_id"]
            capability = capability_by_step.get(
                step_id,
                {},
            )
            evidence = evidence_by_step.get(
                step_id,
                {},
            )
            acquisition = acquisition_by_step.get(
                step_id,
                {},
            )

            if verdict["verdict"] == "READY":
                report["summary"]["ready"] += 1

            elif verdict["verdict"] == "PROHIBITED":
                report["summary"]["prohibited"] += 1

            else:
                report["summary"]["blocked"] += 1

                required = capability.get(
                    "required_capability"
                )

                if required:
                    report["summary"][
                        "capabilities_to_acquire"
                    ].append(required)

            report["steps"].append(
                {
                    "step_id":
                        step_id,
                    "action":
                        verdict["action"],
                    "verdict":
                        verdict["verdict"],
                    "required_capability":
                        capability.get(
                            "required_capability"
                        ),
                    "capability_status":
                        capability.get(
                            "capability_status"
                        ),
                    "matched_evidence":
                        evidence.get(
                            "matched_evidence",
                            [],
                        ),
                    "acquisition_status":
                        acquisition.get(
                            "status"
                        ),
                    "reason":
                        acquisition.get(
                            "reason"
                        ),
                }
            )

        return report
