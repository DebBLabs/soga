# M02 AAuth Approval-Pending `404` Correction and Recovery Proposal

Date: 2026-10-04
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ 42f9603`
Review class: mandatory blind dual review under D-064

## Purpose and source-backed basis

Correct the sole D-136 failure without changing accepted production behavior.
The companion source-only diagnosis establishes that a syntactically complete
but unverifiable poll signature must return the same `404` as an unknown
pending identifier. The failure was an overbroad test expectation, not a
production lifecycle defect.

The D-136 evidence and durable artifacts remain immutable. The D-135 attempt
is consumed and will not be retried.

## Exact create-only correction

Modify only:

1. `tests/test_m02_aauth_approval_pending.py`
   - replace the shared `{400, 401}` assertion in the three-case table with
     exact expected statuses carried by each case;
   - assert unsigned/missing headers return `401`;
   - assert complete malformed signature fields return `404`;
   - assert an oversized signature header returns `401`;
   - preserve the existing exact `401` duplicate-header assertion, `400`
     body-framing assertion, and `404` stale/replay assertions;
   - do not add or remove a test method; retain sixteen approval-pending tests
     and 81 total tests.

2. `tools/m02_aauth_fcf656d/run_approval_pending_tests.py`
   - update only the protected SHA-256 for the corrected test module;
   - replace the evidence directory suffix `approval-pending-v1` with the new,
     initially absent `approval-pending-v2`;
   - preserve the accepted production-module hash, controller trust chain,
     provider gate, test modules and count, limits, redaction, socket guard,
     immutability checks, stderr rule and no-retry behavior unchanged.

The accepted production source
`m02_aauth_fcf656d/approval_pending.py` must remain byte-identical at SHA-256
`18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b`.
Every D-132 and other D-134 source must also remain unchanged.

## Review and execution sequence

This proposal authorizes nothing by itself. If accepted, it may authorize only
the two exact create-only modifications above. Both complete corrected files
must receive blind dual static review before commit or execution.

After static acceptance, a separate prospective PI instruction may authorize
exactly one bounded execution of the corrected committed runner. Before that
run, the execution proposal must be updated or supplemented with the new
commit, hashes, permitted diff, protected-directory status and four SOGA tree
IDs. Any mismatch stops before candidate import or listener creation. No
automatic retry is permitted. Resulting evidence requires blind dual review
and PI acceptance.

## Claim boundary and exclusions

A positive recovery result may establish only the already-proposed bounded
approval-pending lifecycle and preserved regression suite. It does not
establish complete AAuth conformance, verified identity, parental or legal
authority, consent, QR, wallet/WAS, presentation or Misty integration.

No production-source change, execution, retry, dependency operation, external
service, non-loopback listener, wallet/WAS work, QR flow, presentation
integration, personal data, Misty access, physical action, G28 or G29 is
authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.
