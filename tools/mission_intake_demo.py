from intake.mission_intake_engine import MissionIntakeEngine

engine = MissionIntakeEngine()

result = engine.intake(
    "My niece may schedule my cardiology appointments but may not authorize treatment.",
    sector_knowledge=["Healthcare"],
)

print(result)
