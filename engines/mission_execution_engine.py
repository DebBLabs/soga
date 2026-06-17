from engines.execution_plan_builder import (
    ExecutionPlanBuilder,
)
from engines.authority_requirement_mapper import (
    AuthorityRequirementMapper,
)
from engines.capability_discovery_engine import (
    CapabilityDiscoveryEngine,
)
from engines.evidence_resolver import (
    EvidenceResolver,
)
from engines.mission_step_verifier import (
    MissionStepVerifier,
)


class MissionExecutionEngine:

    def execute(
        self,
        cmr,
        standing_capabilities,
        available_evidence,
    ):

        execution_plan = (
            ExecutionPlanBuilder()
            .build(cmr)
        )

        authority_requirements = (
            AuthorityRequirementMapper()
            .map(cmr)
        )

        capability_discovery = (
            CapabilityDiscoveryEngine()
            .discover(
                execution_plan,
                standing_capabilities,
            )
        )

        evidence_resolution = (
            EvidenceResolver()
            .resolve(
                authority_requirements,
                available_evidence,
                standing_capabilities,
            )
        )

        step_verdicts = (
            MissionStepVerifier()
            .verify(
                evidence_resolution,
            )
        )

        return {
            "mission_id":
                cmr["mission_id"],
            "execution_plan":
                execution_plan,
            "capability_discovery":
                capability_discovery,
            "authority_requirements":
                authority_requirements,
            "evidence_resolution":
                evidence_resolution,
            "step_verdicts":
                step_verdicts,
        }
