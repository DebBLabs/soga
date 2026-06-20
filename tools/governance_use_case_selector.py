from __future__ import annotations

import argparse

from tools.cdp_regression import USE_CASES
from tools.run_use_case import execute_use_case, load_use_case


def line():
    print("-" * 72)


def print_lifecycle(package):
    decision = package["governance_determination"]
    receipt = package.get("execution_receipt")
    if isinstance(receipt, dict):
        execution = receipt.get("execution_status")
    else:
        execution = receipt

    print()
    print("Governance Lifecycle")
    line()

    steps = [
        ("Mission step requested", True),
        ("Authority evidence presented", True),
        ("Subject state evaluated", True),
        (f"Governance issued {decision}", True),
        (f"Execution receipt: {execution}", True),
    ]

    for label, complete in steps:
        marker = "✓" if complete else "□"
        print(marker, label)


def print_package(use_case_id, use_case, package):
    print()
    print("=" * 72)
    print("MISSION GOVERNANCE VIEW")
    print("=" * 72)
    print("Use Case:", use_case_id)
    print("Mission:", package["mission"].get("title"))
    print("Request:", use_case["request"])
    print()
    print("Subject Agency State:", package["subject_agency_state"])
    print("Governance Decision:", package["governance_determination"])
    receipt = package.get("execution_receipt")
    if isinstance(receipt, dict):
        execution_status = receipt.get("execution_status")
    else:
        execution_status = receipt

    print("Execution Receipt:", execution_status)
    print()
    print("Dimension Results")
    line()
    for name, value in package["dimension_results"].items():
        print(f"{name}: {value}")

    if package["governance_determination"] == "RESTRICT":
        print()
        print("Required Action")
        line()
        print("Review required before unrestricted execution may proceed.")

    print_lifecycle(package)


def run_use_case_view(use_case_id):
    use_case = load_use_case(use_case_id)
    result = execute_use_case(use_case)

    packages = [
        package.to_dict()
        for package in result["canonical_decision_packages"]
    ]

    if not packages:
        raise AssertionError(f"{use_case_id}: no canonical decision packages")

    print()
    print("#" * 72)
    print("SOGA GOVERNANCE USE CASE SELECTOR")
    print("#" * 72)

    for package in packages:
        print_package(use_case_id, use_case, package)

    print()
    print("PASS:", use_case_id)


def main():
    parser = argparse.ArgumentParser(
        description="Explore SOGA Governance View across regression use cases."
    )
    parser.add_argument(
        "use_case",
        nargs="?",
        choices=USE_CASES + ["all"],
        default="all",
    )
    args = parser.parse_args()

    selected = USE_CASES if args.use_case == "all" else [args.use_case]

    print("Available use cases:")
    for use_case_id in USE_CASES:
        marker = "*" if use_case_id in selected else "-"
        print(marker, use_case_id)

    for use_case_id in selected:
        run_use_case_view(use_case_id)

    print()
    print("=" * 72)
    print("GOVERNANCE SELECTOR PASS")
    print("=" * 72)
    print(f"Use cases shown: {len(selected)}")


if __name__ == "__main__":
    main()
