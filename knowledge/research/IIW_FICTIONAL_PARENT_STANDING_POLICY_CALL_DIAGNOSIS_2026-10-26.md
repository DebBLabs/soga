# IIW Fictional-Parent Standing-Policy Call Diagnosis

Date: 2026-10-26
Authority: D-152 bounded source-only diagnosis
Status: DIAGNOSIS ONLY — NO SOURCE CHANGE OR RETRY AUTHORIZED

## Question

Why did `test_05_no_standing_policy_mutation` observe
`self.base.policy.calls == 1` after starting at `0`?

## Finding

The failure is a test-observation placement defect, not evidence that the
fictional-parent connection changed the standing approval receipt.

`OtherPartyApprovalPolicy.calls` is an evaluation counter. It increments at the
start of `OtherPartyApprovalPolicy.evaluate()`; `replace()` changes `receipt`
but does not increment `calls`.

The failing test sampled `calls` before invoking `begin_encounter()`. That
helper calls the real `/enforce` path. For a directed action with no standing
receipt, `ApprovalPendingSurface.post()` calls
`self.resource.approval_policy.evaluate(...)` once. The resulting absent
approval causes creation of the held pending record and a `202` response. The
counter therefore changes from `0` to `1` before the fictional-parent choice is
recorded.

The subsequent fictional-parent path does not mutate standing policy:

1. `FictionalParentConnection.record()` calls only
   `DemoOperatorAdapter.record_held_input()`.
2. `record_held_input()` creates a bounded receipt and calls
   `ApprovalPendingStore.resolve()` for the held pending identifier.
3. It does not call `DemoOperatorAdapter.replace_standing_input()`,
   `OtherPartyApprovalPolicy.replace()` or `OtherPartyApprovalPolicy.evaluate()`.
4. `iiw_fictional_parent/connection.py` contains no
   `replace_standing_input` reference, matching the test's static assertion.

Thus the observed value `1` is the expected single standing-policy evaluation
needed to enter the pending state. The assertion compared values across the
wrong boundary: it included encounter creation rather than isolating held-input
recording.

## Exact source basis

- `tests/test_iiw_fictional_parent.py:79-84` samples `calls`, then invokes
  `begin_encounter()`, then records the choice;
- `tests/test_iiw_fictional_parent.py:31-40` implements `begin_encounter()` by
  calling `self.base.begin(...)` before constructing the connection;
- `tests/test_m02_aauth_demo_operator.py:156-161` sends the directed `/enforce`
  request in `begin()`;
- `m02_aauth_fcf656d/approval_pending.py:294` evaluates the standing policy for
  that directed request;
- `m02_aauth_fcf656d/other_party_approval.py:109` increments `calls` inside
  `evaluate()`;
- `m02_aauth_fcf656d/other_party_approval.py:103-106` shows `replace()` changes
  only `receipt`;
- `iiw_fictional_parent/connection.py:79-93` uses only the held-input adapter
  seam during `record()`;
- `m02_aauth_fcf656d/demo_operator.py:137-151` resolves the held record without
  invoking the standing-policy seam.

## Minimal prospective correction

A future correction should modify only
`tests/test_iiw_fictional_parent.py:test_05_no_standing_policy_mutation` so it:

1. begins the encounter first;
2. confirms the expected single standing-policy evaluation occurred;
3. snapshots both `policy.calls` and `policy.receipt` after encounter creation;
4. records the fictional-parent held input;
5. confirms neither value changed during held-input recording; and
6. retains the existing static assertion that the connection source does not
   reference `replace_standing_input`.

No production source needs to change for this finding. Before any separately
authorized R2 run, the bounded runner needs the corrected test hash and a new
absent evidence directory, and a new or revised execution proposal and runtime
manifest must pin the corrected test, corrected controller, new source basis
and new evidence path. Those complete artifacts require review before a rerun.

## Boundary

This diagnosis is source-only. It does not change or execute code, establish a
positive fictional-parent result, authorize a retry, or expand any D-152 claim
or exclusion.
