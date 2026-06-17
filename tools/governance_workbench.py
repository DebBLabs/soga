from __future__ import annotations

import json
from pathlib import Path

from tools.run_generated_mission import run


MISSIONS_DIR = Path("generated/missions")
PROTOCOLS = ["aauth", "ucan", "zcap"]
STATES = ["ACTIVE", "IMPAIRED", "LAPSED"]


def main() -> None:
    missions = sorted(MISSIONS_DIR.glob("*.json"))

    print("SOGA Governance Workbench")
    print("=========================")
    print()

    for mission_file in missions:
        mission_data = json.loads(mission_file.read_text(encoding="utf-8"))
        print(f"Mission: {mission_data.get('title')} ({mission_data.get('mission_id')})")
        print("-" * 72)
        print(f"{'Protocol':<10} {'State':<10} {'Decision':<10} {'Execution':<10}")
        print("-" * 72)

        for protocol in PROTOCOLS:
            for state in STATES:
                result = run(str(mission_file), protocol, state)
                decision = result["decision_package"]["decision"]
                execution = result["execution_status"]["execution_status"]
                print(f"{protocol:<10} {state:<10} {decision:<10} {execution:<10}")

        print()

if __name__ == "__main__":
    main()
