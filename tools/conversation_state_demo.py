from pprint import pprint

from models.conversation_state import (
    ConversationState,
)

state = ConversationState()

state.questions.append(
    {
        "question":
            "What authority is delegated?",
        "scope":
            "mission_only",
    }
)

state.answers.append(
    {
        "answer":
            "May schedule appointments only.",
    }
)

print()
print("CONVERSATION STATE")
print("==================")
print()

pprint(state)
