from pprint import pprint

from engines.evidence_justification_engine import (
    EvidenceJustificationEngine,
)
from engines.evidence_selection_engine import (
    EvidenceSelectionEngine,
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

selection = EvidenceSelectionEngine().select(
    execution["evidence_resolution"]
)

justification = EvidenceJustificationEngine().justify(
    selection
)

print()
print("EVIDENCE JUSTIFICATION DEMO")
print("===========================")
print()

pprint(justification)
