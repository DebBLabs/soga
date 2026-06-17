"""
SOGA Canonical Decision Package
Version: 0.1
Status: Reference Implementation

This module defines the normative execution-time governance artifact.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime, timezone


class GovernanceDetermination(str, Enum):
    ALLOW = "ALLOW"
    RESTRICT = "RESTRICT"
    DENY = "DENY"


class DimensionEvaluation(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    FAIL = "FAIL"


class SubjectAgencyState(str, Enum):
    INDEPENDENT = "Independent"
    SUPERVISED = "Supervised"
    MANAGED = "Managed"
    DELEGATED = "Delegated"
    LAPSED = "Lapsed"


class Reachability(str, Enum):
    REACHABLE = "Reachable"
    UNREACHABLE = "Unreachable"
    UNKNOWN = "Unknown"


@dataclass
class AuthorityInputs:
    elapsed_time: Optional[Any] = None
    delegation_chain_state: Optional[Any] = None
    delegation_attenuation: Optional[Any] = None
    revocation_status: Optional[Any] = None
    additional_inputs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DimensionResults:
    mission: DimensionEvaluation
    authority: DimensionEvaluation
    subject_agency_state: DimensionEvaluation
    reachability: DimensionEvaluation
    execution_context: DimensionEvaluation
    policy: DimensionEvaluation


@dataclass
class CanonicalDecisionPackage:

    governance_determination: GovernanceDetermination

    dimension_results: DimensionResults

    authority_inputs: AuthorityInputs

    subject_agency_state: SubjectAgencyState

    reachability: Reachability

    mission: Any

    execution_context: Any

    policy: Any

    restrict_mode: Optional[str] = None

    execution_receipt: Optional[str] = None

    provenance: Optional[str] = None

    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def to_dict(self):
        return asdict(self)

    def validate(self):

        if (
            self.governance_determination
            not in GovernanceDetermination
        ):
            raise ValueError(
                "Invalid Governance Determination"
            )

        if (
            self.governance_determination
            == GovernanceDetermination.RESTRICT
            and not self.restrict_mode
        ):
            raise ValueError(
                "RESTRICT requires restrict_mode"
            )
