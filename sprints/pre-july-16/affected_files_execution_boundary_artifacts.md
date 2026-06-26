# Affected Files — Execution Boundary Architectural Artifacts

Date: 2026-06-27

Status: Draft for Gate 1 Review

---

## Purpose

This plan defines the next implementation work after repository-memory setup.

The work must treat the execution boundary as a first-class architectural artifact.

The Mission Planning Workbench and Governance Decision Workbench are not UI panels or pages. They are visualizations of two separate architectural components.

Implementation must not run ahead of the locked constitutional and architectural files:

- knowledge/constitution/PROJECT_CONSTITUTION.md
- knowledge/constitution/ARCHITECTURE_PRINCIPLES.md

---

## Locked Architectural Constraints

The following constraints are binding.

1. Mission Builder owns planning.

2. Runtime/Orchestrator owns execution requests.

3. SOGA owns execution-time governance.

4. Execution Layer owns carrying out or refusing the action.

5. Mission Planning Workbench visualizes pre-execution mission planning.

6. Governance Decision Workbench visualizes execution-boundary governance.

7. Mission Builder does not produce governance outputs.

8. Governance Decision Workbench evaluates one execution request at a time.

9. Protocol artifacts are evidence, not governance decisions.

10. One execution event maps to exactly one Canonical Decision Package.

---

## Task 2 — Execution Boundary Artifact

### Objective

Define an explicit architectural artifact representing the execution boundary.

This artifact should show the transition from mission planning to runtime governance.

### Candidate Files

Create or update:

- docs/execution_boundary_artifact_v0_1.md
- docs/stable_interfaces_v0_1.md
- docs/service_map_v0_1.md
- knowledge/working/CURRENT_STATE.md
- knowledge/working/IMPLEMENTATION_STATUS.md

### Possible Code Impact

Do not implement yet without Gate 1 approval.

Potential future files:

- engines/execution_orchestrator.py
- engines/runtime_governance_engine.py
- execution/interface.py
- verify/runtime_envelope_model.py

---

## Task 4 — Two Workbench Architectural Artifacts

### Objective

Define the Mission Planning Workbench and Governance Decision Workbench as architectural views of distinct system responsibilities.

Do not implement as UI panels first.

### Candidate Files

Create or update:

- docs/mission_planning_workbench_artifact_v0_1.md
- docs/governance_decision_workbench_artifact_v0_1.md
- docs/governance_overview.md
- docs/north_star_governance_lifecycle.md
- web/mission_planning_workbench.html
- web/governance_workbench.html

### Possible Code Impact

Do not implement yet without Gate 1 approval.

Potential future files:

- tools/build_mission_planning_workbench_ui.py
- tools/build_governance_workbench_ui.py
- tools/governance_workbench.py
- tools/workbench.py

---

## AAuth Integration Boundary

The AAuth integration is external evidence and execution context.

Current working implementation remains in:

- external-repos/aauth-full-demo/backend/app/services/a2a_service.py
- external-repos/aauth-full-demo/backend/app/services/soga_governance_stub.py

This should not drive the core SOGA architecture.

It is an implementation demonstration of the execution boundary, not the source of architectural truth.

---

## Gate 1 Questions

1. Are these the correct affected files for Tasks 2 and 4?

2. Should Task 2 produce only documentation first, or should it include a reference Python artifact model?

3. Should Task 4 update existing workbench files or create new artifact documents first?

4. Is replacement of the AAuth stub part of pre-sprint closeout, or the first Sprint 8 task?

5. Should the Mission Builder ownership proposal be resolved before these artifacts are finalized?

---

## Recommendation

Proceed in this order:

1. Gate 1 confirms affected files.

2. Create execution-boundary artifact document.

3. Create two workbench artifact documents.

4. Update working state.

5. Run regression.

6. Only then resume code implementation.

