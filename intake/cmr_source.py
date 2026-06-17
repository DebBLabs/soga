from __future__ import annotations

from builders.mission_builder import (
    mission_file_to_template,
)

from intake.mission_intake_engine import (
    MissionIntakeEngine,
)


def cmr_from_mission_file(path):
    """
    Existing path.

    Mission file -> CMR.
    """

    return mission_file_to_template(path)


def cmr_from_human_intent(
    human_intent,
    sector_knowledge=None,
):
    """
    Sprint 6 path.

    Human Intent -> Mission Intake -> CMR.
    """

    result = MissionIntakeEngine().intake(
        human_intent,
        sector_knowledge=sector_knowledge,
    )

    if result["status"] != "PASS":
        return result

    return result["cmr"]
