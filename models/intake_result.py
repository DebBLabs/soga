from dataclasses import dataclass, field
from typing import Any, Optional

from models.mission_working_representation import (
    MissionWorkingRepresentation,
)


@dataclass
class IntakeResult:
    """
    Final output of Mission Intake.

    This object represents the state of intake
    before CMR compilation.
    """

    request: str

    candidate_observations: list[dict[str, Any]] = field(
        default_factory=list
    )

    mission_working_representation: Optional[
        MissionWorkingRepresentation
    ] = None

    validation: dict[str, Any] = field(
        default_factory=dict
    )

    questions: list[dict[str, Any]] = field(
        default_factory=list
    )
