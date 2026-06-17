from engines.intake_engine import MissionIntakeEngine
from pprint import pprint

engine = MissionIntakeEngine()

request = (
    "My niece should manage my medical appointments "
    "while I am traveling."
)

result = engine.inspect(request)

print("Mission Intake Glean Proof")
print("==========================")
print("Request:")
print(request)
print()

print("Detected sectors:")
for s in result["detected_sectors"]:
    print(" -", s)

print()
print("Gleaned:")
pprint(result["gleaned"])

print()
print("Unresolved:")
for item in result["unresolved"]:
    print(" -", item)
