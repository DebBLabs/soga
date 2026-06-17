import json
import subprocess
import sys


USE_CASES = [
    "banking",
    "caregiver",
    "emergency",
    "enterprise",
    "guardianship",
    "insurance",
    "medical_appointments",
    "research",
    "shopping",
    "travel",
]


REQUIRED_PACKAGE_FIELDS = [
    "governance_determination",
    "dimension_results",
    "authority_inputs",
    "subject_agency_state",
    "reachability",
    "mission",
    "execution_context",
    "policy",
    "execution_receipt",
    "provenance",
    "timestamp",
]


REQUIRED_DIMENSIONS = [
    "mission",
    "authority",
    "subject_agency_state",
    "reachability",
    "execution_context",
    "policy",
]


def run_use_case(use_case_id):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.run_use_case",
            use_case_id,
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    return json.loads(result.stdout)


def validate_package(use_case_id, package):
    for field in REQUIRED_PACKAGE_FIELDS:
        if field not in package:
            raise AssertionError(
                f"{use_case_id}: missing field {field}"
            )

    if "subject_governance_state" in package:
        raise AssertionError(
            f"{use_case_id}: forbidden field subject_governance_state"
        )

    dimensions = package["dimension_results"]

    for dimension in REQUIRED_DIMENSIONS:
        if dimension not in dimensions:
            raise AssertionError(
                f"{use_case_id}: missing dimension {dimension}"
            )

    if "subject_governance_state" in dimensions:
        raise AssertionError(
            f"{use_case_id}: forbidden dimension subject_governance_state"
        )

    if package["governance_determination"] not in [
        "ALLOW",
        "RESTRICT",
        "DENY",
    ]:
        raise AssertionError(
            f"{use_case_id}: invalid governance determination"
        )

    for dimension, value in dimensions.items():
        if value not in [
            "PASS",
            "REVIEW",
            "FAIL",
        ]:
            raise AssertionError(
                f"{use_case_id}: invalid dimension value "
                f"{dimension}={value}"
            )

    if (
        package["governance_determination"] == "RESTRICT"
        and not package.get("restrict_mode")
    ):
        raise AssertionError(
            f"{use_case_id}: RESTRICT missing restrict_mode"
        )


def main():
    total_packages = 0

    for use_case_id in USE_CASES:
        output = run_use_case(use_case_id)

        packages = output[
            "canonical_decision_packages"
        ]

        if not packages:
            raise AssertionError(
                f"{use_case_id}: no canonical decision packages"
            )

        for package in packages:
            validate_package(
                use_case_id,
                package,
            )

        total_packages += len(packages)

        print(
            f"PASS {use_case_id}: "
            f"{len(packages)} canonical decision packages"
        )

    print()
    print(
        f"CDP REGRESSION PASS: "
        f"{len(USE_CASES)} use cases, "
        f"{total_packages} canonical decision packages"
    )


if __name__ == "__main__":
    main()
