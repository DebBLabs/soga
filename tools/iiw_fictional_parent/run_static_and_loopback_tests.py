#!/usr/bin/env python3
"""Bounded future controller for the fictional-parent role-play package."""

import hashlib
import importlib.util
import io
import json
import os
import platform
from pathlib import Path
import subprocess
import sys
import time
import types
import unittest


REPO = Path(__file__).resolve().parents[2]
BASE_PATH = REPO / "tools/m02_aauth_fcf656d/run_demo_operator_tests.py"
BASE_RELATIVE = "tools/m02_aauth_fcf656d/run_demo_operator_tests.py"
BASE_SHA256 = "37bc90282e1cf99226c8ce8086b82644a5c429cb7048f6ff9048778bbd95e112"
VERIFICATION_ENV = {
    "GIT_OPTIONAL_LOCKS": "0", "LANG": "C", "LC_ALL": "C",
    "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
}
if not BASE_PATH.is_file() or BASE_PATH.is_symlink():
    raise RuntimeError("accepted demo-operator controller unavailable")
BASE_BYTES = BASE_PATH.read_bytes()
if hashlib.sha256(BASE_BYTES).hexdigest() != BASE_SHA256:
    raise RuntimeError("accepted demo-operator controller hash mismatch")
BASE_COMMITTED = subprocess.run(
    ["/usr/bin/git", "show", "HEAD:" + BASE_RELATIVE], cwd=REPO,
    env=VERIFICATION_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    timeout=10, check=False)
if BASE_COMMITTED.returncode != 0 or BASE_COMMITTED.stdout != BASE_BYTES:
    raise RuntimeError("accepted demo-operator controller is not committed")
base = types.ModuleType("iiw_fictional_parent_controller_base")
base.__file__ = str(BASE_PATH)
exec(compile(BASE_BYTES, str(BASE_PATH), "exec"), base.__dict__)
core = base.core

DURABLE_ROOT = REPO.parent / "research-evidence/soga"
EVIDENCE_DIR = DURABLE_ROOT / "executions/iiw-fictional-parent-v1"
STDOUT_PATH = EVIDENCE_DIR / "fictional-parent-evidence.json"
STDERR_PATH = EVIDENCE_DIR / "fictional-parent-stderr.bin"
RUN_RECORD_PATH = EVIDENCE_DIR / "run-record.json"
TIMEOUT_SECONDS = 90
STREAM_LIMIT_BYTES = 2_000_000
EXPECTED_TEST_COUNT = 128
CHILD_MODE = "IIW_FICTIONAL_PARENT_TEST_CHILD"
POSITIVE_RESULT = "IIW_FICTIONAL_PARENT_TESTS_VERIFIED"
NEGATIVE_RESULT = "IIW_FICTIONAL_PARENT_TESTS_FAILED"

HASHES = dict(base.HASHES)
HASHES.update({
    BASE_RELATIVE: BASE_SHA256,
    "iiw_qr_session/session.py":
        "2aeeb9bd0e355b2d19521665dbc94569058355e34b365d534282d78f423c7907",
    "iiw_qr_session/gateway.py":
        "9c5824df29ff0909d76e22c65af0ba277cda6d4c9370a720a2613d4256c6e3b8",
    "iiw_qr_session/package.py":
        "3f079c3bd7c834758a1062926f5083d556497ab8013a2426ea5bef95584495c9",
    "iiw_qr_session/README.md":
        "7d73b5c5dd0490031027059f31ca6ec1e942a628e54141b03e7b69178340e8f8",
    "tests/test_iiw_qr_session.py":
        "e700137956d85183a474d08ac7d67a2da2d073471acc65616ef31c7d4a113df4",
    "iiw_fictional_parent/session.py":
        "9e456f08bcc5351c9b47dd6e30809ae1cb16804505bbba77113fa65ec3c68972",
    "iiw_fictional_parent/connection.py":
        "d3cfec526e50d0443372d8b7ee66a269a8f61afdf36b86c33157b83c8a6cc24c",
    "iiw_fictional_parent/gateway.py":
        "6bb1c45424adb71008600e0ebf6bd988efe325c5111d557bddf8fba70b1e30f0",
    "iiw_fictional_parent/__init__.py":
        "98d94e37c9f0a72053e6f51835e464f4b4b8168d5cc69404098346a9aaca0ade",
    "iiw_fictional_parent/README.md":
        "ec58edd4fceafbecf51c7103f25591cb5f686c277a291ef2433b1e18ac3a3a92",
    "tests/test_iiw_fictional_parent.py":
        "e7bfe9af2b333f591b7f47b203782b5848283479036a99bc684714c5429d826c",
})
TEST_MODULES = base.TEST_MODULES + (
    ("iiw_qr_session_tests", "tests/test_iiw_qr_session.py"),
    ("iiw_fictional_parent_tests", "tests/test_iiw_fictional_parent.py"),
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


def exact_runtime_state():
    observed = {"system": platform.system(), "machine": platform.machine(),
                "python": platform.python_version(),
                "interpreter": sys.executable}
    expected = {"system": "Darwin", "machine": "arm64", "python": "3.9.6",
                "interpreter": "/Library/Developer/CommandLineTools/usr/bin/python3"}
    if observed != expected:
        raise RuntimeError("exact runtime identity mismatch")
    return observed


def package_origins():
    result = {}
    for name, module in sorted(sys.modules.items()):
        if not name.startswith(("iiw_fictional_parent", "iiw_qr_session")):
            continue
        value = getattr(module, "__file__", None)
        if value is None:
            result[name] = "namespace"
            continue
        resolved = Path(value).resolve()
        if REPO.resolve() not in resolved.parents:
            raise RuntimeError("package module origin escaped repository")
        result[name] = str(resolved.relative_to(REPO.resolve()))
    return result


def child_main():
    sys.dont_write_bytecode = True
    runtime = exact_runtime_state()
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
    forbidden = ("eyJ", "resource-token=\"ey", bytes(range(32)).hex(),
                 "q" * 32, "p" * 32)
    if any(value in report for value in forbidden):
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
        "module_origins": core.module_origins(),
        "package_origins": package_origins(), "runtime": runtime,
        "report": report,
    }
    sys.stdout.write(json.dumps(document, sort_keys=True, separators=(",", ":")))
    return 0 if passed else 1


def parent_main():
    started = time.time()
    before = {"sources": core.protected_state(), "provider": core.provider_state(),
              "runner": runner_state(), "runtime": exact_runtime_state()}
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
        stdout, stderr, returncode = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout, stderr, returncode = error.stdout or b"", error.stderr or b"", None
    stdout_overflow = len(stdout) > STREAM_LIMIT_BYTES
    stderr_overflow = len(stderr) > STREAM_LIMIT_BYTES
    if not stdout_overflow:
        core.atomic_write(STDOUT_PATH, stdout)
    if not stderr_overflow:
        core.atomic_write(STDERR_PATH, stderr)
    try:
        parsed, parse_error = json.loads(stdout.decode("utf-8")), None
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        parsed, parse_error = None, type(error).__name__
    try:
        after = {"sources": core.protected_state(), "provider": core.provider_state(),
                 "runner": runner_state(), "runtime": exact_runtime_state()}
        if after != before:
            raise RuntimeError("protected state changed")
        post_error = None
    except Exception as error:
        after, post_error = None, type(error).__name__ + ": " + str(error)
    stderr_allowed = (stderr == b"" or
                      (len(stderr) == core.ALLOWED_STDERR_LENGTH and
                       core.digest(stderr) == core.ALLOWED_STDERR_SHA256))
    positive = (not timed_out and not stdout_overflow and not stderr_overflow and
                returncode == 0 and stderr_allowed and isinstance(parsed, dict) and
                parsed.get("result") == POSITIVE_RESULT and post_error is None)
    record = {
        "result": "IIW_FICTIONAL_PARENT_EXECUTION_POSITIVE" if positive else
                  "IIW_FICTIONAL_PARENT_EXECUTION_NEGATIVE",
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
