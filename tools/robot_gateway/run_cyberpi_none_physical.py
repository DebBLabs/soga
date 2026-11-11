"""Physical observation controller. Requires a separately approved exact request."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import stat
import subprocess
import sys
import termios
import time

ROOT = Path("/Users/debb/dev/soga-clean")
EVIDENCE_ROOT = Path("/Users/debb/dev/research-evidence/soga/evidence")
HERE = Path(__file__).absolute()
MANIFEST = HERE.with_name("cyberpi-none-runtime-manifest.json")
MANIFEST_SHA = "a5eda5cc415b290d651cd69466e0eb00cc377f4e7ba7c5c699fe95485980dc69"
PROBE = ROOT / "robot_gateway/cyberpi_none_observation.py"
PROTOCOL = ROOT / "robot_gateway/cyberpi_f3f4_protocol.py"


def read_regular(path):
    path = Path(path)
    if not path.is_absolute() or path.resolve() != path or not stat.S_ISREG(path.lstat().st_mode):
        raise RuntimeError("canonical_regular_file_required")
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise RuntimeError("regular_file_required")
        return stream.read()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise RuntimeError("duplicate_key")
        obj[key] = value
    return obj


def record(path):
    return json.loads(read_regular(path), object_pairs_hook=unique)


def git(*args):
    return subprocess.check_output(
        ["/usr/bin/git", "--no-optional-locks", "-C", str(ROOT), *args],
        env={"PATH": "/usr/bin:/bin", "HOME": "/Users/debb", "LC_ALL": "C"}, timeout=5,
    ).decode().splitlines()


def pins(request, manifest):
    if git("rev-parse", "HEAD") != [request["head"]] or git("status", "--porcelain=v1", "--untracked-files=all") != request["status"]:
        raise RuntimeError("repository_mismatch")
    if request["status"] != ["?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md"]:
        raise RuntimeError("unexpected_status")
    observed = {}
    for relative, expected in manifest["sources"].items():
        path = ROOT / relative
        if path.resolve() != path or not path.is_relative_to(ROOT):
            raise RuntimeError("invalid_source_path")
        value = sha(read_regular(path))
        if value != expected:
            raise RuntimeError("source_hash_mismatch")
        observed[str(path)] = value
    for absolute, expected in manifest["protected"].items():
        value = sha(read_regular(absolute))
        if value != expected:
            raise RuntimeError("protected_hash_mismatch")
        observed[absolute] = value
    runtime = request["runtime"]
    if type(runtime) is not dict or not runtime:
        raise RuntimeError("runtime_pins_required")
    for absolute, expected in runtime.items():
        observed[absolute] = sha(read_regular(absolute))
        if observed[absolute] != expected:
            raise RuntimeError("runtime_hash_mismatch")
    for module in tuple(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename and filename != str(HERE):
            path = str(Path(filename).resolve())
            if path not in runtime:
                raise RuntimeError("unlisted_loaded_runtime:" + path)
    if sha(read_regular(HERE)) != request["controller_sha256"]:
        raise RuntimeError("controller_hash_mismatch")
    return observed


def load_verified(name, path, expected):
    data = read_regular(path)
    if sha(data) != expected:
        raise RuntimeError("load_hash_mismatch")
    import types
    module = types.ModuleType(name)
    exec(compile(data, str(path), "exec"), module.__dict__)
    return module


def worker(request, preflight, manifest):
    probe = load_verified("none_probe", PROBE, manifest["sources"][str(PROBE.relative_to(ROOT))])
    protocol = load_verified("protocol", PROTOCOL, manifest["sources"][str(PROTOCOL.relative_to(ROOT))])
    io = probe.SerialIO(preflight["device_path"], preflight["device_rdev"],
                        os_api=os, termios_api=termios, selectors_api=selectors, stat_api=stat)
    def interrupted(signum, frame):
        raise probe.ObservationAbort(signal.Signals(signum).name)
    signal.signal(signal.SIGINT, interrupted)
    signal.signal(signal.SIGTERM, interrupted)
    result = probe.observe(io, time.monotonic, lambda raw: probe.classify_response(raw, protocol))
    result["hupcl"] = io.hupcl
    result["write_syscall_attempted"] = io.syscall_attempted
    result["operator_postflight"] = "pending"
    result["physical_outcome"] = "unknown"
    print(json.dumps(result), flush=True)


def capture(command, policy):
    output = bytearray()
    deadline = time.monotonic() + 20.0
    if policy.signum is not None:
        return b"", None, "abort_before_worker", False
    process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, start_new_session=True)
    error, killed, code = None, False, None
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while True:
                now = time.monotonic()
                action = policy.action(now, deadline)
                if action == "forward":
                    process.send_signal(policy.signum)
                if action == "kill":
                    raise TimeoutError("wall_or_abort_grace_expired")
                events = selector.select(min(0.05, max(0.0, deadline - now)))
                if not events:
                    if process.poll() is not None:
                        continue
                    continue
                chunk = os.read(process.stdout.fileno(), min(4096, 32769 - len(output)))
                if not chunk:
                    break
                output.extend(chunk)
                if len(output) > 32768:
                    raise RuntimeError("output_limit")
        code = process.wait(timeout=max(0, deadline - time.monotonic()))
    except BaseException as failure:
        error = type(failure).__name__ + ":" + str(failure)
    finally:
        if process.poll() is None:
            killed = True
            process.kill()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                error = (error or "") + ";reap_unknown"
        process.stdout.close()
    if policy.signum is not None:
        error = (error or "") + ";parent_signal=" + str(policy.signum)
    return bytes(output[:32768]), code, error, killed


def main():
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode) or len(sys.argv) != 2:
        raise RuntimeError("exact_invocation_required")
    if HERE != ROOT / "tools/robot_gateway/run_cyberpi_none_physical.py":
        raise RuntimeError("committed_location_required")
    manifest_bytes = read_regular(MANIFEST)
    if sha(manifest_bytes) != MANIFEST_SHA:
        raise RuntimeError("manifest_hash_mismatch")
    manifest = json.loads(manifest_bytes, object_pairs_hook=unique)
    request_path = Path(sys.argv[1])
    request_bytes = read_regular(request_path)
    request = json.loads(request_bytes, object_pairs_hook=unique)
    expected_keys = {"head", "status", "controller_sha256", "manifest_sha256", "runtime",
                     "command", "evidence", "preflight", "preflight_sha256", "authority"}
    if set(request) != expected_keys:
        raise RuntimeError("request_schema")
    interpreter = str(Path(sys.executable).resolve())
    if request["command"] != [interpreter, "-I", "-B", "-S", str(HERE), str(request_path)]:
        raise RuntimeError("command_mismatch")
    if request["manifest_sha256"] != MANIFEST_SHA or interpreter not in request["runtime"]:
        raise RuntimeError("request_pin_mismatch")
    probe = load_verified("none_gate", PROBE, manifest["sources"][str(PROBE.relative_to(ROOT))])
    authority = record(request["authority"])
    probe.validate_authority(authority, sha(request_bytes))
    preflight_bytes = read_regular(request["preflight"])
    if sha(preflight_bytes) != request["preflight_sha256"]:
        raise RuntimeError("preflight_hash_mismatch")
    preflight = json.loads(preflight_bytes, object_pairs_hook=unique)
    device = Path(preflight["device_path"])
    metadata = device.lstat()
    probe.validate_preflight(preflight, time.time(), {
        "canonical": device.resolve() == device, "parent": str(device.parent), "name": device.name,
        "character": stat.S_ISCHR(metadata.st_mode), "rdev": metadata.st_rdev,
    })
    evidence = Path(request["evidence"])
    if evidence.parent != EVIDENCE_ROOT or evidence.resolve() != evidence or os.path.lexists(evidence):
        raise RuntimeError("new_evidence_required")
    before = pins(request, manifest)
    source = read_regular(HERE)
    bootstrap = ("namespace={'__name__':'_physical_worker','__file__':" + repr(str(HERE)) + "}\n"
                 "exec(compile(" + repr(source) + "," + repr(str(HERE)) + ",'exec'),namespace)\n"
                 "namespace['worker'](" + repr(request) + "," + repr(preflight) + "," + repr(manifest) + ")\n")
    policy = probe.AbortPolicy()
    old_handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}
    def parent_signal(signum, frame):
        policy.receive(signum)
    for sig in old_handlers:
        signal.signal(sig, parent_signal)
    created = False
    output, code, error, killed, after = b"", None, None, False, None
    try:
        evidence.mkdir(mode=0o700)
        created = True
        output, code, error, killed = capture([interpreter, "-I", "-B", "-S", "-c", bootstrap], policy)
    except BaseException as failure:
        error = type(failure).__name__ + ":" + str(failure)
    finally:
        if created:
            try:
                after = pins(request, manifest)
                if sha(read_regular(request_path)) != sha(request_bytes):
                    raise RuntimeError("request_changed")
            except BaseException as failure:
                error = (error or "") + ":" + str(failure)
            with (evidence / "worker.log").open("xb") as stream:
                stream.write(output)
            result = {"before": before, "after": after, "code": code, "error": error,
                      "request_sha256": sha(request_bytes), "operator_postflight": "pending",
                      "bootstrap_sha256": sha(bootstrap.encode()), "parent_signal": policy.signum,
                      "worker_killed": killed, "raw_lost_if_worker_killed": killed,
                      "close_outcome_if_worker_killed": "unknown" if killed else "see_worker"}
            with (evidence / "result.json").open("x") as stream:
                json.dump(result, stream, indent=2)
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
    return 0 if code == 0 and error is None and policy.signum is None and before == after else 1


if __name__ == "__main__":
    raise SystemExit(main())
