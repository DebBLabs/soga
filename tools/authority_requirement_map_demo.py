from pprint import pprint

from engines.authority_requirement_mapper import (
    AuthorityRequirementMapper,
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

cmr = MissionIntakeEngine().run(
    request,
    answers,
)

requirements = (
    AuthorityRequirementMapper()
    .map(cmr)
)

print()
print("AUTHORITY REQUIREMENT MAP DEMO")
print("==============================")
print()

print("CMR mission_id:")
print(cmr["mission_id"])
print()

print("STEP-LEVEL AUTHORITY REQUIREMENTS")
print("---------------------------------")
pprint(requirements)
