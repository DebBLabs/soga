from __future__ import annotations

from typing import Any, Dict

from verify.mission_template import MissionTemplate


def mission_to_aauth_artifact(mission: MissionTemplate) -> Dict[str, Any]:
    artifact = {
        "authorization_details": [
            {
                "type": "aauth_mission_statement",
                "mission_id": mission.mission_id,
                "subject_id": mission.subject_id,
                "actions": mission.allowed_actions,
                "description": mission.objective,
                "soga_constraints": {
                    "forbidden_conditions": mission.forbidden_actions,
                    "bounds": mission.bounds,
                },
            }
        ],
        "source": "mission_builder_aauth_projection",
    }

    if "subject_agency_state" in mission.metadata:
        artifact["subject_agency_state"] = (
            mission.metadata["subject_agency_state"]
        )

    return artifact


def mission_to_ucan_artifact(mission: MissionTemplate) -> Dict[str, Any]:
    action = (
        mission.allowed_actions[0]
        if mission.allowed_actions
        else "step1"
    )

    fct = {
        "mission_id": mission.mission_id,
        "subject_id": mission.subject_id,
        "objective": mission.objective,
    }

    if "subject_agency_state" in mission.metadata:
        fct["subject_agency_state"] = (
            mission.metadata["subject_agency_state"]
        )

    return {
        "ucan": {
            "iss": f"did:key:{mission.subject_id}",
            "aud": "did:key:delegated-agent",
            "jti": f"ucan-{mission.mission_id}",
            "att": [
                {
                    "with": "resource://mission/" + mission.mission_id,
                    "can": action,
                }
            ],
            "fct": fct,
        },
        "source": "mission_builder_ucan_projection",
    }


def mission_to_zcap_artifact(mission: MissionTemplate) -> Dict[str, Any]:
    action = (
        mission.allowed_actions[0]
        if mission.allowed_actions
        else "step1"
    )

    artifact = {
        "capability": {
            "@context": "https://w3id.org/security/v2",
            "id": f"urn:zcap:{mission.mission_id}",
            "type": "Capability",
            "controller": mission.subject_id,
            "parentCapability": "urn:zcap:root:mission-builder-demo",
            "invocationTarget": "resource://mission/" + mission.mission_id,
            "allowedAction": [action],
            "caveat": [
                {
                    "type": "SOGARuntimeGovernanceCaveat",
                    "forbidden_conditions": mission.forbidden_actions,
                    "bounds": mission.bounds,
                }
            ],
        },
        "mission_id": mission.mission_id,
        "source": "mission_builder_zcap_projection",
    }

    if "subject_agency_state" in mission.metadata:
        artifact["subject_agency_state"] = (
            mission.metadata["subject_agency_state"]
        )

    return artifact
