from pprint import pprint

from engines.runtime_dimension_evaluator import (
    RuntimeDimensionEvaluator,
)

step = {
    "action": "schedule_appointment",
    "status": "SELECTED",
    "selected_evidence":
        "oauth_or_gnap_token",
}

runtime = {
    "subject_agency_state":
        "Independent",
    "reachability":
        "Reachable",
    "execution_context_valid":
        True,
}

print()
print("RUNTIME DIMENSION DEMO")
print("======================")
print()

pprint(
    RuntimeDimensionEvaluator().evaluate(
        step,
        runtime,
    )
)
