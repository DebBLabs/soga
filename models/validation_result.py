from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:

    status: str = "WORKING"

    findings: list[dict[str, Any]] = field(
        default_factory=list
    )

    questions: list[dict[str, Any]] = field(
        default_factory=list
    )
