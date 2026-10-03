# M02 AAuth Other-Party Approval Execution Proposal

Date: 2026-10-03
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ 1a45a431ecc184508e107f4c79ff50e740cd11f0`
Review class: mandatory blind dual review under D-064

## Purpose and accepted basis

Execute once the D-130-accepted additive other-party approval package and its
complete regression suite. D-130 accepted these exact committed artifacts:

- `m02_aauth_fcf656d/other_party_approval.py` at SHA-256
  `c5a244da3ef5e6694df663af2ff0fb5cd83cdf928fa49c1ab708b197c35d78b0`;
- `tests/test_m02_aauth_other_party_approval.py` at SHA-256
  `a24e5f76832a5b8df7e9ed67409c18b03ce4a2b773103d813285048019e30a66`;
- `tools/m02_aauth_fcf656d/run_other_party_approval_tests.py` at SHA-256
  `b0fa483f3ab0ea343de847b8b4acb78096afc81bd81d3f69b0206ef579a3bdc1`.

The exact source basis is commit
`1a45a431ecc184508e107f4c79ff50e740cd11f0`. Execution is permitted only at
the single later commit that records the prospective authorization, and only
when a pre-execution
`git diff --name-only 1a45a431ecc184508e107f4c79ff50e740cd11f0 HEAD`
lists no paths except this proposal,
`knowledge/strategy/DECISION_LOG.md` and
`knowledge/working/CURRENT_STATE.md`. Record the execution commit, the complete
diff-name result and the `HEAD` tree IDs for `engines`, `input_adapters`,
`verify` and `advisory` in the durable evidence report. The runner's
committed-byte, protected-source and provider checks must also pass unchanged.

## Single bounded execution

After this proposal receives two blind independent PASS reviews and the PI
prospectively authorizes the run, execute exactly once:

from repository-root working directory `/Users/debb/dev/soga-clean`:

`/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_other_party_approval_tests.py`

The exact accepted runner must enforce its reviewed controls:

- verify the accepted base controller before executing its already-verified
  bytes;
- verify every accepted source and test hash and require committed-clean bytes;
- verify the durable provider runtime and accepted manifest;
- load exactly the accepted 53-test regression suite and twelve additive tests,
  requiring 65 tests with zero failures, errors, skips, expected failures or
  unexpected successes;
- permit only literal `127.0.0.1` ephemeral listeners used by the tests;
- use the fixed isolated child, minimal environment, no stdin, 90-second limit
  and 2,000,000-byte limit per output stream;
- accept stderr only when empty or the exact already-accepted bounded Darwin
  diagnostic;
- redact token material, verify module origins and pre/post immutability, and
  perform no automatic retry; and
- write once to the currently absent durable directory
  `/Users/debb/dev/research-evidence/soga/executions/other-party-approval-v1`.

Any pre-start mismatch stops before candidate import or listener creation. Any
post-start timeout, overflow, unexpected stderr, count mismatch, import escape,
source or provider mutation, failed invariant, failure, error, skip or nonzero
exit is a consumed gated negative. Preserve all bounded evidence and do not
retry.

## Required evidence review and claim boundary

Both blind gates must review the resulting evidence before PI acceptance or
further use. A positive result may establish only that the bounded additive
fixture makes the next directed action depend on a separately represented,
exactly bound, explicitly `unverified-demo-input` other-party receipt while
preserving the accepted AAuth/SOGA flow and 53-test regression baseline.

It does not establish the approver's identity, parental or legal authority,
consent or assent, refusal precedence, continuous consent, cryptographic token
revocation, AAuth `requirement=approval` pending/polling conformance, complete
AAuth conformance, or a real QR, wallet, WAS, phone, presentation or Misty
integration.

## Exclusions

This proposal authorizes nothing by itself. No execution, retry, source change,
dependency operation, external service, non-loopback listener, wallet/WAS work,
QR flow, presentation integration, personal data, Misty access, physical
action, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.
