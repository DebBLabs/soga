# CURRENT STATE
## Deb B Labs Research Program

Last Updated: 2026-08-06

---

# Synchronization Contract

This document is the repository synchronization contract.

Every collaborator shall synchronize from this document before beginning
substantive work.

Repository artifacts take precedence over conversation, AI memory,
summaries, or discussion.

This document is the sole synchronization contract. Strategy artifacts
in `knowledge/strategy/` are subordinate to it and referenced by it.

---

## Repository HEAD

Current HEAD: ea27973

Repository HEAD is displayed by:

    git rev-parse --short HEAD

---

## Current Program Phase

Program: Embodied Governance Research Program
(per `knowledge/strategy/PROGRAM_CHARTER.md`)

Phase: Program Initialization

Active Sprint: G0 — Program Initialization

---

## Program Structure

- Program governance: continuous — `knowledge/strategy/PROGRAM_CHARTER.md`
- Continuous program tracks: Research, Implementation, Standards,
  Funding & Partnerships, Outreach — `knowledge/strategy/TRACKS.md`
- Research sprints: time-boxed —
  `knowledge/strategy/SPRINT_ROADMAP_G0_G30.md`
- Decisions: `knowledge/strategy/DECISION_LOG.md`

---

## Authorized Sprint Sequence

G0 → G24 → G25 → G26 → G27 → G28 → G29 → G30

(Definitions, entry criteria, and exit criteria in the sprint roadmap.)

---

## Last Completed Sprint

Repository Synchronization Sprint — COMPLETE (see prior CURRENT_STATE
revision for deliverables; G23 adopted, methodology established).

---

## Active Work

### G0 — Program Initialization
Status: ACTIVE — deliverables complete, awaiting Gate 1
Deliverables: strategy artifacts published; CURRENT_STATE.md amended;
HEAD field corrected; drift resolved; `live_governance_workbench.py`
dispositioned as a deferred, noncanonical exploratory artifact.
D-011 RESOLVED 2026-08-05 — conceptual clarification obtained via written
exchange with Dick Hardt. Governance is not a single function requiring an
attachment point; SOGA is the PS's governance policy.
Exit: Gate 1 verification (Claude, advisory) against the five criteria in the
sprint roadmap; next-sprint activation authorized by the PI.

---

## Stable Repository Architecture

Canonical execution pipeline (unchanged):

Mission Builder
→ Stage Gate
→ RuntimeEnvelope
→ Governance Policy Server
→ Canonical Decision Package
→ Capability Registry
→ REST / MCP / human execution surface

No architecture changed. No governance logic changed. No runtime
behavior changed.

---

## Research Methodology

`docs/RESEARCH_METHODOLOGY.md` — evidence classes: Verified, Observed,
Hypothesis, Future Research. Architectural changes are authorized only
after sufficient verified evidence.

---

## Repository Guardrails

G19 — Ecosystem Neutrality
G20 — Repository Documentation Integrity
G21 — Repository Artifact Fidelity
G22 — Execution Command Convention
G23 — Primary Source Grounding

---

## Immediate Next Action

Run Gate 1 verification and close G0.

Then resolve the roadmap conflict below before activating anything.

ROADMAP CONFLICT — PI decision required.
The authorized sequence is G24 then G25. On 2026-08-05 an external commitment
was made to Dick Hardt: permission endpoint implemented and one notional
mission run through it by end of August, followed by office hours or a call.
That is implementation work and maps to neither G24 nor G25 as written.
Either the roadmap moves or the commitment does. Do not slide silently.

Sprint scope changes from the 2026-08-05 findings:
- G24 thinner. PIC resolved (Nicola Gallo, Provenance Identity Continuity;
  already cited in the published threat model). AAuth office-hour
  reconciliation superseded by Dick Hardt's written answers.
- G25 partially satisfied from primary source. Remainder requires code.
- G26 narrower. Two of three candidate mission models eliminated: missions are
  immutable and have no steps, and evolve only through the mission log.

Findings: `knowledge/research/AAUTH_FINDINGS_2026-08-05.md`
