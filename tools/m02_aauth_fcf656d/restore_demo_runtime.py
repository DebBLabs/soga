#!/usr/bin/env python3
"""Recover the exact durable AAuth demo provider. Create-only under D-118."""

import base64
import csv
import hashlib
import http.client
import json
import os
from pathlib import Path, PurePosixPath
import platform
import ssl
import stat
import subprocess
import sys
import time
from urllib.parse import urlsplit


REPO = Path(__file__).resolve().parents[2]
EVIDENCE_PARENT = REPO.parent / "research-evidence"
DURABLE_ROOT = EVIDENCE_PARENT / "soga"
WHEEL_ROOT = DURABLE_ROOT / "inputs/aauth/fcf656d/wheels"
RUNTIME_ROOT = DURABLE_ROOT / "runtimes/aauth-fcf656d-provider"
TARGET = RUNTIME_ROOT / "site-packages"
SCRATCH = RUNTIME_ROOT / "scratch"
MANIFEST_ROOT = DURABLE_ROOT / "manifests"
MANIFEST_PATH = MANIFEST_ROOT / "aauth-fcf656d-provider.json"
PYTHON = "/usr/bin/python3"
EXPECTED_PYTHON = "3.9.6"
EXPECTED_EXECUTABLE = ("/Library/Developer/CommandLineTools/Library/Frameworks/"
                       "Python3.framework/Versions/3.9/bin/python3.9")
EXPECTED_PLATFORM = "darwin"
EXPECTED_MACHINE = "arm64"
EXPECTED_PIP = "21.2.4"
PIP_METADATA = Path("/Library/Developer/CommandLineTools/Library/Frameworks/"
                    "Python3.framework/Versions/3.9/lib/python3.9/site-packages/"
                    "pip-21.2.4.dist-info/METADATA")
CONNECT_TIMEOUT = 15
ARTIFACT_TIMEOUT = 120
INSTALL_TIMEOUT = 180
CHUNK = 65_536
READ_MARGIN = 65_536
STREAM_LIMIT = 2_000_000
WHEELS = (
    ("cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl", 4_035_307,
     "ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0",
     "https://files.pythonhosted.org/packages/84/a9/ee16a903f13755e914d1eecc482fe64d1f10761c3960e5d8fa6837377aff/cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl"),
    ("cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl", 180_509,
     "de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7",
     "https://files.pythonhosted.org/packages/3d/de/38d9726324e127f727b4ecc376bc85e505bfe61ef130eaf3f290c6847dd4/cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl"),
    ("pycparser-2.23-py3-none-any.whl", 118_140,
     "e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934",
     "https://files.pythonhosted.org/packages/a0/e3/59cd50310fc9b59512193629e1984c1f95e5c8ae6e5d8c69532ccc65a7fe/pycparser-2.23-py3-none-any.whl"),
    ("typing_extensions-4.15.0-py3-none-any.whl", 44_614,
     "f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548",
     "https://files.pythonhosted.org/packages/18/67/36e9267722cc04a6b9f15c7f3441c2363321a3ea07da7ae0c0707beb2a9c/typing_extensions-4.15.0-py3-none-any.whl"),
)
EXPECTED_DISTRIBUTIONS = {
    "cryptography": "50.0.1", "cffi": "2.0.0",
    "pycparser": "2.23", "typing-extensions": "4.15.0",
}
BASE_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C", "LC_ALL": "C",
    "GIT_OPTIONAL_LOCKS": "0", "PIP_CONFIG_FILE": "/dev/null",
    "PIP_NO_INDEX": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1",
    "PIP_NO_CACHE_DIR": "1", "PYTHONNOUSERSITE": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
}
NETWORK_DENIED_PIP = """
import runpy, sys
def deny_network(event, args):
    if event.startswith('socket.'):
        raise RuntimeError('network prohibited after acquisition: ' + event)
sys.addaudithook(deny_network)
sys.argv = ['pip'] + sys.argv[1:]
runpy.run_module('pip', run_name='__main__')
"""


class RetrievalError(RuntimeError):
    """Carry bounded failed-request evidence to the durable manifest."""

    def __init__(self, message, record):
        super().__init__(message)
        self.record = record


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def mode(path):
    return format(stat.S_IMODE(path.lstat().st_mode), "04o")


def require_confined(path, root):
    resolved_parent = path.parent.resolve(strict=True)
    require(resolved_parent == root or root in resolved_parent.parents,
            "path escapes dedicated durable root: " + str(path))
    require(EVIDENCE_PARENT.resolve(strict=True) not in (path.resolve(strict=False),),
            "refusing evidence-parent target")


def atomic_write(path, data, final_mode=0o400):
    require_confined(path, DURABLE_ROOT.resolve(strict=True))
    partial = path.with_name(path.name + ".partial")
    with partial.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    partial.chmod(final_mode)
    partial.replace(path)


def file_identity(path):
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode) and not path.is_symlink(),
            "unsafe file: " + str(path))
    return {"path": str(path), "mode": mode(path), "size": metadata.st_size,
            "sha256": sha256(path)}


def repository_state():
    env = {key: BASE_ENV[key] for key in ("PATH", "LANG", "LC_ALL", "GIT_OPTIONAL_LOCKS")}
    head = subprocess.run(["/usr/bin/git", "-C", str(REPO), "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True, timeout=10, env=env)
    status = subprocess.run(["/usr/bin/git", "-C", str(REPO), "status", "--porcelain"],
                            check=True, capture_output=True, text=True, timeout=10, env=env)
    return {"root": str(REPO), "head": head.stdout.strip(),
            "status_porcelain": status.stdout.splitlines()}


def environment_identity():
    observed = {"python": platform.python_version(), "sys_platform": sys.platform,
                "machine": platform.machine(), "pip": static_pip_version(),
                "resolved_executable": str(Path(sys.executable).resolve())}
    expected = {"python": EXPECTED_PYTHON, "sys_platform": EXPECTED_PLATFORM,
                "machine": EXPECTED_MACHINE, "pip": EXPECTED_PIP,
                "resolved_executable": EXPECTED_EXECUTABLE}
    require(observed == expected, "pinned environment mismatch")
    return observed


def static_pip_version():
    require(PIP_METADATA.is_file() and not PIP_METADATA.is_symlink(),
            "pinned pip metadata absent or unsafe")
    versions = [line.split(":", 1)[1].strip()
                for line in PIP_METADATA.read_text(encoding="utf-8").splitlines()
                if line.startswith("Version:")]
    require(versions == [EXPECTED_PIP], "pinned pip version mismatch")
    return versions[0]


def prepare_roots():
    require(EVIDENCE_PARENT.is_dir() and not EVIDENCE_PARENT.is_symlink(),
            "durable evidence parent absent or unsafe")
    require(not WHEEL_ROOT.exists() and not RUNTIME_ROOT.exists() and not MANIFEST_PATH.exists(),
            "recovery target already exists")
    paths = (
        DURABLE_ROOT,
        DURABLE_ROOT / "inputs",
        DURABLE_ROOT / "inputs/aauth",
        DURABLE_ROOT / "inputs/aauth/fcf656d",
        WHEEL_ROOT,
        DURABLE_ROOT / "runtimes",
        RUNTIME_ROOT,
        TARGET,
        SCRATCH,
        MANIFEST_ROOT,
    )
    for path in paths:
        if path.exists() or path.is_symlink():
            require(path.is_dir() and not path.is_symlink(),
                    "durable path component is unsafe: " + str(path))
        else:
            path.mkdir(mode=0o700)
        require(path.resolve(strict=True) == path and
                (path == DURABLE_ROOT or DURABLE_ROOT in path.parents),
                "durable path component escaped root: " + str(path))


def retrieve(filename, expected_size, expected_hash, url):
    parsed = urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname == "files.pythonhosted.org"
            and parsed.port is None and parsed.username is None and parsed.password is None
            and parsed.fragment == "", "fixed wheel URL policy violation")
    started = time.monotonic()
    partial = WHEEL_ROOT / (filename + ".partial")
    final = WHEEL_ROOT / filename
    record = {"filename": filename, "url": url, "expected_size": expected_size,
              "expected_sha256": expected_hash, "redirect_count": 0,
              "started_at": utc_now()}
    received = 0
    digest = hashlib.sha256()
    connection = http.client.HTTPSConnection(parsed.hostname, 443,
                                              timeout=CONNECT_TIMEOUT,
                                              context=ssl.create_default_context())
    try:
        request_path = parsed.path + (("?" + parsed.query) if parsed.query else "")
        connection.request("GET", request_path,
                           headers={"Accept": "application/octet-stream",
                                    "User-Agent": "SOGA-bounded-recovery/1"})
        response = connection.getresponse()
        record.update(http_status=response.status, location=response.getheader("Location"))
        require(not (300 <= response.status < 400) and record["location"] is None,
                "redirect refused")
        require(response.status == 200, "unexpected HTTP status")
        declared = response.getheader("Content-Length")
        require(declared is None or int(declared) == expected_size,
                "declared content length mismatch")
        with partial.open("xb") as handle:
            partial.chmod(0o600)
            while True:
                remaining = ARTIFACT_TIMEOUT - (time.monotonic() - started)
                require(remaining > 0, "artifact timeout")
                require(connection.sock is not None, "TLS socket unavailable")
                connection.sock.settimeout(min(remaining, CONNECT_TIMEOUT))
                block = response.read(CHUNK)
                if not block:
                    break
                received += len(block)
                require(received <= expected_size + READ_MARGIN, "artifact byte limit exceeded")
                digest.update(block)
                handle.write(block)
            handle.flush()
            os.fsync(handle.fileno())
        require(received == expected_size and digest.hexdigest() == expected_hash,
                "wheel identity mismatch")
        partial.replace(final)
        final.chmod(0o400)
        record.update(result="VERIFIED", received_size=received,
                      observed_sha256=digest.hexdigest(), finished_at=utc_now())
        return record
    except Exception as error:
        record.update(result="FAILED", error_type=type(error).__name__,
                      error=str(error), received_size=received,
                      observed_sha256=digest.hexdigest(), finished_at=utc_now())
        if partial.exists():
            if received == expected_size:
                quarantine = WHEEL_ROOT / (filename + ".UNVERIFIED")
                partial.replace(quarantine)
                quarantine.chmod(0o400)
                record["quarantine"] = file_identity(quarantine)
            else:
                partial.unlink()
                record["partial_removed_after_identity_recorded"] = True
        raise RetrievalError(str(error), record) from error
    finally:
        connection.close()


def confined_record_path(relative):
    pure = PurePosixPath(relative)
    require(relative and not pure.is_absolute() and ".." not in pure.parts,
            "unsafe RECORD path")
    candidate = TARGET.joinpath(*pure.parts)
    require(TARGET in candidate.parents, "RECORD path escapes target")
    return candidate


def metadata_identity(path):
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Name:") or line.startswith("Version:"):
            key, value = line.split(":", 1)
            require(key.lower() not in values, "duplicate metadata identity")
            values[key.lower()] = value.strip()
    return values.get("name", "").lower().replace("_", "-"), values.get("version")


def verify_record(dist_info):
    record_path = dist_info / "RECORD"
    require(record_path.is_file() and not record_path.is_symlink(), "missing RECORD")
    checked = set()
    with record_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            require(len(row) == 3, "invalid RECORD row")
            relative, encoded_hash, encoded_size = row
            require(relative not in checked, "duplicate RECORD path")
            path = confined_record_path(relative)
            require(path.is_file() and not path.is_symlink(), "unsafe RECORD target")
            if not encoded_hash or not encoded_size:
                require(path == record_path and not encoded_hash and not encoded_size,
                        "unexpected unhashed RECORD entry")
            else:
                algorithm, value = encoded_hash.split("=", 1)
                observed = base64.urlsafe_b64encode(bytes.fromhex(sha256(path))).decode().rstrip("=")
                require(algorithm == "sha256" and observed == value
                        and path.stat().st_size == int(encoded_size), "RECORD mismatch")
            checked.add(relative)
    return checked


def verify_installation():
    require(TARGET.is_dir() and not TARGET.is_symlink(), "installed target unsafe")
    require(not any(path.is_symlink() for path in TARGET.rglob("*")),
            "installed tree contains symlink")
    found = {}
    accounted = set()
    record_counts = {}
    dist_infos = sorted(TARGET.rglob("*.dist-info"))
    require(all(path.parent == TARGET and path.is_dir() for path in dist_infos),
            "nested distribution metadata")
    for dist_info in dist_infos:
        name, version = metadata_identity(dist_info / "METADATA")
        require(name in EXPECTED_DISTRIBUTIONS and name not in found,
                "unexpected or duplicate distribution")
        found[name] = version
        entries = verify_record(dist_info)
        accounted.update(entries)
        record_counts[name] = len(entries)
    require(found == EXPECTED_DISTRIBUTIONS, "distribution identity mismatch")
    actual = {str(path.relative_to(TARGET)) for path in TARGET.rglob("*")
              if path.is_file() and not path.is_symlink()}
    require(actual == accounted, "unaccounted installed file")
    return {"distributions": found, "record_entries_verified": record_counts,
            "regular_files_verified": len(actual)}


def verify_scratch():
    require(SCRATCH.is_dir() and not SCRATCH.is_symlink(), "scratch unsafe")
    entries = list(os.scandir(SCRATCH))
    require(len(entries) <= 1, "unexpected scratch inventory")
    if not entries:
        return {"entries": 0}
    require(entries[0].name == "xcrun_db", "unexpected scratch artifact")
    item = file_identity(SCRATCH / "xcrun_db")
    require(item["mode"] == "0600" and item["size"] <= 4096,
            "xcrun_db policy mismatch")
    return {"entries": 1, "xcrun_db": item}


def main():
    require(len(sys.argv) == 1, "no command-line arguments permitted")
    before_repo = repository_state()
    environment = environment_identity()
    controller = file_identity(Path(__file__).resolve())
    prepare_roots()
    record = {"result": "RUNNING", "started_at": utc_now(), "authority": "D-118",
              "controller": controller, "repository_before": before_repo,
              "environment": environment, "durable_root": str(DURABLE_ROOT),
              "wheel_retrievals": []}
    try:
        for wheel in WHEELS:
            try:
                record["wheel_retrievals"].append(retrieve(*wheel))
            except RetrievalError as error:
                record["wheel_retrievals"].append(error.record)
                raise
        verified_wheels = [file_identity(WHEEL_ROOT / item[0]) for item in WHEELS]
        env = dict(BASE_ENV)
        env["TMPDIR"] = str(SCRATCH)
        command = [PYTHON, "-I", "-B", "-c", NETWORK_DENIED_PIP,
                   "install", "--no-index", "--no-deps", "--only-binary=:all:",
                   "--no-cache-dir", "--no-compile", "--target", str(TARGET)]
        command.extend(str(WHEEL_ROOT / item[0]) for item in WHEELS)
        completed = subprocess.run(command, cwd=REPO, env=env, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   timeout=INSTALL_TIMEOUT, check=False)
        require(len(completed.stdout) <= STREAM_LIMIT and len(completed.stderr) <= STREAM_LIMIT,
                "pip output limit exceeded")
        record.update(pip_command=command, pip_returncode=completed.returncode,
                      pip_stdout_length=len(completed.stdout),
                      pip_stdout_sha256=hashlib.sha256(completed.stdout).hexdigest(),
                      pip_stdout=completed.stdout.decode("utf-8", errors="replace"),
                      pip_stderr_length=len(completed.stderr),
                      pip_stderr_sha256=hashlib.sha256(completed.stderr).hexdigest(),
                      pip_stderr=completed.stderr.decode("utf-8", errors="replace"))
        require(completed.returncode == 0, "pip installation failed")
        installed = verify_installation()
        scratch = verify_scratch()
        require(verified_wheels == [file_identity(WHEEL_ROOT / item[0]) for item in WHEELS],
                "wheel changed during installation")
        after_repo = repository_state()
        require(after_repo == before_repo, "repository changed during recovery")
        record.update(result="VERIFIED_DURABLE_RUNTIME", finished_at=utc_now(),
                      wheels=verified_wheels, installed=installed, scratch=scratch,
                      repository_after=after_repo)
        atomic_write(MANIFEST_PATH,
                     (json.dumps(record, sort_keys=True, indent=2) + "\n").encode())
        return 0
    except Exception as error:
        record.update(result="FAILED", finished_at=utc_now(),
                      error_type=type(error).__name__, error=str(error))
        atomic_write(MANIFEST_PATH,
                     (json.dumps(record, sort_keys=True, indent=2) + "\n").encode())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
