#!/usr/bin/python3
from __future__ import annotations

import hashlib
import json
import os
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path("/Users/debb/dev/soga-clean")
PRESENTATION = Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak")
MANIFEST = ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json"
MANIFEST_SHA256 = "f4a84b8b1a3e732009afeaf56ba443177c7acf62844ce25074cb4cad0761ab99"
TEST_MODULE = ROOT / "tests/test_robot_gateway_misty_stop_only_probe.py"
EXPECTED_STATUS = ["?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md"]
PACKAGE_PATHS = {
    "robot_gateway/misty_stop_probe.py",
    "robot_gateway/STOP_ONLY_VERIFICATION.md",
    "tests/test_robot_gateway_misty_stop_only_probe.py",
    "tools/robot_gateway/misty-stop-only-runtime-manifest.json",
    "tools/robot_gateway/run_misty_stop_only_probe.py",
    "tools/robot_gateway/run_misty_stop_only_synthetic_tests.py",
}
# The separately reviewed CyberPi package may coexist only as new paths.
CYBERPI_ADDITION_PATHS = {
    "knowledge/proposals/IIW_MBOT2_CYBERPI_PROTOCOL_VERIFICATION_PROPOSAL_2026-11-05.md",
    "robot_gateway/cyberpi_f3f4_protocol.py",
    "robot_gateway/CYBERPI_PROTOCOL_VERIFICATION.md",
    "tests/test_robot_gateway_cyberpi_protocol.py",
    "tools/robot_gateway/run_cyberpi_protocol_tests.py",
    "tools/robot_gateway/cyberpi-protocol-runtime-manifest.json",
    "knowledge/proposals/MBOT2_FIRST_PROTOCOL_OBSERVATION_R2_2026-11-09.md",
    "knowledge/proposals/TWO_ROBOT_SWITCHING_RUNTIME_R2_2026-11-09.md",
    "robot_gateway/CYBERPI_NONE_OBSERVATION.md",
    "robot_gateway/OPERATOR_RUNTIME.md",
    "robot_gateway/SWITCHING_REVIEW.md",
    "robot_gateway/cyberpi_none_observation.py",
    "robot_gateway/operator_runtime.py",
    "robot_gateway/owned_gateway.py",
    "robot_gateway/switching.py",
    "tests/test_robot_gateway_cyberpi_none_observation.py",
    "tests/test_robot_gateway_operator_runtime.py",
    "tests/test_switching.py",
    "tools/robot_gateway/cyberpi-none-runtime-manifest.json",
    "tools/robot_gateway/operator-runtime-manifest.json",
    "tools/robot_gateway/run_cyberpi_none_physical.py",
    "tools/robot_gateway/run_cyberpi_none_synthetic.py",
    "tools/robot_gateway/run_operator_runtime_synthetic.py",
}
ALLOWED_COMMIT_PATHS = PACKAGE_PATHS | {
    "knowledge/strategy/DECISION_LOG.md",
    "knowledge/working/CURRENT_STATE.md",
}

ENVIRONMENT = lambda: os.environ
ARGUMENTS = lambda: sys.argv
FLAGS = lambda: sys.flags
PATH_EXISTS = lambda path: path.exists()
MAKE_DIRECTORY = lambda path: path.mkdir(mode=0o700, parents=False)
WRITE_BYTES = lambda path, value: path.write_bytes(value)
WRITE_TEXT = lambda path, value: path.write_text(value, encoding="utf-8")
MONOTONIC = time.monotonic
LOAD_MANIFEST = lambda: json.loads(MANIFEST.read_text(encoding="utf-8"), object_pairs_hook=_reject_manifest_pairs, parse_constant=_reject_manifest_constant)
SNAPSHOT = lambda manifest: snapshot(manifest)
RUN_CHILD = lambda expected, timeout, limit: bounded_child(expected, timeout, limit)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reject_manifest_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RuntimeError("duplicate_json_key")
        result[key] = value
    return result


def _reject_manifest_constant(_value):
    raise RuntimeError("non_finite_json_number")


def git(*args: str, cwd=ROOT, allowed=(0,)) -> str:
    result = subprocess.run(["/usr/bin/git", "-C", str(cwd), *args], env={"PATH": "/usr/bin:/bin", "HOME": "/Users/debb", "LANG": "C", "LC_ALL": "C"}, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10, check=False)
    if result.returncode not in allowed or result.stderr:
        raise RuntimeError("git_observation_failed")
    return result.stdout


def verify_basis(manifest: dict[str, object]) -> dict[str, object]:
    basis = manifest.get("repository_basis")
    if not isinstance(basis, str):
        raise RuntimeError("invalid_repository_basis")
    git("merge-base", "--is-ancestor", basis, "HEAD")
    changed = set(git("diff", "--no-renames", "--name-only", basis + "..HEAD").splitlines())
    extra = changed - ALLOWED_COMMIT_PATHS
    if not PACKAGE_PATHS.issubset(changed) or not extra.issubset(CYBERPI_ADDITION_PATHS):
        raise RuntimeError("repository_basis_mismatch")
    if extra:
        additions = git("diff", "--no-renames", "--diff-filter=A", "--name-only", basis + "..HEAD")
        if not extra.issubset(additions.splitlines()):
            raise RuntimeError("repository_basis_mismatch")
    presentation_head = git("rev-parse", "HEAD", cwd=PRESENTATION).strip()
    if presentation_head != manifest.get("presentation_basis"):
        raise RuntimeError("presentation_basis_mismatch")
    return {"repository_basis": basis, "head": git("rev-parse", "HEAD").strip(), "changed_paths": sorted(changed), "presentation_head": presentation_head}


def snapshot(manifest: dict[str, object]) -> dict[str, object]:
    result = {
        "basis": verify_basis(manifest),
        "head": git("rev-parse", "HEAD").strip(),
        "status": git("status", "--porcelain=v1", "--untracked-files=all").splitlines(),
        "presentation_head": git("rev-parse", "HEAD", cwd=PRESENTATION).strip(),
        "presentation_status": git("status", "--porcelain=v1", "--untracked-files=all", cwd=PRESENTATION).splitlines(),
    }
    if result["status"] != EXPECTED_STATUS or result["presentation_status"]:
        raise RuntimeError("status_mismatch")
    for section, base in (("source_sha256", ROOT), ("accepted_gateway_sha256", ROOT), ("preserved_sha256", ROOT)):
        result[section] = {name: sha256_path(base / name) for name in manifest[section]}
        if result[section] != manifest[section]:
            raise RuntimeError("hash_mismatch")
    result["presentation_sha256"] = {name: sha256_path(PRESENTATION / name) for name in manifest["presentation_sha256"]}
    result["accepted_evidence_sha256"] = {name: sha256_path(Path(name)) for name in manifest["accepted_evidence_sha256"]}
    if result["presentation_sha256"] != manifest["presentation_sha256"] or result["accepted_evidence_sha256"] != manifest["accepted_evidence_sha256"]:
        raise RuntimeError("external_hash_mismatch")
    return result


AUDIT_FUNCTION = r'''
def audit_event(event, args):
    if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.fork", "os.forkpty", "os.exec", "os.posix_spawn", "os.posix_spawnp", "os.spawn"}:
        raise RuntimeError("audit_denied")
    if event in {"os.remove", "os.rename", "os.replace", "os.mkdir", "os.rmdir", "os.link", "os.symlink", "os.truncate", "os.chmod", "os.chown", "os.utime"}:
        raise RuntimeError("audit_mutation_denied")
    if event == "open" and len(args) >= 2:
        mode = args[1]
        flags = args[2] if len(args) >= 3 else 0
        if (isinstance(mode, str) and any(x in mode for x in "wax+")) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)):
            raise RuntimeError("audit_write_denied")
'''
_audit_namespace = {"os": os}
exec(AUDIT_FUNCTION, _audit_namespace)
audit_event = _audit_namespace["audit_event"]


def controller_self_check() -> dict[str, bool]:
    denied = {}
    for name, event, args in (
        ("network", "socket.connect", (None,)),
        ("process", "subprocess.Popen", (None,)),
        ("mutation", "os.remove", ("x",)),
        ("text_write", "open", ("x", "w", 0)),
        ("flag_write", "open", ("x", None, os.O_WRONLY | os.O_CREAT)),
    ):
        try:
            audit_event(event, args)
        except RuntimeError:
            denied[name] = True
        else:
            denied[name] = False
    audit_event("open", ("x", "r", 0))
    if not all(denied.values()):
        raise RuntimeError("audit_self_check_failed")
    return denied

CHILD = "import importlib.util, os, pathlib, sys, unittest\n" + AUDIT_FUNCTION + r'''
sys.addaudithook(audit_event)
path = pathlib.Path("/Users/debb/dev/soga-clean/tests/test_robot_gateway_misty_stop_only_probe.py")
spec = importlib.util.spec_from_file_location("stop_only_tests", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
if suite.countTestCases() != EXPECTED_COUNT:
    raise SystemExit("unexpected_test_count")
result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
raise SystemExit(0 if result.wasSuccessful() and not result.skipped else 1)
'''


def bounded_child(expected_count: int, timeout: int, limit: int) -> tuple[int | None, bytes, bytes, str]:
    child = "EXPECTED_COUNT = " + str(expected_count) + "\n" + CHILD
    process = subprocess.Popen(
        ["/usr/bin/python3", "-I", "-B", "-c", child], cwd=str(ROOT),
        env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0", "LANG": "C", "LC_ALL": "C"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=True,
    )
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    streams = {process.stdout: bytearray(), process.stderr: bytearray()}
    for stream in streams:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ)
    deadline = time.monotonic() + timeout
    outcome = "completed"
    try:
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
                if len(streams[stream]) > limit:
                    outcome = "output_overflow"
                    os.killpg(process.pid, signal.SIGKILL)
                    break
            if outcome != "completed":
                break
    except BaseException:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)
        raise
    try:
        returncode = process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        returncode = process.wait(timeout=5)
    for key in tuple(selector.get_map().values()):
        selector.unregister(key.fileobj)
    return returncode, bytes(streams[process.stdout][:limit]), bytes(streams[process.stderr][:limit]), outcome


def main() -> None:
    for key in ENVIRONMENT():
        if "PROXY" in key.upper() or (key.startswith("GIT_") and key != "GIT_PAGER"):
            raise RuntimeError("ambient_environment_refused")
    flags = FLAGS()
    if ARGUMENTS() != [str(Path(__file__).resolve())] or flags.isolated != 1 or flags.dont_write_bytecode != 1:
        raise RuntimeError("invocation_mismatch")
    if sha256_path(MANIFEST) != MANIFEST_SHA256:
        raise RuntimeError("manifest_hash_mismatch")
    manifest = LOAD_MANIFEST()
    if manifest.get("interpreter") != "/usr/bin/python3":
        raise RuntimeError("interpreter_mismatch")
    evidence_dir = Path(manifest["synthetic_evidence_directory"])
    if PATH_EXISTS(evidence_dir):
        raise RuntimeError("evidence_directory_must_be_absent")
    before = SNAPSHOT(manifest)
    audit_self_check = controller_self_check()
    MAKE_DIRECTORY(evidence_dir)
    started = MONOTONIC()
    stdout = b""
    stderr = b""
    returncode: int | None = None
    outcome = "controller_failure"
    error: str | None = None
    limit = int(manifest["synthetic_max_stream_bytes"])
    try:
        returncode, stdout, stderr, outcome = RUN_CHILD(int(manifest["synthetic_expected_test_count"]), int(manifest["synthetic_timeout_seconds"]), limit)
    except BaseException as exc:
        error = type(exc).__name__
    WRITE_BYTES(evidence_dir / "stdout.bin", stdout)
    WRITE_BYTES(evidence_dir / "stderr.bin", stderr)
    after: dict[str, object] = {}
    try:
        after = SNAPSHOT(manifest)
    except BaseException as exc:
        error = error or type(exc).__name__
        outcome = "postcondition_failure"
    text = stdout.decode("utf-8", errors="replace")
    passed = sum(1 for line in text.splitlines() if line.rstrip().endswith(" ... ok"))
    evidence = {
        "schema": "iiw-misty-stop-only-synthetic-evidence-v1",
        "returncode": returncode, "controller_error": error, "outcome": outcome,
        "expected_test_count": manifest["synthetic_expected_test_count"], "passed_test_count": passed,
        "elapsed_seconds": MONOTONIC() - started,
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(), "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
        "manifest_sha256": MANIFEST_SHA256, "controller_sha256": sha256_path(Path(__file__).resolve()),
        "before": before, "after": after,
        "audit_self_check": audit_self_check,
        "configured_controls": {"network_denied_by_audit_hook": True, "process_creation_denied_in_child": True,
        "filesystem_mutation_denied_in_child": True}, "automatic_retry": False,
    }
    WRITE_TEXT(evidence_dir / "evidence.json", json.dumps(evidence, sort_keys=True, separators=(",", ":")) + "\n")
    if returncode != 0 or error or outcome != "completed" or stderr or passed != manifest["synthetic_expected_test_count"] or before != after:
        raise RuntimeError("synthetic_test_failure")


if __name__ == "__main__":
    main()
