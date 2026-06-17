from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from verify.decision_package import DecisionPackage, GovernanceOutcome
from verify.mission_template import MissionLifecycle
from verify.runtime_envelope_model import RuntimeEnvelope, SubjectGovernanceState


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_receipt_id() -> str:
    return f"rcpt-{uuid4().hex[:12]}"


class GovernancePDP:
    """
    Minimal SOGA Governance PDP.

    This evaluator consumes a protocol-independent Runtime Envelope
    and produces a protocol-independent Decision Package.

    It is intentionally small and deterministic. It is not protocol-specific.
    """

    evaluator_version = "soga-governance-pdp-v0.1"

    def evaluate(self, envelope: RuntimeEnvelope) -> DecisionPackage:
        """
        Evaluate a Runtime Envelope and produce a Decision Package.
        """

        runtime_refs = {
            "request_id": envelope.request_id,
            "mission_id": envelope.mission.mission_id,
            "subject_id": envelope.subject.subject_id,
            "authority_id": envelope.authority.authority_id,
            "source_protocol": envelope.authority.source_protocol,
            "evaluated_at": now_iso(),
        }

        audit_refs = {
            "evaluator_version": self.evaluator_version,
            "receipt_id": new_receipt_id(),
        }

        # Terminal or structurally invalid mission lifecycle.
        if envelope.mission.lifecycle in {
            MissionLifecycle.COMPLETED,
            MissionLifecycle.ABANDONED,
        }:
            return DecisionPackage(
                request_id=envelope.request_id,
                receipt_id=audit_refs["receipt_id"],
                decision=GovernanceOutcome.DENY,
                reason_class="mission",
                rule="mission_lifecycle_not_executable",
                explanation=(
                    f"Mission lifecycle is {envelope.mission.lifecycle.value}; "
                    "execution is not legitimate for a completed or abandoned mission."
                ),
                constraints={},
                directives=["deny_execution"],
                runtime_references=runtime_refs,
                audit_references=audit_refs,
            )

        # Boundary subject governance state.
        if envelope.subject.governance_state == SubjectGovernanceState.LAPSED:
            return DecisionPackage(
                request_id=envelope.request_id,
                receipt_id=audit_refs["receipt_id"],
                decision=GovernanceOutcome.DENY,
                reason_class="subject_agency_state",
                rule="subject_agency_state_lapsed",
                explanation=(
                    "Subject Agency State is LAPSED; no formal delegable "
                    "governance authority remains to be exercised on behalf of the subject."
                ),
                constraints={},
                directives=["deny_execution"],
                runtime_references=runtime_refs,
                audit_references=audit_refs,
            )

        # Authority must cover the requested action.
        requested_action = str(envelope.execution_context.get("requested_action", ""))
        if requested_action and requested_action not in envelope.authority.allowed_actions:
            return DecisionPackage(
                request_id=envelope.request_id,
                receipt_id=audit_refs["receipt_id"],
                decision=GovernanceOutcome.DENY,
                reason_class="authority",
                rule="requested_action_not_authorized",
                explanation=(
                    f"Requested action '{requested_action}' is not included in "
                    "the normalized authority evidence."
                ),
                constraints={},
                directives=["deny_execution"],
                runtime_references=runtime_refs,
                audit_references=audit_refs,
            )

        # Restricted subject governance states preserve a continuation path.
        if envelope.subject.governance_state in {
            SubjectGovernanceState.SUPERVISED,
            SubjectGovernanceState.MANAGED,
            SubjectGovernanceState.DELEGATED,
        }:
            return DecisionPackage(
                request_id=envelope.request_id,
                receipt_id=audit_refs["receipt_id"],
                decision=GovernanceOutcome.RESTRICT,
                reason_class="subject_agency_state",
                rule="subject_agency_state_requires_constraints",
                explanation=(
                    f"Subject Agency State is {envelope.subject.governance_state.value}; "
                    "execution remains possible only under additional governance constraints."
                ),
                constraints={
                    "bounded_execution": True,
                    "restrict_mode": "SUPERVISED_EXECUTION",
                    "subject_agency_state": envelope.subject.governance_state.value,
                },
                directives=["require_supervision"],
                runtime_references=runtime_refs,
                audit_references=audit_refs,
            )

        # Default allow for active mission, valid authority, and independent subject governance.
        return DecisionPackage(
            request_id=envelope.request_id,
            receipt_id=audit_refs["receipt_id"],
            decision=GovernanceOutcome.ALLOW,
            reason_class="policy",
            rule="default_allow",
            explanation="No governance condition presently prevents execution.",
            constraints={},
            directives=[],
            runtime_references=runtime_refs,
            audit_references=audit_refs,
        )
