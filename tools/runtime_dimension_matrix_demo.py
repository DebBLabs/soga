from pprint import pprint

from engines.runtime_dimension_evaluator import (
    RuntimeDimensionEvaluator,
)

evaluator = RuntimeDimensionEvaluator()

step = {
    "step_id": "step-schedule_appointment",
    "action": "schedule_appointment",
    "status": "SELECTED",
    "selected_evidence": "oauth_or_gnap_token",
}

scenarios = {
    "ALLOW": {
        "subject_agency_state": "Independent",
        "reachability": "Reachable",
        "execution_context_valid": True,
    },
    "RESTRICT": {
        "subject_agency_state": "Independent",
        "reachability": "Unreachable",
        "bounded_continuation_allowed": True,
        "execution_context_valid": True,
    },
    "DENY": {
        "subject_agency_state": "Lapsed",
        "reachability": "Reachable",
        "execution_context_valid": True,
    },
}

print()
print("RUNTIME DIMENSION MATRIX DEMO")
print("=============================")
print()

for name, runtime in scenarios.items():
    print(name)
    print("-" * len(name))
    pprint(
        evaluator.evaluate(
            step,
            runtime,
        )
    )
    print()
