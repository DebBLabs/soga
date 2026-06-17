from datetime import datetime, timedelta, timezone

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
    "reachability": "Reachable",
    "execution_context_valid": True,
    "authority": {
        "delegation_time":
            datetime.now(timezone.utc)
            - timedelta(days=2),
        "execution_time":
            datetime.now(timezone.utc),
        "delegation_chain": [
            "principal",
            "niece",
        ],
        "max_elapsed_seconds":
            86400,
        "max_delegation_hops":
            2,
    },
}

result = SOGARuntimeEngine().execute(
    request=request,
    answers=answers,
    available_evidence=available_evidence,
    runtime=runtime,
)

print()
print("AUTHORITY RUNTIME DEMO")
print("======================")
print()

print("Computed authority:")
print(result["runtime"]["authority"])
print()

for decision in result["governance_decisions"]:
    print(decision["step_id"])
    print("action:", decision["action"])
    print("decision:", decision["decision"])
    print("reason:", decision["reason"])
    print("dimensions:", decision["dimensions"])
    print()
