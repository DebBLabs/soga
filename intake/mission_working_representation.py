from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class MissionWorkingRepresentation:
    """
    Transient reasoning artifact.

    Exists only between Glean and Validation.
    It is NOT a governance artifact.
    """

    original_request: str

    candidate_observations: List[str] = field(default_factory=list)

    inferred_subject: Dict = field(default_factory=dict)

    inferred_delegates: List[Dict] = field(default_factory=list)

    inferred_resources: List[Dict] = field(default_factory=list)

    inferred_allowed_actions: List[str] = field(default_factory=list)

    inferred_forbidden_actions: List[str] = field(default_factory=list)

    inferred_bounds: Dict = field(default_factory=dict)

    unresolved_questions: List[str] = field(default_factory=list)

    confidence_notes: List[str] = field(default_factory=list)

    sector_knowledge_used: List[str] = field(default_factory=list)
