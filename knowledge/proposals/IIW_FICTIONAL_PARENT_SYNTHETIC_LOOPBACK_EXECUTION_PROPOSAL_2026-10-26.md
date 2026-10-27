# IIW Fictional-Parent Synthetic Loopback Execution Proposal

Date: 2026-10-26
Status: PROPOSED — NOT AUTHORIZED
Prepared from accepted package: `main @ ec93a4bf604f078212ae015a0bec42252bf60032`
Review class: mandatory blind dual review under D-064

## Purpose

Authorize exactly one bounded synthetic-loopback execution of the D-150
accepted fictional-parent QR connection controller. The run exercises the
fictional-role disclosure, one-use choice transport, held-input adapter and
signed polling only through the accepted test composition. It does not generate
a live QR, contact a phone, bind a LAN address, modify the presentation or call
Misty.

## Exact inputs

The separately reviewed runtime manifest
`tools/iiw_fictional_parent/runtime-manifest.json` pins:

- the seven D-150 accepted package files at their request-014 hashes;
- every hash-protected AAuth/SOGA, D-148 QR and D-150 fictional-parent source
  and test used by the combined suite;
- the true five-controller inheritance chain, including the other-party
  controller and excluding the D-148 QR controller, which is not executed;
- the accepted durable AAuth provider manifest at SHA-256
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`;
- `Darwin`, `arm64`, Python `3.9.6` and observed interpreter
  `/Library/Developer/CommandLineTools/usr/bin/python3`; and
- the D-150 static import boundary permitting `iiw_qr_session.package` while
  forbidding `iiw_qr_session.session` specifically in
  `iiw_fictional_parent/*.py`. The combined D-148 baseline does load
  `iiw_qr_session.session` in the same child process.

The manifest is an operator holdpoint and review artifact; it is not imported
by the controller. The controller independently enforces its embedded source
hashes, inherited full provider verification, committed-source checks and
runtime identity. It enforces repository confinement for observed module and
package origins; the D-150 test suite separately enforces the scoped static
import boundary. The manifest itself must be
hash-pinned in the prospective execution decision and is not self-enumerated.

## Fixed paths and command

- repository: `/Users/debb/dev/soga-clean`;
- runtime manifest:
  `/Users/debb/dev/soga-clean/tools/iiw_fictional_parent/runtime-manifest.json`;
- accepted durable provider manifest:
  `/Users/debb/dev/research-evidence/soga/manifests/aauth-fcf656d-provider.json`;
- evidence directory:
  `/Users/debb/dev/research-evidence/soga/executions/iiw-fictional-parent-v1`;
- controller:
  `/Users/debb/dev/soga-clean/tools/iiw_fictional_parent/run_static_and_loopback_tests.py`;
- parent command invoked once without a shell:
  `/usr/bin/python3 -I -S -B /Users/debb/dev/soga-clean/tools/iiw_fictional_parent/run_static_and_loopback_tests.py`.

The operator launches that parent with `cwd=/Users/debb/dev/soga-clean` and an
environment exactly equal to the accepted `core.BASE_ENV`: `PATH=/usr/bin:/bin:/usr/sbin:/sbin`,
`LANG=C`, `LC_ALL=C`, `GIT_OPTIONAL_LOCKS=0` and
`PYTHONDONTWRITEBYTECODE=1`. `IIW_FICTIONAL_PARENT_TEST_CHILD` must be absent.
Only the verified parent adds `IIW_FICTIONAL_PARENT_TEST_CHILD=1` to a copy of
that environment when it constructs the identical child command. Neither
process receives an ambient proxy, registry, credential, Python-path or
external-service setting.

## Pre-start holdpoints

Stop before invocation unless all controls pass:

1. local `main`, `origin/main` and the prospective execution commit are equal;
2. source basis `ec93a4bf604f078212ae015a0bec42252bf60032` is an ancestor of
   that execution commit; the complete diff from that basis contains only this
   proposal, the runtime manifest and the prospective decision/canonical-state
   records; the `engines`, `input_adapters`, `verify` and `advisory` tree IDs
   equal their source-basis values; and all manifest-listed files match exactly;
3. the controller and every controller-chain member are exact committed files
   at their manifest hashes;
4. the runtime manifest and proposal match the exact hashes accepted by the PI;
5. tracked repository status is empty; the unrelated untracked PI proposal is
   excluded and need not be opened;
6. the provider manifest is the accepted durable regular file at its exact hash,
   and the inherited controller's full provider verification can run before any
   signed AAuth test path imports native provider code;
7. system, machine, Python and interpreter match the manifest exactly;
8. the evidence directory is absent and its durable parent is a non-symlinked
   directory outside the repository;
9. read-only inspection confirms no `/private/tmp/iiw-qr-manifest-*` directory
   exists, no prior controller or child process exists and no listener is attributable
   to this test identity; and
10. the exact parent argv, repository cwd and `core.BASE_ENV` are recorded; the
    parent environment contains no child-mode variable or ambient additions.

All ten holdpoints, including the provider-manifest hash, are first established
by read-only operator inspection. The parent then enforces protected-source,
provider, controller and exact-runtime state before evidence-directory creation
and before spawning the child that imports the native provider. A refusal before evidence
directory creation is a failed pre-start holdpoint, consumes no attempt and
authorizes no retry without PI disposition. The attempt is consumed when the
controller creates the fixed evidence directory.

## Authorized behavior for one later run

If prospectively accepted, exactly one invocation may:

- perform the inherited full static verification of the durable provider and
  load its pinned native code only inside the bounded child;
- import only the exact committed, hash-pinned sources in the controller chain;
- bind and connect only literal `127.0.0.1` ephemeral TCP listeners under the
  inherited socket guard;
- run exactly 128 tests: the accepted 93-test AAuth/SOGA operator baseline,
  accepted 17-test D-148 QR baseline and 18 D-150 fictional-parent tests;
- allow the D-148 manifest tests to create and clean their bounded
  `/private/tmp/iiw-qr-manifest-*` temporary directories;
- enforce the controller's 90-second limit and 2,000,000-byte limit for each
  output stream, with overflow detected and flagged after child completion; and
- make durable writes only to `fictional-parent-evidence.json`,
  `fictional-parent-stderr.bin` and `run-record.json` beneath the fixed,
  initially absent evidence directory, apart from the bounded temporary QR
  manifest fixtures that must be removed before completion.

Positive requires all 128 tests to pass with zero failure, error, skip,
expected failure or unexpected success; observed loopback bind and connect;
allowed stderr only; no timeout or overflow; an exact structured positive
marker; repository-confined `module_origins` and `package_origins`; and unchanged source, provider,
controller and runtime state before and after.

## Stop rules and cleanup

- No automatic retry.
- Any failed or indeterminate holdpoint prevents invocation.
- Any timeout, overflow, disallowed stderr, malformed payload, source/provider/
  runtime variance, origin escape, non-loopback socket attempt, leftover
  process/listener, leftover `/private/tmp/iiw-qr-manifest-*` directory or
  evidence-boundary variance is a gated negative result.
- The parent and child must end before disposition.
- After the run, independently verify by read-only process and listening-socket
  inspection that nothing attributable remains, and by read-only filesystem
  inspection that no `/private/tmp/iiw-qr-manifest-*` directory remains.
- Preserve the evidence directory exactly for blind dual review, including a
  negative result. Do not delete, rewrite or reuse it.

## Evidence and review

After the one run, create a standalone durable report recording the exact
execution commit; proposal, manifest, controller, source and provider-manifest
hashes; all pre-start observations; exact command and environment; start/end
times; result and return code; evidence file names and hashes; test and socket
counts; `module_origins` and `package_origins`; timeout/overflow flags; post-run immutability and
cleanup; and the claim boundary. Both blind gates must review the evidence
before PI acceptance or further use.

## Claim boundary and exclusions

A positive result may establish only the bounded localhost fictional-parent
role-play composition: an adult participant supplies unverified fictional input,
the accepted held-input adapter records it once, and signed polling observes the
result while preserving the accepted 110-test AAuth/SOGA and QR baselines.

It does not establish complete AAuth conformance, verified identity, a real
parent-child relationship, parental or legal authority, legal consent, a live
QR or phone interaction, Beryl/LAN behavior, presentation integration,
wallet/WAS, Misty, physical action, G28 or G29.

No dependency operation, retrieval, external service, non-loopback listener,
live QR, phone/device contact, personal data, presentation modification,
wallet/WAS work, Misty access or physical action is authorized. The unrelated
PI routine-tool proposal remains excluded and untouched.
