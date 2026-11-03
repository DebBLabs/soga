#!/usr/bin/python3
"""Bounded synthetic-test controller for the Misty-first shared gateway.

This controller is intentionally not a public-demo launcher.  It runs only the
reviewed local test module in an isolated child, denies network/process/write
operations in that child, and creates a bounded durable evidence package.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time


REPOSITORY = Path("/Users/debb/dev/soga-clean")
PRESENTATION = Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak")
MANIFEST = REPOSITORY / "tools/robot_gateway/misty-phase-runtime-manifest.json"
MANIFEST_SHA256 = "27c0758984fa0653652d52cd8d47c45276fe357a6888f0f9b232c5037bd45aa6"
INTERPRETER = "/usr/bin/python3"
TIMEOUT_SECONDS = 60
MAX_STREAM_BYTES = 2_000_000
EXPECTED_TEST_COUNT = 34
EVIDENCE_DIRECTORY = Path(
    "/Users/debb/dev/research-evidence/soga/evidence/iiw-misty-gateway-static-v1"
)
EXCLUDED_UNTRACKED = (
    "knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md"
)
PACKAGE_PATHS = {
    "robot_gateway/README.md",
    "robot_gateway/__init__.py",
    "robot_gateway/coordinator.py",
    "robot_gateway/gateway.py",
    "robot_gateway/misty_invitation.py",
    "robot_gateway/strict_json_post.py",
    "robot_gateway/unavailable_mbot2.py",
    "tests/test_robot_gateway_misty_phase.py",
    "tools/robot_gateway/run_static_and_synthetic_tests.py",
    "tools/robot_gateway/misty-phase-runtime-manifest.json",
}
ALLOWED_COMMIT_PATHS = PACKAGE_PATHS | {
    "knowledge/strategy/DECISION_LOG.md",
    "knowledge/working/CURRENT_STATE.md",
}

PRESENTATION_SHA256 = {
    "bridge.py": "b044191e767084c1e6ac4d272eb756aa4fee1370cea3c0cbd5ab75b4ffb4754b",
    "index.html": "60c54ee203225797a1f026a17bbdfddb73a7ca8c8ececf7cf882eb3cd4286da7",
    "Start IIW Table.command": "27c0be9b8ecd4ba42dbac6a6a8055cdcc2209cefee735a8cffdb0cfb9a4356ac",
    "IIW_TABLE_OPERATOR_CHECKLIST.md": "04e2fa1c2d34d18121b81749bc6dca6c44ff7dbca422c4868032c5f43170b127",
}

ACCEPTED_EVIDENCE_SHA256 = {
    "/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v11/evidence.json": "b863e09dede1dfe0462ebbfa12c2ce6e6e7dfb439874e750b5d831659885d9d5",
    "/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v11/bridge.stdout.txt": "669f6f984ee8699fb3182f69a635523b8a6b4047ac7fc77f9c1232f55fd2b81d",
    "/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v11/bridge.stderr.txt": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "/Users/debb/dev/soga-clean/knowledge/research/IIW_FLOW_A_BERYL_IPAD_V11_REHEARSAL_EVIDENCE_2026-11-02.md": "4885723c1f04dce61b257f3dd01b6935604f0bb6d39c52ffc91efff89358a14a",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_output(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["/usr/bin/git", "-C", str(repository), *arguments],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("git observation failed")
    return completed.stdout.decode("utf-8", "strict")


def repository_status() -> list[str]:
    lines = git_output(REPOSITORY, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    permitted = {"?? " + EXCLUDED_UNTRACKED}
    unexpected = [line for line in lines if line not in permitted]
    if unexpected:
        raise RuntimeError("SOGA working tree differs from reviewed execution boundary")
    return lines


def verify_repository_basis(source_basis: str) -> dict[str, object]:
    git_output(REPOSITORY, "merge-base", "--is-ancestor", source_basis, "HEAD")
    changed = set(
        git_output(REPOSITORY, "diff", "--name-only", source_basis + "..HEAD").splitlines()
    )
    if not PACKAGE_PATHS.issubset(changed) or not changed.issubset(ALLOWED_COMMIT_PATHS):
        raise RuntimeError("committed package differs from reviewed source basis")
    return {"source_basis": source_basis, "head": git_output(REPOSITORY, "rev-parse", "HEAD").strip(), "changed_paths": sorted(changed)}


def presentation_status() -> list[str]:
    lines = git_output(PRESENTATION, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    if lines:
        raise RuntimeError("presentation working tree is not clean")
    return lines


def verify_hash_map(root: Path, expected: dict[str, str]) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, wanted in sorted(expected.items()):
        path = root / relative
        actual = sha256(path)
        if actual != wanted:
            raise RuntimeError("protected hash mismatch: " + relative)
        observed[relative] = actual
    return observed


def verify_absolute_hash_map(expected: dict[str, str]) -> dict[str, str]:
    observed: dict[str, str] = {}
    for raw_path, wanted in sorted(expected.items()):
        actual = sha256(Path(raw_path))
        if actual != wanted:
            raise RuntimeError("accepted evidence hash mismatch: " + raw_path)
        observed[raw_path] = actual
    return observed


def load_manifest() -> dict[str, object]:
    if sha256(MANIFEST) != MANIFEST_SHA256:
        raise RuntimeError("runtime manifest hash mismatch")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    exact = {
        "presentation_basis": git_output(PRESENTATION, "rev-parse", "HEAD").strip(),
        "expected_test_count": EXPECTED_TEST_COUNT,
        "interpreter": INTERPRETER,
        "timeout_seconds": TIMEOUT_SECONDS,
        "max_stream_bytes": MAX_STREAM_BYTES,
        "evidence_directory": str(EVIDENCE_DIRECTORY),
    }
    for key, actual in exact.items():
        if data.get(key) != actual:
            raise RuntimeError("manifest/controller mismatch: " + key)
    if data.get("presentation_sha256") != PRESENTATION_SHA256:
        raise RuntimeError("manifest/controller presentation pins differ")
    if data.get("accepted_evidence_sha256") != ACCEPTED_EVIDENCE_SHA256:
        raise RuntimeError("manifest/controller evidence pins differ")
    source_basis = data.get("repository_basis")
    if not isinstance(source_basis, str):
        raise RuntimeError("manifest repository basis is invalid")
    verify_repository_basis(source_basis)
    return data


CHILD = r'''
import os
import sys

def deny(event, args):
    if event in {"socket.connect", "socket.bind", "socket.listen", "socket.getaddrinfo",
                 "socket.gethostbyaddr", "socket.gethostbyname", "socket.sendto", "socket.sendmsg",
                 "subprocess.Popen", "os.system", "os.fork", "os.forkpty",
                 "os.exec", "os.posix_spawn", "os.posix_spawnp", "os.spawn"}:
        raise PermissionError("operation denied by bounded test audit policy")
    if event in {"os.remove", "os.rename", "os.rmdir", "os.mkdir", "os.link", "os.symlink",
                 "os.truncate", "os.chmod", "os.chown", "os.utime"}:
        raise PermissionError("filesystem mutation denied by bounded test audit policy")
    if event == "open" and len(args) >= 2:
        mode = args[1]
        flags = args[2] if len(args) >= 3 else 0
        if (isinstance(mode, str) and any(c in mode for c in "wax+")) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
        ):
            raise PermissionError("write denied by bounded test audit policy")

sys.addaudithook(deny)
sys.path.insert(0, "/Users/debb/dev/soga-clean")
import unittest
suite = unittest.defaultTestLoader.loadTestsFromName("tests.test_robot_gateway_misty_phase")
if suite.countTestCases() != 34:
    raise SystemExit("unexpected test count")
result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
'''


def bounded_child() -> tuple[int | None, bytes, bytes, str]:
    process = subprocess.Popen(
        [INTERPRETER, "-I", "-B", "-c", CHILD],
        cwd=str(REPOSITORY),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"},
    )
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    streams = {process.stdout: bytearray(), process.stderr: bytearray()}
    for stream in streams:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ)
    deadline = time.monotonic() + TIMEOUT_SECONDS
    outcome = "completed"
    while selector.get_map():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            outcome = "timeout"
            os.killpg(process.pid, signal.SIGKILL)
            break
        for key, _ in selector.select(min(remaining, 0.25)):
            stream = key.fileobj
            chunk = os.read(stream.fileno(), 65536)
            if not chunk:
                selector.unregister(stream)
                continue
            streams[stream].extend(chunk)
            if len(streams[stream]) > MAX_STREAM_BYTES:
                outcome = "output_overflow"
                os.killpg(process.pid, signal.SIGKILL)
                break
        if outcome != "completed":
            break
        if process.poll() is not None and not selector.get_map():
            break
    try:
        returncode = process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        returncode = process.wait(timeout=5)
    for stream in tuple(selector.get_map().values()):
        selector.unregister(stream.fileobj)
    stdout = bytes(streams[process.stdout][:MAX_STREAM_BYTES])
    stderr = bytes(streams[process.stderr][:MAX_STREAM_BYTES])
    return returncode, stdout, stderr, outcome


def main() -> None:
    if EVIDENCE_DIRECTORY.exists():
        raise RuntimeError("evidence directory must be absent")
    manifest = load_manifest()
    source_expected = manifest["source_sha256"]
    preserved_expected = manifest["preserved_sha256"]
    if not isinstance(source_expected, dict) or not isinstance(preserved_expected, dict):
        raise RuntimeError("invalid manifest hash maps")
    before = {
        "repository_basis": verify_repository_basis(str(manifest["repository_basis"])),
        "repository_status": repository_status(),
        "presentation_status": presentation_status(),
        "source_sha256": verify_hash_map(REPOSITORY, source_expected),
        "preserved_sha256": verify_hash_map(REPOSITORY, preserved_expected),
        "presentation_sha256": verify_hash_map(PRESENTATION, PRESENTATION_SHA256),
        "accepted_evidence_sha256": verify_absolute_hash_map(ACCEPTED_EVIDENCE_SHA256),
        "controller_sha256": sha256(Path(__file__).resolve()),
    }
    EVIDENCE_DIRECTORY.mkdir(parents=False, exist_ok=False)
    stdout = b""
    stderr = b""
    returncode: int | None = None
    outcome = "controller_failure"
    controller_error: str | None = None
    started = time.monotonic()
    try:
        returncode, stdout, stderr, outcome = bounded_child()
    except Exception as exc:
        controller_error = type(exc).__name__
    elapsed = time.monotonic() - started
    after: dict[str, object] = {}
    try:
        after = {
            "repository_basis": verify_repository_basis(str(manifest["repository_basis"])),
            "repository_status": repository_status(),
            "presentation_status": presentation_status(),
            "source_sha256": verify_hash_map(REPOSITORY, source_expected),
            "preserved_sha256": verify_hash_map(REPOSITORY, preserved_expected),
            "presentation_sha256": verify_hash_map(PRESENTATION, PRESENTATION_SHA256),
            "accepted_evidence_sha256": verify_absolute_hash_map(ACCEPTED_EVIDENCE_SHA256),
            "controller_sha256": sha256(Path(__file__).resolve()),
        }
    except Exception as exc:
        controller_error = controller_error or type(exc).__name__
        outcome = "postcondition_failure"
    (EVIDENCE_DIRECTORY / "stdout.bin").write_bytes(stdout)
    (EVIDENCE_DIRECTORY / "stderr.bin").write_bytes(stderr)
    evidence = {
        "schema": "iiw-misty-gateway-static-evidence-v1",
        "manifest_sha256": MANIFEST_SHA256,
        "interpreter": INTERPRETER,
        "interpreter_version": sys.version.split()[0],
        "expected_test_count": EXPECTED_TEST_COUNT,
        "returncode": returncode,
        "outcome": outcome,
        "controller_error_type": controller_error,
        "elapsed_seconds": round(elapsed, 6),
        "limits": {"timeout_seconds": TIMEOUT_SECONDS, "max_bytes_per_stream": MAX_STREAM_BYTES},
        "enforcement": {
            "child_network_denied_by_audit_hook": True,
            "child_process_creation_denied_by_audit_hook": True,
            "child_writes_denied_by_audit_hook": True,
            "physical_robot_access": "not_performed_by_test_design_and_network_denied",
        },
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
        "before": before,
        "after": after,
    }
    (EVIDENCE_DIRECTORY / "evidence.json").write_text(
        json.dumps(evidence, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    success = returncode == 0 and outcome == "completed" and controller_error is None and before == after
    if not success:
        raise RuntimeError("bounded Misty gateway synthetic execution did not pass")


if __name__ == "__main__":
    main()
