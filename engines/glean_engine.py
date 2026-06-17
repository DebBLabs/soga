from __future__ import annotations

from typing import Any

from models.mission_working_representation import MissionWorkingRepresentation


class GleanEngine:
    """
    Glean is the reasoning process that constructs a mission-specific
    working representation from current observations, accumulated
    Subject Representation, Mission Context, and Sector Knowledge.

    It does not update persistent Subject Representation.
    It does not compile the CMR.
    It does not evaluate execution-time authority.
    """

    def glean(
        self,
        candidate_observations: list[dict[str, Any]],
        subject_representation: dict[str, Any],
        mission_context: dict[str, Any],
        sector_knowledge: list[str],
    ) -> MissionWorkingRepresentation:
        return MissionWorkingRepresentation(
            candidate_observations=candidate_observations,
            subject_representation=subject_representation,
            mission_context=mission_context,
            sector_knowledge=sector_knowledge,
            inferred={},
            unresolved=[],
        )
