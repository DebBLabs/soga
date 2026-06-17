from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List


SECTION_NAMES = [
    "Scenario",
    "Objective",
    "Preferences",
    "Hard Constraints",
    "Fallback Behaviors",
    "Governance Questions",
    "Notes",
]


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def title_from_markdown(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# Reference Mission:"):
            return line.replace("# Reference Mission:", "").strip()
    return "Untitled Reference Mission"


def section_text(text: str, section: str) -> str:
    pattern = rf"^## {re.escape(section)}\s*$"
    lines = text.splitlines()

    start = None
    for index, line in enumerate(lines):
        if re.match(pattern, line):
            start = index + 1
            break

    if start is None:
        return ""

    collected = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        collected.append(line)

    return "\n".join(collected).strip()


def bullet_list(block: str) -> List[str]:
    items = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def paragraph(block: str) -> str:
    lines = [
        line.strip()
        for line in block.splitlines()
        if line.strip()
        and not line.strip().startswith("- ")
        and line.strip() != "---"
    ]
    return " ".join(lines).strip()


def build_canonical_mission(path: Path) -> Dict:
    text = read_markdown(path)
    title = title_from_markdown(text)
    mission_slug = slugify(title)

    return {
        "mission_id": f"mission-{mission_slug}",
        "title": title,
        "source_reference_mission": str(path),
        "subject": {
            "subject_id": "subject-001",
            "display_name": "Subject",
        },
        "subject_agent": {
            "agent_id": "subject_agent",
            "role": "agent_acting_on_behalf_of_subject",
        },
        "scenario": paragraph(section_text(text, "Scenario")),
        "objective": paragraph(section_text(text, "Objective")),
        "preferences": bullet_list(section_text(text, "Preferences")),
        "hard_constraints": bullet_list(section_text(text, "Hard Constraints")),
        "fallback_behaviors": bullet_list(section_text(text, "Fallback Behaviors")),
        "governance_questions": bullet_list(section_text(text, "Governance Questions")),
        "notes": paragraph(section_text(text, "Notes")),
        "governance": {
            "subject_agency_state": "ACTIVE",
            "evaluate_at_execution": True,
        },
        "metadata": {
            "builder": "reference_mission_builder",
            "status": "generated_from_reference_mission_v0_1",
        },
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python3 -m builders.reference_mission_builder missions/reference/birthday_gift.md"
        )

    input_path = Path(sys.argv[1])
    mission = build_canonical_mission(input_path)

    output_path = Path("generated/missions") / f"{mission['mission_id']}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(mission, indent=2) + "\n", encoding="utf-8")

    print("Reference Mission Builder")
    print("=========================")
    print(f"input:  {input_path}")
    print(f"output: {output_path}")
    print()
    print(json.dumps(mission, indent=2))


if __name__ == "__main__":
    main()
