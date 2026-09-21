#!/usr/bin/env python3
"""Bounded normative-source retrieval controller. Create-only; not authorized to run."""

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


ROOT = Path("/private/tmp/m02-aauth-fcf656d-phase-b0-20260921/sources")
CONNECT_TIMEOUT = 15
TOTAL_TIMEOUT = 120
MAX_BYTES = 2_097_152
CHUNK = 65_536
DOCUMENTS = (
    ("rfc9421.txt", "https://www.rfc-editor.org/rfc/rfc9421.txt",
     (b"Request for Comments: 9421", b"HTTP Message Signatures", b"February 2024")),
    ("rfc9530.txt", "https://www.rfc-editor.org/rfc/rfc9530.txt",
     (b"Request for Comments: 9530", b"Digest Fields", b"February 2024")),
    ("rfc9651.txt", "https://www.rfc-editor.org/rfc/rfc9651.txt",
     (b"Request for Comments: 9651", b"Structured Field Values for HTTP", b"September 2024")),
    ("draft-hardt-httpbis-signature-key-09.txt",
     "https://www.ietf.org/archive/id/draft-hardt-httpbis-signature-key-09.txt",
     (b"draft-hardt-httpbis-signature-key-09", b"HTTP Signature Keys", b"13 September 2026")),
)
ALLOWED_HOSTS = {"www.rfc-editor.org", "www.ietf.org"}


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
    with open(tmp, "wb") as handle:
        handle.write((json.dumps(record, indent=2, sort_keys=True) + "\n").encode())
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    os.chmod(path, 0o600)


def retrieve(filename, url, markers):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS or parsed.port:
        raise RuntimeError("document URL violates fixed HTTPS host policy")
    path = parsed.path + (("?" + parsed.query) if parsed.query else "")
    started = time.monotonic()
    item = {"filename": filename, "url": url, "started_at": utc_now(),
            "final_host": parsed.hostname,
            "final_host_basis": "requested host; redirects prohibited",
            "maximum_bytes": MAX_BYTES, "required_markers":
            [marker.decode("ascii") for marker in markers],
            "redirect_count": 0, "redirect_chain": []}
    connection = http.client.HTTPSConnection(parsed.hostname, 443,
                                              timeout=CONNECT_TIMEOUT,
                                              context=ssl.create_default_context())
    partial = ROOT / (filename + ".partial")
    try:
        connection.request("GET", path, headers={"Accept": "text/plain",
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
        if declared is not None and int(declared) > MAX_BYTES:
            raise RuntimeError("declared content length exceeded cap")
        digest = hashlib.sha256()
        received = 0
        with open(partial, "xb") as handle:
            os.chmod(partial, 0o600)
            while True:
                remaining = TOTAL_TIMEOUT - (time.monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError("total document timeout")
                sock.settimeout(min(remaining, CONNECT_TIMEOUT))
                block = response.read(CHUNK)
                if not block:
                    break
                received += len(block)
                if received > MAX_BYTES:
                    raise RuntimeError("response body exceeded cap")
                digest.update(block)
                handle.write(block)
            handle.flush()
            os.fsync(handle.fileno())
        data = partial.read_bytes()
        missing = [marker.decode("ascii") for marker in markers if marker not in data]
        item.update(received_size=received, observed_sha256=digest.hexdigest(),
                    missing_markers=missing, finished_at=utc_now())
        if missing:
            quarantine = ROOT / (filename + ".UNVERIFIED")
            os.replace(partial, quarantine)
            os.chmod(quarantine, 0o400)
            item.update(final_path=str(quarantine), final_mode=mode(quarantine))
            raise RuntimeError("document identity mismatch; complete response quarantined")
        final = ROOT / filename
        os.replace(partial, final)
        os.chmod(final, 0o400)
        item.update(result="VERIFIED_IDENTITY", final_path=str(final),
                    final_mode=mode(final))
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
        for entry in DOCUMENTS:
            record["items"].append(retrieve(*entry))
        if sorted(p.name for p in ROOT.iterdir()) != sorted(
                [entry[0] for entry in DOCUMENTS]):
            raise RuntimeError("unexpected file inventory before evidence write")
        record.update(result="VERIFIED_IDENTITY", finished_at=utc_now())
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
