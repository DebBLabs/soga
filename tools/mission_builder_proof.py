from __future__ import annotations

import argparse
import json

from builders.mission_builder import mission_file_to_template


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a canonical MissionTemplate from a mission JSON file."
    )
    parser.add_argument(
        "mission_file",
        nargs="?",
        default="missions/gift_purchase_mission.json",
        help="Mission JSON file",
    )
    args = parser.parse_args()

    mission = mission_file_to_template(args.mission_file)

    print("Mission Builder Proof")
    print("=====================")
    print("Mission file:")
    print(f"  {args.mission_file}")
    print()
    print("Canonical MissionTemplate:")
    print(json.dumps(mission.to_dict(), indent=2))


if __name__ == "__main__":
    main()
