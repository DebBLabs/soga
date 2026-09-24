# M02 AAuth `fcf656d` Phase 1 Focused-Test Execution Evidence

Date: 2026-09-24
Execution commit: `a2f18a55efa7c56ec6b773fa636df13d0824a0b6`
Review: request 055, blind Gate 1 PASS and blind Gate 2 PASS
Result: gated negative; single D-104 attempt consumed

## Accepted result

The exact committed Steps 1–3 package ran once under the pinned Python 3.9.6
and `cryptography 50.0.1` environment. Twenty-four focused tests ran: 23 passed
and one failed. There were no errors, skips, expected failures or unexpected
successes.

The sole failure was
`HttpSignatureTests.test_created_window_skew_and_replay`. The test signed a
request with `created=106`, verified it with `now=100`, and expected
`SignatureProfileError`; no exception was raised. The evidence therefore
supports a bounded source-only diagnosis of the clock-skew expectation and
implementation. It does not authorize correction or another execution.

## Exact evidence

Preserved temporary directory:
`/private/tmp/m02-aauth-fcf656d-phase1-tests-20260922`

- `phase1-test-evidence.json` — 5,490 bytes, SHA-256
  `3f00c0037f528d0f33cbed1faec55e10a97fc8778e7242218d6ffcaf1010c9e7`;
- `phase1-test-stderr.bin` — 110 bytes, SHA-256
  `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`;
- `run-record.json` — 6,174 bytes, SHA-256
  `57b7695589d059aaf796b0ba03a3d438d0e2408c206e15e3d8111042243f8724`.

The controller SHA-256 was
`177b4f1231fb30ca053308a4dbfb726c05cdc5b917d6ed614a83c1c817ac4303`.
The run record binds the exact controller and seven package/test blobs, records
one isolated child invocation, reports no timeout, and preserves both streams.
The stderr is the exact pinned macOS `confstr()` diagnostic.

## Verified execution properties

- The AST count, loaded suite count, executed count and report count all equal
  24.
- The evidence identifies all 24 committed tests: 23 `ok` and one `FAIL`.
- All provider module origins resolve beneath the pinned provider root and all
  candidate module origins resolve beneath the exact package root.
- The 223-entry installation inventory, four wheel identities and D-099/D-102
  provider evidence were unchanged before and after execution.
- All seven committed package/test blobs and the controller were unchanged.
- The report contains no compact JWS, JWK coordinate or HTTP-signature header
  material. The sensitive-value redaction paths were not exercised by this
  particular failure and therefore remain statically reviewed but empirically
  unproved.
- No retry occurred.

## Passing boundary

The run positively exercised the encoded profile, Structured Fields, JOSE,
metadata and most HTTP Message Signature behavior. In particular, the
cross-token-type test passed: a person token was rejected when the verifier
expected an auth token. This is verifier-layer behavior only; no endpoint yet
requires or issues an auth token.

## Claim boundary

This evidence does not establish complete AAuth `-11` conformance, a real
person/resource/auth token exchange, `mission_s256` continuity, audience
checking, supervision, resource enforcement, external interoperability or a
Misty demonstration. It establishes only that the exact committed Steps 1–3
package passed 23 of its 24 encoded focused tests and failed deterministically
at the named future-timestamp assertion.
