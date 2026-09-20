# M02 AAuth `-11` Steps 1–3 Implementation Proposal

Date: 2026-09-20
Status: PROPOSED — NOT AUTHORIZED FOR IMPLEMENTATION OR EXECUTION
Prepared at: `main @ f5ab9be3f41ee87a690a1be77d0dcaaf94e7be1f`
Author/integrator: Codex
Review class: mandatory dual review under D-064

## Purpose

Create the cryptographic and request-authentication foundation for one real,
mission-bound AAuth flow without yet issuing an AAuth person, resource, or auth
token. This proposal implements only Steps 1–3 of the D-084 accepted gap report:

1. pin every new conformance claim and fixture to AAuth editor's-copy commit
   `fcf656de1926535f5bd6fc0538147ead6646e727`;
2. add asymmetric token primitives with mandatory Ed25519 support, exact AAuth
   token `typ` values, public JWKS, strict algorithm/key consistency checks, and
   wrong-token-type rejection; and
3. add signed-agent HTTP request verification and truthful interim Person Server
   metadata without claiming the full Person Server conformance floor.

The result is foundation code, not a complete AAuth transaction. Steps 4–9,
including mission approval, real token endpoints and resource enforcement, remain
separately gated.

## Verified basis

- D-084 accepts
  `knowledge/research/M02_AAUTH_FCF656D_CONFORMANCE_GAP_2026-09-20.md` at
  SHA-256 `048594716738b9192a5da7a81444a46636160eb5f0ba8dc7321e0d3254582bc6`.
- The primary specification is the detached checkout at exact commit
  `fcf656de1926535f5bd6fc0538147ead6646e727`; its protocol markdown has SHA-256
  `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`.
- The existing `m02_person_server` package deliberately uses HS256 compact
  tokens with generic `typ: JWT` and HMAC request signatures. It is accepted
  test scaffolding and must remain available under its existing claim boundary.
- The current environment has no discoverable Python `cryptography` or `nacl`
  module. Python's standard library does not provide the needed Ed25519/JWS
  implementation. No dependency may be selected, installed, or vendored by
  inference.

## Proposed architecture

Create a separate `m02_aauth_fcf656d` package and focused tests. Do not rewrite
the accepted `m02_person_server` crypto or its fixtures in place. The new package
may reuse dependency-free canonicalization helpers only when their behavior is
explicitly tested and their provenance remains clear.

The package contains four bounded layers:

1. `profile.py` — immutable identifiers for the pinned source commit, protocol
   digest, supported token types and required signature components.
2. `jose.py` — compact JWS signing and verification through one reviewed
   Ed25519 provider; protected headers require the fully specified `alg` value
   `Ed25519`, an exact allowed AAuth `typ`, and a nonempty `kid`. Verification
   resolves only public JWKs and rejects `alg=none`, the polymorphic `EdDSA`
   identifier, symmetric algorithms, an absent `alg`, unknown `kid`, malformed
   keys, duplicate or unknown critical parameters, and any `kty`/`crv`
   disagreement. Every key the package publishes or accepts must carry a fully
   specified `alg` member; a key whose `alg` is absent must be rejected.
3. `http_signatures.py` — generation and verification of the AAuth request
   signature form using the pinned draft's required covered components:
   `@method`, `@authority`, `@path`, and `signature-key`; body-bearing PS
   requests also require `content-digest` and `content-type`. Verification binds
   the derived components to the received request, verifies content digest
   before consuming JSON, rejects omitted/duplicated required components, and
   requires the integer `created` signature parameter and verifies it against
   the pinned draft's default 60-second validity window. A short-lived replay
   cache keyed by `(signing-key-thumbprint, created, @method, @authority,
   @path)` is an explicit stricter SOGA policy choice permitted, but not required,
   by the draft; the profile defines no nonce mechanism.
4. `metadata.py` — interim discovery metadata that remains explicitly
   nonconformant/test-only. It may truthfully publish the issuer and JWKS URI
   once they exist, but it must not publish or imply the four-field Person Server
   conformance floor until both required token endpoints are implemented.

Private keys remain in memory for tests and are never serialized, logged, placed
in SQLite, returned through metadata, or committed as fixtures. Public test JWKs
and deterministic non-secret test vectors may be committed only if independently
verified to contain no private `d` parameter.

## Dependency holdpoint

Before any implementation is authorized, a short dependency record must identify
one maintained Python provider that supports Ed25519 key generation, raw signing
and verification, and public-key serialization. The record must pin its exact
name, version, distribution hashes, license, primary-source documentation and
Python compatibility; identify direct and transitive packages; and state whether
a wheel contains native code. Both gates must review that record.

Dependency acquisition, installation, registry access, lockfile creation and
vendoring are not authorized by this proposal. A later PI authorization must
name the exact artifact and permitted network operation. Calling the `openssl`
executable from runtime code is not an approved substitute.

## Proposed phases

### Phase 0 — dependency and source-profile review

Create the dependency record and exact normative-requirement matrix only. Read
the pinned checkout and current repository; do not install, import, compile or
execute candidate code. Both blind gates review the complete record before the
PI selects a provider or authorizes acquisition.

### Phase 1 — create only

After the provider is selected, acquired and independently verified under a
separate prospective decision, create the complete new package and focused test
files. Do not import the provider, run tests, compile code, start a listener or
execute any created source. Both eligible blind reviewers inspect every created
file before commit or execution.

### Phase 2 — bounded execution

Not authorized by this proposal. A separate execution proposal must pin the
reviewed source hashes, dependency environment, exact commands, finite limits,
cleanup, evidence fields and stop rules. It must distinguish pure unit tests
from any loopback HTTP test because a listener requires separate authority.

## Required tests to create in Phase 1

- Ed25519 sign/verify positive vectors and altered header, payload and signature;
- exact AAuth `typ` acceptance and cross-type rejection, including a person token
  presented to an auth-token verifier;
- rejection of `none`, the polymorphic `EdDSA` identifier, HS256, unsupported
  algorithms, unknown `kid`, private JWK publication, an absent `alg`, and
  mismatched `alg`/`kty`/`crv`;
- deterministic public JWKS shape with no private material;
- a published JWKS in which every selected key carries a fully specified `alg`,
  and rejection of a supplied selected key that omits `alg`;
- all four base HTTP signature components required exactly once;
- body requests additionally requiring and verifying `content-digest` and
  `content-type`;
- altered method, authority, path, body, content type or signature-key;
- missing or non-integer `created`, duplicate components, signatures outside the
  60-second default window, excessive forward clock skew, and replayed signatures;
- bounded parsing failures for malformed structured fields and oversized input;
- metadata that is truthful before token endpoints exist and a regression test
  proving it does not claim the Person Server conformance floor; and
- regression protection showing the accepted Stage 2 package and fixtures were
  not modified or silently reclassified as conformant.

Every negative test names its intended rejection stage. Test fixtures use only
generated or clearly marked non-secret material.

## Evidence required from any later execution

- exact SOGA commit and clean/expected working-tree state;
- pinned AAuth commit and protocol digest;
- exact dependency identity, installed distribution hash and license record;
- hashes of every new source and test file;
- exact commands, exit statuses and complete test counts;
- confirmation that no listener, external service or network access occurred;
- confirmation that no private key or secret entered output or repository files;
- before/after repository status; and
- an explicit claim boundary: Steps 1–3 foundation only, not a complete AAuth
  Person Server or mission flow.

The Phase 0 requirement matrix must separately define identifiers serving
different protocol purposes: JWT header `kid` selects an issuer key from JWKS;
the signing-key thumbprint used by the optional replay cache is computed from
the resolved public key; and `agent_jkt` is a resource-token claim used only in
a later step. The implementation must not silently treat these as interchangeable
or require `kid` itself to be a JWK thumbprint unless a later reviewed profile
decision explicitly does so.

## Stop rules

Stop before implementation or execution if:

- the selected provider cannot be pinned and independently verified;
- the provider or its transitive dependencies require an unreviewed build,
  service, credential, network action or incompatible license;
- the pinned specification is unavailable or differs from the accepted hashes;
- implementing the required signature form would require guessing beyond the
  pinned draft or its normative references;
- preserving the accepted Stage 2 package would require destructive changes; or
- any requested action crosses into Steps 4–9 or another excluded boundary.

## Claim boundary and exclusions

A successful later Phase 2 would establish only that SOGA has pinned AAuth
`-11` cryptographic token primitives, public JWKS handling, signed-agent request
verification and truthful interim metadata under the tested profile. It would
not establish a conformant Person Server, a valid person/resource/auth token
flow, an approved mission, authorization, supervision, revocation, wallet
presentation, WAS integration, participant admission or robot execution.

This proposal itself authorizes no code creation, dependency operation, import,
compilation, lint, test, runtime execution, listener, external/network service,
Freewallet or WAS integration, personal data, payment, QR flow, Misty access,
physical actuation, G28 or G29. The unrelated PI routine-tool proposal remains
excluded and untouched.

## Required review and PI decisions

1. Both eligible blind reviewers read this complete proposal and verify its
   claims against the pinned draft and current repository.
2. The PI decides whether to accept the proposal and authorize Phase 0 only.
3. Provider selection and acquisition receive their own prospective decision.
4. Phase 1 creation and Phase 2 execution each require separate prospective PI
   authorization after their respective review holdpoints.
