class EvidenceAcquisitionEngine:
    """
    Determines whether missing evidence can be
    acquired for a mission step.

    This is not a protocol picker.
    It records acquisition requirements when
    evidence is not already available.
    """

    def acquire(
        self,
        step_verdicts,
        evidence_resolution,
    ):

        acquisitions = []

        resolution_by_step = {
            item["step_id"]: item
            for item in evidence_resolution
        }

        for verdict in step_verdicts:

            step_id = verdict["step_id"]
            resolution = resolution_by_step.get(
                step_id,
                {},
            )

            if verdict["verdict"] == "READY":

                acquisitions.append(
                    {
                        "step_id": step_id,
                        "action": verdict["action"],
                        "status": "NOT_REQUIRED",
                        "reason": "Evidence already satisfies step.",
                    }
                )

            elif verdict["verdict"] == "PROHIBITED":

                acquisitions.append(
                    {
                        "step_id": step_id,
                        "action": verdict["action"],
                        "status": "NOT_ALLOWED",
                        "reason": "Step is prohibited by mission constraint.",
                    }
                )

            else:

                acquisitions.append(
                    {
                        "step_id": step_id,
                        "action": verdict["action"],
                        "status": "REQUIRED",
                        "acceptable_evidence": (
                            resolution.get(
                                "unmatched_acceptable_evidence",
                                [],
                            )
                        ),
                        "reason": (
                            "Step cannot proceed until sufficient "
                            "evidence is acquired."
                        ),
                    }
                )

        return acquisitions
