"""Exact-request synthetic runner. Execution requires a separate PI decision."""
import ast
import hashlib
import json
import os
from pathlib import Path
import queue
import selectors
import signal
import socket
import stat
import subprocess
import sys
import threading
import time
import types
import unittest
import unittest.mock
from dataclasses import dataclass, replace
from typing import Protocol, runtime_checkable

ROOT = Path("/Users/debb/dev/soga-clean")
HERE = Path(__file__).absolute()
MANIFEST = HERE.with_name("cyberpi-none-runtime-manifest.json")
MANIFEST_SHA = "a5eda5cc415b290d651cd69466e0eb00cc377f4e7ba7c5c699fe95485980dc69"
EVIDENCE_ROOT = Path("/Users/debb/dev/research-evidence/soga/evidence")
EXCLUDED = ["?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md"]
DENY_PROCESS = {"subprocess.Popen", "os.system", "os.fork", "os.forkpty", "os.exec",
                "os.posix_spawn", "os.posix_spawnp", "os.spawn", "pty.spawn"}
DENY_MUTATION = {"os.remove", "os.rename", "os.rmdir", "os.mkdir", "os.link", "os.symlink",
                 "os.chmod", "os.chown", "os.truncate", "os.utime", "os.chdir",
                 "os.fchdir", "os.setxattr", "os.removexattr"}
DENY_IMPORT = {"serial", "pyserial", "makeblock", "cyberpi", "socket", "_socket", "ctypes", "_ctypes"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_regular(path):
    path = Path(path)
    if not path.is_absolute() or path.resolve() != path or not stat.S_ISREG(path.lstat().st_mode):
        raise RuntimeError("canonical_regular_file_required")
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise RuntimeError("regular_file_required")
        return stream.read()


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RuntimeError("duplicate_key")
        result[key] = value
    return result


def git(*args):
    return subprocess.check_output(
        ["/usr/bin/git", "--no-optional-locks", "-C", str(ROOT), *args],
        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": "/Users/debb"}, timeout=5,
    ).decode().splitlines()


def audit(event, args):
    if event.startswith("socket.") or event in DENY_PROCESS or event in DENY_MUTATION:
        raise PermissionError(event)
    if event == "open":
        raise PermissionError("all_open_denied")
    if event == "import" and args[0].split(".")[0] in DENY_IMPORT:
        raise PermissionError("device_import_denied")


def child(sources, manifest):
    # All standard-library test dependencies are imported before installing audit.
    sys.addaudithook(audit)
    samples = [(event, ()) for event in sorted(DENY_PROCESS | DENY_MUTATION)]
    samples += [("socket.connect", ()), ("open", ("/dev/cu.synthetic", "r", 0)),
                ("open", ("/dev/tty.synthetic", "r", 0)), ("open", ("synthetic", "w", os.O_WRONLY))]
    samples += [("import", (name,)) for name in sorted(DENY_IMPORT)]
    for event, args in samples:
        try:
            sys.audit(event, *args)
        except PermissionError:
            continue
        raise RuntimeError("audit_denial_missing")
    for relative, data in sources.items():
        if sha(data) != manifest["sources"][relative]:
            raise RuntimeError("child_source_pin_mismatch")
    for package in ("g27_tip_jar", "robot_gateway"):
        module = types.ModuleType(package)
        module.__path__ = []
        sys.modules[package] = module
    loaded = {}
    for name, relative in manifest["modules"]:
        module = types.ModuleType(name)
        module.__file__ = str(ROOT / relative)
        module.__package__ = name.rpartition(".")[0]
        sys.modules[name] = module
        exec(compile(sources[relative], str(ROOT / relative), "exec"), module.__dict__)
        loaded[name] = module
    suite = unittest.TestSuite()
    for name, relative in manifest["tests"]:
        module = types.ModuleType(name)
        module.__dict__.update(protocol=loaded.get("robot_gateway.cyberpi_f3f4_protocol"),
                               observation=loaded.get("robot_gateway.cyberpi_none_observation"))
        module.__file__ = str(ROOT / relative)
        exec(compile(sources[relative], str(ROOT / relative), "exec"), module.__dict__)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    if suite.countTestCases() != manifest["test_count"]:
        raise RuntimeError("test_count_mismatch")
    print(json.dumps({"audit_denials": len(samples), "expected_tests": manifest["test_count"]}), flush=True)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() and not result.skipped and result.testsRun == manifest["test_count"] else 1


def snapshot(request, manifest):
    if git("rev-parse", "HEAD") != [request["head"]] or git("status", "--porcelain=v1", "--untracked-files=all") != EXCLUDED:
        raise RuntimeError("repository_mismatch")
    if request["status"] != EXCLUDED:
        raise RuntimeError("request_status_mismatch")
    hashes, sources = {}, {}
    for relative, expected in manifest["sources"].items():
        path = ROOT / relative
        if not path.is_relative_to(ROOT) or path.resolve() != path:
            raise RuntimeError("source_path_mismatch")
        data = read_regular(path)
        if sha(data) != expected:
            raise RuntimeError("source_hash_mismatch:" + relative)
        sources[relative] = data
        hashes[str(path)] = sha(data)
    for absolute, expected in manifest["protected"].items():
        data = read_regular(absolute)
        if sha(data) != expected:
            raise RuntimeError("protected_hash_mismatch")
        hashes[absolute] = expected
    for absolute, expected in request["runtime"].items():
        if sha(read_regular(absolute)) != expected:
            raise RuntimeError("runtime_hash_mismatch")
        hashes[absolute] = expected
    interpreter = str(Path(sys.executable).resolve())
    if interpreter not in request["runtime"]:
        raise RuntimeError("interpreter_not_pinned")
    if sha(read_regular(HERE)) != request["controller_sha256"]:
        raise RuntimeError("controller_hash_mismatch")
    return {"head": request["head"], "status": EXCLUDED, "hashes": hashes}, sources


def capture(command, timeout, limit):
    output = bytearray()
    deadline = time.monotonic() + timeout
    process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"})
    code, error = None, None
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not selector.select(remaining):
                    raise TimeoutError("child_deadline")
                chunk = os.read(process.stdout.fileno(), min(4096, limit + 1 - len(output)))
                if not chunk:
                    break
                output.extend(chunk)
                if len(output) > limit:
                    raise RuntimeError("output_limit")
        code = process.wait(timeout=max(0, deadline - time.monotonic()))
    except BaseException as failure:
        error = type(failure).__name__ + ":" + str(failure)
    finally:
        if process.poll() is None:
            process.kill()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                error = (error or "") + ";reap_unknown"
        process.stdout.close()
    return bytes(output[:limit]), code, error


def main():
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode) or len(sys.argv) != 2:
        raise RuntimeError("exact_invocation_required")
    if HERE != ROOT / "tools/robot_gateway/run_cyberpi_none_synthetic.py":
        raise RuntimeError("committed_location_required")
    manifest_bytes = read_regular(MANIFEST)
    if sha(manifest_bytes) != MANIFEST_SHA:
        raise RuntimeError("manifest_hash_mismatch")
    manifest = json.loads(manifest_bytes, object_pairs_hook=unique)
    request_path = Path(sys.argv[1])
    request_bytes = read_regular(request_path)
    request = json.loads(request_bytes, object_pairs_hook=unique)
    if set(request) != {"head", "status", "controller_sha256", "manifest_sha256", "runtime", "command", "evidence"}:
        raise RuntimeError("request_schema")
    interpreter = str(Path(sys.executable).resolve())
    if request["command"] != [interpreter, "-I", "-B", "-S", str(HERE), str(request_path)] or request["manifest_sha256"] != MANIFEST_SHA:
        raise RuntimeError("request_pin_mismatch")
    if type(request["runtime"]) is not dict or not request["runtime"]:
        raise RuntimeError("runtime_inventory_required")
    evidence = Path(request["evidence"])
    if evidence.parent != EVIDENCE_ROOT or evidence.resolve() != evidence or os.path.lexists(evidence):
        raise RuntimeError("new_evidence_required")
    before, sources = snapshot(request, manifest)
    source = read_regular(HERE)
    bootstrap = ("namespace={'__name__':'_synthetic_child','__file__':" + repr(str(HERE)) + "}\n"
                 "exec(compile(" + repr(source) + "," + repr(str(HERE)) + ",'exec'),namespace)\n"
                 "raise SystemExit(namespace['child'](" + repr(sources) + "," + repr(manifest) + "))\n")
    evidence.mkdir(mode=0o700)
    output, code, error = capture([interpreter, "-I", "-B", "-S", "-c", bootstrap],
                                  manifest["timeout_seconds"], manifest["max_output"])
    after = None
    try:
        after, _ = snapshot(request, manifest)
        if sha(read_regular(request_path)) != sha(request_bytes):
            raise RuntimeError("request_changed")
    except BaseException as failure:
        error = (error or "") + ":" + str(failure)
    with (evidence / "child.log").open("xb") as stream:
        stream.write(output)
    with (evidence / "result.json").open("x") as stream:
        json.dump({"before": before, "after": after, "code": code, "error": error,
                   "command": request["command"], "request_sha256": sha(request_bytes),
                   "bootstrap_sha256": sha(bootstrap.encode())}, stream, indent=2)
    return 0 if code == 0 and error is None and before == after else 1


if __name__ == "__main__":
    raise SystemExit(main())
