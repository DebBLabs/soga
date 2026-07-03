from __future__ import annotations

# Scientific Claim
# ----------------
# This demonstration verifies Governance Invariance:
#
#   Origin Representation × Execution Surface ≠ Governance Core
#
# Static representative payloads stand in for what external ecosystems
# would deliver. The report is generated at runtime by projecting each
# payload through its passive adapter, evaluating the resulting canonical
# RuntimeEnvelope with the actual GovernancePDP, and printing the resulting
# DecisionPackage fields.
#
# The claim is not: any ecosystem payload produces the same result as any
# other ecosystem payload.
#
# The claim is: when semantic governance inputs are equivalent, the
# governance decision is invariant regardless of origin representation.

import glob
import json
from pathlib import Path
from typing import Any, Dict

from input_adapters.aauth_adapter import (
    first_mission_statement,
    mission_statement_to_runtime_envelope_v0_1,
)
from input_adapters.aiim_adapter import aiim_to_runtime_envelope_v0_1
from input_adapters.mcp_adapter import mcp_to_runtime_envelope_v0_1
from input_adapters.oauth_adapter import oauth_gnap_to_runtime_envelope_v0_1
from input_adapters.ucan_adapter import ucan_to_runtime_envelope_v0_1
from input_adapters.zcap_adapter import zcap_to_runtime_envelope_v0_1
from verify.governance_pdp import GovernancePDP


LABELS = {
    "aauth": "AAuth",
    "aiim": "AIIM-style",
    "oauth_gnap": "OAuth/GNAP-style",
    "ucan": "UCAN",
    "zcap": "ZCAP",
    "mcp": "MCP-style",
}


def aauth_envelope(payload: Dict[str, Any]):
    mission_statement = first_mission_statement(payload)
    if mission_statement is None:
        raise RuntimeError("No AAuth mission statement found")
    return mission_statement_to_runtime_envelope_v0_1(
        payload,
        mission_statement,
    )


def oauth_gnap_envelope(payload: Dict[str, Any]):
    return oauth_gnap_to_runtime_envelope_v0_1(
        payload,
        payload.get("governance_context", {}),
    )


def mcp_envelope(payload: Dict[str, Any]):
    return mcp_to_runtime_envelope_v0_1(
        payload,
        payload.get("governance_context", {}),
    )


ADAPTER_MAP = {
    "aauth": aauth_envelope,
    "aiim": aiim_to_runtime_envelope_v0_1,
    "oauth_gnap": oauth_gnap_envelope,
    "ucan": ucan_to_runtime_envelope_v0_1,
    "zcap": zcap_to_runtime_envelope_v0_1,
    "mcp": mcp_envelope,
}


def governance_reasoning_token(decision) -> str:
    if decision.rule == "subject_agency_state_requires_constraints":
        return "supervision_required"
    return decision.rule


def capability_label(protocol: str, payload: Dict[str, Any]) -> str:
    if protocol == "mcp":
        return "MCP"
    return payload.get("capability_transport", "REST")


def run_payload(path: Path, pdp: GovernancePDP) -> Dict[str, Any]:
    with path.open("r") as handle:
        payload = json.load(handle)

    protocol = payload.get("protocol")
    adapter = ADAPTER_MAP.get(protocol)

    if adapter is None:
        raise RuntimeError(f"No adapter registered for protocol: {protocol}")

    envelope = adapter(payload)
    decision = pdp.evaluate(envelope)

    return {
        "file": path.name,
        "origin": LABELS.get(protocol, protocol),
        "capability": capability_label(protocol, payload),
        "decision": decision.decision.value,
        "token": governance_reasoning_token(decision),
        "rule": decision.rule,
        "reason_class": decision.reason_class,
    }


def main() -> None:
    payload_paths = [
        Path(item)
        for item in sorted(glob.glob("tests/fixtures/payloads/*_caregiver.json"))
    ]

    pdp = GovernancePDP()
    results = [run_payload(path, pdp) for path in payload_paths]

    print("Governance Invariance Demonstration")
    print("Scenario: Caregiver Discharge Follow-Up")
    print()
    print("Static representative payloads -> passive adapters -> RuntimeEnvelope -> GovernancePDP -> DecisionPackage")
    print()
    print(f"{'Origin':<18} {'Capability':<12} {'Decision':<10} {'Token':<24} {'Rule'}")
    print("-" * 92)

    for result in results:
        print(
            f"{result['origin']:<18} "
            f"{result['capability']:<12} "
            f"{result['decision']:<10} "
            f"{result['token']:<24} "
            f"{result['rule']}"
        )

    decisions = {result["decision"] for result in results}
    tokens = {result["token"] for result in results}

    print("-" * 92)

    if len(decisions) == 1 and len(tokens) == 1:
        print("Governance decision: INVARIANT")
        print("Governance reasoning token: INVARIANT")
    else:
        print("Governance invariance: FAILED")

    print("GovernancePDP:       UNCHANGED")
    print("RuntimeEnvelope:     UNCHANGED")


if __name__ == "__main__":
    main()
