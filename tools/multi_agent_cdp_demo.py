from pprint import pprint

from advisory.agent_evidence import AgentEvidence
from advisory.runtime_advisory_inputs import RuntimeAdvisoryInputs
from advisory.advisory_dimension_evidence import (
    advisory_dimension_review_signals,
)
from intake.mission_intake_engine import MissionIntakeEngine
from engines.soga_runtime_engine import SOGARuntimeEngine


HUMAN_INTENT = (
    "My niece may schedule my cardiology appointments "
    "but may not authorize treatment."
)


def main():
    intake = MissionIntakeEngine().intake(
        HUMAN_INTENT,
        sector_knowledge=["Healthcare"],
    )

    if intake["status"] != "PASS":
        raise RuntimeError(intake)

    cmr_template = intake["cmr"]

    cmr = {
        "mission_id": cmr_template.mission_id,
        "title": cmr_template.references.get("title"),
        "objective": cmr_template.objective,
        "subject": {
            "subject_id": cmr_template.subject_id,
            "display_name": "Subject",
        },
        "actors": cmr_template.references.get("actors", []),
        "resources": cmr_template.references.get("resources", []),
        "allowed_actions": cmr_template.allowed_actions,
        "forbidden_actions": cmr_template.forbidden_actions,
        "bounds": cmr_template.bounds,
        "governance": {
            "evaluate_at_execution": True,
        },
    }

    advisory = RuntimeAdvisoryInputs()

    advisory.add(
        AgentEvidence(
            agent_id="agent_a",
            evidence_type="subject_agency_state",
            evidence_content={
                "observation": "subject appears capable",
            },
            provenance={
                "source": "assessment_a",
            },
            confidence=0.92,
        )
    )

    advisory.add(
        AgentEvidence(
            agent_id="agent_b",
            evidence_type="subject_agency_state",
            evidence_content={
                "observation": "subject may be impaired",
                "disagreement": True,
            },
            provenance={
                "source": "assessment_b",
            },
            confidence=0.81,
        )
    )

    runtime = {
        "subject_agency_state": "Independent",
        "reachability": "Reachable",
        "advisory_inputs": {
            "advisory_agents": advisory.to_list(),
        },
        "provenance": {
            "governance_source": "SOGA-RuntimeGovernanceEngine",
            "advisory_agents": advisory.to_list(),
        },
    }

    review_signals = advisory_dimension_review_signals(
        runtime
    )

    result = SOGARuntimeEngine().execute_cmr(
        cmr=cmr,
        available_evidence=[
            {
                "evidence_id": "appointment-calendar-access",
                "supports": "schedule_appointment",
            }
        ],
        runtime=runtime,
    )

    packages = [
        package.to_dict()
        for package in result[
            "canonical_decision_packages"
        ]
    ]

    print()
    print("SOGA MULTI-AGENT CDP DEMO")
    print("=========================")
    print()

    print("Human Intent")
    print("------------")
    print(HUMAN_INTENT)
    print()

    print("Generated CMR")
    print("-------------")
    pprint(cmr)
    print()

    print("Advisory Agent Inputs")
    print("---------------------")
    pprint(runtime["advisory_inputs"])
    print()

    print("Review Signals")
    print("--------------")
    pprint(review_signals)
    print()

    print("Governance Decisions")
    print("--------------------")
    pprint(result["governance_decisions"])
    print()

    print("Canonical Decision Packages")
    print("---------------------------")
    pprint(packages)
    print()

    print("Decision Package Count")
    print("----------------------")
    print(len(packages))


if __name__ == "__main__":
    main()
