from pprint import pprint

from engines.mission_intake_engine import (
    MissionIntakeEngine,
)
from engines.cmr_compiler import (
    CMRCompiler,
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

result = MissionIntakeEngine().run(
    request,
    answers,
)

cmr = CMRCompiler().compile(
    result["mwr"]
)

print()
print("CMR COMPILER DEMO")
print("=================")
print()

print("INTAKE STATUS")
print(result["status"])
print()

print("GENERATED CMR")
print("-------------")
pprint(cmr)
