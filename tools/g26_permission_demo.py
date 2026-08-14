#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aauth_permission import PermissionService


def main() -> None:
    service = PermissionService(deferred_response_supported=True)
    mission = service.approve_mission(
        approver="https://person.example/alice",
        agent="https://agent.example/caregiver",
        approved_at="2026-08-14T14:00:00+00:00",
        approved_tools=[{"name": "schedule_visit", "description": "Schedule a caregiver visit"}],
        description="Arrange the subject's approved caregiver visit.",
    )
    common = {
        "action": "schedule_visit",
        "mission": {"approver": mission.approver, "s256": mission.s256},
        "agent": mission.agent,
    }
    independent = service.permission({
        **common,
        "subject": {"subject_id": "subject-001", "subject_agency_state": "INDEPENDENT"},
    })
    supervised = service.permission({
        **common,
        "subject": {"subject_id": "subject-001", "subject_agency_state": "SUPERVISED"},
    })
    record = {
        "canonical_test": "same action + same mission + different subject agency state",
        "mission_s256": mission.s256,
        "action": common["action"],
        "independent": {"http_status": independent[0], "response": independent[1]},
        "supervised": {"http_status": supervised[0], "response": supervised[1]},
        "restrict_path_exercised": "deferred response",
        "mission_log": [as_json(entry) for entry in service.mission_log.entries(mission.s256)],
    }
    print(json.dumps(record, indent=2, sort_keys=True))


def as_json(entry):
    return {
        "sequence": entry.sequence,
        "recorded_at": entry.recorded_at,
        "kind": entry.kind,
        "actor": entry.actor,
        "attribution": entry.attribution,
        "payload": entry.payload,
    }


if __name__ == "__main__":
    main()
