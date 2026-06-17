from intake.glean import glean
from intake.validation import validate
from intake.cmr_builder import mwr_to_cmr


class MissionIntakeEngine:
    """
    Representation engine.

    Produces a validated CMR.

    Performs no governance reasoning.
    """

    def intake(
        self,
        human_intent,
        subject_representation=None,
        mission_context=None,
        sector_knowledge=None,
        debug=False,
    ):
        mwr = glean(
            human_intent,
            subject_representation,
            mission_context,
            sector_knowledge,
        )

        validation = validate(mwr)

        if validation["status"] != "PASS":
            return {
                "status": "FINDING",
                "validation": validation,
            }

        cmr = mwr_to_cmr(mwr)

        result = {
            "status": "PASS",
            "validation": validation,
            "cmr": cmr,
        }

        if debug:
            result["mwr"] = mwr

        return result
