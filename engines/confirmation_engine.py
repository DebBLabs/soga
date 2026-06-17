class ConfirmationEngine:
    """
    Consumes confirmed answers and determines
    whether they apply only to this mission
    or should be proposed for persistent
    Subject Representation.
    """

    def process(
        self,
        question: dict,
        answer,
    ):

        scope = question.get(
            "scope",
            "mission_only",
        )

        if scope == "subject_persistent":

            return {
                "destination": "subject_representation",
                "value": answer,
            }

        if scope == "mission_only":

            return {
                "destination": "mission_working_representation",
                "value": answer,
            }

        return {
            "destination": "discard",
            "value": answer,
        }
