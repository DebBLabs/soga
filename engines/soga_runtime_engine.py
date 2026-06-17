from engines.authority_computation_engine import (
    AuthorityComputationEngine,
)
from engines.capability_gap_engine import (
    CapabilityGapEngine,
)
from engines.canonical_decision_package_adapter import (
    CanonicalDecisionPackageAdapter,
)
from engines.evidence_acquisition_engine import (
    EvidenceAcquisitionEngine,
)
from engines.evidence_justification_engine import (
    EvidenceJustificationEngine,
)
from engines.evidence_selection_engine import (
    EvidenceSelectionEngine,
)
from engines.execution_orchestrator import (
    ExecutionOrchestrator,
)
from engines.mission_execution_engine import (
    MissionExecutionEngine,
)
from engines.mission_intake_engine import (
    MissionIntakeEngine,
)
from engines.runtime_acquisition_planner import (
    RuntimeAcquisitionPlanner,
)
from engines.runtime_governance_engine import (
    RuntimeGovernanceEngine,
)
from engines.subject_capability_loader import (
    SubjectCapabilityLoader,
)


class SOGARuntimeEngine:
    """
    Canonical SOGA runtime pipeline.
    """

    def execute(
        self,
        request,
        answers,
        available_evidence,
        runtime=None,
    ):

        cmr = MissionIntakeEngine().run(
            request,
            answers,
        )

        return self.execute_cmr(
            cmr,
            available_evidence,
            runtime=runtime,
        )

    def execute_cmr(
        self,
        cmr,
        available_evidence,
        runtime=None,
    ):

        runtime = runtime or {}

        if "authority" in runtime:
            runtime = dict(runtime)
            runtime["authority"] = (
                AuthorityComputationEngine()
                .compute(runtime["authority"])
            )

        subject_id = cmr["subject"]["subject_id"]

        standing_capabilities = (
            SubjectCapabilityLoader()
            .load(subject_id)
        )

        execution = MissionExecutionEngine().execute(
            cmr,
            standing_capabilities,
            available_evidence,
        )

        evidence_selection = (
            EvidenceSelectionEngine()
            .select(
                execution["evidence_resolution"]
            )
        )

        evidence_justification = (
            EvidenceJustificationEngine()
            .justify(
                evidence_selection
            )
        )

        acquisition = (
            EvidenceAcquisitionEngine()
            .acquire(
                execution["step_verdicts"],
                execution["evidence_resolution"],
            )
        )

        gap_report = (
            CapabilityGapEngine()
            .analyze(
                execution,
                acquisition,
            )
        )

        runtime_plan = (
            RuntimeAcquisitionPlanner()
            .plan(
                gap_report
            )
        )

        governance_decisions = (
            RuntimeGovernanceEngine()
            .evaluate(
                runtime_plan,
                evidence_selection=evidence_selection,
                runtime=runtime,
            )
        )

        receipts = (
            ExecutionOrchestrator()
            .run(
                cmr,
                standing_capabilities,
                available_evidence,
                governance_decisions=governance_decisions,
            )
        )

        canonical_decision_packages = (
            CanonicalDecisionPackageAdapter()
            .build_many(
                decisions=governance_decisions,
                cmr=cmr,
                runtime=runtime,
                receipts=receipts["receipts"],
            )
        )

        return {
            "mission": cmr,
            "subject_id": subject_id,
            "standing_capabilities": standing_capabilities,
            "execution": execution,
            "evidence_selection": evidence_selection,
            "evidence_justification": evidence_justification,
            "acquisition": acquisition,
            "capability_gap_report": gap_report,
            "runtime_plan": runtime_plan,
            "governance_decisions": governance_decisions,
            "canonical_decision_packages": canonical_decision_packages,
            "receipts": receipts["receipts"],
            "runtime": runtime,
        }
