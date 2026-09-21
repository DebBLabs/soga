#!/usr/bin/env python3
"""Statically verify the preserved D-093 installation without importing it."""

import base64
import csv
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys


REPO = Path(__file__).resolve().parents[2]
WHEEL_ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels")
INSTALL_PARENT = Path("/private/tmp/m02-aauth-fcf656d-phase1-install-20260921")
TARGET = INSTALL_PARENT / "site-packages"
SCRATCH = INSTALL_PARENT / "tmp"
RAW_EVIDENCE = INSTALL_PARENT / "evidence.json"
CONTROLLER = REPO / "tools/m02_aauth_fcf656d/install_verified_wheels.py"
RAW_EVIDENCE_SHA256 = "caaacd3791b77e83668d94769c7226c7ecd65a41105cab2996b391798f9a6bb3"
CONTROLLER_SHA256 = "84f4594b25a68f4560eeb575b7977cbfc7047331daddf9006ea578a2acd34b13"
XCRUN_DB_SHA256 = "767b97e4e6c44f3e9a7b2496c54bcc1c3901650873f4fc67d811e051bd9f6e8b"
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
EXPECTED_DISTRIBUTIONS = {
    "cryptography": "50.0.1",
    "cffi": "2.0.0",
    "pycparser": "2.23",
    "typing-extensions": "4.15.0",
}
GIT_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
    "LANG": "C",
    "LC_ALL": "C",
    "GIT_OPTIONAL_LOCKS": "0",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def file_identity(path):
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), "not a regular file: " + str(path))
    require(not path.is_symlink(), "symlink rejected: " + str(path))
    return {"path": str(path), "mode": format(stat.S_IMODE(metadata.st_mode), "04o"),
            "size": metadata.st_size, "sha256": sha256(path)}


def repository_state():
    head = subprocess.run(
        ["/usr/bin/git", "-C", str(REPO), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True, timeout=10, env=GIT_ENV)
    status = subprocess.run(
        ["/usr/bin/git", "-C", str(REPO), "status", "--porcelain"],
        check=True, capture_output=True, text=True, timeout=10, env=GIT_ENV)
    return {"root": str(REPO), "head": head.stdout.strip(),
            "status_porcelain": status.stdout.splitlines()}


def inventory(root):
    require(root.is_dir() and not root.is_symlink(), "inventory root absent or unsafe")
    result = []

    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in sorted(entries, key=lambda item: item.name):
                path = Path(entry.path)
                relative = str(path.relative_to(root))
                metadata = entry.stat(follow_symlinks=False)
                require(not entry.is_symlink(), "symlink rejected: " + relative)
                if stat.S_ISDIR(metadata.st_mode):
                    result.append({"path": relative, "type": "dir",
                                   "mode": format(stat.S_IMODE(metadata.st_mode), "04o")})
                    walk(path)
                elif stat.S_ISREG(metadata.st_mode):
                    result.append({"path": relative, "type": "file",
                                   "mode": format(stat.S_IMODE(metadata.st_mode), "04o"),
                                   "size": metadata.st_size, "sha256": sha256(path)})
                else:
                    raise RuntimeError("non-regular installation entry: " + relative)

    walk(root)
    return result


def verify_sources():
    expected_names = {item[0] for item in WHEELS} | {"evidence.json"}
    require(WHEEL_ROOT.is_dir() and not WHEEL_ROOT.is_symlink(), "wheel root absent or unsafe")
    require({entry.name for entry in os.scandir(WHEEL_ROOT)} == expected_names,
            "wheel source inventory mismatch")
    observed = []
    for filename, expected_size, expected_hash in WHEELS:
        item = file_identity(WHEEL_ROOT / filename)
        require(item["size"] == expected_size and item["sha256"] == expected_hash,
                "wheel identity mismatch: " + filename)
        observed.append(item)
    return observed


def metadata_identity(metadata_path):
    require(metadata_path.is_file() and not metadata_path.is_symlink(),
            "missing or unsafe METADATA: " + str(metadata_path))
    name = version = None
    with open(metadata_path, "r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("Name:"):
                require(name is None, "duplicate Name field")
                name = line.split(":", 1)[1].strip().lower().replace("_", "-")
            elif line.startswith("Version:"):
                require(version is None, "duplicate Version field")
                version = line.split(":", 1)[1].strip()
    require(name is not None and version is not None, "incomplete METADATA identity")
    return name, version


def confined_record_path(relative):
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and relative != "" and ".." not in pure.parts,
            "unsafe RECORD path: " + relative)
    candidate = TARGET.joinpath(*pure.parts)
    require(candidate == TARGET or TARGET in candidate.parents,
            "RECORD path escapes target: " + relative)
    return candidate


def verify_record(dist_info):
    record = dist_info / "RECORD"
    require(record.is_file() and not record.is_symlink(), "missing or unsafe RECORD")
    checked = set()
    with open(record, newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            require(len(row) == 3, "invalid RECORD row")
            relative, encoded_hash, encoded_size = row
            require(relative not in checked, "duplicate RECORD path: " + relative)
            path = confined_record_path(relative)
            require(path.is_file() and not path.is_symlink(),
                    "RECORD path absent or unsafe: " + relative)
            if encoded_hash == "" or encoded_size == "":
                require(path == record and encoded_hash == "" and encoded_size == "",
                        "unexpected unhashed RECORD entry: " + relative)
            else:
                require("=" in encoded_hash, "malformed RECORD hash")
                algorithm, value = encoded_hash.split("=", 1)
                require(algorithm == "sha256", "unexpected RECORD hash algorithm")
                observed = base64.urlsafe_b64encode(
                    bytes.fromhex(sha256(path))).decode("ascii").rstrip("=")
                require(observed == value and path.stat().st_size == int(encoded_size),
                        "RECORD verification failed: " + relative)
            checked.add(relative)
    return checked


def verify_installation():
    require(TARGET.is_dir() and not TARGET.is_symlink(), "installed target absent or unsafe")
    found = {}
    record_counts = {}
    accounted = set()
    dist_infos = sorted(TARGET.rglob("*.dist-info"))
    require(all(path.parent == TARGET and path.is_dir() and not path.is_symlink()
                for path in dist_infos), "nested or unsafe .dist-info entry")
    for dist_info in sorted(dist_infos):
        name, version = metadata_identity(dist_info / "METADATA")
        require(name not in found, "duplicate installed distribution: " + name)
        require(name in EXPECTED_DISTRIBUTIONS, "unexpected installed distribution: " + name)
        found[name] = version
        paths = verify_record(dist_info)
        accounted.update(paths)
        record_counts[name] = len(paths)
    require(found == EXPECTED_DISTRIBUTIONS, "installed distribution set mismatch")
    actual_files = {
        item["path"] for item in inventory(TARGET) if item["type"] == "file"
    }
    require(actual_files == accounted, "RECORD union does not equal installed files")
    return {"distributions": found, "record_entries_verified": record_counts,
            "regular_files_verified": len(actual_files)}


def verify_scratch():
    require(SCRATCH.is_dir() and not SCRATCH.is_symlink(), "scratch absent or unsafe")
    entries = list(os.scandir(SCRATCH))
    require(len(entries) == 1 and entries[0].name == "xcrun_db",
            "scratch inventory mismatch")
    item = file_identity(SCRATCH / "xcrun_db")
    require(item["mode"] == "0600" and item["size"] == 499 and
            item["sha256"] == XCRUN_DB_SHA256, "xcrun_db identity mismatch")
    return item


def main():
    require(len(sys.argv) == 1, "no command-line arguments permitted")
    self_identity = file_identity(Path(__file__))
    repository = repository_state()
    sources_before = verify_sources()
    raw_before = file_identity(RAW_EVIDENCE)
    controller = file_identity(CONTROLLER)
    require(raw_before["sha256"] == RAW_EVIDENCE_SHA256, "D-093 evidence hash mismatch")
    require(controller["sha256"] == CONTROLLER_SHA256, "controller hash mismatch")
    parent_inventory = inventory(INSTALL_PARENT)
    installation = verify_installation()
    scratch = verify_scratch()
    sources_after = verify_sources()
    raw_after = file_identity(RAW_EVIDENCE)
    require(sources_after == sources_before, "wheel sources changed during verification")
    require(raw_after == raw_before, "D-093 evidence changed during verification")
    result = {
        "result": "STATIC_INSTALLATION_VERIFIED",
        "claim_boundary": "identity, containment, and RECORD completeness only",
        "verifier": self_identity,
        "repository": repository,
        "wheel_sources_before": sources_before,
        "installation_parent_inventory": parent_inventory,
        "installation": installation,
        "scratch": scratch,
        "wheel_sources_after": sources_after,
        "d093_evidence_before": raw_before,
        "d093_evidence_after": raw_after,
        "installation_controller": controller,
        "access_time_caveat": "ordinary reads may update filesystem access metadata",
    }
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        sys.stdout.write(json.dumps({
            "result": "FAILED",
            "error_type": type(error).__name__,
            "error": str(error),
        }, indent=2, sort_keys=True) + "\n")
        raise SystemExit(1)
