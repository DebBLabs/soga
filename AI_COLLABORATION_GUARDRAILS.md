# AI Collaboration Guardrails
## Deb B Labs Research Program

This document records formally adopted guardrails governing AI-assisted research and repository work.

Repository artifacts are authoritative over conversation, AI memory, summaries, or inference.

---

## G19 — Ecosystem Neutrality

SOGA shall remain protocol-neutral.

External ecosystems may provide authority evidence.

They shall not become implicit architectural dependencies without explicit authorization.

---

## G20 — Repository Documentation Integrity

Repository documentation shall accurately reflect the implemented repository.

Research, proposals, and future ideas shall not be presented as implemented architecture.

---

## G21 — Repository Artifact Fidelity

Repository artifacts shall be generated as complete replacement files.

Repository artifacts shall:

- be complete
- preserve internal consistency
- be immediately pasteable
- require no manual reconstruction

Fragments, partial edits, or mixed narrative are not acceptable repository artifacts.

---

## G22 — Execution Command Convention

Repository execution commands shall be documented using the repository's canonical command form.

Examples shall match executable repository behavior.

---

## G23 — Primary Source Grounding

No architectural claim about an external specification, protocol, standard, or published framework may be built solely on memory, inference, secondary summaries, or partial topic-driven reading.

### Origin

During AAuth and SOGA alignment work, AI collaborators operated for an extended period using a plausible, internally consistent, and partly incorrect model of AAuth's Person Server.

The incorrect model remained convincing until the primary specification was read directly.

This guardrail was adopted to prevent similar failures.

### Required Sequence

Before producing architectural comparisons or implementation recommendations involving external work:

1. Read foundational terminology and architecture.
2. Read relevant mechanisms and interaction flows.
3. Compare with SOGA.
4. State whether the primary source was read directly and recently.
5. Classify unverified conclusions as provisional.
6. Preserve uncertainty where the source is incomplete or exploratory.

### Evidence Discipline

The following are not sufficient grounding:

- citations alone
- remembered definitions
- search-result excerpts
- partial or topic-driven reading

Primary Source Grounding requires direct reading of the relevant source.

### Required Classification

Claims involving external work shall be classified as:

- Verified
- Observed
- Hypothesis
- Future Research

### Applies To

This guardrail applies to all AI collaborators and all external specifications, standards, implementations, research papers, presentations, and published documentation.

It is not limited to AAuth.

---

## Status

These guardrails govern repository research and architectural work upon commit of this file.

