from engines.execution_orchestrator import (
    ExecutionOrchestrator,
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

cmr = (
    MissionIntakeEngine()
    .run(
        request,
        answers,
    )
)

subject_id = cmr["subject"]["subject_id"]

standing_capabilities = (
    SubjectCapabilityLoader()
    .load(subject_id)
)

result = (
    ExecutionOrchestrator()
    .run(
        cmr,
        standing_capabilities,
        available_evidence,
    )
)

print()
print("EXECUTION ORCHESTRATOR DEMO")
print("===========================")
print()

print("Mission:")
print(result["mission_id"])
print()

print("Subject capabilities loaded from profile:")
for capability in standing_capabilities:
    print(
        "-",
        capability["capability_id"],
        capability["capability"],
        capability["evidence_type"],
        capability["status"],
    )
print()

for receipt in result["receipts"]:

    print("STEP")
    print("----")
    print(receipt["step_id"])
    print("action:", receipt["action"])
    print("decision:", receipt["decision"])
    print("execution_status:", receipt["execution_status"])
    print("reason:", receipt["reason"])
    print()
