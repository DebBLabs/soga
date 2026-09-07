# M02 AAuth Editor Delta — 2026-09-07

## Purpose and boundary

This read-only research note checks changes in the public AAuth editor repository
since the exact revision used by M02 Stage 1. It does not claim protocol
conformance, authorize implementation, activate a later M02 stage, or authorize
execution of any wallet, WAS, Posta, external, or robot service.

## Provenance and method

- Published reference remains `draft-hardt-oauth-aauth-protocol-10`.
- M02 Stage 1 editor baseline:
  `39a017d64c1a35dea6188e3fae71f4a3f3aa03e7`.
- Editor repository current revision checked:
  `b6ca19bad10f2a819d97782807fce448436a5866`.
- Repository: `https://github.com/dickhardt/AAuth`.

The comparison used the repository commit log, file statistics, full diffs of
all changed drafts, and targeted searches in a clean temporary clone. The
repository-wide delta contains four commits across the protocol, budgets, and
bootstrap drafts:

1. `04c528899e22cbdd222a57adb8be6da4204f6fc7` — changes four-party
   budget-ceiling omission from the resource's full offer to no budget grant.
2. `0a5044456b981f3eae14c6c9bcb3389427cc27cf` — editorial link-relation,
   environments, and pointer corrections (three insertions and three deletions).
3. `4ce6a6fd480a1572b650ec264ced81183fb22d40` — adds the many-agents,
   one-operator key layout and sub-agent token-acquisition patterns.
4. `b6ca19bad10f2a819d97782807fce448436a5866` — names the Supervisor role
   and adds an informative appendix describing a minimal Person Server.

The editor document still identifies its history as `-11`; this check found no
new `-12` revision label. Most person-token flow changes relevant to the earlier
M02 assessment predate the Stage 1 baseline and are therefore not new findings
in this delta.

## Material changes

### Affirmative Person Server budget ceiling

The budgets draft now says that, in four-party access, omission of the budget
parameter by the Person Server grants no budget claim. A Person Server granting
the resource's full offer must affirmatively echo that offer. This reverses the
prior omission behavior, which treated silence as the full ceiling. It is a
fail-closed semantic change relevant to any later budget integration, but M02
Stage 2 implements no budget extension and requires no runtime correction from
this change.

### Many agents under one operator and sub-agent bootstrap

The bootstrap draft now distinguishes a self-hosted domain's published Agent
Provider key from each agent's own token-bound signing key when one operator
runs several agents. It also describes two sub-agent acquisition patterns: a
self-hosted Agent Provider can mint the sub-agent token, while a hosted Agent
Provider can accept a request from an eligible top-level parent agent. The added
shape includes distinct subjects and confirmation keys and a `parent_agent`
relationship. This is directly relevant to the program's multi-agent identity
and delegation research, but it neither supplies participant-to-mission
admission nor authorizes adoption in M02 Stage 2.

### Supervisor

The draft now names a Supervisor: normally the Person, or a supervision server
to which the Person Server delegates. The Supervisor does not appear on the
wire, and the text says the wire protocol is unchanged. The draft references an
AAuth Supervision Protocol as companion work; no corresponding specification
file was present in the checked repository revision.

SOGA may be a candidate supervision service, but that is a hypothesis only.
This delta does not establish semantic compatibility, delegation semantics, or
an integration plan.

### Informative minimal Person Server

The new appendix is explicitly informative. It describes four required metadata
fields for the minimal profile: `issuer`, `jwks_uri`,
`person_token_endpoint`, and `auth_token_endpoint`. It describes a one-person
server, retained person tokens, a direct authorization-token endpoint,
out-of-band consent, and support for long waits. It does not require the full
mission, permission, audit, interaction, or control surfaces for that minimal
profile.

## Comparison with accepted M02 Stage 2

M02 Stage 2 is deliberately test-only and explicitly makes no AAuth-conformance
claim. Its local metadata endpoint and fields are profile-specific; its test key
metadata is not a public JWKS; and it uses test-only HMAC signing. The new
informative appendix therefore sharpens, but does not invalidate, the boundary
already stated by the implementation.

The Stage 2 proposal described Person Server metadata and a public verification
key document as a responsibility. The accepted implementation narrowed that to
test-only HMAC metadata and disclosed the difference. Independent review should
determine whether the canonical record states that proposal-to-implementation
narrowing clearly enough.

No runtime-code correction is required solely because of this editor delta.
Before any Stage 3 implementation or conformance claim, a later proposal must
explicitly decide whether to add protocol-shaped metadata, JWKS, person-token,
and authorization-token seams or retain a bounded nonconformant profile.

## Findings that remain open

- Participant admission is distinct from the reusable person-token lifecycle.
- Representative authority and affected-person assent or refusal are not made
  complete by the Supervisor naming change.
- SOGA-as-Supervisor is not adopted.
- No wallet composition, external exposure, production identity, or Misty
  access follows from this research.
