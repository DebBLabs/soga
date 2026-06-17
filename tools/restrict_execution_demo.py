from pprint import pprint

from engines.restrict_execution_engine import (
    RestrictExecutionEngine,
)

step = {
    "step_id": "step-schedule_appointment",
    "action": "schedule_appointment",
}

modes = [
    {
        "mode": "bounded_continuation",
        "reason": "Execution context permits only bounded continuation.",
    },
    {
        "mode": "supervised_execution",
        "reason": "Subject governance state requires supervision.",
    },
    {
        "mode": "delayed_execution",
        "reason": "Subject is not currently reachable.",
    },
    {
        "mode": "reduced_authority",
        "reason": "Authority attenuation requires reduced scope.",
    },
    {
        "mode": "partial_execution",
        "reason": "Only part of the mission may continue.",
    },
    {
        "mode": "escalation",
        "reason": "Policy requires escalation.",
    },
]

print()
print("RESTRICT EXECUTION DEMO")
print("=======================")
print()

engine = RestrictExecutionEngine()

for mode in modes:
    print(mode["mode"])
    pprint(
        engine.execute(
            step,
            mode,
        )
    )
    print()
