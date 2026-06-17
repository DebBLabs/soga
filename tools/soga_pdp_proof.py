from __future__ import annotations

import json

from verify.governance_pdp import GovernancePDP
from verify.mission_template import MissionLifecycle, MissionTemplate
from verify.runtime_envelope_model import (
    AuthorityEvidence,
    Reachability,
    RuntimeEnvelope,
    SubjectGovernanceState,
    SubjectState,
)


def build_envelope(governance_state: SubjectGovernanceState) -> RuntimeEnvelope:
    mission = MissionTemplate(
        mission_id="mission-soga-proof-001",
        lifecycle=MissionLifecycle.ACTIVE,
        subject_id="subject-001",
        objective="Demonstrate protocol-independent execution-time governance.",
        allowed_actions=["step1"],
    )

    authority = AuthorityEvidence(
        authority_id="authority-soga-proof-001",
        authority_type="capability",
        allowed_actions=["step1"],
        source_protocol="notional",
        references={"demo": "soga_pdp_proof"},
    )

    subject = SubjectState(
        subject_id="subject-001",
        governance_state=governance_state,
        reachability=Reachability.REACHABLE,
    )

    return RuntimeEnvelope(
        request_id=f"req-{governance_state.value.lower()}",
        mission=mission,
        authority=authority,
        subject=subject,
        execution_context={"requested_action": "step1"},
        policy={"profile": "soga-baseline-v0.1"},
    )


def print_case(title: str, envelope: RuntimeEnvelope) -> None:
    pdp = GovernancePDP()
    decision = pdp.evaluate(envelope)

    print(title)
    print("-" * len(title))
    print(json.dumps(decision.to_dict(), indent=2))
    print()


def main() -> None:
    print("SOGA PDP Proof")
    print("==============")
    print("Same mission.")
    print("Same authority.")
    print("Same requested action.")
    print("Different Subject Governance State.")
    print("Different Decision Package.")
    print()

    print_case(
        "CASE 1: INDEPENDENT subject",
        build_envelope(SubjectGovernanceState.INDEPENDENT),
    )

    print_case(
        "CASE 2: SUPERVISED subject",
        build_envelope(SubjectGovernanceState.SUPERVISED),
    )

    print_case(
        "CASE 3: LAPSED subject",
        build_envelope(SubjectGovernanceState.LAPSED),
    )


if __name__ == "__main__":
    main()
