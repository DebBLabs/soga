#!/usr/bin/env python3
"""Isolated exact-wheel installer. Create-only; not authorized to run."""

import base64
import csv
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time


PYTHON = "/usr/bin/python3"
EXPECTED_PYTHON = "Python 3.9.6"
EXPECTED_PIP = "21.2.4"
PIP_METADATA = Path("/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/site-packages/pip-21.2.4.dist-info/METADATA")
WHEEL_ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels")
INSTALL_PARENT = Path("/private/tmp/m02-aauth-fcf656d-phase1-install-20260921")
TARGET = INSTALL_PARENT / "site-packages"
SCRATCH = INSTALL_PARENT / "tmp"
TIMEOUT = 180
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
EXPECTED_DISTRIBUTIONS = {"cryptography": "50.0.1", "cffi": "2.0.0",
                          "pycparser": "2.23", "typing-extensions": "4.15.0"}


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def mode(path):
    return format(stat.S_IMODE(path.stat().st_mode), "04o")


def tree_inventory(root):
    if not root.exists():
        return []
    result = []
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        kind = "symlink" if path.is_symlink() else "file" if path.is_file() else "dir"
        entry = {"path": relative, "type": kind, "mode": mode(path)}
        if path.is_file() and not path.is_symlink():
            entry.update(size=path.stat().st_size, sha256=sha256(path))
        result.append(entry)
    return result


def repository_state():
    repo = Path(__file__).resolve().parents[2]
    env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C",
           "LC_ALL": "C", "GIT_OPTIONAL_LOCKS": "0"}
    head = subprocess.run(["/usr/bin/git", "-C", str(repo), "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True, timeout=10,
                          env=env)
    status = subprocess.run(["/usr/bin/git", "-C", str(repo), "status", "--porcelain"],
                            check=True, capture_output=True, text=True, timeout=10,
                            env=env)
    return {"root": str(repo), "head": head.stdout.strip(),
            "status_porcelain": status.stdout.splitlines()}


def static_pip_version():
    if not PIP_METADATA.is_file():
        raise RuntimeError("pinned pip metadata absent")
    versions = [line.split(":", 1)[1].strip() for line in
                PIP_METADATA.read_text(encoding="utf-8").splitlines()
                if line.startswith("Version:")]
    if versions != [EXPECTED_PIP]:
        raise RuntimeError("pinned pip version mismatch")
    return versions[0]


def verify_sources():
    actual = []
    expected_names = {entry[0] for entry in WHEELS} | {"evidence.json"}
    if {path.name for path in WHEEL_ROOT.iterdir()} != expected_names:
        raise RuntimeError("wheel source inventory mismatch")
    for filename, expected_size, expected_hash in WHEELS:
        path = WHEEL_ROOT / filename
        observed = {"path": str(path), "size": path.stat().st_size,
                    "mode": mode(path), "sha256": sha256(path)}
        if observed["size"] != expected_size or observed["sha256"] != expected_hash:
            raise RuntimeError("wheel source identity mismatch: " + filename)
        actual.append(observed)
    return actual


def parse_metadata(path):
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Name:") or line.startswith("Version:"):
            key, value = line.split(":", 1)
            values[key.lower()] = value.strip()
    return values


def verify_record(dist_info):
    record = dist_info / "RECORD"
    if not record.is_file():
        raise RuntimeError("missing RECORD: " + dist_info.name)
    checked = set()
    with open(record, newline="", encoding="utf-8") as handle:
        for relative, encoded_hash, encoded_size in csv.reader(handle):
            path = (TARGET / relative).resolve()
            if TARGET.resolve() not in path.parents:
                raise RuntimeError("RECORD path escapes target: " + relative)
            if not path.is_file() or path.is_symlink():
                raise RuntimeError("RECORD path absent or unsafe: " + relative)
            if not encoded_hash:
                if path != record:
                    raise RuntimeError("unexpected unhashed RECORD entry: " + relative)
                checked.add(str(path.relative_to(TARGET)))
                continue
            algorithm, value = encoded_hash.split("=", 1)
            if algorithm != "sha256":
                raise RuntimeError("unexpected RECORD hash algorithm")
            observed = base64.urlsafe_b64encode(bytes.fromhex(sha256(path))).decode().rstrip("=")
            if observed != value or path.stat().st_size != int(encoded_size):
                raise RuntimeError("RECORD verification failed: " + relative)
            checked.add(str(path.relative_to(TARGET)))
    return checked


def verify_installation():
    found = {}
    records = {}
    accounted = set()
    for dist_info in sorted(TARGET.glob("*.dist-info")):
        metadata = parse_metadata(dist_info / "METADATA")
        name = metadata.get("name", "").lower().replace("_", "-")
        version = metadata.get("version")
        if name in found:
            raise RuntimeError("duplicate installed distribution: " + name)
        found[name] = version
        record_paths = verify_record(dist_info)
        records[name] = len(record_paths)
        accounted.update(record_paths)
    if found != EXPECTED_DISTRIBUTIONS:
        raise RuntimeError("installed distribution set mismatch")
    if any(path.is_symlink() for path in TARGET.rglob("*")):
        raise RuntimeError("installed tree contains symlink")
    actual_files = {str(path.relative_to(TARGET)) for path in TARGET.rglob("*")
                    if path.is_file() and not path.is_symlink()}
    if actual_files != accounted:
        raise RuntimeError("installed tree contains unaccounted or missing RECORD files")
    return {"distributions": found, "record_entries_verified": records}


def write_evidence(record):
    path = INSTALL_PARENT / "evidence.json"
    tmp = INSTALL_PARENT / "evidence.json.partial"
    with open(tmp, "xb") as handle:
        handle.write((json.dumps(record, indent=2, sort_keys=True) + "\n").encode())
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    os.chmod(path, 0o400)


def main():
    if len(sys.argv) != 1:
        raise SystemExit("no command-line arguments permitted")
    controller_hash = sha256(Path(__file__))
    repo = repository_state()
    pip_version = static_pip_version()
    sources = verify_sources()
    if INSTALL_PARENT.exists() or TARGET.exists() or SCRATCH.exists():
        raise SystemExit("refusing pre-existing install path")
    INSTALL_PARENT.mkdir(mode=0o700)
    TARGET.mkdir(mode=0o700)
    SCRATCH.mkdir(mode=0o700)
    before = tree_inventory(INSTALL_PARENT)
    env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C", "LC_ALL": "C",
           "PIP_CONFIG_FILE": "/dev/null", "PIP_NO_INDEX": "1",
           "PIP_DISABLE_PIP_VERSION_CHECK": "1", "PIP_NO_CACHE_DIR": "1",
           "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1",
           "TMPDIR": str(SCRATCH)}
    command = [PYTHON, "-m", "pip", "install", "--no-index", "--no-deps",
               "--only-binary=:all:", "--no-cache-dir", "--no-compile",
               "--target", str(TARGET)] + [str(WHEEL_ROOT / item[0]) for item in WHEELS]
    record = {"started_at": utc_now(), "controller_sha256": controller_hash,
              "repository": repo, "python_expected": EXPECTED_PYTHON,
              "pip_version_static": pip_version, "sources": sources,
              "target": str(TARGET), "scratch": str(SCRATCH),
              "inventory_before": before, "command": command,
              "environment": env, "result": "RUNNING"}
    try:
        version = subprocess.run([PYTHON, "--version"], check=True,
                                 capture_output=True, text=True, timeout=10, env=env)
        observed_python = (version.stdout or version.stderr).strip()
        record["python_observed"] = observed_python
        if observed_python != EXPECTED_PYTHON:
            raise RuntimeError("Python version mismatch")
        completed = subprocess.run(command, stdin=subprocess.DEVNULL,
                                   capture_output=True, text=True, timeout=TIMEOUT,
                                   check=False, env=env)
        record.update(pip_exit_status=completed.returncode,
                      pip_stdout=completed.stdout, pip_stderr=completed.stderr)
        if completed.returncode != 0:
            raise RuntimeError("pip installation failed")
        if any(SCRATCH.iterdir()):
            raise RuntimeError("pip scratch directory not empty")
        record["sources_after"] = verify_sources()
        record["installed"] = verify_installation()
        SCRATCH.rmdir()
        record["scratch_removed"] = True
        record["inventory_after"] = tree_inventory(INSTALL_PARENT)
        record.update(result="VERIFIED_INSTALLATION", finished_at=utc_now())
        write_evidence(record)
        return 0
    except Exception as exc:
        record.update(result="FAILED", error=type(exc).__name__ + ": " + str(exc),
                      inventory_after=tree_inventory(INSTALL_PARENT),
                      finished_at=utc_now())
        write_evidence(record)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
