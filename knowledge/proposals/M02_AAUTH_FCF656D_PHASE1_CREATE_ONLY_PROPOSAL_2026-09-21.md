# M02 AAuth `fcf656d` Phase 1 Create-Only Proposal

Date: 2026-09-21
Status: PROPOSED — NOT YET AUTHORIZED
Prepared at: `main @ 631b4711781bbb7c7ef0ec5326bd8afe04ef75fd`
Review class: mandatory blind dual review under D-064

## Purpose

Create, but do not execute, the Steps 1–3 AAuth foundation accepted in D-085,
using the normative matrices accepted through D-092 and the Ed25519 provider
behavior accepted in D-099.

## Exact create-only package

Create only:

- `m02_aauth_fcf656d/__init__.py`
- `m02_aauth_fcf656d/profile.py`
- `m02_aauth_fcf656d/structured_fields.py`
- `m02_aauth_fcf656d/jose.py`
- `m02_aauth_fcf656d/http_signatures.py`
- `m02_aauth_fcf656d/metadata.py`
- `tests/test_m02_aauth_fcf656d.py`

Do not modify `m02_person_server`, its tests or accepted fixtures.
The dedicated `structured_fields.py` shared parser/serializer is the later
D-092 matrix's explicit refinement of the four-layer D-085 architecture.

## Required behavior

### Profile and bounded parsing

Pin AAuth commit `fcf656de1926535f5bd6fc0538147ead6646e727`, protocol
SHA-256 `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`,
the exact AAuth token `typ` values, the fully specified `Ed25519` algorithm,
the required HTTP covered components, the 60-second freshness window and
explicit input/member/nesting/byte limits. Implement only the RFC 9651 types and
forms required by the accepted matrix. Reject duplicate keys and parameters as
the disclosed stricter SOGA anti-smuggling rule; do not call that RFC behavior.

### JOSE and JWKS

Use only the independently accepted `cryptography 50.0.1` provider interface.
Implement compact JWS signing and verification, deterministic public JWKS,
strict `alg`/`typ`/`kid` handling, key consistency, public-only publication and
cross-token-type rejection. Reject `none`, `EdDSA`, symmetric algorithms,
missing or unknown `kid`, absent JWK `alg`, private `d`, malformed keys and
`kty`/`crv`/`alg` disagreement. Private keys remain in memory and must not be
serialized, logged or committed.

### HTTP Message Signatures

Implement the accepted bounded AAuth/RFC 9421/9530/9651/Signature Keys `-09`
profile. Cover `@method`, `@authority`, `@path` and `signature-key` exactly once;
body requests also cover `content-digest` and `content-type`. Derive request
components from the received request, verify SHA-256 content digest before JSON
use, require integer `created`, apply the 60-second window and bounded forward
skew, correlate one signature label and resolve only the `jwt` Signature-Key
scheme. Wire `alg` and `keyid` cannot override the resolved JWK. Include the
stricter bounded replay cache keyed by public-key thumbprint, `created`, method,
authority and path. No nonce, live JWKS fetch, egress, listener or transport is
implemented. Emit and parse the six accepted `Signature-Error` codes using the
bounded Structured Fields grammar. Do not implement the unresolved RFC 9421
`sf` component parameter; encountering a need for it is a stop condition.

### Metadata

Publish truthful test-only issuer/JWKS information but do not publish or imply
the four-field Person Server conformance floor or any unimplemented token
endpoint.

### Tests to create

Create all positive and negative tests listed in the accepted Steps 1–3
proposal and normative matrices, including exact token-type confusion,
algorithm/key mismatches, public-only JWKS, signature component ordering and
duplication, altered request/body/content type, digest-before-JSON ordering,
freshness/skew/replay, malformed and oversized Structured Fields, uniform
signature errors, metadata truthfulness, and non-modification of the accepted
Stage 2 package.

Tests may generate ephemeral keys only when later executed. No private fixture
or production-like identity data may be committed.

## Provider binding

Source may import the reviewed public APIs of `cryptography`, but this phase
may not import or execute them. D-099 accepted only the APIs exercised by the
accepted evidence: `Ed25519PrivateKey.from_private_bytes`, `public_key()`,
`public_bytes_raw()`, `sign()`, and `Ed25519PublicKey.verify()`.
JWK-based verification additionally requires
`Ed25519PublicKey.from_public_bytes`, which the accepted evidence does not
cover. Source created in this phase may reference it, but no later execution
phase may rely on JWK-based verification until a separately proposed and
reviewed bounded extension of the provider evidence exercises that API against
the pinned installation. A later execution controller must bind imports only
to the accepted installation at
`/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages`, verify
its accepted static and provider evidence first, and use an isolated interpreter.
That later controller and execution require separate review and PI authority.

## Review and stop rules

After creation, both blind gates must inspect every complete source and test
file before commit or execution. Stop if implementation requires guessing past
the accepted matrices, a new dependency, network access, an unreviewed parser or
algorithm, modification of accepted Stage 2 material, or any Step 4–9 behavior.

## Claim boundary and exclusions

This phase creates source and tests only. It establishes no functioning code or
conformance. It does not issue person, resource or auth tokens; approve a
mission; supervise an action; enforce a resource; integrate Freewallet or WAS;
admit a participant; expose a listener; access a network or external service;
or access Misty.

No import, native-code execution, compilation, lint, test, listener, dependency
operation, wallet/WAS work, QR flow, Misty access, physical actuation, G28 or
G29 is authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.
