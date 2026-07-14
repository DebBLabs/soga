# Research Methodology
## Deb B Labs Research Program

This document defines the standing methodology for research conducted within the SOGA repository.

Its purpose is to preserve scientific rigor, repository integrity, and architectural discipline when humans and AI collaborators investigate external specifications, implementation behavior, and emerging architectural questions.

---

## 1. Repository Is Canonical

Repository artifacts take precedence over:

- conversation history
- AI memory
- summaries
- informal notes
- inferred project state

Before substantive work begins, collaborators shall inspect the repository and synchronize against:

- `knowledge/working/CURRENT_STATE.md`
- relevant specifications
- relevant implementation files
- current Git status and history

Conversation may support the work.

Conversation does not define repository truth.

---

## 2. Inspect Before Write

Before modifying an existing artifact:

1. Read the current artifact in full.
2. Inspect related implementation and documentation.
3. Identify the exact gap being addressed.
4. Preserve unrelated content.
5. Produce a complete replacement artifact when required by repository guardrails.

No artifact shall be rewritten from memory.

---

## 3. Primary Source Grounding

External architectural claims must follow G23 — Primary Source Grounding.

Before comparing an external specification, protocol, standard, implementation, or framework with SOGA:

1. Read foundational role, terminology, trust, and architectural definitions.
2. Read the relevant mechanisms, flows, appendices, and edge cases.
3. Compare the external work with SOGA only after those readings.
4. State whether the source was read directly and recently.
5. Preserve uncertainty where the source is incomplete, ambiguous, exploratory, or silent.

A citation alone is not grounding.

A search-result excerpt is not grounding.

A topic-driven partial reading is not sufficient grounding.

---

## 4. Evidence Classification

Every research artifact shall classify material using one of four evidence levels.

### Verified

Confirmed through one or more of:

- executed repository behavior
- committed repository artifacts
- primary specification text
- authoritative source documentation
- authoritative meeting transcript

Verified does not mean universally proven.

It means the statement is directly supported by the cited evidence.

### Observed

Reported, demonstrated, or discussed by another party but not independently verified.

Examples:

- a statement made during a meeting
- a demonstration viewed but not reproduced
- a claim made in Slack
- an architectural interpretation offered by an external participant

Observed material must not be promoted to Verified without independent confirmation.

### Hypothesis

A current architectural interpretation, possible explanation, mapping, or design direction under investigation.

Hypotheses may guide research.

They are not implementation requirements or canonical architecture.

### Future Research

An explicitly unresolved question requiring:

- additional primary-source review
- repository inspection
- experimentation
- implementation evidence
- external consultation

Future Research items belong in research artifacts or the backlog until formally authorized.

---

## 5. Research Is Not Architecture

Research findings do not become canonical architecture automatically.

Promotion into architecture requires:

1. Primary-source grounding where external work is involved.
2. Clear evidence classification.
3. Repository inspection.
4. Explicit Gate review.
5. Explicit authorization.
6. Documentation and implementation alignment.

A useful idea is not the same as an adopted design.

---

## 6. Research Is Not Implementation

The repository shall distinguish among:

- implemented behavior
- representative fixture behavior
- illustrative examples
- research hypotheses
- future work

Static fixtures shall not be described as live protocol integrations.

Representative mappings shall not be described as specification-verified unless they have been checked against the primary source.

Planned interfaces shall not be described as implemented.

---

## 7. Terminology Normalization

Terminology corrections shall be separated from architectural changes.

A terminology normalization pass may:

- correct transcription errors
- normalize protocol names
- align capitalization
- distinguish conventional terms from project-specific terms
- document unresolved naming questions

A terminology normalization pass shall not silently:

- move component boundaries
- alter runtime behavior
- rename canonical interfaces
- redefine architectural responsibilities

Examples requiring explicit verification include:

- AAuth, not AOTH
- AuthZEN capitalization
- KYAOS / CHAOS project naming
- conventional PAP, PDP, PEP, verifier, and validator terminology

---

## 8. Attribution Discipline

Research artifacts shall distinguish:

- what the repository demonstrates
- what Deb B Labs concludes
- what an external participant stated
- what an AI collaborator inferred

Meeting conclusions shall not be attributed to participants unless supported by the transcript or direct record.

Team preference shall not be represented as external agreement.

Discovery and contribution attribution shall remain accurate.

---

## 9. Protocol and Ecosystem Neutrality

SOGA remains protocol-neutral unless explicitly changed through architectural review.

Protocol-specific behavior belongs at adapter or projection boundaries.

The governance core shall not be altered merely to mirror one external ecosystem.

When protocols differ, the repository shall distinguish:

- verified protocol artifacts
- representative protocol evidence
- illustrative ecosystem context
- unverified mappings

---

## 10. Incremental Research Progression

Research should proceed through the following sequence:

Observation
→ Evidence classification
→ Primary-source review
→ Hypothesis
→ Experiment or implementation inspection
→ Gate review
→ Architectural proposal
→ Authorized implementation

Steps may reveal that no architectural change is required.

That is a valid research outcome.

---

## 11. Multi-AI Collaboration

AI collaborators may propose, challenge, inspect, and review.

No AI collaborator is authoritative.

When collaborators disagree:

1. Inspect the repository.
2. Read the primary source.
3. Identify the evidence level.
4. Preserve unresolved disagreement as research.
5. Escalate architectural promotion through Gate review.

The human principal retains final editorial and architectural authority.

---

## 12. Required Research Artifact Structure

New research artifacts should include:

- Purpose
- Scope
- Source status
- Verified findings
- Observed findings
- Hypotheses
- Future Research
- Architectural impact
- Implementation impact
- Open questions
- References or provenance

Sections may be omitted when genuinely inapplicable, but evidence levels must remain visible.

---

## 13. Repository Update Sequence

Documentation and research synchronization shall follow this order:

1. Inspect repository state.
2. Capture research artifacts.
3. Update backlog.
4. Update public documentation.
5. Update reviewer entry points.
6. Run repository and regression checks.
7. Complete Gate review.
8. Commit.
9. Update `CURRENT_STATE.md` last.
10. Commit the synchronized current state.

---

## Status

This methodology becomes the standing SOGA research methodology upon commit of this file.
