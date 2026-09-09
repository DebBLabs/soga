#!/usr/bin/env python3
"""Unexecuted bounded IPv6-state diagnosis authorized for creation by D-055."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from typing import Any


IMAGE = "docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb"
IMAGE_ID = "sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb"
NETWORK = "soga-m02-r4-ipv6-diagnosis-network"
CONTAINER = "soga-m02-r4-ipv6-diagnosis-container"
LABEL = "org.debblabs.soga.task=M02-stage3ar4-ipv6-diagnosis"
KNOWN_STOPPED_CONTAINER = "nifty_hawking"
COMMAND_TIMEOUT_SECONDS = 10.0
OPERATION_TIMEOUT_SECONDS = 20.0
CLEANUP_TIMEOUT_SECONDS = 2.0
TOTAL_TIMEOUT_SECONDS = 35.0
MAX_EXISTING_CONTAINERS = 128
MAX_EXISTING_NETWORKS = 128
MAX_INTERFACES = 16
MAX_OUTPUT_BYTES = 4096
HEX_ID = re.compile(r"^[0-9a-f]{12,64}$")
ACTIVE_DEADLINE: float | None = None


DIAGNOSIS_JS = rf"""
const fs = require('node:fs');
const MAX_INTERFACES = {MAX_INTERFACES};

function fail(category) {{
  console.log(JSON.stringify({{result: 'FAIL', category}}));
  process.exitCode = 1;
}}

function readOptional(path) {{
  try {{
    return {{status: 'present', text: fs.readFileSync(path, 'utf8')}};
  }} catch (error) {{
    if (error && error.code === 'ENOENT') return {{status: 'missing', text: ''}};
    throw new Error('unreadable_input');
  }}
}}

function nonblankLines(text) {{
  return text.split(/\n/).map(line => line.trim()).filter(Boolean);
}}

function readDisable(path) {{
  const record = readOptional(path);
  if (record.status === 'missing') return 'missing';
  const value = record.text.trim();
  if (value !== '0' && value !== '1') throw new Error('invalid_disable_value');
  return value;
}}

function main() {{
  const addressInput = readOptional('/proc/net/if_inet6');
  const routeInput = readOptional('/proc/net/ipv6_route');
  let nonLoopbackAddressCount = 0;
  let loopbackDefaultRouteCount = 0;
  let nonLoopbackDefaultRouteCount = 0;

  if (addressInput.status === 'present') {{
    for (const line of nonblankLines(addressInput.text)) {{
      const fields = line.split(/\s+/);
      if (fields.length !== 6) throw new Error('malformed_if_inet6');
      if (!/^[0-9a-fA-F]{{32}}$/.test(fields[0]) ||
          !/^[0-9a-fA-F]{{1,8}}$/.test(fields[1]) ||
          !/^[0-9a-fA-F]{{1,2}}$/.test(fields[2]) ||
          !/^[0-9a-fA-F]{{1,2}}$/.test(fields[3]) ||
          !/^[0-9a-fA-F]{{1,2}}$/.test(fields[4]) || !fields[5]) {{
        throw new Error('unknown_if_inet6_format');
      }}
      if (fields[5].trim() !== 'lo') nonLoopbackAddressCount += 1;
    }}
  }}

  if (routeInput.status === 'present') {{
    for (const line of nonblankLines(routeInput.text)) {{
      const fields = line.split(/\s+/);
      if (fields.length !== 10) throw new Error('malformed_ipv6_route');
      const widths = [32, 2, 32, 2, 32, 8, 8, 8, 8];
      for (let index = 0; index < widths.length; index += 1) {{
        const pattern = new RegExp(`^[0-9a-fA-F]{{${{widths[index]}}}}$`);
        if (!pattern.test(fields[index])) throw new Error('unknown_ipv6_route_format');
      }}
      const name = fields[9].trim();
      if (!name) throw new Error('unknown_ipv6_route_format');
      if (fields[0] === '00000000000000000000000000000000' && fields[1] === '00') {{
        if (name === 'lo') loopbackDefaultRouteCount += 1;
        else nonLoopbackDefaultRouteCount += 1;
      }}
    }}
  }}

  let confNames;
  try {{
    confNames = fs.readdirSync('/proc/sys/net/ipv6/conf').sort();
  }} catch (error) {{
    if (error && error.code === 'ENOENT') confNames = [];
    else throw new Error('unreadable_disable_directory');
  }}
  if (confNames.length > MAX_INTERFACES + 3) throw new Error('interface_set_unbounded');

  const special = {{}};
  for (const name of ['all', 'default', 'lo']) {{
    special[name] = readDisable(`/proc/sys/net/ipv6/conf/${{name}}/disable_ipv6`);
  }}
  const ordinaryNames = confNames.filter(name => !['all', 'default', 'lo'].includes(name)).sort();
  if (ordinaryNames.length > MAX_INTERFACES) throw new Error('interface_set_unbounded');
  const interfaces = ordinaryNames.map((name, index) => ({{
    interface_index: index + 1,
    disable_ipv6: readDisable(`/proc/sys/net/ipv6/conf/${{name}}/disable_ipv6`)
  }}));

  console.log(JSON.stringify({{
    result: 'PASS', category: 'normalized_ipv6_state',
    address_source: addressInput.status, route_source: routeInput.status,
    non_loopback_address_count: nonLoopbackAddressCount,
    loopback_default_route_count: loopbackDefaultRouteCount,
    non_loopback_default_route_count: nonLoopbackDefaultRouteCount,
    disable_ipv6: {{...special, interfaces}}
  }}));
}}

try {{ main(); }} catch (error) {{ fail(error && error.message ? error.message : 'diagnosis_failed'); }}
""".strip()


def emit(control: str, result: str, **details: object) -> None:
    print(json.dumps({"control": control, "result": result, **details}, sort_keys=True), flush=True)


def command(
    args: list[str],
    *,
    check: bool = True,
    timeout: float = COMMAND_TIMEOUT_SECONDS,
    respect_operation_deadline: bool = True,
) -> subprocess.CompletedProcess[str]:
    if respect_operation_deadline and ACTIVE_DEADLINE is not None:
        remaining = ACTIVE_DEADLINE - time.monotonic()
        if remaining <= 0:
            raise RuntimeError("operation deadline exhausted")
        timeout = min(timeout, remaining)
    try:
        return subprocess.run(args, text=True, capture_output=True, check=check, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("bounded command timeout") from error
    except subprocess.CalledProcessError as error:
        operation = ":".join(args[:2])
        raise RuntimeError(f"bounded command failed:{operation}") from error


def fixed_resource_exists(resource: str, name: str) -> bool:
    if resource == "container":
        args = ["docker", "ps", "-a", "--filter", f"name=^{name}$", "--format", "{{.ID}}"]
    elif resource == "network":
        args = ["docker", "network", "ls", "--filter", f"name=^{name}$", "--format", "{{.ID}}"]
    else:
        raise ValueError("unsupported fixed resource type")
    values = [line.strip() for line in command(args).stdout.splitlines() if line.strip()]
    if len(values) > 1 or any(not HEX_ID.fullmatch(value) for value in values):
        raise RuntimeError("fixed resource inventory malformed")
    return bool(values)


def bounded_container_ids(*, running_only: bool) -> list[str]:
    args = ["docker", "ps"]
    if not running_only:
        args.append("-a")
    args.extend(["--format", "{{.ID}}"])
    ids = [line.strip() for line in command(args).stdout.splitlines() if line.strip()]
    if len(ids) > MAX_EXISTING_CONTAINERS or any(not HEX_ID.fullmatch(value) for value in ids):
        raise RuntimeError("container inventory malformed or unbounded")
    return ids


def bounded_network_count() -> int:
    ids = [
        line.strip()
        for line in command(["docker", "network", "ls", "--format", "{{.ID}}"])
        .stdout.splitlines()
        if line.strip()
    ]
    if len(ids) > MAX_EXISTING_NETWORKS or any(not HEX_ID.fullmatch(value) for value in ids):
        raise RuntimeError("network inventory malformed or unbounded")
    return len(ids)


def published_binding_count(container_ids: list[str]) -> int:
    count = 0
    for container_id in container_ids:
        raw = command(["docker", "container", "inspect", container_id]).stdout
        if len(raw.encode()) > 1_000_000:
            raise RuntimeError("container inspection output exceeded bound")
        try:
            bindings = json.loads(raw)[0]["HostConfig"].get("PortBindings") or {}
        except (IndexError, KeyError, TypeError, json.JSONDecodeError) as error:
            raise RuntimeError("container binding inventory could not be normalized") from error
        for values in bindings.values():
            if values:
                count += len(values)
                if count > MAX_EXISTING_CONTAINERS * 64:
                    raise RuntimeError("published binding inventory unbounded")
    return count


def inspect_image() -> None:
    observed = command(
        ["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}|{{.Os}}|{{.Architecture}}"]
    ).stdout.strip()
    if observed != f"{IMAGE_ID}|linux|arm64":
        raise RuntimeError("cached image identity or platform mismatch")
    emit("cached_image", "PASS", platform="linux/arm64", runtime="node-v24.20.0-required")


def assert_preconditions() -> None:
    all_ids = bounded_container_ids(running_only=False)
    running_count = len(bounded_container_ids(running_only=True))
    network_count = bounded_network_count()
    binding_count = published_binding_count(all_ids)
    container_collision = fixed_resource_exists("container", CONTAINER)
    network_collision = fixed_resource_exists("network", NETWORK)
    known_stopped_present = fixed_resource_exists("container", KNOWN_STOPPED_CONTAINER)
    emit(
        "bounded_inventory", "OBSERVED", container_count=len(all_ids), network_count=network_count,
        running_container_count=running_count, docker_published_host_port_count=binding_count,
        diagnostic_container_collision=container_collision,
        diagnostic_network_collision=network_collision,
        known_stopped_container_present=known_stopped_present,
        background_mcp_absence_proven=False,
    )
    if container_collision or network_collision:
        raise RuntimeError("fixed diagnostic resource collision")
    if running_count:
        raise RuntimeError("pre-existing running Docker container holdpoint")
    if binding_count:
        raise RuntimeError("Docker-published host port holdpoint")
    emit("preconditions", "PASS")


def create_network() -> None:
    command([
        "docker", "network", "create", "--internal", "--driver", "bridge", "--ipv6=false",
        "--label", LABEL, NETWORK,
    ])


def inspect_network() -> None:
    raw = command(["docker", "network", "inspect", NETWORK]).stdout
    if len(raw.encode()) > 100_000:
        raise RuntimeError("network inspection output exceeded bound")
    try:
        record = json.loads(raw)[0]
        valid = (
            record["Internal"] is True and record["Attachable"] is False
            and record.get("EnableIPv6") is False and not (record.get("Containers") or {})
        )
    except (IndexError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("network inspection could not be normalized") from error
    if not valid:
        raise RuntimeError("diagnostic network configuration mismatch")
    emit("diagnostic_network", "PASS", internal=True, attachable=False, ipv6_enabled=False)


def create_container() -> None:
    command([
        "docker", "create", "--pull=never", "--platform", "linux/arm64", "--name", CONTAINER,
        "--network", NETWORK, "--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=4m",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges:true", "--memory", "128m",
        "--cpus", "0.5", "--pids-limit", "48", "--user", "65534:65534", "--label", LABEL,
        IMAGE, "node", "-e", DIAGNOSIS_JS,
    ])


def execute_container_command() -> dict[str, Any]:
    result = command(["docker", "start", "-a", CONTAINER], check=False)
    raw = result.stdout.strip()
    if len(raw.encode()) > MAX_OUTPUT_BYTES or len(result.stderr.encode()) > MAX_OUTPUT_BYTES:
        raise RuntimeError("diagnostic output exceeded bound")
    if result.stderr.strip():
        raise RuntimeError("diagnostic command emitted stderr")
    lines = raw.splitlines()
    if len(lines) != 1:
        raise RuntimeError("diagnostic output record count mismatch")
    try:
        record = json.loads(lines[0])
    except json.JSONDecodeError as error:
        raise RuntimeError("diagnostic output was not normalized JSON") from error
    if not isinstance(record, dict) or record.get("result") != "PASS" or result.returncode != 0:
        category = str(record.get("category", "diagnostic_failure"))[:100] if isinstance(record, dict) else "diagnostic_failure"
        raise RuntimeError(f"diagnostic container failed:{category}")
    expected_keys = {
        "result", "category", "address_source", "route_source",
        "non_loopback_address_count", "loopback_default_route_count",
        "non_loopback_default_route_count", "disable_ipv6",
    }
    if set(record) != expected_keys or record["category"] != "normalized_ipv6_state":
        raise RuntimeError("diagnostic output schema mismatch")
    if record["address_source"] not in {"present", "missing"} or record["route_source"] not in {"present", "missing"}:
        raise RuntimeError("diagnostic source category invalid")
    counts = [
        record["non_loopback_address_count"], record["loopback_default_route_count"],
        record["non_loopback_default_route_count"],
    ]
    if any(type(value) is not int or value < 0 or value > 65535 for value in counts):
        raise RuntimeError("diagnostic count invalid")
    disable = record["disable_ipv6"]
    if not isinstance(disable, dict) or set(disable) != {"all", "default", "lo", "interfaces"}:
        raise RuntimeError("disable_ipv6 schema mismatch")
    allowed_status = {"0", "1", "missing"}
    if any(disable[key] not in allowed_status for key in ("all", "default", "lo")):
        raise RuntimeError("disable_ipv6 category invalid")
    interfaces = disable["interfaces"]
    if not isinstance(interfaces, list) or len(interfaces) > MAX_INTERFACES:
        raise RuntimeError("disable_ipv6 interface set invalid")
    for index, interface in enumerate(interfaces, start=1):
        if (
            not isinstance(interface, dict)
            or set(interface) != {"interface_index", "disable_ipv6"}
            or interface["interface_index"] != index
            or interface["disable_ipv6"] not in allowed_status
        ):
            raise RuntimeError("disable_ipv6 interface record invalid")
    return {
        "category": record["category"],
        "address_source": record["address_source"],
        "route_source": record["route_source"],
        "non_loopback_address_count": counts[0],
        "loopback_default_route_count": counts[1],
        "non_loopback_default_route_count": counts[2],
        "disable_ipv6": disable,
    }


def verify_container_exit() -> None:
    try:
        state = json.loads(command(["docker", "container", "inspect", CONTAINER]).stdout)[0]["State"]
        valid = not state.get("Running") and state.get("ExitCode") == 0 and not state.get("OOMKilled")
    except (IndexError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("container exit state could not be normalized") from error
    except RuntimeError as error:
        raise RuntimeError("container exit verification failed") from error
    if not valid:
        raise RuntimeError("diagnostic container did not exit cleanly")


def verify_absence() -> list[str]:
    errors: list[str] = []
    try:
        if command(
            ["docker", "ps", "-a", "--filter", f"name=^{CONTAINER}$", "--format", "{{.ID}}"],
            timeout=CLEANUP_TIMEOUT_SECONDS,
            respect_operation_deadline=False,
        ).stdout.strip():
            errors.append("diagnostic container remains")
    except Exception:
        errors.append("container absence check failed")
    try:
        if command(
            ["docker", "network", "ls", "--filter", f"name=^{NETWORK}$", "--format", "{{.ID}}"],
            timeout=CLEANUP_TIMEOUT_SECONDS,
            respect_operation_deadline=False,
        ).stdout.strip():
            errors.append("diagnostic network remains")
    except Exception:
        errors.append("network absence check failed")
    return errors


def run_diagnosis() -> bool:
    global ACTIVE_DEADLINE
    started = time.monotonic()
    ACTIVE_DEADLINE = started + OPERATION_TIMEOUT_SECONDS
    passed = False
    preconditions_passed = False
    created_network = False
    created_container = False
    cleanup_errors: list[str] = []
    removal_observations: list[str] = []
    try:
        assert_preconditions()
        preconditions_passed = True
        inspect_image()
        created_network = True
        create_network()
        inspect_network()
        created_container = True
        create_container()
        record = execute_container_command()
        verify_container_exit()
        emit("ipv6_diagnosis", "PASS", **record)
        passed = True
    except Exception as error:
        emit("diagnosis" if preconditions_passed else "precondition", "FAIL", error=str(error)[:300])
    finally:
        if created_container:
            try:
                if command(
                    ["docker", "rm", "-f", CONTAINER], check=False,
                    timeout=CLEANUP_TIMEOUT_SECONDS, respect_operation_deadline=False,
                ).returncode != 0:
                    removal_observations.append("container_removal_nonzero")
            except Exception:
                removal_observations.append("container_removal_command_failed")
        if created_network:
            try:
                if command(
                    ["docker", "network", "rm", NETWORK], check=False,
                    timeout=CLEANUP_TIMEOUT_SECONDS, respect_operation_deadline=False,
                ).returncode != 0:
                    removal_observations.append("network_removal_nonzero")
            except Exception:
                removal_observations.append("network_removal_command_failed")
        if preconditions_passed:
            cleanup_errors.extend(verify_absence())
            emit(
                "cleanup",
                "FAIL" if cleanup_errors else "PASS",
                error_count=len(cleanup_errors),
                error_categories=cleanup_errors,
                removal_observations=removal_observations,
            )
        else:
            emit("cleanup", "NOT_APPLICABLE", reason="precondition_failed_before_creation")
    ACTIVE_DEADLINE = None
    if time.monotonic() - started > TOTAL_TIMEOUT_SECONDS:
        emit("total_time", "FAIL", category="total_execution_timeout")
        return False
    return passed and preconditions_passed and not cleanup_errors


if __name__ == "__main__":
    sys.exit(0 if run_diagnosis() else 1)
