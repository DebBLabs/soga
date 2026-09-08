# M02 Stage 3 Proposal — Wallet/WAS Composition Seam

Date: 2026-09-07
Status: DRAFT FOR INDEPENDENT REVIEW — NOT AUTHORIZED FOR IMPLEMENTATION OR SERVICE EXECUTION
Prepared from checkpoint: `main @ c6c922984874382f48ff63e0210a6d6f2a8e44c2`

## Purpose

Demonstrate the narrowest truthful handoff that the selected wallet and Wallet
Attached Storage implementations can make into the accepted M02 Stage 2 local
Person Server. Stage 3 asks whether wallet-controlled evidence can cross a real
localhost boundary, be cryptographically verified, remain distinct from storage
authority, and become an explicit input to Person Server processing without
being mistaken for mission permission, representative authority, participant
admission, payment, or action execution.

This proposal does not itself authorize implementation, dependency installation,
service execution, external access, or a conformance claim.

## Evidence basis and selected candidates

The selection is derived from the adopted Stage 1 source review:

- Freewallet: `interop-alliance/freewallet`, `main @
  8e806c049b1134e36e72ab243ea3fbeb93153c37`, version 0.42.0,
  AGPL-3.0. It supplies the current wallet-originated interaction-URL,
  credential, key, and storage-grant candidate surfaces.
- WAS teaching server: `interop-alliance/was-teaching-server`, `main @
  2090a606f2723e4d57ef0090db55fd1bdab9427e`, version 0.27.0,
  AGPL-3.0-or-later. It supplies the current protected-storage, zCap,
  revocation, and conditional-write candidate surfaces.
- Accepted local Person Server: SOGA `m02_person_server` at `c6c9229`, with
  test-only HMAC identities, SQLite state, literal-loopback HTTP, and bounded
  B-038 live expiry/revocation support. It is not AAuth conformant and has no
  public JWKS.

The repository's older local candidate checkouts remain at Freewallet
`403bc55` and WAS teaching server `9139b1e`; they are evidence only and must not
be silently used as the Stage 3 runtime. Clean detached checkouts at the exact
selected Stage 1 SHAs must be obtained before execution.

The installed local runtime reports Node 26.7.0 and pnpm 11.19.0. The selected
candidate sources require Node 24 or later and pnpm 11.20.0. Stage 3 must use an
explicit project-local or otherwise reviewed pnpm 11.20.0 invocation; it must
not silently mutate the global package manager.

## Proposed disposition

Use the selected upstream applications unmodified as local research runtimes.
Do not fork, patch, redistribute, or describe either AGPL application as SOGA
code. Keep any SOGA adapter and tests in this repository under the existing
project license, with the process boundary and message contract documented.
The proposal makes no conclusion about whether later deployment, modification,
or network interaction would create additional AGPL obligations.

Stage 3 is divided into two separately authorized phases. Authorization of
Stage 3A does not authorize Stage 3B.

### Stage 3A — exact-source runtime reproduction

1. Create clean detached checkouts outside the SOGA repository at the two exact
   selected SHAs.
2. Record origin, SHA, license, lockfile hash, Node version, pnpm version, and
   every dependency-install command before execution.
3. Install only lockfile-pinned dependencies inside those detached checkouts.
   Package-registry access is permitted only if separately authorized by the PI;
   no application runtime is permitted external-network access merely because
   dependency installation was allowed.
4. Build and run each selected application on literal loopback using test-only
   state. Prefer the teaching server's documented non-Postgres local mode if it
   exists at the selected SHA. If Postgres, Docker, a global install, cloud
   service, remote DID resolution, remote context retrieval, telemetry, or an
   undocumented credential is required, stop and record the requirement rather
   than enabling it.
5. Record ports, processes, local storage paths, outbound attempts, startup and
   shutdown behavior, and whether the documented interfaces are actually
   reachable. Stop all processes at the holdpoint.

Stage 3A always ends with a standalone reproduction and interface-evidence
report, independent Gate 1 and Gate 2 review, and PI disposition. Failure at
Stage 3A ends the phase with that evidence report. It does not authorize
substitute software, a different SHA, or source modification.

### Stage 3B — narrow authenticated handoff

Stage 3B requires a separate later PI authorization based on accepted Stage 3A
evidence that both selected runtimes reproduced within the stated boundary and
that a source-supported interaction path exists. No SOGA adapter code or Stage
3B test may be written under Stage 3A authority.

Add the smallest test-only wallet handoff adapter at the local Person Server.
The adapter may accept only a documented Freewallet-originated response or
evidence envelope whose bytes, issuer/controller, key, audience, nonce,
challenge, issuance time, expiry, and replay identifier can be verified from
the selected source behavior. Unknown or unsupported security fields fail
closed. The adapter must retain the original evidence hash and a separate
normalized interpretation; it must not silently discard or reinterpret open
fields.

The successful path is:

`Freewallet interaction → verified test evidence → local PS handoff adapter →
explicit uninterpreted or supported evidence record → separately authenticated
WAS storage grant/write/read → PS processing`

The SOGA test harness drives the independent loopback clients and coordinates
each arrow in this path. No direct Freewallet-to-Person-Server or
Person-Server-to-WAS behavior is attributed to a candidate unless its selected
source and observed runtime supply it.

Only evidence fields that the implementation validates may become
decision-relevant. Storage zCaps authorize WAS operations only. A successful
wallet exchange or storage write does not create a person token, approve a
mission action, establish representative authority, record affected-person
assent, admit a participant session, prove payment, or authorize execution.

If Freewallet's documented response cannot be verified by a bounded local
adapter, or if no supported handoff exists, stop and record that negative result.
Do not invent a Freewallet API, wrap a fixture in wallet terminology, or claim
composition through a test object that did not cross the selected runtime.

The Person Server adapter is limited to receiving and verifying the wallet
evidence payload at `/_test/wallet-evidence`. It must not contain a WAS client,
invoke a storage capability, or coordinate the candidate services; those client
actions belong only to the bounded SOGA test harness.

## AAuth and Person Server boundary

The post-Stage-1 editor delta adds an informative minimal-Person-Server appendix
with `issuer`, `jwks_uri`, `person_token_endpoint`, and `auth_token_endpoint`.
Stage 3 does not claim conformance to that appendix. The accepted Stage 2 HMAC
metadata remains test-only and is not renamed as JWKS.

Stage 3 may define a wallet-evidence handoff route only under an explicit
non-protocol namespace such as `/_test/wallet-evidence`. It may not represent
that route as an AAuth endpoint. Adding protocol-shaped public-key metadata,
JWKS, person-token, or authorization-token behavior requires a separate design
and later PI disposition.

## Trust and data boundaries

- Use generated test-only wallet identities, keys, credentials, DIDs, subjects,
  missions, capabilities, and storage. Do not use Deb's wallet, identity
  documents, production credentials, personal data, payment instrument, or
  public DID.
- Bind every handoff to one local recipient, nonce/challenge, short expiry,
  evidence hash, and one-time replay record.
- Never place credentials, tokens, private keys, capabilities, or secrets in
  URLs, console output, audit text, screenshots, or committed fixtures.
- Keep raw secrets out of SOGA audit records. Record stable hashes and test
  identifiers sufficient to reproduce the decision path.
- Reject redirects, proxies, DNS destinations, wildcard binds, silent fallback,
  arbitrary callback URLs, and any destination other than reviewed literal
  loopback endpoints.
- Do not permit browser extension installation, system keychain changes,
  production browser profiles, camera use, microphone use, or QR scanning.
- Shut down all Stage 3 services and record process termination before review.

## Required implementation evidence

### Reproduction evidence

- Exact selected origins and SHAs are present and clean.
- License and lockfile hashes are recorded.
- Dependency resolution is reproducible and confined to the detached
  checkouts.
- Both applications start and stop on literal loopback, or the precise blocker
  is recorded without substitution.
- A network-observation record distinguishes package installation from runtime
  behavior and identifies every attempted non-loopback destination.

### Positive control

One generated test wallet interaction must traverse the actual selected
Freewallet runtime, produce source-supported evidence, cross a real loopback
handoff into the Stage 2 Person Server adapter, and cause one separately
authenticated write and read against the selected WAS teaching server. The
record must show the original evidence hash, verification result, normalized
supported fields, storage capability identifier or hash, PS correlation ID,
and complete SOGA decision if governance is invoked.

The positive result is a verified evidence and storage handoff only. It is not
proof of AAuth conformance, person identity, authority for another person,
participant consent, mission permission, action execution, or physical outcome.

### Named negative controls

- altered wallet evidence;
- wrong controller or verification key;
- wrong audience or callback recipient;
- wrong nonce/challenge;
- expired or future-issued evidence;
- replay of the same evidence;
- unrecognized security field;
- wallet evidence accepted but explicitly uninterpreted;
- wallet evidence that cannot satisfy a governance requirement;
- missing, expired, attenuated, wrong-target, or revoked WAS capability;
- storage success presented as mission permission;
- wallet possession or payment presented as representative authority;
- redirect, proxy, DNS, wildcard-bind, or non-loopback escape;
- secret material in an audit or log record; and
- shutdown leaving any selected service running.

Each negative control must assert the intended failure stage. A test that passes
because an earlier unrelated component failed proves nothing.

### Regression evidence

- Run focused Stage 3 tests.
- Run the complete SOGA test suite.
- Preserve all Stage 2 person-token, revocation, pending, reevaluation,
  one-time-delivery, and B-038 fail-closed behavior.

## Stop conditions and unresolved choices

Stop and return to the PI if:

- the exact selected source or lockfile cannot be reproduced;
- candidate documentation and package metadata disagree materially;
- license obligations cannot be kept explicit at the process boundary;
- required runtime behavior needs external services or source modification;
- the selected WAS teaching server requires Postgres or Docker; record the
  requirement without installing or starting either;
- completing the selected Freewallet interaction requires a graphical browser
  or platform WebAuthn/WebCrypto behavior unavailable in the reviewed test
  environment; record the limitation rather than substituting an unreviewed
  mock or browser automation;
- the wallet response lacks a verifiable source-supported handoff shape;
- satisfying the positive control would require inventing identity, authority,
  consent, participant-session, payment, or AAuth semantics;
- the implementation would add public JWKS or protocol-shaped token endpoints;
  or
- any request would expand to production credentials, external exposure,
  physical execution, Misty, R3, G28, or G29.

The participant-session owner, representative-authority evidence, independent
affected-person assent/refusal, general B-038 delegation and attenuation path,
AGPL deployment consequences, and protocol-shaped Person Server/JWKS design
remain unresolved.

## Explicit nonauthorization

This proposal authorizes nothing. If independently reviewed and accepted, the
PI may separately authorize Stage 3A source acquisition, dependency
installation, selected local service execution, and interface evidence. Stage
3B adapter implementation requires a later PI authorization after the Stage 3A
evidence passes both gates. Any resulting Stage 3B code must itself pass
independent Gate 1 and Gate 2 review and receive separate PI acceptance before
merge or commit. No authority for Stage 4, public or
external exposure, production identity, personal wallet use, payment,
participant-session implementation, representative or affected-person policy,
Misty access, physical actuation, R3 implementation, G28 activation, or G29
research follows.
