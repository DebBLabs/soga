#!/usr/bin/env python3
"""Bounded exact-wheel acquisition controller. Create-only; not yet authorized to run."""

import hashlib
import http.client
import json
import os
from pathlib import Path
import ssl
import stat
import subprocess
import sys
import time
from urllib.parse import urlsplit


ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels")
CONNECT_TIMEOUT = 15
TOTAL_TIMEOUT = 120
READ_MARGIN = 65_536
CHUNK = 65_536
MANIFEST = (
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


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def mode(path):
    return format(stat.S_IMODE(path.stat().st_mode), "04o")


def inventory():
    return [{"name": path.name, "mode": mode(path), "size": path.stat().st_size,
             "type": "file" if path.is_file() else "other"}
            for path in sorted(ROOT.iterdir())]


def repository_state():
    repo = Path(__file__).resolve().parents[2]
    git_env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C",
               "LC_ALL": "C", "GIT_OPTIONAL_LOCKS": "0"}
    head = subprocess.run(["/usr/bin/git", "-C", str(repo), "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True, timeout=10,
                          env=git_env)
    tree = subprocess.run(["/usr/bin/git", "-C", str(repo), "status", "--porcelain"],
                          check=True, capture_output=True, text=True, timeout=10,
                          env=git_env)
    return {"root": str(repo), "head": head.stdout.strip(),
            "status_porcelain": tree.stdout.splitlines()}


def write_evidence(record):
    path = ROOT / "evidence.json"
    tmp = ROOT / "evidence.json.partial"
    data = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode()
    with open(tmp, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    os.chmod(path, 0o600)


def retrieve(filename, expected_size, expected_hash, url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "files.pythonhosted.org" or parsed.port:
        raise RuntimeError("manifest URL violates fixed HTTPS host policy")
    path = parsed.path + (("?" + parsed.query) if parsed.query else "")
    started = time.monotonic()
    item = {"filename": filename, "url": url, "started_at": utc_now(),
            "expected_size": expected_size, "expected_sha256": expected_hash,
            "redirect_count": 0, "redirect_chain": []}
    connection = http.client.HTTPSConnection(parsed.hostname, 443,
                                              timeout=CONNECT_TIMEOUT,
                                              context=ssl.create_default_context())
    partial = ROOT / (filename + ".partial")
    try:
        connection.request("GET", path, headers={"Accept": "application/octet-stream",
                                                  "User-Agent": "SOGA-bounded-research/1"})
        response = connection.getresponse()
        item["http_status"] = response.status
        item["location"] = response.getheader("Location")
        if 300 <= response.status < 400 or item["location"] is not None:
            item["redirect_count"] = 1
            item["redirect_chain"] = [item["location"]]
            raise RuntimeError("redirect refused")
        if response.status != 200:
            raise RuntimeError("unexpected HTTP status")
        sock = connection.sock
        if sock is None:
            raise RuntimeError("TLS socket unavailable")
        item["tls"] = {"version": sock.version(), "cipher": sock.cipher()[0],
                       "peer_certificate_sha256": hashlib.sha256(
                           sock.getpeercert(binary_form=True)).hexdigest()}
        declared = response.getheader("Content-Length")
        item["declared_content_length"] = declared
        if declared is not None and int(declared) != expected_size:
            raise RuntimeError("declared content length mismatch")
        digest = hashlib.sha256()
        received = 0
        with open(partial, "xb") as handle:
            os.chmod(partial, 0o600)
            while True:
                remaining = TOTAL_TIMEOUT - (time.monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError("total artifact timeout")
                sock.settimeout(min(remaining, CONNECT_TIMEOUT))
                block = response.read(CHUNK)
                if not block:
                    break
                received += len(block)
                if received > expected_size + READ_MARGIN:
                    raise RuntimeError("response body exceeded bounded cap")
                digest.update(block)
                handle.write(block)
            handle.flush()
            os.fsync(handle.fileno())
        observed_hash = digest.hexdigest()
        item.update(received_size=received, observed_sha256=observed_hash,
                    finished_at=utc_now())
        if received != expected_size:
            partial.unlink(missing_ok=True)
            raise RuntimeError("received content length mismatch")
        if observed_hash != expected_hash:
            quarantine = ROOT / (filename + ".UNVERIFIED")
            os.replace(partial, quarantine)
            os.chmod(quarantine, 0o400)
            item.update(final_path=str(quarantine), final_mode=mode(quarantine))
            raise RuntimeError("SHA-256 mismatch; complete artifact quarantined")
        final = ROOT / filename
        os.replace(partial, final)
        os.chmod(final, 0o400)
        item.update(result="VERIFIED", final_path=str(final), final_mode=mode(final))
        return item
    except Exception as exc:
        if partial.exists():
            partial.unlink()
        item.update(result="FAILED", error=type(exc).__name__ + ": " + str(exc),
                    finished_at=utc_now())
        raise RuntimeError(json.dumps(item, sort_keys=True)) from exc
    finally:
        connection.close()


def main():
    if len(sys.argv) != 1:
        raise SystemExit("no command-line arguments permitted")
    controller_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    repo_state = repository_state()
    if ROOT.exists() or ROOT.parent.exists():
        raise SystemExit("refusing pre-existing target root or parent")
    ROOT.parent.mkdir(mode=0o700)
    ROOT.mkdir(mode=0o700)
    os.chmod(ROOT.parent, 0o700)
    os.chmod(ROOT, 0o700)
    record = {"controller": Path(__file__).name, "started_at": utc_now(),
              "controller_sha256": controller_hash,
              "repository": repo_state, "target": str(ROOT),
              "target_parent_mode": mode(ROOT.parent), "target_initial_mode": mode(ROOT),
              "inventory_before": inventory(), "items": [], "result": "RUNNING"}
    try:
        for entry in MANIFEST:
            record["items"].append(retrieve(*entry))
        if sorted(p.name for p in ROOT.iterdir()) != sorted(
                [entry[0] for entry in MANIFEST]):
            raise RuntimeError("unexpected file inventory before evidence write")
        record.update(result="VERIFIED", finished_at=utc_now())
        record["inventory_after"] = inventory()
        record["preservation_modes_intended"] = {
            "files": "0400", "evidence": "0400", "target": "0500",
            "target_parent": "0700"}
        write_evidence(record)
        for path in ROOT.iterdir():
            os.chmod(path, 0o400)
        os.chmod(ROOT, 0o500)
        return 0
    except Exception as exc:
        try:
            detail = json.loads(str(exc))
            if isinstance(detail, dict):
                record["items"].append(detail)
        except (json.JSONDecodeError, TypeError):
            record["error"] = type(exc).__name__ + ": " + str(exc)
        else:
            if not isinstance(detail, dict):
                record["error"] = type(exc).__name__ + ": " + str(exc)
        record.update(result="FAILED", finished_at=utc_now())
        record["inventory_after"] = inventory()
        write_evidence(record)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
