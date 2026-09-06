# M02 Stage 2 Bounded Local Person Server — Implementation Evidence

Date: 2026-09-06
Status: READY FOR INDEPENDENT IMPLEMENTATION REVIEW
Authorization: D-036
Implementation base: `2debcd10db5b6a7082b04d339b2bb2967cd6de5b`

## Implemented boundary

Stage 2 adds `m02_person_server`, a test-only local Person Server slice with:

- a literal-loopback HTTP surface on an OS-assigned port;
- SQLite persistence for test signing keys, agents, missions, person tokens,
  authenticated request identifiers, pending permissions, and audit events;
- signed and retained local person tokens bound to issuer, audience, mission,
  subject, lifetime, identifier, and agent confirmation key;
- HMAC-authenticated test-agent permission requests and pending polls;
- server-owned policy limits and retained live expiry/revocation state;
- per-action SOGA evaluation with the complete decision retained separately
  from its AAuth-shaped projection;
- bounded pending approval/decline, exact evidence binding, expiry,
  reevaluation, and terminal delivery; and
- operator-authenticated setup and mutation fixtures confined to `/_test/`.

The HMAC credentials and key metadata are explicitly test-only. They are not a
public-key JWKS, production identity system, or AAuth conformance claim.

## B-038 partial repair

`evaluate_aauth_execution_request` now accepts an internal-only
`verified_authority_state` parameter. The Stage 2 Person Server builds it from
its verified and retained token record after checking the signed request and
token bindings. The public request cannot provide this state or its limits.

The previous hardcoded behavior remains only for pre-M02 compatibility callers
and is not used by the Stage 2 path. Expiry, revocation, elapsed token age,
issuer, audience, mission, agent, and token identity are live on the selected
profile. Delegation depth and attenuation remain explicitly unavailable; a
mission requiring either fails closed. B-038 therefore remains open beyond
this profile.

## Corrections made during implementation

Before tests were accepted, review of the developing code rejected:

1. caller-supplied `runtime_authority` as a trust source;
2. unknown delegation and attenuation facts represented as known-safe values;
3. caller-selected authority policy limits;
4. administrative routes outside the `/_test/` namespace;
5. unauthenticated pending-state reads;
6. rejection of byte-equivalent retries instead of idempotent reuse; and
7. approval evidence that was not bound to the original pending request.

The final implementation contains the corrected behavior and named regression
tests for these boundaries.

## Test evidence

Focused command, run with permission to bind test-owned literal-loopback ports:

    python3 -m unittest tests.test_m02_person_server -v

Initial gate result: **38 tests passed** in 6.135 seconds.

Complete repository command, run with the same local-loopback permission:

    python3 -m unittest discover -s tests -p 'test_*.py' -v

Initial gate result: **126 tests passed** in 19.363 seconds.

Claude Gate 1 and Gemini/AGy Gate 2 independently returned PASS on that
implementation. Before acceptance, three Gate 1 hardening recommendations were
taken: actual terminal permission delivery through authenticated polling is now
atomic and single-use; unavailable-required authority facts fail closed in the
bridge itself as well as the Person Server; and optional subject comparison is
explicit. The resulting test exposed and corrected an initial-path subject
binding gap: when `subject.person_id` is present, it must equal the verified
person-token subject before SOGA evaluation.

Final corrected focused result after taking both recheck coverage
recommendations: **44 tests passed** in 6.644 seconds.

Final corrected complete result: **132 tests passed** in 20.393 seconds.

The 44 Stage 2 tests include named controls for signature alteration, issuer,
audience, agent confirmation, mission and action binding, future issuance,
expiry, revocation, late approval, exact approval binding, reevaluation rather
than direct grant, byte-equivalent idempotency, conflicting reuse, concurrent
permission and revocation, SQLite restart, audit secret exclusion, unsupported
authority facts, central bridge fail-closed behavior, subject-token binding,
single-use terminal permission delivery, magic-header rejection, parsing and
size limits, authenticated polling, `/_test/` route isolation, unsupported
methods/routes, and real loopback traversal into SOGA.

The final two tests independently exercise the reevaluation-path subject
comparison after retained-state inconsistency and the terminal-result-once-then-
410 lifecycle across real loopback HTTP. They implement the only two
nonblocking coverage recommendations from the hardening recheck; no production
code changed afterward.

The terminal walkthrough initially caused the package-isolation test to fail
because its explanatory banner named the prohibited robot-specific boundary.
The banner now says generic `robot access`. The subsequent full run exposed a
schedule-dependent test assumption: concurrent byte-identical callers may
either observe `still being evaluated` or receive the same completed result.
The assertion now permits both while requiring one SOGA decision and no
divergent result. That concurrency test passed 25 consecutive stress runs
before the final focused and complete suites above.

## Nonclaims

No wallet, WAS, or Posta service was run or imported. No related dependency was
installed. No endpoint was exposed beyond literal loopback. No production key,
credential, or personal identity was used. No participant-session,
representative-authority, or affected-person policy was implemented. No R3
behavior was adopted. No resource execution surface, physical-success result,
Misty access, actuation, or G28 activation exists in this package.

This evidence does not accept or close Stage 2. Independent forward and reverse
implementation reviews were completed, and the PI accepted Stage 2 under
D-037. A narrow review of the subsequently added visible terminal walkthrough
remains required before commit.
