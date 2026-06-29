# CURRENT STATE
## Deb B Labs Research Program

Last Updated: 2026-06-29

---

# Synchronization Contract

This document is the repository synchronization contract.

Every collaborator shall synchronize from this document before
beginning substantive work.

If additional repository documents are required, they are listed
under Required Reading.

Synchronization is complete only after this document and any listed
Required Reading have been reviewed.

---

# Repository Version

Branch: main
Commit: 71f78aa
Repository Status: RuntimeEnvelope Specification v0.1 committed. Sprint 9 authorized. Implementation not yet started.

---

# Current Program Phase

Program: Pre-July 16 Program
Phase: Phase 3 — Active
Gate: Repository synchronization before Sprint 9

---

# Current Sprint

Sprint: Sprint 9 — Governed Interaction Inputs
Research Question: What is the minimum information required to govern a Compaia interaction?
Status: Authorized. Not yet started.

---

# Regression Baseline

Current verified baseline:

- AAuth ACTIVE: ALLOW / EXECUTING
- UCAN ACTIVE: ALLOW / EXECUTING
- ZCAP ACTIVE: ALLOW / EXECUTING
- AAuth IMPAIRED: RESTRICT / HOLDING
- UCAN IMPAIRED: RESTRICT / HOLDING
- ZCAP IMPAIRED: RESTRICT / HOLDING

Regression command:

python3 -m tools.regression_baseline

Result:

All baseline cases passed.

---

# Changed Since Previous Sync

- AI Collaboration Guardrails created at knowledge/grounding/AI_COLLABORATION_GUARDRAILS.md.
- SESSION_BOOTSTRAP updated to distinguish orientation from operational guardrails.
- CURRENT_STATE designated as the repository synchronization contract.
- Session initialization protocol tested with Claude.
- Claude correctly reported lack of repository access and requested CURRENT_STATE.md only.
- Sprint 9 authorized but not started.
- Start-session packaging concept identified for future tooling; tool should package repository state, not generate it.

---

# Required Reading

- knowledge/grounding/SESSION_BOOTSTRAP.md
- knowledge/grounding/AI_COLLABORATION_GUARDRAILS.md

---

# Current Priorities

1. Finish repository synchronization updates.
2. Test CURRENT_STATE-based initialization with Claude.
3. Begin Sprint 9 after synchronization is confirmed.

---

# Open Risks

- State provenance remains an open research question.
- Per-hop governance evaluation remains future architecture under B-020.
- Protocol Projection remains an open verification item.
- Avoid allowing adapter work to collapse into governance logic.
- Avoid replacing existing repository structures before inspecting them.

---

# Immediate Next Action

Provide CURRENT_STATE.md and Required Reading artifacts to Claude and confirm synchronization before Sprint 9 begins.


---

# Sprint 9 Completion

Sprint 9 — Governed Interaction Inputs: COMPLETE.

Artifact:

- sprints/pre-july-16/sprint-9-governed-interaction-inputs.md

Research Outcome:

- Defined a provisional, optional, additive
  `execution_context.interaction_context`
  schema for Compaia interaction governance.

Repository Status:

- No executable code modified.
- No RuntimeEnvelope implementation changes.
- No adapter modifications.
- No regression modifications.

Regression Baseline:

Verified on 2026-06-29.

Results:

- AAuth ACTIVE → ALLOW / EXECUTING
- UCAN ACTIVE → ALLOW / EXECUTING
- ZCAP ACTIVE → ALLOW / EXECUTING
- AAuth IMPAIRED → RESTRICT / HOLDING
- UCAN IMPAIRED → RESTRICT / HOLDING
- ZCAP IMPAIRED → RESTRICT / HOLDING

All baseline cases passed.

Promotion Path:

- specifications/runtime-envelope/v0.1/interaction_context.md

Pending:

- Gate 2 implementation authorization before any Python changes.

