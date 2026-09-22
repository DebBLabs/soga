#!/usr/bin/env python3
"""Bounded runner for the pinned Ed25519 provider extension."""

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
RUNNER_RELATIVE = Path("tools/m02_aauth_fcf656d/run_ed25519_public_key_import.py")
CHILD_RELATIVE = Path("tools/m02_aauth_fcf656d/verify_ed25519_public_key_import.py")
CHILD = REPO / CHILD_RELATIVE
INSTALL_PARENT = Path("/private/tmp/m02-aauth-fcf656d-phase1-install-20260921")
PROVIDER_ROOT = INSTALL_PARENT / "site-packages"
WHEEL_ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels")
STATIC_EVIDENCE = Path(
    "/private/tmp/m02-aauth-fcf656d-static-recovery-20260921/"
    "static-verification-evidence.json"
)
D099_ROOT = Path("/private/tmp/m02-aauth-fcf656d-ed25519-provider-r2-20260921")
D099_PROVIDER_EVIDENCE = D099_ROOT / "provider-evidence.json"
D099_RUN_RECORD = D099_ROOT / "run-record.json"
EVIDENCE_DIR = Path("/private/tmp/m02-aauth-fcf656d-provider-extension-20260922")
STDOUT_PATH = EVIDENCE_DIR / "provider-extension-evidence.json"
STDERR_PATH = EVIDENCE_DIR / "provider-extension-stderr.bin"
RUN_RECORD_PATH = EVIDENCE_DIR / "run-record.json"
TIMEOUT_SECONDS = 30
STREAM_LIMIT_BYTES = 1_000_000
ALLOWED_DARWIN_STDERR_SHA256 = (
    "2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61"
)
ALLOWED_DARWIN_STDERR_LENGTH = 110
EXPECTED_STATIC_EVIDENCE_SHA256 = (
    "fe66cc77cc1e4ceabcd99968fd6ab372c6b066b0f0e8c48291660e3636f792b0"
)
EXPECTED_D099_PROVIDER_EVIDENCE_SHA256 = (
    "d6c7564e55e81fbc11931fb0306b9ce4c210f968fce587cc1f6919ebaba505fe"
)
EXPECTED_D099_RUN_RECORD_SHA256 = (
    "6cb4f1ab9a5f13fe99b524c8df8f051f0bca75886e449d997dd89ae3db3d2591"
)
WHEELS = (
    ("cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl", 4_035_307,
     "ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0"),
    ("cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl", 180_509,
     "de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7"),
    ("pycparser-2.23-py3-none-any.whl", 118_140,
     "e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934"),
    ("typing_extensions-4.15.0-py3-none-any.whl", 44_614,
     "f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548"),
)
GIT_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C", "LC_ALL": "C",
    "GIT_OPTIONAL_LOCKS": "0", "PYTHONDONTWRITEBYTECODE": "1",
}
CHILD_ENV = dict(GIT_ENV)


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


def git_bytes(arguments):
    completed = subprocess.run(
        ["/usr/bin/git", "-C", str(REPO)] + arguments,
        check=True, capture_output=True, timeout=10, env=GIT_ENV)
    return completed.stdout


def repository_state_and_sources():
    head = git_bytes(["rev-parse", "HEAD"]).decode("ascii").strip()
    status = git_bytes(["status", "--porcelain", "--untracked-files=all"])
    status_lines = status.decode("utf-8", errors="strict").splitlines()
    protected = {str(RUNNER_RELATIVE), str(CHILD_RELATIVE)}
    for line in status_lines:
        payload = line[3:] if len(line) >= 3 else ""
        require(not any(path in protected for path in payload.split(" -> ")),
                "runner or child has a working-tree entry")
    runner_blob = git_bytes(["show", "HEAD:" + str(RUNNER_RELATIVE)])
    child_blob = git_bytes(["show", "HEAD:" + str(CHILD_RELATIVE)])
    require(RUNNER.read_bytes() == runner_blob, "runner differs from committed blob")
    require(CHILD.read_bytes() == child_blob, "child differs from committed blob")
    return {
        "head": head, "status_porcelain": status_lines,
        "runner_sha256": sha256_bytes(runner_blob),
        "child_sha256": sha256_bytes(child_blob),
    }


def verify_exact_json(path, expected_hash, expected_result, label):
    require(regular_nonsymlink(path), label + " absent or unsafe")
    require(sha256(path) == expected_hash, label + " hash mismatch")
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), label + " is not a JSON object")
    require(value.get("result") == expected_result, label + " result mismatch")
    return value


def verify_static_inputs():
    require(directory_nonsymlink(INSTALL_PARENT), "installation parent absent or unsafe")
    require(directory_nonsymlink(PROVIDER_ROOT), "provider root absent or unsafe")
    require(directory_nonsymlink(WHEEL_ROOT), "wheel root absent or unsafe")
    baseline = verify_exact_json(
        STATIC_EVIDENCE, EXPECTED_STATIC_EVIDENCE_SHA256,
        "STATIC_INSTALLATION_VERIFIED", "static evidence")
    d099_evidence = verify_exact_json(
        D099_PROVIDER_EVIDENCE, EXPECTED_D099_PROVIDER_EVIDENCE_SHA256,
        "ED25519_PROVIDER_VERIFIED", "D-099 provider evidence")
    d099_record = verify_exact_json(
        D099_RUN_RECORD, EXPECTED_D099_RUN_RECORD_SHA256,
        "ED25519_PROVIDER_POSITIVE", "D-099 run record")
    require(d099_record.get("stdout_sha256") == EXPECTED_D099_PROVIDER_EVIDENCE_SHA256,
            "D-099 record does not bind provider evidence")
    require(d099_record.get("parsed_result") == d099_evidence.get("result"),
            "D-099 parsed result mismatch")
    for filename, size, digest in WHEELS:
        path = WHEEL_ROOT / filename
        require(regular_nonsymlink(path), "wheel absent or unsafe: " + filename)
        require(path.stat().st_size == size and sha256(path) == digest,
                "wheel identity mismatch: " + filename)
    inventory = baseline.get("installation_parent_inventory", [])
    require(isinstance(inventory, list), "static inventory is not a list")
    expected_paths = {entry["path"] for entry in inventory}
    actual_paths = set()
    for directory, names, files in os.walk(INSTALL_PARENT, followlinks=False):
        for name in names + files:
            path = Path(directory) / name
            actual_paths.add(str(path.relative_to(INSTALL_PARENT)))
            require(not path.is_symlink(), "preserved tree contains symlink")
    require(actual_paths == expected_paths, "preserved inventory path set mismatch")
    for entry in inventory:
        path = INSTALL_PARENT / entry["path"]
        metadata = path.lstat()
        require(not path.is_symlink(), "preserved tree contains symlink")
        require(format(stat.S_IMODE(metadata.st_mode), "04o") == entry["mode"],
                "preserved entry mode mismatch")
        if entry["type"] == "dir":
            require(stat.S_ISDIR(metadata.st_mode), "preserved directory mismatch")
        elif entry["type"] == "file":
            require(stat.S_ISREG(metadata.st_mode), "preserved file mismatch")
            require(metadata.st_size == entry["size"] and
                    sha256(path) == entry["sha256"],
                    "preserved file identity mismatch")
        else:
            raise RuntimeError("unexpected baseline entry type")
    return {
        "static_evidence_sha256": EXPECTED_STATIC_EVIDENCE_SHA256,
        "d099_provider_evidence_sha256": EXPECTED_D099_PROVIDER_EVIDENCE_SHA256,
        "d099_run_record_sha256": EXPECTED_D099_RUN_RECORD_SHA256,
        "inventory_entries_verified": len(inventory),
        "wheel_count_verified": len(WHEELS),
    }


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
    require(regular_nonsymlink(RUNNER), "runner absent or unsafe")
    require(regular_nonsymlink(CHILD), "child absent or unsafe")
    repository = repository_state_and_sources()
    static_inputs = verify_static_inputs()
    require(not EVIDENCE_DIR.exists() and not EVIDENCE_DIR.is_symlink(),
            "evidence directory already exists")
    EVIDENCE_DIR.mkdir(mode=0o700)
    command = ["/usr/bin/python3", "-I", "-S", "-B", str(CHILD)]
    started_at = utc_now()
    started = time.monotonic()
    stdout = b""
    stderr = b""
    exit_status = None
    timed_out = False
    launch_error = None
    try:
        completed = subprocess.run(
            command, stdin=subprocess.DEVNULL, capture_output=True,
            timeout=TIMEOUT_SECONDS, check=False, env=CHILD_ENV)
        stdout, stderr = completed.stdout, completed.stderr
        exit_status = completed.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout, stderr = error.stdout or b"", error.stderr or b""
        launch_error = "provider child timed out"
    except Exception as error:
        launch_error = type(error).__name__ + ": " + str(error)
    stdout_overflow = len(stdout) > STREAM_LIMIT_BYTES
    stderr_overflow = len(stderr) > STREAM_LIMIT_BYTES
    if not stdout_overflow:
        atomic_write(STDOUT_PATH, stdout, 0o400)
    if not stderr_overflow:
        atomic_write(STDERR_PATH, stderr, 0o400)
    parsed = None
    error_text = launch_error
    if error_text is None and (stdout_overflow or stderr_overflow):
        error_text = "provider output exceeds bound"
    if error_text is None:
        try:
            decoded = stdout.decode("utf-8", errors="strict")
            parsed, end = json.JSONDecoder().raw_decode(decoded)
            require(decoded[end:].strip() == "", "stdout contains multiple JSON values")
            require(isinstance(parsed, dict), "stdout JSON is not an object")
            require(parsed.get("result") in {
                "ED25519_PROVIDER_EXTENSION_VERIFIED", "FAILED"},
                "unexpected provider-extension result")
        except Exception as error:
            error_text = type(error).__name__ + ": " + str(error)
    stderr_sha256 = sha256_bytes(stderr)
    allowed_darwin_stderr = (
        len(stderr) == ALLOWED_DARWIN_STDERR_LENGTH
        and stderr_sha256 == ALLOWED_DARWIN_STDERR_SHA256)
    if error_text is None and stderr != b"" and not allowed_darwin_stderr:
        error_text = "stderr is neither empty nor the pinned Darwin diagnostic"
    positive = (
        error_text is None and exit_status == 0
        and parsed.get("result") == "ED25519_PROVIDER_EXTENSION_VERIFIED")
    if not positive and error_text is None:
        error_text = "provider child returned a negative result"
    parsed_value = parsed.get("result") if isinstance(parsed, dict) else None
    record = {
        "result": "ED25519_PROVIDER_EXTENSION_POSITIVE" if positive else "FAILED",
        "error": error_text, "started_at": started_at, "finished_at": utc_now(),
        "duration_seconds": round(time.monotonic() - started, 6),
        "timeout": timed_out, "timeout_seconds": TIMEOUT_SECONDS,
        "stream_limit_bytes": STREAM_LIMIT_BYTES, "exit_status": exit_status,
        "stdout_length": len(stdout), "stdout_sha256": sha256_bytes(stdout),
        "stdout_preserved": not stdout_overflow,
        "stderr_length": len(stderr), "stderr_sha256": stderr_sha256,
        "stderr_preserved": not stderr_overflow,
        "pinned_darwin_stderr_matched": allowed_darwin_stderr,
        "parsed_result": parsed_value if isinstance(parsed_value, str) else None,
        "command": command, "environment": CHILD_ENV,
        "repository": repository, "static_inputs": static_inputs,
    }
    atomic_write(RUN_RECORD_PATH,
                 (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode(),
                 0o400)
    return 0 if positive else 1


if __name__ == "__main__":
    raise SystemExit(main())
