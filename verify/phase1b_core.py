"""
SOGA Phase 1B Core Evaluator

Reference implementation of execution-time governance.

This module performs governance evaluation and returns a
Canonical Decision Package.
"""

from decision_package_builder import build_decision_package


def evaluate(request, runtime):

    # -------------------------------------------------
    # Governance Determination
    # -------------------------------------------------

    if runtime.get("revoked", False):
        determination = "DENY"

    elif runtime.get("restricted", False):
        determination = "RESTRICT"

    else:
        determination = "ALLOW"

    # -------------------------------------------------
    # Dimension Evaluations
    # -------------------------------------------------

    dimensions = {
        "mission": runtime.get("mission_result", "PASS"),
        "authority": runtime.get("authority_result", "PASS"),
        "subject_agency_state":
            runtime.get("subject_result", "PASS"),
        "reachability":
            runtime.get("reachability_result", "PASS"),
        "execution_context":
            runtime.get("execution_context_result", "PASS"),
        "policy":
            runtime.get("policy_result", "PASS"),
    }

    # -------------------------------------------------
    # Authority Inputs
    # -------------------------------------------------

    authority_inputs = {
        "elapsed_time":
            runtime.get("elapsed_time"),

        "delegation_chain_state":
            runtime.get("delegation_chain_state"),

        "delegation_attenuation":
            runtime.get("delegation_attenuation"),

        "revocation_status":
            runtime.get("revocation_status"),

        "additional_inputs":
            runtime.get("authority_additional", {}),
    }

    # -------------------------------------------------
    # Build Canonical Decision Package
    # -------------------------------------------------

    package = build_decision_package(

        determination=determination,

        dimensions=dimensions,

        authority_inputs=authority_inputs,

        subject_agency_state=
            runtime.get(
                "subject_agency_state",
                "Independent",
            ),

        reachability=
            runtime.get(
                "reachability",
                "Reachable",
            ),

        mission=request.get("mission"),

        execution_context=
            runtime.get(
                "execution_context",
                {},
            ),

        policy=
            runtime.get(
                "policy",
                {},
            ),

        execution_receipt=
            runtime.get(
                "execution_receipt",
                "generated",
            ),

        provenance=
            runtime.get(
                "provenance",
                "SOGA-PDP",
            ),

        restrict_mode=
            runtime.get(
                "restrict_mode"
            ),
    )

    return package

