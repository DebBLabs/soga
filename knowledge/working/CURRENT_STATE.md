# CURRENT STATE
## Deb B Labs Research Program

Last Updated: 2026-09-08

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

Phase: M02 — Stage 3A-R4 internal-only preflight accepted as a negative result

Active Sprint: M02 — Wallet-Assisted AAuth Person Server

Active authorization boundary: D-055 authorizes creation—but not execution—of
the bounded R4 IPv6 control diagnosis script after the complete corrected
proposal received PASS from both gates. The one D-053 execution is consumed.
The complete unexecuted diagnostic script must receive PASS from both gates
before commit or execution. Docker execution, candidate startup or access,
another R4 preflight, reachability testing, MCP invocation, external services,
Stage 3B, Misty access, and policy change remain prohibited.

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
G27 — Embodied Capability and Physical Safety Model: COMPLETE. Bounded modeling,
fake-surface, and localhost acceptance scope closed 2026-08-30 under D-027.
M01 — Governed Misty A QR Action Precursor: COMPLETE. One bounded,
QR-requested `m01.signal_light` action completed under D-032; outcome recorded
under D-033 and sprint accepted 2026-09-06 under D-034.

---

## Active Work

### M02 — Wallet-Assisted AAuth Person Server
Status: STAGES 1–2 COMPLETE; STAGE 3A-R4 IPV6 DIAGNOSIS SCRIPT CREATED UNDER D-055

M02 investigates which Person Server responsibilities can be supplied by a
person-controlled wallet and Wallet Attached Storage and which remain in a
separate AAuth Person Server and SOGA governance service. The Person Server is
reusable infrastructure; Misty Tip Jar is its first embodied proving mission,
not its owner or limit.

Stage 1 inspected six clean detached source checkouts, verified revisions,
licenses, documented-but-unexecuted runnable status, and material changes since
the August evidence, and produced the responsibility/conformance matrix in
`knowledge/research/M02_STAGE1_WALLET_PERSON_SERVER_CONFORMANCE_REFRESH_2026-09-06.md`.
Claude Gate 1 and Gemini/AGy Gate 2 independently returned PASS; the durable
summary is `knowledge/research/M02_STAGE1_REVIEW_EVIDENCE_SUMMARY_2026-09-06.md`.

The evidence supports a hybrid composition hypothesis: wallet UI/keys/evidence,
WAS protected storage and atomic primitives, a separate AAuth Person Server,
separate SOGA governance, separately owned participant admission, and
resource/adapter enforcement. This is not an adopted build/reuse decision.
Published AAuth `-10`, later base-editor material, and exploratory R3 remain
separately sourced; R3 `per-call` is not adopted behavior.

The current AAuth execution bridge's B-038 inability to derive live authority
validity, revocation, expiry, delegation depth, elapsed time, and attenuation
from incoming evidence remains a binding limitation. B-039 requires
representative approval to remain distinct from the affected person's assent
or refusal. Wallet, QR, payment, credential, and session possession establish
none of those authorities by themselves.

The Stage 2 proposal in
`knowledge/proposals/M02_STAGE2_LOCAL_PERSON_SERVER_PROPOSAL_2026-09-06.md`
received independent PASS results from Claude Gate 1 and Gemini/AGy Gate 2 at
`2debcd1`. D-036 prospectively authorizes its bounded localhost implementation,
including the narrow B-038 repair, local test-agent harness, test-only
cryptographic identities, and explicit SQLite persistence model. Exact
implementation evidence is recorded in
`knowledge/proposals/M02_STAGE2_IMPLEMENTATION_EVIDENCE_2026-09-06.md`.
Claude Gate 1 and Gemini/AGy Gate 2 returned PASS on the implementation and
again on the post-PASS hardening. The final focused suite passes 44/44 and the
complete repository suite passes 132/132. D-037 accepts Stage 2 and authorizes
commit after narrow review of the subsequently added terminal-visible
walkthrough harness. The exact committed hash was subsequently rerun: 44/44
focused tests and 132/132 repository tests passed. Evidence is recorded in
`knowledge/proposals/M02_STAGE2_POSTCOMMIT_VERIFICATION_2026-09-07.md`.
The proposal's public verification-key-document responsibility was narrowed in
the accepted implementation to test-only HMAC key metadata; it remains an open
protocol-shaped JWKS decision and is not an AAuth conformance claim.
The Stage 3 wallet/WAS composition proposal in
`knowledge/proposals/M02_STAGE3_WALLET_WAS_COMPOSITION_PROPOSAL_2026-09-07.md`
received independent PASS results from Claude Gate 1 and Gemini/AGy Gate 2.
D-038 authorized only its Stage 3A exact-source reproduction phase. Both exact
sources and locked dependencies were reproduced and both sources built. Before
service startup, the selected WAS executable was found to hardcode a wildcard
`0.0.0.0` listener. Stage 3A therefore stopped without starting either service,
modifying either source, or creating a wrapper. The standalone report at
`knowledge/research/M02_STAGE3A_EXACT_SOURCE_RUNTIME_EVIDENCE_2026-09-08.md`
received PASS from both gates and was accepted as a negative result under
D-039. Stage 3B remains separately unauthorized pending a reviewed response to
the wildcard-bind limitation.

The response proposal at
`knowledge/proposals/M02_STAGE3A_LOOPBACK_RECOVERY_PROPOSAL_2026-09-08.md`
uses the selected WAS package's documented library-composition seam so a
SOGA-owned research launcher, rather than upstream protocol code, owns the
literal-loopback listener. After required containment corrections, Claude Gate
1 and Gemini/AGy Gate 2 returned PASS. D-040 authorized only that recovery
attempt. The exact reviewed macOS sandbox profile rejected literal
`127.0.0.1` during parsing, before Node or either candidate ran. The unsafe
unexecuted launcher and profile were removed rather than adopted. The standalone
report at
`knowledge/research/M02_STAGE3AR_LOOPBACK_RECOVERY_EVIDENCE_2026-09-08.md`
received final PASS from both gates and was accepted under D-041. Stage 3B
remains unauthorized pending a separately reviewed containment approach.

The fixed-port response proposal at
`knowledge/proposals/M02_STAGE3AR2_FIXED_PORT_CONTAINMENT_PROPOSAL_2026-09-08.md`
narrows the symbolic `localhost` sandbox exception to ports `46321` and `46322`
while retaining literal `127.0.0.1` application listeners and URLs. Its
preflight distinguishes sandbox denial from ordinary refusal and characterizes
wildcard, IPv6, other-loopback-port, and TEST-NET behavior before either
candidate may start. Claude Gate 1 and Gemini/AGy Gate 2 returned PASS. D-042
authorized only that Stage 3A-R2 attempt. The literal IPv4 nonce exchange
passed and other-port and TEST-NET connections were denied, but the same
symbolic-`localhost` rule admitted a prohibited `0.0.0.0` wildcard bind. The
pre-start control failed, so the launcher was never executed and neither
candidate was imported, served, or started. The temporary profile, preflight,
and launcher were removed rather than adopted. The standalone report at
`knowledge/research/M02_STAGE3AR2_FIXED_PORT_CONTAINMENT_EVIDENCE_2026-09-08.md`
received final PASS from both gates and was accepted under D-043. Stage 3B
remains unauthorized pending a separately reviewed containment decision.

The Docker containment proposal at
`knowledge/proposals/M02_STAGE3AR3_DOCKER_CONTAINMENT_PROPOSAL_2026-09-08.md`
uses an internal Docker network and literal host-loopback publication while
treating both as hypotheses that require empirical negative controls. It
requires a locally cached immutable Node 24+ image, two isolated disposable
candidate containers, explicit finite WAS limits, pre-execution review of every
script, and complete cleanup. Claude Gate 1 and Gemini/AGy Gate 2 returned PASS
on the proposal and its precision corrections. D-044 authorizes only that
Stage 3A-R3 characterization and conditional candidate reachability attempt.

Phase 0 found Docker Desktop `28.5.2` on `linux/arm64`, no fixed-name R3
resources or fixed-port listeners, and only two cached Python A2A/GNAP images.
Because no local Node 24+ image existed, D-044's no-acquisition boundary stopped
the attempt before scripts, containers, networks, registry access, or candidate
execution. Both gates confirmed the evidence at
`knowledge/research/M02_STAGE3AR3_DOCKER_CONTAINMENT_EVIDENCE_2026-09-08.md`.
They also verified the Docker Official Image selection and full arm64 manifest
digest in
`knowledge/proposals/M02_STAGE3AR3_NODE_IMAGE_ACQUISITION_PROPOSAL_2026-09-08.md`.
D-045 authorized only its one pinned pull and isolated Node version check. The
full-digest image was acquired once, immutable metadata matched, and the
network-disabled disposable verification returned exact Node `v24.20.0`.
Cleanup left no R3 container, network, or fixed-port listener. Both gates
returned PASS on
`knowledge/research/M02_STAGE3AR3_NODE_IMAGE_ACQUISITION_EVIDENCE_2026-09-08.md`,
and D-046 accepts that result and permits creation and review of the R3
scripts. Both complete scripts subsequently received PASS results from Claude
Gate 1 and Gemini/AGy Gate 2 after fail-closed cleanup, collision preservation,
deterministic selection, holdpoint timing, and bounded diagnostics corrections.
D-047 authorized execution of only the synthetic containment preflight. The
preflight created and verified its internal network, but its literal-loopback
nonce endpoint did not become ready within the finite window. It failed closed
with exit status 1 and cleanup left no R3 container, network, or fixed-port
listener. No candidate ran. Both gates returned PASS on the standalone evidence
at
`knowledge/research/M02_STAGE3AR3_SYNTHETIC_PREFLIGHT_EVIDENCE_2026-09-08.md`,
and D-048 accepts the run as a gated negative result.

Read-only diagnosis localized the missing evidence and identified a
path-dependent readiness-loop defect without establishing the runtime cause.
The bounded recovery proposal at
`knowledge/proposals/M02_STAGE3AR3_PREFLIGHT_DIAGNOSIS_RECOVERY_PROPOSAL_2026-09-09.md`
received PASS from both gates after corrections. D-049 authorizes creation—but
not execution—of the corrected synthetic preflight and requires complete-file
PASS reviews before commit or execution.

The complete corrected file then received PASS from both gates. It uses a
wall-clock readiness deadline, bounded and normalized diagnostics, explicit
subprocess timeouts, a named synthetic gateway value, host-address redaction,
and cleanup-dependent final success. D-050 accepts that reviewed script and
authorizes its exact committed version to execute once, followed by independent
cleanup verification and dual-gate evidence review.

That one corrected diagnostic execution made 49 host-loopback connection
attempts over approximately 9.8 seconds. The host never reached the synthetic
nonce endpoint, while bounded container state and logs plus an internal
self-readiness probe established that the synthetic server was running and
serving the expected nonce inside the container. This is positive server-health
discrimination and localizes the observed failure to the host-publication path
for the exact tested topology; it does not identify a specific Docker component
or generalize to other environments. The later non-loopback-host and egress
controls did not run, so containment did not pass. Independent checks confirmed
complete cleanup. Both gates returned PASS on
`knowledge/research/M02_STAGE3AR3_DIAGNOSTIC_PREFLIGHT_EVIDENCE_2026-09-09.md`,
and D-051 accepts the run as a gated negative result.

The internal-only R4 proposal at
`knowledge/proposals/M02_STAGE3AR4_INTERNAL_ONLY_CONTAINMENT_PROPOSAL_2026-09-09.md`
responds to the accepted host-publication failure by removing host publication
entirely and placing a synthetic server and a separate test-only client on one
IPv4-only internal Docker network. It preserves strict host-path probes, makes
no claim that embedded-DNS forwarding is absent, and leaves later caller
placement unresolved. Both gates returned PASS after IPv6, gateway-refusal,
DNS-scope, Docker-alias, namespace-sharing, inherited-port, and cleanup-
attribution corrections. D-052 authorizes creation—but not execution—of the R4
synthetic script and requires complete-file PASS reviews before commit or run.

The complete R4 script subsequently received PASS from both gates after adding
bounded failure-time state and log diagnostics, deliberate flushed IPv6
categories, strict handling of missing Docker IPv6 metadata, bounded alias
discovery, self-correlating redacted alias indexes, and readiness-command
failure handling within the monotonic deadline. D-053 accepts the exact reviewed
script and authorizes one execution after commit and push, followed by
independent cleanup verification and dual-gate evidence review.

That one R4 execution passed preconditions, cached-image verification, both
network inspections, and server isolation. Docker reported IPv6 disabled and
no server endpoint IPv6 address or gateway, but the in-container kernel check
returned the combined category `ipv6_present`, meaning either a non-loopback
IPv6 address or a default-route record was observed. The bounded category does
not distinguish which and establishes no usable IPv6, host, or external
reachability. The run stopped before readiness, inter-container exchange, and
all later path controls. Both synthetic processes were healthy at the stop
point, and independent checks confirmed complete cleanup. Both gates returned
PASS on
`knowledge/research/M02_STAGE3AR4_INTERNAL_ONLY_PREFLIGHT_EVIDENCE_2026-09-09.md`,
and D-054 accepts the run as a gated negative result.

The 2026-09-07 editor-repository delta from the Stage 1 AAuth baseline
`39a017d` to `b6ca19b` names the off-wire Supervisor role and adds an
informative minimal-Person-Server appendix. It does not invalidate Stage 2's
explicit test-only, nonconformant boundary, but it sharpens the protocol-shaped
metadata, JWKS, person-token, and authorization-token choices that must be made
before a later implementation or conformance claim. See
`knowledge/research/M02_AAUTH_EDITOR_DELTA_2026-09-07.md`.

A temporary persistent-polling pilot proved file transport and shutdown but did
not prove fresh reviewer reasoning or provide the PI-required live visibility.
It was not adopted. Real gates remain visible one-shot reviews, with Codex
responsible for actively monitoring both response files through completion.
A subsequent synthetic foreground AGy repair invoked fresh reasoning, streamed
tool activity, completed two sequential requests without restarting the queue
runner, rejected denied or empty responses as errors, and stopped cleanly. It
does not support interactive approvals and is not yet adopted for real gates.

The D-050 and D-053 executions are consumed. D-055 authorizes only creation and
dual review of the bounded IPv6 diagnosis script; it authorizes no execution.
Candidate startup or access, further R3 work, additional R4 execution or
modification, and any Stage 3B code or tests remain prohibited. No service may
be externally exposed; neither Misty robot may be powered, connected, queried,
configured, discovered, or actuated.

### M01 — Governed Misty A QR Action Precursor
Status: COMPLETE (accepted 2026-09-06 under D-034)

M01 completed one bounded governed physical action. The G3100 use was a
one-time accepted exception and is not precedent. Deb confirmed on 2026-09-06
that Misty A is powered off and on the shelf. Beryl placement is mandatory
before every future Misty power-on or access but was not represented as already
complete. D-032 is exhausted; D-034 authorizes no subsequent robot access and
does not activate G28.

### G27 — Embodied Capability and Physical Safety Model
Status: COMPLETE (activated 2026-08-20; completed 2026-08-30 under D-027)

The G27 session-grant package passed advisory review and is committed at
`dc50ea2`:

- `knowledge/research/G27_TIP_JAR_SCENARIO_DECOMPOSITION.md`
- `knowledge/research/G27_SESSION_GRANT_PERSON_SERVER_CONTRACT_2026-08-18.md`
- `knowledge/research/G27_SESSION_GRANT_CANDIDATE_CONFORMANCE_2026-08-18.md`

D-023 adopts the six Tip Jar policy dispositions and prototype boundary in
`knowledge/strategy/G27_POLICY_DISPOSITIONS_2026-08-20.md`.

The remaining G27 modeling artifacts are adopted and committed:

- isolation and network requirements at `a52b7e8`;
- capability safety model at `a434db1`; and
- the D-023 policy dispositions at `84d3546`.

D-024 authorizes bounded G27 acceptance implementation using fake recording
surfaces only. The authorization and its terminal-only scope clarification are
committed at `6d687b3` and `bce388f`. The bounded implementation and interactive
two-stage acceptance flow are committed at `4a7acac` and `d95db19`.

PI-retained external reports record independent Claude and AGy review passes
and the PI's visible terminal walkthrough; those review transcripts are not
repository artifacts. Their reviewed scope, checkpoints, results, corrections,
and unresolved limits are summarized canonically in
`knowledge/research/G27_REVIEW_EVIDENCE_SUMMARY_2026-08-30.md`. The full
repository test suite passes 63 tests.
The implementation demonstrates an observably Pending request, separately
delivered governance, target-bound dispatch to recording surfaces, unknown
physical outcome, replay and concurrency controls, and a safety halt defeating
a late ALLOW. It contains no robot, network, HTTP, actuation, or physical-success
path in the active G27 runtime or adapter.

G27 is complete at its bounded acceptance boundary under D-027. Canonical-state
synchronization through stage one is committed at `ec955cf`. D-025
prospectively authorizes the loopback-only split-service acceptance stage at
`90a668e`. The implementation is
committed at `a5af621`; the D-026 platform-wide safety-latch admission rule and
explicit session-count assertions are committed at `680e444`. The PI-visible
terminal walkthrough and Claude technical gate are summarized in
`knowledge/research/G27_D025_REVIEW_EVIDENCE_SUMMARY_2026-08-30.md`. The full
suite passes 72 tests. Independent AGy verification reported PASS with no
blocking findings and confirmed that D-026 refines section 4 of the safety
model. Its reverse review identified D-023 per-action cardinality as specified
but not implemented; that boundary is recorded in `g27_tip_jar/GAPS.md` and in
D-027 rather than treated as completed. Any Misty power, connection,
external-network access, discovery, status request, or actuation requires a
later explicit decision and remains outside D-024, D-025, D-026, and D-027.

The corrected embodied-execution and Misty community landscape research note
passed independent Claude and AGy research gates, as recorded in PI-retained
external reports, and is adopted at
`knowledge/research/EMBODIED_EXECUTION_AND_MISTY_COMMUNITY_LANDSCAPE_2026-08-20.md`.
It is research context only and did not authorize D-025. D-025 was separately
authorized prospectively at `90a668e` and does not authorize G28 entry, robot
connection, actuation, or public demonstration. G28 entry remains closed.

### Post-G27 Representative-Authority Research Input

The corrected
`knowledge/research/REPRESENTATIVE_AUTHORITY_CONTRACT_2026-08-31.md` passed a
read-only Gate 1 against `2b39c89` and is adopted as non-authorizing research
input. Scenario inspection establishes three open boundaries: the AAuth bridge
does not receive live authority validity inputs; affected-person assent or
refusal has no independent decision-relevant path; and a credential does not
establish co-presence or a representative relationship. These are recorded as
B-038, B-039, and B-040.

The artifact selects no credential, wallet, protocol extension, component owner,
legal rule, or precedence rule. This post-G27 research does not reopen G27,
authorize implementation, enter G28 or G29, authorize sensor use, or permit
powering, connecting, discovering, querying, or actuating either Misty.

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

Complete dual-gate full-file review of the unexecuted IPv6 diagnosis script
created under D-055. Do not execute or commit it before both reviews pass.
Execution requires a later separate prospective PI authorization. Do not modify
or rerun either accepted R3/R4 preflight, run the candidate-startup script,
compare configurations, or start a candidate.

Preserve the open choices: the hybrid composition remains a hypothesis; the
AGPL and DID Cooperative license boundaries, protocol-shaped Person Server
surface, exact trust messages, remaining B-038 authority inputs, B-039
affected-person path, and participant-session owner remain unresolved.

Do not write Stage 3B code or tests, implement an integration, expose a service,
use personal data or payment, enter or rewrite G28/G29, or access either Misty
robot. Application runtime external-network access remains prohibited. Beryl
placement remains mandatory before future Misty power-on or access. The
separate PI routine-tool-approval proposal remains unadopted and outside D-055.
