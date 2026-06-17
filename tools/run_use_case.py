import json
import sys
from pathlib import Path

from engines.soga_runtime_engine import (
    SOGARuntimeEngine,
)


def load_use_case(use_case_id):
    path = (
        Path("use_cases")
        / use_case_id
        / "use_case.json"
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def execute_use_case(use_case):
    if "cmr" in use_case:
        return (
            SOGARuntimeEngine()
            .execute_cmr(
                cmr=use_case["cmr"],
                available_evidence=use_case.get(
                    "available_evidence",
                    [],
                ),
            )
        )

    return (
        SOGARuntimeEngine()
        .execute(
            request=use_case["request"],
            answers=use_case["answers"],
            available_evidence=use_case.get(
                "available_evidence",
                [],
            ),
        )
    )


def packages_to_dict(result):
    return [
        package.to_dict()
        for package in result[
            "canonical_decision_packages"
        ]
    ]


def print_json(use_case, result):
    print(
        json.dumps(
            {
                "use_case": {
                    "title": use_case["title"],
                    "request": use_case["request"],
                },
                "canonical_decision_packages":
                    packages_to_dict(result),
                "supporting_diagnostics": {
                    "evidence_selection_count": len(
                        result["evidence_selection"]
                    ),
                    "governance_decision_count": len(
                        result["governance_decisions"]
                    ),
                    "execution_receipt_count": len(
                        result["receipts"]
                    ),
                },
            },
            indent=2,
            default=str,
        )
    )


def print_human(use_case, result):

    print()
    print(
        "SOGA CANONICAL DECISION PACKAGE RUNNER"
    )
    print(
        "======================================"
    )
    print()

    print("Use case:")
    print(use_case["title"])
    print()

    print("Request:")
    print(use_case["request"])
    print()

    print(
        "Canonical Decision Packages"
    )
    print(
        "---------------------------"
    )

    for package in result[
        "canonical_decision_packages"
    ]:

        print(
            json.dumps(
                package.to_dict(),
                indent=2,
                default=str,
            )
        )
        print()

    print(
        "Supporting Diagnostics"
    )
    print(
        "----------------------"
    )

    print(
        "Evidence selections:",
        len(
            result[
                "evidence_selection"
            ]
        ),
    )

    print(
        "Governance decisions:",
        len(
            result[
                "governance_decisions"
            ]
        ),
    )

    print(
        "Execution receipts:",
        len(
            result[
                "receipts"
            ]
        ),
    )


def main():

    if len(sys.argv) < 2:
        print()
        print("Usage:")
        print(
            "  python3 -m tools.run_use_case <use_case_id> [--json]"
        )
        print()
        print("Available:")
        for path in sorted(
            Path("use_cases").glob(
                "*/use_case.json"
            )
        ):
            print(" -", path.parent.name)
        print()
        return

    output_json = "--json" in sys.argv[2:]

    use_case = load_use_case(
        sys.argv[1]
    )

    result = execute_use_case(
        use_case
    )

    if output_json:
        print_json(
            use_case,
            result,
        )
    else:
        print_human(
            use_case,
            result,
        )


if __name__ == "__main__":
    main()
