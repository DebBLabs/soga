from __future__ import annotations

from engines.intake_engine import MissionIntakeEngine


def main() -> None:
    engine = MissionIntakeEngine()

    result = engine.inspect(
        "My niece should manage my medical appointments while I am traveling.",
        sector="healthcare",
    )

    print("Mission Intake Engine Proof")
    print("===========================")
    print(f"status: {result['status']}")
    print(f"sector: {result['sector']}")
    print()
    print("Files loaded")
    print("------------")
    for filename in result["sector_package"]["files_loaded"]:
        print(f"✓ {filename}")

    if result["sector_package"]["files_missing"]:
        print()
        print("Files missing")
        print("-------------")
        for filename in result["sector_package"]["files_missing"]:
            print(f"✗ {filename}")

    print()
    print("Notes")
    print("-----")
    for note in result["notes"]:
        print(f"- {note}")


if __name__ == "__main__":
    main()
