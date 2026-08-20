# CURRENT STATE
## Deb B Labs Research Program

Last Updated: 2026-08-20

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

Phase: Embodied Capability and Physical Safety Model

Active Sprint: G27 — Embodied Capability and Physical Safety Model

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
G26 — Mission Model and Permission Endpoint: COMPLETE. Exit criteria satisfied
2026-08-16; see D-022 and completed B-030.

---

## Active Work

### G27 — Embodied Capability and Physical Safety Model
Status: ACTIVE (activated 2026-08-20)

The G27 session-grant package passed advisory review and is committed at
`dc50ea2`:

- `knowledge/research/G27_TIP_JAR_SCENARIO_DECOMPOSITION.md`
- `knowledge/research/G27_SESSION_GRANT_PERSON_SERVER_CONTRACT_2026-08-18.md`
- `knowledge/research/G27_SESSION_GRANT_CANDIDATE_CONFORMANCE_2026-08-18.md`

D-023 adopts the six Tip Jar policy dispositions and prototype boundary in
`knowledge/strategy/G27_POLICY_DISPOSITIONS_2026-08-20.md`. This completes a
substantial G27 decision package; it does not complete G27.

Remaining G27 exit work:

- per-capability risk, authority, context, interruptibility, revocation,
  degradation, audit, and locality model;
- Misty A/Misty B state-isolation specification;
- network-placement and partition behavior;
- mid-actuation interruption semantics;
- bystander/non-delegating affected-subject threat-model extension;
- positive control reaching Authority Established through permitted semantic
  action without relaxing a boundary; and
- prototype negative-control acceptance criteria.

Neither Misty may be powered or connected until the required isolation and
network-placement controls exist. G28 entry remains closed.

### G26 — Mission Model and Permission Endpoint
Status: COMPLETE (activated 2026-08-06; completed 2026-08-16)

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

Exit criteria satisfied. The mission-model ADR criterion is satisfied by
D-013, D-019, and `knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md`.
D-018's rescope supersedes the roadmap's fuller three-candidate exit artifact;
no reconstruction of that evaluation is required. The permission endpoint and
canonical caregiver lifecycle are demonstrated, and connector inspection is
complete through B-030. See D-022.

External commitment: Dick Hardt, end of August 2026 — permission endpoint
implemented and one notional mission run through it, then office hours or a
call.

### 2026-08-14 — G26 caregiver approval integration validated

G26 AAuth permission integration is implemented, Stage Gate PASS,
live-walkthrough validated, and regression-protected through Controls 7 and 9.

Demonstrated continuous flow:

SOGA RESTRICT/HOLDING → conformant AAuth approval pending → unchanged first
poll → PS-authenticated approval assertion → same mission/action/SUPERVISED
subject re-evaluated → SOGA ALLOW → one-time AAuth granted → subsequent 410.

B-032 is complete. No runtime or StageGateEngine changes were required for
negative-control coverage.

Known implementation/demo limitations:

- Mock HTTP server currently emits HTTP/1.0.
- Pending state is process-local/in-memory.

These are implementation/demo limitations and are not G26 governance findings.

### 2026-08-16 — Gate 1a implementation lineage and current architecture PASS

Gate 1a received an advisory agent gate-verification PASS under D-008 at
`1811c87cd239f4843a4805ded985e11ad9f54235`. The PASS records the gate findings;
it does not itself constitute PI authorization. The executed G26/AAuth path was:

AAuth adapter → RuntimeEnvelope → RuntimeGovernanceEngine/SOGA → Canonical
Decision Package → PermissionService.

Mission Builder, StageGateEngine, GovernedExecutionLoop, and capability registry
are present in the repository but were not reached by that path.

This created a synchronization/architecture-description contradiction with the
then-standing "Canonical execution pipeline (unchanged)" statement. B-033
resolved the contradiction prospectively by identifying that pipeline as
target/designed architecture, without declaring either path obsolete or
characterizing the prior statement as historically erroneous.

Gate 1a also established a documentation defect in
`knowledge/working/IMPLEMENTATION_STATUS.md`: its Person Server / Person Server
Integration, Christian Posta Demo, and Runtime Restrict status statements do not
match the implementation and reachable-history evidence. See B-034. This is a
documentation defect, not a Gate 1a evidence problem.

External-claim boundary: current G26 demonstrates governance determination at
the permission boundary, evidence-driven re-evaluation, mock Person Server
authentication, and process-local state. It does not demonstrate governed
execution of the requested external action. Permission enforcement and action
execution remain distinct claims.

---

## Target/Designed Repository Architecture

Target/designed architecture pipeline — not a claim of complete current traversal:

Mission Builder
→ Stage Gate
→ RuntimeEnvelope
→ Governance Policy Server
→ Canonical Decision Package
→ Capability Registry
→ REST / MCP / human execution surface

Commit `2dd9d5c` deliberately promoted this pipeline into the stable
architecture block as the "Canonical execution pipeline (unchanged)," together
with the statement that no architecture, governance logic, or runtime behavior
changed. That adoption is preserved as repository chronology. Gate 1a does not
establish whether the complete pipeline was reachable when the statement was
adopted and does not characterize the prior statement as historically
erroneous.

Prospectively, the standing pipeline is not a claim that a current test, demo,
or runtime traverses every listed component end to end. Gate 1a found no such
current traversal. The current G26 path receives an already-approved mission,
so Mission Builder is outside G26 scope; G26 terminates at the permission
boundary, so Capability Registry and external action execution are also outside
its scope. G26 reaches the canonical decision-package path through the AAuth
bridge. The older governed-execution path reaches Mission Builder,
StageGateEngine, RuntimeEnvelope, GovernancePDP, the older `DecisionPackage`,
and Capability Registry resolution, but not external action execution.

B-035 established a schema-level convergence obligation only. StageGateEngine
operates on a mission-execution step in the older step-bearing model; G26
operates on a permission request/action under the native immutable, step-free
AAuth mission. G26 is bound to a future canonical Stage Gate clearance-evidence
schema, not to StageGateEngine itself. No mechanism-level convergence,
replacement, or coexistence is required or established. The future disposition
of StageGateEngine is deferred to Gate 1b, where the continuing role of the
older step-bearing governed-mission model will be evaluated.

Future schema convergence must preserve G26's assurance and binding properties
and must not weaken D-019, D-020, or the recorded G26 trust boundary. See D-021
and B-036.

Current G26 proves permission-boundary governance and evidence-driven
re-evaluation; it does not prove governed execution of the requested external
action. Permission enforcement and action execution remain distinct claims.

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

Execute the remaining G27 conceptual work before implementation or robot
connection:

1. define the testable Misty A/Misty B isolation property;
2. define network placement and partition behavior;
3. complete the per-capability and conceptual safety model;
4. define positive- and negative-control acceptance criteria; and
5. submit the completed G27 model to its exit gate.

Preserve the real-first prototype boundary in D-023. Do not reopen settled G26
semantics absent new evidence. Do not enter G28 or power/connect either Misty
before G27 entry criteria are satisfied.
