"""Future execution controller. Requires a separately reviewed exact request."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import stat
import subprocess
import sys
import time
import types
import unittest

ROOT = Path("/Users/debb/dev/soga-clean")
PRESENTATION = Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak")
RESEARCH_ROOT = Path("/Users/debb/dev/research-evidence/soga")
EVIDENCE_ROOT = RESEARCH_ROOT / "evidence"
HERE = Path(__file__).absolute()
MANIFEST = HERE.with_name("cyberpi-protocol-runtime-manifest.json")
MANIFEST_SHA = "4d05c17577218fc74a91b6eac1d7515658652c51b502ecbcac21ab1dfab9ae1e"
PROTOCOL = "robot_gateway/cyberpi_f3f4_protocol.py"
TESTS = "tests/test_robot_gateway_cyberpi_protocol.py"
EXCLUDED = "?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md"
MUTATIONS = {
    "os.remove", "os.rename", "os.rmdir", "os.mkdir", "os.link", "os.symlink",
    "os.chmod", "os.chown", "os.truncate", "os.utime", "os.setxattr", "os.removexattr",
    "os.chdir", "os.chflags", "os.fchdir",
}
PROCESS = {"subprocess.Popen", "os.system", "os.fork", "os.forkpty", "os.exec", "os.posix_spawn", "os.posix_spawnp", "os.spawn", "pty.spawn"}
FORBIDDEN_IMPORTS = {"serial", "pyserial", "makeblock", "cyberpi", "socket", "_socket", "subprocess", "ctypes", "_ctypes"}


def checked_bytes(path):
    if not path.is_absolute() or path.resolve() != path or not stat.S_ISREG(path.lstat().st_mode):
        raise RuntimeError("expected canonical regular file: " + str(path))
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise RuntimeError("opened input is not a regular file")
        return stream.read()


def digest(path):
    return hashlib.sha256(checked_bytes(path)).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["/usr/bin/git", "--no-optional-locks", "-C", str(root), *args],
        timeout=5, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": "/Users/debb"},
    ).decode().splitlines()


def audit(event, args):
    if event.startswith("socket.") or event in PROCESS or event in MUTATIONS:
        raise PermissionError(event)
    if event == "import" and args[0].split(".")[0] in FORBIDDEN_IMPORTS:
        raise PermissionError(event)
    if event == "open":
        path, _, flags = args
        if isinstance(path, (str, bytes, os.PathLike)) and os.fsdecode(path).startswith("/dev/"):
            raise PermissionError("device_open")
        write_flags = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
        raise PermissionError("write_open" if flags & write_flags else "read_open")


def child(source, tests, controller_source, expected_count):
    # Preload the approved standard library dependencies before installing the hook.
    import ast
    import enum
    import functools
    import operator

    sys.addaudithook(audit)
    samples = [
        ("socket.connect", ()),
        ("subprocess.Popen", ()),
        ("os.mkdir", ()),
        ("open", ("/dev/cu.synthetic", "r", os.O_RDONLY)),
        ("open", ("/dev/tty.synthetic", "r", os.O_RDONLY)),
        ("open", ("synthetic", "w", os.O_WRONLY)),
        ("open", (Path("synthetic"), "r", os.O_RDONLY)),
        ("open", (0, "r", os.O_RDONLY)),
    ]
    samples.extend((event, ()) for event in sorted(PROCESS | MUTATIONS))
    samples.extend(("import", (name,)) for name in sorted(FORBIDDEN_IMPORTS))
    for event, args in samples:
        try:
            sys.audit(event, *args)
        except PermissionError:
            continue
        raise RuntimeError("audit self-test failed: " + event)

    namespace = types.ModuleType("cyberpi_candidate")
    exec(compile(source, PROTOCOL, "exec"), namespace.__dict__)
    if (namespace.MAX_BODY, namespace.MAX_STREAM) != (256, 4096):
        raise RuntimeError("parser limits mismatch")
    print(json.dumps({
        "audit_denials": len(samples),
        "checksums": namespace.checksum_candidates(),
        "fixtures": {item.name: namespace.fixture_record(item) for item in namespace.Fixture},
    }))
    test_module = types.ModuleType("cyberpi_synthetic_tests")
    test_module.__dict__.update(protocol=namespace, protocol_source=source,
                                test_source=tests, controller_source=controller_source)
    exec(compile(tests, TESTS, "exec"), test_module.__dict__)
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)
    if suite.countTestCases() != expected_count:
        raise RuntimeError("test count mismatch")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() and result.testsRun == expected_count and not result.skipped else 1


def snapshot(manifest, request):
    head = git(ROOT, "rev-parse", "HEAD")[0]
    status = git(ROOT, "status", "--porcelain=v1", "--untracked-files=all")
    if head != request["head"] or status != [EXCLUDED] or request["status"] != status:
        raise RuntimeError("repository head or status mismatch")
    git(ROOT, "merge-base", "--is-ancestor", manifest["repository_basis"], head)
    if git(PRESENTATION, "rev-parse", "HEAD") != [manifest["presentation_basis"]]:
        raise RuntimeError("presentation head mismatch")
    if git(PRESENTATION, "status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError("presentation status mismatch")
    hashes = {}
    for root, key in ((ROOT, "created"), (ROOT, "protected"), (PRESENTATION, "presentation")):
        for relative, expected in manifest[key].items():
            path = root / relative
            if path.resolve() != path or not stat.S_ISREG(path.stat().st_mode):
                raise RuntimeError("invalid pinned file: " + relative)
            value = digest(path)
            if value != expected:
                raise RuntimeError("hash mismatch: " + relative)
            hashes[str(path)] = value
    proposal = ROOT / "knowledge/proposals/IIW_MBOT2_CYBERPI_PROTOCOL_VERIFICATION_PROPOSAL_2026-11-05.md"
    handoff = RESEARCH_ROOT / "handoffs/MBOT2_CYBERPI_F3F4_G_HANDOFF_2026-11-03.txt"
    for path, expected in (
        (proposal, manifest["proposal_sha256"]),
        (handoff, manifest["handoff_sha256"]),
        (HERE, request["controller_sha256"]),
        (MANIFEST, MANIFEST_SHA),
    ):
        value = digest(path)
        if value != expected:
            raise RuntimeError("hash mismatch: " + str(path))
        hashes[str(path)] = value
    return {"head": head, "status": status, "hashes": hashes}


def capture(command, manifest):
    limit = manifest["max_output"]
    deadline = time.monotonic() + manifest["timeout_seconds"]
    output = bytearray()
    process = subprocess.Popen(
        command, cwd=ROOT, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    with process.stdout, selectors.DefaultSelector() as selector:
        selector.register(process.stdout, selectors.EVENT_READ)
        try:
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not selector.select(remaining):
                    raise TimeoutError("child timeout")
                data = os.read(process.stdout.fileno(), min(4096, limit - len(output) + 1))
                if not data:
                    break
                available = limit - len(output)
                output.extend(data[:available])
                if len(data) > available:
                    raise RuntimeError("child output limit")
            code = process.wait(timeout=max(0, deadline - time.monotonic()))
            return bytes(output), code, None
        except (TimeoutError, subprocess.TimeoutExpired, RuntimeError) as error:
            if process.poll() is None:
                process.kill()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                return bytes(output), None, str(error) + "; child reap timed out"
            return bytes(output), process.returncode, str(error)


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate request key")
        result[key] = value
    return result


def build_child_command(interpreter, manifest, request):
    # There is no child CLI. Only the approved parent builds this bootstrap,
    # using the exact bytes that it verifies here, then applies capture limits.
    source, tests, controller_source = (
        checked_bytes(ROOT / PROTOCOL), checked_bytes(ROOT / TESTS), checked_bytes(HERE)
    )
    for data, expected in (
        (source, manifest["created"][PROTOCOL]),
        (tests, manifest["created"][TESTS]),
        (controller_source, request["controller_sha256"]),
    ):
        if hashlib.sha256(data).hexdigest() != expected:
            raise RuntimeError("child source hash mismatch")
    bootstrap = (
        "import sys\n"
        "if not (sys.flags.isolated and sys.flags.dont_write_bytecode and sys.flags.no_site): "
        "raise SystemExit(2)\n"
        f"controller = {controller_source!r}\n"
        f"namespace = {{'__name__': '_cyberpi_child', '__file__': {str(HERE)!r}}}\n"
        f"exec(compile(controller, {str(HERE)!r}, 'exec'), namespace)\n"
        f"raise SystemExit(namespace['child']({source!r}, {tests!r}, controller, "
        f"{manifest['test_count']!r}))\n"
    )
    return [interpreter, "-I", "-B", "-S", "-c", bootstrap]


def main():
    if not (sys.flags.isolated and sys.flags.dont_write_bytecode and sys.flags.no_site):
        raise RuntimeError("requires -I -B -S")
    if HERE != ROOT / "tools/robot_gateway/run_cyberpi_protocol_tests.py":
        raise RuntimeError("requires committed repository location")
    if digest(MANIFEST) != MANIFEST_SHA:
        raise RuntimeError("manifest hash mismatch")
    manifest_bytes = checked_bytes(MANIFEST)
    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA:
        raise RuntimeError("manifest changed during read")
    manifest = json.loads(manifest_bytes)
    if len(sys.argv) != 2:
        raise RuntimeError("requires exact execution request path")
    request_path = Path(sys.argv[1])
    if not request_path.is_absolute() or request_path.resolve() != request_path or any(request_path.is_relative_to(root) for root in (ROOT, PRESENTATION)):
        raise RuntimeError("requires canonical external request path")
    request_bytes = checked_bytes(request_path)
    request_hash = hashlib.sha256(request_bytes).hexdigest()
    request = json.loads(request_bytes, object_pairs_hook=unique_keys)
    keys = {"head", "status", "controller_sha256", "manifest_sha256", "interpreter",
            "interpreter_sha256", "command", "test_count", "evidence"}
    if type(request) is not dict or set(request) != keys:
        raise RuntimeError("execution request shape mismatch")
    interpreter = str(Path(sys.executable).resolve())
    command = [interpreter, "-I", "-B", "-S", str(HERE), str(request_path)]
    if (request["manifest_sha256"] != MANIFEST_SHA or request["test_count"] != manifest["test_count"]
            or request["command"] != command or request["interpreter"] != interpreter
            or request["interpreter_sha256"] != digest(Path(interpreter))):
        raise RuntimeError("execution request pin mismatch")
    evidence = Path(request["evidence"])
    if evidence.parent != EVIDENCE_ROOT or evidence.resolve() != evidence or os.path.lexists(evidence):
        raise RuntimeError("requires a new evidence directory")
    before = snapshot(manifest, request)
    if evidence.parent.resolve() != EVIDENCE_ROOT or not evidence.parent.is_dir():
        raise RuntimeError("requires canonical durable evidence parent")
    child_command = build_child_command(interpreter, manifest, request)
    evidence.mkdir(mode=0o700)
    output, code, error = b"", None, None
    after = None
    try:
        output, code, error = capture(child_command, manifest)
    except Exception as failure:
        error = str(failure)
    finally:
        try:
            after = snapshot(manifest, request)
            if digest(request_path) != request_hash:
                raise RuntimeError("execution request changed")
        except Exception as failure:
            error = f"{error or 'after snapshot failed'}: {failure}"
        with (evidence / "child.log").open("xb") as stream:
            stream.write(output)
        with (evidence / "result.json").open("x", encoding="utf-8") as stream:
            json.dump({"before": before, "after": after, "command": command,
                       "child_bootstrap_sha256": hashlib.sha256(child_command[-1].encode()).hexdigest(), "code": code, "error": error,
                       "request_sha256": request_hash}, stream, indent=2)
    return 0 if code == 0 and error is None and before == after else 1


if __name__ == "__main__":
    raise SystemExit(main())
