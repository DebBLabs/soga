from __future__ import annotations

import json

from tools.subject_agency_state_demo import run_state


def print_section(title):
    print()
    print(title)
    print("-" * len(title))


def main():
    mission_file = "missions/gift_purchase_mission.json"

    print("SOGA CANONICAL CAREGIVER SCENARIO")
    print("=================================")
    print()
    print("Purpose:")
    print("Show RESTRICT as a first-class governance lifecycle.")
    print()
    print("Scenario:")
    print("Alice is the subject.")
    print("Beth is the caregiver delegate.")
    print("The mission is to purchase a birthday gift.")
    print("Alice's Subject Agency State is SUPERVISED.")
    print("Execution requires caregiver approval before proceeding.")

    print_section("STEP 1 — Mission")
    print("Mission: Birthday Gift Purchase")
    print("Subject: Alice")
    print("Delegate: Beth")
    print("Mission Step: Complete Purchase")

    print_section("STEP 2 — Authority Evidence")
    print("Authority Requirement: Bounded purchasing authority")
    print("Authority Evidence: AAuth-shaped mission evidence")
    print("Authority Rationale:")
    print("The delegate is attempting to perform a purchase on behalf of the subject.")

    print_section("STEP 3 — Runtime Subject State")
    print("Subject Agency State: SUPERVISED")

    restrict_result = run_state(mission_file, "SUPERVISED")

    print_section("STEP 4 — Governance Evaluation")
    print("Governance Result:", restrict_result["governance_determination"])
    print("Restrict Mode:", restrict_result["restrict_mode"])
    print("Execution Status:", restrict_result["execution_status"])
    print()
    print("RESTRICT CDP / Execution Receipt:")
    print(json.dumps(restrict_result, indent=2, default=str))

    if restrict_result["governance_determination"] != "RESTRICT":
        raise AssertionError("Expected RESTRICT before approval")

    if restrict_result["execution_status"] != "HOLDING":
        raise AssertionError("Expected HOLDING before approval")

    print_section("STEP 5 — Approval Event")
    print("Approval Source: Beth")
    print("Approval Evidence: human_confirmation")
    print("Approval Status: GRANTED")
    print()
    print("Note:")
    print("For Gate 2, approval is represented as scenario evidence.")
    print("Production approval lifecycle is future work.")

    allow_result = run_state(mission_file, "INDEPENDENT")

    print_section("STEP 6 — Re-Evaluation")
    print("Governance Result:", allow_result["governance_determination"])
    print("Execution Status:", allow_result["execution_status"])
    print()
    print("ALLOW CDP / Execution Receipt:")
    print(json.dumps(allow_result, indent=2, default=str))

    if allow_result["governance_determination"] != "ALLOW":
        raise AssertionError("Expected ALLOW after approval")

    if allow_result["execution_status"] != "EXECUTING":
        raise AssertionError("Expected EXECUTING after approval")

    print_section("PASS")
    print("Canonical Caregiver Scenario demonstrated:")
    print("RESTRICT → HOLDING → approval evidence → ALLOW → EXECUTING")


if __name__ == "__main__":
    main()
