from intake.mission_intake_engine import MissionIntakeEngine

from builders.protocol_projection import (
    mission_to_aauth_artifact,
)

from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)

from verify.governance_pdp import GovernancePDP


HUMAN_INTENT = (
    "My niece may schedule my cardiology appointments "
    "but may not authorize treatment."
)


def main():

    intake = MissionIntakeEngine().intake(
        HUMAN_INTENT,
        sector_knowledge=["Healthcare"],
    )

    if intake["status"] != "PASS":
        raise RuntimeError(intake)

    cmr = intake["cmr"]

    artifact = mission_to_aauth_artifact(cmr)

    mission_statement = first_mission_statement(
        artifact,
    )

    if mission_statement is None:
        raise RuntimeError(
            "No AAuth mission statement found"
        )

    envelope = (
        mission_statement_to_runtime_envelope_v0_1(
            artifact,
            mission_statement,
        )
    )

    decision = GovernancePDP().evaluate(
        envelope,
    )

    print()
    print("SOGA MISSION → CDP DEMO")
    print("=======================")
    print()

    print("Human Intent")
    print("------------")
    print(HUMAN_INTENT)
    print()

    print("Generated CMR")
    print("-------------")
    print(cmr)
    print()

    print("Governance Determination")
    print("------------------------")
    print(decision.decision.value)
    print()

    print("Rule")
    print("----")
    print(decision.rule)
    print()

    print("Explanation")
    print("-----------")
    print(decision.explanation)


if __name__ == "__main__":
    main()
