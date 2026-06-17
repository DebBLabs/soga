from pprint import pprint
from dataclasses import asdict, is_dataclass

from intake.mission_intake_engine import MissionIntakeEngine
from builders.protocol_projection import mission_to_aauth_artifact
from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from verify.governance_pdp import GovernancePDP

HUMAN_INTENT = (
    "My niece may schedule my cardiology appointments "
    "but may not authorize treatment."
)

def show(obj):
    if is_dataclass(obj):
        pprint(asdict(obj))
    else:
        pprint(obj)

result = MissionIntakeEngine().intake(
    HUMAN_INTENT,
    sector_knowledge=["Healthcare"],
    debug=True,
)

mwr = result["mwr"]
cmr = result["cmr"]

artifact = mission_to_aauth_artifact(cmr)
ms = first_mission_statement(artifact)
envelope = mission_statement_to_runtime_envelope_v0_1(
    artifact,
    ms,
)
decision = GovernancePDP().evaluate(envelope)

print("\n===================================")
print("SOGA MISSION INTAKE DEMO")
print("===================================\n")

print("Human Intent")
print("------------")
print(HUMAN_INTENT)

print("\nCandidate Observations")
print("----------------------")
show(mwr.candidate_observations)

print("\nMission Working Representation")
print("------------------------------")
show(mwr)

print("\nValidation")
print("----------")
show(result["validation"])

print("\nCanonical Mission Representation")
print("--------------------------------")
show(cmr)

print("\nRuntime Result")
print("--------------")
print({
    "governance_determination": decision.decision.value,
    "rule": decision.rule,
    "explanation": decision.explanation,
})
