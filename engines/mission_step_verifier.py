class MissionStepVerifier:
    """
    Converts evidence resolution into
    runtime-facing step verdicts.
    """

    STATUS_MAP = {
        "SATISFIED": "READY",
        "UNSATISFIED": "BLOCKED",
        "PROHIBITED": "PROHIBITED",
    }

    def verify(
        self,
        evidence_resolution,
    ):

        verdicts = []

        for item in evidence_resolution:

            verdict = self.STATUS_MAP.get(
                item.get("status"),
                "BLOCKED",
            )

            verdicts.append(
                {
                    "step_id":
                        item["step_id"],
                    "action":
                        item["action"],
                    "verdict":
                        verdict,
                    "evidence_status":
                        item.get("status"),
                    "matched_evidence":
                        item.get("matched_evidence", []),
                }
            )

        return verdicts
