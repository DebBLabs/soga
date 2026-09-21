# M02 AAuth `fcf656d` Phase 1 Normative Matrix Extension

Date: 2026-09-21
Status: CREATE-ONLY DRAFT — NOT YET INDEPENDENTLY REVIEWED
Authority: D-091
Author/integrator: Codex

## Relationship to the accepted baseline

This artifact extends, and does not replace or modify,
`knowledge/research/M02_AAUTH_FCF656D_PHASE0_NORMATIVE_MATRIX_2026-09-20.md`
at accepted SHA-256
`2dc6a6e45e353113a56b4f318ca143f10024c5dbbb2332ac9087fe69dad0e003`.
The AAuth profile remains pinned to commit
`fcf656de1926535f5bd6fc0538147ead6646e727` and protocol SHA-256
`295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`.

## Pinned companion inputs

| Source | Preserved path | Accepted SHA-256 |
|---|---|---|
| RFC 9421 | `/private/tmp/m02-aauth-fcf656d-phase-b0-20260921/sources/rfc9421.txt` | `612655786bf4293bfc486e4177571467fbb3de6e6f0eea90cb74c346a34fdf3c` |
| RFC 9530 | `/private/tmp/m02-aauth-fcf656d-phase-b0-20260921/sources/rfc9530.txt` | `544dbb7d9afceafa8c9931d9924ca6cff2b4807274166d7ed2483342ef2cdd6a` |
| RFC 9651 | `/private/tmp/m02-aauth-fcf656d-phase-b0-20260921/sources/rfc9651.txt` | `fe27f2ec8819911afbe4bd11f6fcb947580da4c49e5423a1fff960e252ced26d` |
| HTTP Signature Keys | `/private/tmp/m02-aauth-fcf656d-phase-b0-20260921/sources/draft-hardt-httpbis-signature-key-09.txt` | `b5e8602e217bbccd254b93419d0b54ec2b2a6cdce38351983624718029528a5d` |

All four hashes must be recomputed before these rows are used. A mismatch stops
work. Section references below refer to these exact documents.

## RFC 9421 — HTTP Message Signatures

| ID | Requirement | Force | Source | Component / required assertion | Status |
|---|---|---:|---|---|---|
| R94-01 | Build the signature base from the ordered covered-component identifiers and their canonical values, followed by `@signature-params`. | MUST | §§2, 2.5 | HTTP signer/verifier; fixed positive vectors and altered-order/value negatives. | Planned, unimplemented |
| R94-02 | Treat component identifiers and their parameters as Structured Fields and preserve the exact order serialized in `Signature-Input`. | MUST | §§2.1, 2.3, 4.1 | Reject duplicate/missing required coverage and noncanonical or malformed parameter forms. | Planned, unimplemented |
| R94-03 | Canonicalize repeated HTTP field lines using the specified combination algorithm unless strict Structured Field serialization applies. | MUST | §2.1 | Multi-line and whitespace transformation vectors. | Planned, unimplemented |
| R94-04 | A signer MAY add the `sf` component parameter; only when it is present MUST the field value use strict Structured Field serialization. AAuth `fcf656d` does not select `sf`, so adopting it is an unresolved SOGA profile decision and implementation holdpoint. | MAY; conditional MUST | §2.1.1 | Do not presume `sf`; if later selected, add strict-serialization positive/negative vectors for each selected field. | Holdpoint |
| R94-05 | Derive `@method`, `@authority`, and `@path` from the received request rather than trusting supplied application values. | MUST | §§2.2.1, 2.2.3, 2.2.6 | Alter each received request component and require failure. | Planned, unimplemented |
| R94-06 | Parse `created` and optional `expires` as signature parameters; apply the AAuth freshness/error profile from baseline H-03/H-08/H-10. | MUST/profile | §§2.3, 3.2; AAuth | Missing, noninteger, old, future-skew and expired vectors. | Planned, unimplemented |
| R94-07 | Correlate a chosen label across `Signature-Input` and `Signature`; absence, ambiguity or malformed Byte Sequence fails. | MUST | §§4.1, 4.2 | Label mismatch, duplicate-label and malformed signature vectors. | Planned, unimplemented |
| R94-08 | Do not treat RFC 9421 `alg` or `keyid` as authoritative where AAuth explicitly derives the algorithm and key through `Signature-Key`. | AAuth specialization | RFC §§2.3, 3.3; AAuth baseline H-04/H-05 | Wire `alg` ignored; `keyid` cannot override resolved key. | Planned, unimplemented |

## RFC 9530 — Content-Digest

| ID | Requirement | Force | Source | Component / required assertion | Status |
|---|---|---:|---|---|---|
| R95-01 | Construct `Content-Digest` over the HTTP message content bytes, not the decoded representation, using a registered algorithm key and Byte Sequence value. | MUST | §§2, 5 | Body signer; known SHA-256 vectors. | Planned, unimplemented |
| R95-02 | For the initial SOGA profile, emit and require `sha-256`; unsupported or deprecated-only digest choices do not satisfy the profile. | SOGA selection | §§2, 5–6; AAuth H-02 | Missing/unsupported/weak-only algorithm negatives. | Planned, unimplemented |
| R95-03 | Parse the field as an RFC 9651 Dictionary and verify the selected digest before consuming JSON or trusting the body. | MUST/profile | §2; AAuth H-02 | Malformed field, altered body and valid-digest/invalid-JSON ordering tests. | Planned, unimplemented |
| R95-04 | Multiple digest algorithms do not permit a weak or bad member to satisfy required `sha-256`. SOGA's stricter duplicate-key rejection rule R96-04 prevents RFC 9651 last-wins duplicate `sha-256` members from hiding an earlier value. | SOGA safety rule/profile | §§2, 6.6; RFC 9651 §§4.2.2, 4.2.3.2 | Multiple-member, duplicate and conflicting-value negatives. | Planned, unimplemented |
| R95-05 | A trailer-only digest does not satisfy this bounded request profile unless a later reviewed transport profile explicitly supports trailers. | SOGA boundary | §2; proposal | Reject missing header digest; no trailer claim. | Planned, unimplemented |

## RFC 9651 — Structured Fields

| ID | Requirement | Force | Source | Component / required assertion | Status |
|---|---|---:|---|---|---|
| R96-01 | Parse and serialize Dictionary, List, Inner List, Item and Parameters using the exact algorithms; any algorithm failure fails the field. | MUST | §§3, 4 | Shared bounded parser/serializer; official examples and malformed corpus. | Planned, unimplemented |
| R96-02 | Support only the bare-item types required here: Integer, String, Token, Byte Sequence and Boolean; reject out-of-range, invalid-character and invalid-base64 forms. | MUST | §§3.3.1, 3.3.3–3.3.6, 4.2 | Per-type boundary and rejection vectors. | Planned, unimplemented |
| R96-03 | Serialize keys, parameters and members canonically, preserving defined order and lowercase key constraints. | MUST | §§4.1.1–4.1.3 | Round-trip canonical vectors and altered serialization negatives. | Planned, unimplemented |
| R96-04 | RFC parsing uses last-wins for duplicate dictionary keys and parameters. SOGA deliberately rejects duplicates as a stricter anti-smuggling safety rule. Independently, trailing/unconsumed input fails parsing. | SOGA safety rule; trailing-input MUST | §§4.2, 4.2.2, 4.2.3.2 | Duplicate-key/parameter and trailing-garbage negatives; do not claim duplicate rejection as RFC conformance. | Planned, unimplemented |
| R96-05 | Enforce explicit input, member-count, nesting and byte-size limits stricter than the protocol maxima before allocation. | SOGA safety rule | RFC §6; proposal | Oversized dictionary/list/string/bytes inputs fail boundedly. | Planned, unimplemented |

## HTTP Signature Keys `-09`

| ID | Requirement | Force | Source | Component / required assertion | Status |
|---|---|---:|---|---|---|
| SK-01 | Parse `Signature-Key` as a Structured Fields Dictionary keyed by signature label and select the member matching the label being verified. | MUST | §§3, 3.1 | Missing, extra, mismatched and multiple-label vectors. | Planned, unimplemented |
| SK-02 | For AAuth agent requests, require the `jwt` scheme; unsupported or unregistered schemes produce the specified uniform error and are not probed. | AAuth specialization/MUST | §§3, 3.5, 5.4.2; AAuth H-09 | `hwk`, `jwks`, `jwks_uri`, unknown scheme negatives. | Planned, unimplemented |
| SK-03 | Validate the `jwt` scheme's required parameters and assertion before using its claims or resolved key. | MUST | §3.5 | Missing/malformed/invalid assertion and key-binding vectors. | Planned, unimplemented |
| SK-04 | Where `jwks_uri` is later used, validate its required identifier, discovery-key and key-id members, apply HTTPS/egress admission, and cache under reviewed limits. | MUST/later phase | §3.6; baseline M-02–M-04 | Recorded future requirement; no Steps 1–3 live fetch. | Deferred |
| SK-05 | Determine the JOSE signing algorithm only from the selected JWK's fully specified `alg`; reject absent, polymorphic, unsupported, symmetric or key-inconsistent algorithms. | MUST | §3.3 | Baseline J-03–J-06 negative vectors. | Planned, unimplemented |
| SK-06 | Do not use the RFC 9421 `alg` signature parameter for JOSE signing algorithms under this profile. | MUST | §3.3; AAuth H-04 | Signer omits; verifier ignores malicious value. | Planned, unimplemented |
| SK-07 | Parse `Accept-Signature-Scheme` and `Accept-Signature-Alg` only as negotiation feedback; never broaden local trust or algorithm policy from peer advertisement. | MUST/SOGA boundary | §4 | Unsupported negotiation and downgrade vectors. | Planned, unimplemented |
| SK-08 | Emit/parse `Signature-Error` with its Structured Fields grammar and map `unsupported_algorithm`, `unsupported_scheme`, `invalid_input`, `required_input`, `invalid_signature`, and `clock_skew` without leaking key-validation detail. | MUST/profile | §5, §§5.3–5.4 | Exact error-code/status/header vectors. | Planned, unimplemented |
| SK-09 | Honor cache directives only in a later reviewed discovery implementation; cache state cannot bypass issuer/egress/key validation. | MUST/later phase | §6; baseline M-02/M-03 | Deferred design requirement. | Deferred |

## Cross-document precedence and identifier separation

1. AAuth `fcf656d` controls where it intentionally specializes the companion
   specifications: required covered components, `jwt` scheme, freshness window,
   omission/ignoring of HTTP-signature `alg`, and constrained `keyid` behavior.
2. RFC 9421 controls signature-base construction and general verification
   mechanics; RFC 9530 controls digest meaning; RFC 9651 controls Structured
   Field grammar; Signature Keys `-09` controls key-conveyance schemes and
   related negotiation/errors.
3. No material conflict was identified for Steps 1–3. Any implementation-time
   ambiguity or newly discovered conflict is a stop condition requiring review.
4. JWT header `kid` selects an issuer JWK. HTTP-signature `keyid` is normally
   omitted and cannot override `Signature-Key`. A resolved public-key thumbprint
   is only the SOGA replay-cache identifier. Later `agent_jkt` is a resource-token
   claim. The four values are not interchangeable.

## Claim boundary

This matrix is a requirements artifact, not implementation evidence. It creates
no source code, tests, parser, key, token, listener or conformance claim. It must
receive blind dual review and PI acceptance before Phase 1 source creation.
