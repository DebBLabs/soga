from pprint import pprint

from engines.orchestrator import (
    MissionIntakeOrchestrator,
)
from engines.confirmation_engine import (
    ConfirmationEngine,
)
from engines.persistence_router import (
    PersistenceRouter,
)

request = (
    "My niece should manage my medical "
    "appointments while I am traveling."
)

print()
print("=" * 70)
print("MISSION INTAKE LIFECYCLE")
print("=" * 70)
print()

orchestrator = MissionIntakeOrchestrator()

result = orchestrator.run(request)

print("REQUEST")
print("-------")
print(request)
print()

print("QUESTIONS")
print("---------")

for i, q in enumerate(result.questions, 1):
    print(f"{i}. {q['question']}")
    print(f"   scope={q['scope']}")
print()

confirmation = ConfirmationEngine()
router = PersistenceRouter()

for q in result.questions:

    answer = (
        "May schedule appointments "
        "but may not authorize treatment."
    )

    confirmed = confirmation.process(
        q,
        answer,
    )

    routed = router.route(
        q,
        answer,
    )

    print("ANSWER")
    print("------")
    print(answer)
    print()

    print("CONFIRMATION")
    pprint(confirmed)
    print()

    print("PERSISTENCE")
    pprint(routed)
    print()

print("=" * 70)
