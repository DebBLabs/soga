class SubjectRepresentationUpdater:
    """
    Responsible for proposing updates to the
    persistent Subject Representation.

    It does not write directly. Future policy
    may require additional review.
    """

    def propose(
        self,
        item,
    ):

        return {
            "status": "PROPOSED",
            "destination": "subject_representation",
            "item": item,
        }
