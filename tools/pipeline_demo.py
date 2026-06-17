from engines.orchestrator import MissionIntakeOrchestrator

request = (
    "My niece should manage my medical "
    "appointments while I am traveling."
)

print()
print("=" * 70)
print("SOGA MISSION INTAKE PIPELINE")
print("=" * 70)
print()

print("REQUEST")
print("-------")
print(request)
print()

orchestrator = MissionIntakeOrchestrator()

result = orchestrator.run(request)

print("CANDIDATE OBSERVATIONS")
print("----------------------")

for obs in result.candidate_observations:
    print(
        f"✓ {obs['semantic_type']}: "
        f"{obs['value']} "
        f"(confidence={obs['confidence']})"
    )

print()

print("MISSION WORKING REPRESENTATION")
print("------------------------------")

mwr = result.mission_working_representation

print("Candidate Observations:", len(mwr.candidate_observations))
print("Subject Representation:", mwr.subject_representation)
print("Mission Context:", mwr.mission_context)
print("Sector Knowledge:", mwr.sector_knowledge)
print()

validation = result.validation

print("VALIDATION")
print("----------")
print("Status:", validation.status)
print()

for finding in validation.findings:

    print(
        f"{finding['gate']}: "
        f"{finding['status']}"
    )

    print(
        f"    {finding['reason']}"
    )

print()

print("QUESTIONS")
print("---------")

if not validation.questions:
    print("(none)")
else:
    for i, q in enumerate(validation.questions, 1):
        print(f"{i}. {q['question']}")
        print(f"   scope: {q['scope']}")
        print()

print("=" * 70)
print("Future")
print("=" * 70)
print("""
Confirmation
      │
      ▼
Subject Representation
      │
      ▼
Canonical Mission Representation
      │
      ▼
SOGA Runtime
""")
