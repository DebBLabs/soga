from intake.mission_working_representation import (
    MissionWorkingRepresentation,
)


def _contains_any(text, terms):
    return any(term in text for term in terms)


def glean(
    human_intent: str,
    subject_representation=None,
    mission_context=None,
    sector_knowledge=None,
):
    """
    Representation only.

    No governance reasoning.
    """

    mwr = MissionWorkingRepresentation(
        original_request=human_intent,
    )

    mwr.candidate_observations.append(human_intent)

    text = human_intent.lower()

    # Subject candidate
    if _contains_any(text, ["my ", " me ", " i "]):
        mwr.inferred_subject = {
            "candidate": "me",
        }
    else:
        mwr.unresolved_questions.append(
            "subject_not_identified"
        )

    # Delegate candidates
    delegates = [
        "niece",
        "lawyer",
        "assistant",
        "caregiver",
        "agent",
    ]

    for delegate in delegates:
        if delegate in text:
            mwr.inferred_delegates.append(
                {
                    "candidate": delegate,
                }
            )

    if not mwr.inferred_delegates:
        mwr.unresolved_questions.append(
            "delegate_not_identified"
        )

    # Allowed action candidates
    if _contains_any(text, ["schedule", "book"]):
        if _contains_any(text, ["appointment", "appointments"]):
            mwr.inferred_allowed_actions.append(
                "schedule_appointment"
            )

    if _contains_any(text, ["buy", "purchase", "order"]):
        mwr.inferred_allowed_actions.append(
            "purchase_item"
        )

    if _contains_any(text, ["rebook", "change travel"]):
        mwr.inferred_allowed_actions.append(
            "rebook_travel"
        )

    # Forbidden action candidates
    if "may not authorize treatment" in text:
        mwr.inferred_forbidden_actions.append(
            "authorize_treatment"
        )

    if "may not approve" in text and "upgrade" in text:
        mwr.inferred_forbidden_actions.append(
            "approve_unnecessary_upgrade"
        )

    if "may not spend over" in text:
        mwr.inferred_forbidden_actions.append(
            "spend_over_budget"
        )

    # Bounds candidates
    if "cardiology" in text:
        mwr.inferred_bounds["domain"] = "cardiology"

    if "appointment" in text:
        mwr.inferred_bounds["mission_type"] = (
            "appointment_management"
        )

    if not mwr.inferred_allowed_actions:
        mwr.unresolved_questions.append(
            "allowed_action_not_identified"
        )

    mwr.sector_knowledge_used = sector_knowledge or []

    return mwr
