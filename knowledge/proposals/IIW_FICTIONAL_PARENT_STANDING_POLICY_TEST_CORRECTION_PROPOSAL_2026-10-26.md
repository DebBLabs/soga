# IIW Fictional-Parent Standing-Policy Test Correction Proposal

Date: 2026-10-26
Status: PROPOSED — NOT AUTHORIZED
Basis: D-152 accepted gated negative and source-only diagnosis
Review class: mandatory blind dual review under D-064

## Purpose

Correct only the misplaced observation boundary in
`test_05_no_standing_policy_mutation`, then prepare the existing bounded
controller for a separately authorized R2 execution. The production package is
not changed.

## Create-only correction scope

If prospectively authorized, modify only:

1. `tests/test_iiw_fictional_parent.py` — in
   `test_05_no_standing_policy_mutation`, begin the encounter before sampling
   the policy state; assert `self.base.policy.calls == 1` immediately after
   encounter creation to prove it produced exactly one
   standing-policy evaluation; snapshot `policy.calls` and `policy.receipt`;
   record the held fictional-parent choice; assert that both snapshots remain
   unchanged; retain the static no-`replace_standing_input` assertion.
2. `tools/iiw_fictional_parent/run_static_and_loopback_tests.py` — update only
   the corrected test-file hash and select the new, initially absent durable
   evidence directory
   `/Users/debb/dev/research-evidence/soga/executions/iiw-fictional-parent-v2`.

Every other source hash, controller control, test composition, runtime bound,
socket guard, provider check, redaction rule, evidence limit and exclusion must
remain byte-identical to the D-151 reviewed controller.

## Required review sequence

1. Both blind gates review this diagnosis and proposal before any correction.
2. After PI create-only authorization, implement exactly the two-file change.
3. Both blind gates review the complete corrected test and controller before
   commit or execution.
4. Create and blind-dual-review a new or revised R2 execution proposal and
   runtime manifest pinning the corrected test and controller hashes, new source
   basis and new evidence path.
5. A separate prospective PI decision is required before any R2 execution.

## Exclusions

This proposal does not authorize a source edit, import, compilation, lint,
test, execution, listener, retry, live QR, phone/device contact, Beryl/LAN,
presentation modification, wallet/WAS, Misty, physical action, G28 or G29. The
unrelated PI routine-tool proposal remains excluded and untouched.
