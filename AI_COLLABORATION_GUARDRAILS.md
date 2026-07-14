# AI Collaboration Guardrails
## Deb B Labs Research Program

This document records formally adopted guardrails governing AI-assisted research and repository work.

Repository artifacts are authoritative over conversation, AI memory, summaries, or inference.

Guardrails G19–G22 are already committed and referenced in `knowledge/working/CURRENT_STATE.md`.

This document adds G23.

---

## G23 — Primary Source Grounding

No architectural claim about an external specification, protocol, standard, or published framework may be built solely on memory, general knowledge, inference, secondary summaries, or partial topic-driven reading.

### Origin

During AAuth and SOGA alignment work, AI collaborators operated for an extended period using a plausible, internally consistent, and partly incorrect model of AAuth's Person Server.

The Person Server was initially treated as resource-scoped.

The primary specification defines it as person-scoped: the person chooses the Person Server, and that server may operate across the person's agents and missions.

The incorrect model remained convincing until the foundational specification text was read directly.

### Required Sequence

Before producing an architectural claim, comparison, diagram, mapping, or implementation recommendation involving an external source:

1. Read the source's foundational role, terminology, trust, and architectural definitions first.
2. Read the relevant mechanisms, flows, appendices, and edge cases second.
3. Compare the external architecture with SOGA only after completing those readings.
4. State plainly whether the primary source was read directly and recently.
5. If the source was not read directly and recently, classify the claim as unverified and provisional.
6. Preserve uncertainty where the source itself is incomplete, ambiguous, exploratory, or silent.

### Evidence Discipline

A citation alone is not grounding.

A previously fetched definition recalled from memory is not grounding.

A search-result excerpt is not grounding.

A topic-driven reading that skips foundational definitions is not sufficient grounding.

Primary Source Grounding requires a current, direct reading of the relevant source architecture and mechanisms.

### Required Classification

Claims involving external work shall be classified as one of:

- **Verified** — confirmed through primary specification text, executed repository behavior, canonical repository artifacts, or an authoritative transcript.
- **Observed** — stated, demonstrated, or discussed by another party but not independently verified.
- **Hypothesis** — an architectural interpretation or proposed explanation under investigation.
- **Future Research** — explicitly unresolved and requiring further inspection, experimentation, or primary-source review.

### Applies To

This guardrail applies to all AI collaborators and all external material, including specifications, protocols, standards, implementations, research papers, presentations, and published documentation.

It is not limited to AAuth.

---

## Status

G23 is formally adopted for repository and research work upon commit of this file.
