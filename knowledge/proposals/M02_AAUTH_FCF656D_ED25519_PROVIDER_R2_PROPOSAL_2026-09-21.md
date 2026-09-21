# M02 AAuth `fcf656d` Ed25519 Provider R2 Proposal

Date: 2026-09-21

## Purpose

Obtain one clean outer-gate result for the already observed Ed25519 provider
behavior without suppressing or broadening stderr handling.

## Evidence basis

The first committed provider run at `a5e17aa` is consumed and remains a gated
negative because the outer runner observed nonempty stderr. Its child exited
zero and preserved a positive RFC 8032 Test 1 result. The 110 stderr bytes have
SHA-256 `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`
and are byte-identical to the earlier static-verifier warning. Both request-039
reviewers found that the warning affects the outer disposition, not the
cryptographic result. Its precise intermittent host trigger is not claimed.

## Exact correction

Change only the outer runner. Preserve raw stderr before evaluation. Accept
stderr only when it is empty or is exactly 110 bytes with the pinned SHA-256
above. Any other content, including a superset containing those bytes, fails.
Record whether the pinned diagnostic matched. Use the fresh evidence directory
`/private/tmp/m02-aauth-fcf656d-ed25519-provider-r2-20260921`.

The child verifier is unchanged. All existing source, installation, wheel,
static-evidence, repository, timeout, stream-bound, atomic-write and no-retry
controls remain in force.

## Execution and claim boundary

After the corrected runner and this proposal are committed, run the runner
exactly once. Preserve all evidence. A positive result may establish only the
pinned installation's bounded Ed25519 provider behavior against the encoded RFC
8032 vector and negative cases. It is not AAuth conformance.

No network access, dependency or pip operation, listener, wallet/WAS work,
Misty access, G28 or G29 is authorized. No automatic retry is authorized.
Both blind gates must review the resulting evidence before acceptance.
