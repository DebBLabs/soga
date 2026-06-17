class EvidenceJustificationEngine:
    """
    Explains why selected evidence was chosen
    for each mission step.

    This is not protocol justification.
    It explains evidence sufficiency.
    """

    def justify(
        self,
        evidence_selection,
    ):

        justifications = []

        for item in evidence_selection:

            if item["status"] == "NOT_ALLOWED":

                justifications.append(
                    {
                        "step_id": item["step_id"],
                        "action": item["action"],
                        "selected_evidence": None,
                        "justification": (
                            "No evidence may authorize this step "
                            "because the mission prohibits it."
                        ),
                        "alternatives": [],
                    }
                )

                continue

            if item["selected_evidence"] is None:

                justifications.append(
                    {
                        "step_id": item["step_id"],
                        "action": item["action"],
                        "selected_evidence": None,
                        "justification": (
                            "No available evidence satisfies "
                            "the step requirement."
                        ),
                        "alternatives": item.get(
                            "alternatives",
                            [],
                        ),
                    }
                )

                continue

            justifications.append(
                {
                    "step_id": item["step_id"],
                    "action": item["action"],
                    "selected_evidence":
                        item["selected_evidence"],
                    "justification": (
                        "Selected evidence was available "
                        "and satisfies the authority requirement "
                        "for this step."
                    ),
                    "alternatives": item.get(
                        "alternatives",
                        [],
                    ),
                }
            )

        return justifications
