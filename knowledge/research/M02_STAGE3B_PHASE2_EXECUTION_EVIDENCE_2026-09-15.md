# M02 Stage 3B-2 Execution Evidence

Date: 2026-09-15

Authorization: D-067

Committed target: `61f8e9d36897c0415215f15e1b287d003e2f76b4`

Result: GATED NEGATIVE — `execution:focused_tests`

## Boundary

This was the one Phase 3B-2 execution authorized by D-067. The attempt is
consumed. It used the exact committed controller and focused test suite with
the preserved local WAS candidate. It authorized no retry, diagnosis, repair,
external service, listener, Freewallet integration, personal data, payment,
Misty access, physical actuation, G28, or G29.

## Pre-use verification

Immediately before execution:

- local `HEAD` was
  `61f8e9d36897c0415215f15e1b287d003e2f76b4`;
- the preserved WAS candidate was commit
  `2090a606f2723e4d57ef0090db55fd1bdab9427e` with tree
  `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`;
- its `dist/` contained 298 files;
- the pinned runtimes reported Node `v26.7.0` and Python `3.9.6`; and
- the only unrelated working-tree item was the untracked, excluded PI
  routine-tool-approval proposal.

The controller's own preflight completed; otherwise execution could not have
reached the focused-test status check reported in the traceback.

## Exact execution

```text
/usr/bin/python3 -c 'import json; from m02_was_composition.controller import run_once; print(json.dumps(run_once(expected_soga_head="61f8e9d36897c0415215f15e1b287d003e2f76b4"), sort_keys=True))'
```

Execution context: the controller command ran with elevated permission outside
the default agent sandbox, from `/Users/debb/dev/soga-clean`. No other
permission change was made for this run.

Observed exit: nonzero after 19.1 seconds (operator-observed terminal output;
not retained as an artifact).

Observed terminal result (operator-observed; not retained as an artifact):

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/Users/debb/dev/soga-clean/m02_was_composition/controller.py", line 93, in run_once
    if status:raise RuntimeError('execution:focused_tests')
RuntimeError: execution:focused_tests
```

The controller captured but did not expose the focused test process's stdout
or stderr on failure. Therefore this evidence does not identify which test
failed, and no cause is inferred. No rerun occurred.

## Post-run verification

The controller reached line 93 only after its unconditional postflight block.
No postflight exception replaced the observed result. Under the reviewed
controller, that means its repository/candidate snapshot comparison,
user-visible listener comparison, and temporary-path checks completed without
raising.

Separate read-only checks immediately afterward found:

- SOGA contained only the same excluded untracked PI proposal;
- the WAS tracked working tree was unchanged;
- the WAS commit and tree remained exact;
- `dist/` still contained 298 files;
- no `m02-stage3b-run-*`, `m02-stage3b-fake-*`, or
  `m02-was-composition-modules-*` path was printed;
- no surviving Phase 3B worker, test, or `worker.mjs` process was found (the
  process search printed only the verification command and its `rg` process);
- the post-run user-visible TCP listener inventory hash was
  `9b4bf8be1b2db07dcbbd734a6c1d844c92f20fbd3bc3b5f09f905500f2516e40`.
  This was operator-observed and not retained as an artifact; the exact command
  was `/usr/sbin/lsof -nP -a -u "$(id -u)" -iTCP -sTCP:LISTEN | shasum -a 256`.

The committed target was pushed: local `HEAD` and `origin/main` both resolved
to `61f8e9d36897c0415215f15e1b287d003e2f76b4` after the push.

The initial sandboxed `ps` check was denied by the host (`operation not
permitted`); it was repeated once as a read-only post-run inspection outside
that sandbox. This was not a candidate or test execution.

## Claim boundary and next disposition

This result establishes that the single authorized controller invocation
reached the focused test suite and failed closed as `execution:focused_tests`.
It does not establish successful Person Server/WAS composition and does not
identify the failing test. The standalone evidence and cleanup observations
require two blind independent reviews under B-044. Any diagnosis, code change,
test execution, or retry requires a new prospective PI authorization.
