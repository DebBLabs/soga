# Corrected composition execution — outer runner addendum

Date: 2026-09-17
Status: CREATE-ONLY UNDER D-078 — EXECUTION UNAUTHORIZED

Complements, without replacing, execution proposal SHA-256
5b45bf79ad7241e9ce7ab1ee4626811bf2aadd21456551c79633fb496230b102.
All its pre-use checks, synthetic-first holdpoint, exact runtime/source pins,
new evidence-root creation, retained old evidence, independent cleanup and
claim boundaries remain mandatory coordinator duties. This runner does not
perform or replace those checks and does not itself convey authority.

Both blind reviewers must read complete tools/m02_was_composition_execution.py
and this addendum before any commit/run. Prospective PI execution permission
remains required. No code has been imported, parsed, compiled, linted or run.

After authorization and the required pre-use checks, invoke from SOGA with
PYTHONDONTWRITEBYTECODE=1 in the launching environment, using exactly:

1. /usr/bin/python3 tools/m02_was_composition_execution.py --step synthetic --head EXECUTION_HEAD
2. Only after synthetic success, directory comparison and exclusive new evidence
   root creation: /usr/bin/python3 tools/m02_was_composition_execution.py --step diagnostic --head EXECUTION_HEAD

Replace EXECUTION_HEAD only with the recorded full prospective execution commit.
The runner launches the proposal's exact child commands under its minimal
environment. It polls deadline/overflow/read-error without displaying raw output;
captures at most 65536 bytes per stream; terminates its owned outer process group
with TERM then KILL after one second; waits finitely for reaping and reader drain.
Unfinished drain/reaping, cap breach, nonzero status or timeout fails closed.
Its 60/240-second deadlines allow bounded signal/reaping/drain grace afterward.
Hashes on overflow describe retained prefixes, not complete streams.

The runner never prints captured raw errors. It reports fixed outer outcomes,
status, byte counts, retained-stream hashes, timing and synthetic test count.
Diagnostic acceptance still requires independent inspection of record.json:
34 tests, no failure/error/skip or truncation, successful execution/postflight,
and the unchanged candidate/source controls. Runner exit zero alone is insufficient.

Attempt markers are reserved exclusively at mode 0600 beneath owned 0700
/private/tmp/m02-stage3b-outer-20260917-001. Reserve before child spawn: a spawn
failure conservatively leaves the reservation occupied, not automatic retry
authority. Never remove/reuse markers. Retain them as temporary command evidence;
transcribe outcomes into the standalone durable report. The synthetic marker
does not authorize the diagnostic step; the coordinator holdpoint does.

The controller starts its focused child in another session. Killing the outer
group therefore does NOT prove all descendants stopped. Its existing inner
180-second deadline remains primary for that child; after ANY outer failure,
stop and independently inspect descendants and leftover roots read-only. No
unapproved repair/extra signals to other groups, retry or cleanup is authorized.
Normal completion also requires independent scoped process/socket/root checks.
If cleanup cannot be verified, report it as incomplete, not success.

No WAS HTTP app/service, listener, network, dependency change, Docker, Freewallet,
live Person Server change, payment, Misty, physical action, G28 or G29. Existing
composition sources and unrelated PI proposal remain untouched. This addendum
and runner require both blind PASS reviews before commit and separate PI authority
before execution; the prior proposal passes do not cover this new source.
