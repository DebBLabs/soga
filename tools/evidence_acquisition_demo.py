from pprint import pprint

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

standing_capabilities = (
    SubjectCapabilityLoader()
    .load(
        cmr["subject"]["subject_id"]
    )
)

execution = MissionExecutionEngine().execute(
    cmr,
    standing_capabilities,
    available_evidence,
)

acquisition = EvidenceAcquisitionEngine().acquire(
    execution["step_verdicts"],
    execution["evidence_resolution"],
)

print()
print("EVIDENCE ACQUISITION DEMO")
print("=========================")
print()

print("STEP VERDICTS")
print("-------------")
pprint(execution["step_verdicts"])
print()

print("ACQUISITION")
print("-----------")
pprint(acquisition)
