from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from verify.mission_template import MissionLifecycle, MissionTemplate


def load_mission_file(path: str | Path) -> Dict[str, Any]:
    mission_path = Path(path)
    with mission_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_mission_template(data: Dict[str, Any]) -> MissionTemplate:
    subject = data.get("subject", {})
    governance = data.get("governance", {})

    metadata = {
        "builder": "mission_builder",
        "evaluate_at_execution": governance.get(
            "evaluate_at_execution",
            True,
        ),
    }

    if "subject_agency_state" in governance:
        metadata["subject_agency_state"] = governance[
            "subject_agency_state"
        ]

    return MissionTemplate(
        mission_id=str(data["mission_id"]),
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id=str(
            subject.get("subject_id", "subject-unknown")
        ),
        objective=str(data.get("objective", "")),
        allowed_actions=list(
            data.get("allowed_actions", [])
        ),
        forbidden_actions=list(
            data.get("forbidden_actions", [])
        ),
        bounds=dict(data.get("bounds", {})),
        references={
            "title": data.get("title"),
            "actors": data.get("actors", []),
            "resources": data.get("resources", []),
        },
        metadata=metadata,
    )


def mission_file_to_template(path: str | Path) -> MissionTemplate:
    return build_mission_template(load_mission_file(path))
