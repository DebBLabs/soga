#!/usr/bin/env python3
"""Bounded controller for the additive demo-operator adapter."""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import types
import unittest


REPO = Path(__file__).resolve().parents[2]
BASE_PATH = Path(__file__).with_name("run_approval_pending_tests.py")
BASE_RELATIVE = "tools/m02_aauth_fcf656d/run_approval_pending_tests.py"
BASE_SHA256 = "fb76b2135042178a6915ddca03f409e85981ddf40df49937839355540aab0ee7"
VERIFICATION_ENV = {
    "GIT_OPTIONAL_LOCKS": "0", "LANG": "C", "LC_ALL": "C",
    "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
}
if not BASE_PATH.is_file() or BASE_PATH.is_symlink():
    raise RuntimeError("accepted approval-pending controller is not a regular file")
BASE_BYTES = BASE_PATH.read_bytes()
if hashlib.sha256(BASE_BYTES).hexdigest() != BASE_SHA256:
    raise RuntimeError("accepted approval-pending controller hash mismatch")
BASE_COMMITTED = subprocess.run(
    ["/usr/bin/git", "show", "HEAD:" + BASE_RELATIVE], cwd=REPO,
    env=VERIFICATION_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    timeout=10, check=False)
if BASE_COMMITTED.returncode != 0 or BASE_COMMITTED.stdout != BASE_BYTES:
    raise RuntimeError("accepted approval-pending controller is not committed source")
base = types.ModuleType("m02_approval_pending_controller_base")
base.__file__ = str(BASE_PATH)
exec(compile(BASE_BYTES, str(BASE_PATH), "exec"), base.__dict__)
core = base.core

DURABLE_ROOT = REPO.parent / "research-evidence/soga"
EVIDENCE_DIR = DURABLE_ROOT / "executions/demo-operator-v1"
STDOUT_PATH = EVIDENCE_DIR / "demo-operator-evidence.json"
STDERR_PATH = EVIDENCE_DIR / "demo-operator-stderr.bin"
RUN_RECORD_PATH = EVIDENCE_DIR / "run-record.json"
TIMEOUT_SECONDS = 90
STREAM_LIMIT_BYTES = 2_000_000
EXPECTED_TEST_COUNT = 93
CHILD_MODE = "M02_AAUTH_DEMO_OPERATOR_CHILD"
POSITIVE_RESULT = "AAUTH_DEMO_OPERATOR_TESTS_VERIFIED"
NEGATIVE_RESULT = "AAUTH_DEMO_OPERATOR_TESTS_FAILED"
EXECUTION_POSITIVE = "AAUTH_DEMO_OPERATOR_EXECUTION_POSITIVE"
EXECUTION_NEGATIVE = "AAUTH_DEMO_OPERATOR_EXECUTION_NEGATIVE"

HASHES = dict(base.HASHES)
HASHES.update({
    BASE_RELATIVE: BASE_SHA256,
    "m02_aauth_fcf656d/demo_operator.py":
        "b65160deffccf80220a0f466384a98ad1c3d21101dc44a1ee3b5d8099bf238a3",
    "tests/test_m02_aauth_demo_operator.py":
        "25abd4b5af7f8eaeaf1585d641bb8e08d024b2cabd09c685c0a319cad5b50f67",
})
TEST_MODULES = base.TEST_MODULES + (
    ("m02_demo_operator_tests", "tests/test_m02_aauth_demo_operator.py"),
)

base.HASHES = HASHES
core.HASHES = HASHES


def runner_state():
    path = Path(__file__).resolve()
    relative = str(path.relative_to(REPO))
    value = path.read_bytes()
    committed = subprocess.run(
        ["/usr/bin/git", "show", "HEAD:" + relative], cwd=REPO,
        env=core.BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    status = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--", relative], cwd=REPO,
        env=core.BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    if (committed.returncode != 0 or committed.stdout != value or
            status.returncode != 0 or status.stdout):
        raise RuntimeError("controller is not exact committed source")
    return {"path": relative, "sha256": core.digest(value)}


def child_main():
    sys.dont_write_bytecode = True
    script_dir = str(Path(__file__).resolve().parent)
    sys.path[:] = [item for item in sys.path if item not in ("", script_dir)]
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(core.PROVIDER_ROOT))
    socket_counts = core.install_socket_guard()
    suite = unittest.TestSuite()
    load_error = None
    try:
        for name, relative in TEST_MODULES:
            spec = importlib.util.spec_from_file_location(name, REPO / relative)
            if spec is None or spec.loader is None:
                raise RuntimeError("exact test module cannot be loaded")
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    except Exception as error:
        load_error = type(error).__name__
    stream = io.StringIO()
    if load_error is None:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        counts = {
            "tests_run": result.testsRun, "failures": len(result.failures),
            "errors": len(result.errors), "skips": len(result.skipped),
            "expected_failures": len(result.expectedFailures),
            "unexpected_successes": len(result.unexpectedSuccesses),
        }
    else:
        counts = {"tests_run": 0, "failures": 0, "errors": 1, "skips": 0,
                  "expected_failures": 0, "unexpected_successes": 0}
    report = core.redact(stream.getvalue())
    if "eyJ" in report or "resource-token=\"ey" in report:
        raise RuntimeError("redaction invariant failed")
    passed = (load_error is None and counts["tests_run"] == EXPECTED_TEST_COUNT and
              all(counts[name] == 0 for name in
                  ("failures", "errors", "skips", "expected_failures",
                   "unexpected_successes")) and socket_counts["bind"] > 0 and
              socket_counts["connect"] > 0)
    document = {
        "result": POSITIVE_RESULT if passed else NEGATIVE_RESULT,
        "expected_test_count": EXPECTED_TEST_COUNT, "counts": counts,
        "load_error_type": load_error, "socket_audit_counts": socket_counts,
        "module_origins": core.module_origins(), "report": report,
    }
    sys.stdout.write(json.dumps(document, sort_keys=True, separators=(",", ":")))
    return 0 if passed else 1


def parent_main():
    started = time.time()
    before = {"sources": core.protected_state(), "provider": core.provider_state(),
              "runner": runner_state()}
    if not DURABLE_ROOT.is_dir() or DURABLE_ROOT.is_symlink():
        raise RuntimeError("durable evidence root unavailable")
    if EVIDENCE_DIR.exists():
        raise RuntimeError("evidence directory already exists")
    EVIDENCE_DIR.mkdir(mode=0o700, parents=True)
    environment = dict(core.BASE_ENV)
    environment[CHILD_MODE] = "1"
    command = ["/usr/bin/python3", "-I", "-S", "-B", str(Path(__file__).resolve())]
    timed_out = False
    try:
        completed = subprocess.run(
            command, cwd=REPO, env=environment, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS, check=False)
        stdout = completed.stdout
        stderr = completed.stderr
        returncode = completed.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        returncode = None
    stdout_overflow = len(stdout) > STREAM_LIMIT_BYTES
    stderr_overflow = len(stderr) > STREAM_LIMIT_BYTES
    if not stdout_overflow:
        core.atomic_write(STDOUT_PATH, stdout)
    if not stderr_overflow:
        core.atomic_write(STDERR_PATH, stderr)
    try:
        parsed = json.loads(stdout.decode("utf-8"))
        parse_error = None
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        parsed = None
        parse_error = type(error).__name__
    try:
        after = {"sources": core.protected_state(), "provider": core.provider_state(),
                 "runner": runner_state()}
        if after != before:
            raise RuntimeError("protected state changed")
        post_error = None
    except Exception as error:
        after = None
        post_error = type(error).__name__ + ": " + str(error)
    stderr_allowed = (stderr == b"" or
                      (len(stderr) == core.ALLOWED_STDERR_LENGTH and
                       core.digest(stderr) == core.ALLOWED_STDERR_SHA256))
    positive = (not timed_out and not stdout_overflow and not stderr_overflow and
                returncode == 0 and stderr_allowed and isinstance(parsed, dict) and
                parsed.get("result") == POSITIVE_RESULT and post_error is None)
    record = {
        "result": EXECUTION_POSITIVE if positive else EXECUTION_NEGATIVE,
        "command": command, "started_at": started,
        "duration_seconds": time.time() - started, "timeout": timed_out,
        "returncode": returncode, "stdout_length": len(stdout),
        "stdout_sha256": core.digest(stdout), "stdout_overflow": stdout_overflow,
        "stdout_preserved": not stdout_overflow, "stderr_length": len(stderr),
        "stderr_sha256": core.digest(stderr), "stderr_allowed": stderr_allowed,
        "stderr_overflow": stderr_overflow, "stderr_preserved": not stderr_overflow,
        "parsed_result": parsed.get("result") if isinstance(parsed, dict) else None,
        "parse_error": parse_error, "post_verification_error": post_error,
        "source_state": before,
    }
    core.atomic_write(
        RUN_RECORD_PATH,
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
    return 0 if positive else 1


if __name__ == "__main__":
    raise SystemExit(child_main() if os.environ.get(CHILD_MODE) == "1" else parent_main())
