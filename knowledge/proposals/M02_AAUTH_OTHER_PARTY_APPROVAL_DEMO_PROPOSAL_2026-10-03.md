# M02 AAuth Other-Party Approval Demo Proposal

Date: 2026-10-03  
Status: DRAFT — REVIEW REQUIRED; NO IMPLEMENTATION OR EXECUTION AUTHORIZED  
Repository basis: `main @ 1cb9e4460f494124aeacee78b0bfcddd285bdfa0`  
Protocol basis: bounded AAuth editor profile pinned to `fcf656d`  
Target milestone: Permission to Speak readiness by 2026-10-09

## Purpose

Add one bounded application-policy experiment to the accepted D-128 localhost
gateway:

> Holding agent, Deb authority, mission, participant, resource and requested
> action constant, does the next directed-action authorization change solely
> because a separately represented asserted-parent approval is active, absent
> or withdrawn?

The experiment must not represent a button click as verified parent identity,
verified relationship, legal authority, child assent or an AAuth Person. It
tests flow placement and fail-closed behavior, not legal sufficiency.

## Architectural placement

Preserve the accepted topology:

`agent -> resource requirement -> independent SOGA Person Server -> resource enforcement`

The resource owns a bounded application-level approval policy at the point of
action. The existing person-token, resource-token, PS/SOGA supervision and
auth-token sequence runs unchanged. At `/enforce`, the resource first verifies
the auth token and its existing subject, mission and scope bindings, then
evaluates the local other-party approval receipt for the participant named in
the signed action body.

- Active, exactly bound approval plus a valid AAuth chain allows the directed
  action.
- Absent, withdrawn, expired, malformed or wrongly bound approval returns a
  controlled application-level HTTP `403`; the action is not performed.
- Ambient actions do not require or consult other-party approval.
- Approval is necessary but never sufficient: SOGA denial or failure prevents
  auth-token issuance even when approval is active.

This stage deliberately does **not** emit AAuth `requirement=approval`.
The pinned `fcf656d` text at its approval-pending sections and published AAuth
`-11` section 11.6.4 require `Location`, `Retry-After`, a bounded pending
resource and polling to a terminal response. Those semantics are outside this
experiment. Section 11.6.4 approval “from another party” remains the candidate
placement the demonstration asks the protocol author about.

SOGA remains the Person Server's governance policy; this additive resource
policy is not Mockin Seam D and does not move SOGA. The approval receipt does
not overwrite Deb's authority state or masquerade as the AAuth Person.

## Exact action model

Use two exact test-only scopes:

- ambient: `misty.acknowledge_tip`;
- directed: `misty.address_participant`.

The additive enforcement surface must reject unknown scope spellings. The
directed test holds these
values constant across approval states:

- agent identifier and confirmation key;
- Deb's mission and authority inputs;
- `mission_s256`;
- resource and participant subject;
- requested directed scope;
- justification;
- clock and token lifetime.

Only the approval receipt state changes.

## Other-party approval receipt

Create `m02_aauth_fcf656d/other_party_approval.py` with an exact, immutable
test-profile receipt and policy. The receipt must carry:

- opaque `receipt_id`;
- `asserted_role` fixed to `parent`;
- `assurance` fixed to `unverified-demo-input`;
- exact participant subject;
- exact `mission_s256`;
- exact directed scope;
- state `APPROVED` or `WITHDRAWN`;
- `observed_at` and `expires_at` integer times; and
- non-empty local source label.

Validation must reject missing, extra, mistyped, empty, negative, reversed-time
or unknown values. The policy must use exact equality for participant, mission
and scope; require `observed_at <= now < expires_at`; treat no record,
withdrawal, expiry and any mismatch as not approved; and emit a bounded
decision receipt carrying policy version, separated input provenance, outcome
and reason without identity, token, key or signature material.

There is no approval HTTP endpoint in this stage. Tests install or withdraw a
receipt directly through the in-memory fixture before sending the next
authorization request. This prevents an unauthenticated network route from
becoming a disguised authorization switch. A real phone, wallet or UI input is
a later security boundary.

## Additive enforcement surface

Do not modify any accepted D-128 source. In
`m02_aauth_fcf656d/other_party_approval.py`, add:

- `ApprovalGovernedResource(Resource)`, which calls the accepted
  `Resource.enforce` first and then applies the other-party policy to the
  signed action body's exact `participant` and `scope`; and
- `ApprovalResourceSurface(ResourceSurface)`, which uses the governed resource
  for `/enforce`, returns the existing success response only when both AAuth
  enforcement and other-party policy allow, and otherwise returns controlled
  JSON `403 {"authorization":"denied",
  "reason":"other_party_approval_required"}`.

For directed actions the signed action body is an agent assertion, not proof of
participant identity. Exact matching against the resource-held receipt prevents
an approval for participant X from authorizing participant Y. The resource's
decision receipt must preserve that provenance distinction.

Withdrawal is re-evaluated at every directed `/enforce` call. It therefore
blocks use of a previously issued auth token for the next directed action,
without claiming the token itself was revoked. Ambient enforcement uses the
accepted AAuth checks but must not call the other-party policy; a sentinel test
must prove non-consultation.

The existing `requirement=auth-token` challenge, D-113 sources, token types,
token contents, signature profile, mission continuity, PS/SOGA supervision and
base enforcement logic remain byte-identical.

## Required tests

Create `tests/test_m02_aauth_other_party_approval.py` with exactly twelve test
methods covering:

1. exact receipt schema and type rejection;
2. unknown scope fail-closed;
3. ambient action proceeds with a sentinel policy that fails if consulted;
4. directed action with no receipt returns controlled application-level `403`;
5. wrong participant, mission or scope cannot satisfy the directed action;
6. active exactly bound approval plus SOGA ALLOW completes the unchanged
   four-hop exchange and directed enforcement;
7. active approval plus SOGA DENY, RESTRICT, malformed result or exception
   issues no auth token, proving approval is not sufficient;
8. withdrawal makes the next directed enforcement fail closed;
9. an auth token issued before withdrawal remains cryptographically valid but
   cannot pass the re-evaluated directed-action policy;
10. a cross-participant action using an otherwise valid token is denied;
11. expired and future-observed receipts fail closed; and
12. a single-variable comparison proves all listed constants are identical and
    only receipt state changes the next directed-action outcome.

Tests must also establish that decision receipts retain the explicit
`unverified-demo-input` assurance and separated source attribution. They must
not contain real names, personal data, child data, photographs, wallet data or
robot identifiers beyond the existing fictional Misty scope strings.

## Batched implementation and review sequence

After blind dual review and prospective PI authorization, create in one batch:

1. `m02_aauth_fcf656d/other_party_approval.py`;
2. `tests/test_m02_aauth_other_party_approval.py`; and
3. `tools/m02_aauth_fcf656d/run_other_party_approval_tests.py`.

The runner must pin every existing D-128 source/test hash plus the complete new
package, run the accepted 53-test regression suite followed by the exact twelve
new tests (65 total), use the accepted durable provider manifest, permit only
literal `127.0.0.1` ephemeral listeners, impose the existing 90-second and
2,000,000-byte per-stream limits, prohibit retry, verify pre/post immutability,
redact secrets and write once to a new absent durable directory:

`research-evidence/soga/executions/other-party-approval-v1`

Both blind gates review every complete source, test and runner in one static
round. Only after dual PASS, commit and prospective PI execution authority may
the exact runner execute once. Resulting evidence then receives blind dual
review before acceptance.

## Claim boundary

A positive result would establish only that this bounded additive
resource-enforcement fixture can make the next directed action depend on a
separately represented, exactly bound, explicitly unverified other-party
approval while preserving the accepted AAuth/SOGA flow. It would show the two
layers as an AND: AAuth/SOGA authorization is required, and resource-side
other-party policy may still refuse the action.

It would not establish:

- who the clicking person is;
- that the person is a parent, guardian or authorized representative;
- legal sufficiency, consent, assent or refusal precedence;
- continuous consent or cryptographic revocation of an already-issued token;
- conformance to AAuth's approval-pending polling protocol;
- published AAuth `-11` conformance beyond the bounded profile;
- a real QR, wallet, phone, presentation or Misty integration; or
- G28 or G29 readiness.

## Stop rules and exclusions

Stop on any attempt to represent the receipt as verified identity or legal
authority; merge it into Deb's authority state; add an unauthenticated approval
listener or route; emit `requirement=approval` without its required pending
protocol; allow a directed action with absent, withdrawn, expired or mismatched
state; consult approval for an ambient action; alter any accepted D-128 source,
token format or SOGA semantic; reuse prior evidence directories; access an
external service; or exceed any bound.

This proposal authorizes nothing by itself. No implementation, import,
compilation, lint, test, listener, execution, wallet/WAS operation, QR flow,
presentation integration, personal-data processing, Misty access, physical
action, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.
