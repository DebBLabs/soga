from pprint import pprint

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

engine = MissionIntakeEngine()

cmr = engine.run(
    request,
    answers,
)

print()
print("MISSION INTAKE ENGINE DEMO")
print("==========================")
print()

print("PUBLIC OUTPUT: CMR")
print("------------------")
pprint(cmr)
print()

diagnostics = engine.run_diagnostics(
    request,
    answers,
)

print("DIAGNOSTIC STATUS")
print("-----------------")
print(diagnostics["status"])
print()
