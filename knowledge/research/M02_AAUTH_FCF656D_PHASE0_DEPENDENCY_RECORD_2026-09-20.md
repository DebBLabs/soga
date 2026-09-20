# M02 AAuth `fcf656d` Phase 0 Dependency Record

Date: 2026-09-20
Status: PHASE 0 DRAFT — NOT YET INDEPENDENTLY REVIEWED
Authority: D-085, record-only; no acquisition, installation, import or execution
Author/integrator: Codex

## Decision sought

Select a maintained Python provider for the Ed25519 operations required by the
Steps 1–3 proposal. This record does **not** make that selection because D-085
prohibits network access and the local machine does not contain enough primary
evidence to verify an exact distributable artifact.

## Locally verified need

- AAuth commit `fcf656de1926535f5bd6fc0538147ead6646e727` requires every party
  to support the fully specified `Ed25519` algorithm and prohibits `EdDSA`,
  `none` and symmetric algorithms (`draft-hardt-oauth-aauth-protocol.md:2471,
  2501-2508`).
- The existing `m02_person_server` uses Python-standard-library HMAC and is
  explicitly test-only; it cannot satisfy that requirement.
- Under `/usr/bin/python3` 3.9.6, module discovery returned no installed
  `cryptography`, `nacl`, `jwcrypto`, `josepy` or `authlib` provider during the
  independent proposal review. The accepted proposal also independently
  established that neither `cryptography` nor `nacl` resolves.
- Python's standard library supplies no Ed25519 JWS implementation suitable for
  this profile. Runtime delegation to the `openssl` executable is explicitly
  excluded by the accepted proposal.

## Candidate, not selection

`cryptography` is the leading candidate because its public API is known to
provide Ed25519 key generation, signing, verification and public-key encoding.
That statement is a candidate capability hypothesis here, not a verified
artifact selection. No installed distribution, cached wheel, source archive,
lockfile entry or locally retained primary documentation was found in the
authorized local evidence.

The following facts remain unverified and therefore block selection:

| Required fact | Phase 0 result |
|---|---|
| Exact package and version | `cryptography`, version unresolved |
| Primary-source API documentation | Not locally available |
| Release provenance and maintenance status | Not locally verified |
| Python 3.9.6 and macOS arm64 compatibility | Not locally verified for an exact release |
| Distribution filename and SHA-256 | Not available locally |
| License text and exact release applicability | Not locally verified |
| Direct and transitive dependencies | Not resolved for an exact artifact |
| Native-code content | Expected to require explicit inspection; unresolved |
| Reproducible acquisition command and registry origin | Not authorized or established |

## Required acquisition research

A separately authorized, read-only network research step must use authoritative
project documentation and package-index metadata to identify one exact release,
then record:

1. canonical project and package-index URLs;
2. exact version and release date;
3. supported Python and platform versions;
4. exact macOS arm64 distribution filename and SHA-256, or the exact source
   distribution if no acceptable wheel exists;
5. license identifier and the license text shipped by that release;
6. all required direct and transitive distributions and their hashes;
7. whether any artifact contains native code and what build/runtime libraries
   it embeds or requires;
8. the minimal APIs used for Ed25519 generation, raw sign/verify and public JWK
   serialization inputs; and
9. known security advisories or compatibility constraints material to the
   selected release.

Acquisition must then receive its own prospective authorization naming the
exact artifact, registry traffic and destination environment. A dependency
record alone must never trigger an install.

## Stop condition and result

Phase 0 dependency selection is **INCOMPLETE BY AUTHORIZED BOUNDARY**. The local
evidence proves that an Ed25519 provider is necessary and absent; it does not
support choosing an exact package artifact. Stop before network research,
download, installation, import or implementation.

This is a useful gated result rather than a failure: it prevents an implicit
dependency choice from entering the conformance foundation.

