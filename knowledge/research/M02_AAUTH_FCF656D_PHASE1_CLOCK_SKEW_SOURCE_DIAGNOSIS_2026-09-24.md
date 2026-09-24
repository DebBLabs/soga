# M02 AAuth `fcf656d` Phase 1 Clock-Skew Source Diagnosis

Date: 2026-09-24  
Status: SOURCE-ONLY DIAGNOSIS — NO CORRECTION OR EXECUTION AUTHORIZED

## Scope

This report diagnoses the single deterministic failure accepted under D-105:
`test_created_window_skew_and_replay` expected a `SignatureProfileError` for
`created=106`, `now=100`, but no exception was raised. The diagnosis used only
the committed implementation and test sources and the exact preserved AAuth
and HTTP Signature Keys sources. No source was modified, imported, compiled,
linted, tested or executed.

## Finding

The failing assertion is inconsistent with the pinned requirements and the
implemented profile. It is a test-fixture defect, not evidence of an
implementation defect.

- `m02_aauth_fcf656d/profile.py` defines both the freshness window and forward
  skew window as 60 seconds.
- `m02_aauth_fcf656d/http_signatures.py` raises `clock_skew` only when
  `created > now + 60`.
- AAuth `fcf656d`, Freshness and Replay, requires rejection with `clock_skew`
  only when `created` is further ahead than the validity window and sets the
  default window to 60 seconds.
- `draft-hardt-httpbis-signature-key-09`, Section 5.4.14, likewise defines
  `clock_skew` for a `created` value further ahead than the verifier's signature
  validity window.
- The test's `created=106`, `now=100` differs by six seconds. It is inside the
  60-second window and therefore must not raise `clock_skew`.

## Bounded corrective direction

A later, separately authorized correction should change the excessive-future
fixture to a value beyond the window. With the current strict `>` comparison,
`created=161`, `now=100` is the smallest integer case that must raise
`clock_skew`. The correction should also add or preserve an explicit boundary
case proving that `created=160`, `now=100` is accepted.

This report does not authorize that edit, any other source modification, or a
test retry. A correction and any execution require a separately reviewed
proposal and prospective PI authorization.

## Claim boundary

The diagnosis is limited to the accepted D-105 clock-skew failure. It does not
establish full AAuth conformance, a live token exchange, mission-hash
continuity, audience verification, supervision, resource enforcement, wallet
or WAS integration, QR admission, or Misty operation.

