#!/usr/bin/env python3
"""Create-only bounded controller; execution requires separate authorization."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import types
import unittest


REPO = Path(__file__).resolve().parents[2]
TIMEOUT_SECONDS = 60
STREAM_LIMIT_BYTES = 1_000_000
EXPECTED_TEST_COUNT = 17
CHILD_MODE = "IIW_QR_SESSION_TEST_CHILD"
SOURCE_HASHES = {
    "iiw_qr_session/session.py":
        "2aeeb9bd0e355b2d19521665dbc94569058355e34b365d534282d78f423c7907",
    "iiw_qr_session/gateway.py":
        "9c5824df29ff0909d76e22c65af0ba277cda6d4c9370a720a2613d4256c6e3b8",
    "iiw_qr_session/package.py":
        "3f079c3bd7c834758a1062926f5083d556497ab8013a2426ea5bef95584495c9",
    "tests/test_iiw_qr_session.py":
        "e700137956d85183a474d08ac7d67a2da2d073471acc65616ef31c7d4a113df4",
    "iiw_qr_session/README.md":
        "7d73b5c5dd0490031027059f31ca6ec1e942a628e54141b03e7b69178340e8f8",
}
BASE_ENV = {
    "GIT_OPTIONAL_LOCKS": "0", "LANG": "C", "LC_ALL": "C",
    "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
}


def digest(value):
    return hashlib.sha256(value).hexdigest()


def source_state():
    result = {}
    for relative, expected in SOURCE_HASHES.items():
        path = REPO / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("required source is not a regular file")
        value = path.read_bytes()
        observed = digest(value)
        if observed != expected:
            raise RuntimeError("required source hash mismatch")
        committed = subprocess.run(
            ["/usr/bin/git", "show", "HEAD:" + relative], cwd=REPO,
            env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=10, check=False)
        if committed.returncode != 0 or committed.stdout != value:
            raise RuntimeError("required source is not exact committed source")
        result[relative] = observed
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
        raise RuntimeError("controller is not exact committed source")
    return {"path": relative, "sha256": digest(value)}


def tracked_state():
    completed = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--untracked-files=no"],
        cwd=REPO, env=BASE_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=10, check=False)
    if completed.returncode != 0 or completed.stderr or completed.stdout:
        raise RuntimeError("tracked repository state is not clean")
    return digest(completed.stdout)


def runtime_state():
    bundle_text = os.environ.get("IIW_QR_BUNDLE_ROOT", "")
    manifest_text = os.environ.get("IIW_QR_RUNTIME_MANIFEST", "")
    if not bundle_text or not manifest_text:
        raise RuntimeError("bundle root and runtime manifest are required")
    bundle = Path(bundle_text)
    manifest = Path(manifest_text)
    if bundle.resolve(strict=True) != REPO.resolve(strict=True):
        raise RuntimeError("runtime bundle root mismatch")
    namespace = types.ModuleType("iiw_qr_session")
    namespace.__path__ = [str(REPO / "iiw_qr_session")]
    namespace.__package__ = "iiw_qr_session"
    sys.modules["iiw_qr_session"] = namespace
    sys.path.insert(0, str(REPO))
    try:
        from iiw_qr_session.package import validate_manifest
        value = validate_manifest(bundle, manifest)
    finally:
        if sys.path and sys.path[0] == str(REPO):
            sys.path.pop(0)
    return {"manifest_sha256": digest(manifest.read_bytes()),
            "system": value["system"], "machine": value["machine"],
            "python": value["python"]}


def install_socket_guard():
    counts = {"bind": 0, "connect": 0}
    original_bind = socket.socket.bind
    original_connect = socket.socket.connect

    def checked(address):
        if not (isinstance(address, tuple) and len(address) >= 2 and
                address[0] == "127.0.0.1"):
            raise RuntimeError("non-loopback socket attempt")

    def guarded_bind(instance, address):
        checked(address)
        counts["bind"] += 1
        return original_bind(instance, address)

    def guarded_connect(instance, address):
        checked(address)
        counts["connect"] += 1
        return original_connect(instance, address)

    socket.socket.bind = guarded_bind
    socket.socket.connect = guarded_connect
    return counts


def child_main():
    sys.dont_write_bytecode = True
    source_state()
    runtime = runtime_state()
    script_dir = str(Path(__file__).resolve().parent)
    sys.path[:] = [entry for entry in sys.path if entry not in ("", script_dir)]
    sys.path.insert(0, str(REPO))
    socket_counts = install_socket_guard()
    spec = importlib.util.spec_from_file_location(
        "iiw_qr_session_tests", REPO / "tests/test_iiw_qr_session.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("test module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    counts = {"tests_run": result.testsRun, "failures": len(result.failures),
              "errors": len(result.errors), "skips": len(result.skipped)}
    passed = (counts == {"tests_run": EXPECTED_TEST_COUNT, "failures": 0,
                         "errors": 0, "skips": 0} and
              socket_counts["bind"] > 0 and socket_counts["connect"] > 0)
    report = stream.getvalue()
    secrets_forbidden = (
        bytes(range(32)).hex(), "adult-demo-participant", "127.0.0.1", "eyJ")
    if any(secret in report for secret in secrets_forbidden):
        raise RuntimeError("evidence leakage detected")
    sys.stdout.write(json.dumps({
        "result": "IIW_QR_SESSION_TESTS_VERIFIED" if passed else "IIW_QR_SESSION_TESTS_FAILED",
        "counts": counts, "socket_audit_counts": socket_counts,
        "source_hashes": source_state(), "runtime": runtime, "report": report,
    }, sort_keys=True, separators=(",", ":")))
    return 0 if passed else 1


def parent_main():
    output_root_text = os.environ.get("IIW_QR_EVIDENCE_DIR", "")
    if not output_root_text:
        raise RuntimeError("operator-selected durable evidence directory required")
    output_root = Path(output_root_text)
    if output_root.exists() or not output_root.is_absolute():
        raise RuntimeError("evidence directory must be absent and absolute")
    parent = output_root.parent
    if (not parent.is_dir() or parent.is_symlink() or
            REPO.resolve() == parent.resolve() or REPO.resolve() in parent.resolve().parents):
        raise RuntimeError("evidence parent must be durable and outside source bundle")
    before = {"sources": source_state(), "runner": runner_state(),
              "tracked": tracked_state(), "runtime": runtime_state()}
    output_root.mkdir(mode=0o700, parents=False)
    environment = dict(BASE_ENV)
    environment[CHILD_MODE] = "1"
    environment["IIW_QR_BUNDLE_ROOT"] = os.environ["IIW_QR_BUNDLE_ROOT"]
    environment["IIW_QR_RUNTIME_MANIFEST"] = os.environ["IIW_QR_RUNTIME_MANIFEST"]
    started = time.time()
    timed_out = False
    try:
        completed = subprocess.run(
            ["/usr/bin/python3", "-I", "-S", "-B", str(Path(__file__).resolve())],
            cwd=REPO, env=environment, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS, check=False)
        stdout, stderr, returncode = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        returncode = None
    overflow = len(stdout) > STREAM_LIMIT_BYTES or len(stderr) > STREAM_LIMIT_BYTES
    stdout = stdout[:STREAM_LIMIT_BYTES]
    stderr = stderr[:STREAM_LIMIT_BYTES]
    after = {"sources": source_state(), "runner": runner_state(),
             "tracked": tracked_state(), "runtime": runtime_state()}
    if before != after:
        raise RuntimeError("source mutation detected")
    (output_root / "stdout.json").write_bytes(stdout)
    (output_root / "stderr.bin").write_bytes(stderr)
    payload = None
    try:
        payload = json.loads(stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass
    positive = (not timed_out and not overflow and returncode == 0 and stderr == b"" and
                isinstance(payload, dict) and
                payload.get("result") == "IIW_QR_SESSION_TESTS_VERIFIED")
    record = {
        "returncode": returncode, "timed_out": timed_out,
        "output_overflow": overflow, "positive": positive,
        "elapsed_seconds": round(time.time() - started, 6),
        "stdout_sha256": digest(stdout),
        "stderr_sha256": digest(stderr),
        "source_hashes": after,
    }
    (output_root / "run-record.json").write_text(
        json.dumps(record, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    return 0 if positive else 1


if __name__ == "__main__":
    raise SystemExit(child_main() if os.environ.get(CHILD_MODE) == "1" else parent_main())

