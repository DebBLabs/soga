#!/usr/bin/env python3
"""Bounded controller for the D-116 localhost AAuth gateway package."""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
import unittest


REPO = Path("/Users/debb/dev/soga-clean")
PROVIDER_ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages")
EVIDENCE_DIR = Path("/private/tmp/m02-aauth-fcf656d-localhost-gateway-20260924")
STDOUT_PATH = EVIDENCE_DIR / "localhost-gateway-evidence.json"
STDERR_PATH = EVIDENCE_DIR / "localhost-gateway-stderr.bin"
RUN_RECORD_PATH = EVIDENCE_DIR / "run-record.json"
TIMEOUT_SECONDS = 90
STREAM_LIMIT_BYTES = 2_000_000
EXPECTED_TEST_COUNT = 53
CHILD_MODE = "M02_AAUTH_LOCALHOST_GATEWAY_CHILD"
POSITIVE_RESULT = "AAUTH_LOCALHOST_GATEWAY_TESTS_VERIFIED"
NEGATIVE_RESULT = "AAUTH_LOCALHOST_GATEWAY_TESTS_FAILED"
ALLOWED_STDERR_LENGTH = 110
ALLOWED_STDERR_SHA256 = "2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61"
HASHES = {
    "m02_aauth_fcf656d/__init__.py": "c480bf75ecea51a368627cb00dabdd96ed9e48df784497ce9b7efee80f8f58e8",
    "m02_aauth_fcf656d/exchange.py": "ed82a97873f7c535917dd0ecbecf81e31287015c3dfbc77396cb3dc8675fdf0f",
    "m02_aauth_fcf656d/http_signatures.py": "f6ae4f4463852b310d09608d4a60084a566733e857098bcd42f2bc1a659cab65",
    "m02_aauth_fcf656d/identifiers.py": "54c495785fc5fc26d24e3c406bb334d0022410faff37696d40220e1b83759579",
    "m02_aauth_fcf656d/jose.py": "cda9b577746116e65c34977706593475a8637a3ec6823375dda7baffa961cdd4",
    "m02_aauth_fcf656d/localhost.py": "095f01512efeb865208c21f11bd0b3864b3ba54166a1e3a72993bc5d8df2183b",
    "m02_aauth_fcf656d/metadata.py": "c1a473ee3f21ed4832668fadb87e9db72dbade4278f99aa35efff868db225a5a",
    "m02_aauth_fcf656d/profile.py": "fb7b9b51ada64c7e45f61eb24991078cbe5d172cdf781887bf6843c27fb7afbf",
    "m02_aauth_fcf656d/soga_supervision.py": "af1f19eb0710027d7c161e07e060813b9be3f578f252f2a9f3d7f942640dee6a",
    "m02_aauth_fcf656d/structured_fields.py": "9d774a03dd096577a9ce917b40f4c3693e30758319fa05f455feb3b734c78a71",
    "m02_aauth_fcf656d/tokens.py": "34f705123acb83772f9f2428409593233f004384c46b2cf96f0358615cf2dd04",
    "tests/test_m02_aauth_fcf656d.py": "89b71359c6c071453fab289aa85443aa4f7156e4a2d263d8ac12f85bee4deaad",
    "tests/test_m02_aauth_fcf656d_exchange.py": "89dcede33566a1531d9c5630d9598da940ffd7ac99dfb4610a875e3559aad916",
    "tests/test_m02_aauth_fcf656d_localhost.py": "b61bd0359c0d43eb23b51b537b96dd951bd05558ae4530e117cd28f6b537d2cc",
}
TEST_MODULES = (
    ("m02_phase1_tests", "tests/test_m02_aauth_fcf656d.py"),
    ("m02_exchange_tests", "tests/test_m02_aauth_fcf656d_exchange.py"),
    ("m02_localhost_tests", "tests/test_m02_aauth_fcf656d_localhost.py"),
)
BASE_ENV = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C", "LC_ALL": "C",
            "GIT_OPTIONAL_LOCKS": "0", "PYTHONDONTWRITEBYTECODE": "1"}


def digest(value):
    return hashlib.sha256(value).hexdigest()


def protected_state():
    result = {}
    for relative, expected in HASHES.items():
        value = (REPO / relative).read_bytes()
        if digest(value) != expected:
            raise RuntimeError("protected source mismatch: " + relative)
        committed = subprocess.run(
            ["/usr/bin/git", "show", "HEAD:" + relative], cwd=REPO, env=BASE_ENV,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=False)
        if committed.returncode != 0 or committed.stdout != value:
            raise RuntimeError("protected source is not committed: " + relative)
        result[relative] = expected
    status = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--"] + list(HASHES),
        cwd=REPO, env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    if status.returncode != 0 or status.stdout:
        raise RuntimeError("protected source has working-tree changes")
    return result


def provider_state():
    paths = (
        PROVIDER_ROOT / "cryptography/__init__.py",
        PROVIDER_ROOT / "cryptography/hazmat/bindings/_rust.abi3.so",
        PROVIDER_ROOT / "_cffi_backend.cpython-39-darwin.so",
    )
    if not PROVIDER_ROOT.is_dir() or PROVIDER_ROOT.is_symlink():
        raise RuntimeError("pinned provider unavailable")
    result = {}
    for path in paths:
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("pinned provider file unavailable")
        result[str(path.relative_to(PROVIDER_ROOT))] = digest(path.read_bytes())
    return result


def runner_state():
    path = Path(__file__).resolve()
    relative = str(path.relative_to(REPO))
    value = path.read_bytes()
    committed = subprocess.run(
        ["/usr/bin/git", "show", "HEAD:" + relative], cwd=REPO, env=BASE_ENV,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=False)
    status = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--", relative], cwd=REPO,
        env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    if committed.returncode != 0 or committed.stdout != value or status.returncode != 0 or status.stdout:
        raise RuntimeError("controller is not exact committed source")
    return {"path": relative, "sha256": digest(value)}


def install_socket_guard():
    counts = {"bind": 0, "connect": 0}
    resolution_events = {
        "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr"}
    address_events = {"socket.bind", "socket.connect"}
    allowed_events = {"socket.__new__"}

    def guard(event, arguments):
        if event in resolution_events:
            host = arguments[0] if arguments else None
            if host != "127.0.0.1":
                raise RuntimeError("name resolution prohibited")
            return
        if event in allowed_events:
            return
        if event.startswith("socket.") and event not in address_events:
            raise RuntimeError("unpermitted socket operation: " + event)
        if event not in address_events:
            return
        address = arguments[1] if len(arguments) > 1 else None
        if (not isinstance(address, tuple) or len(address) != 2 or
                address[0] != "127.0.0.1" or type(address[1]) is not int or
                address[1] < 0 or address[1] > 65535):
            raise RuntimeError("non-loopback socket operation prohibited")
        if event == "socket.bind" and address[1] != 0:
            raise RuntimeError("only ephemeral loopback bind is permitted")
        if event == "socket.connect" and address[1] == 0:
            raise RuntimeError("connection to port zero is prohibited")
        counts[event.removeprefix("socket.")] += 1

    sys.addaudithook(guard)
    return counts


def module_origins():
    repository_prefixes = ("m02_aauth_fcf656d", "engines", "input_adapters",
                           "verify", "advisory")
    provider_prefixes = ("cryptography", "cffi", "_cffi_backend", "pycparser",
                         "typing_extensions")
    result = {}
    for name, module in sorted(sys.modules.items()):
        origin = getattr(module, "__file__", None)
        if not origin:
            continue
        path = Path(origin).resolve()
        if name.startswith(repository_prefixes):
            path.relative_to(REPO)
            result[name] = str(path)
        elif name.startswith(provider_prefixes):
            path.relative_to(PROVIDER_ROOT)
            result[name] = str(path)
    return result


def redact(value):
    value = re.sub(r"eyJ[A-Za-z0-9._-]+", "<redacted-jws>", value)
    value = re.sub(r'(resource-token=")[^"]+("?)', r'\1<redacted-token>\2', value)
    value = re.sub(r"(['\"]x['\"]\s*:\s*)['\"][A-Za-z0-9_-]+['\"]",
                   r"\1'<redacted-jwk-coordinate>'", value)
    return value


def child_main():
    sys.dont_write_bytecode = True
    script_dir = str(Path(__file__).resolve().parent)
    sys.path[:] = [item for item in sys.path if item not in ("", script_dir)]
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(PROVIDER_ROOT))
    socket_counts = install_socket_guard()
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
        counts = {"tests_run": result.testsRun, "failures": len(result.failures),
                  "errors": len(result.errors), "skips": len(result.skipped),
                  "expected_failures": len(result.expectedFailures),
                  "unexpected_successes": len(result.unexpectedSuccesses)}
    else:
        counts = {"tests_run": 0, "failures": 0, "errors": 1, "skips": 0,
                  "expected_failures": 0, "unexpected_successes": 0}
    report = redact(stream.getvalue())
    if "eyJ" in report or "resource-token=\"ey" in report:
        raise RuntimeError("redaction invariant failed")
    passed = (load_error is None and counts["tests_run"] == EXPECTED_TEST_COUNT and
              all(counts[name] == 0 for name in
                  ("failures", "errors", "skips", "expected_failures",
                   "unexpected_successes")) and socket_counts["bind"] > 0 and
              socket_counts["connect"] > 0)
    document = {"result": POSITIVE_RESULT if passed else NEGATIVE_RESULT,
                "expected_test_count": EXPECTED_TEST_COUNT, "counts": counts,
                "load_error_type": load_error, "socket_audit_counts": socket_counts,
                "module_origins": module_origins(), "report": report}
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
    before = {"sources": protected_state(), "provider": provider_state(),
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
    try:
        parsed = json.loads(stdout.decode("utf-8"))
        parse_error = None
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        parsed, parse_error = None, type(error).__name__
    try:
        after = {"sources": protected_state(), "provider": provider_state(),
                 "runner": runner_state()}
        if after != before:
            raise RuntimeError("protected state changed")
        post_error = None
    except Exception as error:
        after, post_error = None, type(error).__name__ + ": " + str(error)
    stderr_allowed = (stderr == b"" or
                      (len(stderr) == ALLOWED_STDERR_LENGTH and
                       digest(stderr) == ALLOWED_STDERR_SHA256))
    positive = (not timed_out and not stdout_overflow and not stderr_overflow and
                returncode == 0 and stderr_allowed and isinstance(parsed, dict) and
                parsed.get("result") == POSITIVE_RESULT and post_error is None)
    record = {"result": "AAUTH_LOCALHOST_GATEWAY_EXECUTION_POSITIVE" if positive else
                         "AAUTH_LOCALHOST_GATEWAY_EXECUTION_NEGATIVE",
              "command": command, "started_at": started,
              "duration_seconds": time.time() - started, "timeout": timed_out,
              "returncode": returncode, "stdout_length": len(stdout),
              "stdout_sha256": digest(stdout), "stdout_overflow": stdout_overflow,
              "stdout_preserved": not stdout_overflow, "stderr_length": len(stderr),
              "stderr_sha256": digest(stderr), "stderr_allowed": stderr_allowed,
              "stderr_overflow": stderr_overflow, "stderr_preserved": not stderr_overflow,
              "parsed_result": parsed.get("result") if isinstance(parsed, dict) else None,
              "parse_error": parse_error, "post_verification_error": post_error,
              "source_state": before}
    atomic_write(RUN_RECORD_PATH,
                 json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
    return 0 if positive else 1


if __name__ == "__main__":
    raise SystemExit(child_main() if os.environ.get(CHILD_MODE) == "1" else parent_main())
