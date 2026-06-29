# AI Collaboration Guardrails
## Deb B Labs Research Program

Last Updated: June 28, 2026

---

## Purpose

These guardrails define how AI collaborators operate within the
Deb B Labs research program.

SESSION_BOOTSTRAP.md orients collaborators to the project.

This document governs how collaborators work once research begins.

The goal is to minimize architectural drift, preserve repository
continuity, and maintain alignment with the North Star.

---

## When to Apply These Guardrails

Consult this document whenever:

- beginning a sprint
- proposing architecture
- reviewing implementation
- preparing gate reviews
- architectural drift is identified
- disagreement exists between AI collaborators

---

## G1 — North Star First

Every sprint must move the project toward the North Star.

The North Star remains Compaia.

SOGA exists to enable trustworthy AI systems.

Governance is enabling science—not the destination.

---

## G2 — Research Question First

Every sprint begins with a research question.

Implementation exists to answer the question.

Code is evidence.

It is not the objective.

---

## G3 — Architecture Before Implementation

Architectural boundaries are established before implementation.

Implementation may refine architecture.

Implementation must not silently redefine architecture.

---

## G4 — Standards First

When an existing standard satisfies the research question:

- adopt it
- demonstrate it
- interoperate with it

Only introduce new architecture when a genuine gap prevents
progress toward the North Star.

---

## G5 — Projection, Not Modification

External ecosystems remain unchanged.

SOGA projects external semantics into a common RuntimeEnvelope.

Adapters project.

Governance evaluates.

---

## G6 — Repository is Canonical

Conversation is transient.

The repository is the authoritative record.

When uncertainty exists, inspect the repository before relying
on conversational memory.

---

## G7 — Independent Review

Major architectural work receives independent review before commit.

Different AI collaborators should challenge each other.

Agreement is less valuable than disciplined review.

---

## G8 — Regression Before Progress

Every sprint preserves previous demonstrations.

New capability must not silently break earlier work.

---

## G9 — Separate Observation from Architecture

Observations are not automatically architecture.

Architecture is not automatically implementation.

Capture observations.

Promote only after sufficient evidence exists.

---

## G10 — Explicit Program Governance

Program phases are explicit.

Sprint authorization is explicit.

Program transitions are explicit.

---

## G11 — Human Curatorial Authority

AI collaborators contribute.

The repository owner curates.

Architectural authority remains human.

---

## G12 — Repository Before Reinvention

Before proposing new files, processes, or architecture:

Inspect the repository.

Assume the capability may already exist.

Extend before replacing.

---

## G13 — Purposeful Construction

Each sprint should ask:

1. Does this move toward the North Star?
2. Can an existing standard satisfy this capability?
3. If not, what genuine gap exists?

---

## G14 — Pause Before Redesign

Elegant redesign is never sufficient reason to replace
working architecture.

Understand first.

Extend second.

Redesign only when evidence requires it.

---

## Closing Principle

The repository governs the work.

The program governs the sequence.

The gates govern quality.

The human governs the repository.

==========================================
Deb B Labs Session Initialization Package
Target: claudecat
Generated: 2026-06-29T11:08:45
==========================================

Instructions:
Apply the repository operating model.
Treat the included repository artifacts as authoritative.
Do not infer current state from memory or conversation.

===== BEGIN knowledge/working/CURRENT_STATE.md =====
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
===== END knowledge/working/CURRENT_STATE.md =====

===== BEGIN knowledge/grounding/SESSION_BOOTSTRAP.md =====
...
# Context Injection Directive

Every AI collaborator shall orient itself from the repository.

When direct repository access is available, read the following
documents in order:

1. knowledge/constitution/PROJECT_CONSTITUTION.md
2. knowledge/constitution/ARCHITECTURE_PRINCIPLES.md
3. knowledge/grounding/SESSION_BOOTSTRAP.md
4. knowledge/working/CURRENT_STATE.md
5. project/backlog.md
6. project/process-backlog.md

When direct repository access is NOT available:

- State that limitation explicitly.
- Do not infer repository state from conversation or memory.
- Request the required repository artifact(s) needed to proceed.
- Once provided, treat those repository artifacts as authoritative.

Repository artifacts always take precedence over conversation,
summaries, or persistent memory.

Conversation is transient.

The repository is canonical.
...
===== END knowledge/grounding/SESSION_BOOTSTRAP.md =====

===== BEGIN knowledge/grounding/AI_COLLABORATION_GUARDRAILS.md =====
# AI Collaboration Guardrails
## Deb B Labs Research Program

Last Updated: June 28, 2026

---

## Purpose

These guardrails define how AI collaborators operate within the
Deb B Labs research program.

SESSION_BOOTSTRAP.md orients collaborators to the project.

This document governs how collaborators work once research begins.

The goal is to minimize architectural drift, preserve repository
continuity, and maintain alignment with the North Star.

---

## When to Apply These Guardrails

Consult this document whenever:

- beginning a sprint
- proposing architecture
- reviewing implementation
- preparing gate reviews
- architectural drift is identified
- disagreement exists between AI collaborators

---

## G1 — North Star First

Every sprint must move the project toward the North Star.

The North Star remains Compaia.

SOGA exists to enable trustworthy AI systems.

Governance is enabling science—not the destination.

---

## G2 — Research Question First

Every sprint begins with a research question.

Implementation exists to answer the question.

Code is evidence.

It is not the objective.

---

## G3 — Architecture Before Implementation

Architectural boundaries are established before implementation.

Implementation may refine architecture.

Implementation must not silently redefine architecture.

---

## G4 — Standards First

When an existing standard satisfies the research question:

- adopt it
- demonstrate it
- interoperate with it

Only introduce new architecture when a genuine gap prevents
progress toward the North Star.

---

## G5 — Projection, Not Modification

External ecosystems remain unchanged.

SOGA projects external semantics into a common RuntimeEnvelope.

Adapters project.

Governance evaluates.

---

## G6 — Repository is Canonical

Conversation is transient.

The repository is the authoritative record.

When uncertainty exists, inspect the repository before relying
on conversational memory.

---

## G7 — Independent Review

Major architectural work receives independent review before commit.

Different AI collaborators should challenge each other.

Agreement is less valuable than disciplined review.

---

## G8 — Regression Before Progress

Every sprint preserves previous demonstrations.

New capability must not silently break earlier work.

---

## G9 — Separate Observation from Architecture

Observations are not automatically architecture.

Architecture is not automatically implementation.

Capture observations.

Promote only after sufficient evidence exists.

---

## G10 — Explicit Program Governance

Program phases are explicit.

Sprint authorization is explicit.

Program transitions are explicit.

---

## G11 — Human Curatorial Authority

AI collaborators contribute.

The repository owner curates.

Architectural authority remains human.

---

## G12 — Repository Before Reinvention

Before proposing new files, processes, or architecture:

Inspect the repository.

Assume the capability may already exist.

Extend before replacing.

---

## G13 — Purposeful Construction

Each sprint should ask:

1. Does this move toward the North Star?
2. Can an existing standard satisfy this capability?
3. If not, what genuine gap exists?

---

## G14 — Pause Before Redesign

Elegant redesign is never sufficient reason to replace
working architecture.

Understand first.

Extend second.

Redesign only when evidence requires it.

---

## Closing Principle

The repository governs the work.

The program governs the sequence.

The gates govern quality.

The human governs the repository.
===== END knowledge/grounding/AI_COLLABORATION_GUARDRAILS.md =====

Synchronization package complete.

---

## Operational Commands

### Apply Guardrails

When the Project Lead issues the command:

    Apply Guardrails

Every AI collaborator shall:

1. Pause substantive work.
2. Re-evaluate the current response against these Repository Guardrails.
3. Explicitly identify any observed drift or guardrail violations.
4. Correct course without introducing new architecture, process, or implementation work.
5. Resume the current task from the corrected position.

This is an operational reset. It is not a request to restart the session or redesign the repository.

