# M02 Stage 3B — Source-only failure diagnosis

Date: 2026-09-17
Status: PROPOSED — DIAGNOSIS UNAUTHORIZED
Prepared at: 1444bb0086813fb875f733883ba15d2c01128ab7
Author/integrator: Codex. Proposed classification: mandatory blind dual review;
this proposal concerns the next evidence basis for a material composition claim.

## Established starting point

D-073 accepted diagnostic evidence, not composition success. The single D-072
attempt is consumed. The retained record identifies seven AssertionError
failures and two CompositionError errors in 31 focused tests; failure stages
are unknown. The successful synthetic-test step and cleanup verification do not establish a
root cause. The earlier D-067 failure must not be retrospectively attributed.
The reviewed diagnostic evidence SHA-256 is
`cdd474696d906a4467e7e1e0b7bf74b2f386a0fa6198660c7e3d77d8a26fa8ca`.

## Requested bounded research authority

After both blind proposal reviews and prospective PI authorization, permit
Codex to inspect local source as text only, using read-only file/search/hash/git
commands. No imports, evaluation, compilation, lint, test, worker, or application
execution. This phase creates only a standalone SOGA research report; it may
not modify implementation, tests, candidate files, or governance boundaries.

Inspect these exact SOGA files and their directly referenced local modules:

- m02_was_composition/adapter.py
- m02_was_composition/worker.mjs
- m02_was_composition/controller.py
- m02_was_composition/diagnostic_tests.py
- tests/test_m02_was_composition.py

Read the preserved WAS checkout source/package metadata only where an actual
import or API use in the worker requires it. Require its existing fixed root
`/private/tmp/m02-stage3lib-20260910/was-teaching-server`, commit
`2090a606f2723e4d57ef0090db55fd1bdab9427e`, tree
`540d85cea6cc7ab50ee6f00b0dead2084c1d65de`, clean tracked source. If absent or
changed, stop and report; no restoration, build, or package operation.
Read the retained diagnostic record and accepted report without changing them.
Record SOGA HEAD, working-tree state, and hashes of every relied-on source.

## Research questions and complete self-audit

1. Trace the two failing positive round-trip tests through adapter, worker,
   WAS imports/storage calls and result parsing. Identify demonstrable static
   contradictions; label all runtime explanations as hypotheses.
2. Compare every worker-reported stage literal and dynamic stage path with
   the runner allowlist and adapter CompositionError propagation. Determine
   whether the missing stage information is statically explained or remains
   unresolved. Do not widen the allowlist or expose exception bodies here.
3. Inspect all seven failing test methods, including test_control_characters.
   Separate canonicalization assertions, negative-control expectations,
   observation/cleanup expectations, and worker result assertions. Do not
   assume one shared cause merely because failures occurred in the same run.
4. Verify the source-level compatibility of the actual package-root exports,
   module resolution, dependency loading, guard installation order, and
   storage root construction. Distinguish possible integration bugs from
   upstream limitations and permission/environment hypotheses.
5. State the minimum evidence still needed, if any, for each unresolved cause.
   Recommend the smallest next create-only correction or diagnostic proposal
   only after auditing the whole relevant path. A recommendation grants no
   repair or run authority.

## Evidence and stop rules

Produce one report with exact files/lines/hashes, source-supported findings,
separately labelled hypotheses, unresolved questions and verification limits.
Preserve the complete list of nine failed/error test methods from the retained
record. No secret, credential, raw execution traceback or personal data.
Record read-only commands and any denied operation; do not bypass a denial.
Stop on changed required inputs, missing local dependency source, need for
external retrieval or code execution, or any new authority requirement.
No execution result can be inferred from static inspection.

Codex self-audits the complete report before two blind evidence reviews.
Each reviewer receives its own exact hash list and must not read the peer
queue or claude-to-cg before posting, and must include independence and
contributor statements. Reviewers inspect source read-only; no execution.
Report adoption, canonical synchronization, commit/push and any subsequent
implementation or diagnostic execution require separate PI acceptance.

## Exclusions and preserved direction

No test/run/retry, code repair, instrumentation change, dependency installation,
network, listener, service, Docker, Freewallet execution/integration, personal
data, payment, Misty access, physical action, G28 or G29. Preserve the WAS
environment and diagnostic directory unchanged. The unrelated PI routine-tool
proposal remains unread and untouched. This does not substitute new mocks for
the intended Freewallet/WAS/separate AAuth Person Server composition.
The proposal and queue carry no prospective authority.
