class EvidenceResolver:
    """
    Resolves step-level authority requirements
    against currently available evidence and
    standing Subject capabilities.

    This is not a protocol picker.
    It checks whether required authority can
    be satisfied before execution.
    """

    def resolve(
        self,
        requirements,
        available_evidence,
        standing_capabilities=None,
    ):

        standing_capabilities = standing_capabilities or []

        results = []

        available_types = {
            item.get("type")
            for item in available_evidence
        }

        capability_types = {
            item.get("evidence_type")
            for item in standing_capabilities
            if item.get("status") == "active"
        }

        satisfiers = available_types.union(
            capability_types
        )

        for requirement in requirements:

            acceptable = set(
                requirement.get(
                    "acceptable_evidence",
                    [],
                )
            )

            matched = sorted(
                acceptable.intersection(
                    satisfiers
                )
            )

            if requirement.get("status") == "PROHIBITED":

                results.append(
                    {
                        "step_id": requirement["step_id"],
                        "action": requirement["action"],
                        "status": "PROHIBITED",
                        "matched_evidence": [],
                        "unmatched_acceptable_evidence": [],
                    }
                )

                continue

            unmatched = sorted(
                acceptable.difference(
                    satisfiers
                )
            )

            results.append(
                {
                    "step_id": requirement["step_id"],
                    "action": requirement["action"],
                    "status": (
                        "SATISFIED"
                        if matched
                        else "UNSATISFIED"
                    ),
                    "matched_evidence": matched,
                    "unmatched_acceptable_evidence": unmatched,
                    "standing_capabilities_checked": (
                        standing_capabilities
                    ),
                }
            )

        return results
