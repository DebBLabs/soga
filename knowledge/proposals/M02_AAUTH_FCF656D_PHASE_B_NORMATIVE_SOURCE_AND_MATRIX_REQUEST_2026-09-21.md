# M02 AAuth `fcf656d` Phase B Normative-Source and Matrix Request

Date: 2026-09-21
Status: DRAFT REQUEST — NOT AUTHORIZED FOR RETRIEVAL OR MATRIX EDIT
Prepared at: `main @ 1694e9a`
Authority to create: D-088
Author/integrator: Codex
Review class: mandatory blind dual review

## Purpose

Request two sequential, separately held activities: retrieve and identify exact
normative source documents, then extend the accepted Phase 0 matrix from only
those reviewed local copies. The B0 evidence review and PI acceptance must occur
before B1 matrix editing.

## Phase B0 — exact-source retrieval request

Request one retrieval attempt for exactly:

| Document | Exact URL |
|---|---|
| RFC 9421 | `https://www.rfc-editor.org/rfc/rfc9421.txt` |
| RFC 9530 | `https://www.rfc-editor.org/rfc/rfc9530.txt` |
| RFC 9651 | `https://www.rfc-editor.org/rfc/rfc9651.txt` |
| HTTP Signature Keys `-09` | `https://www.ietf.org/archive/id/draft-hardt-httpbis-signature-key-09.txt` |

The future execution authorization must name a new fixed owner-only target under
`/private/tmp` and a create-then-review controller. The controller must permit
only one GET of each exact URL; refuse every redirect, including a same-host
redirect; use a 15-second connection timeout, a 120-second total timeout per
document, and a maximum response body of 2,097,152 bytes per document; and make
no index/search query, alternate-format request, latest-version resolution,
mirror request, authentication request, retry, or substitution. A missing
`Content-Length` is permitted only under the received-byte cap; a declared or
received length over the cap is a stop condition.

For each response, evidence must record exact URL, final host, redirect chain or
affirmative no-redirect result, status, byte size, computed SHA-256, retrieval
time, document title/identifier, and internal publication/date markers. A title,
identifier or revision mismatch is a stop condition. Retrieved documents remain
research inputs, not accepted normative inputs, until both blind reviews and PI
acceptance of the B0 evidence.

The SHA-256 values accepted from B0 become the mandatory document pins for B1.
B1 must recompute and match all four hashes before reading or using the files.

## Phase B1 — matrix extension request

Only after B0 acceptance, request creation of a new extension artifact:

`knowledge/research/M02_AAUTH_FCF656D_PHASE1_NORMATIVE_MATRIX_EXTENSION_2026-09-21.md`

The extension must cite and preserve, without modification, the accepted Phase
0 matrix at
`knowledge/research/M02_AAUTH_FCF656D_PHASE0_NORMATIVE_MATRIX_2026-09-20.md`,
SHA-256
`2dc6a6e45e353113a56b4f318ca143f10024c5dbbb2332ac9087fe69dad0e003`,
and state that it extends rather than replaces that record.

The edit must use the accepted local documents and AAuth commit
`fcf656de1926535f5bd6fc0538147ead6646e727` only. Each added row must identify
the exact source section, requirement strength, SOGA component, required
positive/negative test and implementation status.

The extension must cover the six areas enumerated in the D-088 proposal:
RFC 9421 signature construction and verification; RFC 9530 Content-Digest;
RFC 9651 parsing and canonical serialization; Signature Keys `-09` schemes,
`alg`, `keyid`, discovery, errors and label correlation; cross-document
specialization/conflict; and separation of JWT `kid`, public-key thumbprint,
HTTP-signature `keyid`, and later `agent_jkt`.

Any unresolved normative conflict is recorded as a Phase 1 implementation
holdpoint. Do not invent a wire representation or silently choose precedence.
The completed matrix requires both blind reviews and PI acceptance before it is
an implementation input.

## Claim boundary and exclusions

B0 success would prove only exact retrieval and identity of four normative
documents. B1 success would prove only that a reviewed requirements matrix was
derived from those documents and the pinned AAuth source. Neither proves an
implementation or conformance.

This request does not authorize itself. It authorizes no retrieval, matrix edit,
wheel operation, dependency installation, import, implementation, compilation,
test, listener, Steps 4–9, wallet/WAS work, personal data, payment, Misty access,
physical actuation, G28 or G29. The unrelated PI routine-tool proposal remains
excluded and untouched.
