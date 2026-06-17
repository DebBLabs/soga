class MWRUpdater:
    """
    Applies confirmed mission-only
    information back into the
    Mission Working Representation.
    """

    def apply(
        self,
        mwr,
        routed,
    ):

        if (
            routed.get("destination")
            == "mission_working_representation"
        ):

            mwr.inferred.setdefault(
                "confirmed_answers",
                []
            ).append(
                routed["value"]
            )

        return mwr
