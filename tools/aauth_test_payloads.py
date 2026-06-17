from __future__ import annotations

from typing import Any, Dict


def build_aauth_mission_payload(subject_agency_state: str) -> Dict[str, Any]:
    return {
        "authorization_details": [
            {
                "type": "aauth_mission_statement",
                "mission_id": "mission-person-server-soga-001",
                "subject_id": "subject-001",
                "delegation_id": "del-person-server-soga-001",
                "agent_id": "agent-001",
                "person_server_id": "ps-001",
                "resource_id": "resource-001",
                "resource_ref": "resource://demo/step1",
                "actions": ["step1"],
                "r3_refs": ["r3-demo-step1"],
                "r3_granted": {
                    "actions": ["step1"],
                    "resource": "resource://demo/step1",
                },
                "r3_conditional": {
                    "requires_runtime_governance": True,
                },
                "soga_constraints": {
                    "supervision_required": True,
                    "restrict_if_subject_agency_state": [
                        "IMPAIRED",
                        "HELD",
                        "UNREACHABLE",
                    ],
                },
                "expires_at": "2026-12-31T12:00:00Z",
            }
        ],
        "subject_agency_state": subject_agency_state,
        "guest_present": False,
        "operator_present": True,
        "source": "person_server_soga_proof",
    }
