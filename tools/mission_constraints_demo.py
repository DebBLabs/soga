"""
Mission Constraints Demo

Demonstrates that mission-authored constraints can be projected into
SOGA runtime constraint form without changing evaluator logic.
"""


SCENARIOS = [
    {
        "name": "Health — subject unreachable",
        "mission_id": "health-check",
        "action_type": "send_health_update",
        "constraints": {
            "global": {
                "subject_must_be_reachable": True,
            },
            "stage_gate": [],
            "delegation": {},
        },
        "expected_constraint": "subject_must_be_reachable",
    },
    {
        "name": "Finance — approval required above threshold",
        "mission_id": "finance-transfer",
        "action_type": "transfer_funds",
        "constraints": {
            "global": {
                "approval_required_above": 500,
            },
            "stage_gate": [],
            "delegation": {},
        },
        "expected_constraint": "approval_required_above",
    },
    {
        "name": "Robotics — interaction boundary change",
        "mission_id": "robot-assist",
        "action_type": "continue_robot_assist",
        "constraints": {
            "global": {
                "restrict_if_interaction_boundary_changes": True,
            },
            "stage_gate": [],
            "delegation": {},
        },
        "expected_constraint": "restrict_if_interaction_boundary_changes",
    },
    {
        "name": "Agent team — redelegation depth exceeded",
        "mission_id": "agent-team-task",
        "action_type": "delegate_subtask",
        "constraints": {
            "global": {},
            "stage_gate": [],
            "delegation": {
                "redelegation_depth": 1,
            },
        },
        "expected_constraint": "redelegation_depth",
    },
]


def project_constraints(constraints):
    projected = {
        "global": {},
        "stage_gate": [],
        "delegation": {},
    }

    for scope in ("global", "delegation"):
        for key, value in constraints.get(scope, {}).items():
            projected[scope][key] = {
                "value": value,
                "governance_reasoning_token": None,
            }

    for item in constraints.get("stage_gate", []):
        if isinstance(item, dict):
            entry = dict(item)
            entry.setdefault("governance_reasoning_token", None)
            projected["stage_gate"].append(entry)

    return projected


def main():
    print("Mission Constraints Demo")
    print("========================")

    for scenario in SCENARIOS:
        soga_constraints = project_constraints(scenario["constraints"])

        print()
        print(scenario["name"])
        print("-" * len(scenario["name"]))
        print("mission_id:", scenario["mission_id"])
        print("action_type:", scenario["action_type"])
        print("expected_constraint:", scenario["expected_constraint"])
        print("soga_constraints:", soga_constraints)


if __name__ == "__main__":
    main()
