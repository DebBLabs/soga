from intake.cmr_source import (
    cmr_from_human_intent,
    cmr_from_mission_file,
)


human_intent_cmr = cmr_from_human_intent(
    "My niece may schedule my cardiology appointments but may not authorize treatment.",
    sector_knowledge=["Healthcare"],
)

mission_file_cmr = cmr_from_mission_file(
    "missions/gift_purchase_mission.json",
)

print("CMR SOURCE DEMO")
print("===============")
print()

print("Human Intent -> CMR")
print("-------------------")
print(human_intent_cmr)
print()

print("Mission File -> CMR")
print("-------------------")
print(mission_file_cmr)
