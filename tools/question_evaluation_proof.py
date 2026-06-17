from engines.intake_engine import MissionIntakeEngine

engine = MissionIntakeEngine()

request = (
    "My niece should manage my medical appointments "
    "while I am traveling."
)

result = engine.inspect(request)

print("Mission Intake Question Evaluation Proof")
print("========================================")
print("Request:")
print(request)
print()

for sector, items in result["evaluated_questions"].items():
    print(sector.upper())
    print("-" * len(sector))
    for item in items:
        if item["status"] != "ASK":
            print(f"{item['status']:8} {item['id']:8} {item['question']}")
            print(f"         reason: {item['reason']}")
    print()
