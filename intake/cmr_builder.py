from __future__ import annotations

from verify.mission_template import (
    MissionLifecycle,
    MissionTemplate,
)

from intake.mission_working_representation import (
    MissionWorkingRepresentation,
)


def mwr_to_cmr(
    mwr: MissionWorkingRepresentation,
) -> MissionTemplate:
    """
    Converts a validated MWR into a CMR.

    Performs no governance reasoning.
    """

    subject_id = "subject-001"

    if mwr.inferred_subject:
        subject_id = "subject-001"

    return MissionTemplate(
        mission_id="mission-intake-generated-001",
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=subject_id,
        objective=mwr.original_request,
        allowed_actions=mwr.inferred_allowed_actions,
        forbidden_actions=mwr.inferred_forbidden_actions,
        bounds=mwr.inferred_bounds,
        references={
            "title": mwr.original_request,
            "actors": [
                {
                    "actor_id": d.get(
                        "candidate",
                        "delegate",
                    ),
                    "role": "delegated_representative",
                }
                for d in mwr.inferred_delegates
            ],
            "resources": mwr.inferred_resources,
        },
        metadata={
            "builder": "mission_builder",
            "evaluate_at_execution": True,
        },
    )
