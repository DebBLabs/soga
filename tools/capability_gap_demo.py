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

gap_report = CapabilityGapEngine().analyze(
    execution,
    acquisition,
)

print()
print("CAPABILITY GAP DEMO")
print("===================")
print()

print("Mission:")
print(gap_report["mission_id"])
print()

for step in gap_report["steps"]:

    print("STEP")
    print("----")
    print(step["step_id"])
    print("action:", step["action"])
    print("verdict:", step["verdict"])
    print("required_capability:", step["required_capability"])
    print("capability_status:", step["capability_status"])
    print("matched_evidence:", step["matched_evidence"])
    print("acquisition_status:", step["acquisition_status"])
    print("reason:", step["reason"])
    print()

print("SUMMARY")
print("-------")
print("ready:", gap_report["summary"]["ready"])
print("blocked:", gap_report["summary"]["blocked"])
print("prohibited:", gap_report["summary"]["prohibited"])
print(
    "capabilities_to_acquire:",
    gap_report["summary"]["capabilities_to_acquire"],
)
