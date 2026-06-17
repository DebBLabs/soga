class ConversationEngine:
    """
    Conducts the intake conversation.

    Future:
        Question
            ↓
        Human Answer
            ↓
        Update MWR
            ↓
        Revalidate
    """

    def next_question(
        self,
        questions,
    ):

        if not questions:
            return None

        return questions[0]
