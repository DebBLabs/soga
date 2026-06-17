from builders.mission_builder import build_mission_template
from builders.protocol_projection import (
    mission_to_aauth_artifact,
)
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

mission = build_mission_template(cmr)

artifact = mission_to_aauth_artifact(
    mission
)

print()
print("END TO END DEMO")
print("================")
print()
print("Mission ID:")
print(mission.mission_id)
print()
print("Generated AAuth artifact:")
print(artifact)
