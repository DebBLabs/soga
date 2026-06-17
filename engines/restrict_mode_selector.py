class RestrictModeSelector:
    """
    Maps governance dimension REVIEW results
    into a RESTRICT execution mode.

    The PDP selects the mode.

    The execution layer implements it.
    """

    def select(
        self,
        dimensions,
    ):

        if dimensions["reachability"] == "REVIEW":
            return {
                "mode": "delayed_execution",
                "reason":
                    "Subject is not currently reachable; "
                    "bounded continuation or delay required.",
            }

        if dimensions["authority"] == "REVIEW":
            return {
                "mode": "reduced_authority",
                "reason":
                    "Authority attenuation requires reduced scope.",
            }

        if dimensions["subject_agency_state"] == "REVIEW":
            return {
                "mode": "supervised_execution",
                "reason":
                    "Subject governance state requires supervision.",
            }

        if dimensions["execution_context"] == "REVIEW":
            return {
                "mode": "bounded_continuation",
                "reason":
                    "Execution context permits only bounded continuation.",
            }

        if dimensions["policy"] == "REVIEW":
            return {
                "mode": "escalation",
                "reason":
                    "Policy requires escalation before completion.",
            }

        return {
            "mode": "partial_execution",
            "reason":
                "Partial execution selected as default RESTRICT path.",
        }
