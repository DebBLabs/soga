from pprint import pprint

from engines.execution_plan_builder import (
    ExecutionPlanBuilder,
)
from engines.mission_intake_engine import (
    MissionIntakeEngine,
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

cmr = MissionIntakeEngine().run(
    request,
    answers,
)

plan = ExecutionPlanBuilder().build(
    cmr
)

print()
print("EXECUTION PLAN DEMO")
print("===================")
print()

pprint(plan)
