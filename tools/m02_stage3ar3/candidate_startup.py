#!/usr/bin/env python3
"""Conditional exact-candidate reachability check for M02 Stage 3A-R3."""

from __future__ import annotations

import json
import pathlib
import socket
import subprocess
import sys
import time
import urllib.request

from preflight import IMAGE, NETWORK, run_preflight

WAS = pathlib.Path("/private/tmp/m02-stage3a-20260908/was-teaching-server")
FREEWALLET = pathlib.Path("/private/tmp/m02-stage3a-20260908/freewallet")
WAS_CONTAINER = "soga-m02-r3-was"
FREEWALLET_CONTAINER = "soga-m02-r3-freewallet"

STATIC_JS = r"""
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = '/workspace/dist';
const types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json'};
http.createServer((req, res) => {
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, 'http://127.0.0.1').pathname); }
  catch { res.writeHead(400); res.end(); return; }
  const relative = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const target = path.resolve(root, relative);
  if (target !== root && !target.startsWith(root + path.sep)) { res.writeHead(403); res.end(); return; }
  fs.stat(target, (error, stat) => {
    if (error || !stat.isFile()) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, {'content-type': types[path.extname(target)] || 'application/octet-stream'});
    fs.createReadStream(target).pipe(res);
  });
}).listen(46322, '0.0.0.0');
""".strip()


def emit(control: str, result: str, **details: object) -> None:
    print(json.dumps({"control": control, "result": result, **details}, sort_keys=True), flush=True)


def command(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=check)


def get(url: str) -> tuple[int, str]:
    with urllib.request.urlopen(url, timeout=2.0) as response:
        response.read(1)
        return response.status, response.headers.get_content_type()


def wait_get(url: str) -> tuple[int, str]:
    for _ in range(30):
        try:
            return get(url)
        except Exception:
            time.sleep(0.1)
    raise RuntimeError(f"endpoint did not become ready: {url}")


def container_diagnostic(name: str) -> dict[str, object]:
    state = command(["docker", "inspect", name, "--format", "{{json .State}}"], check=False)
    logs = command(["docker", "logs", "--tail", "20", name], check=False)
    return {
        "state": state.stdout.strip()[:2000],
        "logs": (logs.stdout + logs.stderr).strip()[:2000],
    }


def verify_sources() -> None:
    expected = {
        WAS: "2090a606f2723e4d57ef0090db55fd1bdab9427e",
        FREEWALLET: "8e806c049b1134e36e72ab243ea3fbeb93153c37",
    }
    for root, revision in expected.items():
        if command(["git", "-C", str(root), "rev-parse", "HEAD"]).stdout.strip() != revision:
            raise RuntimeError(f"source revision mismatch: {root}")
        if command(["git", "-C", str(root), "status", "--short", "--untracked-files=no"]).stdout.strip():
            raise RuntimeError(f"tracked source is dirty: {root}")
    build_info = json.loads((WAS / "dist/build-info.json").read_text())
    if build_info.get("version") != "0.27.0" or not str(build_info.get("commit", "")).startswith("2090a606f2723e4d57ef0090db55fd1bdab9427e"):
        raise RuntimeError(f"unexpected WAS build stamp: {build_info}")
    if not (FREEWALLET / "dist/index.html").is_file():
        raise RuntimeError("Freewallet build output missing")


def run_candidates() -> bool:
    passed = False
    cleanup_ok = True
    created_network = False
    created_was = False
    created_freewallet = False
    try:
        if not run_preflight():
            raise RuntimeError("fresh containment preflight did not pass")
        verify_sources()
        command(["docker", "network", "create", "--internal", "--driver", "bridge", "--label", "org.debblabs.soga.task=M02-stage3ar3", NETWORK])
        created_network = True

        common = [
            "--rm", "--pull=never", "--platform", "linux/arm64", "--network", NETWORK,
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges:true",
            "--memory", "256m", "--cpus", "0.75", "--pids-limit", "64", "--user", "65534:65534",
        ]
        command([
            "docker", "run", "-d", *common, "--name", WAS_CONTAINER,
            "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=8m,uid=65534,gid=65534",
            "--tmpfs", "/workspace/data:rw,noexec,nosuid,nodev,size=16m,uid=65534,gid=65534",
            "--mount", f"type=bind,src={WAS},dst=/workspace,readonly",
            "-w", "/workspace", "-p", "127.0.0.1:46321:46321/tcp",
            "-e", "SERVER_URL=http://127.0.0.1:46321", "-e", "PORT=46321",
            "-e", "STORAGE_LIMIT_PER_SPACE=1048576", "-e", "MAX_UPLOAD_BYTES=262144",
            "-e", "MAX_SPACES_PER_CONTROLLER=2", "-e", "MAX_COLLECTIONS_PER_SPACE=4",
            "-e", "MAX_RESOURCES_PER_SPACE=16", IMAGE, "node", "dist/start.js",
        ])
        created_was = True
        command([
            "docker", "run", "-d", *common, "--name", FREEWALLET_CONTAINER,
            "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=4m,uid=65534,gid=65534",
            "--mount", f"type=bind,src={FREEWALLET},dst=/workspace,readonly",
            "-w", "/workspace", "-p", "127.0.0.1:46322:46322/tcp",
            IMAGE, "node", "-e", STATIC_JS,
        ])
        created_freewallet = True

        was_health = wait_get("http://127.0.0.1:46321/health")
        was_root = get("http://127.0.0.1:46321/")
        wallet_root = wait_get("http://127.0.0.1:46322/")
        holdpoint_started = time.monotonic()
        wallet_asset = next((path for path in sorted((FREEWALLET / "dist/assets").iterdir()) if path.is_file()), None)
        if wallet_asset is None:
            raise RuntimeError("no Freewallet built asset found")
        asset_result = get(f"http://127.0.0.1:46322/assets/{wallet_asset.name}")
        if time.monotonic() - holdpoint_started > 30:
            raise RuntimeError("candidate holdpoint exceeded 30 seconds")
        emit("candidate_reachability", "PASS", was_health=was_health, was_root=was_root, wallet_root=wallet_root, wallet_asset=asset_result)
        passed = True
    except Exception as error:
        diagnostics = {}
        if created_was:
            diagnostics[WAS_CONTAINER] = container_diagnostic(WAS_CONTAINER)
        if created_freewallet:
            diagnostics[FREEWALLET_CONTAINER] = container_diagnostic(FREEWALLET_CONTAINER)
        emit("candidate_reachability", "FAIL", error=str(error), diagnostics=diagnostics)
    finally:
        if created_was:
            command(["docker", "rm", "-f", WAS_CONTAINER], check=False)
        if created_freewallet:
            command(["docker", "rm", "-f", FREEWALLET_CONTAINER], check=False)
        if created_network:
            command(["docker", "network", "rm", NETWORK], check=False)
        containers = command(["docker", "ps", "-a", "--filter", "name=soga-m02-r3", "--format", "{{.ID}}"]).stdout.strip()
        networks = command(["docker", "network", "ls", "--filter", "name=soga-m02-r3", "--format", "{{.ID}}"]).stdout.strip()
        ports_free = True
        for port in (46321, 46322):
            try:
                with socket.socket() as probe:
                    probe.bind(("127.0.0.1", port))
            except OSError:
                ports_free = False
        cleanup_ok = not containers and not networks and ports_free
        emit("cleanup", "PASS" if cleanup_ok else "FAIL",
             containers=containers, networks=networks, ports_free=ports_free)
    return passed and cleanup_ok


if __name__ == "__main__":
    sys.exit(0 if run_candidates() else 1)
