# DECISION LOG
## Deb B Labs Embodied Governance Research Program

Status: DRAFT v0.1 — decisions below are PROPOSED until the G0
initialization commit; the PI's commit is the act of adoption.
Precedence: subordinate to `knowledge/working/CURRENT_STATE.md`

Format: ID — Date — Decision — Rationale (brief) — Status

---

- **D-001** — 2026-07-20 — Adopt the research-question sprint model:
  sprints produce verified evidence, architectural clarification,
  measured implementation, or research artifacts — not merely code —
  Completes the intent of G23 and the repository methodology —
  PROPOSED.

- **D-002** — 2026-07-20 — Introduce Initialization Sprint G0,
  separating program initialization from research synchronization
  (G24) — The two have different failure modes; separation makes each
  sprint's exit binary — PROPOSED.

- **D-003** — 2026-07-20 — Separate the program into three layers:
  program governance (continuous), program tracks (continuous),
  research sprints (time-boxed); establish five continuous tracks with
  registers in TRACKS.md — Standards participation and funding are
  ongoing commitments, not milestones — PROPOSED.

- **D-004** — 2026-07-20 — Adopt the merged G24–G30 sequence from the
  three-agent review, including: G25→G26→G27 dependency chain; G27
  owns the A/B state-isolation specification and bystander threat-model
  extension; G28 entry requires the G27 isolation spec; G29 precedes
  any public demonstration — Evidence-driven ordering per
  RESEARCH_METHODOLOGY.md — PROPOSED.

- **D-005** — 2026-07-20 — Mission terminology: retain "Mission"
  pending G26; G26 evaluates a minimum of three candidate models on
  evidence, with switching costs as legitimate criteria; the layered
  hierarchy is a candidate, not the assumed answer — Prevents
  confirmation bias; protects the AAuth interoperability asset —
  PROPOSED.

- **D-006** — 2026-07-20 — Misty platform roles: Misty B (new unit,
  advanced perception) is the higher-capability embodied research
  platform; Misty A is the stable comparative baseline and
  lower-capability control — Two-point test of capability-relative
  governance (H3) — PROPOSED.

- **D-007** — 2026-07-20 — Document precedence: CURRENT_STATE.md
  remains the sole synchronization contract; all strategy artifacts are
  subordinate and referenced; the charter cites
  docs/RESEARCH_METHODOLOGY.md rather than restating it — Prevents
  parallel sources of truth — PROPOSED.

- **D-008** — 2026-07-20 — Authority model: PI holds singular editorial
  and decision authority; agent gate verification (Gate 1: Claude) is
  advisory pass/fail with findings; sprint activation is authorized by
  the PI — Consistent with the established repository operating model —
  PROPOSED.

- **D-009** — 2026-07-20 — Fellowship relationship: fellowships fund
  and accelerate the charter's plan; the charter remains the source of
  truth; no funded opportunity redefines the program — Protects
  long-term direction — PROPOSED.

- **D-010** — 2026-07-20 — Tooling/subscription review established as a
  standing quarterly governance item under the Funding & Partnerships
  Track; no cancellation decisions made today — Portfolio review
  follows demonstrated need, not anticipation — PROPOSED.

- **D-011** — 2026-07-20 — Defer
  `knowledge/working/deferred/live_governance_workbench.py` as an
  unadopted exploratory artifact pending conceptual clarification and
  discussion with Dick Hardt. It is not part of the canonical runtime,
  is not authorized for execution or further development, and creates
  no architectural commitment — Preserves incomplete exploratory work
  without treating it as active implementation or concealing it as
  ignored local drift — DEFERRED.

- **D-012** — 2026-07-20 — Adopt pre-commit editorial findings from
  cross-agent review: (a) Outreach Track renamed Living Laboratory &
  Outreach Track — research in human environments, with outreach as
  one activity within it; (b) charter sentence added: standards
  participation informs but does not determine the research agenda;
  (c) optional Outcome field added to track registers; (d) subscription
  review confirmed as standing governance, not procurement —
  Refinements only; no architectural change — PROPOSED.

## D-011 — RESOLVED 2026-08-05
Conceptual clarification obtained via written exchange with Dick Hardt.
Governance is not a single function requiring an attachment point; SOGA is the
PS's governance policy. G0 exit unblocked.

## D-013 — Adopt AAuth mission structure natively
Adopt the AAuth mission object rather than translating into it. Requires a G19
neutrality statement: the fields are generic and map to other substrates.
Retain the adapter boundary despite shape agreement — the draft will move.

## D-014 — Permission endpoint is the first integration surface
Chosen over the token endpoint. Works with or without a mission, requires no
resource or AS participation, and carries the residual decisions that fall
outside `approved_tools`.

## D-015 — AuthZen MCP hook deferred
Extension approval requires a dedicated working group and a vote of all nine
core maintainers. Not an IIW-timeframe deliverable.

## D-016 — PECOSE dropped
Requires letters from five people working on the open source tool. Not
satisfiable this round.

## D-017 — Close G0, G24, and G25
G0 deliverables complete; Gate 1 verified 2026-08-06. G24 satisfied: PIC
resolved, office-hour reconciliation superseded by Dick Hardt's written
answers, research notes synchronized. G25 satisfied for the specification half;
connector and repository inspection carried forward into G26 rather than
deferred.

## D-018 — Activate G26, rescoped
G26 rescoped to mission model plus permission endpoint implementation. The
mission model ADR is narrower than originally planned: two of three candidate
models are eliminated by the specification. The permission endpoint work is
added because it is the first integration surface (D-014) and because an
external commitment exists to Dick Hardt for end of August. This resolves the
roadmap conflict recorded 2026-08-05.

## D-019 — Implement the reviewed G26 mission and permission decision

Authorized by Deb following Claude Stage Gate PASS with the required amendment
incorporated. Adopt the immutable native AAuth mission shape and append-only
mission log; project SOGA `ALLOW` to AAuth `granted` and SOGA `DENY` to AAuth
`denied`. A completely internally discharged pre-grant `RESTRICT` may
ultimately project to `granted`; agent-participation `RESTRICT` remains pending
through AAuth deferred response. If required structured interaction cannot be
represented safely, use the August fallback of AAuth `denied` plus its
specification-defined `reason`. Preserve the underlying SOGA decision and
attribution separately because AAuth `granted`/`denied` cannot reconstruct it.
Do not assign arbitrary SOGA requirements to `clarification`, invent deferred
termination semantics, or solve post-grant obligations. Full rationale and
boundaries: `knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md`.

## D-020 — Resolve G26 pre-grant RESTRICT path semantics

Authorized after Stage Gate review on 2026-08-14. Going forward, `HOLDING`
means that nothing executes until human clearance; `SUPERVISED_EXECUTION`
means execution proceeds under human monitoring without prior clearance.
Subject agency state may contribute to `RESTRICT` but does not select its
operational path. An authorized mission/policy constraint selects the path;
absence of such a declaration fails closed. The canonical caregiver constraint
selects `HOLDING`, requires `supervisor_confirmation`, and references
`authority-caregiver-001`. AAuth `requirement=approval` carries the deferred
prerequisite. Approval evidence causes governance re-evaluation with the same
mission, action, and `SUPERVISED` subject; approval alone never implies
`granted`. Earlier combined terminology remains historical evidence and is
resolved prospectively, not characterized as an established historical error
or supersession. Full semantics and boundaries are recorded in
`knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md`.

## D-021 — Resolve B-035 at the evidence-schema boundary

PI disposition accepted on 2026-08-16. B-035 resolves as a schema-level
convergence obligation; no mechanism-level relationship is required or
established between StageGateEngine and G26. StageGateEngine operates on a
mission-execution step in the older step-bearing model. G26 operates on a
permission request/action under the native immutable, step-free AAuth mission
adopted by D-013. The repository binds G26 provisional approval evidence to a
future canonical Stage Gate clearance-evidence schema, not to StageGateEngine
itself.

Future schema convergence must preserve the assurance and binding properties
established by G26 and must not weaken D-019, D-020, or the recorded G26 trust
boundary. Mechanism-level convergence, replacement, or coexistence is neither
required nor established. The future disposition of StageGateEngine is deferred
to Gate 1b, where the continuing role of the older step-bearing governed-mission
model will be evaluated. This decision authorizes no runtime change, defect
repair, or Gate 1b work.

## D-022 — Close G26 and satisfy the rescoped mission-model ADR exit criterion

PI disposition accepted on 2026-08-16. The G26 mission-model ADR exit criterion
is satisfied by D-013, D-019, and
`knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md`. D-018's rescope
supersedes the roadmap's fuller three-candidate exit artifact; no reconstruction
of that evaluation is required.

The remaining G26 exit criteria are satisfied: the permission endpoint is
running, the canonical caregiver mission was demonstrated through the complete
permission and evidence-driven re-evaluation lifecycle, and the connector
inspection is complete through B-030. G26 is complete. This decision does not
open Gate 1b, alter the older mission model, or authorize runtime changes.

## D-023 — Activate G27 and adopt the Tip Jar policy dispositions

PI disposition accepted on 2026-08-20 following advisory review of the G27
session-grant package committed at `dc50ea2`. Activate G27 — Embodied Capability
and Physical Safety Model — and adopt the six Tip Jar policy dispositions and
prototype boundary recorded in
`knowledge/strategy/G27_POLICY_DISPOSITIONS_2026-08-20.md`.

The adopted model uses one persistent native AAuth mission, a distinct
single-use participation credential, and separate bounded session state. The
first session has a five-minute hard maximum and a one-minute inactivity
timeout; replay, duplicate execution, concurrent physical sessions, and
terminal revival are prohibited. Unknown-age and unknown-identity participants
may reach positive authorization only for the finite, low-risk,
attribute-independent action envelope. Physical safety remains independent and
local.

The prototype is real-first and may substitute provisional components only for
named missing functions while preserving the approved contract and honest
evidence boundaries. This decision authorizes conceptual G27 work only. It does
not authorize implementation, robot power/network connection, physical
execution, G28 entry, or G27 closure. A/B isolation and network-placement
requirements remain preconditions to connecting either Misty.

## D-024 — Authorize bounded G27 acceptance implementation

PI disposition accepted on 2026-08-20. Authorize G27 implementation from this
decision forward solely to produce the acceptance evidence required for G27
exit. The authorized scope is the session-grant lifecycle and state machine,
the target-bound execution adapter, recording-only fake execution surfaces for
Misty A and Misty B, and their acceptance tests.

The fake surfaces may record what they receive but may not simulate or claim a
physical outcome. This decision authorizes no robot power, robot or external
network connection, physical actuation, hardware adapter, robot discovery,
G28 entry, or public demonstration. Unknown implementation choices remain gaps;
they are not decided in code.

The uncommitted G27 implementation package was produced after the PI instructed
CG in chat to begin coding but before that implementation authorization was
recorded in the canonical repository. This decision records the authorization
prospectively and does not backdate or rewrite that sequence. The package must
still pass its technical reviews, PI walkthrough, acceptance review, and commit
controls; this decision alone does not establish G27 exit.

Implementation-scope clarification recorded on 2026-08-20: the PI confirmed
that a local, single-process, terminal-driven two-stage flow and its in-memory
event display are acceptance-test evidence within D-024. They are not a public
demonstration and introduce no transport. Localhost HTTP or any split-service
stage requires a later decision before implementation.

## D-025 — Authorize localhost split-service acceptance implementation

PI disposition accepted on 2026-08-30. Authorize the next G27 acceptance stage
solely to determine whether the D-024 session, governance, target-binding,
safety-precedence, and truthful-outcome semantics survive separation across
localhost service boundaries.

The authorized scope is a terminal-driven local client and loopback-only HTTP
services for the authoritative grant/session lifecycle, separately delivered
governance decisions, and target-bound fake recording surfaces for Misty A and
Misty B. Services must bind only to explicit loopback addresses, use ephemeral
or explicitly configured local ports, and fail closed rather than bind all
interfaces, discover a target, use a hardcoded address fallback, or route to the
other fake platform. One authoritative session service retains the D-024
one-live-session and single-consumption semantics; this decision does not claim
multi-process replicated-state atomicity.

HTTP status establishes only the response of the named local fake service. It
does not establish robot availability, dispatch, start, completion, neutral
state, or physical safety. Fake surfaces remain recording-only and every
physical outcome remains `unknown`. The implementation must preserve distinct
request, decision, dispatch, and outcome events; Pending must be observable;
and a safety halt must defeat a late `ALLOW` across the service boundary.

This decision does not authorize an MCP implementation or claim MCP
conformance. It authorizes no non-loopback or external network access, robot
power, Misty address or credential, robot discovery, status query, hardware
adapter, actuation, physical execution, public demonstration, G28 entry, or G27
closure. Unknown choices remain recorded gaps rather than decisions made in
code. The implementation remains subject to technical review, independent
verification, PI-visible terminal walkthrough, and commit controls.

## D-026 — Make a latched safety stop a platform-wide session-admission gate

PI disposition accepted on 2026-08-30 after the D-025 technical review exposed
an implementation/model mismatch. While a platform safety stop is latched,
participation grants may still be issued because issuance causes no interaction.
However, no grant for that platform may be consumed and no new participant
session may be admitted. A rejected admission leaves the grant unconsumed and
subject to its existing validity and expiry rules.

Session admission may resume only after verified operator release for that
platform. Release never revives the stopped session or interrupted request; the
participant must present a fresh, still-valid grant or obtain a new one. This
decision records the implementation's fail-closed behavior in the adopted G27
safety model. It does not authorize robot contact, execution, G28 entry, or G27
closure.

## D-027 — Close G27 at the bounded acceptance boundary

PI exit disposition accepted on 2026-08-30 after the D-025 implementation,
PI-visible terminal walkthrough, Claude technical gate, correction recheck, and
independent AGy forward-and-reverse verification. Close G27 — Embodied
Capability and Physical Safety Model — as complete for its adopted modeling and
bounded fake/localhost acceptance scope.

The exit evidence consists of the adopted session-grant package, D-023 policy
dispositions, A/B isolation and network requirements, capability safety model,
landscape research, D-024 in-process acceptance implementation, D-025
loopback-only split-service implementation, 72 passing tests, and the canonical
review summaries committed at `322c672`. D-026 refines section 4 of the safety
model by making a latched safety stop a platform-wide session-admission gate;
the model and code agree on that boundary.

This exit does not convert prototype limits into completed capabilities.
Durable or distributed concurrency remains unimplemented. D-023 per-action and
conversation-turn cardinality remains specified but unenforced. Fake surfaces
prove receipt only, not physical outcome or safety. Physical measurement and
robot integration remain for a separately authorized G28. Non-participant
privacy remains B-037 under G29 before public interaction can count as research
evidence.

G27 closure does not activate G28 and authorizes no robot power, connection,
external-network access, discovery, status query, hardware adapter, actuation,
physical execution, MCP conformance claim, production deployment, or public
demonstration.

## D-028 — Activate M01 Misty A precursor at Mission Formation only

PI disposition accepted on 2026-09-04 after Claude/Gate 1 and Gemini/AGy Gate 2
independently reviewed the G28 entry discrepancy and both issued advisory PASS
WITH CONDITIONS rulings. Activate `M01 — Governed Misty A QR Action Precursor`
as a formally named precursor sprint before G28. Preserve the roadmap's G28 —
Governed Misty B Runtime Prototype — without amendment.

M01 begins at Mission Formation for the 2026-09-04 3:00 PM session. The native
immutable AAuth Mission and mission log remain the authoritative mission
representation. Mission Formation may define the objective, boundaries,
allowed and prohibited actions, requirements, risks, acceptance criteria, and
proposed finite C1 action catalog. A human-readable mission specification is
explanatory and may not become a competing mission type.

This decision authorizes Mission Formation only. It does not authorize
implementation, code changes, a physical adapter, robot power, network
connection, discovery, status query, external-network access, actuation, or
public demonstration. Implementation requires a later explicit Mission
Authorization after the completed mission package passes the existing review
process. Physical connection and execution require a still-later explicit
Physical Execution Authorization supported by inherited G27 hardware, network,
independent local safety, target-binding, cardinality, negative-test, and
truthful-receipt evidence.

The temporary HOPE shared-file coordination mechanism may carry bounded review
requests and responses during M01. It carries evidence only, creates no agent or
human authority, and may not infer Deb's authorization from a message or file.
Its permanent adoption is not decided by D-028.

## D-029 — Authorize M01 implementation and non-physical validation

PI Mission Authorization received on 2026-09-05. Adopt
`urn:debblabs:person-server:deb-bucci` as the M01 local test-fixture approver
identifier, `soga-m01-misty-a-qr-agent-v1` as the mission-agent identifier, and
`m01.signal_light` as the sole action eligible for the initial physical run.

Authorize Codex to implement and test the bounded QR-action path using fake and
loopback recording surfaces under the reviewed M01 mission package and inherited
G27 controls. This authorization does not establish a production Person Server
or durable wallet-backed authority service. It does not authorize powering,
connecting, discovering, querying, or actuating Misty; a physical adapter
dispatch; G28 activation; or a physical-success claim. Physical connection and
execution require a later explicit PI Physical Execution Authorization after
independent Gate 1 and Gate 2 implementation review and the inherited G27
pre-connection evidence.

## D-030 — Authorize M01 physical preparation without device connection

PI Physical Preparation Authorization received on 2026-09-05. Authorize
powering Misty A solely to verify reported serial `20221304273`, obtain the
current IP from the trusted Verizon G3100 router record, inspect battery and
physical condition, and confirm the operator-stop procedure. This does not
authorize computer connection, address discovery or scanning, device query,
configuration, or actuation.

The PI subsequently adopted the run-specific Misty A binding supported by the
case serial, router record, historical address corroboration, clean power-on,
and Misty Studio response: serial `20221304273`, MAC `00:d0:ca:01:a2:61`, and
current DHCP IPv4 `192.168.1.183`. Because the lease is dynamic, the address
must be rechecked immediately before any later physical run.

## D-031 — Authorize bounded read-only Misty A connection verification

PI Connection Verification Authorization and later Extended Read-Only
Verification Authorization received on 2026-09-05. Authorize read-only access
to `http://192.168.1.183` solely for identity, battery, network, and system
status; prohibit configuration and LED, speech, movement, camera, microphone,
mapping, skill, or other action commands, and prohibit address discovery.

One root GET returned HTTP 200 and Misty Studio. Loading the visible Misty
Studio dashboard then automatically initialized its ordinary Live Data page,
including camera preview and distance telemetry, without an operator click.
Codex stopped and closed the tab immediately because camera access was outside
the stated categories. The PI reviewed the visible behavior and classified it
as normal website API initialization rather than actuation. The dashboard
showed 100% battery and a Halt control. No control, configuration, or actuation
command was sent. This decision records observed evidence only and does not
authorize physical execution.

## D-032 — Authorize one M01 Misty A physical signal-light execution

PI Physical Execution Authorization received on 2026-09-05. Adopt
`urn:debblabs:misty-a:20221304273` as the canonical Misty A platform identifier
for this run and confirm the binding MAC `00:d0:ca:01:a2:61` at current DHCP
IPv4 `192.168.1.183`. The PI attests that Misty is stable, surroundings are
clear, battery is 100%, and the PI is present with immediate access to Halt or
hardware power-off.

Authorize exactly one `m01.signal_light` execution: POST pink
`(255,105,180)` to `/api/led`, wait 1.0 second, then POST yellow
`(255,255,0)` to the same endpoint. Authorize no retry and no other endpoint or
action. For this single Dazza/HOPE acceptance run, the PI accepts use of the
current G3100 network before moving Misty behind the Beryl router immediately
afterward.

Execution must use the independently reviewed runner and still requires the PI
to type `EXECUTE m01.signal_light` in the terminal. Stop after the terminal
receipt and PI visual observation. API acknowledgment does not establish
physical success; physical and neutral outcomes remain unknown until the PI
records an observation.

## D-033 — Record M01 authorized physical execution outcome

The single D-032 `m01.signal_light` execution occurred on 2026-09-05 through
the independently reviewed governed runner. One earlier terminal invocation
cancelled before dispatch because its confirmation did not match. The successful
invocation reported governance granted and API acknowledgment for both the pink
signal and yellow neutral commands, with no retry.

The PI directly observed the pink signal. The PI described the final color as
yellow or green and then concluded it was yellow given the commanded value and
API acknowledgment. Record the neutral physical outcome as consistent with
yellow by PI observation and inference, not independently measured. No
follow-up query or command was sent. This records evidence but does not close
M01, activate G28, or authorize further physical action.

## D-034 — Accept and close M01 with Beryl as a pre-next-access prerequisite

PI disposition received on 2026-09-06: **ACCEPT M01**. Gate 1 and Gate 2
reviewed the exit reconciliation at `ddcdabb` and recommended acceptance after
the documented corrections. The completed M01 objective was one bounded,
QR-requested, governed `m01.signal_light` action with truthful separation of API
acknowledgment, direct pink observation, and the inferred neutral appearance.
The post-authorization test repair passed the complete 88-test suite.

The Verizon G3100 use remains a one-time accepted exception and creates no
precedent. Misty A was not moved behind the Beryl router. Deb directly confirmed
on 2026-09-06 that Misty A is powered off and on the shelf; this is PI-observed
physical-state evidence, not a software query. Beryl placement is reclassified
prospectively as a hard prerequisite before every future Misty power-on,
connection, query, configuration, discovery, demonstration, or actuation. No
future Misty A network exposure under any router is authorized until that
placement is confirmed through a later decision.

The runner's decision-log check establishes presence of a durable plaintext
authorization record; it is not cryptographic or unforgeable. Deb states from
her own knowledge as PI and physical-asset owner that Misty B is already owned;
the repository independently establishes neither ownership nor a procurement
requirement. Unit qualification, isolation, and explicit PI authorization
remain required before any use.

D-032 is exhausted. D-034 closes M01 but activates no successor mission,
authorizes no robot access, and does not activate or rewrite G28.

## D-035 — Authorize M02 Stage 1 wallet-assisted Person Server research only

PI authorization received on 2026-09-06. Activate `M02 — Wallet-Assisted AAuth
Person Server` at Stage 1 current-source research only under the independently
reviewed mission-formation proposal. Authorize clean read-only source checkouts
at exact pinned revisions, source-diff inspection, license and documented
runnable-status verification without service execution, and production of a
responsibility/conformance matrix.

Stage 1 must keep Freewallet, Wallet Attached Storage, the AAuth Person Server,
SOGA governance, participant admission, representative authority,
affected-person assent/refusal, payment/donation, and resource enforcement as
distinct responsibilities. It must preserve B-038's missing live
validity/revocation inputs and B-039's independent affected-person path as open
constraints rather than implying that wallet evidence resolves them. Published
AAuth `-10`, later editor base changes, and R3 must remain separately sourced;
R3 `per-call` is research input, not adopted behavior.

D-035 authorizes no wallet or WAS service execution, integration implementation,
dependency installation, external exposure, production credential use, Misty
access, or G28 activation. Stages 2 through 4 require later independent review
and explicit PI authorization.

## D-036 — Authorize M02 Stage 2 bounded localhost Person Server implementation

PI authorization received on 2026-09-06 after the Stage 2 proposal received
independent PASS results from Claude Gate 1 and Gemini/AGy Gate 2 at
`2debcd10db5b6a7082b04d339b2bb2967cd6de5b`.

Authorize M02 Stage 2 bounded localhost Person Server implementation, including
the narrowly described B-038 live-input repair, using test-only identities and
no execution surface. Authorize a local test-agent acceptance harness and a
small SQLite-backed local store so restart, transaction, and one-authoritative-
transition behavior can be stated and tested explicitly. Test and administrative
fixtures must use a visibly non-protocol `/_test/` namespace.

The implementation must replace spoofable magic-header trust with verified
test cryptographic bindings; derive supported current validity, expiry,
revocation, mission, agent, issuer, and audience inputs from retained Person
Server evidence; keep policy limits separate; and fail closed when a selected
policy requires unavailable delegation-depth, elapsed-time, or attenuation
evidence. This is a bounded partial repair of B-038 for the selected local
person-token profile, not closure of the general backlog item or a conformance
claim.

No wallet/WAS/Posta service execution or dependency installation, external
exposure, production credentials, participant-session implementation,
representative/affected-person policy, Misty access, physical actuation, R3
implementation, or G28 activation is authorized.

## D-037 — Accept M02 Stage 2 bounded localhost Person Server implementation

PI acceptance received on 2026-09-06 after independent forward and reverse
implementation gates and post-PASS hardening rechecks returned PASS. Accept and
authorize committing the bounded localhost Person Server package, D-036,
synchronized canonical state, B-038 partial-repair status, tests, and review
evidence. Final verification passed 44/44 focused Stage 2 tests and 132/132
repository tests before the visible walkthrough harness was added.

The PI additionally required direct terminal-visible evidence before final
gates. The `m02_person_server walkthrough` harness was added within D-036 to
show real loopback HTTP, SQLite state, signed mission/action permission reaching
SOGA, deferred resolution, one-time terminal delivery, and revocation, while
showing explicitly that no execution surface exists. It must receive a narrow
independent review before inclusion in the accepted commit.

D-037 does not authorize M02 Stages 3–4, wallet/WAS/Posta service execution,
external exposure, production credentials, Misty access, physical actuation,
R3 implementation, or G28 activation.

## D-038 — Authorize M02 Stage 3A exact-source runtime reproduction

PI authorization received on 2026-09-07 after the M02 Stage 3 wallet/WAS
composition proposal received independent PASS results from Claude Gate 1 and
Gemini/AGy Gate 2.

Authorize M02 Stage 3A exact-source runtime reproduction under the reviewed
proposal. This authorization permits clean detached checkouts of Freewallet
`8e806c0` and WAS teaching server `2090a60`, lockfile-pinned dependency
installation within those checkouts, and test-only literal-loopback execution
and interface auditing. Package-registry access is permitted only for the
approved dependency installation; application runtime external-network access
is prohibited.

Stop if WAS requires Postgres or Docker, Freewallet requires unavailable
graphical-browser/WebAuthn/WebCrypto support, or either runtime requires source
modification, external services, production credentials, or undocumented
trust. Stage 3A must end with services stopped and a standalone evidence report
reviewed by both gates.

D-038 does not authorize Stage 3B code or tests, Stage 4, public exposure,
personal data, payment, Misty access, physical actuation, R3, G28, or G29.

## D-039 — Accept M02 Stage 3A as a gated negative result

PI acceptance received on 2026-09-08 after the standalone Stage 3A evidence
report received PASS results from Claude Gate 1 and Gemini/AGy Gate 2.

Accept M02 Stage 3A as a gated negative result. Authorize committing and
pushing the standalone evidence report and synchronized canonical state. The
exact selected Freewallet and WAS sources were acquired, installed from their
locked dependencies, and built. No candidate service was started: the selected
WAS executable hardcodes a wildcard `0.0.0.0` listener, which conflicts with
D-038's literal-loopback boundary and could not be changed or wrapped under
Stage 3A authority.

Stage 3B remains unauthorized pending a separately reviewed response to the WAS
wildcard-bind limitation. All other D-038 boundaries remain in force.

## D-040 — Authorize M02 Stage 3A-R source-supported loopback recovery

PI authorization received on 2026-09-08 after the recovery proposal and its
network-containment corrections received PASS results from Claude Gate 1 and
Gemini/AGy Gate 2.

Authorize M02 Stage 3A-R source-supported loopback recovery under the reviewed
proposal. Permit a bounded SOGA research launcher using the exact existing
Freewallet `8e806c0` and WAS `2090a60` build outputs, WAS's documented
package-root exports, temporary test-only storage, finite limits, and literal
`127.0.0.1` listeners. Require the OS-level network-containment preflight to
pass before either candidate starts, and require all services and listeners
stopped afterward.

D-040 authorizes no dependency installation or registry access, upstream source
modification, Stage 3B code or tests, wallet interaction, Person Server
integration, external exposure, personal data, payment, Misty access, physical
actuation, R3, G28, or G29.

## D-041 — Accept M02 Stage 3A-R as a gated negative result

PI acceptance received on 2026-09-08 after the Stage 3A-R evidence report and
its archival correction received PASS results from Claude Gate 1 and
Gemini/AGy Gate 2.

Accept M02 Stage 3A-R as a gated negative result. Authorize committing and
pushing the standalone evidence report and synchronized canonical state. No
launcher or sandbox profile is adopted. The reviewed literal-IP sandbox profile
failed parsing before Node, any synthetic socket, or either candidate ran. The
unsafe unexecuted research machinery was removed; its material profile text and
review findings remain in the standalone evidence record.

Stage 3B remains unauthorized pending a separately reviewed containment
approach. All D-040 boundaries remain in force.

## D-042 — Authorize M02 Stage 3A-R2 fixed-port containment

PI authorization received on 2026-09-08 after the fixed-port containment
proposal received PASS results from Claude Gate 1 and Gemini/AGy Gate 2.

Authorize M02 Stage 3A-R2 fixed-port containment under the independently
reviewed proposal. Permit creation and execution of the bounded research
harness and preflight using the existing exact Freewallet `8e806c0` and WAS
`2090a60` build outputs, fixed ports `46321` and `46322`, temporary test-only
storage, and the reviewed sandbox controls. Require all pre-start controls to
pass and all processes and listeners to stop afterward.

Stage 3B and all other activities excluded by the reviewed proposal remain
unauthorized.

## D-043 — Accept M02 Stage 3A-R2 as a gated negative result

PI acceptance received on 2026-09-08 after the Stage 3A-R2 evidence report and
removal correction received PASS results from Claude Gate 1 and Gemini/AGy
Gate 2.

Accept M02 Stage 3A-R2 as a gated negative result. Authorize committing and
pushing the standalone evidence report and synchronized canonical state. The
fixed-port symbolic-`localhost` sandbox profile passed the literal IPv4 nonce
exchange and denied a different loopback port and TEST-NET, but it also admitted
the prohibited `0.0.0.0` wildcard bind. The required pre-start control therefore
failed and neither candidate was imported, served, or started.

No R2 launcher, preflight program, or sandbox profile is adopted; the temporary
research machinery was removed before acceptance and the standalone report
preserves the executed profile and complete preflight output. Stage 3B remains
unauthorized pending a separately reviewed containment decision. All D-042
boundaries remain in force.

## D-044 — Authorize M02 Stage 3A-R3 Docker containment characterization

PI authorization received on 2026-09-08 after the Docker containment proposal
and its precision corrections received PASS results from Claude Gate 1 and
Gemini/AGy Gate 2.

Authorize Docker Desktop startup, daemon readiness and local-image inventory,
creation and execution of the independently reviewed synthetic containment
preflight, and—only if every preflight control passes—bounded reachability
testing of exact Freewallet `8e806c0` and WAS `2090a60` build outputs in two
disposable containers. Use only a selected immutable, already-local Node 24+
image, fixed host ports `127.0.0.1:46321` and `127.0.0.1:46322`, an internal
Docker network, temporary test-only storage, finite limits, and the reviewed
isolation controls.

Every privilege, license, subscription, update, network-access, or security
prompt is a PI holdpoint. Every preflight or startup script must receive both
independent reviews before execution. Require complete cleanup and standalone
evidence reviewed by both gates.

D-044 authorizes no image pull, build, load, import, registry access,
dependency operation, source modification, Stage 3B work, wallet interaction,
Person Server integration, external exposure, personal data, payment, Misty
access, physical actuation, R3 protocol work, G28, or G29.

## D-045 — Authorize digest-pinned Node image acquisition for Stage 3A-R3

PI authorization received on 2026-09-08 after Claude Gate 1 and Gemini/AGy
Gate 2 independently confirmed the Stage 3A-R3 Phase 0 stop and returned PASS
on the digest-pinned image-acquisition proposal.

Authorize acquisition and verification of the exact `linux/arm64` Node image
identified by full digest in
`knowledge/proposals/M02_STAGE3AR3_NODE_IMAGE_ACQUISITION_PROPOSAL_2026-09-08.md`,
with every boundary and exclusion in that proposal remaining in force. The
selected reference is
`docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb`.

D-045 permits exactly one digest-pinned pull for `linux/arm64`, only the
anonymous Docker Hub token exchange and content-layer downloads intrinsic to
that pull, local immutable metadata verification, and one disposable
network-disabled `node --version` verification container under the reviewed
isolation and resource controls. Exact Node `v24.20.0`, cleanup, standalone
evidence, and both post-execution gates are required.

D-045 authorizes no Docker login, other image, mutable-tag reliance, mirror
substitution, build, load, import, tag, push, package operation, containment
preflight, port publication, candidate execution, Stage 3B, wallet interaction,
Person Server integration, external exposure, personal data, payment, Misty
access, physical actuation, R3 protocol work, G28, or G29.
