from pprint import pprint

from engines.authority_requirement_mapper import (
    AuthorityRequirementMapper,
)
from engines.evidence_resolver import EvidenceResolver
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

available_evidence = [
    {
        "type": "human_confirmation",
        "source": "intake_conversation",
    },
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

requirements = AuthorityRequirementMapper().map(
    cmr
)

resolution = EvidenceResolver().resolve(
    requirements,
    available_evidence,
    standing_capabilities,
)

print()
print("MISSION VERIFICATION DEMO")
print("=========================")
print()

print("MISSION")
print("-------")
pprint(cmr)
print()

print("EXECUTION PLAN")
print("--------------")
pprint(plan)
print()

print("AUTHORITY REQUIREMENTS")
print("----------------------")
pprint(requirements)
print()

print("VERIFICATION")
print("------------")
pprint(resolution)
