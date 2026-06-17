from intake.mission_working_representation import (
    MissionWorkingRepresentation,
)


def validate(
    mwr: MissionWorkingRepresentation,
):
    """
    Validation only.

    No governance reasoning.
    """

    findings = []

    if not mwr.original_request.strip():
        findings.append("missing_request")

    if not mwr.candidate_observations:
        findings.append("missing_candidate_observations")

    if not mwr.inferred_subject:
        findings.append("missing_subject")

    if not mwr.inferred_delegates:
        findings.append("missing_delegate")

    if not mwr.inferred_allowed_actions:
        findings.append("missing_allowed_action")

    if len(
        set(mwr.inferred_allowed_actions)
        &
        set(mwr.inferred_forbidden_actions)
    ):
        findings.append("contradictory_actions")

    if mwr.unresolved_questions:
        findings.append(
            {
                "unresolved_questions":
                    mwr.unresolved_questions,
            }
        )

    if findings:
        return {
            "status": "FINDING",
            "findings": findings,
        }

    return {
        "status": "PASS",
        "findings": [],
    }
