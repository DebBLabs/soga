# M02 AAuth `fcf656d` Phase 1 Acquisition and Matrix-Extension Proposal

Date: 2026-09-21
Status: PROPOSED — CREATE-ONLY ARTIFACT; NO ACQUISITION OR MATRIX EDIT AUTHORIZED
Prepared at: `main @ 7a34579`
Author/integrator: Codex
Review class: mandatory blind dual review under D-064 and B-044 controls

## Purpose

Prepare the two prerequisites for create-only implementation of the accepted
AAuth Steps 1–3 foundation:

1. acquire and independently verify the exact four-wheel Ed25519 dependency
   closure selected under D-087; and
2. extend the accepted Phase 0 normative matrix with exact, testable rules from
   RFC 9421, RFC 9530, RFC 9651, and
   `draft-hardt-httpbis-signature-key-09`.

This proposal separates acquisition from matrix creation and requires evidence
review at each boundary. It does not authorize either activity by its existence.

## Accepted basis

- D-085 accepts the Steps 1–3 implementation proposal at SHA-256
  `f8b7f3d7ffd19e517e893304a2ef68bc8c1f7f8a407bbb5b7881ce9f11643f91`.
- D-086 accepts the Phase 0 dependency record and normative matrix.
- D-087 accepts the dependency/reference selection report at SHA-256
  `dc6d1547dcc03fbac8acc3e38a6370a3406b6f11b3d7b07995bea33ec5cb105b`.
- The governing AAuth source remains editor's-copy commit
  `fcf656de1926535f5bd6fc0538147ead6646e727`; protocol SHA-256
  `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`.

## Phase A — exact-wheel acquisition and verification

### Fixed acquisition set

Acquire exactly these four artifacts from their immutable PyPI file URLs:

| Artifact | Exact SHA-256 | Exact size (bytes) | Immutable file URL |
|---|---|---:|---|
| `cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl` | `ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0` | 4,035,307 | `https://files.pythonhosted.org/packages/84/a9/ee16a903f13755e914d1eecc482fe64d1f10761c3960e5d8fa6837377aff/cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl` |
| `cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl` | `de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7` | 180,509 | `https://files.pythonhosted.org/packages/3d/de/38d9726324e127f727b4ecc376bc85e505bfe61ef130eaf3f290c6847dd4/cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl` |
| `pycparser-2.23-py3-none-any.whl` | `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934` | 118,140 | `https://files.pythonhosted.org/packages/a0/e3/59cd50310fc9b59512193629e1984c1f95e5c8ae6e5d8c69532ccc65a7fe/pycparser-2.23-py3-none-any.whl` |
| `typing_extensions-4.15.0-py3-none-any.whl` | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` | 44,614 | `https://files.pythonhosted.org/packages/18/67/36e9267722cc04a6b9f15c7f3441c2363321a3ea07da7ae0c0707beb2a9c/typing_extensions-4.15.0-py3-none-any.whl` |

The execution request must carry these four full URLs verbatim rather than
resolving package names or versions at run time.

### Acquisition controls

- Use a newly created fixed directory under `/private/tmp`, named prospectively
  in the execution authorization. Refuse a pre-existing nonempty target.
- Permit outbound HTTPS only to the four predeclared immutable file URLs. No
  index query, resolver, mirror, authentication, update check, advisory query,
  source archive, alternate wheel, redirect to an unapproved host, or retry is
  permitted.
- Download bytes only. Do not invoke `pip`, import a wheel, unpack it, install
  it, inspect executable/native contents, or execute package code.
- Apply finite connection and total-operation timeouts. Refuse a response whose
  declared or received length differs from the pinned size, and cap each read at
  its pinned size plus a small fixed margin named in the execution proposal.
- Compute each SHA-256 immediately after acquisition. A filename, byte-count,
  hash, host, HTTP result, start/end time, and exit status belong in evidence.
- Any redirect, missing artifact, size anomaly, hash mismatch, partial file,
  unexpected additional file, TLS/network error, or timeout stops the phase.
  There is no automatic retry or substitution.
- On failure, remove only artifacts that are incomplete or truncated. Retain a
  complete artifact that fails hash verification quarantined in place and
  labelled unverified, with its observed hash and size recorded; do not reuse,
  install or re-download it. Preserve the bounded diagnostic record in both
  cases. On success, preserve the exact directory read-only pending review.

### Phase A result and holdpoint

Phase A can establish only that the four selected distribution bytes were
retrieved from the authorized hosts and match their accepted hashes. It does not
establish installability, importability, runtime correctness, absence of
vulnerabilities, or AAuth conformance.

Create a standalone acquisition evidence report. Both blind reviewers must
verify the files and evidence before the PI may accept the result or authorize
installation. Matrix work does not depend on installation and may proceed only
if it was separately authorized in the same prospective decision.

## Phase B — normative-matrix extension

### Inputs

- accepted Phase 0 matrix
  `knowledge/research/M02_AAUTH_FCF656D_PHASE0_NORMATIVE_MATRIX_2026-09-20.md`;
- the pinned local AAuth checkout and protocol digest above; and
- exact local or freshly verified copies of RFC 9421, RFC 9530, RFC 9651 and
  Signature Keys `-09` whose source URLs and document identities are recorded.

Obtaining or refreshing any of these documents is network activity and requires
its own prospective authorization naming the exact URLs. Without that authority,
Phase B may proceed only against copies already held locally and hash-recorded.

If any normative document cannot be pinned exactly or conflicts materially with
the accepted AAuth source, stop and record the conflict; do not invent a wire
format or silently choose one source.

### Required matrix additions

For every row, record the normative source and section, requirement strength,
SOGA component, required positive/negative test, and implementation status.
Cover at least:

1. RFC 9421 signature-base construction; component identifier and parameter
   serialization; `Signature-Input`/`Signature` label correlation; `created`,
   `expires`, algorithm and key identifiers; duplicate, missing and malformed
   field rejection; and derived request components used by the AAuth profile.
2. RFC 9530 `Content-Digest` construction and verification over the received
   content, including malformed, unsupported, missing, altered and
   multiple-digest behavior applicable to the profile.
3. RFC 9651 types and canonical serialization used by all selected fields,
   including Dictionary/List/Item/Token/String/Byte Sequence parsing limits,
   duplicate handling and invalid-form rejection.
4. Signature Keys `-09` `jwt` and `jwks_uri` schemes; `alg` and `keyid`
   parameter requirements; selected-member behavior; algorithm determination;
   discovery admission/cache rules; `Signature-Error` grammar and codes; and
   label correlation with RFC 9421.
5. Cross-document precedence: identify each intentional AAuth specialization,
   every ambiguity, and every actual conflict. An unresolved conflict is a
   Phase 1 implementation holdpoint.
6. Identifier separation: JWT `kid`, resolved public-key thumbprint, HTTP
   signature `keyid`, and later resource-token `agent_jkt` must not be treated
   as interchangeable without an explicit reviewed rule.

The extension edits the matrix only. It creates no implementation, test file,
fixture, dependency environment, key material, listener, or executable source.

### Phase B result and holdpoint

Both blind reviewers must check the complete extended matrix directly against
the pinned normative texts. PI acceptance is required before the matrix becomes
an implementation input. Any Phase 1 source creation remains separately
authorized under the already accepted Steps 1–3 phase structure.

## Evidence and review package

The later execution package must contain:

- exact pre-execution SOGA HEAD and working-tree state;
- the prospective PI decision authorizing the precise phase(s);
- exact URLs, filenames, sizes and expected/observed hashes for Phase A;
- the complete redirect chain for every Phase A request, or an affirmative
  record that no redirect occurred;
- exact source identities and section references for Phase B;
- commands/actions, timestamps, exit states, stop-rule outcomes and network
  observations;
- before/after filesystem and repository status;
- confirmation that no dependency was installed, imported or executed; and
- an explicit claim boundary for each phase.

Review requests must be separately hash-pinned. Reviewers must not read peer
responses or coordination notes before posting and must disclose authorship,
cross-reading, network activity and repository modifications.

## Exclusions

This proposal does not authorize download, installation, extraction, import,
compilation, lint, test, implementation, listener, external runtime service,
Steps 4–9, Freewallet or WAS integration, QR flow, personal or production data,
payment, Misty access, physical actuation, G28 or G29. The unrelated PI
routine-tool proposal remains excluded and untouched.

## Required decisions

1. Both blind gates review this exact proposal.
2. The PI may reject it, request corrections, or accept it and authorize Phase
   A, Phase B, both, or neither.
3. Acquisition acceptance, installation, Phase 1 source creation and any later
   execution each remain separate prospective decisions.
