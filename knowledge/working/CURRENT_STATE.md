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

Repository HEAD is authoritative only as reported live by:

    git rev-parse HEAD

This document does not record a HEAD value. A recorded value would be
invalidated by the commit that updates it.

---

## Current Program Phase

Program: Embodied Governance Research Program
(per `knowledge/strategy/PROGRAM_CHARTER.md`)

Phase: Mission Model and Permission Endpoint

Active Sprint: G26 — Mission Model and Permission Endpoint

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

G0 — Program Initialization: COMPLETE (Gate 1 verified 2026-08-06).
G24 — Research Synchronization: COMPLETE. PIC resolved (Nicola Gallo,
Provenance Identity Continuity). AAuth office-hour reconciliation superseded by
Dick Hardt's written answers of 2026-08-05. Research notes synchronized to
`knowledge/research/AAUTH_FINDINGS_2026-08-05.md`.
G25 — AAuth Integration Investigation: COMPLETE for the specification half.
Connector and repository inspection carried forward into G26.

---

## Active Work

### G26 — Mission Model and Permission Endpoint
Status: ACTIVE (activated 2026-08-06)

Scope:
- Resolve the mission model ADR. Narrowed by the 2026-08-05 findings: missions
  are immutable, have no step structure, and evolve only through the mission
  log.
- Implement the AAuth permission endpoint as the first integration surface.
- Adopt the AAuth mission object natively (D-013).
- Run one notional mission end to end through the permission endpoint.
- Inspect the connector implementation and cloned repository state (carried
  forward from G25).

Exit: mission model ADR recorded; permission endpoint running; one notional
mission demonstrated; connector inspection complete.

External commitment: Dick Hardt, end of August 2026 — permission endpoint
implemented and one notional mission run through it, then office hours or a
call.

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

Execute G26.

Sequence:
1. Inspect the connector implementation and cloned repository state.
2. Adopt the AAuth mission object natively — approver, agent, approved_at,
   approved_tools, description; `s256` over canonical form; immutable after
   approval.
3. Build the append-only mission log with decision attribution (person vs.
   delegate acting on their behalf).
4. Stand up a mock Person Server exposing the permission endpoint.
5. Route the decision to the governance engine: approved intent, mission log,
   and subject agency state in; ALLOW / RESTRICT / DENY plus obligations out.
6. Support both paths — with a mission and without. Permission works either way.
7. Demonstrate: same action, same mission, different subject agency state,
   different outcome.

Deferred within G26: token endpoint, access server, federation, HTTP Message
Signatures, well-known metadata, live revocation, agent identity.

Known open design question, expected to surface during implementation: RESTRICT
is three-valued at an endpoint that expects granted or refused. How a restricted
permission is rendered is an implementation choice the specification does not
make.

Findings: `knowledge/research/AAUTH_FINDINGS_2026-08-05.md`
