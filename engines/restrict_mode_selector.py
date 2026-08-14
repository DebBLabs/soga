class RestrictModeSelector:
    """
    Maps governance dimension REVIEW results
    into a RESTRICT execution mode.

    The PDP selects the mode.

    The execution layer implements it.
    """

    def select(self, dimensions, *, policy=None, action=None):

        policy = policy or {}

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
            from engines.restrict_policy import authorized_restrict_constraint

            constraint = authorized_restrict_constraint(policy, action)
            if constraint is not None:
                return {
                    "mode": constraint["restrict_path"],
                    "reason": "Authorized mission/policy constraint selected the RESTRICT path.",
                    "constraint": constraint,
                }
            return {
                "mode": "fail_closed",
                "reason": "SOGA RESTRICT has no authorized operational path; no path was inferred.",
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
