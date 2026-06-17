from pprint import pprint

from engines.persistence_router import (
    PersistenceRouter,
)

router = PersistenceRouter()

question = {
    "question":
        "Preferred pharmacy?",
    "scope":
        "subject_persistent",
}

answer = "CVS"

result = router.route(
    question,
    answer,
)

print()
print("PERSISTENCE ROUTER DEMO")
print("=======================")
print()

pprint(result)
