# IIW Fictional-Parent Synthetic Loopback R2 Execution Proposal

Date: 2026-10-27
Status: PROPOSED — NOT AUTHORIZED
Source basis: `main @ d8db6ba1acdcc67c76d7e7d835e652fef6bf1617`
Review class: mandatory blind dual review under D-064

## Purpose

Authorize exactly one bounded R2 execution of the D-154 corrected
fictional-parent controller. R2 repeats the D-151 128-test composition with one
reviewed test-boundary correction only. It does not generate a live QR, contact
a phone, bind a LAN address, modify the presentation or call Misty.

## Correction basis

D-152 accepted the D-151 gated negative: 127 of 128 tests passed and
`test_05_no_standing_policy_mutation` failed because its evaluation counter was
sampled before the expected pending-path evaluation. D-153 accepted the
source-only diagnosis. D-154 accepted:

- corrected test SHA-256
  `6cfbadf11a25a054e1c9d3a368eb9fac7d04c3eced48095ced99bdc38d23f114`;
- corrected controller SHA-256
  `6e3b9d4fd18c9a34f84a86b8b6111e607c51b2e8a49a00a75c683d728c479153`.

The test now isolates held-input recording after the one expected standing-
policy evaluation and compares both policy call count and receipt across that
boundary. Production source is unchanged.

## Exact inputs

The separately reviewed revised
`tools/iiw_fictional_parent/runtime-manifest.json` must pin:

- source basis `d8db6ba1acdcc67c76d7e7d835e652fef6bf1617`;
- the corrected test and controller hashes above;
- the unchanged remaining 34 protected files;
- the true five-controller inheritance chain;
- the accepted durable provider manifest at SHA-256
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`;
- Darwin arm64, Python 3.9.6 and interpreter
  `/Library/Developer/CommandLineTools/usr/bin/python3`; and
- the unchanged scoped fictional-parent static import boundary.

The manifest is an operator holdpoint and review artifact, not a controller
input. The controller independently enforces embedded hashes, committed source,
provider/runtime identity, socket confinement, origin confinement and pre/post
immutability.

## Fixed paths and invocation

- repository: `/Users/debb/dev/soga-clean`;
- manifest:
  `/Users/debb/dev/soga-clean/tools/iiw_fictional_parent/runtime-manifest.json`;
- provider manifest:
  `/Users/debb/dev/research-evidence/soga/manifests/aauth-fcf656d-provider.json`;
- new evidence directory:
  `/Users/debb/dev/research-evidence/soga/executions/iiw-fictional-parent-v2`;
- controller:
  `/Users/debb/dev/soga-clean/tools/iiw_fictional_parent/run_static_and_loopback_tests.py`;
- exact shell-free parent argv:
  `/usr/bin/python3 -I -S -B /Users/debb/dev/soga-clean/tools/iiw_fictional_parent/run_static_and_loopback_tests.py`.

The operator invokes the parent once with repository cwd and environment exactly
equal to `core.BASE_ENV`: `PATH=/usr/bin:/bin:/usr/sbin:/sbin`, `LANG=C`,
`LC_ALL=C`, `GIT_OPTIONAL_LOCKS=0`, `PYTHONDONTWRITEBYTECODE=1`, with
`IIW_FICTIONAL_PARENT_TEST_CHILD` absent. Only the verified parent adds child
mode when spawning the bounded child.

## Pre-start holdpoints

Stop before invocation unless all controls pass:

1. local `main`, `origin/main` and the prospective R2 execution commit match;
2. D-154 source basis `d8db6ba1acdcc67c76d7e7d835e652fef6bf1617` is
   an ancestor; the complete diff contains only this proposal, the revised
   manifest and prospective decision/canonical-state records; and `engines`,
   `input_adapters`, `verify` and `advisory` tree IDs match that basis;
3. all 36 manifest entries match exact committed files;
4. the proposal and manifest match the hashes accepted prospectively by the PI;
5. tracked status is empty; the excluded PI proposal need not be opened;
6. the provider manifest and full inherited provider verification match;
7. system, machine, Python and interpreter match the manifest;
8. `iiw-fictional-parent-v2` is absent and its durable parent is a non-symlink
   directory outside the repository;
9. no `/private/tmp/iiw-qr-manifest-*` directory, attributable process or
   listener exists; and
10. the exact parent argv, cwd and environment are recorded, with child mode
    absent.

All holdpoints are first established read-only. The parent then verifies
protected source, provider, controller and runtime state before creating the
evidence directory. A refusal before creation consumes no attempt and permits
no retry without PI disposition. Creation consumes the single R2 attempt.

## Authorized behavior for one later R2 run

If prospectively accepted, one invocation may:

- verify the durable provider and load its pinned native code only inside the
  bounded child;
- import only hash- or tree-pinned repository sources;
- bind/connect only literal `127.0.0.1` ephemeral TCP under the socket guard;
- run exactly 128 tests: 93 AAuth/SOGA baseline, 17 QR baseline and 18
  fictional-parent tests;
- create and clean bounded `/private/tmp/iiw-qr-manifest-*` fixtures;
- detect timeout at 90 seconds and flag either output stream above 2,000,000
  bytes; and
- make durable writes only to `fictional-parent-evidence.json`,
  `fictional-parent-stderr.bin` and `run-record.json` below the initially absent
  `iiw-fictional-parent-v2` directory.

Positive requires all 128 tests to pass with no failure, error, skip, expected
failure or unexpected success; observed loopback bind/connect; permitted
stderr; no timeout/overflow; exact positive marker; repository/provider-confined
origins; and unchanged protected state before and after.

## Stop rules, evidence and review

- No automatic retry.
- Any failed holdpoint prevents invocation.
- Any test failure, timeout, overflow, disallowed stderr, malformed payload,
  state variance, origin escape, non-loopback socket attempt, leftover process,
  listener or QR temporary directory, or evidence-boundary variance is a gated
  negative.
- Preserve the exact evidence directory on either outcome.
- Independently verify post-run cleanup and immutability.
- Create a standalone durable report containing every field required by the
  D-151 proposal, including exact source hashes, start/end times, test/socket
  counts and both origin maps.
- Both blind gates must review the evidence before PI acceptance or use.

## Claim boundary and exclusions

A positive result may establish only the bounded localhost fictional-parent
role-play composition with unverified fictional input and the preserved
AAuth/SOGA and QR baselines. It does not establish complete AAuth conformance,
verified identity, a real parent-child relationship, parental/legal authority,
legal consent, live QR/phone, Beryl/LAN, presentation integration, wallet/WAS,
Misty, physical action, G28 or G29.

No execution, dependency operation, external service, non-loopback listener,
live QR, device contact, personal data, presentation modification, wallet/WAS,
Misty or physical action is authorized by this proposal. The unrelated PI
routine-tool proposal remains excluded and untouched.
