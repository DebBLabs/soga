from __future__ import annotations

import json

from tools.subject_agency_state_demo import run_state


def main():
    result = run_state("SUPERVISED")

    print("SOGA RESTRICT VISIBILITY DEMO")
    print("=============================")
    print()
    print("RESTRICT is not DENY.")
    print("RESTRICT produces a named mode and constrained continuation.")
    print()
    print(json.dumps(result, indent=2, default=str))

    if result["governance_determination"] != "RESTRICT":
        raise AssertionError("Expected RESTRICT outcome")

    if not result["restrict_mode"]:
        raise AssertionError("RESTRICT missing named mode")

    receipt = result["execution_receipt"]

    if receipt["execution_status"] == "ABORTED":
        raise AssertionError("RESTRICT incorrectly aborted execution")

    if receipt["metadata"]["decision"] != "RESTRICT":
        raise AssertionError("Receipt does not reflect RESTRICT")

    if not receipt["metadata"]["constraints"]:
        raise AssertionError("RESTRICT missing constraints")

    print()
    print("PASS: RESTRICT produced constrained continuation.")


if __name__ == "__main__":
    main()
