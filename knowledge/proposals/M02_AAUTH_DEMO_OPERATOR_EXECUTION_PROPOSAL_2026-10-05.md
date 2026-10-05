# M02 AAuth Demo Operator Adapter Execution Proposal

Date: 2026-10-05
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ 19294b4`
Review class: mandatory blind dual review under D-064

## Purpose and accepted basis

Execute once the D-142-accepted demo operator runner and complete regression
suite. D-142 accepted:

- `m02_aauth_fcf656d/demo_operator.py` at SHA-256
  `b65160deffccf80220a0f466384a98ad1c3d21101dc44a1ee3b5d8099bf238a3`;
- `tests/test_m02_aauth_demo_operator.py` at SHA-256
  `25abd4b5af7f8eaeaf1585d641bb8e08d024b2cabd09c685c0a319cad5b50f67`;
- `tools/m02_aauth_fcf656d/run_demo_operator_tests.py` at SHA-256
  `37bc90282e1cf99226c8ce8086b82644a5c429cb7048f6ff9048778bbd95e112`.

The exact source basis is commit
`19294b449471ff898c4e88a1f9b68c2266ae518c`. Execution is permitted only at
the single later commit that records prospective authorization, and only when
`git diff --name-only 19294b449471ff898c4e88a1f9b68c2266ae518c HEAD`
lists no paths except this proposal, `knowledge/strategy/DECISION_LOG.md` and
`knowledge/working/CURRENT_STATE.md`. Immediately before execution, record the
execution commit, complete permitted diff, an empty
`git status --porcelain -- engines input_adapters verify advisory`, and the
`HEAD` tree IDs for those four directories in the durable evidence report.

## Single bounded execution

After this proposal receives two blind independent PASS reviews and the PI
prospectively authorizes the run, execute exactly once from repository root
`/Users/debb/dev/soga-clean`:

`/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_demo_operator_tests.py`

The exact D-142 runner must enforce all inherited controls:

- verify the accepted controller trust chain and every protected committed
  source and test hash before executing verified bytes;
- verify the accepted durable provider runtime and manifest;
- load exactly the accepted 81-test regression suite and twelve demo-operator
  tests, requiring 93 tests with zero failures, errors, skips, expected
  failures or unexpected successes;
- prove both accepted in-process operator seams: standing policy replacement
  and held-request resolution followed by signed polling;
- permit only literal `127.0.0.1` ephemeral listeners used by the tests;
- use the isolated child, minimal environment, no stdin, 90-second limit and
  2,000,000-byte limit per output stream;
- accept stderr only when empty or the exact accepted Darwin diagnostic;
- redact token material, verify module origins and pre/post immutability;
- write once to the currently absent durable directory
  `/Users/debb/dev/research-evidence/soga/executions/demo-operator-v1`; and
- perform no automatic retry.

Any pre-start mismatch stops before candidate import or listener creation. Any
post-start timeout, overflow, unexpected stderr, count mismatch, import escape,
source or provider mutation, failed invariant, failure, error, skip or nonzero
exit is a consumed gated negative. Preserve all evidence and do not retry.

## Required evidence review and claim boundary

Both blind gates must review the resulting evidence before PI acceptance or
further use. A positive result may establish only that a local operator can
feed synthetic, explicitly unverified other-party state into the accepted
standing resource policy and resource-held pending lifecycle through the two
accepted in-process seams. It may establish the twelve exact D-142 test claims,
including standing approval, withdrawal and clearing; held approval and
withdrawal; signed-poll mismatch handling; sanitized output; bounded receipt
tracking; and preservation of the 81-test baseline.

It does not establish verified identity, parental or legal authority, consent
or assent, presentation correctness, complete AAuth conformance, external
service behavior, wallet/WAS, QR, phone, Misty or physical-resource
integration.

## Exclusions

This proposal authorizes nothing by itself. No execution, retry, source change,
dependency operation, external service, non-loopback listener, presentation
modification, personal data, wallet/WAS, QR, Misty access, physical action, G28
or G29 is authorized. The unrelated PI routine-tool proposal remains excluded
and untouched.
