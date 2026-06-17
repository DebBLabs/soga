from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ExecutionContext:
    """
    P13 Execution interface contract.

    This is a boundary object that can later be backed by:
    - stub (default)
    - misty adapter
    - cloud function / container app
    - local tool runner
    without changing the event envelope shape.
    """
    version: str
    provider: str  # stub | misty | azure | local | ...
    output_text: str
    raw: Dict[str, Any]
    timestamp: Optional[str] = None  # ISO8601 Z


def _now_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def build_execution_context(
    *,
    provider: str = "stub",
    output_text: str = "STUB: execution provider not yet wired (P13).",
    raw: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Return the Execution block to embed in the event record.

    P13 default remains stub (no external actions).
    """
    ctx = ExecutionContext(
        version="execution.v0",
        provider=provider,
        output_text=output_text,
        raw=raw or {},
        timestamp=_now_iso_z(),
    )
    return asdict(ctx)