from engines.soga_runtime_engine import (
    SOGARuntimeEngine,
)

request = (
    "My niece should manage my medical "
    "appointments while I am traveling."
)

answers = [
    (
        "May schedule appointments but "
        "may not authorize treatment."
    )
]

available_evidence = [
    {
        "type": "human_confirmation",
        "source": "intake_conversation",
    }
]

result = SOGARuntimeEngine().execute(
    request=request,
    answers=answers,
    available_evidence=available_evidence,
)

print()
print("SOGA FULL RUNTIME DEMO")
print("======================")
print()

print("MISSION")
print("-------")
print(result["mission"]["objective"])
print()

print("SUBJECT")
print("-------")
print(result["subject_id"])
print()

print("STANDING CAPABILITIES")
print("---------------------")
for capability in result["standing_capabilities"]:
    print(
        "-",
        capability["capability_id"],
        capability["capability"],
        capability["evidence_type"],
        capability["status"],
    )
print()

print("EVIDENCE SELECTION")
print("------------------")
for item in result["evidence_selection"]:
    print(item["step_id"])
    print("action:", item["action"])
    print("selected:", item["selected_evidence"])
    print("alternatives:", item["alternatives"])
    print("status:", item["status"])
    print()

print("EVIDENCE JUSTIFICATION")
print("----------------------")
for item in result["evidence_justification"]:
    print(item["step_id"])
    print("action:", item["action"])
    print("selected:", item["selected_evidence"])
    print("justification:", item["justification"])
    print("alternatives:", item["alternatives"])
    print()

print("RUNTIME GOVERNANCE DECISIONS")
print("----------------------------")
for decision in result["governance_decisions"]:
    print(
        decision["step_id"],
        decision["action"],
        "->",
        decision["decision"],
    )
    print("reason:", decision["reason"])
print()

print("EXECUTION RECEIPTS")
print("------------------")
for receipt in result["receipts"]:
    print(receipt["step_id"])
    print("action:", receipt["action"])
    print("decision:", receipt["decision"])
    print("status:", receipt["execution_status"])
    print("reason:", receipt["reason"])
    print()
