# M02 Stage 3B — Bounded Diagnostic Instrumentation

Date: 2026-09-16

Status: PROPOSED — CREATE-ONLY AUTHORIZATION REQUESTED; NO EXECUTION

Prepared at: `ad78cc5fe238dd08755f90741e7c44184d0dfb0f`

Author/integrator: Codex

Classification: mandatory dual review under D-064 with B-044 blind controls.

## Purpose

D-068 accepted one consumed attempt at `execution:focused_tests`. Its failing
test and cause remain unknown because the controller discarded captured test
output on failure. A test assertion, observation/environment issue, ordinary
storage failure, or normal-operation guard interception remain possible.

Prepare instrumentation that makes a future separately authorized run
informative. Do not repair the composition or infer yesterday's cause.

## Proposed create-only scope

Modify only `m02_was_composition/controller.py` and create
`m02_was_composition/diagnostic_tests.py` plus
`tests/test_m02_was_diagnostics.py`. Do not change the adapter, Node worker,
existing focused tests, WAS source, dependencies, or build outputs.

The controller will spawn the diagnostic runner as a separate child process
under its existing process-group termination, 180-second timeout, minimal
environment, and 64 KiB per-stream capture limits. Tests will not run in the
controller process. The child loads exactly the existing focused test module
and uses a standard-library unittest result collector. It delivers one bounded
JSON document on stdout (maximum 16 KiB); the controller validates it and is the
sole writer of the final atomic evidence record. It will record only:

- allowlisted focused test class/method identifiers and outcomes;
- failure/error class names and bounded allowlisted stage identifiers where
  available; never raw exception messages, traceback bodies, or subtest values;
- tests run, failure/error/skip counts, truncation state, and exit status.

Test names must come from the inspected focused module, not arbitrary input.
Unknown stages are recorded as `unknown`, not guessed. Maximum 128 result
records and 16 KiB serialized diagnostic JSON. Exceeding either produces a
small fixed failure document with `truncated=true` and a nonzero exit, without
emitting the oversized report or partial raw content. No stored envelope, token, key, identity value, raw
stdout/stderr, or exception message may be emitted.

The controller will retain that bounded structured report, captured-stream
hashes, execution status, elapsed time, and separate postflight/cleanup status
on success and failure. A postflight failure must not erase an execution
failure. Malformed, missing, excessive, or unexpected runner output fails
closed. The final record must be written atomically to an explicit fresh
temporary diagnostic directory outside both repositories; the directory is
evidence, not an unreported cleanup leftover. Use the distinct prefix
`/private/tmp/m02-stage3b-diagnostics-*`, outside every existing leftover-check
pattern; retain the worker/fake-worker/module leftover controls unchanged.
The later execution decision names the exact fresh path and its non-durable
status. Preserve that directory until a separate PI retention/removal decision;
no automatic deletion is authorized. No output destination is inferred.

Keep the exact candidate/runtime/manifest preflight, minimal environment,
network-attempt guards, per-worker observations, 24-invocation/180-second limits,
64 KiB captured-stream caps, process-group termination, listener comparisons,
and cleanup controls. No added test may invoke WAS or a Node worker. New
instrumentation tests use synthetic unittest cases and mocked controller
results, and verify redaction, limits, malformed output, atomic retention, and
simultaneous execution/postflight failure reporting.

The future diagnostic run would re-execute the existing focused composition
tests, including their guarded Node/WAS operations; only the newly added
instrumentation tests are synthetic. D-066's controller hash remains a
historical record; any modified controller must receive a new exact hash in
the later commit/execution decision. A reported stage is an observed exception
stage where available, not an interpretation of an assertion's expected value.

## Holdpoints

1. Both blind gates review this proposal; PI prospectively authorizes creation.
2. Create the three complete files without importing, compiling, linting,
   testing, or executing them. Both eligible blind reviewers inspect complete
   source and return PASS on exact hashes before commit or execution.
3. PI separately authorizes commit and a finite diagnostic execution proposal.
   That later decision must name the exact committed controller, invocation,
   runtime permission context, fresh evidence path, candidate integrity checks,
   attempt count, retention/preservation and cleanup rules. This proposal
   authorizes no execution, including synthetic instrumentation tests.
4. A future diagnostic result receives two blind reviews and PI disposition.
   Any repair or further run requires its own prospective authorization.

## Claim boundary and exclusions

Instrumentation reveals which tests fail; it does not establish the cause of
the consumed D-067 run, successful composition, or permission/identity/authority.
No automatic repair or retry. No WAS execution, imports, compilation, lint,
tests, listener, network, dependency/build operation, permission/environment
change, Docker, external service, Freewallet integration, personal data,
payment, Misty access, physical actuation, G28, or G29 is authorized here.
Preserve the exact WAS environment unchanged. The unrelated PI routine-tool
proposal remains unread and untouched. This proposal itself authorizes nothing.
