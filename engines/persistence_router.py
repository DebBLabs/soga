from engines.subject_representation_updater import (
    SubjectRepresentationUpdater,
)


class PersistenceRouter:

    def __init__(self):

        self.updater = (
            SubjectRepresentationUpdater()
        )

    def route(
        self,
        question,
        answer,
    ):

        scope = question.get(
            "scope",
            "mission_only",
        )

        if scope == "mission_only":

            return {
                "destination":
                    "mission_working_representation",
                "status":
                    "MISSION_ONLY",
                "value":
                    answer,
            }

        if scope == "subject_persistent":

            return self.updater.propose(
                {
                    "question":
                        question["question"],
                    "answer":
                        answer,
                }
            )

        return {
            "destination":
                "discard",
            "status":
                "DISCARDED",
        }
