from __future__ import annotations

import argparse
import json

from builders.mission_builder import mission_file_to_template
from builders.protocol_projection import (
    mission_to_aauth_artifact,
    mission_to_ucan_artifact,
    mission_to_zcap_artifact,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Project a MissionTemplate into AAuth, UCAN, and ZCAP artifacts."
    )
    parser.add_argument(
        "mission_file",
        nargs="?",
        default="missions/gift_purchase_mission.json",
        help="Mission JSON file",
    )
    args = parser.parse_args()

    mission = mission_file_to_template(args.mission_file)

    print("Mission Projection Proof")
    print("========================")
    print(
        "Canonical MissionTemplate projected into "
        "AAuth, UCAN, and ZCAP-shaped artifacts."
    )
    print()

    print("AAuth projection")
    print("----------------")
    print(json.dumps(mission_to_aauth_artifact(mission), indent=2))
    print()

    print("UCAN projection")
    print("---------------")
    print(json.dumps(mission_to_ucan_artifact(mission), indent=2))
    print()

    print("ZCAP projection")
    print("---------------")
    print(json.dumps(mission_to_zcap_artifact(mission), indent=2))


if __name__ == "__main__":
    main()
