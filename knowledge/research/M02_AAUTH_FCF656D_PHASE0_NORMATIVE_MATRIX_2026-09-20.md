# M02 AAuth `fcf656d` Phase 0 Normative Requirements Matrix

Date: 2026-09-20
Status: PHASE 0 DRAFT — NOT YET INDEPENDENTLY REVIEWED
Authority: D-085, record-only; no implementation or execution
Author/integrator: Codex

## Source identity and scope

- Checkout: `/private/tmp/aauth-fcf656d-20260920`
- Commit: `fcf656de1926535f5bd6fc0538147ead6646e727`
- Protocol SHA-256:
  `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`
- Matrix scope: accepted proposal Steps 1–3 only—source pinning, JOSE/JWKS
  primitives, signed-agent request verification and truthful interim metadata.

Line references below refer to
`draft-hardt-oauth-aauth-protocol.md` at that exact commit. Normative force is
copied as MUST, MUST NOT, SHOULD, SHOULD NOT or MAY; a SOGA choice is labelled
separately and is not attributed to the draft.

## Token and key requirements

| ID | Requirement | Force | Source | Planned assertion |
|---|---|---:|---|---|
| J-01 | Every AAuth party supports fully specified `Ed25519`. | MUST | 2501 | Provider signs and verifies Ed25519 vectors. |
| J-02 | `ES256` support is additional, not required for this first profile. | SHOULD | 2501 | Explicitly out of the first implementation; no claim of support. |
| J-03 | AAuth JWT header `alg` is fully specified; `Ed25519` is recommended. | REQUIRED/SHOULD | 2471 | Require exact `Ed25519`. |
| J-04 | Reject `none`, polymorphic `EdDSA`, and symmetric algorithms. | MUST NOT accept | 2471, 2506-2507 | Negative vectors for each class. |
| J-05 | Each conveyed, referenced or selected JWK carries fully specified `alg`; reject absent `alg`. | MUST | 2482, 2505, 2635 | Publication and verification tests. |
| J-06 | Reject a key whose `kty` or present `crv` disagrees with `alg`. | MUST | 2508 | Mismatch vectors. |
| J-07 | JWT `typ` is `aa-<type>+jwt` and is checked before acting. | MUST | 2472 | Exact allowed types and cross-type rejection. |
| J-08 | JWT header `kid` identifies the issuer signing key in JWKS. | structural | 2473 | Nonempty `kid`; exact selected-key lookup. |
| J-09 | Select the key matching `kid` without requiring unselected JWKS members to be usable. | MUST/MUST NOT | 2637 | Mixed-JWKS vector with unsupported unselected key. |
| J-10 | A selected public JWK contains no private `d` member. | SOGA safety rule | proposal | Reject publication or fixture containing `d`. |
| J-11 | Private test keys remain in memory and out of logs, SQLite and fixtures. | SOGA safety rule | proposal | Static review plus output/fixture checks. |

## HTTP Message Signature requirements

| ID | Requirement | Force | Source | Planned assertion |
|---|---|---:|---|---|
| H-01 | Cover `@method`, `@authority`, `@path`, and `signature-key`. | MUST | 2551-2558 | Each missing/duplicated/altered component fails. |
| H-02 | Body requests to PS or AS endpoints additionally cover `content-digest` and `content-type`. | MUST | 2560-2565 | Digest verified before JSON use; altered body/type fails. |
| H-03 | `Signature-Input` contains integer Unix-time `created`; signer sets current time. | MUST | 2583-2585 | Missing/noninteger values fail. |
| H-04 | Agent omits the HTTP signature `alg` parameter; verifier ignores it if present and derives algorithm from the resolved key. | MUST NOT/MUST | 2587, 2600 | Signer omission and malicious wire `alg` ignored. |
| H-05 | Agent normally omits `keyid`; if present with the same label as `Signature-Key`, both identify the same key and the verifier uses `Signature-Key`. | SHOULD NOT/MUST | 2589 | Mismatch fails; matching value does not override key source. |
| H-06 | Require `Signature`, `Signature-Input`, and `Signature-Key`. | MUST | 2593-2595 | Missing header returns signature failure. |
| H-07 | Reject missing required coverage with `invalid_input` and `required_input`. | MUST | 2596 | Error mapping test. |
| H-08 | Verify `created` within the server window; default 60 seconds. Old gives `invalid_signature`, excessive future skew gives `clock_skew`. | MUST/MAY default | 2597, 2835 | Boundary and distinct-error tests. |
| H-09 | Unsupported/unregistered Signature-Key schemes fail uniformly; AAuth agent requests use `jwt`, not `jwks_uri` or `hwk`. | MUST/MUST NOT | 2516, 2598, 2613-2621 | Scheme rejection tests. |
| H-10 | `expires` is optional but honored and rejected when past if present. | OPTIONAL/MUST | 2625 | Present-expired vector. |
| H-11 | A within-window replay cache may use `(signing-key-thumbprint, created, @method, @authority, @path)`; no nonce is defined. | MAY | 2627 | Adopted as stricter SOGA policy for state-changing requests. |
| H-12 | For delayed verification, cache duration spans accepted signing-to-verification skew. | MUST if used | 2629 | Deferred until delayed-artifact behavior exists. |

## Key discovery and metadata requirements

| ID | Requirement | Force | Source | Planned disposition |
|---|---|---:|---|---|
| M-01 | Token verification discovers issuer JWKS through `{iss}/.well-known/{dwk}`. | profile rule | 2488, 2633 | Define shape; no network fetch in Steps 1–3 tests. |
| M-02 | JWKS responses are cached; unknown `kid` may refresh, with no issuer fetched more than once per minute; cached entries normally expire within 24 hours. | MUST/SHOULD/MUST NOT | 2639-2641 | Design requirement; runtime fetching remains outside current execution scope. |
| M-03 | Egress admission precedes issuer metadata or JWKS fetching. | MUST | 2643 | Stop rule for any later live discovery. |
| M-04 | Endpoint and `jwks_uri` metadata URLs use HTTPS under the protocol profile. | MUST | 2674 | Interim literal-loopback test metadata must not claim conformance. |
| M-05 | A conformant PS metadata floor is `issuer`, `auth_token_endpoint`, `person_token_endpoint`, and `jwks_uri`. | REQUIRED | 2748-2774 | Do not claim this floor before both endpoints exist. |
| M-06 | Interim metadata may truthfully publish local issuer/JWKS information but remains explicitly test-only/nonconformant. | SOGA truthfulness rule | D-084/D-085 | Regression test against false floor claim. |

## Identifier distinctions

| Identifier | Meaning in this phase | Must not be conflated with |
|---|---|---|
| JWT header `kid` | Selects the issuer signing key in JWKS (2473). | A thumbprint or `agent_jkt` unless a later profile explicitly makes that choice. |
| Signing-key thumbprint | Derived replay-cache key component (2627). | JWT `kid`. |
| `agent_jkt` | Resource-token binding claim, introduced in later Step 6. | Any Steps 1–3 key identifier. |
| HTTP signature `keyid` parameter | Normally omitted; when present must agree with `Signature-Key` and never selects a different key (2589). | JWT header `kid`. |

## Exact failure ordering retained for implementation design

The verifier extracts all three signature headers, checks required coverage and
freshness, resolves the `Signature-Key` scheme/key, obtains the algorithm from
that resolved key, validates algorithm/key consistency, and only then verifies
the signature (2593-2603). AAuth maps signature failures to `401`; an authorized-
identity request denied after successful signature verification is `403` and
must not carry signature-negotiation headers (2607-2609).

## Phase 0 result and remaining holdpoints

This matrix supplies the Steps 1–3 normative baseline, including the two items
identified during proposal review: the HTTP signature `alg` parameter is ignored
by verifiers, and `keyid` cannot override `Signature-Key`.

It does not resolve the detailed structured-field serialization rules from RFC
9421, Content-Digest construction from RFC 9530, or the `Signature-Key` scheme
grammar in the referenced HTTP Signature Keys draft. Before Phase 1 source is
created, the reviewed dependency/source profile must either pin those normative
references and incorporate their exact requirements or stop rather than invent
wire syntax. No implementation or execution is authorized by this matrix.

