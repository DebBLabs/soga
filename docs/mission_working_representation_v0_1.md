# Mission Working Representation (MWR) v0.1

Status: Sprint 6 Working Model

## Purpose

The Mission Working Representation (MWR) is a transient reasoning artifact used by the Mission Intake Engine to transform Human Intent into a Canonical Mission Representation (CMR).

The MWR is NOT a governance artifact.

The MWR SHALL NOT:
- determine governance
- determine authority
- determine Subject Agency State
- predict Governance PDP outcomes

## Lifecycle

Human Intent
    ↓
Candidate Observations
    ↓
Glean
    ↓
MWR
    ↓
Validation
    ↓
CMR
    ↓
MWR destroyed

MWR survives only under explicit debug or audit mode.

## Fields

- original_request
- candidate_observations
- inferred_subject
- inferred_delegates
- inferred_resources
- inferred_allowed_actions
- inferred_forbidden_actions
- inferred_bounds
- unresolved_questions
- confidence_notes
- sector_knowledge_used

The MWR is a reasoning workspace, not a runtime artifact.
