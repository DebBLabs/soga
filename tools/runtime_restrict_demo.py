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

runtime = {
    "subject_agency_state": "Independent",
    "reachability": "Unreachable",
    "bounded_continuation_allowed": True,
    "execution_context_valid": True,
}

result = SOGARuntimeEngine().execute(
    request=request,
    answers=answers,
    available_evidence=available_evidence,
    runtime=runtime,
)

print()
print("RUNTIME RESTRICT DEMO")
print("=====================")
print()

print("GOVERNANCE DECISIONS")
print("--------------------")
for decision in result["governance_decisions"]:
    print(decision["step_id"])
    print("action:", decision["action"])
    print("decision:", decision["decision"])
    print("reason:", decision["reason"])
    print("restrict_mode:", decision["restrict_mode"])
    print("dimensions:", decision["dimensions"])
    print()

print("EXECUTION RECEIPTS")
print("------------------")
for receipt in result["receipts"]:
    print(receipt["step_id"])
    print("action:", receipt["action"])
    print("decision:", receipt["decision"])
    print("execution_status:", receipt["execution_status"])
    print("restrict_mode:", receipt.get("restrict_mode"))
    print("reason:", receipt["reason"])
    print("details:", receipt.get("details"))
    print()
