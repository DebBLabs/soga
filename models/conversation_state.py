from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversationState:

    questions: list[dict[str, Any]] = field(
        default_factory=list
    )

    answers: list[dict[str, Any]] = field(
        default_factory=list
    )

    status: str = "WORKING"
