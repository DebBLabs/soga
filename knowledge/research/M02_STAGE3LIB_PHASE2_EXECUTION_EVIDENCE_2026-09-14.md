# M02 Stage 3-Lib Phase 2 Socket-Free Execution Evidence

Date executed: 2026-09-14
Status: POSITIVE RESULT — AWAITING INDEPENDENT REVIEW AND PI DISPOSITION
Authorization: D-062
SOGA checkpoint executed: `6295037d7ae3b219450fc4a796f94fc45b6bef87`

## Claim boundary

This run establishes only that the exact WAS teaching-server candidate can be
imported through its public package root and can provide selected application
and temporary filesystem-storage behavior through Fastify's in-memory
`inject()` path without the harness opening a network listener.

It does not establish Freewallet interaction, wallet-controlled production
storage, Person Server integration, AAuth conformance, external service
containment, person identity, authority, consent, mission permission,
participant-session behavior, physical execution, or Misty readiness.

## Exact candidate and execution identity

- WAS origin: `https://github.com/interop-alliance/was-teaching-server.git`
- detached commit: `2090a606f2723e4d57ef0090db55fd1bdab9427e`
- tree: `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`
- version: `0.27.0`
- LICENSE SHA-256:
  `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef`
- lockfile SHA-256:
  `edda1bc47d02a673e0994e2b184886e02f581f00c85958879b15225e4c7b7884`
- candidate status: tracked-clean with only the previously recorded
  `.npm-cache/` untracked; observed during preflight (not retained as an
  artifact) and re-verified after the run
- compiled entry: `dist/index.js` present
- provenance stamp: `dist/build-info.json` absent, as pre-registered
- Node: `/opt/homebrew/Cellar/node/26.7.0/bin/node`, `v26.7.0`
- reviewed controller SHA-256:
  `0fbb827664a950f37fb4d3af13ace107352a9559d2bfa3abc5da438c7532c897`

The temporary controller matched the complete shell block in the committed
proposal byte for byte before execution.

## Commands and run window

The source-contract test ran exactly:

```text
/opt/homebrew/Cellar/node/26.7.0/bin/node --test /Users/debb/dev/soga-clean/tools/m02_stage3lib/source_contract.test.mjs
```

The test process exited successfully. Its operator-observed terminal
output, which was not retained as an artifact, reported 5 of 5 tests
passing in 50.496916 ms. The five tests cover the absence of a direct
WAS import or harness listener call, guard-before-import ordering,
bounded configuration and cleanup text, repository-boundary behavior,
and both finite deadlines.

The controller then ran exactly:

```text
/private/tmp/m02-stage3lib-phase2-controller-20260914.sh
```

Its complete reviewed content is embedded in
`knowledge/proposals/M02_STAGE3LIB_PHASE2_EXECUTION_PROPOSAL_2026-09-14.md`.
The recorded UTC window was `2026-09-14T20:15:33Z` through
`2026-09-14T20:15:34Z`; controller exit status was zero.

## Compiled-artifact manifest

Before import, the controller generated the manifest from the candidate root
with:

```text
find dist -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256
```

- regular files recorded: 298
- manifest SHA-256:
  `7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586`
- `dist/index.js` was included
- manifest validation: passed
- post-run manifest comparison: byte-for-byte equal

The complete manifest remains as non-durable review evidence at
`/private/tmp/m02-stage3lib-phase2-20260914/dist-manifest.sha256`.

## Observed library behavior

The harness emitted these bounded event records:

```json
{"event":"health","requestClass":"non_mutating","status":200,"contentType":"application/health+json; charset=utf-8"}
{"event":"space_provision","requestClass":"bounded_temporary_write","status":201,"hasLocation":true,"stored":true,"transition":"absent_to_present"}
{"event":"resource_and_precondition_scope","status":"skipped","reason":"no resource exists; creating one requires zcap verification not supplied by this phase"}
{"event":"complete","physicalOutcome":"not_applicable","networkAttempts":0}
{"event":"cleanup","ok":true,"errors":[]}
```

Interpretation:

- WAS loaded through the bare `was-teaching-server` public package export.
- `createApp()` constructed the application without standalone startup.
- injected `GET /health` returned 200;
- one locally authorized, bounded temporary Space provision returned 201;
- `FileSystemBackend` independently confirmed the Space transitioned from
  absent to present;
- resource creation and precondition behavior were correctly skipped because
  this phase supplied no zcap verification; and
- the harness recorded zero guarded network attempts.

## Socket, process, and listener observations

- readiness marker observed: yes
- harness PID: 21428
- lsof self-control: passed
- live-PID lsof positive control: passed
- live harness TCP/UDP socket count at the synchronized pre-import holdpoint: 0
- holdpoint released only after the zero count: yes
- outer timeout: no
- harness exit status: 0
- PID absent after wait: yes (`kill -0` returned nonzero)
- unprivileged, user-visible TCP listener snapshots before and after: equal

The listener comparison is not a privileged whole-host inventory and does not
cover UDP listening state. The in-process guards were the primary control for
TCP, UDP, TLS, fetch, and listener attempts. These observations do not prove
the absence of every short-lived socket or child process.

## Cleanup and integrity

- temporary data roots before run: 0
- temporary data roots after run: 0
- completion marker absent after run: yes
- harness-local `node_modules` and package symlink absent after run: yes
- cleanup event: `ok=true`, no errors
- SOGA status before and after: byte-for-byte equal
- candidate tracked status unchanged
- compiled-artifact manifest unchanged
- stderr: empty

The only remaining SOGA working-tree item was the separately excluded,
untracked PI routine-tool proposal. It was not read, modified, staged, or
included in this run.

## Output-retention and secret check

Raw harness output remains only beneath the mode-0700 non-repository run root
`/private/tmp/m02-stage3lib-phase2-20260914`. The repository record includes
only the harness's bounded event lines above.

A post-run search found no Authorization header, bearer value,
onboarding token, private key, seed, or full generated `did:key`
controller in stdout or stderr; its exact commands were not retained.
Gate 1 independently reproduced a count-only scan of both files for
`Bearer`, `[Aa]uthorization`, `did:key:z`, `onboarding`,
`BEGIN .*PRIVATE`, `"seed"`, and any 43-character base64url run, with
zero matches. No secret or unrestricted response body is retained here.

## Result

Positive within the stated boundary: the exact WAS candidate supplied useful
health and bounded storage behavior through its documented in-process library
surface without a harness listener or recorded network attempt. Adoption,
composition, cleanup of preserved environments, Stage 3B, and every subsequent
implementation step remain subject to independent review and PI disposition.
