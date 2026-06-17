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

print()
print("=" * 72)
print("MISSION VERIFICATION WALKTHROUGH")
print("=" * 72)
print()

print("1. HUMAN REQUEST")
print("----------------")
print(request)
print()

print("2. MISSION INTAKE")
print("-----------------")
print("The intake engine asks for missing authority boundaries.")
print()
print("Answer supplied:")
print(answers[0])
print()

cmr = MissionIntakeEngine().run(
    request,
    answers,
)

print("3. CANONICAL MISSION REPRESENTATION")
print("------------------------------------")
print("The internal intake process is hidden.")
print("Public output is the CMR.")
print()
pprint(cmr)
print()

print("4. EXECUTION PLAN")
print("-----------------")
print("The CMR is decomposed into execution steps.")
print()

plan = ExecutionPlanBuilder().build(
    cmr
)

pprint(plan)
print()

print("5. AUTHORITY REQUIREMENTS")
print("-------------------------")
print("Each step is mapped to required authority.")
print("This is not protocol selection.")
print()

requirements = AuthorityRequirementMapper().map(
    cmr
)

pprint(requirements)
print()

print("6. AVAILABLE EVIDENCE")
print("---------------------")
print("Evidence may come from confirmation, standing capabilities,")
print("tokens, credentials, legal documents, or future mechanisms.")
print()

print("Available evidence:")
pprint(available_evidence)
print()

print("Standing capabilities:")
pprint(standing_capabilities)
print()

print("7. EVIDENCE RESOLUTION")
print("----------------------")
print("Each step is checked against available evidence and capabilities.")
print()

resolution = EvidenceResolver().resolve(
    requirements,
    available_evidence,
    standing_capabilities,
)

pprint(resolution)
print()

print("8. INTERPRETATION")
print("-----------------")
for item in resolution:
    print(
        f"{item['step_id']}: "
        f"{item['action']} -> {item['status']}"
    )

print()
print("=" * 72)
print("END")
print("=" * 72)
