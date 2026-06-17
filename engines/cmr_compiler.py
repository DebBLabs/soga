class CMRCompiler:
    """
    Compiles a ready Mission Working Representation
    into the existing canonical mission JSON shape.

    This is not the runtime decision.
    This is the mission artifact that can feed
    the existing SOGA pipeline.
    """

    def compile(
        self,
        mwr,
    ):

        observations = {
            obs.get("semantic_type"): obs
            for obs in mwr.candidate_observations
        }

        objective = observations.get(
            "objective",
            {},
        ).get(
            "value",
            "unspecified objective",
        )

        delegate = observations.get(
            "delegate",
            {},
        ).get(
            "value",
            "unspecified delegate",
        )

        confirmed_answers = mwr.inferred.get(
            "confirmed_answers",
            [],
        )

        return {
            "mission_id":
                "mission-intake-generated-001",
            "title":
                objective,
            "objective":
                objective,
            "subject": {
                "subject_id":
                    "subject-001",
                "display_name":
                    "Subject",
            },
            "actors": [
                {
                    "actor_id":
                        delegate,
                    "role":
                        "delegated_representative",
                }
            ],
            "resources": [],
            "allowed_actions": [
                "schedule_appointment",
            ],
            "forbidden_actions": [
                "authorize_treatment",
            ],
            "bounds": {
                "confirmed_authority":
                    confirmed_answers,
            },
            "governance": {
                "subject_agency_state":
                    "ACTIVE",
                "evaluate_at_execution":
                    True,
            },
        }
