# SOGA Repository Inventory v0.1

Status: Initial architectural inventory  
Purpose: Explain what is currently in the repository and how it supports the SOGA mission-centric governance architecture.

## Repository Characterization

This repository is not a production service.

It is a SOGA governance architecture and implementation framework with executable proofs.

The current repository demonstrates how missions, mission steps, authority evidence, Subject Agency State, governance evaluation, Canonical Decision Packages, and reference execution outcomes fit together.

## Primary Architectural Flow

Use Case  
→ Mission  
→ Mission Steps  
→ Requirements / Guardrails  
→ Authority Evidence  
→ Runtime Envelope  
→ Governance PDP  
→ Canonical Decision Package  
→ Reference PEP / Execution Status

Protocols are not the primary organizing layer.

Protocols provide implementation evidence.

## Lifecycle Stages

- Mission Origination
- Mission Authorization
- Mission Execution
- Mission Tracking
- Mission Termination

## Top-Level Components

### `README.md`

Purpose: Public entry point for the repository.

Lifecycle Stage: All stages.

Architectural Role: Explains the core SOGA claim, current demonstrations, and protocol ecosystem alignment.

---

### `docs/`

Purpose: Architecture and specification documentation.

Lifecycle Stage: All stages.

Architectural Role: Defines SOGA concepts, service boundaries, stable interfaces, CDP structure, and repository scope.

Important files:

- `docs/START_HERE.md` — reader orientation
- `docs/canonical_decision_package_v0_1.md` — normative CDP specification
- `docs/service_map_v0_1.md` — maps service boundaries to files
- `docs/stable_interfaces_v0_1.md` — interface contracts
- `docs/repository_curation_v0_1.md` — public/review classification
- `docs/future_deployment_considerations_v0_1.md` — deployment boundaries
- `docs/agent_evidence_model_v0_1.md` — advisory evidence model
- `docs/mission_working_representation_v0_1.md` — mission representation model

---

### `missions/`

Purpose: Human-readable mission examples and source mission templates.

Lifecycle Stage: Mission Origination.

Inputs: Human intent, use case descriptions, mission statements.

Outputs: Mission artifacts usable by mission builders and proof scripts.

Architectural Role: Shows representative missions before runtime governance evaluation.

---

### `generated/`

Purpose: Generated mission JSON artifacts.

Lifecycle Stage: Mission Origination / Mission Authorization.

Inputs: Reference mission definitions.

Outputs: Structured mission JSON used by demos and regression flows.

Architectural Role: Provides concrete mission artifacts for execution-time governance tests.

---

### `use_cases/`

Purpose: Domain-specific use case definitions.

Lifecycle Stage: All stages.

Inputs: Representative domain scenarios.

Outputs: Use case JSON consumed by regression and runtime tooling.

Architectural Role: Provides the frozen regression corpus across banking, caregiver, emergency, enterprise, guardianship, insurance, medical appointments, research, shopping, and travel.

---

### `models/`

Purpose: Mission and intake data models.

Lifecycle Stage: Mission Origination / Mission Authorization.

Inputs: Mission intake and conversation state.

Outputs: Mission Working Representation and related model objects.

Architectural Role: Supports the transition from human intent into structured mission representation.

Important files:

- `models/mission_working_representation.py`
- `models/conversation_state.py`
- `models/intake_result.py`
- `models/validation_result.py`

---

### `intake/`

Purpose: Mission intake and validation layer.

Lifecycle Stage: Mission Origination.

Inputs: Human intent, mission text, intake source material.

Outputs: Canonical mission-related structures and validation results.

Architectural Role: Begins the mission pipeline before authorization or governance evaluation.

Important files:

- `intake/mission_intake_engine.py`
- `intake/mission_working_representation.py`
- `intake/cmr_builder.py`
- `intake/cmr_source.py`
- `intake/validation.py`
- `intake/glean.py`

---

### `builders/`

Purpose: Build mission templates and protocol-projected artifacts.

Lifecycle Stage: Mission Origination / Mission Authorization.

Inputs: Mission JSON, Mission Working Representation, reference mission data.

Outputs: Mission templates and protocol-shaped authority evidence.

Architectural Role: Bridges mission representation into governable structures.

Important files:

- `builders/mission_builder.py` — builds MissionTemplate objects from mission files.
- `builders/reference_mission_builder.py` — supports reference mission construction.
- `builders/protocol_projection.py` — projects mission authority evidence into protocol-shaped forms.

---

### `input_adapters/`

Purpose: Normalize protocol-shaped authority evidence into SOGA-compatible runtime inputs.

Lifecycle Stage: Mission Authorization.

Inputs: AAuth-shaped, UCAN-shaped, ZCAP-shaped, or sample authority artifacts.

Outputs: Runtime Envelope-compatible structures.

Architectural Role: Keeps SOGA protocol-independent.

Important files:

- `input_adapters/aauth_adapter.py`
- `input_adapters/ucan_adapter.py`
- `input_adapters/zcap_adapter.py`
- `input_adapters/sample_adapter.py`
- `input_adapters/notional_aauth_adapter.py`

---

### `verify/`

Purpose: Governance verification, runtime envelope, CDP, and PDP layer.

Lifecycle Stage: Mission Authorization / Mission Execution.

Inputs: Runtime Envelope, mission context, subject state, authority evidence.

Outputs: Governance decisions, Canonical Decision Packages, execution status objects.

Architectural Role: Contains the core governance determination logic and canonical output artifacts.

Important files:

- `verify/runtime_envelope.py`
- `verify/runtime_envelope_model.py`
- `verify/governance_pdp.py`
- `verify/canonical_decision_package.py`
- `verify/decision_package_builder.py`
- `verify/execution_status.py`
- `verify/mission_template.py`

---

### `engines/`

Purpose: Runtime orchestration and mission/governance engines.

Lifecycle Stage: All stages.

Inputs: Mission data, subject capability data, runtime context, authority evidence, advisory evidence.

Outputs: Mission execution structures, governance inputs, CDP-ready determinations, execution plans.

Architectural Role: Implements the larger mission-to-governance orchestration.

Key governance files:

- `engines/soga_runtime_engine.py`
- `engines/runtime_governance_engine.py`
- `engines/runtime_dimension_evaluator.py`
- `engines/restrict_mode_selector.py`
- `engines/canonical_decision_package_adapter.py`

Key mission files:

- `engines/mission_intake_engine.py`
- `engines/mission_execution_engine.py`
- `engines/mission_step_verifier.py`
- `engines/execution_plan_builder.py`
- `engines/cmr_compiler.py`
- `engines/mwr_updater.py`

Key evidence and capability files:

- `engines/authority_computation_engine.py`
- `engines/authority_requirement_mapper.py`
- `engines/capability_discovery_engine.py`
- `engines/capability_gap_engine.py`
- `engines/evidence_acquisition_engine.py`
- `engines/evidence_resolver.py`
- `engines/evidence_selection_engine.py`
- `engines/subject_capability_loader.py`

---

### `advisory/`

Purpose: Advisory agent evidence model.

Lifecycle Stage: Mission Authorization / Mission Execution.

Inputs: Advisory agent observations, confidence, disagreement, provenance.

Outputs: Advisory evidence structures for runtime governance evaluation.

Architectural Role: Allows agents to contribute evidence without becoming governance authorities.

Important files:

- `advisory/agent_evidence.py`
- `advisory/runtime_advisory_inputs.py`
- `advisory/advisory_dimension_evidence.py`
- `advisory/provenance_extension.py`

---

### `execution/`

Purpose: Reference PEP and execution layer.

Lifecycle Stage: Mission Execution / Mission Tracking.

Inputs: Governance decision or Canonical Decision Package.

Outputs: Execution status such as EXECUTING, HOLDING, or ABORTED.

Architectural Role: Demonstrates that downstream execution consumes governance decisions without reconstructing governance logic.

Important files:

- `execution/simple_pep.py`
- `execution/interface.py`
- `execution/provider_base.py`
- `execution/mock_adapter.py`
- `execution/providers/stub_provider.py`

---

### `data/subjects/`

Purpose: Reference subject data.

Lifecycle Stage: Mission Authorization / Mission Execution.

Inputs: Subject profile and capability information.

Outputs: Subject context used by governance and capability evaluation.

Architectural Role: Supports Subject Agency State and subject capability reasoning in reference scenarios.

---

### `tools/`

Purpose: Executable demos, proofs, and regression commands.

Lifecycle Stage: All stages.

Inputs: Missions, use cases, protocol-shaped evidence, subject state.

Outputs: Terminal demonstrations, JSON outputs, regression results.

Architectural Role: Provides executable evidence that the architecture works across key paths.

Primary reviewer commands:

- `tools/protocol_independence_demo.py`
- `tools/subject_agency_state_demo.py`
- `tools/mission_to_cdp_demo.py`
- `tools/pep_end_to_end_proof.py`
- `tools/cdp_regression.py`

Mission and intake proofs:

- `tools/mission_builder_proof.py`
- `tools/mission_end_to_end_proof.py`
- `tools/mission_projection_proof.py`
- `tools/mission_state_variation_proof.py`
- `tools/intake_demo.py`
- `tools/intake_end_to_end_demo.py`

Protocol proofs:

- `tools/aauth_runtime_envelope_v0_1_proof.py`
- `tools/ucan_runtime_envelope_v0_1_proof.py`
- `tools/zcap_runtime_envelope_v0_1_proof.py`
- `tools/pep_end_to_end_proof.py`

Regression and use case runners:

- `tools/run_use_case.py`
- `tools/cdp_regression.py`
- `tools/regression_baseline.py`

---

## Current Validation State

The following commands have been run successfully from the clean repository after copying missing dependencies:

```bash
python3 -m tools.protocol_independence_demo
python3 -m tools.subject_agency_state_demo
python3 -m tools.mission_to_cdp_demo
python3 -m tools.pep_end_to_end_proof
python3 -m tools.cdp_regression
Regression passed across ten use cases.

No known missing code dependency remains for the current proof paths.

Known Presentation Gap

The current demos are terminal-oriented and somewhat protocol-oriented.

The next presentation layer should be mission-oriented:

Use Case
→ Mission Steps
→ Requirements
→ Guardrails
→ Governance Result
→ Implementation Evidence

The protocol artifact should appear as supporting evidence, not as the primary navigation model.

Immediate Next Work

Before adding new functionality:

1. Commit the clean repository.
2. Push to DebBLabs/soga.
3. Fresh clone and rerun validation commands.
4. Then build a mission-step workbench using the existing code.

