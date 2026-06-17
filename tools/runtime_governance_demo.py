from pprint import pprint

from engines.runtime_governance_engine import (
    RuntimeGovernanceEngine,
)
from engines.runtime_acquisition_planner import (
    RuntimeAcquisitionPlanner,
)
from engines.capability_gap_engine import (
    CapabilityGapEngine,
)
from engines.evidence_acquisition_engine import (
    EvidenceAcquisitionEngine,
)
from engines.mission_execution_engine import (
    MissionExecutionEngine,
)
from engines.mission_intake_engine import (
    MissionIntakeEngine,
)
from engines.subject_capability_loader import (
    SubjectCapabilityLoader,
)

request = (
    "My niece should manage my medical "
    "appointments while I am traveling."
)

answers = [
    (
        "May schedule appointments but "
        "may not authorize treatment."
    )
]

available_evidence = [
    {
        "type": "human_confirmation",
        "source": "intake_conversation",
    }
]

cmr = MissionIntakeEngine().run(
    request,
    answers,
)

capabilities = SubjectCapabilityLoader().load(
    cmr["subject"]["subject_id"]
)

execution = MissionExecutionEngine().execute(
    cmr,
    capabilities,
    available_evidence,
)

acquisition = EvidenceAcquisitionEngine().acquire(
    execution["step_verdicts"],
    execution["evidence_resolution"],
)

gap = CapabilityGapEngine().analyze(
    execution,
    acquisition,
)

runtime_plan = RuntimeAcquisitionPlanner().plan(
    gap
)

decisions = RuntimeGovernanceEngine().evaluate(
    runtime_plan
)

print()
print("RUNTIME GOVERNANCE DEMO")
print("=======================")
print()

pprint(decisions)
