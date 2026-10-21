# IIW Real QR Participant Session Proposal

Date: 2026-10-21
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ 474a574eda798bdedde9b659df853065c16e575d`
Review class: mandatory blind dual review under D-064

## Purpose

Create a machine-independent, fail-closed QR participant-session transport.
Replace the R6 mock QR's local slide-navigation affordance with a real,
short-lived interaction that a consenting adult can open from a second device
on an explicitly selected isolated local network. This phase deliberately stops
before connecting that input to the D-144 operator seam, because that seam
records every input as a parent acting through local operator control.

This proposal separates creation, synthetic testing and physical second-device
testing. It authorizes none of them by itself. In particular, no non-loopback
listener may be opened until the complete implementation and execution
instrument receive prospective review and PI authorization.

## Accepted basis and frozen boundary

D-144 establishes only the bounded localhost demo operator adapter over the
accepted standing-policy and held-request seams, with 93 passing tests. The
following remain unchanged during the proposed first implementation phase:

- every accepted `m02_aauth_fcf656d` production module;
- every accepted AAuth/SOGA test and runner;
- the Permission to Speak R6 presentation and bridge;
- the durable provider runtime and manifest; and
- all Misty, wallet and WAS code.

The transport may invoke only a supplied, synthetic callback in later loopback
tests. It must not call `DemoOperatorAdapter`,
`OtherPartyApprovalPolicy.replace()`, `ApprovalPendingStore.resolve()`, or any
other AAuth/SOGA production seam. The accepted operator adapter stamps receipts
with `asserted_role="parent"` and `source="local-operator-demo-control"`, and
the accepted receipt model rejects any other asserted role. Mapping an adult
participant through that seam would create false role and source evidence.
Connecting participant input to AAuth/SOGA therefore remains a named holdpoint
requiring a separately reviewed semantic seam or accepted-source correction.

## Participant and claim model

The first IIW profile is intentionally narrow:

- the scanner is a consenting adult participant;
- no name, email, device identifier, age, parent/child relationship,
  credential or biometric is requested or retained;
- possession of the QR session is not identity, representative authority,
  consent for another person or legal authority;
- the participant may submit exactly one of `ALLOW_DIRECTED_RESPONSE` or
  `DECLINE_DIRECTED_RESPONSE` for the fixture action
  `address_participant`, participant identifier `adult-demo-participant`, and
  the labelled fixture mission described below;
- the resulting input remains labelled `unverified demo input`; and
- the visible and recorded result distinguishes participant input, SOGA
  governance and resource enforcement.

Parent, guardian, caregiver, proxy and other representative-authority scenarios
remain outside this implementation phase.

The participant sees only a fixed acknowledgement: `choice recorded` after an
accepted submission, or an indistinguishable `session unavailable` response for
invalid, expired, replayed or cancelled sessions. No AAuth authorization result
is claimed or displayed in this phase.

## Runtime composition and mission label

The create-only package is a standalone participant-session transport. It does
not construct a Person Server, Resource, AAuth token flow, approval store or
other-party policy. Synthetic tests supply an in-memory callback that records
only the fixed choice and binding fields needed to prove one invocation.

The session binds to the fixed, visibly labelled fixture mission identifier
`iiw-adult-participant-fixture-v1` and fixture action `address_participant`.
These are test labels, not evidence of an approved mission. Expiry uses an
injected clock for pure tests and the system monotonic clock for transport
lifetimes. Any later live AAuth/SOGA composition must separately identify its
constructor, clock source, mission provenance, accepted status and participant
semantics before implementation or execution.

## Machine-independent package requirements

The source package must:

1. use no absolute user, repository, evidence or `/private/tmp` path;
2. resolve all static inputs relative to a verified bundle root;
3. separate platform-neutral source and presentation assets from a
   platform-specific, hash-pinned Python/provider runtime;
4. support an explicit runtime manifest naming operating system, architecture,
   Python version, provider files and complete hashes;
5. refuse unsupported or mismatched platform, source, runtime or manifest;
6. write bounded evidence only beneath an operator-selected durable output
   directory outside the source bundle;
7. require no package installation, build, network retrieval or cloud service
   at execution time; and
8. leave the current Mac development tree and the R6 bundle unchanged.

The first implementation may be created and statically reviewed on the current
Mac. Cross-machine startup, Intel compatibility and second-device access are
separate later evidence claims.

## Session and QR contract

The gateway creates at most one live demonstration session. Its QR contains an
`http` URL composed from an operator-supplied, preflight-validated literal IPv4
private address and fixed gateway path. The cryptographically random
single-session capability is carried in the URL fragment so it is not sent in
the initial HTTP request; page script submits it with the fixed choice. The URL
contains no personal data, AAuth token, signing key, reusable credential or
repository path.

Plain HTTP provides no confidentiality or server authentication. A device or
network observer may capture the later capability submission, race the intended
participant, cause denial of service, or leave the URL fragment in browser
history. The capability grants only one unverified demo choice; it grants no
identity, credential, authority or resource access. Those limits reduce impact
but do not remove the risk. This proposal does not supersede the earlier HTTPS
requirement for deployment or public-event use. It requests a narrow exception
only for one later, separately authorized test on an operator-controlled Beryl
network after its isolation is observed. Shared venue Wi-Fi is prohibited.

The session must:

- have at least 128 bits of cryptographically random capability entropy;
- expire after a fixed maximum of 120 seconds;
- permit at most one accepted participant choice;
- bind the choice to the exact session, mission hash, demonstration action,
  gateway instance and expiry;
- reject malformed, expired, replayed, unknown and cross-session requests
  indistinguishably;
- invalidate the capability after accepted use, operator cancellation,
  timeout or shutdown;
- provide an explicit participant notice before enabling the choice;
- tell the participant that choosing nothing and leaving is permitted;
- return no internal state, token, key, stack trace or policy details; and
- retain no browser fingerprint, source address or participant-supplied text
  in durable evidence.

Withdrawal after a completed action is not claimed by this first QR profile.
The accepted D-144 withdrawal behavior remains a separate local operator
capability until a later proposal defines a participant-owned continuation
session.

## Network and listener boundary

The implementation must never select an interface or address automatically.
A later execution request must name one exact host interface and literal IPv4
private address. A pure, non-listening validator must first reject loopback,
link-local, multicast, unspecified, reserved and non-private IPv4 values. A
separate preflight must prove before binding that:

- the address is assigned to the named interface;
- it is neither wildcard, loopback, link-local nor publicly routed, using the
  offline address classification plus the recorded host route for that exact
  address;
- no process already owns the selected port;
- the exact participant URL uses that literal address;
- external reachability is not required by the test; and
- the operator has separately verified that the selected Beryl network permits
  client-to-host local traffic and supplies the intended isolation boundary.

The server binds only the exact approved literal address and selected port,
accepts only the exact `Host` value, serves only the participant page and its
bounded session endpoint, imposes finite header/body/request/time limits, and
closes fail-closed on unexpected methods, paths, media types or body framing.
It must never bind `0.0.0.0`, `::`, a hostname, loopback plus LAN together, or
an address discovered at runtime.

Default request logging, including client-address logging, must be disabled.

No proposal text may claim that application code alone proves network
containment. Beryl configuration and route behavior are independent
preconditions to be observed in a later controlled test.

## Proposed create-only package

After blind dual review and prospective PI authorization, create only:

1. `iiw_qr_session/session.py` — pure session state and capability validation;
2. `iiw_qr_session/gateway.py` — bounded HTTP codec and synthetic callback
   protocol; it contains no accepted-operator or AAuth/SOGA binding;
3. `iiw_qr_session/package.py` — relative-root and runtime-manifest checks;
4. `tests/test_iiw_qr_session.py` — pure and synthetic transport tests;
5. `tools/iiw_qr_session/run_static_and_loopback_tests.py` — a later-reviewable
   bounded controller restricted to literal loopback for synthetic tests; and
6. a source-only operator README describing preparation, start, stop and
   recovery without asserting that any network execution has occurred.

Creation must not import, compile, lint, test, execute, generate a live QR,
open a listener or contact a device.

## Required tests for a later execution proposal

A later bounded synthetic execution must prove:

1. exact manifest and relative-root acceptance and every mismatch refusal;
2. capability entropy, expiry, single-use and terminal invalidation;
3. exact session/mission/action/gateway binding;
4. malformed, expired, replayed, unknown and cross-session failure;
5. no participant identifiers or request-source addresses in evidence;
6. exact notice-before-choice behavior;
7. fixed choice vocabulary and bounded JSON codec;
8. controlled method, path, media-type, length and framing rejection;
9. supplied synthetic callback invoked once only after valid input, with exact
   fixed choice, fixture mission, action and participant bindings;
10. no AAuth token, key or internal policy content returned or logged;
11. startup refusal for wildcard, hostname, loopback-plus-LAN or unassigned
    address configuration; and
12. complete cleanup with no listener or live capability remaining.

Synthetic tests must use loopback only. A phone/Beryl execution requires a
separate proposal, exact reviewed instrument and prospective PI authorization.

## Evidence and review sequence

1. Both blind gates review this complete proposal.
2. PI acceptance may authorize create-only implementation.
3. Both blind gates review every complete created file before commit.
4. A separately reviewed synthetic execution proposal may authorize one
   loopback-only test run.
5. Only after positive synthetic evidence may a separate Beryl/phone proposal
   request one exact non-loopback execution.
6. Clean-machine and Intel runtime claims require their own observed evidence;
   success on the development Mac is not portability evidence.
7. Use with attendees at IIW or another public demonstration requires a
   separate G29 and privacy disposition; the Beryl/phone test is not event-use
   authority.

## Claim boundary and exclusions

A later positive synthetic result may establish only the session and gateway
logic under loopback. A later positive Beryl result may establish only that one
second device completed the bounded adult-participant interaction over the
named isolated local network.

Neither establishes identity, age, consent for another person, parental,
guardian, caregiver or legal authority, complete AAuth conformance, GNAP or
Transaction Token integration, clean-machine portability, public-network
safety, wallet/WAS integration, presentation correctness, Misty connection,
physical action, G28 or G29.

No repository modification, listener, execution, dependency operation,
network retrieval, external service, participant data collection, QR scan,
wallet/WAS work, Misty access or physical action is authorized by this
proposal. The unrelated PI routine-tool proposal remains excluded and
untouched.

