#!/usr/bin/env python3
"""Unexecuted fail-closed synthetic preflight for M02 Stage 3A-R4."""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import time


IMAGE = "docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb"
IMAGE_ID = "sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb"
NETWORK = "soga-m02-r4-internal"
SERVER = "soga-m02-r4-server"
CLIENT = "soga-m02-r4-client"
LABEL = "org.debblabs.soga.task=M02-stage3ar4"
SERVER_PORT = 46321
INHERITED_PORTS = (46321, 46322)
COMMAND_TIMEOUT_SECONDS = 20.0
READINESS_TIMEOUT_SECONDS = 10.0
READINESS_RETRY_SECONDS = 0.2
MAX_DISCOVERED_ALIASES = 16
FIXED_HOST_ALIASES = (
    "host.docker.internal",
    "gateway.docker.internal",
    "docker.for.mac.host.internal",
    "docker.for.mac.localhost",
    "vm.docker.internal",
    "kubernetes.docker.internal",
)


SERVER_JS = r"""
const http = require('node:http');
const server = http.createServer((req, res) => {
  if (req.url !== '/nonce') { res.writeHead(404); res.end(); return; }
  res.writeHead(200, {'content-type': 'text/plain'});
  res.end('SOGA-M02-R4-NONCE');
});
server.on('error', error => {
  console.error(`SERVER_ERROR ${error.code || error.name || 'unknown'}`);
  process.exitCode = 1;
});
server.listen(46321, '0.0.0.0', () => console.log('LISTENING_OK'));
""".strip()


CLIENT_JS = r"""
console.log('CLIENT_READY');
setInterval(() => {}, 1000);
""".strip()


HTTP_PROBE_JS = r"""
const http = require('node:http');
const host = process.env.SOGA_R4_SERVER_NAME;
let body = '';
const request = http.get({host, port: 46321, path: '/nonce', timeout: 1000}, response => {
  response.setEncoding('utf8');
  response.on('data', chunk => {
    if (body.length < 128) body += chunk.slice(0, 128 - body.length);
  });
  response.on('end', () => {
    const pass = response.statusCode === 200 && body.includes('SOGA-M02-R4-NONCE');
    console.log(JSON.stringify({category: pass ? 'nonce_match' : 'response_without_nonce', pass}));
    process.exitCode = pass ? 0 : 1;
  });
});
request.on('timeout', () => request.destroy(Object.assign(new Error('timeout'), {code: 'TIMEOUT'})));
request.on('error', error => {
  console.log(JSON.stringify({category: error.code || error.name || 'error', pass: false}));
  process.exitCode = 1;
});
""".strip()


IPV6_PROBE_JS = r"""
const fs = require('node:fs');
function main() {
  let nonLoopbackAddress = false;
  let defaultRoute = false;
  try {
    const addresses = fs.readFileSync('/proc/net/if_inet6', 'utf8').trim().split(/\n+/).filter(Boolean);
    nonLoopbackAddress = addresses.some(line => line.trim().split(/\s+/).at(-1) !== 'lo');
  } catch (error) {
    const absent = error.code === 'ENOENT';
    console.log(JSON.stringify({category: absent ? 'ipv6_stack_absent' : 'address_inspection_failed', pass: absent}));
    process.exitCode = absent ? 0 : 1;
    return;
  }
  try {
    const routes = fs.readFileSync('/proc/net/ipv6_route', 'utf8').trim().split(/\n+/).filter(Boolean);
    defaultRoute = routes.some(line => {
      const fields = line.trim().split(/\s+/);
      return fields.length >= 10 && fields[0] === '00000000000000000000000000000000' && fields[1] === '00';
    });
  } catch (error) {
    const absent = error.code === 'ENOENT';
    console.log(JSON.stringify({category: absent ? 'ipv6_route_stack_absent' : 'route_inspection_failed', pass: absent}));
    process.exitCode = absent ? 0 : 1;
    return;
  }
  const pass = !nonLoopbackAddress && !defaultRoute;
  console.log(JSON.stringify({category: pass ? 'ipv6_unassigned_unrouted' : 'ipv6_present', pass}));
  process.exitCode = pass ? 0 : 1;
}
main();
""".strip()


ALIAS_DISCOVERY_JS = r"""
const fs = require('node:fs');
const names = new Set();
for (const path of ['/etc/hosts', '/etc/resolv.conf']) {
  try {
    const text = fs.readFileSync(path, 'utf8');
    for (const token of text.split(/\s+/)) {
      const value = token.toLowerCase().replace(/[^a-z0-9.*_-]/g, '');
      if (value.endsWith('.docker.internal') || value.startsWith('docker.for.mac.')) names.add(value);
    }
  } catch (_) {}
}
console.log(JSON.stringify({aliases: [...names].sort()}));
""".strip()


PATH_PROBE_JS = r"""
const dns = require('node:dns').promises;
const net = require('node:net');
const spec = JSON.parse(process.env.SOGA_R4_PROBE_SPEC);
const locallyDenied = new Set(['ENETUNREACH', 'EHOSTUNREACH', 'EPERM', 'EACCES']);
async function connect(host, port) {
  return await new Promise(resolve => {
    const socket = net.createConnection({host, port});
    let done = false;
    const finish = value => {
      if (done) return;
      done = true;
      socket.destroy();
      resolve(value);
    };
    socket.setTimeout(1000, () => finish({category: 'timeout'}));
    socket.on('connect', () => finish({category: 'connected'}));
    socket.on('error', error => finish({category: error.code || error.name || 'error'}));
  });
}
(async () => {
  let resolved = null;
  if (spec.kind === 'alias') {
    try {
      const found = await dns.lookup(spec.target, {all: true});
      resolved = found.length > 0;
    } catch (error) {
      const category = error.code || error.name || 'resolution_error';
      const pass = category === 'ENOTFOUND' || category === 'EAI_AGAIN';
      console.log(JSON.stringify({category, pass, resolution: 'not_resolved'}));
      process.exitCode = pass ? 0 : 1;
      return;
    }
  }
  const outcome = await connect(spec.target, spec.port);
  const pass = locallyDenied.has(outcome.category);
  console.log(JSON.stringify({
    category: outcome.category,
    pass,
    resolution: resolved === null ? 'not_applicable' : 'resolved'
  }));
  process.exitCode = pass ? 0 : 1;
})().catch(error => {
  console.log(JSON.stringify({category: error.code || error.name || 'probe_runtime', pass: false}));
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


def docker_ids(resource: str, name: str) -> str:
    if resource == "container":
        args = ["docker", "ps", "-a", "--filter", f"name=^{name}$", "--format", "{{.ID}}"]
    elif resource == "network":
        args = ["docker", "network", "ls", "--filter", f"name=^{name}$", "--format", "{{.ID}}"]
    else:
        raise ValueError("unsupported resource")
    return command(args).stdout.strip()


def assert_ports_free() -> None:
    for port in INHERITED_PORTS:
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", port))


def assert_preconditions() -> None:
    collisions: list[str] = []
    for name in (SERVER, CLIENT):
        if docker_ids("container", name):
            collisions.append(f"container:{name}")
    if docker_ids("network", NETWORK):
        collisions.append(f"network:{NETWORK}")
    try:
        assert_ports_free()
    except OSError:
        collisions.append("inherited_host_port")
    if collisions:
        raise RuntimeError("precondition collision: " + ",".join(collisions))
    emit("preconditions", "PASS")


def inspect_image() -> None:
    observed = command(
        ["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}|{{.Os}}|{{.Architecture}}"]
    ).stdout.strip()
    expected = f"{IMAGE_ID}|linux|arm64"
    if observed != expected:
        raise RuntimeError("cached image identity or platform mismatch")
    emit("cached_image", "PASS", platform="linux/arm64", runtime="node-v24.20.0-required")


def inspect_network(*, expected_members: set[str]) -> str:
    raw = command(["docker", "network", "inspect", NETWORK]).stdout
    try:
        records = json.loads(raw)
        record = records[0]
        internal = record["Internal"] is True
        attachable = record["Attachable"] is False
        ipv6_setting = record.get("EnableIPv6")
        gateway = str(record["IPAM"]["Config"][0]["Gateway"])
        members = {
            str(value.get("Name"))
            for value in (record.get("Containers") or {}).values()
            if value.get("Name")
        }
    except (IndexError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise RuntimeError("network inspection could not be normalized") from error
    if (
        not internal
        or not attachable
        or ipv6_setting is not False
        or members != expected_members
        or not gateway
    ):
        raise RuntimeError("network configuration or membership mismatch")
    emit(
        "internal_ipv4_network",
        "PASS",
        attachable=False,
        expected_member_count=len(expected_members),
        internal=True,
        ipv6_enabled=False,
    )
    return gateway


def inspect_container(name: str) -> None:
    raw = command(["docker", "inspect", name]).stdout
    try:
        record = json.loads(raw)[0]
        host_config = record["HostConfig"]
        networks = record["NetworkSettings"]["Networks"]
        endpoint = networks[NETWORK]
        state = record["State"]
        port_bindings = host_config.get("PortBindings")
        network_mode = host_config.get("NetworkMode")
        ipv6_address = endpoint.get("GlobalIPv6Address") or endpoint.get("IPv6Address") or ""
        ipv6_gateway = endpoint.get("IPv6Gateway") or ""
    except (IndexError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"container inspection could not be normalized: {name}") from error
    if set(networks) != {NETWORK} or network_mode != NETWORK:
        raise RuntimeError(f"unexpected network attachment or mode: {name}")
    if port_bindings not in (None, {}):
        raise RuntimeError(f"unexpected host port binding: {name}")
    if ipv6_address or ipv6_gateway:
        raise RuntimeError(f"unexpected IPv6 assignment: {name}")
    if not state.get("Running"):
        raise RuntimeError(f"container not running: {name}")
    emit("container_isolation", "PASS", container_role="server" if name == SERVER else "client")


def container_diagnostic(name: str) -> None:
    state_result = command(
        ["docker", "inspect", name, "--format", "{{json .State}}"],
        check=False,
        timeout=5.0,
    )
    logs_result = command(
        ["docker", "logs", "--tail", "20", name],
        check=False,
        timeout=5.0,
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
    bounded_logs = (logs_result.stdout + logs_result.stderr).strip()[-2000:]
    emit(
        "container_diagnostic",
        "OBSERVED",
        container_role="server" if name == SERVER else "client",
        logs=bounded_logs,
        logs_status=logs_result.returncode,
        state=state,
        state_status=state_result.returncode,
    )


def exec_json(name: str, script: str, *, environment: dict[str, str] | None = None) -> dict[str, object]:
    args = ["docker", "exec"]
    for key, value in sorted((environment or {}).items()):
        args.extend(["-e", f"{key}={value}"])
    args.extend([name, "node", "-e", script])
    result = command(args, check=False, timeout=5.0)
    stdout = result.stdout.strip()
    if len(stdout) > 2000:
        raise RuntimeError("probe output exceeded bound")
    if not stdout:
        category = "probe_no_output" if not result.stderr.strip() else "probe_stderr_only"
        return {"category": category, "pass": False, "exit_status": result.returncode}
    try:
        record = json.loads(stdout.splitlines()[-1])
    except json.JSONDecodeError:
        return {"category": "invalid_probe_record", "pass": False, "exit_status": result.returncode}
    return {
        "category": str(record.get("category", "missing_category"))[:200],
        "pass": bool(record.get("pass")) and result.returncode == 0,
        "resolution": str(record.get("resolution", "not_reported"))[:50],
        "exit_status": result.returncode,
    }


def wait_for_server() -> None:
    started = time.monotonic()
    deadline = started + READINESS_TIMEOUT_SECONDS
    attempt = 0
    while time.monotonic() < deadline:
        attempt += 1
        try:
            record = exec_json(
                SERVER,
                HTTP_PROBE_JS,
                environment={"SOGA_R4_SERVER_NAME": "127.0.0.1"},
            )
        except RuntimeError:
            record = {"category": "probe_command_failure", "pass": False}
        emit(
            "server_readiness_attempt",
            "PASS" if record["pass"] else "WAIT",
            attempt=attempt,
            category=record["category"],
            elapsed_ms=round((time.monotonic() - started) * 1000),
        )
        if record["pass"]:
            return
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(READINESS_RETRY_SECONDS, remaining))
    raise RuntimeError("synthetic server did not become ready")


def verify_intercontainer_nonce() -> None:
    record = exec_json(
        CLIENT,
        HTTP_PROBE_JS,
        environment={"SOGA_R4_SERVER_NAME": SERVER},
    )
    emit(
        "intercontainer_nonce",
        "PASS" if record["pass"] else "FAIL",
        category=record["category"],
        client_role="independent_network_peer",
    )
    if not record["pass"]:
        raise RuntimeError("inter-container nonce exchange failed")


def verify_ipv6_absent(name: str) -> None:
    record = exec_json(name, IPV6_PROBE_JS)
    emit(
        "container_ipv6",
        "PASS" if record["pass"] else "FAIL",
        category=record["category"],
        container_role="server" if name == SERVER else "client",
    )
    if not record["pass"]:
        raise RuntimeError(f"IPv6 assignment or route not conclusively excluded: {name}")


def discover_aliases(name: str) -> set[str]:
    result = command(["docker", "exec", name, "node", "-e", ALIAS_DISCOVERY_JS], check=False, timeout=5.0)
    if result.returncode != 0 or len(result.stdout) > 2000:
        raise RuntimeError(f"host-alias discovery failed: {name}")
    try:
        record = json.loads(result.stdout.splitlines()[-1])
        discovered = {str(value).lower() for value in record.get("aliases", [])}
    except (IndexError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"host-alias discovery could not be normalized: {name}") from error
    if any(not (value.endswith(".docker.internal") or value.startswith("docker.for.mac.")) for value in discovered):
        raise RuntimeError("host-alias discovery returned an out-of-class value")
    if len(discovered) > MAX_DISCOVERED_ALIASES:
        raise RuntimeError("host-alias discovery exceeded count bound")
    emit(
        "host_alias_discovery",
        "PASS",
        container_role="server" if name == SERVER else "client",
        discovered_count=len(discovered),
    )
    return discovered


def path_probe(
    name: str,
    *,
    control: str,
    kind: str,
    target: str,
    port: int,
    target_index: int | None = None,
) -> None:
    specification = json.dumps({"kind": kind, "target": target, "port": port}, separators=(",", ":"))
    record = exec_json(
        name,
        PATH_PROBE_JS,
        environment={"SOGA_R4_PROBE_SPEC": specification},
    )
    role = "server" if name == SERVER else "client"
    emit(
        control,
        "PASS" if record["pass"] else "FAIL",
        category=record["category"],
        container_role=role,
        resolution=record["resolution"],
        target_index=target_index,
    )
    if not record["pass"]:
        raise RuntimeError(f"disqualifying or ambiguous reachability: {control}:{role}")


def verify_paths(gateway: str) -> None:
    for name in (SERVER, CLIENT):
        for index, target in enumerate(("192.0.2.1", "198.51.100.1"), start=1):
            path_probe(
                name,
                control=f"test_net_{index}",
                kind="address",
                target=target,
                port=SERVER_PORT,
            )
        path_probe(
            name,
            control="internal_gateway",
            kind="address",
            target=gateway,
            port=46323,
        )
        aliases = set(FIXED_HOST_ALIASES) | discover_aliases(name)
        for alias_index, alias in enumerate(sorted(aliases), start=1):
            path_probe(
                name,
                control="docker_host_alias",
                kind="alias",
                target=alias,
                port=46323,
                target_index=alias_index,
            )
    emit(
        "dns_forwarding",
        "UNCHARACTERIZED",
        claim="no_absence_of_dns_egress_claim",
        public_hostname_queried=False,
    )


def start_container(name: str, role: str, script: str) -> None:
    command(
        [
            "docker",
            "run",
            "-d",
            "--pull=never",
            "--platform",
            "linux/arm64",
            "--name",
            name,
            "--network",
            NETWORK,
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev,size=4m",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges:true",
            "--memory",
            "128m",
            "--cpus",
            "0.5",
            "--pids-limit",
            "48",
            "--user",
            "65534:65534",
            "--label",
            LABEL,
            "--label",
            f"org.debblabs.soga.role={role}",
            IMAGE,
            "node",
            "-e",
            script,
        ]
    )


def verify_absence() -> list[str]:
    errors: list[str] = []
    for name in (SERVER, CLIENT):
        try:
            if docker_ids("container", name):
                errors.append(f"container remains:{name}")
        except Exception as error:
            errors.append(f"container absence check failed:{name}:{error}")
    try:
        if docker_ids("network", NETWORK):
            errors.append("network remains")
    except Exception as error:
        errors.append(f"network absence check failed:{error}")
    try:
        assert_ports_free()
    except Exception:
        errors.append("inherited host port unavailable")
    return errors


def run_preflight() -> bool:
    passed = False
    preconditions_passed = False
    created_network = False
    created_server = False
    created_client = False
    cleanup_errors: list[str] = []
    try:
        assert_preconditions()
        preconditions_passed = True
        inspect_image()

        command(
            [
                "docker",
                "network",
                "create",
                "--internal",
                "--driver",
                "bridge",
                "--label",
                LABEL,
                NETWORK,
            ]
        )
        created_network = True
        gateway = inspect_network(expected_members=set())

        start_container(SERVER, "server", SERVER_JS)
        created_server = True
        start_container(CLIENT, "client", CLIENT_JS)
        created_client = True

        gateway = inspect_network(expected_members={SERVER, CLIENT})
        for name in (SERVER, CLIENT):
            inspect_container(name)
            verify_ipv6_absent(name)

        wait_for_server()
        verify_intercontainer_nonce()
        assert_ports_free()
        emit("no_host_publication", "PASS", inherited_ports_checked=list(INHERITED_PORTS))
        verify_paths(gateway)

        passed = True
        emit("containment_preflight", "PASS", scope="internal_ipv4_application_paths")
    except Exception as error:
        emit(
            "precondition" if not preconditions_passed else "containment_preflight",
            "FAIL",
            error=str(error)[:1000],
        )
        if preconditions_passed:
            for created, name in ((created_server, SERVER), (created_client, CLIENT)):
                if not created:
                    continue
                try:
                    container_diagnostic(name)
                except Exception as diagnostic_error:
                    emit(
                        "container_diagnostic",
                        "FAIL",
                        container_role="server" if name == SERVER else "client",
                        error=str(diagnostic_error)[:500],
                    )
    finally:
        for created, name in ((created_client, CLIENT), (created_server, SERVER)):
            if not created:
                continue
            try:
                removal = command(["docker", "rm", "-f", name], check=False)
                if removal.returncode != 0:
                    cleanup_errors.append(f"container removal returned nonzero:{name}")
            except Exception as error:
                cleanup_errors.append(f"container removal failed:{name}:{error}")
        if created_network:
            try:
                removal = command(["docker", "network", "rm", NETWORK], check=False)
                if removal.returncode != 0:
                    cleanup_errors.append("network removal returned nonzero")
            except Exception as error:
                cleanup_errors.append(f"network removal failed:{error}")
        if preconditions_passed:
            cleanup_errors.extend(verify_absence())
            if cleanup_errors:
                emit("cleanup", "FAIL", errors=[value[:500] for value in cleanup_errors])
            else:
                emit("cleanup", "PASS")
        else:
            emit("cleanup", "NOT_APPLICABLE", reason="precondition_failed_before_creation")
    return passed and preconditions_passed and not cleanup_errors


if __name__ == "__main__":
    sys.exit(0 if run_preflight() else 1)
