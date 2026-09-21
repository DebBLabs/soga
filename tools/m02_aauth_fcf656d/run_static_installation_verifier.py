#!/usr/bin/env python3
"""Run the preserved-installation verifier once under bounded controls."""

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time


sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).resolve()
VERIFIER_RELATIVE = Path("tools/m02_aauth_fcf656d/verify_preserved_installation.py")
RUNNER_RELATIVE = Path("tools/m02_aauth_fcf656d/run_static_installation_verifier.py")
VERIFIER = REPO / VERIFIER_RELATIVE
VERIFIER_SHA256 = "f75d8448992b08ba1040e77dd5593dc4692be76f76aa1942cd9ed69e3ea9eb71"
WHEEL_ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels")
INSTALL_PARENT = Path("/private/tmp/m02-aauth-fcf656d-phase1-install-20260921")
EVIDENCE_DIR = Path("/private/tmp/m02-aauth-fcf656d-static-recovery-20260921")
EVIDENCE_PATH = EVIDENCE_DIR / "static-verification-evidence.json"
RUN_RECORD_PATH = EVIDENCE_DIR / "run-record.json"
TIMEOUT_SECONDS = 60
STREAM_LIMIT_BYTES = 2_000_000
GIT_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
    "LANG": "C",
    "LC_ALL": "C",
    "GIT_OPTIONAL_LOCKS": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
}
CHILD_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
    "LANG": "C",
    "LC_ALL": "C",
    "GIT_OPTIONAL_LOCKS": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_bytes(content):
    return hashlib.sha256(content).hexdigest()


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def regular_nonsymlink(path):
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISREG(metadata.st_mode) and not path.is_symlink()


def directory_nonsymlink(path):
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISDIR(metadata.st_mode) and not path.is_symlink()


def repository_state():
    head = subprocess.run(
        ["/usr/bin/git", "-C", str(REPO), "rev-parse", "HEAD"],
        check=True, capture_output=True, timeout=10, env=GIT_ENV)
    status = subprocess.run(
        ["/usr/bin/git", "-C", str(REPO), "status", "--porcelain",
         "--untracked-files=all"],
        check=True, capture_output=True, timeout=10, env=GIT_ENV)
    head_text = head.stdout.decode("utf-8", errors="strict").strip()
    status_text = status.stdout.decode("utf-8", errors="strict")
    status_lines = status_text.splitlines()
    protected = {str(VERIFIER_RELATIVE), str(RUNNER_RELATIVE)}
    for line in status_lines:
        payload = line[3:] if len(line) >= 3 else ""
        paths = payload.split(" -> ")
        require(not any(path in protected for path in paths),
                "verifier or runner has a working-tree entry")
    return {"head": head_text, "status_porcelain": status_lines}


def atomic_write(path, content, mode):
    temporary = path.with_name(path.name + ".partial")
    with open(temporary, "xb") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def main():
    require(len(sys.argv) == 1, "no command-line arguments permitted")
    require(regular_nonsymlink(VERIFIER), "verifier absent or unsafe")
    require(sha256(VERIFIER) == VERIFIER_SHA256, "verifier hash mismatch")
    require(regular_nonsymlink(RUNNER), "runner absent or unsafe")
    repository = repository_state()
    runner_hash = sha256(RUNNER)
    require(directory_nonsymlink(WHEEL_ROOT), "wheel root absent or unsafe")
    require(directory_nonsymlink(INSTALL_PARENT), "installation parent absent or unsafe")
    require(not EVIDENCE_DIR.exists() and not EVIDENCE_DIR.is_symlink(),
            "evidence directory already exists")

    EVIDENCE_DIR.mkdir(mode=0o700)
    started_at = utc_now()
    started = time.monotonic()
    command = ["/usr/bin/python3", str(VERIFIER)]
    record = {
        "result": "RUNNING",
        "started_at": started_at,
        "runner_sha256": runner_hash,
        "verifier_sha256": VERIFIER_SHA256,
        "repository": repository,
        "command": command,
        "environment": CHILD_ENV,
        "timeout_seconds": TIMEOUT_SECONDS,
        "stream_limit_bytes": STREAM_LIMIT_BYTES,
        "timeout": False,
    }
    stdout = b""
    stderr = b""
    exit_status = None
    parsed_result = None
    error = None

    try:
        completed = subprocess.run(
            command, stdin=subprocess.DEVNULL, capture_output=True,
            timeout=TIMEOUT_SECONDS, check=False, env=CHILD_ENV)
        stdout = completed.stdout
        stderr = completed.stderr
        exit_status = completed.returncode
    except subprocess.TimeoutExpired as exc:
        record["timeout"] = True
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        error = "verifier timed out"
    except Exception as exc:
        error = type(exc).__name__ + ": " + str(exc)

    record.update(
        finished_at=utc_now(),
        duration_seconds=round(time.monotonic() - started, 6),
        exit_status=exit_status,
        stdout_length=len(stdout),
        stderr_length=len(stderr),
        stdout_sha256=sha256_bytes(stdout),
        stderr_sha256=sha256_bytes(stderr),
    )

    if error is None and len(stdout) > STREAM_LIMIT_BYTES:
        error = "stdout exceeds bound"
    if error is None and len(stderr) > STREAM_LIMIT_BYTES:
        error = "stderr exceeds bound"
    if error is None and stderr != b"":
        error = "stderr is not empty"

    if len(stdout) <= STREAM_LIMIT_BYTES:
        atomic_write(EVIDENCE_PATH, stdout, 0o400)

    if error is None:
        try:
            decoded = stdout.decode("utf-8", errors="strict")
            decoder = json.JSONDecoder()
            parsed_result, end = decoder.raw_decode(decoded)
            require(decoded[end:].strip() == "", "stdout contains multiple JSON values")
            require(isinstance(parsed_result, dict), "stdout JSON is not an object")
            require(parsed_result.get("result") in
                    {"STATIC_INSTALLATION_VERIFIED", "FAILED"},
                    "unexpected verifier result")
        except Exception as exc:
            error = type(exc).__name__ + ": " + str(exc)

    positive = (error is None and exit_status == 0 and
                parsed_result.get("result") == "STATIC_INSTALLATION_VERIFIED")
    if not positive and error is None:
        error = "verifier returned a negative result"
    record["parsed_result"] = (
        parsed_result.get("result") if isinstance(parsed_result, dict) else None
    )
    record["error"] = error
    record["result"] = "STATIC_VERIFICATION_POSITIVE" if positive else "FAILED"
    atomic_write(
        RUN_RECORD_PATH,
        (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        0o400,
    )
    return 0 if positive else 1


if __name__ == "__main__":
    raise SystemExit(main())
