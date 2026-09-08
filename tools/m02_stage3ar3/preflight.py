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

SERVER_JS = r"""
const http = require('node:http');
const server = http.createServer((req, res) => {
  if (req.url !== '/nonce') { res.writeHead(404); res.end(); return; }
  res.writeHead(200, {'content-type': 'text/plain'});
  res.end('SOGA-M02-R3-NONCE');
});
server.listen(46321, '0.0.0.0');
""".strip()

PROBE_JS = r"""
const dns = require('node:dns').promises;
const net = require('node:net');
const gateway = process.argv[1];
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
""".strip()


def emit(control: str, result: str, **details: object) -> None:
    print(json.dumps({"control": control, "result": result, **details}, sort_keys=True), flush=True)


def command(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=check)


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


def fetch_nonce(host: str) -> bool:
    with socket.create_connection((host, PORT), timeout=1.0) as connection:
        connection.sendall(b"GET /nonce HTTP/1.0\r\nHost: localhost\r\n\r\n")
        received = b""
        while True:
            chunk = connection.recv(4096)
            if not chunk:
                break
            received += chunk
        return b"SOGA-M02-R3-NONCE" in received


def wait_for_nonce() -> None:
    for _ in range(30):
        try:
            if fetch_nonce("127.0.0.1"):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("loopback nonce endpoint did not become ready")


def run_preflight() -> bool:
    passed = False
    cleanup_ok = True
    created_network = False
    created_container = False
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
            "docker", "run", "-d", "--rm", "--pull=never", "--platform", "linux/arm64",
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

        addresses = host_addresses()
        if not addresses:
            raise RuntimeError("no active non-loopback IPv4 address available for negative control")
        for address in addresses:
            try:
                reachable = fetch_nonce(address)
            except OSError as error:
                emit("non_loopback_host", "PASS", address=address, error=type(error).__name__)
            else:
                raise RuntimeError(f"published endpoint reachable through {address}: {reachable}")

        probe = command(["docker", "exec", CONTAINER, "node", "-e", PROBE_JS, gateway], check=False)
        for line in probe.stdout.splitlines():
            print(line, flush=True)
        if probe.returncode != 0:
            raise RuntimeError("container egress or host-gateway control failed")

        passed = True
        emit("containment_preflight", "PASS")
    except Exception as error:
        emit("containment_preflight", "FAIL", error=str(error))
    finally:
        if created_container:
            command(["docker", "rm", "-f", CONTAINER], check=False)
        if created_network:
            command(["docker", "network", "rm", NETWORK], check=False)
        try:
            assert_absent()
            emit("cleanup", "PASS")
        except Exception as error:
            emit("cleanup", "FAIL", error=str(error))
            cleanup_ok = False
    return passed and cleanup_ok


if __name__ == "__main__":
    sys.exit(0 if run_preflight() else 1)
