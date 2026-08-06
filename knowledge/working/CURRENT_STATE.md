# CURRENT STATE
## Deb B Labs Research Program

Last Updated: 2026-07-20

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

Current HEAD: (set to the G0 initialization commit hash at commit time)

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

Status: ACTIVE

Deliverables: strategy artifacts published; CURRENT_STATE.md amended
(this revision); HEAD field corrected; drift resolved;
`live_governance_workbench.py` formally dispositioned as a deferred,
noncanonical exploratory artifact pending conceptual clarification and
discussion with Dick Hardt (D-011).

Exit: Gate 1 verification (Claude, advisory) against the five criteria
in the sprint roadmap; G24 activation authorized by the PI.

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

Complete G0 deliverables, run Gate 1 verification, and upon PI
authorization activate G24 (Research Synchronization: PIC report and
feedback, Why PIC review, AAuth office-hour reconciliation, research
notes synchronization).

The AAuth Integration Investigation (G25) remains the first
inspection-phase objective and follows G24.

---
## Session Addendum — 2026-08-05

D-011 resolved; G0 exit unblocked, Gate 1 may run.

Findings recorded in `knowledge/research/AAUTH_FINDINGS_2026-08-05.md`.

External commitment: Dick Hardt, end of August — permission endpoint
implemented, one notional mission run through it, then office hours or a call.

ROADMAP CONFLICT — requires PI decision, not a silent slide.
The authorized sequence is G24 then G25. The commitment above is implementation
work and maps to neither as written. Either the roadmap moves or the commitment
does.

Scope changes:
- G24 thinner. PIC resolved (Nicola Gallo, Provenance Identity Continuity;
  already cited in the published threat model). AAuth office-hour reconciliation
  superseded by Dick's written answers.
- G25 partially satisfied from primary source. Remainder requires code.
- G26 narrower. Two of three candidate mission models eliminated: missions are
  immutable and have no steps, and evolve only through the log.

Open items:
- AAuth chapter: Appendix B.3.7 citation unresolved; confused-deputy claim needs
  scoping to identity-based access mode; key-rotation persistence claim
  unverified; "Offline: No" is inference, not spec.
- Published threat model Editors field misspells the editor's name.

---
## Session Addendum — 2026-08-05

D-011 resolved; G0 exit unblocked, Gate 1 may run.

Findings recorded in `knowledge/research/AAUTH_FINDINGS_2026-08-05.md`.

External commitment: Dick Hardt, end of August — permission endpoint
implemented, one notional mission run through it, then office hours or a call.

ROADMAP CONFLICT — requires PI decision, not a silent slide.
The authorized sequence is G24 then G25. The commitment above is implementation
work and maps to neither as written. Either the roadmap moves or the commitment
does.

Scope changes:
- G24 thinner. PIC resolved (Nicola Gallo, Provenance Identity Continuity;
  already cited in the published threat model). AAuth office-hour reconciliation
  superseded by Dick's written answers.
- G25 partially satisfied from primary source. Remainder requires code.
- G26 narrower. Two of three candidate mission models eliminated: missions are
  immutable and have no steps, and evolve only through the log.

Open items:
- AAuth chapter: Appendix B.3.7 citation unresolved; confused-deputy claim needs
  scoping to identity-based access mode; key-rotation persistence claim
  unverified; "Offline: No" is inference, not spec.
- Published threat model Editors field misspells the editor's name.
