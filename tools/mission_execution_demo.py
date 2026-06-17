from pprint import pprint

from engines.mission_execution_engine import (
    MissionExecutionEngine,
)
from engines.mission_intake_engine import (
    MissionIntakeEngine,
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

standing_capabilities = [
    {
        "capability_id":
            "cap-calendar-create-001",
        "provider":
            "calendar_service",
        "capability":
            "create_calendar_event",
        "evidence_type":
            "oauth_or_gnap_token",
        "status":
            "active",
    }
]

cmr = (
    MissionIntakeEngine()
    .run(
        request,
        answers,
    )
)

result = (
    MissionExecutionEngine()
    .execute(
        cmr,
        standing_capabilities,
        available_evidence,
    )
)

print()
print("MISSION EXECUTION DEMO")
print("======================")
print()

pprint(result)
