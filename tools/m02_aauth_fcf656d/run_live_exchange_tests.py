#!/usr/bin/env python3
"""Bounded controller for the exact D-110 AAuth live-exchange test package."""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest


REPO = Path("/Users/debb/dev/soga-clean")
PROVIDER_ROOT = Path(
    "/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages")
EVIDENCE_DIR = Path("/private/tmp/m02-aauth-fcf656d-live-exchange-20260924")
STDOUT_PATH = EVIDENCE_DIR / "live-exchange-test-evidence.json"
STDERR_PATH = EVIDENCE_DIR / "live-exchange-test-stderr.bin"
RUN_RECORD_PATH = EVIDENCE_DIR / "run-record.json"
TIMEOUT_SECONDS = 60
STREAM_LIMIT_BYTES = 2_000_000
EXPECTED_TEST_COUNT = 35
ALLOWED_STDERR_LENGTH = 110
ALLOWED_STDERR_SHA256 = (
    "2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61")
CHILD_MODE = "M02_AAUTH_LIVE_EXCHANGE_CHILD"
POSITIVE_RESULT = "AAUTH_LIVE_EXCHANGE_TESTS_VERIFIED"
NEGATIVE_RESULT = "AAUTH_LIVE_EXCHANGE_TESTS_FAILED"
PACKAGE_HASHES = {
    "m02_aauth_fcf656d/__init__.py":
        "c480bf75ecea51a368627cb00dabdd96ed9e48df784497ce9b7efee80f8f58e8",
    "m02_aauth_fcf656d/exchange.py":
        "ed82a97873f7c535917dd0ecbecf81e31287015c3dfbc77396cb3dc8675fdf0f",
    "m02_aauth_fcf656d/http_signatures.py":
        "f6ae4f4463852b310d09608d4a60084a566733e857098bcd42f2bc1a659cab65",
    "m02_aauth_fcf656d/identifiers.py":
        "54c495785fc5fc26d24e3c406bb334d0022410faff37696d40220e1b83759579",
    "m02_aauth_fcf656d/jose.py":
        "cda9b577746116e65c34977706593475a8637a3ec6823375dda7baffa961cdd4",
    "m02_aauth_fcf656d/metadata.py":
        "c1a473ee3f21ed4832668fadb87e9db72dbade4278f99aa35efff868db225a5a",
    "m02_aauth_fcf656d/profile.py":
        "fb7b9b51ada64c7e45f61eb24991078cbe5d172cdf781887bf6843c27fb7afbf",
    "m02_aauth_fcf656d/structured_fields.py":
        "9d774a03dd096577a9ce917b40f4c3693e30758319fa05f455feb3b734c78a71",
    "m02_aauth_fcf656d/tokens.py":
        "34f705123acb83772f9f2428409593233f004384c46b2cf96f0358615cf2dd04",
    "tests/test_m02_aauth_fcf656d.py":
        "89b71359c6c071453fab289aa85443aa4f7156e4a2d263d8ac12f85bee4deaad",
    "tests/test_m02_aauth_fcf656d_exchange.py":
        "89dcede33566a1531d9c5630d9598da940ffd7ac99dfb4610a875e3559aad916",
}
TEST_MODULES = (
    ("m02_phase1_focused_tests", "tests/test_m02_aauth_fcf656d.py"),
    ("m02_live_exchange_tests", "tests/test_m02_aauth_fcf656d_exchange.py"),
)
BASE_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C", "LC_ALL": "C",
    "GIT_OPTIONAL_LOCKS": "0", "PYTHONDONTWRITEBYTECODE": "1",
}
PROVIDER_PREFIXES = ("cryptography", "cffi", "_cffi_backend", "pycparser",
                     "typing_extensions")


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def source_state():
    state = {}
    for relative, expected in PACKAGE_HASHES.items():
        path = REPO / relative
        value = path.read_bytes()
        observed = sha256_bytes(value)
        if observed != expected:
            raise RuntimeError("protected source identity mismatch: " + relative)
        committed = subprocess.run(
            ["/usr/bin/git", "show", "HEAD:" + relative], cwd=REPO,
            env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=10, check=False)
        if committed.returncode != 0 or committed.stdout != value:
            raise RuntimeError("protected source is not committed: " + relative)
        state[relative] = observed
    status = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--"] + list(PACKAGE_HASHES),
        cwd=REPO, env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    if status.returncode != 0 or status.stdout:
        raise RuntimeError("protected source has working-tree changes")
    return state


def provider_state():
    if not PROVIDER_ROOT.is_dir() or PROVIDER_ROOT.is_symlink():
        raise RuntimeError("pinned provider root unavailable")
    required = (
        PROVIDER_ROOT / "cryptography/__init__.py",
        PROVIDER_ROOT / "cryptography/hazmat/bindings/_rust.abi3.so",
        PROVIDER_ROOT / "_cffi_backend.cpython-39-darwin.so",
    )
    result = {}
    for path in required:
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("pinned provider file unavailable")
        result[str(path.relative_to(PROVIDER_ROOT))] = sha256_bytes(path.read_bytes())
    return result


def runner_state():
    path = Path(__file__).resolve()
    relative = str(path.relative_to(REPO))
    value = path.read_bytes()
    committed = subprocess.run(
        ["/usr/bin/git", "show", "HEAD:" + relative], cwd=REPO,
        env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    if committed.returncode != 0 or committed.stdout != value:
        raise RuntimeError("controller is not committed at HEAD")
    status = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--", relative], cwd=REPO,
        env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    if status.returncode != 0 or status.stdout:
        raise RuntimeError("controller has working-tree changes")
    return {"path": relative, "sha256": sha256_bytes(value)}


def module_origins():
    origins = {}
    for name, module in sorted(sys.modules.items()):
        if not (name.startswith("m02_aauth_fcf656d") or
                name.startswith(PROVIDER_PREFIXES)):
            continue
        origin = getattr(module, "__file__", None)
        if not origin:
            continue
        resolved = Path(origin).resolve()
        if name.startswith("m02_aauth_fcf656d"):
            resolved.relative_to((REPO / "m02_aauth_fcf656d").resolve())
        else:
            resolved.relative_to(PROVIDER_ROOT.resolve())
        origins[name] = str(resolved)
    return origins


def redact_report(value):
    value = re.sub(r"eyJ[A-Za-z0-9._-]+", "<redacted-jws>", value)
    value = re.sub(r"(['\"]x['\"]\s*:\s*)['\"][A-Za-z0-9_-]+['\"]",
                   r"\1'<redacted-jwk-coordinate>'", value)
    value = re.sub(r"(?i)(signature(?:-key|-input)?\s*[:=]\s*)\S+",
                   r"\1<redacted-signature>", value)
    return value


def install_network_guard():
    forbidden = {"socket.__new__", "socket.bind", "socket.connect",
                 "socket.getaddrinfo", "socket.gethostbyname"}

    def guard(event, _arguments):
        if event in forbidden:
            raise RuntimeError("network operation prohibited: " + event)

    sys.addaudithook(guard)


def child_main():
    sys.dont_write_bytecode = True
    script_dir = str(Path(__file__).resolve().parent)
    sys.path[:] = [entry for entry in sys.path if entry not in ("", script_dir)]
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(PROVIDER_ROOT))
    install_network_guard()
    suite = unittest.TestSuite()
    load_error = None
    try:
        for module_name, relative in TEST_MODULES:
            spec = importlib.util.spec_from_file_location(module_name, REPO / relative)
            if spec is None or spec.loader is None:
                raise RuntimeError("unable to load exact test module")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
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
    report = redact_report(stream.getvalue())
    if "eyJ" in report:
        raise RuntimeError("redaction invariant failed")
    passed = (load_error is None and counts["tests_run"] == EXPECTED_TEST_COUNT
              and all(counts[name] == 0 for name in
                      ("failures", "errors", "skips", "expected_failures",
                       "unexpected_successes")))
    document = {
        "result": POSITIVE_RESULT if passed else NEGATIVE_RESULT,
        "expected_test_count": EXPECTED_TEST_COUNT, "counts": counts,
        "load_error_type": load_error, "module_origins": module_origins(),
        "report": report,
    }
    sys.stdout.write(json.dumps(document, sort_keys=True, separators=(",", ":")))
    return 0 if passed else 1


def atomic_write(path, value):
    partial = path.with_name(path.name + ".partial")
    with partial.open("xb") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())
    partial.chmod(0o400)
    partial.replace(path)


def parent_main():
    started = time.time()
    before = {"sources": source_state(), "provider": provider_state(),
              "runner": runner_state()}
    if EVIDENCE_DIR.exists():
        raise RuntimeError("evidence directory already exists")
    EVIDENCE_DIR.mkdir(mode=0o700)
    environment = dict(BASE_ENV)
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
        atomic_write(STDOUT_PATH, stdout)
    if not stderr_overflow:
        atomic_write(STDERR_PATH, stderr)
    parsed = None
    parse_error = None
    try:
        parsed = json.loads(stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        parse_error = type(error).__name__
    post_error = None
    try:
        after = {"sources": source_state(), "provider": provider_state(),
                 "runner": runner_state()}
        if after != before:
            raise RuntimeError("protected state changed")
    except Exception as error:
        after = None
        post_error = type(error).__name__ + ": " + str(error)
    stderr_allowed = (
        stderr == b"" or
        (len(stderr) == ALLOWED_STDERR_LENGTH and
         sha256_bytes(stderr) == ALLOWED_STDERR_SHA256))
    positive = (not timed_out and not stdout_overflow and not stderr_overflow
                and returncode == 0 and stderr_allowed
                and isinstance(parsed, dict) and parsed.get("result") == POSITIVE_RESULT
                and post_error is None)
    record = {
        "result": "AAUTH_LIVE_EXCHANGE_EXECUTION_POSITIVE" if positive else
                  "AAUTH_LIVE_EXCHANGE_EXECUTION_NEGATIVE",
        "command": command, "environment": {CHILD_MODE: "1"},
        "started_at": started, "duration_seconds": time.time() - started,
        "timeout": timed_out, "returncode": returncode,
        "stdout_overflow": stdout_overflow,
        "stdout_preserved": not stdout_overflow,
        "stdout_length": len(stdout), "stdout_sha256": sha256_bytes(stdout),
        "stderr_overflow": stderr_overflow,
        "stderr_preserved": not stderr_overflow,
        "stderr_allowed": stderr_allowed,
        "stderr_length": len(stderr), "stderr_sha256": sha256_bytes(stderr),
        "parsed_result": parsed.get("result") if isinstance(parsed, dict) else None,
        "parse_error": parse_error, "post_verification_error": post_error,
        "source_state": before,
    }
    atomic_write(RUN_RECORD_PATH,
                 json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return 0 if positive else 1


if __name__ == "__main__":
    raise SystemExit(child_main() if os.environ.get(CHILD_MODE) == "1" else parent_main())
