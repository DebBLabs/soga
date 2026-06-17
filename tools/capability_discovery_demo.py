from pprint import pprint

from engines.capability_discovery_engine import (
    CapabilityDiscoveryEngine,
)
from engines.execution_plan_builder import (
    ExecutionPlanBuilder,
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

standing_capabilities = [
    {
        "capability_id": "cap-calendar-create-001",
        "provider": "calendar_service",
        "capability": "create_calendar_event",
        "evidence_type": "oauth_or_gnap_token",
        "status": "active",
    }
]

cmr = MissionIntakeEngine().run(
    request,
    answers,
)

plan = ExecutionPlanBuilder().build(
    cmr
)

discovery = CapabilityDiscoveryEngine().discover(
    plan,
    standing_capabilities,
)

print()
print("CAPABILITY DISCOVERY DEMO")
print("=========================")
print()

print("EXECUTION PLAN")
print("--------------")
pprint(plan)
print()

print("STANDING CAPABILITIES")
print("---------------------")
pprint(standing_capabilities)
print()

print("CAPABILITY DISCOVERY")
print("--------------------")
pprint(discovery)
