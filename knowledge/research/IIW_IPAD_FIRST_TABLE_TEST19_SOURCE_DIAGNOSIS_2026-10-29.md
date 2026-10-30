# IIW iPad-First Table Test 19 Source Diagnosis

Date: 2026-10-29
Status: SOURCE-ONLY DIAGNOSIS — PENDING BLIND DUAL REVIEW
Authority: D-163

## Question

Why did `test_19_proxy_forwards_raw_choice_under_lock` fail during the consumed
D-162 execution, and does the accepted source show an observed proxy defect or
a test-scope defect?

## Exact sources inspected

- presentation commit: `15a855fea252e7b7ea14936326d5f4b06312b86a`;
- `test_fictional_parent_presentation.py` SHA-256
  `69371f1fb336f92c42857f939310a4621b9a22f6b98dc1dde08f43b9b9ea54ae`;
- `bridge.py` SHA-256
  `a71bb86a1dd86b80d58e67699f1c6db9bfd9725ab209c1d6fe8d5d4daacf31d6`;
- accepted stderr SHA-256
  `cf09f5c4f2f080e2ac7662a8281aa132ee05f71b9519a2446b18d0b03551acb3`.

No source was imported, compiled, linted, tested, executed or modified.

## Findings

Test 19 contains two whole-text assertions on `bridge.py`:

1. require the exact raw forwarding statement
   `return self._proxy("POST", self.path, raw_body)`; and
2. prohibit `json.dumps(body).encode("utf-8")` anywhere in the file.

The first assertion passes. The exact raw forwarding statement appears in the
`/fictional-parent-choice` path while the bridge lock is held. The handler reads
the request once into `raw_body`, validates the origin and lease, and passes
those bytes directly to `_proxy`. The JSON parsing branch begins only after
that path returns.

The second assertion fails because the same text occurs once in the generic
`Handler._send` response helper. There it serializes an outbound response body
when the body is not already bytes. It does not transform the inbound
fictional-parent choice before proxying.

The whole-file negative assertion therefore ranges beyond the behavior named
by the test. The accepted source supports the diagnosis that the sole observed
failure is a test-scope defect. The D-162 evidence does not show a failure of
raw choice forwarding, lock coverage or the proxy request path.

## Correction boundary for a later proposal

A later create-only correction should modify the test so its negative assertion
is confined to the `/fictional-parent-choice` request-handling branch, while
retaining positive assertions that the branch:

- reads the request into `raw_body` once;
- holds `bridge.lock` while validating the active lease and pending state; and
- calls `_proxy("POST", self.path, raw_body)` without parsing or reserializing
  those bytes.

The production `bridge.py` does not require a correction for this finding.
Any exact test implementation, controller hash update, evidence-path change or
rerun requires separate prospective review and PI authorization.

## Claim boundary

This diagnosis resolves only the cause of the single D-162 test failure from
the accepted source. It does not convert D-162 into a positive result, establish
the 159-test claim, authorize a code change or rerun, or establish Beryl/iPad,
live QR, verified identity, parenthood, legal authority, consent, complete
AAuth conformance, Project Agent, wallet/WAS, mBot2, Misty, G28 or G29.
