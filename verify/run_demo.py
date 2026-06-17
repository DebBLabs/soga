"""
SOGA Sprint 4 Demo Runner

The demo consumes the Canonical Decision Package as the
normative execution-time governance artifact.

Visualization, audit, and execution layers consume the
Decision Package and SHALL NOT reconstruct governance logic.
"""

import json

from phase1b_core import evaluate


def process_request(request, runtime):

    #
    # Evaluate
    #

    package = evaluate(request, runtime)

    #
    # Canonical artifact
    #

    decision_package = package.to_dict()

    #
    # Persist artifact
    #

    with open("decision_package.json", "w") as f:
        json.dump(
            decision_package,
            f,
            indent=2,
            default=str,
        )

    return decision_package


if __name__ == "__main__":

    sample_request = {
        "mission": "Healthcare Proxy",
    }

    sample_runtime = {

        "mission_result": "PASS",
        "authority_result": "PASS",
        "subject_result": "PASS",
        "reachability_result": "REVIEW",
        "execution_context_result": "PASS",
        "policy_result": "PASS",

        "subject_agency_state": "Delegated",
        "reachability": "Unreachable",

        "elapsed_time": None,
        "delegation_chain_state": None,
        "delegation_attenuation": None,
        "revocation_status": None,

        "execution_context": {
            "phase": "Emergency"
        },

        "policy": {
            "profile": "Healthcare"
        },

        "execution_receipt": "demo",

        "provenance": "SOGA-PDP",

        "restricted": True,

        "restrict_mode": "SUPERVISED_EXECUTION",
    }

    artifact = process_request(
        sample_request,
        sample_runtime,
    )

    print(json.dumps(
        artifact,
        indent=2,
        default=str,
    ))

