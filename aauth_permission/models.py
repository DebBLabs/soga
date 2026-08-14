from __future__ import annotations

import hashlib
import json
import base64
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


@dataclass(frozen=True)
class ApprovedTool:
    name: str
    description: str


@dataclass(frozen=True)
class Mission:
    """Native AAuth mission value; immutable after approval."""

    approver: str
    agent: str
    approved_at: str
    approved_tools: tuple[ApprovedTool, ...]
    description: str
    s256: str

    @classmethod
    def approve(
        cls,
        *,
        approver: str,
        agent: str,
        approved_tools: Sequence[Mapping[str, str]],
        description: str,
        approved_at: str | None = None,
    ) -> "Mission":
        timestamp = approved_at or datetime.now(timezone.utc).isoformat()
        tools = tuple(
            ApprovedTool(name=item["name"], description=item["description"])
            for item in approved_tools
        )
        canonical = {
            "agent": agent,
            "approved_at": timestamp,
            "approved_tools": [asdict(tool) for tool in tools],
            "approver": approver,
            "description": description,
        }
        return cls(
            approver=approver,
            agent=agent,
            approved_at=timestamp,
            approved_tools=tools,
            description=description,
            s256=base64.urlsafe_b64encode(
                hashlib.sha256(_canonical_json(canonical)).digest()
            ).decode("ascii").rstrip("="),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "approver": self.approver,
            "agent": self.agent,
            "approved_at": self.approved_at,
            "approved_tools": [asdict(tool) for tool in self.approved_tools],
            "description": self.description,
            "s256": self.s256,
        }


@dataclass(frozen=True)
class MissionLogEntry:
    sequence: int
    recorded_at: str
    kind: str
    actor: str
    attribution: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ProvisionalG26ApprovalEvidence:
    """Temporary G26 evidence; must converge on canonical Stage Gate evidence."""

    pending_id: str
    evaluation_reference: str
    mission_s256: str
    action: str
    originating_soga_decision: str
    constraint_reference: str
    restrict_path: str
    required_evidence: str
    authority_reference: str
    asserted_by: str
    person_server_authenticated_assertion: bool
    holder_attribution_asserted: bool
    human_attribution: str | None
    result: str
    recorded_at: str
    provenance: str
    reevaluation_reference: str | None = None
    reevaluation_result: str | None = None
    evidence_schema: str = "provisional-g26-approval-evidence-v1"
    convergence_obligation: str = (
        "future-canonical-stage-gate-clearance-evidence-schema"
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MissionLog:
    """Append-only in-memory log used by the G26 mock Person Server."""

    def __init__(self) -> None:
        self._entries: dict[str, list[MissionLogEntry]] = {}

    def append(
        self,
        mission_s256: str,
        *,
        kind: str,
        actor: str,
        attribution: str,
        payload: Mapping[str, Any],
    ) -> MissionLogEntry:
        entries = self._entries.setdefault(mission_s256, [])
        entry = MissionLogEntry(
            sequence=len(entries) + 1,
            recorded_at=datetime.now(timezone.utc).isoformat(),
            kind=kind,
            actor=actor,
            attribution=attribution,
            payload=dict(payload),
        )
        entries.append(entry)
        return entry

    def entries(self, mission_s256: str) -> tuple[MissionLogEntry, ...]:
        return tuple(self._entries.get(mission_s256, ()))
