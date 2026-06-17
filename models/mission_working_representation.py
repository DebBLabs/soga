from dataclasses import dataclass, field
from typing import Any


@dataclass
class MissionWorkingRepresentation:
    """
    Temporary mission-specific representation produced by
    the Glean process.

    It is NOT persistent truth.

    It combines:
        - candidate observations
        - subject representation
        - mission context
        - sector knowledge

    It exists only for the current mission.
    """

    candidate_observations: list[dict[str, Any]] = field(default_factory=list)

    subject_representation: dict[str, Any] = field(default_factory=dict)

    mission_context: dict[str, Any] = field(default_factory=dict)

    sector_knowledge: list[str] = field(default_factory=list)

    inferred: dict[str, Any] = field(default_factory=dict)

    unresolved: list[str] = field(default_factory=list)

    validation_findings: list[dict[str, Any]] = field(default_factory=list)

    proposed_updates: list[dict[str, Any]] = field(default_factory=list)

    persistence_scope: str = "mission_only"

    intake_status: str = "working"
