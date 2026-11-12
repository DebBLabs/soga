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
import tempfile
import termios
import time

ROOT = Path("/Users/debb/dev/soga-clean")
EVIDENCE_ROOT = Path("/Users/debb/dev/research-evidence/soga/evidence")
HERE = Path(__file__).absolute()
MANIFEST = HERE.with_name("cyberpi-none-v3-runtime-manifest.json")
MANIFEST_SHA = "b318339737efd66e5fcecec6aa703d541a0e19743c3944f49827e47d88f73461"
PROBE = ROOT / "robot_gateway/cyberpi_none_observation_v3.py"
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


def git(*args):
    return subprocess.check_output(
        ["/usr/bin/git", "--no-optional-locks", "-C", str(ROOT), *args],
        env={"PATH": "/usr/bin:/bin", "HOME": "/Users/debb", "LC_ALL": "C"}, timeout=5,
    ).decode().splitlines()


def pins(request, manifest, probe):
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
    inventory_check(runtime, probe)
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


def clock_sample():
    return time.time(), time.monotonic()


def inventory_check(runtime, probe):
    paths = (str(Path(filename).resolve()) for module in tuple(sys.modules.values())
             if (filename := getattr(module, "__file__", None)) and filename != str(HERE))
    probe.check_inventory(paths, runtime)


def device_metadata(path):
    metadata = path.lstat()
    return {"canonical": path.resolve() == path, "parent": str(path.parent),
            "name": path.name, "character": stat.S_ISCHR(metadata.st_mode),
            "rdev": metadata.st_rdev}


def worker(runtime, preflight, authority, parent_sample, cutoff, manifest):
    def interrupted(signum, frame):
        raise probe.ObservationAbort(signal.Signals(signum).name)

    probe = load_verified("none_probe", PROBE, manifest["sources"][str(PROBE.relative_to(ROOT))])
    signal.signal(signal.SIGINT, interrupted)
    signal.signal(signal.SIGTERM, interrupted)
    protocol = load_verified("protocol", PROTOCOL, manifest["sources"][str(PROTOCOL.relative_to(ROOT))])
    inventory_check(runtime, probe)
    device = Path(preflight["device_path"])
    probe.validate_preflight(preflight, time.time(), device_metadata(device))

    def before_open():
        probe.check_open(preflight, authority, parent_sample, cutoff, clock_sample())

    io = probe.SerialIO(str(device), preflight["device_rdev"],
                        os_api=os, termios_api=termios, selectors_api=selectors, stat_api=stat,
                        before_open=before_open)
    result = probe.observe(io, time.monotonic, lambda raw: probe.classify_response(raw, protocol))
    result["hupcl"] = io.hupcl
    result["write_syscall_attempted"] = io.syscall_attempted
    result["operator_postflight"] = "pending"
    result["physical_outcome"] = "unknown"
    print(json.dumps(result), flush=True)


def capture(command, policy, input_stream, limits):
    output = bytearray()
    deadline = time.monotonic() + limits["capture_seconds"]
    output_limit = limits["worker_output_bytes"]
    if policy.signum is not None:
        return b"", None, "abort_before_worker", False
    process = subprocess.Popen(command, cwd=ROOT, stdin=input_stream,
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
                chunk = os.read(process.stdout.fileno(), min(4096, output_limit + 1 - len(output)))
                if not chunk:
                    break
                output.extend(chunk)
                if len(output) > output_limit:
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
    return bytes(output[:output_limit]), code, error, killed


def verify_signature(request, payload):
    verifier = request["verifier"]
    if type(verifier) is not dict or set(verifier) != {"path", "sha256", "dependencies"}:
        raise RuntimeError("verifier_schema")
    executable = verifier["path"]
    if sha(read_regular(executable)) != verifier["sha256"]:
        raise RuntimeError("verifier_pin_mismatch")
    if type(verifier["dependencies"]) is not dict or not verifier["dependencies"]:
        raise RuntimeError("verifier_dependencies_required")
    for path, expected in verifier["dependencies"].items():
        if sha(read_regular(path)) != expected:
            raise RuntimeError("verifier_dependency_mismatch")
    key = read_regular(request["approval_public_key"])
    signature = read_regular(request["authority_signature"])
    if sha(key) != request["approval_public_key_sha256"] or not 8 <= len(signature) <= 80:
        raise RuntimeError("approval_key_or_signature_mismatch")
    with tempfile.TemporaryDirectory(prefix="cyberpi-v3-signature-") as scratch:
        public = Path(scratch) / "public.pem"
        detached = Path(scratch) / "approval.der"
        public.write_bytes(key)
        detached.write_bytes(signature)
        completed = subprocess.run(
            [executable, "dgst", "-sha256", "-verify", str(public), "-signature", str(detached)],
            input=payload, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, cwd=scratch, timeout=5,
            check=False,
        )
    return completed.returncode == 0


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def persist_reservation(evidence, reservation):
    with (evidence / "reservation.json").open("x") as stream:
        json.dump(reservation, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(evidence)


def main():
    initial = clock_sample()
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode) or len(sys.argv) != 2:
        raise RuntimeError("exact_invocation_required")
    if HERE != ROOT / "tools/robot_gateway/run_cyberpi_none_physical_v3.py":
        raise RuntimeError("committed_location_required")
    manifest_bytes = read_regular(MANIFEST)
    if sha(manifest_bytes) != MANIFEST_SHA:
        raise RuntimeError("manifest_hash_mismatch")
    manifest = json.loads(manifest_bytes, object_pairs_hook=unique)
    request_path = Path(sys.argv[1])
    request_bytes = read_regular(request_path)
    request = json.loads(request_bytes, object_pairs_hook=unique)
    expected_keys = {"head", "status", "controller_sha256", "manifest_sha256", "runtime",
                     "command", "evidence", "preflight", "authority", "authority_signature",
                     "attempt_id", "host", "unit_claim", "firmware_claim", "misty_units",
                     "approval_public_key", "approval_public_key_sha256", "verifier",
                     "operation", "operator", "limits"}
    if set(request) != expected_keys or request["operator"] != "Deb" or request["host"] != os.uname().nodename:
        raise RuntimeError("request_schema_or_host")
    if request["operation"] != "literal_none_observation" or request["limits"] != manifest["physical_limits"]:
        raise RuntimeError("request_scope_mismatch")
    interpreter = str(Path(sys.executable).resolve())
    if request["command"] != [interpreter, "-I", "-B", "-S", str(HERE), str(request_path)]:
        raise RuntimeError("command_mismatch")
    if request["manifest_sha256"] != MANIFEST_SHA or interpreter not in request["runtime"]:
        raise RuntimeError("request_pin_mismatch")
    probe = load_verified("none_gate", PROBE, manifest["sources"][str(PROBE.relative_to(ROOT))])
    if manifest["physical_limits"] != probe.physical_limits():
        raise RuntimeError("physical_limits_mismatch")
    request_hash = sha(request_bytes)
    preflight_bytes = read_regular(request["preflight"])
    preflight = json.loads(preflight_bytes, object_pairs_hook=unique)
    preflight_hash = sha(preflight_bytes)
    authority_bytes = read_regular(request["authority"])
    authority = json.loads(authority_bytes, object_pairs_hook=unique)
    probe.validate_authority(authority, request_hash, preflight_hash, request["attempt_id"],
                             lambda: verify_signature(request, authority_bytes))
    probe.validate_preflight(preflight, initial[0])
    probe.validate_binding(preflight, request)
    probe.remaining(preflight, authority, initial)
    evidence = Path(request["evidence"])
    if evidence.parent != EVIDENCE_ROOT or evidence.resolve() != evidence or os.path.lexists(evidence):
        raise RuntimeError("new_evidence_required")
    before = pins(request, manifest, probe)
    source = read_regular(HERE)
    if sha(source) != request["controller_sha256"]:
        raise RuntimeError("controller_changed")
    policy = probe.AbortPolicy()
    old_handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}

    def parent_signal(signum, frame):
        policy.receive(signum)

    def create_evidence():
        nonlocal created
        evidence.mkdir(mode=0o700)
        created = True

    reservation = {
        "stable_request_sha256": request_hash, "preflight_sha256": preflight_hash,
        "attempt_id": request["attempt_id"], "authority_sha256": sha(authority_bytes),
        "approval_reference": authority["approval_reference"], "approved_at": authority["approved_at"],
        "expires_at": authority["expires_at"], "observed_at": preflight["observed_at"],
        "parent_entry_sample": initial, "operator_postflight": "pending",
    }
    for sig in old_handlers:
        signal.signal(sig, parent_signal)
    created = False
    output, code, error, killed, after, final, cutoff = b"", None, None, False, None, None, None
    try:
        probe.reserve_attempt(create_evidence, lambda: persist_reservation(evidence, reservation),
                              lambda: sync_directory(EVIDENCE_ROOT))
        final = clock_sample()
        cutoff = probe.open_cutoff(preflight, authority, initial, final)
        bootstrap = ("namespace={'__name__':'_physical_worker','__file__':" + repr(str(HERE)) + "}\n"
                     "exec(compile(" + repr(source) + "," + repr(str(HERE)) + ",'exec'),namespace)\n"
                     "namespace['worker'](" + repr(tuple(request["runtime"])) + "," + repr(preflight)
                     + "," + repr(authority) + "," + repr(final) + "," + repr(cutoff) + ","
                     + repr(manifest) + ")\n")
        with tempfile.TemporaryFile(dir=evidence) as stream:
            stream.write(bootstrap.encode())
            stream.seek(0)
            output, code, error, killed = capture(
                [interpreter, "-I", "-B", "-S", "-"], policy, stream, manifest["physical_limits"]
            )
    except BaseException as failure:
        error = type(failure).__name__ + ":" + str(failure)
    finally:
        try:
            if created:
                try:
                    after = pins(request, manifest, probe)
                    if sha(read_regular(request_path)) != request_hash:
                        raise RuntimeError("request_changed")
                except BaseException as failure:
                    error = (error or "") + ":" + str(failure)
                report = probe.worker_report(output, lambda raw: json.loads(raw, object_pairs_hook=unique))
                if report is None:
                    error = (error or "") + ":worker_report_missing_or_invalid"
                with (evidence / "worker.log").open("xb") as stream:
                    stream.write(output)
                result = {"before": before, "after": after, "code": code, "error": error,
                          "reservation": reservation, "preflight": preflight,
                          "parent_final_sample": final, "monotonic_open_cutoff": cutoff,
                          "operator_postflight": "pending", "parent_signal": policy.signum,
                          "worker_killed": killed, "raw_lost_if_worker_killed": killed,
                          "worker_report_valid": report is not None,
                          "close_outcome": "unknown" if report is None else report["close"],
                          "pre_reservation_single_attempt_is_policy": True}
                with (evidence / "result.json").open("x") as stream:
                    json.dump(result, stream, indent=2)
        finally:
            for sig, handler in old_handlers.items():
                signal.signal(sig, handler)
    return 0 if code == 0 and error is None and policy.signum is None and before == after else 1


if __name__ == "__main__":
    raise SystemExit(main())
