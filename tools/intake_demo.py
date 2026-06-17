from pprint import pprint

from engines.orchestrator import (
    MissionIntakeOrchestrator,
)

request = (
    "My niece should manage my medical "
    "appointments while I am traveling."
)

orchestrator = MissionIntakeOrchestrator()

result = orchestrator.run(request)

print()
print("=" * 60)
print("MISSION INTAKE REASONING DEMO")
print("=" * 60)
print()

print("STEP 1 — CURRENT REQUEST")
print("------------------------")
print(result.request)
print()

print("STEP 2 — CANDIDATE OBSERVATIONS")
print("-------------------------------")
pprint(result.candidate_observations)
print()

print("STEP 3 — GLEAN")
print("----------------")
print("Inputs:")
print("  ✓ Candidate Observations")
print("  ✓ Subject Representation")
print("  ✓ Mission Context")
print("  ✓ Sector Knowledge")
print()

print("STEP 4 — MISSION WORKING REPRESENTATION")
print("---------------------------------------")
pprint(result.mission_working_representation)
print()

print("STEP 5 — VALIDATION")
print("-------------------")
pprint(result.validation)
print()

print("STEP 6 — QUESTIONS")
print("------------------")
pprint(result.questions)
print()

print("=" * 60)
print("Future:")
print("MWR -> Confirmation -> Subject Representation")
print("MWR -> CMR -> SOGA Runtime")
print("=" * 60)
