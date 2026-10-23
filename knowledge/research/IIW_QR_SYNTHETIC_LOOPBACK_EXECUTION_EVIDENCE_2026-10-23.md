# IIW QR Synthetic-Loopback Execution Evidence

Date: 2026-10-23  
Decision authority: D-147  
Execution commit: `3df3748b9262fd01c9d4610497dd6d1dafbef443`  
Result: **POSITIVE — pending blind dual evidence review and PI acceptance**

## Claim boundary

This report records one bounded synthetic-loopback execution of the accepted
adult-participant QR session package. It establishes only the encoded 17-test
fixture transport and its synthetic callback. It does not establish a live QR,
phone or device interaction; verified identity; parental or legal authority;
consent; an AAuth/SOGA production connection; wallet/WAS; Misty; G28; or G29.

## Accepted inputs

- proposal SHA-256:
  `80dc0345b03f267a1c8f9e225070e0333a46adcc32ee268f051c26f183beb658`;
- runtime manifest SHA-256:
  `2c11ec1ea27d6e8c2de0752fce4523bb1ffff7b6196286e78fb805dde44112c1`;
- controller SHA-256:
  `606832278adaf69dac6ddc84e63a74eef96068046fa83540537232df785b6ba4`.

The manifest bound the six accepted package, test, controller and README files
to the exact D-146 hashes.

## Pre-start observations

- local `main`, `origin/main` and execution commit were identical at
  `3df3748b9262fd01c9d4610497dd6d1dafbef443`;
- tracked repository status was empty;
- the unrelated untracked PI routine-tool proposal was excluded and unread;
- the fixed evidence directory was absent;
- its existing parent was a non-symlinked durable directory outside the
  repository;
- `/private/tmp` contained no `iiw-qr-manifest-*` entry;
- read-only process and listening-socket inspection found no prior controller,
  test process or attributed listener. The inspection command itself and its
  `rg` child were the only matching process lines;
- proposal and manifest hashes matched the accepted values.

The controller performed the delegated runtime/manifest checks inside the
single authorized invocation before it created the evidence directory.

## Exact invocation

The controller was invoked once, without a shell-expanded Python path, using:

```text
env -i
IIW_QR_BUNDLE_ROOT=/Users/debb/dev/soga-clean
IIW_QR_RUNTIME_MANIFEST=/Users/debb/dev/soga-clean/tools/iiw_qr_session/runtime-manifest.json
IIW_QR_EVIDENCE_DIR=/Users/debb/dev/research-evidence/soga/executions/iiw-qr-session-loopback-v1
/usr/bin/python3 -I -S -B
/Users/debb/dev/soga-clean/tools/iiw_qr_session/run_static_and_loopback_tests.py
```

No retry occurred.

## Durable evidence

Directory:
`/Users/debb/dev/research-evidence/soga/executions/iiw-qr-session-loopback-v1`

| File | Bytes | SHA-256 |
|---|---:|---|
| `stdout.json` | 2,390 | `b1e45a18b27ca194f0fda4639109d50d1e03e64594b79b018c7413b737b2d136` |
| `stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `run-record.json` | 1,151 | `7e0a0efede0f2a17f9ce94c779381bb9a403cdf1d6c973719b162e3774c153ce` |

## Observed result

- controller exit: `0`;
- positive marker: `IIW_QR_SESSION_TESTS_VERIFIED`;
- tests: 17 run, 0 failures, 0 errors, 0 skips;
- elapsed time: 3.969022 seconds;
- timeout: false;
- output overflow: false;
- stderr: empty;
- loopback socket audit: 7 binds and 22 connects;
- runtime: Darwin, arm64, Python 3.9.6;
- source, controller, tracked-tree and runtime state remained unchanged.

## Cleanup and preservation

Post-run read-only inspection found no remaining controller/test child, no
attributed listening socket and no `/private/tmp/iiw-qr-manifest-*` directory.
The repository was unchanged except for the separately excluded untracked PI
proposal and this subsequently created evidence report. The fixed evidence
directory is preserved unchanged for blind dual review.

No result is accepted until both eligible blind reviewers return PASS and the
PI issues an acceptance decision.
