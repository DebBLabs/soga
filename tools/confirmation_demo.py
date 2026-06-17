from pprint import pprint

from engines.confirmation_engine import (
    ConfirmationEngine,
)

engine = ConfirmationEngine()

question = {
    "question":
        "What authority is delegated "
        "to the identified representative?",
    "scope": "mission_only",
}

answer = (
    "May schedule appointments "
    "but may not authorize treatment."
)

result = engine.process(
    question,
    answer,
)

print()
print("CONFIRMATION DEMO")
print("=================")
print()

print("QUESTION")
print(question["question"])
print()

print("ANSWER")
print(answer)
print()

print("ROUTING")
pprint(result)
