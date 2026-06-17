from __future__ import annotations

import json
from pathlib import Path

from tools.run_generated_mission import run


MISSIONS_DIR = Path("generated/missions")

PROTOCOLS = {
    "1": "aauth",
    "2": "ucan",
    "3": "zcap",
}

SUBJECT_STATES = {
    "1": "ACTIVE",
    "2": "IMPAIRED",
    "3": "LAPSED",
}


def choose(label: str, options: list[str]) -> int:
    while True:
        value = input(f"{label}: ").strip()
        if value.isdigit():
            index = int(value)
            if 1 <= index <= len(options):
                return index - 1
        print("Please enter a valid number.")


def load_missions() -> list[Path]:
    return sorted(MISSIONS_DIR.glob("*.json"))


def print_missions(missions: list[Path]) -> None:
    print("Available Missions")
    print("------------------")
    for i, path in enumerate(missions, start=1):
        data = json.loads(path.read_text(encoding="utf-8"))
        print(f"{i}. {data.get('title')} ({data.get('mission_id')})")
    print()


def print_protocols() -> None:
    print("Protocols")
    print("---------")
    print("1. AAuth")
    print("2. UCAN")
    print("3. ZCAP")
    print()


def print_subject_states() -> None:
    print("Subject States")
    print("--------------")
    print("1. Independent")
    print("2. Supervised")
    print("3. Lapsed")
    print()


def display_result(result: dict) -> None:
    envelope = result["runtime_envelope"]
    decision = result["decision_package"]
    status = result["execution_status"]

    print()
    print("Governance Result")
    print("=================")
    print(f"mission_id:       {envelope['mission']['mission_id']}")
    print(f"protocol:         {envelope['authority']['source_protocol']}")
    print(f"subject_state:    {envelope['subject']['governance_state']}")
    print(f"decision:         {decision['decision']}")
    print(f"reason_class:     {decision['reason_class']}")
    print(f"rule:             {decision['rule']}")
    print(f"execution_status: {status['execution_status']}")
    print()

    directives = decision.get("directives", [])
    constraints = decision.get("constraints", {})

    print("Directives")
    print("----------")
    print(directives if directives else "None")
    print()

    print("Constraints")
    print("-----------")
    print(json.dumps(constraints, indent=2) if constraints else "None")
    print()


def main() -> None:
    missions = load_missions()

    if not missions:
        raise SystemExit("No generated missions found. Run the reference mission builder first.")

    print()
    print("SOGA Governance Workbench")
    print("=========================")
    print("Create or select a mission, project it into a protocol, evaluate it under a subject state, and compare governance outcomes.")
    print()

    print_missions(missions)
    mission_index = choose("Select mission", [str(path) for path in missions])
    mission_file = missions[mission_index]

    print()
    print_protocols()
    protocol_index = choose("Select protocol", list(PROTOCOLS.values()))
    protocol = PROTOCOLS[str(protocol_index + 1)]

    print()
    print_subject_states()
    state_index = choose("Select subject state", list(SUBJECT_STATES.values()))
    state = SUBJECT_STATES[str(state_index + 1)]

    result = run(str(mission_file), protocol, state)
    display_result(result)


if __name__ == "__main__":
    main()
