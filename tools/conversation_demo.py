from engines.conversation_engine import (
    ConversationEngine,
)

engine = ConversationEngine()

questions = [
    {
        "question":
            "What authority is delegated "
            "to the identified representative?",
        "scope":
            "mission_only",
    }
]

print()
print("CONVERSATION DEMO")
print("=================")
print()

q = engine.next_question(
    questions
)

print(q)
