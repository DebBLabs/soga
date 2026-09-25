# M02 AAuth `fcf656d` Minimal Live-Exchange Execution Evidence

Date: 2026-09-24
Status: ACCEPTED GATED POSITIVE UNDER D-113

## Authority and execution

D-112 authorized exactly one execution of the blind dual-reviewed controller,
with no automatic retry. Execution occurred at commit
`f5639c76b7611d41c4ff14573039a8772f627c13`.

- controller SHA-256:
  `059ea6fc0e420674c8383211b05957ae2b04d6492abb00c9a1d3140d372ce289`;
- evidence directory:
  `/private/tmp/m02-aauth-fcf656d-live-exchange-20260924`.

The single execution completed without timeout or retry.

## Accepted evidence

- `live-exchange-test-evidence.json`: SHA-256
  `e0cf8734703625e1c5e49abbf273886b5fd8a2c64395950fdea83042910c47ec`;
- `live-exchange-test-stderr.bin`: 110 bytes; SHA-256
  `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`;
- `run-record.json`: SHA-256
  `cc0782708dcf409f2be932d6f72e2238d6348d5c4b118216491704f67f6c7dbb`.

The stderr is the exact pinned and permitted macOS diagnostic. Both blind
request-066 reviewers independently returned PASS with no blocking findings.

## Result

The evidence records `AAUTH_LIVE_EXCHANGE_TESTS_VERIFIED` and
`AAUTH_LIVE_EXCHANGE_EXECUTION_POSITIVE`.

- expected tests: 35;
- tests run: 35;
- failures: 0;
- errors: 0;
- skips: 0;
- expected failures: 0;
- unexpected successes: 0.

The executed suite includes the existing 24 Phase 1 tests and 11 minimal
live-exchange tests. The latter exercise strict identifiers and metadata,
person-token issuance, resource-token issuance, Person Server supervision,
auth-token issuance, final resource enforcement, unchanged `mission_s256`,
confirmation-key and audience binding, lifetime ceilings, tamper and scope
rejection, supervision failure closure, and rejection of a person token where
an auth token is required.

The controller verified the exact committed source, tests, pinned provider and
controller identities before and after execution. It recorded no timeout,
stream overflow, mutation, confinement escape or evidence leakage. Network and
listener creation were prohibited by the controller's audit guard.

## Claim boundary

This positive result establishes only that the exact committed, transport-free
minimal AAuth exchange package passes its 35 encoded bounded tests under the
pinned Ed25519 provider. It is not a claim of complete AAuth conformance or a
live network, wallet, WAS, QR or Misty integration.

No additional execution or other excluded activity is authorized.
