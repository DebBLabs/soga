# M02 WAS durable preservation evidence

Date: 2026-09-17
Status: COPY VERIFIED — BLIND DUAL EVIDENCE REVIEW AND PI ACCEPTANCE PENDING
Author/integrator: Codex
Authority: D-081 recorded prospectively before utility invocation, following
explicit PI permission for one copy and no restoration/candidate execution/retry.
Repository HEAD during operation:53e7022201fecdf14a8cd7ff085380d425d002e4.
D-081 is a working-tree decision recorded before execution, not a pre-run
committed decision. The preservation proposal required prospective authority
but did not require a pre-run decision commit.

## Reviewed and executed artifacts

Both blind request-050 reviewers PASS before copy:
- proposal f1144310c9d81a56096b0f508769b1d40501a64bd14e5ec1e70cd2a00d64999d
- utility43f01413f655cb8cf681a1c2796cf83460744ec5776e8f9e4457bdfbdd3efa37.
Both final hashes and independence/non-authoring statements verified.
Exact utility source is transcribed below, since its temporary location is
non-durable. No candidate imports or executable dependency/package code.

Exact command, cwd /Users/debb/dev/soga-clean:
```
/usr/bin/env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /private/tmp/hope-m02-stage3lib-20260914/preserve_was.py
```
Explicit platform permission executed outside default agent sandbox; no
persistent permission/configuration change. Single utility invocation, exit0.
Utility ran /usr/bin/ditto once on the exact source/destination; no retries.

## Result and full-tree verification

Source /private/tmp/m02-stage3lib-20260910 remains in place.
Durable bundle /Users/debb/dev/research-evidence/m02-was-20260917-001;
candidate copy beneath environment/was-teaching-server.
The existing source and new destination inventories were equal before/after:
29235 relative entries with regular-file modes/sizes/content SHA-256 and
symlink types/targets included. Covers checkout/.git, dependencies/.npm-cache
and dist, not just build files. No moved/deleted/re-permissioned source files.
The utility's source-before == source-after == copy requirement passed.
Utility elapsed9693ms within cooperative600-second deadline.

Retained full manifest.json SHA-256:
ceef625d8b233b55d8f7494347c6273301603fb7c9a208d4ff31115496e83f0c.
Verification.json SHA-256:
7b8ba65b5e07ed333ab78a0cdd33cf524cc4c46485a229f6e95e678929dced73.
Parent/bundle0700 and manifest/verification0600 observed independently with stat.
attempt.json remains reserved; absence of verification.json would mean
unverified partial output, but verification.json is present here.

Exact verification.json transcription:
```json
{"destination":"/Users/debb/dev/research-evidence/m02-was-20260917-001/environment","elapsed_ms":9693,"entries":29235,"manifest_s256":"ceef625d8b233b55d8f7494347c6273301603fb7c9a208d4ff31115496e83f0c","source":"/private/tmp/m02-stage3lib-20260910","source_unchanged":true,"status":"verified_logical_copy"}
```

Independent post-copy read-only checks:
- shasum -a256 manifest.json/verification.json; stat -f modes of parent,
  bundle and both evidence files;
- GIT_OPTIONAL_LOCKS=0 git -C copied-WAS rev-parse HEAD HEAD^{tree}:
 2090a606f2723e4d57ef0090db55fd1bdab9427e /
 540d85cea6cc7ab50ee6f00b0dead2084c1d65de;
- GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=no: clean;
- separate local stdlib pathlib/hashlib inspection recomputed sorted dist
  rows for source and copy: both298 files, manifest
 7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586;
 build-info.json absent in both.
Before invocation, utility/proposal pins and source Git commit/tree/cleanliness
were directly rechecked. Dist baseline was established in accepted D-080 evidence
and independently confirmed by both request-050 reviews; this preservation
invocation did not perform a new separate pre-copy dist-only hash command.
Full-tree pre/post equality and independent post-copy expected dist hashes
corroborate that unchanged candidate. No completed upstream build claim.

## Durability and limitations

This is durable LOCAL preservation expected to survive reboot/shutdown and
OS temporary cleanup, not disk failure, user deletion or whole-machine loss.
Equality is logical content/type/mode equality; inode/hardlink identity,
timestamps, owners and extended attributes are not independently claimed.
The manifest did not record the root directory itself, only its descendants.
The full-tree evidence is retained in the durable bundle for gate verification;
the entire29235-row manifest is not transcribed into the repository.
Copy does not demonstrate dependency executability or browser portability.

Accepted runtime still hardcodes /private/tmp/m02-stage3lib-20260910.
Durable backup is NOT a new runtime root. Any future restore to that exact path
needs separately reviewed prospective authority and verification. No restoration,
candidate execution, build, package/network activity, listeners, Docker, wallet,
PS integration, Misty access, G28/G29 or automatic retry occurred.
B-043 remains OPEN: adopted durability control does not close the separate
restoration/abandonment disposition. Original environment/diagnostic evidence
remain retained. No unrelated PI proposal read or changed.

## Exact preservation utility source
```python
"""Create-only preservation utility; review and PI authorization before use."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import time

SOURCE = Path('/private/tmp/m02-stage3lib-20260910')
PARENT = Path('/Users/debb/dev/research-evidence')
BUNDLE = PARENT / 'm02-was-20260917-001'
DEST = BUNDLE / 'environment'
LIMIT = 600
START = time.monotonic()


def check_time():
    if time.monotonic() - START > LIMIT:
        raise RuntimeError('preservation_deadline')


def manifest(root):
    rows = []
    for directory, directories, files in os.walk(root, followlinks=False):
        check_time()
        for name in sorted(directories + files):
            path = Path(directory) / name
            info = path.lstat()
            row = [str(path.relative_to(root)), stat.S_IMODE(info.st_mode)]
            if stat.S_ISLNK(info.st_mode):
                target = os.readlink(path)
                resolved = path.resolve(strict=True)
                if root.resolve() not in resolved.parents and resolved != root.resolve():
                    raise RuntimeError('external_link')
                row += ['link', target]
            elif stat.S_ISDIR(info.st_mode):
                row += ['directory']
            elif stat.S_ISREG(info.st_mode):
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    while True:
                        check_time()
                        chunk = stream.read(1024 * 1024)
                        if not chunk:
                            break
                        digest.update(chunk)
                row += ['file', info.st_size, digest.hexdigest()]
            else:
                raise RuntimeError('unsupported_file_type')
            rows.append(row)
    return sorted(rows)


def write_exclusive(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')
    descriptor = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return hashlib.sha256(raw).hexdigest()


def main():
    if SOURCE.is_symlink() or not SOURCE.is_dir():
        raise RuntimeError('source_root')
    for path in (Path('/Users/debb'), Path('/Users/debb/dev'), PARENT):
        if path.is_symlink():
            raise RuntimeError('destination_ancestor_link')
    before = manifest(SOURCE)
    try:
        PARENT.mkdir(mode=0o700)
    except FileExistsError:
        if not PARENT.is_dir():
            raise RuntimeError('destination_parent')
    if PARENT.stat().st_uid != os.getuid() or stat.S_IMODE(PARENT.stat().st_mode) != 0o700:
        raise RuntimeError('destination_permissions')
    BUNDLE.mkdir(mode=0o700)  # occupied target is never reused or overwritten
    write_exclusive(BUNDLE / 'attempt.json', {'status': 'copy_reserved', 'source': str(SOURCE)})
    remaining = max(1, LIMIT - (time.monotonic() - START))
    subprocess.run(['/usr/bin/ditto', str(SOURCE), str(DEST)], check=True,
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, timeout=remaining,
                   env={'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'C', 'LC_ALL': 'C'})
    copied = manifest(DEST)
    after = manifest(SOURCE)
    if before != after or before != copied:
        raise RuntimeError('manifest_mismatch')
    digest = write_exclusive(BUNDLE / 'manifest.json', {'schema': 1, 'rows': before})
    result = {'status': 'verified_logical_copy', 'source': str(SOURCE), 'destination': str(DEST),
              'manifest_s256': digest, 'entries': len(before), 'source_unchanged': True,
              'elapsed_ms': int((time.monotonic() - START) * 1000)}
    write_exclusive(BUNDLE / 'verification.json', result)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
```

## Next holdpoint

Both gates inspect source/copy/manifest independently read-only, without opening
peer reviews before posting. Evidence quality and preservation acceptance only;
no integration, restoration or execution authority follows from review.
