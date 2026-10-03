# M02 AAuth Approval-Pending Lifecycle Execution Proposal

Date: 2026-10-03
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ 27f8fdb1a84bb5aad8bc2b6534636c369991143b`
Review class: mandatory blind dual review under D-064

## Purpose and accepted basis

Execute once the D-134-accepted approval-pending lifecycle package and its
complete regression suite. D-134 accepted these exact committed artifacts:

- `m02_aauth_fcf656d/approval_pending.py` at SHA-256
  `18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b`;
- `tests/test_m02_aauth_approval_pending.py` at SHA-256
  `314f567a39ac4388a8a49f39f0ba965200aa72c9aabb630bc3fecfda8bf6fdf8`;
- `tools/m02_aauth_fcf656d/run_approval_pending_tests.py` at SHA-256
  `2d639991ef4c5aa918e9ee6328056450f56dcbfd6fdf9db2aaff63641b9cd4bc`.

The exact source basis is commit
`27f8fdb1a84bb5aad8bc2b6534636c369991143b`. Execution is permitted only at
the single later commit that records prospective authorization, and only when
a pre-execution
`git diff --name-only 27f8fdb1a84bb5aad8bc2b6534636c369991143b HEAD`
lists no paths except this proposal, `knowledge/strategy/DECISION_LOG.md` and
`knowledge/working/CURRENT_STATE.md`. Immediately before execution, record the
execution commit, the complete permitted diff-name result, an empty
`git status --porcelain -- engines input_adapters verify advisory`, and the
`HEAD` tree IDs for those four directories in the durable evidence report.
The runner's committed-byte, protected-source and provider checks must also
pass unchanged.

## Single bounded execution

After this proposal receives two blind independent PASS reviews and the PI
prospectively authorizes the run, execute exactly once from repository root
`/Users/debb/dev/soga-clean`:

`/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_approval_pending_tests.py`

The exact D-134 runner must enforce its reviewed controls:

- verify the accepted D-130 controller before executing its already-verified
  bytes, preserving the established controller trust chain;
- verify every accepted source and test hash and require committed-clean bytes;
- verify the durable provider runtime and accepted manifest;
- load exactly the accepted 65-test regression suite and sixteen additive
  approval-pending tests, requiring 81 tests with zero failures, errors, skips,
  expected failures or unexpected successes;
- permit only literal `127.0.0.1` ephemeral listeners used by the tests;
- use the fixed isolated child, minimal environment, no stdin, 90-second limit
  and 2,000,000-byte limit per output stream;
- accept stderr only when empty or the exact already-accepted bounded Darwin
  diagnostic;
- redact token material, verify module origins and pre/post immutability, and
  perform no automatic retry; and
- write once to the currently absent durable directory
  `/Users/debb/dev/research-evidence/soga/executions/approval-pending-v1`.

Any pre-start mismatch stops before candidate import or listener creation. Any
post-start timeout, overflow, unexpected stderr, count mismatch, import escape,
source or provider mutation, failed invariant, failure, error, skip or nonzero
exit is a consumed gated negative. Preserve all bounded evidence and do not
retry.

## Required evidence review and claim boundary

Both blind gates must review the resulting evidence before PI acceptance or
further use. A positive result may establish only the bounded localhost
approval-pending lifecycle while preserving the accepted 65-test AAuth/SOGA
and other-party-approval baseline. Specifically, it may establish that:

- an already-active exact approval permits the directed action immediately;
- an absent or inactive exact approval creates a finite resource-held pending
  invocation and returns `requirement=approval` with a poll location;
- a correctly bound signed poll observes pending state, and an out-of-band
  approval permits exactly one completion;
- withdrawal, denial, expiry, signature failure, replay, token/key mismatch,
  capacity overflow and connection-framing errors fail closed; and
- the explicitly unverified other-party receipt remains separate from the
  AAuth Person's delegated authority and from SOGA supervision.

It does not establish the approver's identity, parental or legal authority,
consent or assent, refusal precedence, continuous consent, cryptographic token
revocation, complete AAuth conformance, or a real QR, wallet, WAS, phone,
presentation or Misty integration.

## Exclusions

This proposal authorizes nothing by itself. No execution, retry, source change,
dependency operation, external service, non-loopback listener, wallet/WAS work,
QR flow, presentation integration, personal data, Misty access, physical
action, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.
