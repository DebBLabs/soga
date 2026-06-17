import json

from builders.mission_builder import build_mission_template
from engines.mission_intake_engine import MissionIntakeEngine

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

mission = build_mission_template(
    cmr
)

print()
print("INTAKE TO MISSION TEMPLATE DEMO")
print("===============================")
print()

print("CMR")
print("---")
print(json.dumps(cmr, indent=2))
print()

print("MISSION TEMPLATE")
print("----------------")
print(json.dumps(mission.to_dict(), indent=2))
