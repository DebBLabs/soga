"""
SOGA Canonical Decision Package Builder
"""

from typing import Any, Dict

from verify.canonical_decision_package import (
    CanonicalDecisionPackage,
    GovernanceDetermination,
    DimensionEvaluation,
    DimensionResults,
    AuthorityInputs,
    SubjectAgencyState,
    Reachability,
)


def _dimension(value: str) -> DimensionEvaluation:
    return DimensionEvaluation[value.upper()]


def _determination(value: str) -> GovernanceDetermination:
    return GovernanceDetermination[value.upper()]


def _subject_state(value: str) -> SubjectAgencyState:
    lookup = {
        "independent": SubjectAgencyState.INDEPENDENT,
        "supervised": SubjectAgencyState.SUPERVISED,
        "managed": SubjectAgencyState.MANAGED,
        "delegated": SubjectAgencyState.DELEGATED,
        "lapsed": SubjectAgencyState.LAPSED,
    }
    return lookup[value.lower()]


def _reachability(value: str) -> Reachability:
    lookup = {
        "reachable": Reachability.REACHABLE,
        "unreachable": Reachability.UNREACHABLE,
        "unknown": Reachability.UNKNOWN,
    }
    return lookup[value.lower()]


def build_decision_package(
    determination: str,
    dimensions: Dict[str, str],
    authority_inputs: Dict[str, Any],
    subject_agency_state: str,
    reachability: str,
    mission: Any,
    execution_context: Any,
    policy: Any,
    execution_receipt: str,
    provenance: str,
    restrict_mode=None,
):

    package = CanonicalDecisionPackage(

        governance_determination=_determination(
            determination
        ),

        dimension_results=DimensionResults(
            mission=_dimension(
                dimensions["mission"]
            ),
            authority=_dimension(
                dimensions["authority"]
            ),
            subject_agency_state=_dimension(
                dimensions["subject_agency_state"]
            ),
            reachability=_dimension(
                dimensions["reachability"]
            ),
            execution_context=_dimension(
                dimensions["execution_context"]
            ),
            policy=_dimension(
                dimensions["policy"]
            ),
        ),

        authority_inputs=AuthorityInputs(
            elapsed_time=authority_inputs.get(
                "elapsed_time"
            ),
            delegation_chain_state=authority_inputs.get(
                "delegation_chain_state"
            ),
            delegation_attenuation=authority_inputs.get(
                "delegation_attenuation"
            ),
            revocation_status=authority_inputs.get(
                "revocation_status"
            ),
            additional_inputs=authority_inputs.get(
                "additional_inputs",
                {},
            ),
        ),

        subject_agency_state=_subject_state(
            subject_agency_state
        ),

        reachability=_reachability(
            reachability
        ),

        mission=mission,
        execution_context=execution_context,
        policy=policy,

        restrict_mode=restrict_mode,

        execution_receipt=execution_receipt,
        provenance=provenance,
    )

    package.validate()

    return package
