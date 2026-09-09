#!/usr/bin/env python3
"""Fail-closed Docker Desktop containment preflight for M02 Stage 3A-R3."""

from __future__ import annotations

import json
import re
import socket
import subprocess
import sys
import time

IMAGE = "docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb"
NETWORK = "soga-m02-r3-internal"
CONTAINER = "soga-m02-r3-preflight"
PORT = 46321
OTHER_PORT = 46323
COMMAND_TIMEOUT_SECONDS = 20.0
READINESS_TIMEOUT_SECONDS = 10.0
READINESS_RETRY_SECONDS = 0.2

SERVER_JS = r"""
const http = require('node:http');
const server = http.createServer((req, res) => {
  if (req.url !== '/nonce') { res.writeHead(404); res.end(); return; }
  res.writeHead(200, {'content-type': 'text/plain'});
  res.end('SOGA-M02-R3-NONCE');
});
server.on('error', error => {
  console.error(`SERVER_ERROR ${error.code || error.name || 'unknown'}`);
  process.exitCode = 1;
});
server.listen(46321, '0.0.0.0', () => console.log('LISTENING_OK'));
""".strip()

PROBE_JS = r"""
const dns = require('node:dns').promises;
const net = require('node:net');
const gateway = process.env.SOGA_SYNTHETIC_GATEWAY;
const targets = [
  ['test_net_1', '192.0.2.1', 46321, false],
  ['test_net_2', '198.51.100.1', 46321, false],
  ['gateway', gateway, 46323, true],
];
async function connect(host, port) {
  return await new Promise(resolve => {
    const s = net.createConnection({host, port});
    const done = value => { s.destroy(); resolve(value); };
    s.setTimeout(1000, () => done({status: 'timeout'}));
    s.on('connect', () => done({status: 'connected'}));
    s.on('error', e => done({status: 'error', code: e.code}));
  });
}
(async () => {
  let failed = false;
  for (const [name, host, port, isHostPath] of targets) {
    const result = await connect(host, port);
    const locallyDenied = ['ENETUNREACH', 'EHOSTUNREACH', 'EPERM', 'EACCES'].includes(result.code);
    const pass = locallyDenied;
    if (!pass) failed = true;
    console.log(JSON.stringify({control: name, host, port, result, pass,
      note: isHostPath ? 'ECONNREFUSED proves gateway reachability and therefore fails' : undefined}));
  }
  try {
    const found = await dns.lookup('host.docker.internal', {all: true});
    console.log(JSON.stringify({control: 'host_docker_internal_resolution', found, pass: false}));
    failed = true;
  } catch (e) {
    const pass = ['ENOTFOUND', 'EAI_AGAIN'].includes(e.code);
    console.log(JSON.stringify({control: 'host_docker_internal_resolution', error: e.code, pass}));
    if (!pass) failed = true;
  }
  process.exitCode = failed ? 1 : 0;
})().catch(error => {
  console.log(JSON.stringify({control: 'probe_runtime', error: error.code || error.name || 'unknown', pass: false}));
  process.exitCode = 1;
});
""".strip()

SELF_PROBE_JS = r"""
const http = require('node:http');
let body = '';
const request = http.get({host: '127.0.0.1', port: 46321, path: '/nonce', timeout: 1000}, response => {
  response.setEncoding('utf8');
  response.on('data', chunk => { if (body.length < 128) body += chunk.slice(0, 128 - body.length); });
  response.on('end', () => {
    const pass = response.statusCode === 200 && body.includes('SOGA-M02-R3-NONCE');
    console.log(JSON.stringify({control: 'self_readiness', category: pass ? 'nonce_match' : 'response_without_nonce', pass}));
    process.exitCode = pass ? 0 : 1;
  });
});
request.on('timeout', () => request.destroy(new Error('timeout')));
request.on('error', error => {
  console.log(JSON.stringify({control: 'self_readiness', category: error.message === 'timeout' ? 'timeout' : (error.code || error.name || 'error'), pass: false}));
  process.exitCode = 1;
});
""".strip()


def emit(control: str, result: str, **details: object) -> None:
    print(json.dumps({"control": control, "result": result, **details}, sort_keys=True), flush=True)


def command(
    args: list[str],
    *,
    check: bool = True,
    timeout: float = COMMAND_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            text=True,
            capture_output=True,
            check=check,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        operation = " ".join(args[:2])
        raise RuntimeError(f"command timeout: {operation}") from error


def assert_absent() -> None:
    containers = command(["docker", "ps", "-a", "--filter", f"name=^{CONTAINER}$", "--format", "{{.ID}}"]).stdout.strip()
    networks = command(["docker", "network", "ls", "--filter", f"name=^{NETWORK}$", "--format", "{{.ID}}"]).stdout.strip()
    if containers or networks:
        raise RuntimeError("fixed-name Docker resource already exists")
    for port in (46321, 46322):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", port))


def host_addresses() -> list[str]:
    output = command(["ifconfig"]).stdout
    addresses = sorted(set(re.findall(r"\binet (\d+\.\d+\.\d+\.\d+)\b", output)))
    return [address for address in addresses if not address.startswith("127.")]


def fetch_nonce(host: str, *, timeout: float = 1.0) -> bool:
    with socket.create_connection((host, PORT), timeout=timeout) as connection:
        connection.sendall(b"GET /nonce HTTP/1.0\r\nHost: localhost\r\n\r\n")
        received = b""
        while True:
            chunk = connection.recv(4096)
            if not chunk:
                break
            received += chunk
            if len(received) > 8192:
                return False
        return b"SOGA-M02-R3-NONCE" in received


def wait_for_nonce() -> None:
    started = time.monotonic()
    deadline = started + READINESS_TIMEOUT_SECONDS
    attempt = 0
    while time.monotonic() < deadline:
        attempt += 1
        remaining = max(0.001, deadline - time.monotonic())
        try:
            matched = fetch_nonce("127.0.0.1", timeout=min(1.0, remaining))
            if matched:
                emit(
                    "nonce_attempt",
                    "PASS",
                    attempt=attempt,
                    category="nonce_match",
                    elapsed_ms=round((time.monotonic() - started) * 1000),
                )
                return
            category = "response_without_nonce"
        except OSError as error:
            category = type(error).__name__
        emit(
            "nonce_attempt",
            "WAIT",
            attempt=attempt,
            category=category,
            elapsed_ms=round((time.monotonic() - started) * 1000),
        )
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(READINESS_RETRY_SECONDS, remaining))
    raise RuntimeError("loopback nonce endpoint did not become ready")


def container_diagnostic() -> dict[str, object]:
    state_result = command(
        ["docker", "inspect", CONTAINER, "--format", "{{json .State}}"],
        check=False,
    )
    binding_result = command(
        ["docker", "inspect", CONTAINER, "--format", "{{json .HostConfig.PortBindings}}"],
        check=False,
    )
    logs_result = command(
        ["docker", "logs", "--tail", "20", CONTAINER],
        check=False,
    )
    state: object = None
    if state_result.returncode == 0 and state_result.stdout.strip():
        try:
            full_state = json.loads(state_result.stdout)
            state = {
                "running": bool(full_state.get("Running")),
                "exit_code": full_state.get("ExitCode"),
                "oom_killed": bool(full_state.get("OOMKilled")),
                "error": str(full_state.get("Error", ""))[:500],
            }
        except json.JSONDecodeError:
            state = {"parse_error": True}
    diagnostic: dict[str, object] = {
        "state": state,
        "state_status": state_result.returncode,
        "binding": binding_result.stdout.strip()[:2000],
        "binding_status": binding_result.returncode,
        "logs": (logs_result.stdout + logs_result.stderr).strip()[-2000:],
        "logs_status": logs_result.returncode,
    }
    emit("container_diagnostic", "OBSERVED", **diagnostic)
    return diagnostic


def self_readiness() -> bool:
    probe = command(
        ["docker", "exec", CONTAINER, "node", "-e", SELF_PROBE_JS],
        check=False,
        timeout=5.0,
    )
    category = "exec_failed"
    detail = ""
    if probe.stdout.strip():
        try:
            record = json.loads(probe.stdout.splitlines()[-1])
            category = str(record.get("category", "invalid_probe_record"))[:200]
        except json.JSONDecodeError:
            category = "invalid_probe_record"
            detail = probe.stdout.strip()[-500:]
    elif probe.stderr.strip():
        detail = probe.stderr.strip()[-500:]
    emit(
        "container_self_readiness",
        "PASS" if probe.returncode == 0 else "FAIL",
        category=category,
        detail=detail,
        exit_status=probe.returncode,
    )
    return probe.returncode == 0


def run_preflight() -> bool:
    passed = False
    cleanup_ok = True
    created_network = False
    created_container = False
    diagnostics_captured = False
    try:
        assert_absent()
        image = command(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}|{{.Os}}|{{.Architecture}}"]).stdout.strip()
        expected = "sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb|linux|arm64"
        if image != expected:
            raise RuntimeError(f"image mismatch: {image}")

        command(["docker", "network", "create", "--internal", "--driver", "bridge", "--label", "org.debblabs.soga.task=M02-stage3ar3", NETWORK])
        created_network = True
        inspected = command(["docker", "network", "inspect", NETWORK, "--format", "{{json .Internal}}|{{json .Attachable}}|{{(index .IPAM.Config 0).Gateway}}"]).stdout.strip()
        internal, attachable, gateway = inspected.split("|", 2)
        if internal != "true" or attachable != "false" or not gateway:
            raise RuntimeError(f"network mismatch: {inspected}")
        emit("internal_network", "PASS", gateway=gateway)

        command([
            "docker", "run", "-d", "--pull=never", "--platform", "linux/arm64",
            "--name", CONTAINER, "--network", NETWORK, "--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=4m",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges:true", "--memory", "128m", "--cpus", "0.5",
            "--pids-limit", "32", "--user", "65534:65534", "-p", f"127.0.0.1:{PORT}:{PORT}/tcp",
            IMAGE, "node", "-e", SERVER_JS,
        ])
        created_container = True
        wait_for_nonce()
        emit("literal_loopback_nonce", "PASS")

        binding = command(["docker", "inspect", CONTAINER, "--format", "{{json (index .HostConfig.PortBindings \"46321/tcp\")}}"]).stdout.strip()
        if json.loads(binding) != [{"HostIp": "127.0.0.1", "HostPort": "46321"}]:
            raise RuntimeError(f"unexpected host binding: {binding}")
        emit("host_port_binding", "PASS", binding=json.loads(binding))

        container_diagnostic()
        diagnostics_captured = True
        if not self_readiness():
            raise RuntimeError("container self-readiness probe failed")

        addresses = host_addresses()
        if not addresses:
            raise RuntimeError("no active non-loopback IPv4 address available for negative control")
        for address_index, address in enumerate(addresses, start=1):
            try:
                reachable = fetch_nonce(address)
            except OSError as error:
                emit(
                    "non_loopback_host",
                    "PASS",
                    address_index=address_index,
                    error=type(error).__name__,
                )
            else:
                raise RuntimeError(
                    "published endpoint reachable through a non-loopback host address: "
                    f"index={address_index}, nonce_match={reachable}"
                )

        probe = command(
            [
                "docker", "exec", "-e", f"SOGA_SYNTHETIC_GATEWAY={gateway}",
                CONTAINER, "node", "-e", PROBE_JS,
            ],
            check=False,
        )
        for line in probe.stdout[:2000].splitlines():
            print(line, flush=True)
        if probe.returncode != 0:
            raise RuntimeError("container egress or host-gateway control failed")

        passed = True
        emit("containment_preflight", "PASS")
    except Exception as error:
        emit("containment_preflight", "FAIL", error=str(error))
        if created_container and not diagnostics_captured:
            try:
                container_diagnostic()
                diagnostics_captured = True
                state = command(
                    ["docker", "inspect", CONTAINER, "--format", "{{json .State.Running}}"],
                    check=False,
                )
                if state.returncode == 0 and state.stdout.strip() == "true":
                    self_readiness()
            except Exception as diagnostic_error:
                emit("container_diagnostic", "FAIL", error=str(diagnostic_error))
    finally:
        cleanup_errors: list[str] = []
        if created_container:
            try:
                removal = command(["docker", "rm", "-f", CONTAINER], check=False)
                if removal.returncode != 0:
                    cleanup_errors.append("container removal returned nonzero")
            except Exception as error:
                cleanup_errors.append(f"container removal failed: {error}")
        if created_network:
            try:
                removal = command(["docker", "network", "rm", NETWORK], check=False)
                if removal.returncode != 0:
                    cleanup_errors.append("network removal returned nonzero")
            except Exception as error:
                cleanup_errors.append(f"network removal failed: {error}")
        try:
            assert_absent()
        except Exception as error:
            cleanup_errors.append(f"absence verification failed: {error}")
        if cleanup_errors:
            emit("cleanup", "FAIL", errors=cleanup_errors)
            cleanup_ok = False
        else:
            emit("cleanup", "PASS")
    return passed and cleanup_ok


if __name__ == "__main__":
    sys.exit(0 if run_preflight() else 1)
