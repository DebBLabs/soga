# IIW QR Synthetic Loopback Execution Proposal

Date: 2026-10-23
Status: PROPOSED — NOT AUTHORIZED
Prepared from accepted package: `main @ 9d3420fc349b49aabb3c07465a2811193992838e`
Review class: mandatory blind dual review under D-064

## Purpose

Authorize exactly one bounded synthetic-loopback execution of the D-146
accepted IIW QR participant-session controller. The run tests only the
standalone adult-participant fixture transport. It does not generate a live QR,
contact a phone, bind a LAN address or call an AAuth/SOGA production seam.

## Exact inputs

The execution uses only these committed inputs:

- `iiw_qr_session/session.py` — SHA-256
  `2aeeb9bd0e355b2d19521665dbc94569058355e34b365d534282d78f423c7907`;
- `iiw_qr_session/gateway.py` — SHA-256
  `9c5824df29ff0909d76e22c65af0ba277cda6d4c9370a720a2613d4256c6e3b8`;
- `iiw_qr_session/package.py` — SHA-256
  `3f079c3bd7c834758a1062926f5083d556497ab8013a2426ea5bef95584495c9`;
- `tests/test_iiw_qr_session.py` — SHA-256
  `e700137956d85183a474d08ac7d67a2da2d073471acc65616ef31c7d4a113df4`;
- `tools/iiw_qr_session/run_static_and_loopback_tests.py` — SHA-256
  `606832278adaf69dac6ddc84e63a74eef96068046fa83540537232df785b6ba4`;
- `iiw_qr_session/README.md` — SHA-256
  `7d73b5c5dd0490031027059f31ca6ec1e942a628e54141b03e7b69178340e8f8`;
- `tools/iiw_qr_session/runtime-manifest.json` — exact manifest reviewed with
  this proposal and separately hash-pinned before acceptance.

The manifest records `Darwin`, `arm64` and Python `3.9.6` and enumerates all six
runtime source inputs above. The manifest itself is an independently
hash-pinned control input and is not self-enumerated, avoiding a recursive
self-hash. No provider, package installation or non-standard dependency is
used.

## Fixed paths and command

- bundle root: `/Users/debb/dev/soga-clean`;
- runtime manifest:
  `/Users/debb/dev/soga-clean/tools/iiw_qr_session/runtime-manifest.json`;
- evidence directory:
  `/Users/debb/dev/research-evidence/soga/executions/iiw-qr-session-loopback-v1`;
- interpreter: `/usr/bin/python3`, observed as Python `3.9.6`;
- controller:
  `/Users/debb/dev/soga-clean/tools/iiw_qr_session/run_static_and_loopback_tests.py`.

The execution instrument sets exactly:

```text
IIW_QR_BUNDLE_ROOT=/Users/debb/dev/soga-clean
IIW_QR_RUNTIME_MANIFEST=/Users/debb/dev/soga-clean/tools/iiw_qr_session/runtime-manifest.json
IIW_QR_EVIDENCE_DIR=/Users/debb/dev/research-evidence/soga/executions/iiw-qr-session-loopback-v1
```

and invokes the controller once with `/usr/bin/python3 -I -S -B`. The exact
shell-free argument and environment construction must be recorded in the
prospective decision or execution record; no shell expansion or inherited
Python path is permitted.

## Pre-start holdpoints

Stop before execution unless all controls pass:

1. local `main`, `origin/main` and the prospective execution commit are equal;
2. all six accepted source hashes and the separately reviewed manifest hash
   match;
3. each source, manifest and controller is exact committed content;
4. tracked repository status is empty; the unrelated untracked PI proposal is
   excluded and need not be read;
5. the manifest validates the exact running system, machine, Python version and
   all six runtime files;
6. the evidence directory is absent and its existing parent is a non-symlinked
   durable directory outside the repository;
7. no prior process from this test exists and no listener is attributed to it;
8. `/private/tmp` (reached through macOS `/tmp` by the child because its minimal
   environment omits `TMPDIR`) contains no pre-existing directory with the test
   prefix `iiw-qr-manifest-`; and
9. the execution receives no proxy, registry, credential or external-service
   environment variable beyond the controller's exact minimal environment.

Holdpoints 1--4 and 6 are verified by read-only operator inspection of Git,
hashes, committed content and the fixed filesystem paths. Holdpoint 7 is
verified by read-only process inspection and a listening-socket listing filtered
to the controller/test identity. Holdpoint 8 is verified by read-only inspection
of `/private/tmp`. Holdpoint 9 is verified from the controller's exact
shell-free environment construction. Holdpoint 5 is delegated exclusively to
the controller's own pre-start `runtime_state`/manifest validation inside the
single authorized invocation; no separate Python execution or import is
permitted to establish it.

The authorized invocation may begin solely to perform the controller's
pre-start checks. The attempt becomes consumed only when the controller creates
the fixed evidence directory. A controller refusal before that creation is a
failed pre-start holdpoint, consumes no attempt and authorizes no retry without
PI disposition. Before the evidence directory is created, the controller may
perform only its pre-start import of `iiw_qr_session.package` for
`runtime_state` and manifest validation. No test module or test child may start
and no listener may open before the evidence directory is created. Any failed
or indeterminate operator-observed holdpoint prevents invocation entirely.

## Authorized behavior for one later run

If prospectively accepted, the one run may:

- import only the six accepted source inputs and Python standard library;
- create and clean test-only `iiw-qr-manifest-*` temporary directories beneath
  `/private/tmp` (via macOS `/tmp` under the child's minimal environment);
- bind and connect only literal `127.0.0.1` ephemeral TCP listeners under the
  controller's socket guard;
- run exactly the 17 accepted tests;
- enforce the controller's 60-second child timeout and 1,000,000-byte limit per
  output stream; and
- write only `stdout.json`, `stderr.bin` and `run-record.json` beneath the fixed,
  initially absent durable evidence directory.

The controller must return positive only when all 17 tests pass with zero
failures, errors or skips, loopback bind and connect were observed, stderr is
empty, output did not overflow, the child did not time out, the structured
positive marker is exact, and source, controller, tracked-tree and runtime
state are unchanged before and after.

## Stop rules and cleanup

- No automatic retry.
- Any timeout, output overflow, non-empty stderr, malformed child payload,
  source/runtime/tree mismatch, non-loopback socket attempt, leftover listener,
  leftover temporary directory or evidence-boundary variance is a gated
  negative result.
- The child process must end before disposition.
- Verify after the run by read-only process inspection, a listening-socket
  listing filtered to the controller/test identity, and inspection of
  `/private/tmp` that no listener or child remains and no
  `iiw-qr-manifest-*` temporary directory remains.
- Preserve the evidence directory exactly for blind dual review, including a
  negative result. Do not delete, rewrite or reuse it.

## Evidence and review

After the one run, create a standalone durable report recording exact commit,
source and manifest hashes; preflight observations; command and minimal
environment; start/end times; exit and positive/negative status; evidence file
names and hashes; test counts; socket counts; timeout/overflow flags; cleanup;
and claim boundary. Both blind gates must review the evidence before PI
acceptance or any further use.

## Claim boundary and exclusions

A positive result may establish only the D-146 standalone participant-session
state, HTTP codec, loopback transport, confinement and test-controller claims
on this exact Darwin/arm64/Python 3.9.6 environment.

It does not establish a phone-accessible QR, Beryl or LAN behavior, clean-machine
or Intel portability, public-event safety, participant identity, age, consent,
parental or representative authority, AAuth/SOGA integration, complete AAuth
conformance, presentation integration, wallet/WAS, Misty, physical action, G28
or G29.

No dependency operation, package or network retrieval, external service,
non-loopback listener, live QR, phone/device contact, personal data, AAuth/SOGA
production call, wallet/WAS work, Misty access or physical action is authorized.
The unrelated PI routine-tool proposal remains excluded and untouched.
