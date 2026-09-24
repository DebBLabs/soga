#!/usr/bin/env python3
"""Bounded controller for the AAuth fcf656d Phase 1 focused test suite."""

import ast
import hashlib
import io
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
RUNNER_RELATIVE = Path("tools/m02_aauth_fcf656d/run_phase1_tests.py")
TEST_RELATIVE = Path("tests/test_m02_aauth_fcf656d.py")
TEST_PATH = REPO / TEST_RELATIVE
PACKAGE_ROOT = REPO / "m02_aauth_fcf656d"
INSTALL_PARENT = Path("/private/tmp/m02-aauth-fcf656d-phase1-install-20260921")
PROVIDER_ROOT = INSTALL_PARENT / "site-packages"
WHEEL_ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels")
STATIC_EVIDENCE = Path(
    "/private/tmp/m02-aauth-fcf656d-static-recovery-20260921/"
    "static-verification-evidence.json")
D099_EVIDENCE = Path(
    "/private/tmp/m02-aauth-fcf656d-ed25519-provider-r2-20260921/"
    "provider-evidence.json")
D102_EVIDENCE = Path(
    "/private/tmp/m02-aauth-fcf656d-provider-extension-20260922/"
    "provider-extension-evidence.json")
EVIDENCE_DIR = Path("/private/tmp/m02-aauth-fcf656d-phase1-tests-rerun-20260924")
STDOUT_PATH = EVIDENCE_DIR / "phase1-test-evidence.json"
STDERR_PATH = EVIDENCE_DIR / "phase1-test-stderr.bin"
RUN_RECORD_PATH = EVIDENCE_DIR / "run-record.json"
TIMEOUT_SECONDS = 60
STREAM_LIMIT_BYTES = 2_000_000
CHILD_MODE = "M02_AAUTH_PHASE1_CHILD"
POSITIVE_RESULT = "AAUTH_PHASE1_TESTS_VERIFIED"
NEGATIVE_RESULT = "AAUTH_PHASE1_TESTS_FAILED"
ALLOWED_STDERR_LENGTH = 110
ALLOWED_STDERR_SHA256 = (
    "2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61")
EXPECTED_STATIC_SHA256 = (
    "fe66cc77cc1e4ceabcd99968fd6ab372c6b066b0f0e8c48291660e3636f792b0")
EXPECTED_D099_SHA256 = (
    "d6c7564e55e81fbc11931fb0306b9ce4c210f968fce587cc1f6919ebaba505fe")
EXPECTED_D102_SHA256 = (
    "8b4676330643dea6db04c23027bf0e002ca752514a409337712f6ad416a5da8c")
PACKAGE_HASHES = {
    "m02_aauth_fcf656d/__init__.py":
        "c480bf75ecea51a368627cb00dabdd96ed9e48df784497ce9b7efee80f8f58e8",
    "m02_aauth_fcf656d/http_signatures.py":
        "f6ae4f4463852b310d09608d4a60084a566733e857098bcd42f2bc1a659cab65",
    "m02_aauth_fcf656d/jose.py":
        "cda9b577746116e65c34977706593475a8637a3ec6823375dda7baffa961cdd4",
    "m02_aauth_fcf656d/metadata.py":
        "89d6bf45fa1183f23bb3b9af737004962c5d50298b2c7307cd99e1b83cca2653",
    "m02_aauth_fcf656d/profile.py":
        "fb7b9b51ada64c7e45f61eb24991078cbe5d172cdf781887bf6843c27fb7afbf",
    "m02_aauth_fcf656d/structured_fields.py":
        "9d774a03dd096577a9ce917b40f4c3693e30758319fa05f455feb3b734c78a71",
    "tests/test_m02_aauth_fcf656d.py":
        "89b71359c6c071453fab289aa85443aa4f7156e4a2d263d8ac12f85bee4deaad",
}
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
BASE_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C", "LC_ALL": "C",
    "GIT_OPTIONAL_LOCKS": "0", "PYTHONDONTWRITEBYTECODE": "1",
}
PROVIDER_PREFIXES = ("cryptography", "cffi", "_cffi_backend", "pycparser",
                     "typing_extensions")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


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
        check=True, capture_output=True, timeout=10, env=BASE_ENV)
    return completed.stdout


def committed_blob(relative):
    return git_bytes(["show", "HEAD:" + str(relative)])


def verify_json(path, digest, result):
    require(regular_nonsymlink(path), "accepted evidence absent or unsafe")
    require(sha256(path) == digest, "accepted evidence hash mismatch")
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict) and value.get("result") == result,
            "accepted evidence result mismatch")


def verify_sources(require_runner_committed):
    protected = {str(RUNNER_RELATIVE), *PACKAGE_HASHES.keys()}
    status = git_bytes(["status", "--porcelain", "--untracked-files=all"])
    status_lines = status.decode("utf-8", errors="strict").splitlines()
    for line in status_lines:
        payload = line[3:] if len(line) >= 3 else ""
        require(not any(path in protected for path in payload.split(" -> ")),
                "protected source has a working-tree entry")
    observed = {}
    for relative_text, digest in PACKAGE_HASHES.items():
        relative = Path(relative_text)
        blob = committed_blob(relative)
        path = REPO / relative
        require(regular_nonsymlink(path), "protected source absent or unsafe")
        require(sha256_bytes(blob) == digest and path.read_bytes() == blob,
                "protected source identity mismatch: " + relative_text)
        observed[relative_text] = digest
    runner_hash = None
    if require_runner_committed:
        runner_blob = committed_blob(RUNNER_RELATIVE)
        require(RUNNER.read_bytes() == runner_blob, "controller differs from committed blob")
        runner_hash = sha256_bytes(runner_blob)
    return {
        "head": git_bytes(["rev-parse", "HEAD"]).decode("ascii").strip(),
        "status_porcelain": status_lines, "source_sha256": observed,
        "controller_sha256": runner_hash,
    }


def verify_preserved_inputs():
    require(directory_nonsymlink(INSTALL_PARENT), "installation parent absent or unsafe")
    require(directory_nonsymlink(PROVIDER_ROOT), "provider root absent or unsafe")
    require(directory_nonsymlink(WHEEL_ROOT), "wheel root absent or unsafe")
    verify_json(STATIC_EVIDENCE, EXPECTED_STATIC_SHA256,
                "STATIC_INSTALLATION_VERIFIED")
    verify_json(D099_EVIDENCE, EXPECTED_D099_SHA256,
                "ED25519_PROVIDER_VERIFIED")
    verify_json(D102_EVIDENCE, EXPECTED_D102_SHA256,
                "ED25519_PROVIDER_EXTENSION_VERIFIED")
    with open(STATIC_EVIDENCE, "r", encoding="utf-8") as handle:
        baseline = json.load(handle)
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
    for filename, size, digest in WHEELS:
        path = WHEEL_ROOT / filename
        require(regular_nonsymlink(path), "wheel absent or unsafe: " + filename)
        require(path.stat().st_size == size and sha256(path) == digest,
                "wheel identity mismatch: " + filename)
    return {"inventory_entries_verified": len(inventory),
            "wheel_count_verified": len(WHEELS),
            "static_evidence_sha256": EXPECTED_STATIC_SHA256,
            "d099_evidence_sha256": EXPECTED_D099_SHA256,
            "d102_evidence_sha256": EXPECTED_D102_SHA256}


def count_test_methods():
    tree = ast.parse(TEST_PATH.read_text(encoding="utf-8"), filename=str(TEST_PATH))
    return sum(
        1 for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_"))


def module_origins():
    provider_root = PROVIDER_ROOT.resolve()
    package_root = PACKAGE_ROOT.resolve()
    origins = {}
    for name, module in sorted(sys.modules.items()):
        origin = getattr(module, "__file__", None)
        if name.startswith(PROVIDER_PREFIXES):
            if origin is None:
                origins[name] = "<no file origin: built-in or extension submodule>"
            else:
                resolved = Path(origin).resolve()
                require(provider_root in resolved.parents,
                        "provider module escaped pinned root: " + name)
                origins[name] = str(resolved)
        elif name == "m02_aauth_fcf656d" or name.startswith("m02_aauth_fcf656d."):
            require(origin is not None, "candidate module lacks file origin: " + name)
            resolved = Path(origin).resolve()
            require(package_root == resolved.parent or package_root in resolved.parents,
                    "candidate module escaped package root: " + name)
            origins[name] = str(resolved)
        elif origin is not None:
            try:
                resolved = Path(origin).resolve()
            except (OSError, RuntimeError):
                continue
            if REPO.resolve() in resolved.parents:
                require(resolved in (TEST_PATH.resolve(), RUNNER.resolve()),
                        "unexpected repository package imported: " + name)
    require(any(name.startswith("cryptography") for name in origins),
            "cryptography modules were not observed")
    require(any(name.startswith("m02_aauth_fcf656d") for name in origins),
            "candidate modules were not observed")
    return origins


def redact_report(report):
    redacted_lines = []
    for line in report.splitlines(keepends=True):
        for marker, replacement in (
                ("(token=", "(token=<redacted-compact-jws>)"),
                ("(jwk=", "(jwk=<redacted-public-jwk>)"),
                ("(changed=Request(", "(changed=<redacted-signed-request>)")):
            if marker in line:
                line = line.split(marker, 1)[0] + replacement + "\n"
        redacted_lines.append(line)
    report = "".join(redacted_lines)
    require("eyJ" not in report, "redacted report retains compact-JWS prefix")
    require("'x':" not in report and '"x":' not in report,
            "redacted report retains JWK coordinate")
    require("signature-key" not in report and "signature-input" not in report,
            "redacted report retains signed-request headers")
    return report


def child_main():
    require(len(sys.argv) == 1, "no command-line arguments permitted")
    script_dir = str(RUNNER.resolve().parent)
    sys.path[:] = [entry for entry in sys.path if entry not in ("", script_dir)]
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(PROVIDER_ROOT))
    import importlib.util
    import unittest
    expected_count = count_test_methods()
    stream = io.StringIO()
    counts = {"tests_run": 0, "failures": 0, "errors": 0, "skips": 0,
              "expected_failures": 0, "unexpected_successes": 0}
    report = ""
    load_error = None
    result = None
    try:
        spec = importlib.util.spec_from_file_location(
            "m02_phase1_focused_tests", str(TEST_PATH))
        require(spec is not None and spec.loader is not None,
                "focused test module cannot be loaded")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        require(suite.countTestCases() == expected_count,
                "loaded suite count differs from independent count")
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        counts = {
            "tests_run": result.testsRun, "failures": len(result.failures),
            "errors": len(result.errors), "skips": len(result.skipped),
            "expected_failures": len(result.expectedFailures),
            "unexpected_successes": len(result.unexpectedSuccesses),
        }
        report = redact_report(stream.getvalue())
    except Exception as error:
        load_error = type(error).__module__ + "." + type(error).__qualname__
        report = redact_report(stream.getvalue())
    origins = module_origins() if result is not None else {}
    positive = (
        load_error is None and counts["tests_run"] == expected_count
        and all(counts[name] == 0 for name in (
            "failures", "errors", "skips", "expected_failures",
            "unexpected_successes")))
    document = {
        "result": POSITIVE_RESULT if positive else NEGATIVE_RESULT,
        "expected_test_count": expected_count, "counts": counts,
        "load_error_type": load_error, "module_origins": origins,
        "report": report,
    }
    print(json.dumps(document, sort_keys=True, separators=(",", ":")))
    return 0 if positive else 1


def safe_child_main():
    try:
        return child_main()
    except BaseException as error:
        document = {
            "result": NEGATIVE_RESULT,
            "expected_test_count": None,
            "counts": {"tests_run": 0, "failures": 0, "errors": 1,
                       "skips": 0, "expected_failures": 0,
                       "unexpected_successes": 0},
            "load_error_type": type(error).__module__ + "." + type(error).__qualname__,
            "module_origins": {}, "report": "",
        }
        print(json.dumps(document, sort_keys=True, separators=(",", ":")))
        return 1


def atomic_write(path, content, mode):
    temporary = path.with_name(path.name + ".partial")
    with open(temporary, "xb") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def controller_main():
    require(len(sys.argv) == 1, "no command-line arguments permitted")
    require(regular_nonsymlink(RUNNER), "controller absent or unsafe")
    repository_before = verify_sources(require_runner_committed=True)
    preserved_before = verify_preserved_inputs()
    version = subprocess.run(
        ["/usr/bin/python3", "--version"], check=True, capture_output=True,
        timeout=10, env=BASE_ENV)
    version_stderr_hash = sha256_bytes(version.stderr)
    version_stderr_allowed = (
        version.stderr == b"" or
        (len(version.stderr) == ALLOWED_STDERR_LENGTH
         and version_stderr_hash == ALLOWED_STDERR_SHA256))
    require(version.stdout == b"Python 3.9.6\n" and version_stderr_allowed,
            "interpreter version or diagnostic mismatch")
    expected_count = count_test_methods()
    require(expected_count > 0, "no focused test methods found")
    require(not EVIDENCE_DIR.exists() and not EVIDENCE_DIR.is_symlink(),
            "evidence directory already exists")
    EVIDENCE_DIR.mkdir(mode=0o700)
    command = ["/usr/bin/python3", "-I", "-S", "-B", str(RUNNER)]
    child_env = dict(BASE_ENV)
    child_env[CHILD_MODE] = "1"
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
            timeout=TIMEOUT_SECONDS, check=False, env=child_env)
        stdout, stderr, exit_status = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout, stderr = error.stdout or b"", error.stderr or b""
        launch_error = "focused test child timed out"
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
        error_text = "focused test output exceeds bound"
    if error_text is None:
        try:
            decoded = stdout.decode("utf-8", errors="strict")
            parsed, end = json.JSONDecoder().raw_decode(decoded)
            require(decoded[end:].strip() == "", "stdout contains multiple JSON values")
            require(isinstance(parsed, dict), "stdout JSON is not an object")
            require(parsed.get("result") in {POSITIVE_RESULT, NEGATIVE_RESULT},
                    "unexpected focused-test result")
        except Exception as error:
            error_text = type(error).__name__ + ": " + str(error)
    stderr_hash = sha256_bytes(stderr)
    pinned_stderr = len(stderr) == ALLOWED_STDERR_LENGTH and stderr_hash == ALLOWED_STDERR_SHA256
    if error_text is None and stderr != b"" and not pinned_stderr:
        error_text = "stderr is neither empty nor the pinned Darwin diagnostic"
    post_error = None
    repository_after = None
    preserved_after = None
    try:
        repository_after = verify_sources(require_runner_committed=True)
        preserved_after = verify_preserved_inputs()
        require(repository_after["source_sha256"] == repository_before["source_sha256"],
                "protected source changed during execution")
        require(preserved_after == preserved_before,
                "preserved inputs changed during execution")
    except Exception as error:
        post_error = type(error).__name__ + ": " + str(error)
    counts = parsed.get("counts", {}) if isinstance(parsed, dict) else {}
    positive = (
        error_text is None and post_error is None and exit_status == 0
        and parsed.get("result") == POSITIVE_RESULT
        and parsed.get("expected_test_count") == expected_count
        and counts.get("tests_run") == expected_count
        and all(counts.get(name) == 0 for name in (
            "failures", "errors", "skips", "expected_failures",
            "unexpected_successes")))
    if not positive and error_text is None:
        error_text = "focused tests returned a negative result"
    record = {
        "result": "AAUTH_PHASE1_TEST_EXECUTION_POSITIVE" if positive else "FAILED",
        "error": error_text, "post_verification_error": post_error,
        "started_at": started_at, "finished_at": utc_now(),
        "duration_seconds": round(time.monotonic() - started, 6),
        "timeout": timed_out, "timeout_seconds": TIMEOUT_SECONDS,
        "stream_limit_bytes": STREAM_LIMIT_BYTES, "exit_status": exit_status,
        "stdout_length": len(stdout), "stdout_sha256": sha256_bytes(stdout),
        "stdout_preserved": not stdout_overflow,
        "stderr_length": len(stderr), "stderr_sha256": stderr_hash,
        "stderr_preserved": not stderr_overflow,
        "pinned_darwin_stderr_matched": pinned_stderr,
        "parsed_result": parsed.get("result") if isinstance(parsed, dict) else None,
        "expected_test_count": expected_count, "counts": counts,
        "module_origins": parsed.get("module_origins", {})
        if isinstance(parsed, dict) else {},
        "command": command, "environment": child_env,
        "repository_before": repository_before,
        "repository_after": repository_after,
        "preserved_inputs_before": preserved_before,
        "preserved_inputs_after": preserved_after,
    }
    atomic_write(RUN_RECORD_PATH,
                 (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode(),
                 0o400)
    return 0 if positive else 1


if __name__ == "__main__":
    if os.environ.get(CHILD_MODE) == "1":
        raise SystemExit(safe_child_main())
    raise SystemExit(controller_main())
