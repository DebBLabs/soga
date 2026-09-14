# M02 Stage 3-Lib — Phase 2 Socket-Free Execution Proposal

Date: 2026-09-14
Status: PROPOSED — NOT YET EXECUTABLE
Prepared from checkpoint: `main @ 4e874592bc75beef34bb05d7f89b34d5319a8075`

## Purpose

Execute once the exact reviewed and committed Stage 3-Lib harness at
`tools/m02_stage3lib/harness.mjs` to determine whether WAS teaching server
commit `2090a606f2723e4d57ef0090db55fd1bdab9427e` works through its public
package-root library surface without starting its standalone application or
opening a network listener.

The PI directed preparation of this proposal. No execution authority exists
until both gates PASS this exact proposal and a decision-log entry records the
PI's prospective authorization of one run.

## Established prerequisite

D-061, as amended on 2026-09-14, records that the preserved upstream build is
incomplete only at the final `write-build-info` provenance-stamp step. Direct
`createApp()` use does not call `assertFreshBuild()`, and `/health` falls back
to the package version when `dist/build-info.json` is absent. The compiled
`dist/` is conditionally usable for this separately authorized library test.
Its provenance rests on the accepted Option A restoration evidence, and a
complete pre-use `dist/` SHA-256 manifest is mandatory.

Preserved candidate root:

`/private/tmp/m02-stage3lib-20260910/was-teaching-server`

Required identity:

- origin: `https://github.com/interop-alliance/was-teaching-server.git`
- detached commit: `2090a606f2723e4d57ef0090db55fd1bdab9427e`
- tree: `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`
- version: `0.27.0`
- lockfile SHA-256:
  `edda1bc47d02a673e0994e2b184886e02f581f00c85958879b15225e4c7b7884`
- tracked source clean, with only the previously recorded checkout-local
  `.npm-cache/` untracked
- `dist/index.js` present and `dist/build-info.json` absent

Any mismatch stops before test or harness execution.

## Fixed execution environment and evidence paths

Working directory: `/Users/debb/dev/soga-clean`

Node executable: `/opt/homebrew/Cellar/node/26.7.0/bin/node` (required observed
version: `v26.7.0`)

Run root: `/private/tmp/m02-stage3lib-phase2-20260914`

- raw stdout: `$RUN_ROOT/harness.stdout.jsonl`
- raw stderr: `$RUN_ROOT/harness.stderr.txt`
- pre-use manifest: `$RUN_ROOT/dist-manifest.sha256`
- user-visible TCP-listener snapshots: `$RUN_ROOT/listeners.before` and
  `$RUN_ROOT/listeners.after`
- repository evidence report created only after execution:
  `knowledge/research/M02_STAGE3LIB_PHASE2_EXECUTION_EVIDENCE_2026-09-14.md`

The run root must not exist before authorization is consumed. It is created
once with mode 0700. Raw stdout/stderr and the manifest remain outside both
repositories. The repository evidence retains the manifest-generation command,
file count, manifest SHA-256, harness event records, and bounded results so it
survives loss of the non-durable attachment.

Set `TMPDIR=$RUN_ROOT/tmp`, create that directory before launch, and require no
`$TMPDIR/m02-stage3lib-data-*` entry before or after the harness.

## Authorized run package

After dual PASS and PI acceptance, one attempt may perform only this sequence:

1. Record SOGA HEAD/status and the complete candidate identity above.
2. Record that the public package root resolves to `./dist/index.js`, that it
   exports `createApp` and `FileSystemBackend`, and that `dist/build-info.json`
   is absent.
3. From the fixed working directory, run exactly:
   `/opt/homebrew/Cellar/node/26.7.0/bin/node --test /Users/debb/dev/soga-clean/tools/m02_stage3lib/source_contract.test.mjs`.
   Node's test-file child process is expected for this command and ends before
   the harness begins.
4. If and only if the source-contract tests pass, start the reviewed controller.
   It creates the run root, produces the complete sorted pre-use `dist/`
   SHA-256 manifest, records its file count and hash, and then takes the
   normalized unprivileged, user-visible TCP-listener baseline immediately before
   process creation using:
   `lsof -nP -iTCP -sTCP:LISTEN -Fn | sed -n 's/^n//p' | LC_ALL=C sort -u`.
   This records local listening address and port only, never PID, command, user,
   or remote endpoint.
5. The controller runs
   `/opt/homebrew/Cellar/node/26.7.0/bin/node /Users/debb/dev/soga-clean/tools/m02_stage3lib/harness.mjs`
   once, as a background child of the controlling shell, with stdout and stderr
   redirected to the fixed raw paths and `TMPDIR` fixed as above. Capture `$!`
   as the harness PID. The controlling shell polls the stdout file for the exact
   line `M02_STAGE3LIB_PREIMPORT_READY`, failing closed if it is not observed
   within 10 seconds.
6. During the readiness holdpoint, record the live harness PID's TCP/UDP socket
   count using `lsof -nP -a -p "$HARNESS_PID" -i -Fn | sed -n 's/^n//p' | wc -l`.
   Require zero, then create exactly the existing fixed marker
   `/private/tmp/m02-stage3lib-20260910/observer.complete` using
   `/usr/bin/touch`. The harness deletes any pre-existing marker before emitting
   readiness. The PID check and marker creation must finish inside the
   harness's 15-second holdpoint.
7. Wait subject to a 90-second controller-side outer deadline; there is no second synchronization point and
   no claim of an immediately-before-exit sample. Verify exit code zero and
   PID absence. Take the normalized user-visible TCP-listener snapshot immediately
   after exit with the same command and require byte-for-byte equality with the
   baseline. The in-process guards are the primary control during execution;
   the external observations cannot prove absence of every short-lived socket
   or child process.
8. Verify application close and removal of the harness-created temporary data
   root, package symlink, harness-local `node_modules`, and completion marker.
9. Record final SOGA and candidate status and confirm the `dist/` manifest is
   unchanged.

The harness's temporary `tools/m02_stage3lib/node_modules/` and package symlink
are pre-registered expected transient paths during execution. Repository
integrity means exact pre-run versus post-run `git status --porcelain` equality;
the evidence report is created only afterward. The observer may coordinate only
the fixed readiness marker and read-only socket observations. It may not
inspect owners of unrelated listeners, modify either repository, alter the
candidate, or retry the harness.

The TCP inventory is unprivileged: it does not claim visibility into processes
owned by other users and it does not cover UDP, which has no listening state.
The in-process dgram guards cover UDP attempts. Unrelated user-process listener
churn may yield a negative listener-delta result without investigation.

The controlling terminal writes the following exact reviewed text to
`/private/tmp/m02-stage3lib-phase2-controller-20260914.sh`, sets mode 0700, and
runs it as one foreground-visible `/bin/sh` job after the preflight and
source-contract test succeed. The controller file is outside both repositories
and is removed only after evidence review and PI disposition.

```sh
#!/bin/sh
set -u
export RUN_ROOT=/private/tmp/m02-stage3lib-phase2-20260914
export TMPDIR="$RUN_ROOT/tmp"
test ! -e "$RUN_ROOT" || exit 90
mkdir -m 0700 "$RUN_ROOT" || exit 91
mkdir -m 0700 "$TMPDIR" || exit 92
RESULTS="$RUN_ROOT/controller.results"
record() { printf '%s=%s\n' "$1" "$2" >> "$RESULTS"; }
record started_utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
(cd /private/tmp/m02-stage3lib-20260910/was-teaching-server && find dist -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256) > "$RUN_ROOT/dist-manifest.sha256"
record dist_file_count "$(wc -l < "$RUN_ROOT/dist-manifest.sha256" | tr -d ' ')"
record dist_manifest_sha256 "$(shasum -a 256 "$RUN_ROOT/dist-manifest.sha256" | awk '{print $1}')"
MANIFEST_LINES="$(wc -l < "$RUN_ROOT/dist-manifest.sha256" | tr -d ' ')"
DIST_FILES="$(cd /private/tmp/m02-stage3lib-20260910/was-teaching-server && find dist -type f | wc -l | tr -d ' ')"
if test "$MANIFEST_LINES" -eq 0 || test "$MANIFEST_LINES" -ne "$DIST_FILES" || ! grep -q '  dist/index.js$' "$RUN_ROOT/dist-manifest.sha256"; then
  record manifest_valid 0
  record finished_utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit 93
fi
record manifest_valid 1
PRE_STATUS="$(cd /Users/debb/dev/soga-clean && git status --porcelain)"
record pre_status_sha256 "$(printf '%s' "$PRE_STATUS" | shasum -a 256 | awk '{print $1}')"
PRE_DATA_COUNT="$(find "$TMPDIR" -maxdepth 1 -name 'm02-stage3lib-data-*' -print | wc -l | tr -d ' ')"
record pre_data_count "$PRE_DATA_COUNT"
lsof -nP -p "$$" -Ffn 2>/dev/null | grep -q '^f'
LSOF_SELF_CONTROL=$?
record lsof_self_control_status "$LSOF_SELF_CONTROL"
lsof -nP -iTCP -sTCP:LISTEN -Fn > "$RUN_ROOT/listeners.before.raw"
LISTENER_BEFORE_STATUS=$?
record listener_before_lsof_status "$LISTENER_BEFORE_STATUS"
if test "$LSOF_SELF_CONTROL" -ne 0 || test "$LISTENER_BEFORE_STATUS" -gt 1; then
  record finished_utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit 94
fi
sed -n 's/^n//p' "$RUN_ROOT/listeners.before.raw" | LC_ALL=C sort -u > "$RUN_ROOT/listeners.before"
/opt/homebrew/Cellar/node/26.7.0/bin/node /Users/debb/dev/soga-clean/tools/m02_stage3lib/harness.mjs > "$RUN_ROOT/harness.stdout.jsonl" 2> "$RUN_ROOT/harness.stderr.txt" &
HARNESS_PID=$!
record harness_pid "$HARNESS_PID"
READY=0
for ATTEMPT in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100; do
  grep -Fxq M02_STAGE3LIB_PREIMPORT_READY "$RUN_ROOT/harness.stdout.jsonl" && READY=1 && break
  kill -0 "$HARNESS_PID" 2>/dev/null || break
  sleep 0.1
done
record readiness_seen "$READY"
RELEASED=0
if test "$READY" -eq 1 && kill -0 "$HARNESS_PID" 2>/dev/null; then
  lsof -nP -p "$HARNESS_PID" -Ffn > "$RUN_ROOT/pid-files.txt" 2>/dev/null
  LSOF_CONTROL_STATUS=$?
  if test "$LSOF_CONTROL_STATUS" -eq 0 && grep -q '^f' "$RUN_ROOT/pid-files.txt" && kill -0 "$HARNESS_PID" 2>/dev/null; then
    lsof -nP -a -p "$HARNESS_PID" -i -Fn > "$RUN_ROOT/pid-inet.txt" 2>/dev/null
    LSOF_INET_STATUS=$?
    if { test "$LSOF_INET_STATUS" -eq 0 || test "$LSOF_INET_STATUS" -eq 1; } && kill -0 "$HARNESS_PID" 2>/dev/null; then
      HARNESS_SOCKET_COUNT="$(sed -n 's/^n//p' "$RUN_ROOT/pid-inet.txt" | wc -l | tr -d ' ')"
      record harness_socket_count "$HARNESS_SOCKET_COUNT"
      if test "$HARNESS_SOCKET_COUNT" -eq 0; then
        /usr/bin/touch /private/tmp/m02-stage3lib-20260910/observer.complete
        RELEASED=1
      fi
    fi
    record lsof_inet_status "$LSOF_INET_STATUS"
  fi
  record lsof_control_status "$LSOF_CONTROL_STATUS"
fi
record holdpoint_released "$RELEASED"
OUTER_TIMEOUT=0
COUNT=0
while kill -0 "$HARNESS_PID" 2>/dev/null && test "$COUNT" -lt 900; do
  sleep 0.1
  COUNT=$((COUNT + 1))
done
if kill -0 "$HARNESS_PID" 2>/dev/null; then
  OUTER_TIMEOUT=1
  kill -TERM "$HARNESS_PID" 2>/dev/null
  COUNT=0
  while kill -0 "$HARNESS_PID" 2>/dev/null && test "$COUNT" -lt 20; do
    sleep 0.1
    COUNT=$((COUNT + 1))
  done
  kill -0 "$HARNESS_PID" 2>/dev/null && kill -KILL "$HARNESS_PID" 2>/dev/null
fi
wait "$HARNESS_PID"
HARNESS_STATUS=$?
record outer_timeout "$OUTER_TIMEOUT"
record harness_status "$HARNESS_STATUS"
kill -0 "$HARNESS_PID" 2>/dev/null
PID_KILL0_STATUS=$?
record pid_kill0_after_wait_status "$PID_KILL0_STATUS"
lsof -nP -iTCP -sTCP:LISTEN -Fn > "$RUN_ROOT/listeners.after.raw"
LISTENER_AFTER_STATUS=$?
record listener_after_lsof_status "$LISTENER_AFTER_STATUS"
sed -n 's/^n//p' "$RUN_ROOT/listeners.after.raw" | LC_ALL=C sort -u > "$RUN_ROOT/listeners.after"
cmp -s "$RUN_ROOT/listeners.before" "$RUN_ROOT/listeners.after"
record listener_snapshots_equal "$?"
POST_DATA_COUNT="$(find "$TMPDIR" -maxdepth 1 -name 'm02-stage3lib-data-*' -print | wc -l | tr -d ' ')"
record post_data_count "$POST_DATA_COUNT"
test ! -e /private/tmp/m02-stage3lib-20260910/observer.complete
MARKER_ABSENT=$?
record marker_absent_status "$MARKER_ABSENT"
test ! -e /Users/debb/dev/soga-clean/tools/m02_stage3lib/node_modules
MODULES_ABSENT=$?
record transient_modules_absent_status "$MODULES_ABSENT"
POST_STATUS="$(cd /Users/debb/dev/soga-clean && git status --porcelain)"
record post_status_sha256 "$(printf '%s' "$POST_STATUS" | shasum -a 256 | awk '{print $1}')"
test "$PRE_STATUS" = "$POST_STATUS"
record repository_status_equal "$?"
(cd /private/tmp/m02-stage3lib-20260910/was-teaching-server && find dist -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256) > "$RUN_ROOT/dist-manifest.after.sha256"
cmp -s "$RUN_ROOT/dist-manifest.sha256" "$RUN_ROOT/dist-manifest.after.sha256"
MANIFEST_EQUAL=$?
record dist_manifest_equal "$MANIFEST_EQUAL"
record finished_utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
test "$READY" -eq 1 && test "$RELEASED" -eq 1 && test "$OUTER_TIMEOUT" -eq 0 && test "$HARNESS_STATUS" -eq 0 && test "$PID_KILL0_STATUS" -ne 0 && test "$POST_DATA_COUNT" -eq 0 && test "$MARKER_ABSENT" -eq 0 && test "$MODULES_ABSENT" -eq 0 && test "$MANIFEST_EQUAL" -eq 0 && test "$LISTENER_AFTER_STATUS" -le 1 && cmp -s "$RUN_ROOT/listeners.before" "$RUN_ROOT/listeners.after" && test "$PRE_STATUS" = "$POST_STATUS"
exit $?
```

The controller records each bounded result as it occurs and performs all
post-run observations regardless of harness outcome. If readiness or the live
PID socket check fails, the controller does not create the completion marker;
the harness's own 15-second holdpoint expires and its `finally` cleanup runs.
If the process persists, the controller sends TERM at 90 seconds, allows a
two-second grace, then sends KILL if necessary and records a timeout negative
result. The lsof positive control and live-PID checks prevent inspection failure
or a vanished PID from being misreported as zero sockets. An lsof self-control
and exit-status checks prevent inspection failure from being misreported as
unchanged listener snapshots; the manifest is validated before launch.

## Expected behavior

The reviewed harness must:

- install its in-process network-attempt guards before dynamically importing
  the bare `was-teaching-server` package;
- import only the public package-root exports `createApp` and
  `FileSystemBackend`;
- create a new temporary filesystem data root outside both repositories with
  finite storage, upload, Space, Collection, and Resource limits;
- construct the application without calling `listen`;
- inject `GET /health` and require status 200;
- generate test-only local onboarding and controller material;
- inject one bounded Space-provisioning request, require status 201, and
  verify the stored Space directly through `FileSystemBackend`;
- skip resource and conditional-write behavior that would require unsupplied
  zcap verification;
- record zero guarded network attempts; and
- close and remove every harness-created path in `finally`.

`createApp()` enables pino logging, so raw stdout/stderr may contain standard
request metadata and the host name. Raw output remains only in the mode-0700
non-repository run root. The repository evidence includes only JSON lines with
a top-level harness `event` field plus exit status and bounded observations.
Before retention, check that neither raw nor repository evidence contains the
Authorization header, onboarding token, controller value, private key, or seed.
No secret, unrestricted response body, unrelated listener identity, or personal
data may enter repository evidence.

## Stop rules

The single attempt stops and is recorded as a negative result on any identity
or manifest mismatch, failed source-contract test, observer/readiness failure,
socket or guarded network attempt, listener delta, timeout,
nonzero harness exit, unexpected HTTP result, storage verification failure,
cleanup failure, repository change, or post-run manifest change. No retry,
diagnosis, repair, substitution, dependency operation, or expanded inspection
is permitted by this proposal.

## Evidence and review

Generate the manifest exactly from the candidate root with:

`find dist -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256`

redirected to the fixed manifest path. Record `wc -l` and
`shasum -a 256` of that file. After execution, generate a second temporary
manifest with the identical command and require `cmp -s` equality before
discarding the comparison file.

Define successful application close and cleanup as the harness event
`{"event":"cleanup","ok":true,"errors":[]}`, absence of any
`app_close` cleanup error, absence of the completion marker and
`tools/m02_stage3lib/node_modules`, and no `$TMPDIR/m02-stage3lib-data-*` entry.

Produce one standalone evidence report containing the exact commands, UTC run
window, candidate and repository identities, manifest attachment location and
hash, source-contract results, bounded harness event output, socket counts,
listener comparison result, exit status, cleanup result, and final status.
Both independent gates must review the complete post-run evidence before the
result may be adopted or used to claim WAS library feasibility.

Pre-register the expected harness event sequence: `health` with status 200;
`space_provision` with status 201, location present, stored true, and transition
`absent_to_present`; `resource_and_precondition_scope` skipped; `complete` with
zero network attempts; and `cleanup` successful, followed by process exit zero.

## Explicit exclusions

This proposal does not authorize any build or build recovery; dependency
installation or change; registry, Git, DNS, HTTP, TCP, UDP, TLS, or other
network access; WAS standalone startup or `listen`; deep import or upstream
source modification; Freewallet; wallet interaction; Person Server
integration; Stage 3B; Docker; external service; production credential;
personal data; payment; Misty access; physical actuation; MCP invocation; R3
protocol work; G28; G29; or change to representative-authority, consent,
privacy, or safety policy. The unrelated PI routine-tool proposal remains
outside scope and untouched.
