from engines.validator import Validator
from engines.conversation_engine import (
    ConversationEngine,
)


class IntakeLoop:
    """
    Iteratively refines a Mission Working
    Representation until no further
    questions remain.
    """

    def __init__(self):

        self.validator = Validator()
        self.conversation = (
            ConversationEngine()
        )

    def step(
        self,
        mwr,
    ):

        validation = self.validator.evaluate(
            mwr
        )

        question = self.conversation.next_question(
            validation.questions
        )

        return {
            "validation": validation,
            "next_question": question,
        }
