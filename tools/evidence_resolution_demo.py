from pprint import pprint

from engines.authority_requirement_mapper import (
    AuthorityRequirementMapper,
)
from engines.evidence_resolver import EvidenceResolver
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

requirements = (
    AuthorityRequirementMapper()
    .map(cmr)
)

resolved = (
    EvidenceResolver()
    .resolve(
        requirements,
        available_evidence,
        standing_capabilities,
    )
)

print()
print("EVIDENCE RESOLUTION DEMO")
print("========================")
print()

print("AVAILABLE EVIDENCE")
print("------------------")
pprint(available_evidence)
print()

print("STANDING CAPABILITIES")
print("---------------------")
pprint(standing_capabilities)
print()

print("RESOLUTION")
print("----------")
pprint(resolved)
