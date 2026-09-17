"""Outer bounds only. Creating this file conveys no execution authority."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import threading
import time

SOGA = Path('/Users/debb/dev/soga-clean')
PYTHON = '/usr/bin/python3'
EVIDENCE = Path('/private/tmp/m02-stage3b-diagnostics-20260917-001')
MARKERS = Path('/private/tmp/m02-stage3b-outer-20260917-001')
ENV = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'C', 'LC_ALL': 'C',
       'PYTHONDONTWRITEBYTECODE': '1'}
CAP = 65536


def terminate_group(process):
    # The focused controller child creates its own session; this bounds only
    # this outer group. Independent descendant/cleanup inspection is mandatory.
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    time.sleep(1)
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        return False
    return True


def bounded(command, seconds):
    output, errors = bytearray(), bytearray()
    overflow, read_error = threading.Event(), threading.Event()
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=SOGA, env=ENV, shell=False,
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)

    def drain(stream, target):
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    return
                room = CAP - len(target)
                target.extend(chunk[:room])
                if len(chunk) > room:
                    overflow.set()
                    return
        except (OSError, ValueError):
            read_error.set()

    threads = [threading.Thread(target=drain, args=(stream, target), daemon=True)
               for stream, target in ((process.stdout, output), (process.stderr, errors))]
    for thread in threads:
        thread.start()
    reason = 'completed'
    try:
        while process.poll() is None or any(thread.is_alive() for thread in threads):
            if overflow.is_set() or read_error.is_set():
                reason = 'capture_failure'
                break
            if time.monotonic() - started >= seconds:
                reason = 'outer_timeout'
                break
            time.sleep(.01)
    except BaseException:
        terminate_group(process)
        for thread in threads:
            thread.join(2)
        raise
    reaped = terminate_group(process)
    for thread in threads:
        thread.join(2)
    drained = not any(thread.is_alive() for thread in threads)
    if overflow.is_set() or read_error.is_set():
        reason = 'capture_failure'
    return {'outer': reason, 'status': process.returncode,
            'reaped': reaped, 'drained': drained,
            'stdout_s256': hashlib.sha256(output).hexdigest(),
            'stderr_s256': hashlib.sha256(errors).hexdigest(),
            'stdout_bytes': len(output), 'stderr_bytes': len(errors),
            'elapsed_ms': int((time.monotonic() - started) * 1000)}, bytes(output), bytes(errors)


def reserve(step):
    try:
        MARKERS.mkdir(mode=0o700)
    except FileExistsError:
        if MARKERS.is_symlink() or not MARKERS.is_dir():
            raise RuntimeError('marker_root')
    if MARKERS.stat().st_uid != os.getuid() or MARKERS.stat().st_mode & 0o777 != 0o700:
        raise RuntimeError('marker_permissions')
    descriptor = os.open(str(MARKERS / (step + '.attempt')),
                         os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, 'w') as output:
        output.write('reserved; no automatic reuse\n')
        output.flush()
        os.fsync(output.fileno())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', choices=('synthetic', 'diagnostic'), required=True)
    parser.add_argument('--head', required=True)
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', args.head):
        raise RuntimeError('head_format')
    reserve(args.step)
    if args.step == 'synthetic':
        command = [PYTHON, '-m', 'unittest',
                   'tests.test_m02_was_diagnostics.DiagnosticInstrumentationTests', '-v']
        seconds = 60
    else:
        code = ('import json; from pathlib import Path; '
                'from m02_was_composition.controller import run_diagnostic_once; '
                'print(json.dumps(run_diagnostic_once(expected_soga_head=' + repr(args.head) +
                ', evidence_root=Path(' + repr(str(EVIDENCE)) + ')), sort_keys=True))')
        command = [PYTHON, '-c', code]
        seconds = 240
    result, out, err = bounded(command, seconds)
    ok = (result['outer'] == 'completed' and result['status'] == 0
          and result['reaped'] and result['drained'])
    if args.step == 'synthetic':
        counts = re.findall(rb'^Ran ([0-9]+) tests? in ', err, re.MULTILINE)
        result['tests_run'] = int(counts[0]) if len(counts) == 1 else None
        ok = ok and result['tests_run'] == 9 and bool(re.search(rb'^OK\s*$', err, re.MULTILINE))
    else:
        try:
            value = json.loads(out)
            result['controller_ok'] = isinstance(value, dict) and value.get('ok') is True
        except (ValueError, UnicodeDecodeError):
            result['controller_ok'] = False
        ok = ok and result['controller_ok']
    result['step'] = args.step
    result['ok'] = bool(ok)
    print(json.dumps(result, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
