from pprint import pprint

from engines.restrict_mode_selector import (
    RestrictModeSelector,
)

selector = RestrictModeSelector()

cases = {
    "authority": {
        "mission":"PASS",
        "authority":"REVIEW",
        "subject_agency_state":"PASS",
        "reachability":"PASS",
        "execution_context":"PASS",
        "policy":"PASS",
    },
    "reachability": {
        "mission":"PASS",
        "authority":"PASS",
        "subject_agency_state":"PASS",
        "reachability":"REVIEW",
        "execution_context":"PASS",
        "policy":"PASS",
    },
    "policy": {
        "mission":"PASS",
        "authority":"PASS",
        "subject_agency_state":"PASS",
        "reachability":"PASS",
        "execution_context":"PASS",
        "policy":"REVIEW",
    },
}

print()
print("RESTRICT MODE DEMO")
print("==================")
print()

for name, dimensions in cases.items():
    print(name)
    pprint(selector.select(dimensions))
    print()
