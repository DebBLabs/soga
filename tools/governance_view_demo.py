from __future__ import annotations

from tools.subject_agency_state_demo import run_state


SCENARIOS = [
    {
        "mission_file": "missions/gift_purchase_mission.json",
        "mission": "Birthday Gift Purchase",
        "step": "Complete Purchase",
        "authority": "Delegated purchasing authority",
        "evidence": "AAuth-shaped mission evidence",
        "approval_required": "Beth approval required before purchase may proceed.",
    },
    {
        "mission_file": "generated/missions/mission-medication-refill.json",
        "mission": "Medication Refill",
        "step": "Arrange authorized refill delivery",
        "authority": "Delegated medication refill coordination authority",
        "evidence": "AAuth-shaped mission evidence",
        "approval_required": "Beth approval required before refill action may proceed.",
    },
    {
        "mission_file": "generated/missions/mission-travel-displacement.json",
        "mission": "Travel Displacement",
        "step": "Rebook disrupted travel within delegated limits",
        "authority": "Delegated travel replanning authority",
        "evidence": "AAuth-shaped mission evidence",
        "approval_required": "Beth approval required before travel change may proceed.",
    },
]


def line():
    print("-" * 72)


def print_status(title, scenario, result, required_action):
    print()
    print(title)
    line()
    print("Mission:", scenario["mission"])
    print("Subject: Alice")
    print("Delegate: Beth")
    print("Current Step:", scenario["step"])
    print()
    print("Authority Requirement:", scenario["authority"])
    print("Authority Evidence:", scenario["evidence"])
    print("Protocol Role: Supporting evidence only")
    print()
    print("Subject Agency State:", result["subject_agency_state"])
    print("Governance Decision:", result["governance_determination"])
    print("Execution Status:", result["execution_status"])
    print("Required Action:", required_action)


def print_lifecycle(after_approval=False):
    print()
    print("RESTRICT Lifecycle")
    line()

    steps = [
        ("Mission step requested", True),
        ("Authority evidence presented", True),
        ("Subject state evaluated", True),
        ("Governance issued RESTRICT", True),
        ("Execution entered HOLDING", True),
        ("Approval received", after_approval),
        ("Re-evaluation", after_approval),
        ("ALLOW", after_approval),
        ("EXECUTING", after_approval),
    ]

    for label, complete in steps:
        marker = "✓" if complete else "□"
        print(marker, label)


def run_scenario(scenario):
    restrict_result = run_state(
        scenario["mission_file"],
        "SUPERVISED",
    )

    if restrict_result["governance_determination"] != "RESTRICT":
        raise AssertionError(
            f'{scenario["mission"]}: expected RESTRICT'
        )

    if restrict_result["execution_status"] != "HOLDING":
        raise AssertionError(
            f'{scenario["mission"]}: expected HOLDING'
        )

    print()
    print("=" * 72)
    print("MISSION GOVERNANCE STATUS")
    print("=" * 72)

    print_status(
        "Before Approval",
        scenario,
        restrict_result,
        scenario["approval_required"],
    )

    print_lifecycle(after_approval=False)

    print()
    print("Approval Event")
    line()
    print("Approval Source: Beth")
    print("Approval Status: GRANTED")
    print("Approval Note: Scenario-level approval event for pattern verification.")

    allow_result = run_state(
        scenario["mission_file"],
        "INDEPENDENT",
    )

    if allow_result["governance_determination"] != "ALLOW":
        raise AssertionError(
            f'{scenario["mission"]}: expected ALLOW'
        )

    if allow_result["execution_status"] != "EXECUTING":
        raise AssertionError(
            f'{scenario["mission"]}: expected EXECUTING'
        )

    print_status(
        "After Approval / Re-Evaluation",
        scenario,
        allow_result,
        "No further action required.",
    )

    print_lifecycle(after_approval=True)

    print()
    print("PASS:", scenario["mission"])
    print(
        "RESTRICT → HOLDING → Approval → "
        "Re-Evaluation → ALLOW → EXECUTING"
    )


def main():
    print("SOGA GOVERNANCE VIEW PATTERN VERIFICATION")
    print("=========================================")
    print()
    print("Same actors. Same view structure. Multiple missions.")
    print("Subject: Alice")
    print("Delegate: Beth")

    for scenario in SCENARIOS:
        run_scenario(scenario)

    print()
    print("=" * 72)
    print("PATTERN VERIFICATION PASS")
    print("=" * 72)
    print("Governance View generalized across:")
    for scenario in SCENARIOS:
        print("-", scenario["mission"])


if __name__ == "__main__":
    main()
