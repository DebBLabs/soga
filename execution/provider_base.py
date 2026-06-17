from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol


@dataclass
class ExecutionRequest:
    prompt: str
    context: Dict[str, Any]
    model_hint: Optional[str] = None


@dataclass
class ExecutionResult:
    output_text: str
    provider: str
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Dict[str, Any]] = None


class ExecutionProvider(Protocol):
    name: str

    def execute(self, req: ExecutionRequest) -> ExecutionResult:
        ...