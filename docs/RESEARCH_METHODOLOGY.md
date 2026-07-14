# SOGA Research Methodology

Version: 1.0

Status: Adopted

This methodology defines how research is conducted before architectural change is proposed within SOGA.

Repository architecture shall evolve from verified evidence rather than assumption, intuition, or accumulated discussion.

---

# Research Sequence

All research follows the same progression.

1. Investigate
2. Observe
3. Form Hypotheses
4. Verify
5. Propose
6. Review
7. Authorize
8. Implement
9. Validate

No step may be skipped.

---

## Phase 1 — Investigate

Research begins with inspection.

Sources may include:

- primary specifications
- repository inspection
- executable behavior
- authoritative transcripts
- published papers
- implementation code

Research begins by understanding existing work before proposing new work.

---

## Phase 2 — Observe

Record what is actually present.

Observations describe existing facts.

Observations do not explain.

Observations do not predict.

Observations do not redesign.

---

## Phase 3 — Hypothesize

Hypotheses explain observations.

Hypotheses remain provisional until verified.

Multiple competing hypotheses may coexist.

---

## Phase 4 — Verify

Verification requires evidence.

Evidence may include:

- primary-source specifications
- repository execution
- repository artifacts
- implementation inspection
- reproduced experiments
- authoritative transcripts

Secondary summaries alone are insufficient.

---

## Phase 5 — Propose

Only verified evidence may support architectural proposals.

Proposals shall distinguish:

- existing architecture
- proposed architecture
- research direction

---

## Phase 6 — Review

Architectural proposals undergo review before implementation.

Review may include:

- repository gate review
- standards discussion
- external expert feedback
- implementation feasibility

Review does not authorize implementation.

---

## Phase 7 — Authorization

Implementation begins only after explicit authorization.

Research alone does not authorize implementation.

Discussion alone does not authorize implementation.

Hypotheses alone do not authorize implementation.

---

## Phase 8 — Implementation

Implementation follows approved architecture.

Repository commits shall not silently introduce architectural change.

Architectural changes shall be documented.

---

## Phase 9 — Validation

Validation confirms that implementation matches the approved architecture.

Validation includes:

- repository inspection
- demonstrations
- regression testing
- documentation synchronization

---

# Evidence Classification

Every research claim shall be classified.

## Verified

Confirmed through one or more of:

- primary specification
- executed repository behavior
- canonical repository artifact
- authoritative transcript

---

## Observed

Presented or demonstrated by another party but not independently verified.

---

## Hypothesis

Architectural interpretation under investigation.

Not yet verified.

---

## Future Research

Open question requiring additional investigation.

No architectural conclusion has been reached.

---

# Primary Source Grounding

Architectural comparison with external work requires direct reading of the primary source.

Required sequence:

1. Read foundational architecture and terminology.
2. Read mechanisms and interaction flows.
3. Compare with SOGA.
4. State whether the primary source was read directly and recently.
5. Preserve uncertainty where the source is incomplete or exploratory.

Primary-source grounding is mandatory before architectural comparison.

---

# Repository Discipline

Repository artifacts take precedence over:

- conversation
- summaries
- AI memory
- inference

Research artifacts do not modify architecture.

Backlog items do not modify architecture.

Meeting notes do not modify architecture.

Architecture changes require explicit authorization.

---

# Standing Principles

Research before architecture.

Inspection before implementation.

Evidence before conclusions.

Verification before promotion.

Authorization before change.

Synchronization before new work.

---

## Status

This methodology becomes the standing SOGA research methodology upon commit of this file.

