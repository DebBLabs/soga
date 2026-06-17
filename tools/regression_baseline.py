from __future__ import annotations

import argparse

from tools.run_mission import run_mission


CASES = [
    ("aauth", "ACTIVE", "ALLOW", "EXECUTING"),
    ("ucan", "ACTIVE", "ALLOW", "EXECUTING"),
    ("zcap", "ACTIVE", "ALLOW", "EXECUTING"),
    ("aauth", "IMPAIRED", "RESTRICT", "HOLDING"),
    ("ucan", "IMPAIRED", "RESTRICT", "HOLDING"),
    ("zcap", "IMPAIRED", "RESTRICT", "HOLDING"),
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run SOGA regression baseline cases."
    )
    parser.add_argument(
        "mission_file",
        nargs="?",
        default="missions/gift_purchase_mission.json",
        help="Mission JSON file",
    )
    args = parser.parse_args()

    print("SOGA Regression Baseline")
    print("========================")
    print()

    failures = []

    for protocol, state, expected_decision, expected_status in CASES:
        result = run_mission(args.mission_file, protocol, state)

        decision = result["decision_package"]["decision"]
        status = result["execution_status"]["execution_status"]

        ok = decision == expected_decision and status == expected_status
        marker = "✓" if ok else "✗"

        print(
            f"{marker} {protocol:5} state={state:8} "
            f"decision={decision:8} execution={status}"
        )

        if not ok:
            failures.append(
                {
                    "protocol": protocol,
                    "state": state,
                    "expected": {
                        "decision": expected_decision,
                        "execution_status": expected_status,
                    },
                    "actual": {
                        "decision": decision,
                        "execution_status": status,
                    },
                }
            )

    if failures:
        print()
        print("FAILURES")
        print("--------")
        for failure in failures:
            print(failure)
        raise SystemExit(1)

    print()
    print("All baseline cases passed.")


if __name__ == "__main__":
    main()
