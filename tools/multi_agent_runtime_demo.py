from pprint import pprint

from advisory.agent_evidence import AgentEvidence
from advisory.runtime_advisory_inputs import RuntimeAdvisoryInputs
from advisory.advisory_dimension_evidence import (
    advisory_dimension_review_signals,
)

runtime = {}

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

runtime["advisory_inputs"] = {
    "advisory_agents": advisory.to_list(),
}

review = advisory_dimension_review_signals(runtime)

print()
print("MULTI-AGENT RUNTIME DEMO")
print("========================")
print()

print("Advisory Agent Inputs")
print("---------------------")
pprint(runtime["advisory_inputs"])

print()
print("Review Signals")
print("--------------")
pprint(sorted(review))

print()
print("Governance Principle")
print("--------------------")
print("Agents contributed evidence.")
print("No governance determination was produced.")
print("The PDP remains the sole governance authority.")
