from __future__ import annotations


def advisory_dimension_review_signals(runtime):
    """
    Identifies dimensions requiring additional review based on
    advisory evidence.

    Evidence only. No governance determination.
    """

    advisory_inputs = runtime.get(
        "advisory_inputs",
        {},
    )

    agents = advisory_inputs.get(
        "advisory_agents",
        [],
    )

    review = {}

    for evidence in agents:

        dimension = evidence.get(
            "evidence_type"
        )

        content = evidence.get(
            "evidence_content",
            {}
        )

        if not (
            content.get("disagreement")
            or content.get("uncertain")
            or content.get("contradicts")
        ):
            continue

        if dimension not in review:
            review[dimension] = {
                "reason": "agent_disagreement",
                "contributors": [],
            }

        review[dimension][
            "contributors"
        ].append(
            evidence.get("agent_id")
        )

    return review
