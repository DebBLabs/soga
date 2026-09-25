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

## D-046 — Accept Stage 3A-R3 digest-pinned Node image acquisition

PI acceptance received on 2026-09-08 after the standalone acquisition evidence
received PASS results from Claude Gate 1 and Gemini/AGy Gate 2.

Accept M02 Stage 3A-R3 digest-pinned Node image acquisition and isolated
verification as a gated positive result. Authorize committing and pushing the
standalone acquisition evidence and synchronized canonical state. The exact
`linux/arm64` Docker Official Image selected under D-045 is locally retained by
full digest and returned Node `v24.20.0` in the reviewed network-disabled,
disposable verification container. Cleanup was independently confirmed.

Proceed under D-044 to create, but not execute, the synthetic containment
preflight and candidate-startup scripts for full independent review. Neither
script, the containment preflight, nor any candidate may run until both script
reviews pass. Stage 3B and all other D-044 and D-045 exclusions remain in force.

## D-047 — Authorize Stage 3A-R3 synthetic containment preflight execution

PI authorization received on 2026-09-08 after the complete synthetic
containment preflight and candidate-startup scripts received PASS results from
Claude Gate 1 and Gemini/AGy Gate 2. The reviewed corrections make functional
success contingent on cleanup success, preserve pre-existing resource
collisions, make asset selection deterministic, start the candidate holdpoint
only after both services are ready, and bound failure diagnostics.

Authorize execution of only the independently reviewed M02 Stage 3A-R3
synthetic Docker containment preflight, using the exact digest-pinned image and
reviewed script. Complete cleanup and a standalone evidence report reviewed by
both gates are required.

Candidate startup remains prohibited unless the synthetic preflight passes and
the PI separately authorizes proceeding. Stage 3B and all D-044 through D-046
exclusions remain in force. The separate PI routine-tool-approval proposal is
unadopted and outside this decision.

## D-048 — Accept Stage 3A-R3 synthetic containment preflight as a negative result

PI acceptance received on 2026-09-08 after the standalone synthetic preflight
evidence received PASS results from Claude Gate 1 and Gemini/AGy Gate 2.

Accept M02 Stage 3A-R3 synthetic containment preflight as a gated negative
result. The internal Docker network passed its initial control, but the
literal-loopback synthetic nonce endpoint did not become ready within the
finite readiness window. The preflight exited nonzero and cleanup was confirmed:
no R3 container, R3 network, or fixed-port listener remained. No candidate was
started or contacted.

Authorize committing and pushing the standalone evidence report and
synchronized canonical state. Candidate startup remains prohibited. Any
diagnosis, script modification, repeated preflight, or alternative containment
attempt requires a separately reviewed proposal and authorization. Stage 3B
and all D-047 exclusions remain in force.

## D-049 — Authorize Stage 3A-R3 diagnostic recovery Phase 1 script creation

PI authorization received on 2026-09-09 after
`knowledge/proposals/M02_STAGE3AR3_PREFLIGHT_DIAGNOSIS_RECOVERY_PROPOSAL_2026-09-09.md`
received PASS results from Claude Gate 1 and Gemini/AGy Gate 2, including a
recheck of its cleanup tradeoff, complete interpretation set, and prospective
authorization sequence.

Authorize M02 Stage 3A-R3 diagnostic recovery Phase 1 under that independently
reviewed proposal. Permit modification of only
`tools/m02_stage3ar3/preflight.py` to create—but not execute—the corrected
synthetic diagnostic preflight, including bounded readiness timing, container
state and log capture, self-readiness probing, explicit subprocess timeouts,
async probe compatibility, and fail-closed cleanup controls.

Both independent reviewers must read the complete corrected script and return
PASS before it is committed or executed. Candidate startup, Docker execution,
preflight repetition, Stage 3B, candidate access, external services, Misty
access, and every other proposal exclusion remain prohibited.

## D-050 — Accept and authorize one corrected Stage 3A-R3 diagnostic preflight

PI acceptance and authorization received on 2026-09-09 after the complete
corrected `tools/m02_stage3ar3/preflight.py` received PASS results from Claude
Gate 1 and Gemini/AGy Gate 2. The reviewed script repairs path-dependent
readiness timing, removes Node evaluation and argument ambiguity, captures
bounded container and self-readiness diagnostics, gives every subprocess a
finite timeout, redacts host LAN addresses, and makes success contingent on
best-effort complete cleanup and absence verification.

Accept the corrected synthetic diagnostic preflight as independently reviewed.
Authorize committing and pushing the exact reviewed script, then executing it
once under the committed recovery proposal using only the cached digest-pinned
Node image and synthetic resources. Independent post-run cleanup verification
and a standalone evidence report reviewed by both gates are required.

Candidate startup and every D-049 exclusion remain prohibited. Any additional
run, script modification, candidate access, or expanded diagnosis requires a
new reviewed proposal or authorization as applicable.

## D-051 — Accept corrected Stage 3A-R3 diagnostic preflight as a negative result

PI acceptance received on 2026-09-09 after the standalone corrected diagnostic
preflight evidence received PASS results from Claude Gate 1 and Gemini/AGy Gate
2. Gate 1 independently reproduced the post-run cleanup checks; Gate 2 verified
the complete report, committed script, decision boundary, and interpretation
using file-read-only inspection.

Accept M02 Stage 3A-R3 corrected diagnostic preflight as a gated negative
containment result with positive server-health discrimination. The corrected
preflight made 49 host-loopback connection attempts over approximately 9.8
seconds. At the diagnostic point, the synthetic container remained running,
its bounded log contained `LISTENING_OK`, and its internal self-readiness probe
received the expected nonce. The evidence therefore localizes the observed
failure to the host-publication path for the exact tested topology without
identifying a particular Docker component or rule and without generalizing to
other hosts or configurations.

The later non-loopback-host and container-egress controls did not run, so the
complete containment preflight did not pass. Cleanup was independently
confirmed: no matching R3 container, R3 network, or fixed-port listener
remained. No candidate, wallet, Person Server integration, Stage 3B path, or
Misty system was started or accessed.

Authorize committing and pushing the standalone evidence report and
synchronized canonical state. The one D-050 execution is consumed. Candidate
startup remains prohibited. Any additional run, script change, comparison,
alternative containment design, or candidate access requires separate review
and prospective authorization. All D-050 exclusions remain in force.

## D-052 — Authorize Stage 3A-R4 internal-only preflight script creation

PI authorization received on 2026-09-09 after
`knowledge/proposals/M02_STAGE3AR4_INTERNAL_ONLY_CONTAINMENT_PROPOSAL_2026-09-09.md`
received PASS results from Claude Gate 1 and Gemini/AGy Gate 2. The corrected
proposal makes the claimed result IPv4-only, treats gateway or host-alias active
refusal as disqualifying reachability, excludes Docker embedded-DNS forwarding
from its claim, covers current and legacy Docker Desktop aliases, prohibits
namespace sharing, and keeps precondition and cleanup failures distinct.

Authorize M02 Stage 3A-R4 Phase 1 script creation under the independently
reviewed internal-only containment proposal. Permit creation—but not execution—
of the new R4 synthetic preflight script using the exact cached digest-pinned
Node image specification, two isolated synthetic containers, no host
publication, IPv4-only internal networking, bounded probes, redaction, finite
limits, and fail-closed cleanup. Do not modify the accepted R3 scripts.

Both independent reviewers must read the complete R4 script and return PASS
before it is committed or executed. Docker execution, candidate startup or
access, Freewallet or WAS execution, Stage 3B, wallet interaction, Person Server
integration, external services, Misty access, and every other proposal
exclusion remain prohibited.

## D-053 — Accept and authorize one Stage 3A-R4 synthetic preflight

PI acceptance and authorization received on 2026-09-09 after the complete
`tools/m02_stage3ar4/preflight.py` received PASS results from Claude Gate 1 and
Gemini/AGy Gate 2. The reviewed script creates two independent, unprivileged
synthetic containers on one IPv4-only internal network; publishes no host port;
requires an exact digest-pinned cached image; applies finite resource and time
limits; treats active gateway or host-alias refusal as disqualifying; bounds and
redacts output; captures failure diagnostics; and makes success contingent on
complete cleanup.

Accept the R4 synthetic preflight script as independently reviewed. Authorize
committing and pushing the exact reviewed file, then executing it once using
only the cached digest-pinned Node image and synthetic resources under the
adopted internal-only containment proposal. Complete cleanup, independent
cleanup verification, and a standalone evidence report reviewed by both gates
are required.

Candidate startup and access, Freewallet or WAS execution, Stage 3B, wallet
interaction, Person Server integration, external services, Misty access, and
every D-052 exclusion remain prohibited. Any additional execution or script
change requires separate prospective authorization.

## D-054 — Accept Stage 3A-R4 internal-only preflight as a negative result

PI acceptance received on 2026-09-09 after the standalone R4 internal-only
synthetic preflight evidence received PASS results from Claude Gate 1 and
Gemini/AGy Gate 2. Gate 1 independently reproduced the cleanup checks; Gate 2
verified the complete report, committed script, decision boundary, and control
sequence using file-read-only inspection.

Accept M02 Stage 3A-R4 internal-only synthetic preflight as a gated negative
result at the in-container IPv6 control. Docker-level inspection reported the
internal network IPv6-disabled and the server endpoint without an IPv6 address
or gateway, while the separate in-container kernel check returned the combined
category `ipv6_present`. That category establishes only that a non-loopback IPv6
address or a default-route record was observed; it does not identify which,
establish usable IPv6, host, or external reachability, or establish candidate
containment.

Both synthetic processes were healthy at the stop point. The later readiness,
inter-container, host-publication, TEST-NET, gateway, host-alias, and DNS
controls did not run. Cleanup was independently confirmed: no matching R4
container, R4 network, or fixed-port listener remained. No candidate or
external system was started or accessed.

Authorize committing and pushing the standalone evidence report and
synchronized canonical state. The one D-053 execution is consumed. Candidate
startup and access remain prohibited. Any IPv6-specific diagnosis, script
change, additional execution, alternative containment design, or candidate
access requires separate review and prospective authorization. All D-053
exclusions remain in force.

## D-055 — Authorize Stage 3A-R4 IPv6 diagnosis script creation

PI acceptance and authorization received on 2026-09-09 after the complete
`knowledge/proposals/M02_STAGE3AR4_IPV6_CONTROL_DIAGNOSIS_PROPOSAL_2026-09-09.md`
received PASS from Claude Gate 1 and Gemini/AGy Gate 2. Gate 1 initially found
that the pre-start inventory both prohibited enumeration and required an
undefined classification of MCP-related resources. The corrected proposal
separates internal inspection from emitted output and replaces classification
with two objective holdpoints: zero pre-existing running Docker containers and
zero Docker-published host ports. Both gates then returned PASS with no required
corrections.

Accept the M02 Stage 3A-R4 IPv6 control diagnosis proposal as independently
reviewed. Authorize Phase 1 script creation only: create, but do not execute,
the bounded diagnostic script under the exact reviewed proposal. Require both
independent reviewers to read the complete script and return PASS before commit
or execution.

No Docker execution, candidate startup or access, R4 preflight repetition,
reachability testing, MCP invocation, external service, Stage 3B, Misty access,
or policy change is authorized. Phase 2 requires the exact script to be
committed after both reviews and a separate prospective PI authorization for
one execution.

## D-056 — Authorize one Stage 3A-R4 IPv6 diagnosis execution

PI authorization received on 2026-09-09 after the exact diagnosis proposal,
D-055, synchronized state, and `tools/m02_stage3ar4/ipv6_diagnosis.py` were
committed and pushed at `aac9b7d46d40bf27599d6a64866343e12111224d`. Claude
Gate 1 and Gemini/AGy Gate 2 read the complete unexecuted script and returned
PASS after cleanup-reporting corrections. The exact committed script has not
been executed, imported, compiled, linted, or tested.

Authorize one Phase 2 execution of the exact committed M02 Stage 3A-R4 IPv6
diagnosis script at `aac9b7d` under D-055. Require all pre-start holdpoints,
finite limits, fail-closed cleanup, independent cleanup verification, a
standalone evidence report, and review by both gates.

No R4 preflight repetition, candidate startup or access, reachability testing,
MCP invocation, external service, Stage 3B, Misty access, or policy change is
authorized. This one execution is consumed when the process starts, including
if it stops at a pre-start holdpoint or fails.

## D-057 — Accept Stage 3A-R4 IPv6 diagnosis as a negative result

PI acceptance received on 2026-09-09 after the standalone D-056 evidence
received PASS from Claude Gate 1 and Gemini/AGy Gate 2. Gate 1 independently
confirmed that no fixed diagnostic container, diagnostic network, or inherited
port listener remained. Both gates verified that the exact committed script
stopped at the configured-binding holdpoint before image inspection, resource
creation, procfs reading, or any IPv6 diagnosis.

Accept M02 Stage 3A-R4 IPv6 diagnosis as a gated negative result at the
pre-start configured-binding holdpoint. The bounded inventory observed zero
running Docker containers and two configured `HostConfig.PortBindings` across
the stopped-container inventory. That count does not establish two active host
listeners and identifies no unrelated container or port. The result establishes
no IPv6 condition and no candidate containment.

Authorize committing and pushing D-056, this acceptance, the standalone
evidence report, and synchronized canonical state. No environment inspection
or change, binding identification or removal, holdpoint revision, rerun,
candidate access, Stage 3B, MCP invocation, external service, Misty access, or
policy change is authorized.

## D-058 — Authorize M02 Stage 3-Lib Phase 0 exact-source reacquisition

PI authorization received on 2026-09-10 after
`knowledge/proposals/M02_STAGE3LIB_SOCKET_FREE_WAS_FEASIBILITY_PROPOSAL_2026-09-10.md`
received PASS from Claude Gate 1 and Gemini/AGy Gate 2. Gate 1 first returned
NOT READY on provenance, socket/IPC classification, objective observation,
module resolution, credential-material rules, cleanup, and phase separation.
After correction it identified two additional synchronization and commit-hygiene
gaps. The final complete-file recheck returned PASS. Gate 2 returned PASS on the
initial proposal and both corrected complete-file rechecks. Both reviews were
read-only at `ff16893c148bf4a7a7b19e42d0a9d364739ed18a`; neither candidate was
acquired, installed, built, imported, or executed during review.

Authorize M02 Stage 3-Lib Phase 0 exact-source reacquisition and build
verification under the independently reviewed proposal. Use the fixed temporary
root `/private/tmp/m02-stage3lib-20260910` and reacquire only WAS teaching server
commit `2090a606f2723e4d57ef0090db55fd1bdab9427e` from its recorded origin
through a plain detached checkout with no submodule or LFS fetch. Permit one
`pnpm@11.20.0` frozen-lockfile installation with a checkout-local runner cache
and only the Git and package-registry access intrinsic to those operations.

Require exact origin, commit, version, license, lockfile hash, Node version,
clean-source status, build result, and any `tsx` IPC-pipe event to be recorded
in standalone evidence and reviewed by both gates. Preserve the verified
checkout, dependency tree, and cache unchanged pending PI disposition.

This does not authorize Phase 1 harness or test creation, WAS import or
execution, any listener, Docker, Freewallet, wallet interaction, Person Server
integration, Stage 3B, external runtime services, personal data, payment, Misty
access, physical actuation, G28, or G29.

## D-059 — Accept Stage 3-Lib Phase 0 and authorize Phase 1 creation

PI acceptance and authorization received on 2026-09-10 after
`knowledge/research/M02_STAGE3LIB_PHASE0_ACQUISITION_BUILD_EVIDENCE_2026-09-10.md`
received PASS with no required corrections from Claude Gate 1 and Gemini/AGy
Gate 2. Both reviewers independently verified the preserved checkout at exact
commit `2090a606f2723e4d57ef0090db55fd1bdab9427e`, its hashes, tracked-clean
source, build output, cache-only untracked state, public package-root exports,
`createApp` construction, health route, and the evidence record's limited IPC
and no-runtime claims. No candidate was imported or executed during review.

Accept M02 Stage 3-Lib Phase 0 exact-source acquisition and build evidence as
independently verified. Authorize committing and pushing the standalone Phase 0
evidence and synchronized canonical state. Preserve the exact checkout,
dependency tree, runner cache, and build output unchanged.

Authorize M02 Stage 3-Lib Phase 1 create-only harness and test implementation
under the reviewed proposal. Create only reviewed SOGA-owned source under
`tools/m02_stage3lib`. Require the `FileSystemBackend` data root to be an
explicit temporary directory outside both the SOGA repository and WAS checkout.
Include the fail-closed network-attempt guards, dynamic import ordering,
temporary execution-time package-root symlink logic, finite limits, local
test-material rules, cleanup controls, and tests specified by the proposal.
Also record the exact whole-source finding that the selected WAS source contains
one `.listen(` call, only in `src/start.ts:66`.

Do not execute, import, compile, lint, or test the harness before both
independent reviewers read the complete files and return PASS. No WAS
application execution, listener, Phase 2, Freewallet, wallet interaction,
Person Server integration, Stage 3B, Docker, external runtime service, personal
data, payment, Misty access, physical actuation, G28, or G29 is authorized.

## D-060 — Accept and commit Stage 3-Lib Phase 1 source

Recorded retrospectively on 2026-09-14 without backdating. PI acceptance was
received on 2026-09-10 after Claude Gate 1 and Gemini/AGy Gate 2
read the complete create-only package under `tools/m02_stage3lib`. Initial
reviews returned NOT READY on repository-boundary polarity, repository-root
selection, valid local `did:key` construction, cleanup independence, timeout
termination, test/source agreement, and error preservation. Corrected
complete-file rechecks returned PASS from both gates without executing,
importing, compiling, linting, or testing the package.

Accept M02 Stage 3-Lib Phase 1 create-only harness and tests as independently
reviewed. Authorize committing and pushing only the exact reviewed files under
`tools/m02_stage3lib`. Preserve the exact WAS checkout, dependency tree,
runner cache, and build output unchanged.

That preservation directive records the historical acceptance as given; it was
not met. The temporary root was later found absent after host shutdown. See
B-043 and the proposed exact-environment restoration. This retrospective record
creates no restoration or execution authority. Phase 1 review reports remain
PI-retained outside the repository; D-060 records their scope, sequence, and
results so the canonical decision does not depend on opening the transcripts.

The accepted files were committed and pushed at
`a3a8a87d6d49052f75093b0ae3d380102f73ab10`. This decision authorized source
adoption only. It did not authorize Phase 2 execution, WAS application startup,
a listener, Freewallet, wallet interaction, Person Server integration, Docker,
an external service, personal data, payment, Misty access, physical actuation,
G28, or G29.

## D-061 — Record Option A restoration authorization and consumed negative attempt

Recorded retrospectively on 2026-09-14 without backdating. After commit
`a77d86d1170762bed707011735e1464d4b9403e1` committed the independently reviewed
restoration proposal, the PI explicitly selected Option A and authorized its
exact Git reacquisition, single frozen dependency installation, and single
upstream build before any of those operations began. The authorization was
given directly in the governing conversation but was not recorded in this log
before execution. This entry records the actual sequence; it does not claim
that checkpoint `a77d86d` itself contained execution authority.

The exact source fetch and frozen installation succeeded. The one build attempt
stopped nonzero at upstream `tsx` local-IPC pipe creation during
`write-build-info`. No retry, harness/test execution, WAS application startup,
or Phase 2 activity followed. The attempt is consumed and restoration is not
complete.

The npx debug record shows registry requests for an npm update check, pnpm
metadata, a security-advisory POST carrying the pnpm package identifier, and
the pnpm tarball. The update check and advisory request were not specifically
enumerated in the proposal. Their boundary classification remains for PI
disposition after independent review; this entry does not expand authorization
retrospectively. Phase 2 and every proposal exclusion remain in force.

After both independent gates returned PASS, the PI accepted this as a gated
negative result. The single attempt is consumed, restoration is incomplete,
B-043 remains open, and Phase 2 remains unauthorized. The npm update-check GET
and security-advisory POST are classified as an unanticipated network-boundary
variance that does not invalidate the source or failure evidence; future
dependency authorizations must explicitly address or suppress them. The
recorded `npx --version` check produced no observed network record.

Preserve the exact partial environment unchanged at the non-durable Option A
path as research evidence. It is not usable by the harness. Any retry,
diagnosis, permission change, build, harness execution, or Phase 2 work
requires a new independently reviewed proposal and prospective authorization.

Subsequent amendment on 2026-09-14: the PI abandoned the unadopted build-recovery
proposal without execution. A read-only check of the exact preserved source
established that `assertFreshBuild()` is called only by the standalone server
startup path; direct `createApp()` library use is unaffected, and `/health`
falls back to the package version when `dist/build-info.json` is absent. The
preserved compiled `dist/` is therefore conditionally usable for a separately
authorized Phase 2 library test. Its provenance rests on the independently
reviewed restoration evidence because the build stamp is absent, and a complete
`dist/` hash manifest must be recorded before Phase 2 relies on it. This
amendment does not complete restoration, close B-043, or authorize Phase 2,
WAS application startup, listeners, network access, dependency changes, or any
other previously excluded activity.

## D-062 — Authorize one M02 Stage 3-Lib Phase 2 socket-free execution

Recorded prospectively on 2026-09-14 before any Phase 2 test, controller, or
harness execution. Both independent gates returned PASS on the exact proposal
`knowledge/proposals/M02_STAGE3LIB_PHASE2_EXECUTION_PROPOSAL_2026-09-14.md`;
Gate 1's conditional PASS became unconditional after its two exact fail-closed
edits were applied and confirmed by a diff-only recheck.

The PI accepts that proposal and authorizes committing and pushing it with this
decision, followed by one execution of its exact controller, source-contract
tests, and socket-free WAS harness. The execution must use the fixed candidate,
Node executable, paths, manifest, time bounds, readiness synchronization,
network-attempt guards, unprivileged observations, cleanup checks, standalone
evidence, stop rules, and exclusions stated in the reviewed proposal.

This decision authorizes no build or dependency operation, network listener or
network access, WAS standalone startup, retry, diagnosis, repair, Freewallet,
wallet or Person Server integration, Stage 3B, Docker, external service,
personal data, payment, Misty access, physical actuation, MCP invocation, R3,
G28, G29, or policy change. The one execution attempt is consumed when the
source-contract test or controller begins. Its result may not be adopted until
standalone evidence receives both independent reviews and PI disposition.

Review-sequence correction: Gate 1 prescribed and later confirmed two exact
fail-closed controller edits before execution. Gate 2 had passed the preceding
proposal revision, not those final edits. D-062's statement that both gates had
passed the exact proposal before execution was therefore inaccurate. Gate 2
subsequently verified byte-for-byte that the executed controller matched the
committed final proposal and returned PASS during the post-run evidence gate.
That retrospective verification supports the evidence but does not rewrite the
prospective sequence.

## D-063 — Accept Stage 3-Lib Phase 2 socket-free WAS feasibility

On 2026-09-15, after both independent post-run evidence gates returned
unconditional PASS, the PI accepted M02 Stage 3-Lib Phase 2 as a gated positive
result. The exact WAS teaching-server candidate loaded through its public
package-root library surface; in-memory Fastify injection returned health 200
and one bounded temporary Space provision returned 201 and was verified through
`FileSystemBackend`. The harness recorded zero guarded network attempts, the
synchronized live-PID observation found zero TCP/UDP sockets, the unprivileged
user-visible TCP listener snapshots were unchanged, all 298 compiled artifacts
were unchanged, and cleanup completed.

The accepted evidence is
`knowledge/research/M02_STAGE3LIB_PHASE2_EXECUTION_EVIDENCE_2026-09-14.md`.
This result establishes socket-free WAS library feasibility only. It does not
establish Freewallet interaction, wallet-controlled production storage, Person
Server integration, AAuth conformance, external-service containment, identity,
authority, consent, mission permission, participant sessions, Misty readiness,
or physical execution.

This acceptance authorizes committing and pushing the reviewed evidence and
synchronized canonical state. It does not authorize Stage 3B, Freewallet or
Person Server integration, external services, dependency or network activity,
Misty access, G28, G29, or disposal of preserved non-durable evidence.

## D-064 — Adopt the Risk-Based Independent Review Method

Recorded prospectively on 2026-09-15. The PI accepts and adopts
`knowledge/proposals/RISK_BASED_INDEPENDENT_REVIEW_METHOD_2026-09-15.md` at
SHA-256
`ede23e99ea02c02e76cc4c07a00d6cd0eff02c95c7d23ef88724a67b7d858b22` as a
governance-process change requiring mandatory dual review.

Codex authored and integrated the method. Claude and the earlier Codex review
subagent are disclosed contributors and did not count as independent final
reviewers. Gemini/AGy Gate 2 and the fresh read-only Codex reviewer
`/root/final_method_review` independently reviewed the exact final hash and
returned PASS with no blocking or optional findings.

The method is operative prospectively from this decision. It changes review
routing, authorship allocation, bounded correction practices, and capacity
continuity only. It grants no implementation, execution, external-access,
commit, physical-action, G28, or G29 authority. D-028 remains controlling for
queue authority, and B-041 and B-042 remain in force. The separate PI
routine-tool-approval proposal remains unadopted and outside this decision.

## D-065 — Authorize M02 Stage 3B-1 create-only composition source

Recorded prospectively on 2026-09-15. After independent final PASS reviews by
Claude Gate 1 and Gemini/AGy Gate 2, the PI accepts
`knowledge/proposals/M02_STAGE3B_PERSON_SERVER_WAS_COMPOSITION_PROPOSAL_2026-09-15.md`
at SHA-256
`6e55b3aa4d1d9df477db279e82cde822ba02228bc7f20b62c2d446c16857c12a`.

This decision authorizes committing and pushing that exact proposal, followed
by Phase 3B-1 creation only of its complete adapter, Node worker, controller,
and tests. The created files require complete independent review by both
eligible gates before execution.

No WAS import or execution, code compilation or test run, HTTP-service start,
listener, network or external-service access, dependency change, Phase 3B-2,
Freewallet, personal data, payment, Misty access, physical actuation, G28, or
G29 is authorized. The unrelated PI routine-tool-approval proposal remains
excluded and untouched.

## D-066 — Accept disclosed Phase 3B-1 review-independence deviation

Recorded on 2026-09-15 without backdating or changing any earlier decision.
The PI summarized Gate 2's disclosure as follows: Gate 2 read Gate 1's response
before writing its own in most review rounds, including 001–005, 013–015, and
026–029; Gate 1 reviewed blind. The saved Gate 2 response files do not
themselves contain that disclosure, so this record treats the PI's wording as a
summary rather than a verbatim statement by Gate 2.

The PI accepts this as a deviation from D-064. For Phase 3B-1, the review basis
is Gate 1's blind independent PASS plus Gate 2's informed corroborating PASS.
Past decisions remain in force. Unless individually confirmed otherwise, every
Gate 2 review in this HOPE queue is reclassified as informed corroboration, not
an independent final review. This includes Gate 2 review bases relied on by
D-061 through D-065, including rounds 017–018, 019–022, and 023–025 in addition
to the rounds named above. Those decisions are not reopened, and their technical
findings remain in force.

B-044 records the affected rounds and prospective controls. Beginning with the
Phase 3B-2 evidence review, each gate receives its own hash-pinned request;
neither reviewer may open the other gate's request or response directory, or
`claude-to-cg/`, before posting; every response must end with an explicit
independence statement; and the coordinator must verify both statements before
describing the reviews as independent. Gate 1 contributed wording to D-066 and
B-044 and is not an independent reviewer of those records.

Codex authored and integrated the Phase 3B-1 source reviewed at request 029:

- `m02_was_composition/__init__.py` — SHA-256
  `62e10c1f9bee9b3f27d1f0acb17f71a34ea89fcf30e39f93b83bb620de3d5f97`;
- `m02_was_composition/adapter.py` — SHA-256
  `9b1407c61303ae2c761ae3ecbd11b88256e779338de65d4083789bf232db15ad`;
- `m02_was_composition/worker.mjs` — SHA-256
  `ab3dda127a499452503ebff30bd93d13233dac27a49d10f2b9fc4f1dc177c9ec`;
- `m02_was_composition/controller.py` — SHA-256
  `8a0d3c9a2b5c570cbe158015add4413f654d918907899dccd47519efa8d73206`;
- `tests/test_m02_was_composition.py` — SHA-256
  `8c03c698294c082e07d41a4317bf3b38066b95618090ca65e1f2023ad2001539`.

D-066 accepts that source as input to a prospective Phase 3B-2 authorization
decision. D-066 itself authorizes no commit, import, test, execution, external
access, Freewallet integration, Misty access, G28, or G29.

## D-067 — Accept Phase 3B-1 and authorize one Phase 3B-2 execution

Recorded prospectively on 2026-09-15 before any Phase 3B-2 import, test, or
execution. The PI accepts Phase 3B-1 on the D-066 review basis: Gate 1's blind
independent request-029 PASS plus Gate 2's informed corroborating PASS.

The PI authorizes committing and pushing the five exact hash-pinned source
files recorded in D-066 together with D-066, B-044, and synchronized canonical
state. After that commit, the PI authorizes one execution of the exact committed
controller and focused test suite under D-065, with all stated limits,
observations, cleanup requirements, evidence requirements, and exclusions.

The resulting evidence must receive two blind independent reviews under B-044
before acceptance. No external service, listener, Freewallet integration,
personal data, payment, Misty access, physical actuation, G28, or G29 is
authorized.

## D-068 — Accept Phase 3B-2 gated negative result

Recorded on 2026-09-15 after the single D-067 execution and its evidence
review. The PI accepts M02 Stage 3B-2 as a gated negative result at
`execution:focused_tests`. The D-067 execution is consumed; no specific
failing test or cause is established.

The accepted evidence is
`knowledge/research/M02_STAGE3B_PHASE2_EXECUTION_EVIDENCE_2026-09-15.md` at
SHA-256
`e27869c9690ceb50257fca688a519e8ebbba82662f377ac1384b2dd23089a83a`.

The first B-044 blind mandatory-dual review completed successfully at request
033. Both gates received separate hash-pinned requests, stated that they saw no
other gate's review or correction material before posting, and independently
returned PASS. The coordinator verified both statements before characterizing
the reviews as independent. B-044 is closed.

This decision authorizes committing and pushing the evidence, this acceptance
record, B-044 closure, and synchronized canonical state. It authorizes no
diagnosis, code change, test execution, retry, external service, Freewallet
integration, Misty access, G28, or G29.

## D-069 — Authorize create-only diagnostic instrumentation

Recorded prospectively on 2026-09-16 before implementation. The PI accepts the
diagnostic instrumentation proposal at SHA-256
`06d4833e17f617b83542c4fee32c26d563aa1ea476907d21975e67bb81174ea0` after
both blind request-035 reviewers returned PASS. Codex is author/integrator;
Claude's general retention recommendation is non-authoring review guidance.

Authorize only the proposal's create-only controller modification, diagnostic
runner, and synthetic instrumentation tests. Both eligible blind reviewers must
inspect the complete created files before commit or execution. No imports,
compilation, lint, tests, diagnostic run, composition repair, or other excluded
activity is authorized. The adapter, worker, existing focused tests, exact WAS
environment, and unrelated PI routine-tool proposal remain untouched.

## D-070 — Accept reviewed diagnostic instrumentation for commit

Recorded on 2026-09-16 after both blind request-037 source reviewers returned
PASS and the coordinator verified their independence statements. The PI's
instruction to proceed accepts the create-only instrumentation and authorizes
committing and pushing the exact reviewed source, proposal, D-069, this
acceptance record, and synchronized state.

Codex is author/integrator. The accepted source SHA-256 values are:

- controller: `f8e0775b6351f9626fc5dcd3ad94a17be0b0b233de27c7895056fdc6a1736dcf`;
- diagnostic runner: `26396fa08b02a1971276604bfa7f474ff055c14a88e25075286c6576e59c3b1a`;
- synthetic tests: `e468530de98b29b8849c8ef92668c095d031b13a11a097430381ca50d6120c49`.

No import, compilation, lint, test, diagnostic run, composition repair, or other
excluded activity is authorized. A separate execution proposal may be prepared
for blind review; execution remains held for prospective PI authorization.

## D-071 — Authorize create-only diagnostic bytecode correction

Recorded prospectively on 2026-09-16. The PI authorizes only a create-only
controller correction preserving `PYTHONDONTWRITEBYTECODE=1` in the diagnostic
child environment. Both blind reviewers must PASS the exact corrected source
and revised execution proposal before commit or execution. No tests, diagnostic
run, composition repair, or other excluded activity is authorized.

## D-072 — Authorize one bounded diagnostic execution

Recorded prospectively on 2026-09-16 after the PI instructed “perform diagnostic
run”. Both blind request-039 reviewers returned PASS on the corrected controller
and execution proposal; their independence statements and target hashes were
verified. The reviewed files were committed and pushed at
`8e69a6a7cd03ba76716555349324e1d60812ee3d`.

Authorize the proposal's single synthetic instrumentation check, followed only
on success by its single diagnostic controller invocation, with exact inputs,
minimal environment, finite process-group limits, redacted retained evidence,
cleanup verification, and subsequent blind dual evidence review. Record the
resulting execution commit before invoking either process. No retry, composition
repair, dependency change, listener, external service, Freewallet integration,
Misty access, physical action, G28, or G29 is authorized.

## D-073 — Accept diagnostic gated negative result and pause

Recorded on 2026-09-16 after the PI agreed to accept and wrap up this round.
Both request-040 reviewers returned PASS on evidence SHA-256
`cdd474696d906a4467e7e1e0b7bf74b2f386a0fa6198660c7e3d77d8a26fa8ca`.
Their blind independence/non-contributor statements were verified. These are
evidence-quality passes, not composition acceptance.

Accept the single D-072 execution as a gated negative result: seven synthetic
tests passed; 31 focused tests produced seven failures and two errors. Failing
methods are identified, but stages remain unknown and causes are unresolved.
The attempt is consumed. Controller postflight and independent scoped cleanup
inspection passed. Retain the diagnostic directory and exact WAS environment
unchanged. A worker-stage allowlist mismatch is only a reviewer hypothesis.

Authorize commit and push of the exact reviewed evidence, this acceptance,
and synchronized canonical state. Pause here. Further diagnosis, code change,
test/run, retry, dependency operation, external service, listener, Freewallet
integration, personal data, payment, Misty access, physical actuation, G28,
and G29 remain unauthorized. The unrelated PI proposal is excluded.

## D-074 — Authorize source-only composition diagnosis

Recorded on 2026-09-17 pursuant to the PI's “proceed”, before diagnosis report
creation or any execution. Both blind request-042 reviewers passed the corrected
request-041 proposal at SHA-256
`eff8b224fdc717e765ebf0e5f35dbda32fc9003094d51692dfc426f2d5c4946b`;
their independence statements and final hash were verified.

Authorize only its local text/source inspection and standalone research report.
No imports, tests, code execution, repairs, retry, network, dependency operation,
listener, Freewallet integration, Misty access, physical action, G28 or G29.
Report acceptance, canonical synchronization, commit/push and any subsequent
implementation or execution require separate PI acceptance.

## D-075 — Accept source-only diagnosis research

Recorded on 2026-09-17 following the PI's current-session permission to proceed.
Accept the request-043-reviewed report at SHA-256
`8c0aa2f2a469489aaf86ed1ab95357571988feabfe917257853c5056bc7381a7`.
Both reviewers returned PASS and disclosed blind independent/non-authoring review;
the coordinator verified those statements. Their source verification was scoped,
not an exhaustive dependency/runtime audit. No execution cause is established.

The directly imported interpreter json module inspection is explicitly accepted
as local read-only dependency research; its path/hash and limits are disclosed
in the report. This grants no interpreter or candidate code execution.

Authorize commit/push of the reviewed proposal/report, D-074, this acceptance,
and synchronized state, and preparation/review of a combined create-only
correction proposal. Source-supported package-resolution, guard-mode, byte-contract
and fixture contradictions are research findings, not proof of repaired interop.
The current-session permission does not prospectively adopt an unseen correction
design or lift code/execution holdpoints. Implementation, imports, compilation,
lint, tests, retry, network, dependencies, listeners, Freewallet integration,
Misty access, physical action, G28 and G29 remain unauthorized.

## D-076 — Authorize combined create-only correction

Recorded prospectively on 2026-09-17 following the PI's “Authorized to proceed
with create implementation”. Both blind request-044 reviewers passed the combined
proposal at SHA-256
`d22f91d0d23c2b004fa620ed02cd4810e7b91563f6b3d048b08a19d3b3fd8cc3`.
Their independence statements and final target hash were verified.

Authorize only the proposal's five-file create-only source/test corrections,
preserving explicit candidate identity, guards, limits and cleanup. Both eligible
blind reviewers must inspect complete created files before commit or execution.
No imports, compilation, lint, tests, candidate execution, retry, network,
dependency change, listener, Freewallet integration, Person Server change,
Misty access, physical action, G28 or G29 is authorized.

## D-077 — Accept reviewed combined corrections

Recorded on 2026-09-17 following the PI's “yes please commit and proceed”.
Accept the exact five-file final source reviewed in request 046. Both eligible
reviewers returned blind independent PASS with no blocking findings; current
file hashes match their dispatch. AGy explicitly corrected seven inaccurate
descriptions in its earlier request-045 report; that earlier prose is not relied
on as source evidence. Claude supplied a non-authoring stage-coverage finding;
Codex authored and integrated the correction and regression test.

Final SHA-256 pins:
- adapter.py: 28bcbaeda80c7436353e6872e3fa2f35390e4089ae1ea7d5c64ced93afe071e7
- worker.mjs: f3f58b1d603228c057d9a5af99045cd5783ea5a92ffaa0e550fc0cc1ce2d5b60
- diagnostic_tests.py: 794a1b961d976abeaad044221e031358922016e9817c891e2403663337719403
- tests/test_m02_was_composition.py: 9855fa34dab466314462b9cf4dbe1220e05a521678481d72a5768134d912922f
- tests/test_m02_was_diagnostics.py: 2b15758936df7f95af9f40836f949bcca87ec86d24fbbff2cfadf10f45a4f903

Authorize committing and pushing these reviewed sources, the reviewed combined
proposal, D-076, this acceptance and necessary canonical synchronization. Permit
preparation and blind dual review of a separate bounded execution proposal.
No import, compilation, lint, test, candidate execution, retry, dependency
operation, network, listener, Freewallet integration, Person Server change,
Misty access, physical action, G28 or G29 is authorized. Runtime success remains
unverified. The unrelated PI routine-tool proposal is excluded and untouched.

## D-078 — Authorize create-only outer execution runner

Recorded prospectively on 2026-09-17 after the PI agreed to create the necessary
outer runner. Both blind request-047 reviews PASS the execution proposal at
SHA-256 5b45bf79ad7241e9ce7ab1ee4626811bf2aadd21456551c79633fb496230b102,
but identify its outer deadline/capture enforcement as an unresolved holdpoint.

Authorize creation only of tools/m02_was_composition_execution.py, and a proposal
addendum specifying that runner's invocation, attempt markers and limits. Both
eligible blind reviewers must inspect the complete runner and addendum before
commit or execution. No import, parse, compile, lint, test, runner execution,
WAS execution, retry, network, listener, dependency operation, Freewallet,
Misty access, physical action, G28 or G29. Existing source stays unchanged.

## D-079 — Accept outer runner and authorize one corrected execution

Recorded prospectively on 2026-09-17 after the PI authorized commit/push of the
reviewed runner/proposals, one bounded synthetic check and, only on success,
one diagnostic run, with no automatic retries. Both blind request-048 reviewers
PASS the complete runner/addendum and records; request-047 independently passed
the execution proposal. Final hashes verified against the actual files:
- runner: c8ab204f84c7c976a117eb28b2ef70cb806d3719199aae3b57c0f68a6171ae3a
- addendum: 2ba60853cad6380ea73983137cb60a8f27309b0ad7f90983e1b3a11bda5959e1
- execution proposal: 5b45bf79ad7241e9ce7ab1ee4626811bf2aadd21456551c79633fb496230b102

Authorize committing/pushing those exact artifacts, D-078, this prospective
decision and synchronized state. Record the resulting full EXECUTION_HEAD and
verify source/candidate/runtime inputs and pre-use controls before invocation.
Authorize only the proposal/addendum's single synthetic step and conditional
single diagnostic step under the reviewed limits and platform approval.
An occupied attempt reservation, failed check, missing control or changed input
stops the sequence. No retries or code changes. All three roots are retained
research evidence: diagnostics-20260916-001, diagnostics-20260917-001 and
outer-20260917-001 beneath /private/tmp/m02-stage3b-. The outer-group kill does
not prove descendant cleanup; independently inspect and report incomplete
cleanup rather than repair or retry. Evidence must receive blind dual review
before PI acceptance. Record exact argv; timings include bounded shutdown grace;
stream hashes on overflow describe retained prefixes. Invocation count23 is
static unless actually measured; identifier/holdpoint categories are not induced.
No network, listeners, dependencies/build, Docker, Freewallet, live Person Server
change, personal data, payment, Misty access, physical action, G28 or G29.

## D-080 — Accept corrected synthetic composition result and pause

Recorded on 2026-09-17 after the PI selected this passing round as the stopping
point and authorized commit/push. Both blind request-049 reviewers returned
independent, non-authoring PASS with no blockers on evidence SHA-256
bdd00f2b7eee1ff2a0eb622e89e17b46742da5f200b70c48a85748780d672db0.
Their final independence statements and evidence pins were verified.

Accept the single D-079 sequence at execution commit
742ed046af7f50052423862dba187998b18546a6: synthetic9/9, focused34/34,
zero failure/error/skip/truncation, successful execution/postflight and scoped
independent cleanup. Retained record SHA-256
a85b1e3d676e3fd72c882e5773df6057c44e993a0da8362d60ba2f0a08ff13a6,
6337bytes,0600; exact transcription in durable repository evidence verified.
Both one-time attempts are consumed. Prior negatives remain negative; causes
are not retroactively established. Runtime invocation telemetry is unavailable;
23 calls remains a static prediction. Listener comparison is scoped, not host-wide
proof; raw outer streams were hashed but not retained. These disclosed limits
do not prevent acceptance of this bounded result.

Claim: synthetic Person Server result evidence storage/readback through the
exact socket-free WAS filesystem backend under the tested contracts. Not live
Person Server/token integration, Freewallet presentation or AAuth conformance.
Authorize commit/push of the exact reviewed evidence, this acceptance and
synchronized state. Pause implementation here; no next-stage authority.
Retain old/new diagnostics, attempt markers and exact WAS environment unchanged
pending separate disposition; repository transcription preserves the finding
if temporary roots are lost. No retry, diagnosis, code change, dependency/build,
external/network service, listener, wallet integration, personal data, payment,
Misty access, physical action, G28 or G29. Excluded PI proposal untouched.

## D-081 — Authorize one durable WAS preservation copy

Recorded prospectively on 2026-09-17 after PI authorized one execution of the
reviewed preservation utility, without restoration, candidate execution or retry.
Both blind request-050 reviewers PASS the complete proposal and utility:
- proposal SHA-256 f1144310c9d81a56096b0f508769b1d40501a64bd14e5ec1e70cd2a00d64999d
- utility SHA-256 43f01413f655cb8cf681a1c2796cf83460744ec5776e8f9e4457bdfbdd3efa37
Their blind/non-authoring statements and final pins were verified.

Authorize only one preservation utility invocation under that exact plan with
platform approval: source /private/tmp/m02-stage3lib-20260910 to exclusive durable
bundle /Users/debb/dev/research-evidence/m02-was-20260917-001/environment.
Original remains untouched. Adopt this local durability control: expected to
survive normal reboot/shutdown/temp cleanup, not disk failure or user deletion.
Absent verification.json means unverified partial copy; retain it on failure.
Both blind gates must inspect post-copy evidence before acceptance. B-043 remains
open; copy is not an alternate runtime root. Any future restore to the hardcoded
path needs separate review and prospective authorization. No candidate execution,
network, dependencies/build, listener, Docker, wallet/PS integration, personal
data, payment, Misty access, G28/G29, automatic retry or unrelated PI change.

## D-082 — Accept durable preservation evidence and stop

Recorded on 2026-09-17 following PI's “proceed” after both blind request-051
reviewers returned independent non-authoring PASS with no blockers. Accept
evidence SHA-25664f10e9fbdd935d5007645b0ffe14a59b53249def72f74223ca3aed09ffd8fa2.
Both gates independently recomputed full source/copy logical inventories:
29235 entries, manifest SHA-256
ceef625d8b233b55d8f7494347c6273301603fb7c9a208d4ff31115496e83f0c;
same source/copy candidate commit/tree and expected298-file dist manifest.
One D-081 copy consumed, no retry; original remains untouched in place.

Accept /Users/debb/dev/research-evidence/m02-was-20260917-001/environment
as durable local preservation evidence only. Normal shutdown/temp cleanup is
covered by the selected location; disk failure, deletion and machine loss are
not covered. Full manifest stays in the bundle; utility and verification record
are transcribed in repository evidence. Content/type/mode equality does not
prove copied dependency executability or inode/timestamp/xattr identity.

Authorize commit/push of the exact reviewed preservation proposal/evidence,
D-081, this acceptance, necessary canonical state and B-043 status note.
Keep B-043 open pending separately authorized fixed-path restoration/verification
or explicit abandonment. Pause here. No restoration, candidate/test execution,
retry, source/dependency/build change, network, listener, wallet/PS integration,
Misty access, physical action, G28/G29 or unrelated PI proposal change.

## D-083 — Accept historical restoration and temporary-path degradation result

Recorded on 2026-09-20 after the PI read and formally accepted both reports and
the coordinator's conclusion. The reviewed utility ran once on 2026-09-18 and
verified exact logical restoration of all 29,235 manifest entries, candidate
commit/tree, and the 298-file `dist/` manifest. The durable backup remained
unchanged. Accept that execution as an historically verified positive result.

On 2026-09-20 AGy found the live `/private/tmp` tree missing five empty
directories; local Git no longer recognized it. Accept the current temporary
runtime as degraded and unusable for integration. Periodic macOS temporary-path
maintenance is the probable cause from timing and filesystem evidence, not a
directly observed deletion event. The durable backup remains intact.

Review basis is disclosed: AGy supplied the eligible independent evidence
review; Claude independently recomputed and corroborated all material facts but
is ineligible because it authored the proposal and utility. PI acceptance of
that basis is a package-specific deviation, not a change to D-064 or a claim of
two eligible gates. B-043 remains open. No repeat restoration, runtime-path
change, candidate execution, integration, commit/push, Misty access, G28 or G29
is authorized by this decision.

## D-084 — Accept AAuth `-11` conformance-gap analysis at `fcf656d`

Recorded on 2026-09-20 after two blind independent reviewers returned PASS for
`knowledge/research/M02_AAUTH_FCF656D_CONFORMANCE_GAP_2026-09-20.md` at exact
SHA-256 `048594716738b9192a5da7a81444a46636160eb5f0ba8dc7321e0d3254582bc6`.
The primary source is the detached AAuth editor's-copy checkout at commit
`fcf656de1926535f5bd6fc0538147ead6646e727`; the reviewed protocol file has
SHA-256 `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`.

Accept the report as the authoritative gap analysis for the next AAuth track.
It establishes that the current M02 Person Server is useful test scaffolding but
is not AAuth `-11` conformant: its HMAC JWTs, request signing, metadata, mission
handling and token endpoints do not implement the required asymmetric,
typed-token, HTTP-message-signature and mission-bound flow. Preserve the
existing accepted Stage 2 fixtures and evidence rather than rewriting them in
place.

The next permitted planning action is a prospective implementation proposal for
Steps 1–3 only: pin the source profile; add asymmetric typed-token/JWKS support
with strict algorithm and token-type checks; and add verified signed-agent
requests with truthful interim metadata. This decision does not authorize that
implementation, execution, dependency changes, network access, Steps 4–9,
Freewallet or WAS integration, QR participation, external services, Misty
access, physical action, G28 or G29. The unrelated PI routine-tool proposal
remains excluded and untouched.

## D-085 — Accept AAuth `-11` Steps 1–3 proposal and authorize Phase 0

Recorded prospectively on 2026-09-20. The PI accepts
`knowledge/proposals/M02_AAUTH_FCF656D_STEPS1_3_IMPLEMENTATION_PROPOSAL_2026-09-20.md`
at exact SHA-256
`f8b7f3d7ffd19e517e893304a2ef68bc8c1f7f8a407bbb5b7881ce9f11643f91`
after two blind independent reviewers returned PASS and disclosed non-authorship
and no cross-reading. Authorize commit and push of the exact reviewed proposal,
this prospective decision and synchronized canonical state.

Authorize Phase 0 only: create a dependency record and exact normative-
requirement matrix against AAuth editor's-copy commit
`fcf656de1926535f5bd6fc0538147ead6646e727`, including the HTTP-signature
`alg` and `keyid` parameter rules identified during review. Phase 0 artifacts
carry no selection, acquisition or implementation authority and must receive
both blind independent reviews before PI disposition.

No dependency acquisition or installation, implementation, import, compilation,
testing, listener, network access, Steps 4–9, wallet or WAS integration, QR
flow, Misty access, G28 or G29 is authorized. The unrelated PI routine-tool
proposal remains excluded and untouched.

## D-086 — Accept AAuth Phase 0 and authorize bounded dependency/reference research

Recorded on 2026-09-20 after two blind independent reviewers returned PASS for
the exact Phase 0 package:

- dependency record SHA-256
  `df78c6a267ba884dcb16b5ecc56b09ff3eed24ba9f4012db5302a5c66a28d3e9`;
- normative matrix SHA-256
  `2dc6a6e45e353113a56b4f318ca143f10024c5dbbb2332ac9087fe69dad0e003`.

Accept the package's bounded result: the normative baseline is established, an
Ed25519 provider is required and absent, but local evidence does not support an
exact dependency selection. Authorize commit and push of the exact reviewed
artifacts, this decision and synchronized canonical state.

Authorize a bounded read-only network research phase to identify and verify one
exact Ed25519 provider artifact and pin the authoritative companion specifications
required for Phase 1: RFC 9421, RFC 9530, RFC 9651, and the exact HTTP Signature
Keys draft referenced by AAuth `fcf656d`. Permit retrieval of documentation and
package metadata only. No dependency download or installation, source
implementation, import, compilation, testing, listener, wallet or WAS work,
Misty access, G28 or G29 is authorized. Any acquisition or Phase 1 activity
requires separate review and prospective PI authorization.

## D-087 — Accept AAuth dependency/reference selection and authorize proposal creation

Recorded on 2026-09-21 after AGy returned an independent PASS and Claude Gate 1
returned PASS on a focused recheck that closed its sole evidence blocker. Accept
`knowledge/research/M02_AAUTH_FCF656D_DEPENDENCY_AND_REFERENCE_SELECTION_2026-09-21.md`
at exact SHA-256
`dc6d1547dcc03fbac8acc3e38a6370a3406b6f11b3d7b07995bea33ec5cb105b`.
The accepted result selects one exact four-wheel Ed25519 dependency closure and
pins RFC 9421, RFC 9530, RFC 9651, and
`draft-hardt-httpbis-signature-key-09`. The `pycparser` wheel hash was resolved
by deterministic extraction from the directly retrieved version-specific PyPI
JSON; no distribution artifact was downloaded.

Authorize commit and push of the exact reviewed report, this decision, and
synchronized canonical state. Authorize creation only of a proposal for
acquiring the four exact hash-pinned wheels and extending the normative matrix
for Phase 1. No dependency download or installation, implementation, import,
compilation, testing, listener, wallet or WAS work, Misty access, G28 or G29 is
authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.

## D-088 — Accept AAuth Phase 1 acquisition/matrix proposal and authorize request creation

Recorded on 2026-09-21 after both blind independent reviewers returned PASS for
`knowledge/proposals/M02_AAUTH_FCF656D_PHASE1_ACQUISITION_AND_MATRIX_EXTENSION_PROPOSAL_2026-09-21.md`
at exact SHA-256
`26283f5e7e3346c7229fb7a241642f10e8a31f313cab542f32026b60dc3545e8`.
The corrected proposal durably pins the four wheel URLs, hashes and sizes;
separates incomplete-output cleanup from quarantine of complete hash-mismatched
evidence; requires explicit authority for normative-document retrieval; and
requires affirmative redirect evidence.

Authorize commit and push of the exact reviewed proposal, this decision, and
synchronized canonical state. Authorize creation only of separate bounded Phase
A acquisition and Phase B exact-source retrieval/matrix-extension requests.
The Phase A request must prohibit every redirect, including a same-host
redirect. No wheel or document download, installation, import, implementation,
compilation, testing, listener, wallet or WAS work, Misty access, G28 or G29 is
authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.

## D-089 — Accept AAuth Phase A/B requests and authorize controller creation

Recorded on 2026-09-21 after both blind independent reviewers returned PASS for
the corrected requests:

- Phase A exact-wheel acquisition request SHA-256
  `aeef181ac6b5b6e3082cd53f0be595b91a511e312b4e6544c3603638af7a6163`;
- Phase B normative-source and matrix request SHA-256
  `69cb034a20a7ea33afbdd971f098aac044465dab9c0b731911ed021793522424`.

Accept and authorize commit and push of the exact reviewed requests, this
decision, and synchronized canonical state. Authorize create-only implementation
of the Phase A wheel-acquisition controller and Phase B0 normative-source
retrieval controller under the reviewed controls. Both complete controllers
require blind dual review before commit or execution.

No network retrieval, download, installation, import, matrix edit, compilation,
testing, listener, wallet or WAS work, Misty access, G28 or G29 is authorized.
The unrelated PI routine-tool proposal remains excluded and untouched.

## D-090 — Accept AAuth retrieval controllers and authorize one execution each

Recorded prospectively on 2026-09-21 after both blind independent reviewers
returned PASS for the exact controllers:

- Phase A wheel-acquisition controller SHA-256
  `4105596b13aca01b467e7a8cb42dd79c118713d7fb152840f0c7c4e78ca8f427`;
- Phase B0 normative-source controller SHA-256
  `e47d48cfb90e8e621ed5a9e712157a06d940037b64cd68db33300d448b827034`.

Authorize commit and push of the exact reviewed controllers, this prospective
decision, and synchronized canonical state. After that commit, authorize one
execution of each exact committed controller: Phase A at
`/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels` and Phase B0 at
`/private/tmp/m02-aauth-fcf656d-phase-b0-20260921/sources`. Permit only the
exact HTTPS retrievals encoded in the controllers, with zero redirects, finite
limits, fail-closed cleanup, no retries, and complete evidence.

Both resulting evidence packages require blind dual review before acceptance or
use. No installation, import, matrix edit, implementation, compilation, testing,
listener, wallet or WAS work, Misty access, G28 or G29 is authorized. The
unrelated PI routine-tool proposal remains excluded and untouched.

## D-091 — Accept AAuth Phase A/B0 evidence and authorize Phase B1 creation

Recorded on 2026-09-21 after both blind independent reviewers returned PASS for
the corrected evidence reports:

- Phase A wheel-acquisition evidence SHA-256
  `37097bedd3364881a25739688d465294a7a267f9a5f7fc113cb356a8f8c6d836`;
- Phase B0 normative-source evidence SHA-256
  `c1a6c52f2731db6d4009dd6e696eb244f99cfba61ced77d30b9582b636aad6b3`.

Accept both one-shot executions as gated positive results. Accept these B0
document hashes as mandatory Phase B1 input pins:

- RFC 9421: `612655786bf4293bfc486e4177571467fbb3de6e6f0eea90cb74c346a34fdf3c`;
- RFC 9530: `544dbb7d9afceafa8c9931d9924ca6cff2b4807274166d7ed2483342ef2cdd6a`;
- RFC 9651: `fe27f2ec8819911afbe4bd11f6fcb947580da4c49e5423a1fff960e252ced26d`;
- Signature Keys `-09`:
  `b5e8602e217bbccd254b93419d0b54ec2b2a6cdce38351983624718029528a5d`.

Authorize commit and push of the exact reviewed evidence, this decision, and
synchronized canonical state. Authorize create-only implementation of the
separate Phase 1 normative-matrix extension from the preserved pinned documents.
Also authorize creation only of a bounded proposal for isolated installation
and verification of the four acquired wheels. Both artifacts require blind dual
review before acceptance or installation.

No installation, import, implementation, compilation, testing, listener, wallet
or WAS work, Misty access, G28 or G29 is authorized. The unrelated PI
routine-tool proposal remains excluded and untouched.

## D-092 — Accept AAuth Phase B1 matrix and installation proposal

Recorded on 2026-09-21 after both blind independent reviewers returned PASS for:

- Phase B1 normative-matrix extension SHA-256
  `ba6779c4ff2f01acfb35e87ff090f92297b65b204cf5c5b931e489749a49d3d4`;
- isolated wheel-installation proposal SHA-256
  `384c53ff69e9cfdbc108e57853b43704c084ad945b1330671cafd0c898da94b5`.

Accept both artifacts and authorize commit and push of their exact reviewed
bytes, this decision, and synchronized canonical state. Authorize create-only
implementation of the bounded installation controller. The controller must pin
and record the exact pip version and preserve the reviewed private-scratch
boundary. It requires blind dual review before commit or execution.

Any later provider verification must explicitly authorize execution of
`cryptography`'s bundled native code. No installation, import, native-code
execution, AAuth implementation, testing, listener, wallet or WAS work, Misty
access, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.

## D-093 — Accept isolated installation controller and authorize one execution

Recorded prospectively on 2026-09-21 after both blind independent reviewers
returned PASS for
`tools/m02_aauth_fcf656d/install_verified_wheels.py` at exact SHA-256
`84f4594b25a68f4560eeb575b7977cbfc7047331daddf9006ea578a2acd34b13`.

Authorize commit and push of the exact reviewed controller, this decision, and
synchronized canonical state. Then authorize one execution under the D-092
proposal with no automatic retry. Require standalone evidence and blind dual
review before any import or use.

No provider import, bundled native-code execution, AAuth implementation,
testing, listener, wallet or WAS work, Misty access, G28 or G29 is authorized.
The unrelated PI routine-tool proposal remains excluded and untouched.

## D-094 — Accept isolated installation negative result and authorize recovery proposal

Recorded on 2026-09-21 after both blind independent reviewers returned PASS for
`knowledge/research/M02_AAUTH_FCF656D_ISOLATED_INSTALLATION_EVIDENCE_2026-09-21.md`
at exact SHA-256
`dc19a3cf34a583be625f1ed33d3b506b780986cee4a5b65cf613f1088ff781d3`.

Accept the D-093 attempt as a gated negative result at the reviewed empty-scratch
holdpoint. pip reported successful local installation of the four exact wheels,
but the controller stopped before post-install source, RECORD, distribution-set
and installed-tree verification because private scratch contained `xcrun_db`.
The attempt is consumed and the preserved target remains unaccepted and unusable.

Authorize commit and push of the exact reviewed evidence report, this decision,
and synchronized canonical state. Authorize creation only of a recovery proposal
for static verification of the preserved installed tree without rerunning pip,
importing a provider, executing bundled native code, deleting `xcrun_db`, or
modifying preserved state. Require blind dual review before any recovery verifier
is created or executed.

No retry, cleanup, import, implementation, testing, listener, wallet or WAS work,
Misty access, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.

## D-095 — Record standing AAuth, Freewallet, WAS-authorization and next-priority determinations

Recorded on 2026-09-21 at PI instruction, at `main @ cc78065`. This decision
records four determinations the PI stated directly. It is a record of standing
basis and priority, not an acceptance of any package and not an authorization to
build, execute or integrate anything.

1. **AAuth basis.** The governing AAuth source remains `-11` at the editor's-copy
   commit `fcf656de1926535f5bd6fc0538147ead6646e727`, protocol SHA-256
   `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`. This was
   already established by D-084 and D-085 and is restated here as standing basis,
   not newly decided. Published `-10` and the separate R3 editor draft must not be
   conflated with it.

2. **Freewallet pin.** The governing Freewallet pin for M02 wallet work is
   `8e806c049b1134e36e72ab243ea3fbeb93153c37`, release line `0.42.0`, origin
   `https://github.com/interop-alliance/freewallet.git`, as authorized for
   detached checkout by D-038 and recorded in
   `knowledge/research/M02_STAGE3A_EXACT_SOURCE_RUNTIME_EVIDENCE_2026-09-08.md:23`.
   The in-tree working copy at `external-repos/freewallet` is a different and
   older revision: `403bc554d35f92c2279cf4d7e59b8d676416431b`, `package.json`
   version `0.38.0`, last commit 2026-08-14. That copy is prior evidence only. It
   is superseded by the pin and must not be used as the wallet input for any M02
   composition, conformance or integration claim. D-038 authorized detached
   checkouts at the pin and did not update the in-tree copy, so the divergence is
   expected and must not be silently reconciled by updating either one.
   `knowledge/research/M02_STAGE1_WALLET_PERSON_SERVER_CONFORMANCE_REFRESH_2026-09-06.md:57`
   records that Freewallet changed substantially between the two revisions.

3. **ZCAP on the socket-free WAS library path.** The socket-free WAS library
   composition does not perform zCap authorization when storing or reading Person
   Server evidence. The governing disclosure is
   `knowledge/proposals/M02_STAGE3B_PERSON_SERVER_WAS_COMPOSITION_PROPOSAL_2026-09-15.md:62-67`:
   the worker does not use `createApp`, Fastify routes, onboarding tokens, zCaps,
   HTTP or a listener, and direct storage-backend use "deliberately bypasses the
   candidate's route-level DID and identifier validation, onboarding and zCap
   authorization, and request hooks". Authorization in the selected WAS source
   lives at the Fastify route layer, not in the storage backend, so composing the
   backend as a local library removes it. Consequently every accepted socket-free
   result proves storage-backend composition only, never WAS protocol
   authorization or route behavior.

   The earlier Stage 3lib harness is a distinct and narrower case that must not be
   cited as the bypass disclosure. `tools/m02_stage3lib/harness.mjs:255`, echoed in
   `knowledge/research/M02_STAGE3LIB_PHASE2_EXECUTION_EVIDENCE_2026-09-14.md:94,107-108`,
   records that resource creation and precondition scope were *skipped* because
   "no resource exists; creating one requires zcap verification not supplied by
   this phase". That harness declined to perform the zCap-requiring operation
   rather than going around it. Both facts are now recorded here because no prior
   decision in this log mentioned zCap at all.

4. **Next build priority.** The next build priority is the AAuth `-11` token
   exchange exercised against a simulated Misty. No such simulator exists in the
   repository, and nothing about it has been proposed, reviewed or authorized. It
   requires a prospective proposal, blind dual independent review under D-064 and
   explicit PI authorization before any source is created or run. Recording the
   priority does not schedule, authorize or pre-approve it, and does not displace
   the open D-094 static recovery track.

This decision authorizes no implementation, execution, import, native-code
execution, compilation, test, listener, dependency or package operation, network
access, restoration, commit beyond this record and synchronized canonical state,
Freewallet or WAS integration, wallet custody, personal data, payment, physical
actuation, G28 or G29. It authorizes no Misty access: a simulated Misty is a
software target only, and Beryl router placement remains a hard prerequisite
before any physical Misty access is even proposable. The unrelated PI
routine-tool proposal remains excluded and untouched.

Authorship disclosure: this entry was drafted by Claude Gate 1 at the PI's direct
instruction rather than by the integrator. Under D-064, Gate 1 is therefore
disqualified from serving as an independent reviewer of this entry, and any
review of it must come from two other eligible non-authoring reviewers.

## D-096 — Record consumed static-verifier execution and authorize no-execution recovery proposal

Recorded on 2026-09-21 at PI instruction after both blind request-031 reviewers
passed review of the preserved raw artifacts.

Accept the single static-verifier execution as a consumed gated negative. The
child verifier exited zero and emitted a positive static-verification document,
and both reviewers independently corroborated its static findings. The runner
correctly returned `FAILED` because it observed 110 stderr bytes. Those bytes
were not preserved, so their origin cannot be diagnosed from the evidence and
the installation remains unaccepted.

Authorize creation only of a durable evidence report and a no-execution recovery
proposal based on blind dual independent recomputation of the preserved bytes.
Every future runner with an stderr holdpoint must preserve bounded raw stderr
content before evaluating success.

No retry, provider import, native-code execution, pip operation, AAuth
implementation, listener, network access, wallet or WAS work, Misty access, G28
or G29 is authorized. The unrelated PI routine-tool proposal remains excluded
and untouched.

## D-097 — Accept preserved installation static properties by independent recomputation

Recorded on 2026-09-21 at PI instruction, at
`main @ 0800e450386a7315e6048cea45165d7cbd72aca0`, after both eligible blind
reviewers independently recomputed the preserved D-093 bytes and returned PASS.
The material this acceptance rests on is committed at that hash; this decision
is the acceptance itself and takes effect on commit.

Accept that the preserved installation has the pinned distribution identity,
filesystem containment and RECORD completeness required to proceed to a
separately proposed provider-behavior verification. The consumed static-verifier
execution remains a gated negative and its 110 unpreserved stderr bytes remain
unexplained. This acceptance does not turn that execution positive.

No provider import, native-code execution, retry, pip operation, AAuth
implementation, listener, network access, wallet or WAS work, Misty access, G28
or G29 is authorized. Any provider-behavior proposal must receive blind dual
review and any later execution must receive separate prospective PI authority.
The unrelated PI routine-tool proposal remains excluded and untouched.

## D-098 — Record provider run negative and authorize exact-diagnostic R2

Recorded on 2026-09-21 at PI instruction after both blind request-039 reviewers
passed diagnosis of the preserved first-run evidence.

The first provider execution at `a5e17aa` is consumed and remains a gated
negative because the outer runner correctly rejected 110 nonempty stderr bytes.
The child exited zero and produced an RFC 8032 Test 1 positive result, but that
cryptographic finding remains unaccepted pending a clean outer-gate result.

Authorize the narrow R2 runner correction and one committed execution described
in `knowledge/proposals/M02_AAUTH_FCF656D_ED25519_PROVIDER_R2_PROPOSAL_2026-09-21.md`.
Only empty stderr or exactly 110 bytes with SHA-256
`2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`
may pass; raw stderr must still be preserved and any superset or other content
must fail. The precise intermittent host trigger is not claimed.

No retry, network access, dependency operation, AAuth conformance claim,
listener, wallet/WAS work, Misty access, G28 or G29 is authorized. Resulting
evidence requires blind dual review before acceptance. The unrelated PI
routine-tool proposal remains excluded and untouched.

## D-099 — Accept bounded Ed25519 provider behavior

Recorded on 2026-09-21 at PI instruction after both blind request-040 reviewers
returned PASS on the exact R2 evidence.

Accept the request-040 evidence as establishing bounded deterministic Ed25519
provider behavior for the pinned installation. RFC 8032 Section 7.1 Test 1
reproduced byte-for-byte, all specified negative cases passed, and two separate
executions produced byte-identical provider evidence at SHA-256
`d6c7564e55e81fbc11931fb0306b9ce4c210f968fce587cc1f6919ebaba505fe`.

This establishes provider behavior only, not AAuth conformance, JWT or HTTP
Message Signature correctness, general native-code safety, or behavior beyond
the encoded tests. The first execution remains a consumed gated negative. The
110-byte Darwin diagnostic is accepted only as the exact pinned value.

The corrected R2 runner at SHA-256
`4158eae860fa492048267803faa94f68d185cc8a967b369b0dde8a0aa2ce947a`
was committed and executed under D-098 before prospective blind dual static
review. Both gates reviewed the exact runner and evidence retrospectively in
request 040 and returned PASS. This was a PI-authorized, package-specific
deviation and creates no precedent; future executions return to prospective
review of the exact instrument.

The durable evidence record is
`knowledge/research/M02_AAUTH_FCF656D_ED25519_PROVIDER_R2_EVIDENCE_2026-09-21.md`.
No additional execution, dependency operation, AAuth implementation, network
access, wallet/WAS work, Misty access, G28 or G29 is authorized. The unrelated
PI routine-tool proposal remains excluded and untouched.

## D-100 — Authorize AAuth Steps 1–3 Phase 1 create-only implementation

Recorded on 2026-09-21 at PI instruction after both blind request-042 reviewers
returned PASS.

Accept
`knowledge/proposals/M02_AAUTH_FCF656D_PHASE1_CREATE_ONLY_PROPOSAL_2026-09-21.md`
at SHA-256
`47f54e4cff5cc8ecfce46209a949194b522a63ef503994685ada0f1b09b4dbe4`.
Authorize creation only of the seven source and test files named there, under
its exact provider, normative, preservation, stop-rule and claim boundaries.

Do not import, compile, lint, test or execute the created code. Both blind gates
must review every complete file before commit or execution. No Step 4–9 work,
dependency operation, listener, network access, wallet/WAS integration, QR
flow, Misty access, physical actuation, G28 or G29 is authorized. The unrelated
PI routine-tool proposal remains excluded and untouched.

## D-101 — Authorize create-only Ed25519 provider API extension

Recorded on 2026-09-22 at PI instruction after both blind request-048 reviewers
returned PASS.

Accept
`knowledge/proposals/M02_AAUTH_FCF656D_PUBLIC_KEY_IMPORT_EXTENSION_PROPOSAL_2026-09-21.md`
at SHA-256
`b9916cd068db3e139f616664bcdfff43762613331a2e939dbced8e604ef1ac6a`.
Authorize creation only of the specified child and runner covering bounded
`Ed25519PublicKey.from_public_bytes` and `Ed25519PrivateKey.generate()` provider
behavior. Generated key or signature bytes and their hashes must not enter
evidence.

Do not import, compile, lint, test or execute either source. Both blind gates
must review the complete files before commit or execution. No AAuth Phase 1
execution, dependency operation, network access, listener, wallet/WAS work,
Misty access, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.

## D-102 — Accept bounded Ed25519 provider extension evidence

Recorded on 2026-09-22 at PI instruction after both blind request-050 reviewers
returned PASS with no blocking findings.

Accept the single provider-extension execution as a gated positive result. The
accepted evidence hashes are:

- provider evidence:
  `8b4676330643dea6db04c23027bf0e002ca752514a409337712f6ad416a5da8c`;
- exact 110-byte stderr:
  `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`;
- run record:
  `c83fbe9b632f32445f17720fe2aa77131068bb926fd4f1ec72bd5b3b2525714b`.

The pinned provider successfully exercised
`Ed25519PublicKey.from_public_bytes` and `Ed25519PrivateKey.generate()` under
the encoded positive and negative cases without recording generated key or
signature material. The durable record is
`knowledge/research/M02_AAUTH_FCF656D_PROVIDER_EXTENSION_EVIDENCE_2026-09-22.md`.

This establishes provider behavior only, not AAuth, JOSE, JWT, HTTP Message
Signature, Structured Fields or randomness conformance. It closes the provider
holdpoints for a separately authorized AAuth Phase 1 test execution. It does not
authorize that execution or any additional execution, dependency operation,
network access, listener, wallet/WAS work, Misty access, G28 or G29. The
unrelated PI routine-tool proposal remains excluded and untouched.

## D-103 — Authorize create-only AAuth Phase 1 test controller

Recorded on 2026-09-24 at PI instruction after both blind request-052 reviewers
returned PASS with no blocking findings.

Accept
`knowledge/proposals/M02_AAUTH_FCF656D_PHASE1_TEST_EXECUTION_PROPOSAL_2026-09-22.md`
at SHA-256
`588f42d098f6b45088bd14251773bbe800d3c51dc68265120fff448c4a39731e`.
Authorize creation only of
`tools/m02_aauth_fcf656d/run_phase1_tests.py` under the proposal's exact
controls. The complete controller requires blind dual static review before
commit or execution.

Do not import, compile, lint, test or execute the controller or AAuth package.
No execution, dependency operation, network access, listener, wallet/WAS work,
QR flow, Misty access, physical actuation, G28 or G29 is authorized. The
unrelated PI routine-tool proposal remains excluded and untouched.

## D-104 — Authorize one bounded AAuth Phase 1 test execution

Recorded on 2026-09-24 at PI instruction after both blind request-054 reviewers
returned PASS with no blocking findings.

Accept `tools/m02_aauth_fcf656d/run_phase1_tests.py` at SHA-256
`177b4f1231fb30ca053308a4dbfb726c05cdc5b917d6ed614a83c1c817ac4303`.
Authorize commit and push of that exact controller, followed by exactly one
bounded execution under the accepted proposal and D-103 controls. No automatic
retry is permitted. The resulting evidence requires blind dual review before
acceptance or further use.

This authorizes only the claim-sized Phase 1 focused test execution. It does not
authorize source correction, a second execution, dependency operation, network
access, listener, the October token exchange, wallet/WAS work, QR flow, Misty
access, physical actuation, G28 or G29. The unrelated PI routine-tool proposal
remains excluded and untouched.

## D-105 — Accept Phase 1 focused-test negative and authorize source-only diagnosis

Recorded on 2026-09-24 at PI instruction after both blind request-055 reviewers
returned PASS on the evidence.

Accept the single D-104 execution as a gated negative. The accepted evidence
hashes are:

- focused-test evidence:
  `3f00c0037f528d0f33cbed1faec55e10a97fc8778e7242218d6ffcaf1010c9e7`;
- exact 110-byte stderr:
  `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`;
- run record:
  `57b7695589d059aaf796b0ba03a3d438d0e2408c206e15e3d8111042243f8724`.

Twenty-three of 24 tests passed. The deterministic failure was
`test_created_window_skew_and_replay`: no `SignatureProfileError` was raised for
`created=106`, `now=100`. The D-104 attempt is consumed. The durable record is
`knowledge/research/M02_AAUTH_FCF656D_PHASE1_TEST_EXECUTION_EVIDENCE_2026-09-24.md`.

Authorize bounded source-only diagnosis of that failure. No source
modification, import, compilation, lint, test, execution, retry, dependency
operation, network access, listener, October-exchange implementation,
wallet/WAS work, QR flow, Misty access, physical actuation, G28 or G29 is
authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.

## D-106 — Accept clock-skew diagnosis and authorize create-only recovery

Recorded on 2026-09-24 at PI instruction after Gate 1 passed the corrected
proposal in request 057 and Gate 2 passed the original and corrected proposal
in requests 056 and 057.

Accept the source-only diagnosis at SHA-256
`d4d526c234552ff5192751020486bad07404a3551d495cbf763672fae5533876`
and the correction-and-rerun proposal at SHA-256
`a4ccfa01da383f4e503fe1f791b93b5f0fcf169e8c8ddf5abdcc84ca126acbda`.
The diagnosis establishes that `created=106`, `now=100` is inside the pinned
60-second forward-skew window; the test fixture, not the implementation, is
defective.

Authorize commit and push of those exact artifacts, followed by create-only
implementation of the exact test correction and the two permitted mechanical
controller changes: the corrected test SHA-256 pin and the new fixed evidence
directory. Both complete corrected files require blind dual static review
before commit or execution.

Do not execute tests. No implementation-source change, dependency operation,
network access, listener, October-exchange implementation, wallet/WAS work, QR
flow, Misty access, physical actuation, G28 or G29 is authorized. The unrelated
PI routine-tool proposal remains excluded and untouched.

## D-107 — Authorize one corrected Phase 1 focused-test execution

Recorded on 2026-09-24 at PI instruction after both blind request-058 reviewers
returned PASS with no blocking findings.

Accept the corrected clock-skew test at SHA-256
`89b71359c6c071453fab289aa85443aa4f7156e4a2d263d8ac12f85bee4deaad`
and the mechanically corrected controller at SHA-256
`1d38794aa2e75e7a6889bd1465f2b24c2824e2236df77c049b1f9939bd50136a`.
Authorize commit and push of those exact files, followed by exactly one bounded
execution under the accepted D-106 recovery proposal. No automatic retry is
permitted. The resulting evidence requires blind dual review before acceptance
or further use.

No additional source change, dependency operation, network access, listener,
October-exchange implementation, wallet/WAS work, QR flow, Misty access,
physical actuation, G28 or G29 is authorized. The unrelated PI routine-tool
proposal remains excluded and untouched.

## D-108 — Accept corrected Phase 1 focused-test positive evidence

Recorded on 2026-09-24 at PI instruction after both blind request-059 reviewers
returned PASS with no blocking findings.

Accept the single D-107 execution as a gated positive result. The accepted
evidence hashes are:

- focused-test evidence:
  `0b95d4f7d80607e36e00a557be707fcba71a6036a2df50ef7a0d78fd6da7bbf3`;
- empty stderr:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- run record:
  `5108b8390b55f1c46632b31b022352f8d29f07d614cbc16562fc33f873a38bd8`.

All 24 focused tests passed with zero failures, errors, skips, mutation,
confinement escape or evidence leakage, including the corrected 60/61-second
forward clock-skew boundary. The durable record is
`knowledge/research/M02_AAUTH_FCF656D_PHASE1_CORRECTED_TEST_EXECUTION_EVIDENCE_2026-09-24.md`.

This establishes the bounded Phase 1 test claims only, not complete AAuth
conformance or a live token exchange. No additional execution, dependency
operation, network access, listener, October-exchange implementation,
wallet/WAS work, QR flow, Misty access, physical actuation, G28 or G29 is
authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.

## D-109 — Authorize create-only minimal live AAuth exchange package

Recorded on 2026-09-24 at PI instruction after both blind request-061 reviewers
returned PASS with no blocking findings.

Accept
`knowledge/proposals/M02_AAUTH_FCF656D_MINIMAL_LIVE_EXCHANGE_PROPOSAL_2026-09-24.md`
at SHA-256
`e7e5b45c5acb6589ec624fe63866a45c20e5eddefd5326c498ee748e04ccb075`.
Authorize commit and push of that exact proposal, followed by create-only
implementation of the complete identifiers, tokens, exchange, metadata
extension and exchange-test package under its exact boundaries. Every complete
created or modified file requires blind dual static review before commit or
execution.

Do not import, compile, lint, test or execute the created code. No dependency
operation, network access, listener, external service, personal data, payment,
wallet/WAS work, QR flow, Misty access, physical actuation, G28 or G29 is
authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.

## D-110 — Accept minimal live AAuth exchange static package

Recorded on 2026-09-24 at PI instruction to submit the reviewed static package
without execution, after both blind request-063 reviewers returned PASS with no
blocking findings.

Accept the complete static package at these SHA-256 values:

- `m02_aauth_fcf656d/identifiers.py`:
  `54c495785fc5fc26d24e3c406bb334d0022410faff37696d40220e1b83759579`;
- `m02_aauth_fcf656d/tokens.py`:
  `34f705123acb83772f9f2428409593233f004384c46b2cf96f0358615cf2dd04`;
- `m02_aauth_fcf656d/exchange.py`:
  `ed82a97873f7c535917dd0ecbecf81e31287015c3dfbc77396cb3dc8675fdf0f`;
- `m02_aauth_fcf656d/metadata.py`:
  `c1a473ee3f21ed4832668fadb87e9db72dbade4278f99aa35efff868db225a5a`;
- `tests/test_m02_aauth_fcf656d_exchange.py`:
  `89dcede33566a1531d9c5630d9598da940ffd7ac99dfb4610a875e3559aad916`.

Authorize commit and push of those exact files and synchronized canonical
state. Do not create an execution controller and do not import, compile, lint,
test or execute the package. Any controller creation or execution requires a
new prospective PI decision after the PI returns.

No dependency operation, network access, listener, external service, personal
data, payment, wallet/WAS work, QR flow, Misty access, physical actuation, G28
or G29 is authorized. The unrelated PI routine-tool proposal remains excluded
and untouched.

## D-111 — Authorize create-only minimal live-exchange execution controller

Recorded on 2026-09-24 at PI instruction.

Authorize creation only of a bounded execution controller for the D-110 minimal
live AAuth exchange package at commit `3195161`. The controller must run only
the exact committed Phase 1 and exchange test modules under the pinned provider,
with finite time and output limits, exact source hashes, module-origin
confinement, secret redaction, pre/post immutability checks, a new fixed evidence
directory and no network or listener. The complete controller requires blind
dual static review before commit or execution.

Do not import, compile, lint, test or execute the controller or package. No
dependency operation, external service, personal data, payment, wallet/WAS
work, QR flow, Misty access, physical actuation, G28 or G29 is authorized. The
unrelated PI routine-tool proposal remains excluded and untouched.

## D-112 — Accept live-exchange controller and authorize one bounded execution

Recorded on 2026-09-24 at PI instruction after both blind request-065 reviewers
returned PASS with no blocking findings.

Accept `tools/m02_aauth_fcf656d/run_live_exchange_tests.py` at SHA-256
`059ea6fc0e420674c8383211b05957ae2b04d6492abb00c9a1d3140d372ce289`.
Authorize commit and push of that exact controller, followed by exactly one
bounded execution under the D-111 controls. No automatic retry is authorized.
The resulting evidence requires blind dual review before acceptance or further
use.

No additional execution, dependency operation, network access, listener,
external service, personal data, payment, wallet/WAS work, QR flow, Misty
access, physical actuation, G28 or G29 is authorized. The unrelated PI
routine-tool proposal remains excluded and untouched.

## D-113 — Accept minimal live AAuth exchange positive evidence

Recorded on 2026-09-24 at PI instruction after both blind request-066 reviewers
returned PASS with no blocking findings.

Accept the single D-112 execution as a gated positive result. The accepted
evidence hashes are:

- live-exchange evidence:
  `e0cf8734703625e1c5e49abbf273886b5fd8a2c64395950fdea83042910c47ec`;
- permitted 110-byte stderr:
  `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`;
- run record:
  `cc0782708dcf409f2be932d6f72e2238d6348d5c4b118216491704f67f6c7dbb`.

All 35 tests passed with zero failures, errors, skips, timeout, overflow,
mutation or confinement escape. The durable record is
`knowledge/research/M02_AAUTH_FCF656D_MINIMAL_LIVE_EXCHANGE_EXECUTION_EVIDENCE_2026-09-24.md`.

This establishes the bounded transport-free minimal AAuth exchange only, not
complete AAuth conformance or live wallet, network, WAS, QR or Misty
integration. No additional execution or other excluded activity is authorized.
The unrelated PI routine-tool proposal remains excluded and untouched.

## D-114 — Authorize create-only localhost AAuth transport and gateway package

Recorded on 2026-09-24 at PI instruction after both blind request-068 reviewers
returned PASS with no blocking findings.

Accept
`knowledge/proposals/M02_AAUTH_FCF656D_LOCALHOST_GATEWAY_PROPOSAL_2026-09-24.md`
at SHA-256
`804786a3f89a723f06e10962a66ec3f8728819f8c6e3ee1eb53163127fda50b1`.
Authorize commit and push of that exact proposal, followed by create-only
implementation of its complete localhost transport, SOGA supervision adapter
and test package. Every complete created or modified file requires blind dual
static review before commit or execution.

Do not import, compile, lint, test, bind a listener or execute the created code.
No dependency operation, external service, personal data, wallet/WAS work, QR
flow, Misty access, physical actuation, G28 or G29 is authorized. The unrelated
PI routine-tool proposal remains excluded and untouched.

## D-115 — Accept localhost transport-address amendment

Recorded on 2026-09-24 at PI instruction after both blind request-071 reviewers
returned PASS with no blocking findings.

Accept
`knowledge/proposals/M02_AAUTH_FCF656D_LOCALHOST_TRANSPORT_ADDRESS_AMENDMENT_2026-09-24.md`
at SHA-256
`b47eee5c57836c1140d275602c2df6c8fecfe6511a92a3023726314b93cd5611`.
Authorize commit and push of that exact amendment, then continue the D-114
create-only implementation under the proposal as amended. Preserve every
accepted D-113 source file unchanged. The conformant HTTPS role identifiers
remain security identities; injected literal-loopback addresses are test-only
socket routing and do not establish discovery.

Do not import, compile, lint, test, bind a listener or execute the created code.
Every complete created file requires blind dual static review before commit or
execution. All D-114 exclusions remain in force. The unrelated PI routine-tool
proposal remains excluded and untouched.
