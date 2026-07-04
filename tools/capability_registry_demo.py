import json
from pathlib import Path

from engines.capability_registry import CapabilityRegistry


FIXTURE_DIR = Path("tests/fixtures/capabilities")


def load_registry():
    registry = CapabilityRegistry()

    for fixture_path in sorted(FIXTURE_DIR.glob("*.json")):
        with fixture_path.open("r", encoding="utf-8") as fixture_file:
            capability = json.load(fixture_file)

        registry.register(
            canonical_name=capability["canonical_name"],
            implementations=capability["implementations"],
            required_authority_scope=capability["required_authority_scope"],
            governance_dimensions_affected=(
                capability["governance_dimensions_affected"]
            ),
        )

    return registry


def main():
    registry = load_registry()

    mission_step = {
        "step_id": "D-001",
        "action": "schedule_follow_up_visit",
        "required_capability": "appointment.schedule",
    }

    resolution = registry.resolve(
        mission_step["required_capability"]
    )

    print("Capability Registry Demo")
    print("========================")
    print()
    print("Mission Step")
    print("------------")
    print(f"step_id: {mission_step['step_id']}")
    print(f"action: {mission_step['action']}")
    print(
        "required_capability: "
        f"{mission_step['required_capability']}"
    )
    print()
    print("Available Implementations")
    print("-------------------------")

    for implementation in resolution["implementations"]:
        print(
            f"- {implementation['type']}: "
            f"{implementation['stub_endpoint']}"
        )

    print()
    print("Implementation Invariance")
    print("-------------------------")
    print(
        "Changing REST, MCP, or human implementation does not "
        "change the declared capability or static authority metadata."
    )
    print()
    print("Governance Boundary")
    print("-------------------")
    print(
        "CapabilityRegistry describes capabilities and implementation "
        "options. Governance evaluates authority."
    )


if __name__ == "__main__":
    main()
