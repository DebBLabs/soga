# M02 Stage 3B — One Bounded Diagnostic Execution

Date: 2026-09-16

Status: PROPOSED — EXECUTION UNAUTHORIZED

Prepared at: `22395835e018d28d4eedba2d4a009dea1fd25871`

Author/integrator: Codex; mandatory blind dual review under D-064/B-044.

## Purpose and exact source

D-070 accepted diagnostic instrumentation, not a diagnostic run. Seek evidence
of which current focused tests fail, without repairing the composition or
attributing yesterday's consumed D-067 failure. Source accepted at review 037:

- corrected controller SHA-256 `559a9397e610a7f60cdf34db1b96874ad60509d609a069e2c0bf2e5b78727f2e`;
- runner SHA-256 `26396fa08b02a1971276604bfa7f474ff055c14a88e25075286c6576e59c3b1a`;
- instrumentation tests SHA-256 `e468530de98b29b8849c8ef92668c095d031b13a11a097430381ca50d6120c49`.

## Prospective sequence

The controller correction was created under D-071; it sets
`PYTHONDONTWRITEBYTECODE=1` explicitly in the diagnostic child environment.
The historical non-diagnostic environment is unchanged. Both blind reviewers
must PASS the complete corrected controller and this proposal before commit or
execution; the controller is not yet committed.

After both blind source/proposal reviews PASS and PI authorization, commit/push
the exact corrected controller, this proposal, and prospective records. Record that resulting full SOGA commit
as EXECUTION_HEAD in the standalone command record, then re-verify source hashes,
local/origin HEAD equality, candidate identity and manifest. No code is changed.

Run from `/Users/debb/dev/soga-clean`, outside the default agent sandbox with
explicit platform approval, under a minimal environment containing only
PATH=/usr/bin:/bin:/usr/sbin:/sbin, LANG=C, LC_ALL=C and PYTHONDONTWRITEBYTECODE=1.
No permission/configuration change persists. Application network remains barred
by the reviewed process-local guards; these are not OS-level containment.

1. Execute once `/usr/bin/python3 -m unittest tests.test_m02_was_diagnostics.DiagnosticInstrumentationTests -v`.
   Select this exact class, not the whole module: `SyntheticCase` is a deliberate
   failure helper, not a standalone acceptance test. Permit only synthetic
   test material and mocked controller results; no WAS or Node invocation.
   Capture the test count and status. Apply a 60-second process-group deadline,
   64 KiB per-stream cap, TERM followed after one second by KILL, and wait for
   exit/drain completion. If nonzero, timeout, overflow, cleanup failure, or
   unexpected process occurs, stop; no composition run is permitted.
2. Only after step 1 passes, verify no other `m02-stage3b-diagnostics-*` path
   survived the synthetic check. Stop on any leftover; do not delete it.
   Require the path
   `/private/tmp/m02-stage3b-diagnostics-20260916-001` to be absent. Codex creates
   it as an empty 0700 directory. Never reuse, replace, or delete an existing
   path. It is non-durable temporary research evidence, distinct from all
   worker/fake-worker/module cleanup patterns.
3. Invoke once `/usr/bin/python3 -c 'import json; from pathlib import Path; from m02_was_composition.controller import run_diagnostic_once; print(json.dumps(run_diagnostic_once(expected_soga_head="EXECUTION_HEAD", evidence_root=Path("/private/tmp/m02-stage3b-diagnostics-20260916-001")), sort_keys=True))'`.
   Replace only EXECUTION_HEAD with the full already-recorded execution commit.
   This re-executes current focused composition tests; it is a new diagnostic
   attempt, not authorization to repeat the historical controller entry point.
   The controller preserves its 24-invocation/180-second ceilings, per-worker
   10-second limits, 64 KiB stream caps, pre-import guards/observations, and
   unconditional postflight. Apply an outer 240-second process-group deadline
   and 64 KiB stream caps with the same termination/wait discipline.

No retry occurs if any step fails. Each step consumes its one attempt when its
test/controller process starts. The diagnostic controller's `ok` field—not
merely the Python exit status—determines composition success.

## Pre-use and post-run requirements

Require WAS at the unchanged fixed path, commit
`2090a606f2723e4d57ef0090db55fd1bdab9427e`, tree
`540d85cea6cc7ab50ee6f00b0dead2084c1d65de`, clean tracked source, public backend
export, and unchanged 298-file manifest
`7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586`.
Require Python 3.9.6 and pinned Node `/opt/homebrew/Cellar/node/26.7.0/bin/node`
at v26.7.0. Stop on absent/changed inputs; no restoration or package command.

Retain `record.json` (0600, atomic write, maximum 24576 bytes), its hash, both
execution and postflight outcomes, bounded allowlisted test/stage records, and
stream hashes. Do not emit raw focused exception messages, traces, envelopes,
tokens, or subtest values. Unknown stages remain unknown. Record explicitly
that parameterised failures may identify only the parent test method.

Independently verify no surviving test/worker process or worker/fake/module
temporary root; repositories and WAS artifacts unchanged; and retain the exact
diagnostic evidence directory until a separate PI retention/removal decision.
If the outer timeout fires, inspect cleanup read-only and report any leftovers;
do not remove evidence or undertake an unapproved repair.

The retained `record.json` is the primary diagnostic artifact; printed JSON is
convenience output. If printing fails after retention, inspect the artifact
read-only without rerunning. Transcribe its bounded redacted contents into the
standalone repository evidence so the finding survives temporary-directory loss.

Produce standalone evidence with exact commands, execution commit/hashes,
permission context, statuses, limits, artifact hashes, cleanup observations,
and any missing artifact. Both eligible blind reviewers inspect the evidence
before PI acceptance. No success or cause is inferred from a missing report.

## Exclusions

No source repair, automatic rerun, dependency/build operation, network access,
listener, Docker, external service, Freewallet integration, production data,
payment, Misty access, physical actuation, G28, or G29. Preserve the exact WAS
environment. The unrelated PI routine-tool proposal remains unread/untouched.
This proposal authorizes nothing before review and prospective PI decision.
