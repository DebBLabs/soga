# M02 AAuth Approval-Pending R2 Execution Proposal

Date: 2026-10-05
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ ad743c7`
Review class: mandatory blind dual review under D-064

## Purpose and accepted basis

Execute once the D-138-accepted corrected approval-pending runner and complete
regression suite. D-138 accepted:

- `tests/test_m02_aauth_approval_pending.py` at SHA-256
  `b0936449de6a143102ac012f7783ef138a5fe743a56fae41093b53d2eda37c69`;
- `tools/m02_aauth_fcf656d/run_approval_pending_tests.py` at SHA-256
  `fb76b2135042178a6915ddca03f409e85981ddf40df49937839355540aab0ee7`.

The production lifecycle module remains accepted and byte-identical at
SHA-256
`18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b`.
The D-135 execution remains a consumed gated negative; this proposal does not
retry it. It proposes a new R2 execution with a corrected committed test and a
new evidence target.

The exact source basis is commit `ad743c7`. Execution is permitted only at the
single later commit that records prospective authorization, and only when
`git diff --name-only ad743c7 HEAD` lists no paths except this proposal,
`knowledge/strategy/DECISION_LOG.md` and
`knowledge/working/CURRENT_STATE.md`. Immediately before execution, record the
execution commit, complete permitted diff, an empty
`git status --porcelain -- engines input_adapters verify advisory`, and the
`HEAD` tree IDs for those four directories in the durable evidence report.

## Single bounded R2 execution

After this proposal receives two blind independent PASS reviews and the PI
prospectively authorizes the run, execute exactly once from repository root
`/Users/debb/dev/soga-clean`:

`/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_approval_pending_tests.py`

The exact D-138 runner must enforce all inherited controls:

- verify the accepted controller trust chain and every protected committed
  source and test hash before executing verified bytes;
- verify the accepted durable provider runtime and manifest;
- load exactly the accepted 65-test regression suite and sixteen corrected
  approval-pending tests, requiring 81 tests with zero failures, errors, skips,
  expected failures or unexpected successes;
- permit only literal `127.0.0.1` ephemeral listeners used by the tests;
- use the isolated child, minimal environment, no stdin, 90-second limit and
  2,000,000-byte limit per output stream;
- accept stderr only when empty or the exact accepted Darwin diagnostic;
- redact token material, verify module origins and pre/post immutability;
- write once to the currently absent durable directory
  `/Users/debb/dev/research-evidence/soga/executions/approval-pending-v2`; and
- perform no automatic retry.

Any pre-start mismatch stops before candidate import or listener creation. Any
post-start timeout, overflow, unexpected stderr, count mismatch, import escape,
source or provider mutation, failed invariant, failure, error, skip or nonzero
exit is a consumed gated negative. Preserve all evidence and do not retry.

## Required evidence review and claim boundary

Both blind gates must review the resulting evidence before PI acceptance or
further use. A positive result may establish only the bounded localhost
approval-pending lifecycle and preserved 65-test AAuth/SOGA and other-party
approval baseline. It may establish the exact behavior enumerated in the
D-135 proposal, including immediate active approval, finite pending state,
signed polling, single completion and fail-closed negative cases.

It does not establish complete AAuth conformance, verified approver identity,
parental or legal authority, consent or assent, continuous consent,
cryptographic token revocation, or real QR, wallet, WAS, phone, presentation
or Misty integration.

## Exclusions

This proposal authorizes nothing by itself. No execution, retry, source change,
dependency operation, external service, non-loopback listener, wallet/WAS work,
QR flow, presentation integration, personal data, Misty access, physical
action, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.
