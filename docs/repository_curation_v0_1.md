# SOGA Repository Curation v0.1

Status: Sprint 8 Launch Package

Purpose: Classify repository contents for external review, maintenance, and future evolution.

## Scope

This document identifies which components constitute the public SOGA architecture, which components serve as supporting demonstrations, and which components remain under review or historical retention.

This classification does not imply deletion.

Repository cleanup may occur after external architectural review.

## Classification Principles

The repository is organized around four categories:

- Public Core
- Public Proofs
- Review
- Historical Artifacts

The classification reflects architectural importance, not code quality.

A file may remain technically useful while being classified outside the Public Core.

## Public Core

The Public Core represents the reference implementation of the SOGA architecture.

These components define the architecture that external reviewers are evaluating.

### Mission Intake

- `intake/*`
- `builders/mission_builder.py`
- `intake/cmr_builder.py`
- `intake/cmr_source.py`

### Protocol Integration

- `input_adapters/*`
- `builders/protocol_projection.py`

### Runtime Envelope

- `verify/runtime_envelope.py`
- `verify/runtime_envelope_model.py`

### Subject State

- `engines/subject_capability_loader.py`
- `data/subjects/*`

### Advisory Evidence

- `advisory/*`

### Governance Core

- `verify/governance_pdp.py`
- `engines/runtime_governance_engine.py`
- `engines/runtime_dimension_evaluator.py`
- `engines/restrict_mode_selector.py`

### Canonical Decision Package

- `verify/canonical_decision_package.py`
- `verify/decision_package_builder.py`
- `engines/canonical_decision_package_adapter.py`

### Execution / PEP

- `execution/simple_pep.py`
- `engines/execution_orchestrator.py`
- `engines/restrict_execution_engine.py`

### Regression Suite

- `tools/run_use_case.py`
- `tools/cdp_regression.py`
- `use_cases/*`

### Launch Demonstrations

- `tools/protocol_independence_demo.py`
- `tools/subject_agency_state_demo.py`
- `tools/restrict_visibility_demo.py`
- `tools/mission_to_cdp_demo.py`
- `tools/multi_agent_cdp_demo.py`

## Public Proofs

These files provide supporting evidence for architectural claims but are not the primary launch path.

### Protocol Proofs

- `tools/aauth_runtime_envelope_v0_1_proof.py`
- `tools/ucan_runtime_envelope_v0_1_proof.py`
- `tools/zcap_runtime_envelope_v0_1_proof.py`

### Execution Proofs

- `tools/pep_end_to_end_proof.py`

### Consumer Proofs

- `monitor.py`

Purpose:

Demonstrate protocol independence, protocol normalization, execution enforcement, and CDP consumption.

These files are particularly relevant to protocol authors and ecosystem reviewers.

## Review

These files remain active or have active dependencies but require future evaluation before permanent classification.

### Dependency Review

- `verify/phase1b_core.py`

Reason:

Active dependencies remain. Removal or extraction has not yet been evaluated.

No repository changes should be made to this component until dependency analysis is complete.

## Historical Artifacts

These files remain available for historical reference but are not part of the Sprint 8 launch path.

### Historical Proofs

- `tools/input_adapter_proof.py`
- `tools/runtime_proof.py`
- `verify/run_demo.py`

Reason:

These files reflect earlier architectural phases and are superseded by the Runtime Envelope, Governance PDP, Canonical Decision Package, and current demonstration suite.

## Launch Position

External reviewers should focus on:

1. README
2. Specification
3. Launch Demonstrations
4. Service Map
5. Stable Interfaces
6. Governance Core
7. Regression Results

## Core Principle

The architecture is the product.

The repository exists to communicate, demonstrate, and validate the architecture.

