# AI Collaboration Guardrails
## Deb B Labs Research Program

Last Updated: 2026-06-29

---

## Purpose

These guardrails define how AI collaborators operate within the Deb B Labs research program.

SESSION_BOOTSTRAP.md orients collaborators to the project.

This document governs how collaborators work once research begins.

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

Only introduce new architecture when a genuine gap prevents progress toward the North Star.

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

When uncertainty exists, inspect the repository before relying on conversational memory.

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

Gate reviews occur before program transitions.

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

Elegant redesign is never sufficient reason to replace working architecture.

Understand first.

Extend second.

Redesign only when evidence requires it.

---

## G15 — Repository Execution Discipline

When the repository owner directs an AI collaborator to proceed with an authorized repository task, the collaborator shall produce repository-ready artifacts rather than procedural descriptions.

Specifically:

- Provide complete `cat <<'EOF'` statements for new or modified repository files whenever practical.
- Provide exact shell commands in execution order.
- Do not require the repository owner to reconstruct commands or infer intermediate steps.
- Do not replace executable repository instructions with narrative explanations.
- If execution depends on the result of a previous command, stop at that checkpoint and wait for the result before producing subsequent repository modifications.
- Repository execution artifacts should be copy/paste ready.

The objective is to minimize operator cognitive load and preserve reproducible repository operations.

---

## Operational Command — Apply Guardrails

When the repository owner issues:

Apply Guardrails

Every AI collaborator shall:

1. Pause substantive work.
2. Re-evaluate the current response against these guardrails.
3. Identify drift or guardrail violations.
4. Correct course without introducing new architecture, process, or implementation work.
5. Resume from the corrected position.

---

## Closing Principle

The repository governs the work.

The program governs the sequence.

The gates govern quality.

The human governs the repository.


---

## G16 — Human Repository Authority

AI collaborators perform analysis, inspection, planning,
implementation, and gate reviews.

Their approvals are recommendations.

Repository state changes only through explicit authorization
by the Repository Curator.

Gate approval does not close a sprint.

Repository closeout is a human curatorial act.

CURRENT_STATE.md shall reflect only repository state that has
been explicitly authorized by the Repository Curator.

