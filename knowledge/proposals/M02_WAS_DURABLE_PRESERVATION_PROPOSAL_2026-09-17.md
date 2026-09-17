# M02 — Durable copy of accepted WAS research environment

Date: 2026-09-17
Status: PROPOSED — COPY AND RESTORATION NOT YET EXECUTED
PI requested durable backup after CC note015; Codex author/integrator.
Mandatory blind dual review of this plan and complete preservation utility
before copy. No candidate or package code executes during preservation.

## Scope and durability

Copy only /private/tmp/m02-stage3lib-20260910 (observed395MB), including exact
WAS checkout/.git, node_modules dependency tree, .npm-cache runner cache and
compiled dist. Original remains in place, without chmod, move or deletion.
Select /Users/debb/dev/research-evidence/m02-was-20260917-001/environment as
durable local backup outside repositories and temporary storage. It is expected
to survive normal reboot/shutdown and OS temporary-directory cleanup, but is
not protection against disk failure, user deletion or a whole-machine loss.
No cloud upload, external service, package, network or remote backup.

The durable copy is preservation evidence, NOT an alternate runtime root.
Accepted controller/tests hardcode /private/tmp/m02-stage3lib-20260910; any future
restore TO that exact path requires a separately reviewed prospective decision
and verification, with no assumed reacquisition/build fallback. No source edits,
path substitution/symlink at the runtime root, execution or restoration here.

## Exact reviewed utility and command

Read complete /private/tmp/hope-m02-stage3lib-20260914/preserve_was.py before use.
After both blind reviewers PASS and PI authorizes one copy, verify utility hash
and exact source identity, then invoke once outside sandbox with platform approval:

/usr/bin/env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /private/tmp/hope-m02-stage3lib-20260914/preserve_was.py

The utility hashes every regular file, records relative name/type/mode/size,
records each symlink text and rejects broken/external links and special files.
It inventories source before, copies via /usr/bin/ditto to an exclusively new
owned0700 bundle, inventories destination and source afterward, and requires
three equal logical manifests. Parent must be owned0700, not a symlink; fail
on occupied bundle. Filesystem inode/hardlink identity, timestamps, owners and
extended attributes are not claimed by logical-manifest equality. ditto may
preserve some of those but they are not independently verified. No permission
change to source or copied candidate files. Manifest/evidence files are0600.
Check a600-second cooperative deadline during hashing and bound ditto by its
remaining time; no automatic retry. If interrupted, failure or mismatch occurs,
retain partial bundle labelled unverified; do not remove or reuse it.

## Provenance and independent verification

Before copy, reverify source WAS commit2090a606f2723e4d57ef0090db55fd1bdab9427e,
tree540d85cea6cc7ab50ee6f00b0dead2084c1d65de, clean tracked source and dist298
manifest7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586.
build-info.json remains absent; provenance inherits the accepted restoration
evidence and D-080 exact-candidate positive execution, not completed build.
Record full original and copy logical-manifest hash, utility hash, exact command,
destination modes/status, source unchanged and any verification limit.
Both blind gates independently inspect source/copy/evidence read-only before
acceptance; git queries use GIT_OPTIONAL_LOCKS=0 and never execute npm/pnpm/Node.
Dependencies/cache are covered by every-file logical inventory, not dist alone.
This does not establish browser portability or copied dependency executability.

## B-043 and exclusions

Adopting durability control addresses part of B-043; do NOT close it by this copy
alone. Restore-to-fixed-path verification or explicit abandonment remains a
separate disposition. Retain exact original environment and diagnostic/marker
roots under D-080. No restoration, reacquisition, dependency/build, candidate
import/compile/lint/test, listener, Docker, wallet/PS integration, network,
personal data, payment, Misty access, G28/G29 or unrelated PI proposal change.
Any missing input, external symlink, occupied destination or new permission
requirement is a stop, not permission to improvise.
