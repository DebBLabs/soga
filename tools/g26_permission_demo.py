#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aauth_permission import PermissionService


def as_json(entry):
    return {
        "sequence": entry.sequence,
        "recorded_at": entry.recorded_at,
        "kind": entry.kind,
        "actor": entry.actor,
        "attribution": entry.attribution,
        "payload": entry.payload,
    }


def main() -> None:
    fixture = json.loads(
        (Path(__file__).resolve().parents[1] / "tests/fixtures/missions/caregiver_discharge_followup.json").read_text()
    )
    # Demonstration configuration only; this is not a caregiver liveness policy.
    service = PermissionService(pending_expiry_seconds=300)
    mission = service.approve_mission(
        approver="https://person.example/alice",
        agent="https://agent.example/caregiver",
        approved_at="2026-08-14T14:00:00+00:00",
        approved_tools=[{"name": "schedule_appointment", "description": "Schedule appointment"}],
        description=fixture["objective"],
    )
    service.authorize_mission_policy(mission.s256, fixture["constraints"])
    common = {
        "request_id": "canonical-caregiver-permission-001",
        "action": "schedule_appointment",
        "mission": {"approver": mission.approver, "s256": mission.s256},
        "agent": mission.agent,
        "policy": fixture["constraints"],
    }
    independent = service.permission({
        **common,
        "subject": {"subject_id": fixture["subject_id"], "subject_agency_state": "INDEPENDENT"},
    })
    supervised = service.permission({
        **common,
        "subject": {"subject_id": fixture["subject_id"], "subject_agency_state": "SUPERVISED"},
    })
    pending_id = supervised[1]["pending_id"]
    before_approval = service.pending[pending_id]["originating_soga_decision"]["governance_determination"]
    service.record_approval(
        pending_id,
        result="approve",
        asserted_by=service.person_server_id,
        person_server_authenticated_assertion=True,
        authority_reference="authority-caregiver-001",
        required_evidence="supervisor_confirmation",
        constraint_reference="gate-supervision-required",
        holder_attribution_asserted=True,
        human_attribution="Beth",
    )
    terminal = service.poll(pending_id, agent=mission.agent)
    record = {
        "canonical_test": "same action + same mission + different subject agency state",
        "mission_s256": mission.s256,
        "action": common["action"],
        "independent": {"http_status": independent[0], "response": independent[1]},
        "supervised_before_approval": {
            "subject_agency_state": "SUPERVISED",
            "soga_decision": before_approval,
            "http_status": supervised[0],
            "response": supervised[1],
        },
        "approval_mechanism": {
            "restrict_path": "HOLDING",
            "requirement": "approval",
            "required_evidence": "supervisor_confirmation",
            "authority_reference": "authority-caregiver-001",
            "evidence": service.pending[pending_id]["approval_evidence"],
        },
        "supervised_after_approval": {
            "subject_agency_state": "SUPERVISED",
            "soga_reevaluation": service.pending[pending_id]["reevaluation"]["governance_determination"],
            "http_status": terminal[0],
            "response": terminal[1],
        },
        "mission_log": [as_json(entry) for entry in service.mission_log.entries(mission.s256)],
    }
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
