# M02 AAuth Approval-Pending `404` Source Diagnosis

Date: 2026-10-04
Status: SOURCE-ONLY DIAGNOSIS — NOT YET REVIEWED
Authority: D-136
Basis: `main @ 42f9603`

## Question

Why did the malformed-signature subcase in
`test_10_signature_failures_and_fresh_later_poll` receive HTTP `404` when the
test allowed only `400` or `401`?

## Finding

The implementation's `404` is the intended privacy behavior. The test
assertion is too broad.

The accepted proposal separates two classes of rejected poll:

1. transport or header-shape rejection before a pending record is examined;
2. authentication or binding failure after a syntactically complete request
   reaches a specific pending location.

The first class may return a transport/profile error. The second must not
reveal whether the pending identifier exists. The accepted proposal therefore
requires the resource to verify the HTTP signature and auth token before
revealing pending state, and requires failed verification or binding to produce
an indistinguishable `404` response.

## Exact source path

For the failed subcase, all three required signature headers are present, so
`_poll_request()` in `m02_aauth_fcf656d/approval_pending.py` constructs the
bodyless `Request` and calls `ApprovalPendingStore.poll()`.

`poll()` first finds the pending record and then calls `verify_request()`.
`verify_request()` cannot parse the malformed structured fields and raises
`SignatureProfileError`. `poll()` catches that error together with token and
JOSE verification errors and returns exactly:

```text
404 {"error":"not_found"}
```

That response is the same protected response used for an unknown identifier,
wrong key, wrong token digest or token-binding mismatch. Changing the
implementation to expose `400` or `401` for this case would weaken the accepted
record-existence privacy boundary.

By contrast:

- missing or duplicate signature headers are rejected by `_poll_request()`
  before `poll()` and map to `401`;
- an oversized signature header is rejected by `_poll_request()` and maps to
  `401`;
- prohibited GET body framing is rejected before `poll()` and maps to `400`;
- stale, replayed, malformed or cryptographically invalid signatures that
  reach `poll()` map to the indistinguishable `404`.

## Required correction

Do not change `approval_pending.py`. Correct only the test expectations so each
case asserts its exact accepted status rather than the set `{400, 401}`:

- unsigned/missing signature headers: `401`;
- complete but malformed signature fields: `404`;
- oversized signature header: `401`;
- duplicate signature header: `401`;
- body-framed GET: `400` (already asserted in `test_04`);
- stale and exact-replayed polls: `404` (already asserted).

Because the test hash changes, update only its protected hash in the bounded
runner and select a new absent durable evidence directory for a separately
authorized run. The accepted production module remains byte-identical.

## Boundary

No source or test was modified, imported, compiled, linted, tested or executed
during this diagnosis. No listener was opened and no retry occurred. This
diagnosis grants no correction or execution authority.
