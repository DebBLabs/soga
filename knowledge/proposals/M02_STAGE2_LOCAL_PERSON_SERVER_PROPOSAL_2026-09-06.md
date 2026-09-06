# M02 Stage 2 Proposal — Bounded Local Person Server

Date: 2026-09-06
Status: REVIEWED AND AUTHORIZED FOR IMPLEMENTATION UNDER D-036
Prepared by: Codex/CG after three read-only local Codex investigations
Review target: `main @ 2debcd10db5b6a7082b04d339b2bb2967cd6de5b`

## Purpose

Replace the G26 in-process Person Server mock boundary with the smallest
credible localhost Person Server service that can demonstrate authenticated,
mission-bound AAuth permission and reevaluation messages reaching SOGA.

Stage 2 demonstrates a bounded local protocol and security seam. It does not
claim a production or conformant Person Server, wallet/WAS composition,
interoperability, public deployment, participant-session solution, or robot
readiness.

This proposal does not itself authorize implementation or service execution.

## Evidence basis

The proposal derives from:

- M02 Stage 1 research and its two independent PASS reviews at `2debcd1`;
- the G26 permission and reevaluation implementation;
- B-038 live authority validity/revocation and B-039 affected-person gaps;
- the G27 participant-session and safety boundaries;
- AAuth published `-10`, separately identified current base-editor material,
  and separately exploratory R3;
- Posta Person Server `18d9558` as Apache-2.0 reference lineage, not a selected
  runtime dependency; and
- three parallel read-only Codex investigations of service responsibility,
  security/acceptance controls, and implementation lineage.

## Proposed architectural disposition

### Build a small local service; do not fork the full Posta runtime

Use SOGA's `aauth_permission` package as the integration spine because it
already preserves:

- immutable mission hashing and an append-only mission log;
- per-action SOGA evaluation;
- separate complete SOGA decisions and lossy AAuth projections;
- deferred HOLDING state with expiry;
- authenticated approval evidence followed by reevaluation rather than
  automatic grant; and
- agent-bound, one-time terminal delivery.

Do not rename the current mock as a real Person Server unchanged. It is
in-memory, trusts caller-provided identity headers, has no signed-token or HTTP
message verification, has no PS metadata/JWKS surface, and lacks live authority
validity and revocation inputs.

Posta's current Apache-2.0 implementation may be used as reference lineage for
data contracts, pending-state guards, metadata, signing, and persistence
patterns. Do not import or run it in Stage 2. Its broader FastAPI/SQLAlchemy
stack would expand dependencies, its permission rule is not SOGA's every-action
governance rule, and source inspection did not establish implementation of the
current editor draft's `aa-person+jwt` person token.

### Local topology

Stage 2 consists of separately exercised local components:

`test agent/client → loopback HTTP Person Server → in-process SOGA governance`

The Person Server and client communicate through real loopback HTTP messages.
SOGA remains the Person Server's governance policy implementation through a
defined internal interface; it is not invented as a new AAuth protocol party.

The test agent/client is part of the Stage 2 acceptance harness and is operated
locally by the developer or test runner. It is not a wallet, participant
application, production agent, or separately deployable service.

No wallet, WAS, participant application, resource server, Misty adapter, fake
Misty service, payment service, federation server, or external endpoint is part
of Stage 2.

## Person Server responsibilities in Stage 2

The bounded service owns:

1. PS well-known metadata and a public verification-key document;
2. explicit test-only local signing keys and key identifiers;
3. authenticated agent/request binding;
4. immutable mission creation/lookup and append-only mission records;
5. a narrow person-token issue, retention, presentation, and validation slice;
6. permission requests for every semantic action;
7. invocation of SOGA for every action and separate retention of the complete
   SOGA result and its AAuth projection;
8. pending approval/clarification, expiry, terminal resolution, reevaluation of
   the same mission/action/subject, and one-time terminal delivery;
9. current token validity and revocation state; and
10. correlated, non-secret audit entries.

The narrow person-token profile is explicitly local and editor-draft-shaped,
not a conformance claim. It must bind at least issuer, audience/resource,
subject continuity, agent confirmation key, token identifier, issuance and
expiry, and optional mission hash. The PS must retain the issued-token record
and compare a presented token against it.

## B-038 bounded repair proposed for explicit authorization

Stage 2 should not build a revocation façade that governance cannot see.
Therefore the later PI decision is asked to authorize a bounded repair of the
AAuth execution bridge:

- derive signature/key binding, issuer, audience, token identifier, issued-at,
  expiry, retained-token status, revocation status, mission binding, and agent
  binding from authenticated current PS evidence;
- pass verified current-state values into the SOGA authority evaluation rather
  than accepting caller dictionaries or hardcoded safe values;
- keep policy limits distinct from observed state;
- represent unsupported delegation depth, elapsed delegation time, or
  attenuation evidence as unavailable and fail closed whenever policy requires
  them; and
- add named negative controls proving each supported or unavailable value
  reaches the intended decision stage.

This is a bounded partial implementation of B-038 for the selected Stage 2
token profile. It does not claim to close B-038 for every authority carrier.

## Explicit non-responsibilities

Stage 2 does not decide or implement:

- wallet UI, wallet key custody, Freewallet, or WAS execution;
- representative-authority sufficiency;
- affected-person assent, refusal, or precedence under B-039;
- participant QR/session-grant admission;
- payment or donation;
- external AS federation or independent interoperability;
- production identity proofing or legal identity;
- resource-side or adapter enforcement;
- physical execution, outcome measurement, or Misty access;
- R3 implementation or adoption; or
- G28 activation.

Arbitrary `representative`, `assent`, or `refusal` fields must not silently
become decision-relevant. The service must either reject unsupported semantic
fields or retain them with an explicit uninterpreted status. An approver's
decline remains distinct from an affected person's refusal.

## Security boundary

1. Bind only to literal loopback addresses on OS-assigned ports. Reject
   `0.0.0.0`, hostname discovery, arbitrary destinations, proxies, redirects,
   and silent fallback.
2. Use test-only keys and identifiers. Use no production credential, personal
   identity document, or secret in a URL or log.
3. Validate method, route, content type, body-size limit, JSON-object shape,
   schema, and required fields. Reject ambiguous or unknown security fields.
4. Authentication must depend on verified cryptographic/test trust, not the
   existing `G26-PS-Assertion: authenticated` or caller-controlled
   `AAuth-Agent` headers.
5. Never log private keys, raw bearer/session material, or full tokens. Audit
   stable identifiers and hashes needed for correlation.
6. Keep physical adapters and all Misty modules/addresses unreachable from the
   Stage 2 package.
7. State persistence and concurrency truthfully. A process-local store cannot
   support claims of durability, restart recovery, or multi-process atomicity.

## Minimum interfaces

Exact route names remain proposal-level until Gate review, but the service must
provide the following bounded functions:

- retrieve PS metadata and verification keys;
- create or admit a local test mission through an explicitly non-production
  administrative fixture;
- issue and retain a person token for one configured fake resource and agent
  key;
- submit a signed mission/action permission request;
- return a terminal permission projection or a standard deferred response with
  requirement, location, and retry guidance;
- retrieve pending state with authenticated agent binding;
- submit authenticated approval or clarification evidence bound to the pending
  request; and
- revoke an issued token through an explicitly local administrative fixture so
  live invalidation can be tested.

Any interface invented solely for testing must be labeled non-production and
must not be described as an AAuth-standard endpoint. Administrative and test
fixtures must use an explicit non-protocol route namespace such as `/_test/`.

## State and storage

Stage 2 may begin with a new explicit local store only if its limitations are
part of the acceptance claim. It must track:

- keys and key identifiers;
- missions, policies, updates if selected, and append-only mission records;
- pending requests, expiry, ownership, terminal state, and delivery state;
- issued person-token identifiers, hashes/bindings, expiry, and revocation;
- approval/clarification evidence and reevaluation linkage; and
- correlated SOGA decisions and AAuth projections.

The implementation proposal must choose between:

- an in-memory store with restart and durability explicitly excluded; or
- a small local durable store with restart and transaction behavior explicitly
  tested.

No storage choice may be made silently in code. WAS remains outside Stage 2.

## Required acceptance evidence

Every negative control must have its own named test and assert the intended
failure stage rather than merely observing an earlier error.

### Positive control

A signed, current, exact-issuer/audience/agent/mission/action request crosses
loopback HTTP into the Person Server, reaches SOGA, and returns an AAuth
permission projection while preserving the complete SOGA decision separately.
No execution surface or physical-success result exists.

### Transport and parsing controls

- reject non-loopback bind and destination;
- reject redirects, DNS/proxy escape, missing endpoint, and fallback endpoint;
- reject unsupported methods/routes, wrong content type, oversized body,
  malformed JSON, non-object JSON, and unknown security fields.

### Authentication and binding controls

- reject unsigned, altered, wrong-key, wrong-issuer, wrong-audience/resource,
  wrong-agent, wrong-mission, wrong-action, missing-binding, and future-issued
  material;
- prove that forged legacy magic headers authenticate nothing; and
- reject token/request replay with conflicting bytes or bindings.

### Validity, revocation, and reevaluation controls

- reject expired and revoked person tokens before governance can authorize;
- prove verified current state, not caller dictionaries, supplies the supported
  B-038 inputs;
- fail closed when a policy requires unavailable delegation-depth, elapsed-time,
  or attenuation evidence;
- reject stale, unavailable, or conflicting authority state;
- bind approval/clarification to the original pending identifier, mission,
  action, agent, constraint, and expiry;
- prove a late approval cannot revive expired or revoked state; and
- require reevaluation; approval evidence alone never grants.

### Lifecycle, race, and audit controls

- preserve byte-equivalent idempotency while rejecting conflicting request-ID
  reuse;
- ensure concurrent approval or terminal polling produces one authoritative
  transition and no divergent projections within the declared process model;
- verify one-time terminal delivery if retained by the selected contract;
- verify audit correlation across request, mission, token, decision,
  reevaluation, and projection without recording secrets;
- test the declared restart behavior; and
- run the complete existing SOGA suite.

### Boundary control

A package inspection test must establish that Stage 2 imports or reaches no
Freewallet/WAS runtime, external address, discovery path, Misty module/address,
physical adapter, or physical-success state.

## Stop conditions

Stop and return to the PI if implementation would require:

- running or installing Freewallet, WAS, or Posta's service;
- modifying an upstream checkout or making a public GitHub fork;
- selecting protocol behavior not bounded in the reviewed proposal;
- claiming `-11`, R3, production, or interoperability conformance;
- using production keys, personal identity data, or externally reachable
  services;
- collapsing PS, SOGA, participant, representative, affected-person, payment,
  or resource responsibilities;
- relying on caller assertions or magic headers as authentication;
- allowing external redirects, DNS/proxy routing, fallback, or permissive
  defaults;
- accepting a concurrency path with two authoritative winners;
- accessing either Misty robot; or
- activating or rewriting G28.

## Decision requested after independent review

If Gate 1 and Gate 2 pass this proposal, ask the PI to authorize:

> M02 Stage 2 bounded localhost Person Server implementation, including the
> narrowly described B-038 live-input repair, using test-only identities and no
> execution surface. No wallet/WAS/Posta service execution or dependency
> installation, external exposure, production credentials, participant-session
> implementation, representative/affected-person policy, Misty access,
> physical actuation, R3 implementation, or G28 activation is authorized.

The PI supplied this exact authorization on 2026-09-06 and D-036 records it
prospectively before implementation. Independent implementation review remains
required before Stage 2 is accepted or represented as complete.
