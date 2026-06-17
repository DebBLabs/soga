from __future__ import annotations

from tools.subject_agency_state_demo import run_state


MISSION_FILE = "missions/gift_purchase_mission.json"


def line():
    print("-" * 72)


def print_status(title, result, required_action):
    print()
    print(title)
    line()
    print("Mission: Birthday Gift Purchase")
    print("Subject: Alice")
    print("Delegate: Beth")
    print("Current Step: Complete Purchase")
    print()
    print("Authority Requirement: Delegated purchasing authority")
    print("Authority Evidence: AAuth-shaped mission evidence")
    print("Protocol Role: Supporting evidence only")
    print()
    print("Subject Agency State:", result["subject_agency_state"])
    print("Governance Decision:", result["governance_determination"])
    print("Execution Status:", result["execution_status"])
    print("Required Action:", required_action)


def main():
    restrict_result = run_state(MISSION_FILE, "SUPERVISED")

    if restrict_result["governance_determination"] != "RESTRICT":
        raise AssertionError("Expected RESTRICT")

    if restrict_result["execution_status"] != "HOLDING":
        raise AssertionError("Expected HOLDING")

    print("MISSION GOVERNANCE STATUS")
    print("=========================")

    print_status(
        "Before Approval",
        restrict_result,
        "Beth approval required before execution may proceed.",
    )

    print()
    print("RESTRICT Lifecycle")
    line()
    print("✓ Mission step requested")
    print("✓ Authority evidence presented")
    print("✓ Subject state evaluated")
    print("✓ Governance issued RESTRICT")
    print("✓ Execution entered HOLDING")
    print("□ Approval received")
    print("□ Re-evaluation")
    print("□ ALLOW")
    print("□ EXECUTING")

    print()
    print("Approval Event")
    line()
    print("Approval Source: Beth")
    print("Approval Status: GRANTED")
    print("Approval Note: Scenario-level approval event for Gate 3 demonstration.")

    allow_result = run_state(MISSION_FILE, "INDEPENDENT")

    if allow_result["governance_determination"] != "ALLOW":
        raise AssertionError("Expected ALLOW")

    if allow_result["execution_status"] != "EXECUTING":
        raise AssertionError("Expected EXECUTING")

    print_status(
        "After Approval / Re-Evaluation",
        allow_result,
        "No further action required.",
    )

    print()
    print("RESTRICT Lifecycle")
    line()
    print("✓ Mission step requested")
    print("✓ Authority evidence presented")
    print("✓ Subject state evaluated")
    print("✓ Governance issued RESTRICT")
    print("✓ Execution entered HOLDING")
    print("✓ Approval received")
    print("✓ Re-evaluation")
    print("✓ ALLOW")
    print("✓ EXECUTING")

    print()
    print("PASS")
    line()
    print("Governance View demonstrated:")
    print("RESTRICT → HOLDING → Approval → Re-Evaluation → ALLOW → EXECUTING")


if __name__ == "__main__":
    main()
