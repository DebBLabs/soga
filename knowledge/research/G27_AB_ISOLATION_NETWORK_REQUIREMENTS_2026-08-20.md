# G27 Misty A / Misty B Isolation and Network Requirements

Date: 2026-08-20

Status: ADOPTED — G27 requirements; not implementation authorization,
robot-connection authorization, or evidence of physical behavior

Gate/task: G27 — Embodied Capability and Physical Safety Model

## 1. Scope and evidence discipline

This artifact defines the testable isolation property required by the G27
roadmap and the placement/partition rules required before either Misty is
powered or connected. It applies the session-grant contract committed at
`dc50ea2` and the PI-approved policy dispositions in D-023. It does not select a
deployment product, assign final component ownership, or assert that either
robot currently implements these requirements.

Evidence labels:

- **REPOSITORY EVIDENCE** — an existing committed artifact or executable shape;
- **G27 REQUIREMENT** — an adopted conceptual property that implementation
  must satisfy;
- **G28 VALIDATION** — a property requiring implementation or physical
  measurement after G27 entry criteria are satisfied;
- **UNRESOLVED INSTANTIATION** — a value or component choice that may remain
  open without weakening the required property.

Repository evidence establishes:

- Misty B is the higher-capability embodied research platform and Misty A is
  the stable lower-capability comparative control (D-006).
- G28 entry requires a G27 A/B state-isolation specification, interruption
  semantics, and network-partition behavior
  (`knowledge/strategy/SPRINT_ROADMAP_G0_G30.md`).
- The G26 permission path terminates at the permission boundary and does not
  prove external action execution (`knowledge/working/CURRENT_STATE.md`).
- The capability registry is descriptive and does not itself select or invoke
  implementations (`engines/capability_registry.py`).
- `SimplePEP` maps a decision to an execution status but does not actuate or
  prove physical completion (`execution/simple_pep.py`).
- Repository Misty HTTP calls and sanity checks establish code paths only, not
  retained physical-run evidence (`tools/sanity_check.sh`;
  `verify/verify_server.py`).

### Prior demonstration routing: reusable seam, not an isolation design

The earlier demonstration provides a narrow implementation clue. Its Misty
route takes one configured `MISTY` base URL, checks `/skills/running`, and can
dispatch `/tts/speak` (`tools/sanity_check.sh`). `verify/verify_server.py:17`
likewise contains a direct Misty HTTP-dispatch shape and a hardcoded IP fallback
when `MISTY` is unset. This establishes a natural interception seam immediately
before an external request is emitted and a basic health-check/REST adapter
pattern that may be reused; the hardcoded fallback is specifically prohibited
from carrying forward.

It does **not** establish an A/B router, canonical platform binding, separate
credentials or state, target allowlisting, partition behavior, execution
completion, or mid-actuation interruption. A single configured base URL is
therefore historical **REPOSITORY EVIDENCE**, not evidence that the G27 routing
requirements are already satisfied. Reuse is permitted only behind the
target-bound PEP/adapter boundary and only after the connection-gate evidence
in section 9 exists.

## 2. Isolation subject and boundary

For G27, Misty A and Misty B are distinct execution subjects and distinct
physical enforcement surfaces. Sharing a mission class, semantic-action name,
governance policy, codebase, gateway host, or service implementation does not
permit their mutable runtime state or authority artifacts to be
interchangeable.

The isolation boundary covers:

- robot/platform identity;
- agent and execution-surface identity;
- participation credential and phone/channel binding;
- live and terminal session state;
- subject/current state and observations;
- authority and policy evidence;
- permission requests and governance decisions;
- capability resolution and physical-command targeting;
- local safety state;
- execution status and receipts; and
- audit correlation and queued delivery.

No initial Tip Jar state transfer between Misty A and Misty B is authorized.
A later governed transfer would require an explicit semantic action, authority,
policy, provenance, and receiving-subject validation; it cannot arise from
shared storage or process memory.

## 3. Testable A/B isolation property

**G27 REQUIREMENT — A/B non-interference:**

> For any valid or invalid input addressed to Misty A, the authoritative
> mission/session/permission/execution state and physical command surface of
> Misty B remain unchanged, and vice versa, unless a separately authorized and
> target-bound cross-platform action exists. No such cross-platform action is
> authorized for the first Tip Jar mission.

The property is satisfied only if all invariants below hold.

### I-1 — Canonical target identity

Every mutable runtime artifact names one canonical `platform_id` and one
execution-surface/agent identifier. Misty A and Misty B identifiers are unique,
stable for the test, and never inferred from network address, display name,
discovery order, or “the available robot.” Canonical values remain an
**UNRESOLVED INSTANTIATION** until adopted before execution.

### I-2 — Credential and channel binding

A participation credential binds to the intended platform/session service,
mission `s256`, notice/policy version, and ephemeral channel binding. A
credential issued for A cannot initiate B, and vice versa. Validation occurs
before atomic consumption; a wrong-target attempt does not consume a valid
credential for its correct target.

### I-3 — Session namespace and source of truth

Session identifiers are globally unambiguous or namespaced by `platform_id`.
Authoritative state admits no split-brain writer. A session created for A cannot
be resolved, mutated, terminated, or revived through B's endpoint or state
partition. Shared physical storage is permitted only if access control,
transaction boundaries, keys, queries, and tests preserve this logical
separation.

### I-4 — Evidence and current-state isolation

Observation, subject/current state, participant selection, authority evidence,
tip event, withdrawal, timeout, fault, and safety state bind to exactly one
platform and session. Missing binding fails closed. Evidence from A cannot
satisfy B's policy merely because the action, participant channel, or mission
class is similar.

### I-5 — Decision-package target binding

Every permission request and canonical decision package binds the exact
platform, agent/execution surface, session, semantic action, mission `s256`,
policy version, freshness context, and request/decision reference. A PEP rejects
a decision addressed to another platform, another session, an expired context,
or an unresolved target. `ALLOW` is not portable between A and B.

### I-6 — Capability-resolution isolation

Semantic actions resolve against the named platform's versioned capability
profile. A primitive available on B is not assumed available on A; absence on A
does not cause fallback to B. Registry metadata may be shared, but availability,
health, limits, safety state, adapter selection, and invocation are evaluated
for the bound platform at execution time.

### I-7 — Command-routing isolation

The PEP/adapter uses an explicit allowlisted target binding established before
execution. It does not use broadcast, opportunistic discovery, “first robot,”
last-connected device, mutable global base URL, or silent fallback. A command
for A cannot be emitted to B even when A is unreachable.

The historical single-`MISTY` route may inform an adapter implementation, but
the participant or request cannot supply or mutate that base URL. The final
adapter must derive its endpoint from the adopted `platform_id` binding and
recheck that binding before dispatch.

### I-8 — Safety-state independence

Each platform has an independent local actuation inhibit/safety halt and local
safety state. Failure, reset, partition, or halt of A cannot clear, satisfy, or
mutate B's safety state. A separately accessible all-stop may inhibit both, but
release remains per-platform and cannot be inferred from releasing the other.

### I-9 — Execution and audit attribution

`STARTED`, `COMPLETED`, `INTERRUPTED`, and `FAILED` evidence names the exact
platform, adapter, semantic action, physical primitive/composition, session,
decision, timestamps, and receipt source. A dispatch acknowledgment is not a
completion receipt. Missing or ambiguous platform attribution prohibits a
physical-execution claim.

### I-10 — Failure containment

Malformed input, replay, excessive requests, stale decisions, component crash,
network loss, queue backlog, or storage failure in A's path does not mutate B's
session, permission, execution, safety, or receipt state. Resource exhaustion
must be bounded so one platform/session cannot starve the other's safety or
termination path.

## 4. Required placement by function

Placement is expressed by required failure behavior, not by a selected vendor
or process topology.

### Must remain local to each physical enforcement boundary

The following functions must operate without the remote Person Server,
governance service, external audit sink, participant phone, or the other Misty:

- physical emergency/safety halt and actuation inhibit;
- target-identity enforcement at the final adapter;
- rejection of absent, stale, wrong-platform, wrong-session, or already-used
  execution authorization;
- prevention of conflicting concurrent physical commands;
- interruption at the earliest locally safe boundary;
- transition to or maintenance of the locally defined neutral/safe state; and
- recording of a local execution/interruption receipt sufficient to avoid a
  false completion claim.

These functions may reside on the robot, a dedicated local gateway, or a
coordinated local pair only if loss of any remote dependency cannot disable
them. The exact placement is an **UNRESOLVED INSTANTIATION**; the locality and
failure property are mandatory.

### May be remote, but absence blocks dependent progress

The following may be remote if authentication, freshness, correlation, and
fail-closed behavior are preserved:

- Person Server and mission resolution;
- governance/PDP evaluation;
- authority/claim sources;
- participation-credential issuance;
- authoritative session store;
- policy and catalog resolution; and
- external audit/analytics sink.

No cached `ALLOW` or previously successful session substitutes for an
unreachable required authority, policy, mission, session, or governance input.

### Audit availability rule

A remote audit-sink partition need not stop a safely authorized action only if
the local enforcement boundary first durably records the complete target-bound
decision/execution correlation needed for later delivery. If that local record
cannot be made, the action does not begin. Buffered delivery must be bounded,
ordered, attributable, and unable to cross A/B namespaces.

## 5. Network zones and allowed flows

The minimum conceptual zones are:

1. **Participant zone** — phone/browser and untrusted participant input;
2. **Session edge** — notice, credential presentation, channel binding, status,
   withdrawal, and rate limiting;
3. **Authority/governance zone** — Person Server, mission/policy/authority
   resolution, and SOGA/AAuth decision path;
4. **Local enforcement zone A** — A-bound PEP/adapter, safety, execution state,
   and Misty A command surface;
5. **Local enforcement zone B** — B-bound PEP/adapter, safety, execution state,
   and Misty B command surface; and
6. **Audit zone** — authoritative or buffered append-only evidence sink.

Required flow rules:

- participant input never reaches a Misty command endpoint directly;
- the participant zone cannot select a robot by supplying an arbitrary URL or
  address;
- governance emits a target-bound decision, not a Misty REST command;
- only the correctly bound local PEP/adapter may address its allowlisted Misty;
- A and B command surfaces are not mutually routable by default;
- A/B state stores and receipt queues use distinct access scopes even when
  hosted on shared infrastructure;
- inbound robot discovery and broadcast command paths are disabled or excluded
  from the governed path;
- management and emergency-stop access is separated from participant traffic;
  and
- every cross-zone flow is authenticated, minimal, and attributable.

Exact subnets, hosts, ports, credentials, firewall products, and service owners
are **UNRESOLVED INSTANTIATION** values to be recorded before connection. The
requirements prohibit treating those values as incidental deployment detail.

## 6. Partition and failure behavior

| Partition/failure | Required behavior | Prohibited inference or fallback |
|---|---|---|
| Phone ↔ session edge before consumption | No session is created; credential remains usable only if authoritative atomic state confirms it was not consumed | Do not infer participation from QR display, partial request, or retry |
| Phone ↔ session edge after session creation | No new participant-selected action; the live session follows its one-minute inactivity and five-minute hard limits; local stop remains available through an independent path | Do not replay the last input or extend the session because status delivery failed |
| Session edge ↔ authoritative session store | No issuance, consumption, session creation, mutation, or revival without one authoritative result | Do not create process-local shadow sessions or reconcile two winners later |
| Local enforcement ↔ Person Server/governance before action | No governed action begins; show only the authorized pending/degraded presentation and allow timeout/withdrawal | Do not reuse a prior `ALLOW`, approved tool, or mission alignment as live permission |
| Local enforcement ↔ policy/catalog/authority source | Stop at the earliest missing required dependency | Do not silently use an unversioned cache or omit a required evidence condition |
| Local enforcement ↔ bound Misty before dispatch | Record no execution or a definite `FAILED`; preserve local safety and session semantics | Never fall back to the other Misty or report HTTP/gateway success as robot execution |
| Remote dependency lost during actuation | The local enforcement boundary follows the primitive's declared interruption rule at the earliest locally safe boundary and reaches/maintains neutral; if immediate interruption would itself be unsafe, the independent local safety controller selects the pre-defined safe completion/stop behavior | Do not continue merely because remote governance previously returned `ALLOW`; do not assume that Wi-Fi loss itself proves braking or neutral state; do not wait for a new remote decision to honor safety or withdrawal |
| Remote audit sink unavailable | Continue only when a complete local durable receipt is recorded before actuation and bounded ordered delivery remains possible; otherwise do not begin | Do not drop, merge, or attribute A receipts to B |
| PEP/adapter process crashes before or during dispatch/actuation | The independent local safety halt remains available without that process; no new or queued primitive begins; any active primitive follows its declared local interruption/safe-completion rule; record `FAILED` or unknown outcome unless completion is independently observed | Do not infer that process death stopped physical motion, clear the platform safety state, restart or resume the action automatically, or report completion from the lost dispatch path |
| A-side failure or partition | B state remains unchanged and B receives no A command, evidence, permission, session mutation, or safety release | Do not fail over an A action or participant session to B |
| B-side failure or partition | A state remains unchanged and A receives no B command, evidence, permission, session mutation, or safety release | Do not fail over a B action or participant session to A |
| Ambiguous or conflicting partition state | Fail closed for new physical action; retain independent local safety/stop; record ambiguity without claiming completion | Do not choose the most permissive copy or reconcile by timestamp alone |

Timeout values for governance, network, adapter, and physical-actuation stages
are not established here. They require G28 measurement and PI authorization.
Session inactivity and hard maximum remain the D-023 values.

## 7. Mid-actuation interruption semantics

Every physical primitive or prebounded composition must declare before use:

- whether it is immediately interruptible, boundary-interruptible, or requires
  a specific safe-completion sequence;
- the local signal/mechanism that inhibits or interrupts it;
- the neutral/safe state it targets;
- the conditions under which neutral cannot be verified;
- the receipt states it can truthfully emit; and
- which network and remote dependencies are unnecessary once actuation starts.

On withdrawal, session termination, safety halt, target ambiguity, local fault,
or loss of a dependency required for continued safe execution:

1. no new primitive begins;
2. queued primitives are invalidated;
3. the active primitive stops at the earliest locally safe point;
4. the local safety boundary remains authoritative over physical continuation;
5. the execution result records `INTERRUPTED` or `FAILED`, never `COMPLETED`
   unless completion is independently observed; and
6. a late permission or restored network does not resume the old action.

Actual stopping time, distance, force, pose, and primitive-specific safe points
are **G28 VALIDATION** measurements. G27 requires the declarations and
fail-closed semantics, not invented numeric performance.

## 8. Acceptance tests required before robot connection

The isolation/network package is testable without contacting either Misty by
using two instrumented fake execution surfaces with distinct identifiers and
state stores. Passing these tests does not authorize physical connection; it is
a prerequisite for the connection gate.

### Positive control

Given a valid A-bound mission, credential, session, evidence set, current
context, and permission for one finite age-independent semantic action:

- Authority Established is reached without identity, age, or guardianship
  inference;
- only fake surface A receives one target-bound invocation;
- fake surface B receives none and its state remains byte-for-byte/logically
  unchanged;
- A records the separate decision, projection, execution attempt/result, and
  terminal/session correlation; and
- replay of the same action request returns the prior status/receipt and causes
  no second invocation.

Run the symmetric B-bound case using only capabilities actually declared for B.

### Required negative controls

1. Present an A credential to B.
2. Present an A session/action request to B's PEP.
3. Present an A decision package to B's adapter.
4. Remove or fault the A-bound primitive while B has an equivalent primitive.
5. Replay a consumed credential concurrently.
6. Repeat an already executed action request.
7. Expire the session while governance is pending, then deliver late `ALLOW`.
8. Partition the session edge from the authoritative store during consumption.
9. Partition local enforcement from governance before action.
10. Partition local enforcement from its Misty-equivalent surface before
    dispatch.
11. Lose a remote dependency during a boundary-interruptible fake actuation.
12. Make the remote audit sink unavailable with and without a functioning local
    durable buffer.
13. Halt A and verify B's safety state does not clear or change; repeat
    symmetrically.
14. Exhaust or flood A's participant/session path and verify B's termination and
    safety paths remain available.
15. Supply an artifact with missing or ambiguous `platform_id`.
16. Attempt to override an A-bound adapter with B's URL/address, including the
    historical single-base-URL configuration shape.

Each negative control must fail closed at the earliest affected stage, produce
no wrong-platform invocation, produce no duplicate physical invocation, preserve
the unaffected platform state, and record an attributable outcome.

## 9. Connection-gate evidence

Before either Misty is powered or connected for governed testing, the repository
must contain:

- adopted canonical identifiers for Misty A and Misty B;
- a named network-zone/flow instantiation with allowlisted endpoints;
- the authoritative session-state owner and atomic-consumption mechanism;
- per-platform PEP/adapter target bindings;
- a recorded disposition for the historical single-`MISTY` route: replaced or
  wrapped behind immutable per-platform allowlisted bindings;
- an independent local safety-halt mechanism and operator procedure for each
  platform;
- a provisional-component manifest and convergence obligations;
- passing fake-surface positive and negative isolation tests;
- a receipt schema that distinguishes dispatch, start, completion,
  interruption, failure, and unknown outcome; and
- a connection checklist that proves the intended target before any physical
  command is enabled.

Physical connection then validates only the declared platform and bounded
primitives. It does not authorize a public demonstration or establish G29/G30
evidence.

## 10. Explicit nonclaims and remaining work

This artifact does not establish:

- that either Misty is currently reachable, powered, safe, calibrated, or
  correctly identified;
- actual network topology, credentials, firewall configuration, or service
  ownership;
- measured latency, stopping time, distance, force, obstruction response, or
  neutral pose;
- live mid-actuation revocation;
- validated perception or subject-state inference;
- production-grade durability, availability, or security;
- public-event readiness; or
- G27 completion or G28 entry.

Still required for G27 exit: the full per-capability authority/context/risk,
degradation, audit, interruptibility, and locality matrix; completion of the
bystander/non-delegating affected-subject threat model; and adoption of the
positive/negative-control criteria with the complete G27 model.
