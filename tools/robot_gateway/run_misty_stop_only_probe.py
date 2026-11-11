#!/usr/bin/python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import select
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/Users/debb/dev/soga-clean")
PRESENTATION = Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak")
MANIFEST_PATH = ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json"
MANIFEST_SHA256 = "f4a84b8b1a3e732009afeaf56ba443177c7acf62844ce25074cb4cad0761ab99"
PROBE_PATH = ROOT / "robot_gateway/misty_stop_probe.py"
REQUEST_PATH = Path("/Users/debb/dev/research-evidence/soga/requests/IIW_MISTY_STOP_ONLY_PHYSICAL_EXECUTION_REQUEST.md")
AUTHORITY_PATH = Path("/Users/debb/dev/research-evidence/soga/authorizations/IIW_MISTY_STOP_ONLY_PHYSICAL_EXECUTION_AUTHORITY.md")
PREFLIGHT_PATH = Path("/Users/debb/dev/research-evidence/soga/preflight/iiw-misty-stop-only-physical-v1-preflight.json")
EXCLUDED_STATUS = ["?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md"]
MINIMAL_ENV = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": "/Users/debb", "LANG": "C", "LC_ALL": "C"}
PACKAGE_PATHS = {
    "robot_gateway/misty_stop_probe.py",
    "robot_gateway/STOP_ONLY_VERIFICATION.md",
    "tests/test_robot_gateway_misty_stop_only_probe.py",
    "tools/robot_gateway/misty-stop-only-runtime-manifest.json",
    "tools/robot_gateway/run_misty_stop_only_probe.py",
    "tools/robot_gateway/run_misty_stop_only_synthetic_tests.py",
}
# The separately reviewed CyberPi package may coexist only as new paths.
CYBERPI_ADDITION_PATHS = {
    "knowledge/proposals/IIW_MBOT2_CYBERPI_PROTOCOL_VERIFICATION_PROPOSAL_2026-11-05.md",
    "robot_gateway/cyberpi_f3f4_protocol.py",
    "robot_gateway/CYBERPI_PROTOCOL_VERIFICATION.md",
    "tests/test_robot_gateway_cyberpi_protocol.py",
    "tools/robot_gateway/run_cyberpi_protocol_tests.py",
    "tools/robot_gateway/cyberpi-protocol-runtime-manifest.json",
    "knowledge/proposals/MBOT2_FIRST_PROTOCOL_OBSERVATION_R2_2026-11-09.md",
    "knowledge/proposals/TWO_ROBOT_SWITCHING_RUNTIME_R2_2026-11-09.md",
    "robot_gateway/CYBERPI_NONE_OBSERVATION.md",
    "robot_gateway/OPERATOR_RUNTIME.md",
    "robot_gateway/SWITCHING_REVIEW.md",
    "robot_gateway/cyberpi_none_observation.py",
    "robot_gateway/operator_runtime.py",
    "robot_gateway/owned_gateway.py",
    "robot_gateway/switching.py",
    "tests/test_robot_gateway_cyberpi_none_observation.py",
    "tests/test_robot_gateway_operator_runtime.py",
    "tests/test_switching.py",
    "tools/robot_gateway/cyberpi-none-runtime-manifest.json",
    "tools/robot_gateway/operator-runtime-manifest.json",
    "tools/robot_gateway/run_cyberpi_none_physical.py",
    "tools/robot_gateway/run_cyberpi_none_synthetic.py",
    "tools/robot_gateway/run_operator_runtime_synthetic.py",
}
ALLOWED_COMMIT_PATHS = PACKAGE_PATHS | {"knowledge/strategy/DECISION_LOG.md", "knowledge/working/CURRENT_STATE.md"}

# Narrow injectable seams used only by the isolated synthetic tests. Production
# invocation uses these exact defaults.
PATH_EXISTS = lambda path: path.exists()
MAKE_DIRECTORY = lambda path: path.mkdir(mode=0o700, parents=False)
WRITE_BYTES = lambda path, value: path.write_bytes(value)
WRITE_TEXT = lambda path, value: path.write_text(value, encoding="utf-8")
MONOTONIC = time.monotonic
NOW_UTC = lambda: datetime.now(timezone.utc)
ENVIRONMENT = lambda: os.environ
ARGUMENTS = lambda: sys.argv
FLAGS = lambda: sys.flags
SELECT_READY = lambda: select.select([sys.stdin], [], [], 30.0)[0]
READ_INPUT = lambda: sys.stdin.readline()
RECORD_HASHES = lambda: record_hashes_only()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RuntimeError("duplicate_json_key")
        result[key] = value
    return result


def read_json(path: Path) -> dict[str, object]:
    def reject_constant(_value):
        raise RuntimeError("non_finite_json_number")
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys, parse_constant=reject_constant)
    if not isinstance(value, dict):
        raise RuntimeError("non_object_record")
    return value


def command(argv: list[str], *, allowed=(0,)) -> tuple[int, str]:
    result = subprocess.run(argv, cwd=str(ROOT), env=MINIMAL_ENV, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5, check=False)
    if result.returncode not in allowed or result.stderr:
        raise RuntimeError("local_observation_failed")
    return result.returncode, result.stdout


def repository_observations(manifest: dict[str, object], request: dict[str, object] | None = None) -> dict[str, object]:
    _, head = command(["/usr/bin/git", "-C", str(ROOT), "rev-parse", "HEAD"])
    _, status = command(["/usr/bin/git", "-C", str(ROOT), "status", "--porcelain=v1", "--untracked-files=all"])
    _, presentation_head = command(["/usr/bin/git", "-C", str(PRESENTATION), "rev-parse", "HEAD"])
    _, presentation_status = command(["/usr/bin/git", "-C", str(PRESENTATION), "status", "--porcelain=v1", "--untracked-files=all"])
    status_lines = status.splitlines()
    if status_lines != EXCLUDED_STATUS or presentation_status.splitlines():
        raise RuntimeError("repository_status_mismatch")
    soga_head = head.strip()
    presentation_value = presentation_head.strip()
    if presentation_value != manifest.get("presentation_basis"):
        raise RuntimeError("presentation_basis_mismatch")
    basis = manifest.get("repository_basis")
    if not isinstance(basis, str):
        raise RuntimeError("repository_basis_mismatch")
    command(["/usr/bin/git", "-C", str(ROOT), "merge-base", "--is-ancestor", basis, "HEAD"])
    _, diff = command(["/usr/bin/git", "-C", str(ROOT), "diff", "--no-renames", "--name-only", basis + "..HEAD"])
    changed = set(diff.splitlines())
    extra = changed - ALLOWED_COMMIT_PATHS
    if not PACKAGE_PATHS.issubset(changed) or not extra.issubset(CYBERPI_ADDITION_PATHS):
        raise RuntimeError("repository_basis_mismatch")
    if extra:
        _, additions = command(["/usr/bin/git", "-C", str(ROOT), "diff",
                                "--no-renames", "--diff-filter=A", "--name-only", basis + "..HEAD"])
        if not extra.issubset(additions.splitlines()):
            raise RuntimeError("repository_basis_mismatch")
    if request is not None and (request.get("soga_head") != soga_head or request.get("presentation_head") != presentation_value):
        raise RuntimeError("execution_head_mismatch")
    return {"repository_basis": basis, "soga_head": soga_head, "changed_paths": sorted(changed), "soga_status": status_lines, "presentation_head": presentation_value, "presentation_status": []}


def live_observations() -> dict[str, object]:
    _, address = command(["/usr/sbin/ipconfig", "getifaddr", "en0"])
    _, interface = command(["/sbin/ifconfig", "en0", "inet"])
    _, route = command(["/sbin/route", "-n", "get", "192.168.8.219"])
    rc4317, out4317 = command(["/usr/sbin/lsof", "-nP", "-iTCP:4317", "-sTCP:LISTEN"], allowed=(0, 1))
    rc4318, out4318 = command(["/usr/sbin/lsof", "-nP", "-iTCP:4318", "-sTCP:LISTEN"], allowed=(0, 1))
    inet_values = [line.split()[1] for line in interface.splitlines() if line.strip().startswith("inet ") and len(line.split()) > 1]
    if address.strip() != "192.168.8.247" or inet_values != ["192.168.8.247"]:
        raise RuntimeError("interface_mismatch")
    route_fields = {}
    for line in route.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            route_fields[key.strip()] = value.strip()
    destination = route_fields.get("destination")
    if route_fields.get("route to") != "192.168.8.219" or route_fields.get("interface") != "en0":
        raise RuntimeError("route_mismatch")
    if destination not in ("192.168.8.219", "192.168.8.0"):
        raise RuntimeError("route_destination_mismatch")
    if destination == "192.168.8.0" and route_fields.get("mask") != "255.255.255.0":
        raise RuntimeError("route_mask_mismatch")
    flags_text = route_fields.get("flags", "")
    route_flags = {token.strip() for token in flags_text.strip().strip("<>").split(",") if token.strip()}
    if not route_flags or route_flags & {"G", "GATEWAY"}:
        raise RuntimeError("indirect_route_refused")
    if not (rc4317 == 1 and not out4317 and rc4318 == 1 and not out4318):
        raise RuntimeError("listener_present")
    if route_fields.get("ifa") not in (None, "192.168.8.247"):
        raise RuntimeError("route_source_mismatch")
    invariant = {
        "interface": "en0", "address": address.strip(), "ifconfig_inet": inet_values,
        "route_to": route_fields.get("route to"), "route_interface": route_fields.get("interface"),
        "route_ifa": route_fields.get("ifa"), "on_link": True, "ports_4317_4318_unused": True,
    }
    diagnostic = {"destination": destination, "mask": route_fields.get("mask"), "gateway": route_fields.get("gateway"), "flags": sorted(route_flags), "route_text": route[:4096]}
    return {"invariant": invariant, "diagnostic": diagnostic}


def parse_time(value: object) -> datetime:
    if not isinstance(value, str):
        raise RuntimeError("invalid_observation_time")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise RuntimeError("naive_observation_time")
    return parsed.astimezone(timezone.utc)


def verify_records(manifest: dict[str, object]) -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, str]]:
    request = read_json(REQUEST_PATH)
    authority = read_json(AUTHORITY_PATH)
    preflight = read_json(PREFLIGHT_PATH)
    record_hashes = {
        "request": sha256_path(REQUEST_PATH), "authority": sha256_path(AUTHORITY_PATH),
        "preflight": sha256_path(PREFLIGHT_PATH), "runner": sha256_path(Path(__file__).resolve()),
    }
    request_hash = record_hashes["request"]
    if authority.get("schema") != "iiw-misty-stop-only-physical-authority-v1" or authority.get("request_sha256") != request_hash:
        raise RuntimeError("authority_request_mismatch")
    if request.get("schema") != "iiw-misty-stop-only-physical-request-v1":
        raise RuntimeError("request_schema_mismatch")
    required_request_keys = {
        "schema", "soga_head", "presentation_head", "package_sha256", "manifest_sha256",
        "physical_request_path", "physical_authority_path", "physical_preflight_path",
        "physical_evidence_directory", "physical_preflight_schema",
        "physical_preflight_max_age_seconds", "accepted_synthetic_evidence_sha256", "command",
    }
    if set(request) != required_request_keys:
        raise RuntimeError("request_key_set_mismatch")
    request_pins = {
        "physical_request_path": str(REQUEST_PATH),
        "physical_authority_path": str(AUTHORITY_PATH),
        "physical_preflight_path": str(PREFLIGHT_PATH),
        "physical_evidence_directory": manifest["physical_evidence_directory"],
        "physical_preflight_schema": manifest["physical_preflight_schema"],
        "physical_preflight_max_age_seconds": manifest["physical_preflight_max_age_seconds"],
    }
    for key, expected in request_pins.items():
        if request.get(key) != expected:
            raise RuntimeError("request_pin_mismatch")
    hashes = request.get("package_sha256")
    if not isinstance(hashes, dict):
        raise RuntimeError("missing_package_hashes")
    paths = {
        "robot_gateway/misty_stop_probe.py": PROBE_PATH,
        "tools/robot_gateway/run_misty_stop_only_probe.py": Path(__file__).resolve(),
        "tools/robot_gateway/run_misty_stop_only_synthetic_tests.py": ROOT / "tools/robot_gateway/run_misty_stop_only_synthetic_tests.py",
        "tools/robot_gateway/misty-stop-only-runtime-manifest.json": MANIFEST_PATH,
        "tests/test_robot_gateway_misty_stop_only_probe.py": ROOT / "tests/test_robot_gateway_misty_stop_only_probe.py",
        "robot_gateway/STOP_ONLY_VERIFICATION.md": ROOT / "robot_gateway/STOP_ONLY_VERIFICATION.md",
    }
    if set(hashes) != set(paths):
        raise RuntimeError("package_hash_set_mismatch")
    for name, path in paths.items():
        if hashes[name] != sha256_path(path):
            raise RuntimeError("package_hash_mismatch")
    if request.get("manifest_sha256") != MANIFEST_SHA256 or sha256_path(MANIFEST_PATH) != MANIFEST_SHA256:
        raise RuntimeError("manifest_hash_mismatch")
    if request.get("command") != ["/usr/bin/python3", "-I", "-B", str(Path(__file__).resolve())]:
        raise RuntimeError("command_mismatch")
    synthetic_evidence = request.get("accepted_synthetic_evidence_sha256")
    synthetic_dir = Path(manifest["synthetic_evidence_directory"]).resolve()
    expected_synthetic_paths = {str(synthetic_dir / name) for name in ("evidence.json", "stdout.bin", "stderr.bin")}
    if not isinstance(synthetic_evidence, dict) or set(synthetic_evidence) != expected_synthetic_paths:
        raise RuntimeError("synthetic_evidence_pin_mismatch")
    for absolute, expected in synthetic_evidence.items():
        path = Path(absolute)
        if path.resolve().parent != synthetic_dir or sha256_path(path) != expected:
            raise RuntimeError("synthetic_evidence_pin_mismatch")
    synthetic_record = read_json(synthetic_dir / "evidence.json")
    if not (
        synthetic_record.get("schema") == "iiw-misty-stop-only-synthetic-evidence-v1"
        and synthetic_record.get("returncode") == 0
        and synthetic_record.get("outcome") == "completed"
        and synthetic_record.get("controller_error") is None
        and synthetic_record.get("passed_test_count") == manifest["synthetic_expected_test_count"]
        and synthetic_record.get("manifest_sha256") == MANIFEST_SHA256
    ):
        raise RuntimeError("synthetic_evidence_not_accepted")
    if synthetic_record.get("stdout_sha256") != synthetic_evidence[str(synthetic_dir / "stdout.bin")]:
        raise RuntimeError("synthetic_stdout_pin_mismatch")
    if synthetic_record.get("stderr_sha256") != synthetic_evidence[str(synthetic_dir / "stderr.bin")]:
        raise RuntimeError("synthetic_stderr_pin_mismatch")
    if synthetic_record.get("before") != synthetic_record.get("after"):
        raise RuntimeError("synthetic_state_changed")
    if synthetic_record.get("controller_sha256") != request.get("package_sha256", {}).get("tools/robot_gateway/run_misty_stop_only_synthetic_tests.py"):
        raise RuntimeError("synthetic_controller_pin_mismatch")
    if set(authority) != {"schema", "request_sha256", "authorized_by", "authorized_at", "automatic_retry", "physical_capability"}:
        raise RuntimeError("authority_key_set_mismatch")
    if authority.get("authorized_by") != "Deb" or authority.get("automatic_retry") is not False or authority.get("physical_capability") != "stop_only":
        raise RuntimeError("authority_value_mismatch")
    authorized_at = parse_time(authority.get("authorized_at"))
    if authorized_at > datetime.now(timezone.utc):
        raise RuntimeError("authority_time_invalid")
    if preflight.get("schema") != manifest["physical_preflight_schema"]:
        raise RuntimeError("preflight_schema_mismatch")
    times = preflight.get("observation_times")
    if not isinstance(times, dict) or not times or not all(isinstance(key, str) and isinstance(value, str) for key, value in times.items()):
        raise RuntimeError("missing_observation_times")
    parsed_times = [parse_time(item) for item in times.values()]
    now = datetime.now(timezone.utc)
    oldest, newest = min(parsed_times), max(parsed_times)
    age = (now - oldest).total_seconds()
    if newest > now or age < 0 or age > manifest["physical_preflight_max_age_seconds"]:
        raise RuntimeError("preflight_stale")
    required = {
        "confirmed_by": "Deb", "platform_id": "urn:debblabs:misty-b:20193802932",
        "serial": "20193802932", "config": "010-000002",
        "misty_mac": "00:D0:CA:00:96:C3", "misty_ip": "192.168.8.219",
        "laptop_interface": "en0", "laptop_ip": "192.168.8.247", "associated_client_count": 2,
        "sole_powered_misty": True, "misty_idle": True,
        "misty_not_speaking": True, "misty_not_visibly_moving": True,
        "power_switch_touched_and_reachable": True, "stable_on_dock_or_foam_block": True,
        "beryl_exact_clients": ["00:D0:CA:00:96:C3", "laptop"],
        "remote_admin_disabled": True, "port_forwarding_disabled": True,
        "local_network_permission_confirmed": True, "public_demo_closed": True,
        "rehearsal_closed": True, "misty_studio_closed": True, "other_robot_controller_closed": True,
    }
    required_time_labels = {
        "serial_config_identity", "complete_beryl_inventory", "misty_idle_state",
        "power_switch_access", "stable_placement", "router_controls",
        "local_network_permission", "competing_controllers_closed",
    }
    if set(times) != required_time_labels:
        raise RuntimeError("observation_time_labels_mismatch")
    if set(preflight) != {"schema", "observation_times"} | set(required):
        raise RuntimeError("preflight_key_set_mismatch")
    for key, expected in required.items():
        actual = preflight.get(key)
        if type(actual) is not type(expected):
            raise RuntimeError("preflight_type_mismatch")
        if actual != expected:
            raise RuntimeError("preflight_value_mismatch")
    return request, authority, preflight, record_hashes


def record_hashes_only() -> dict[str, str]:
    return {
        "request": sha256_path(REQUEST_PATH), "authority": sha256_path(AUTHORITY_PATH),
        "preflight": sha256_path(PREFLIGHT_PATH), "runner": sha256_path(Path(__file__).resolve()),
    }


def verify_manifest(manifest: dict[str, object]) -> dict[str, object]:
    observed: dict[str, object] = {}
    for section, base in (("source_sha256", ROOT), ("accepted_gateway_sha256", ROOT), ("preserved_sha256", ROOT)):
        values = manifest.get(section)
        if not isinstance(values, dict):
            raise RuntimeError("manifest_section_missing")
        section_observed = {}
        for relative, expected in values.items():
            actual = sha256_path(base / relative)
            if actual != expected:
                raise RuntimeError("protected_hash_mismatch")
            section_observed[relative] = actual
        observed[section] = section_observed
    presentation_observed = {}
    for relative, expected in manifest["presentation_sha256"].items():
        actual = sha256_path(PRESENTATION / relative)
        if actual != expected:
            raise RuntimeError("presentation_hash_mismatch")
        presentation_observed[relative] = actual
    observed["presentation_sha256"] = presentation_observed
    evidence_observed = {}
    for absolute, expected in manifest["accepted_evidence_sha256"].items():
        actual = sha256_path(Path(absolute))
        if actual != expected:
            raise RuntimeError("evidence_hash_mismatch")
        evidence_observed[absolute] = actual
    observed["accepted_evidence_sha256"] = evidence_observed
    return observed


def load_probe():
    spec = importlib.util.spec_from_file_location("misty_stop_probe_physical", PROBE_PATH)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("probe_loader_missing")
    spec.loader.exec_module(module)
    return module


def readiness() -> None:
    sys.stdout.write("Type PI_READY_AT_POWER_SWITCH within 30 seconds, or STOPPED:\n")
    sys.stdout.flush()
    ready = SELECT_READY()
    if not ready or READ_INPUT().strip() != "PI_READY_AT_POWER_SWITCH":
        raise RuntimeError("pi_readiness_refused")


def main() -> None:
    for key in ENVIRONMENT():
        if "PROXY" in key.upper() or (key.startswith("GIT_") and key != "GIT_PAGER"):
            raise RuntimeError("ambient_environment_refused")
    flags = FLAGS()
    if ARGUMENTS() != [str(Path(__file__).resolve())] or flags.isolated != 1 or flags.dont_write_bytecode != 1:
        raise RuntimeError("invocation_mismatch")
    if sha256_path(MANIFEST_PATH) != MANIFEST_SHA256:
        raise RuntimeError("manifest_hash_mismatch")
    manifest = read_json(MANIFEST_PATH)
    manifest_exact = {
        "interpreter": "/usr/bin/python3", "physical_timeout_seconds": 2.0,
        "physical_max_raw_response_bytes": 73728, "physical_max_body_bytes": 65536,
        "target_host": "192.168.8.219", "target_port": 80,
        "local_source_host": "192.168.8.247", "request_sha256": "863897eae5c306229ffaed3ebfd943fe1c99a03a8753ef8922df174c2d8f13ab",
        "physical_request_path": str(REQUEST_PATH), "physical_authority_path": str(AUTHORITY_PATH),
        "physical_preflight_path": str(PREFLIGHT_PATH),
    }
    for key, expected in manifest_exact.items():
        if manifest.get(key) != expected:
            raise RuntimeError("manifest_value_mismatch")
    before_hashes = verify_manifest(manifest)
    request, authority, preflight, record_hashes = verify_records(manifest)
    before_repo = repository_observations(manifest, request)
    before_live = live_observations()
    probe = load_probe()
    readiness()
    request, authority, preflight, ready_record_hashes = verify_records(manifest)
    if ready_record_hashes != record_hashes:
        raise RuntimeError("record_hold_changed_before_consumption")
    ready_repo = repository_observations(manifest, request)
    ready_live = live_observations()
    if before_repo != ready_repo or before_live["invariant"] != ready_live["invariant"]:
        raise RuntimeError("hold_changed_before_consumption")
    evidence_dir = Path(manifest["physical_evidence_directory"])
    if PATH_EXISTS(evidence_dir):
        raise RuntimeError("evidence_directory_must_be_absent")
    MAKE_DIRECTORY(evidence_dir)
    started_utc = NOW_UTC().isoformat()
    started_mono = MONOTONIC()
    result: dict[str, object] = {"classification": "INTERNAL_FAILED", "acknowledged": False}
    raw = b""
    after_live: dict[str, object] = {}
    after_repo: dict[str, object] = {}
    after_hashes: dict[str, object] = {}
    postcondition_error: str | None = None
    try:
        WRITE_BYTES(evidence_dir / "request.bin", probe.REQUEST_BYTES)
        result, raw = probe.run_probe()
    except BaseException as exc:
        postcondition_error = type(exc).__name__
    post_errors: list[str] = []
    try:
        WRITE_BYTES(evidence_dir / "response.bin", raw)
    except BaseException as exc:
        post_errors.append("response_write:" + str(exc)[:120])
    try:
        if RECORD_HASHES() != ready_record_hashes:
            raise RuntimeError("record_hold_changed_after_consumption")
    except BaseException as exc:
        post_errors.append("records:" + str(exc)[:120])
    try:
        after_live = live_observations()
        if after_live["invariant"] != ready_live["invariant"]:
            raise RuntimeError("live_hold_changed")
    except BaseException as exc:
        post_errors.append("live:" + str(exc)[:120])
    try:
        after_repo = repository_observations(manifest, request)
        if after_repo != ready_repo:
            raise RuntimeError("repository_hold_changed")
    except BaseException as exc:
        post_errors.append("repository:" + str(exc)[:120])
    try:
        after_hashes = verify_manifest(manifest)
        if after_hashes != before_hashes:
            raise RuntimeError("protected_state_changed")
    except BaseException as exc:
        post_errors.append("protected:" + str(exc)[:120])
    if post_errors:
        postcondition_error = postcondition_error or ";".join(post_errors)
    elapsed = MONOTONIC() - started_mono
    evidence = {
        "schema": "iiw-misty-stop-only-physical-evidence-v1",
        "classification": "INTERNAL_FAILED" if postcondition_error else result.get("classification"),
        "probe_result": result,
        "operator_attestation_status": "pending",
        "request_sha256": probe.REQUEST_SHA256,
        "response_sha256": hashlib.sha256(raw).hexdigest(),
        "physical_runner_sha256": record_hashes["runner"],
        "manifest_sha256": MANIFEST_SHA256,
        "execution_request_sha256": record_hashes["request"],
        "authority_sha256": record_hashes["authority"],
        "preflight_sha256": record_hashes["preflight"],
        "preflight": preflight,
        "started_utc": started_utc,
        "ended_utc": NOW_UTC().isoformat(),
        "elapsed_seconds": round(elapsed, 6),
        "limits": {"total_deadline_seconds": 2.0, "max_raw_response_bytes": 73728, "max_body_bytes": 65536},
        "interpreter_version": sys.version.split()[0],
        "postcondition_error_type": postcondition_error,
        "before_protected_sha256": before_hashes,
        "after_protected_sha256": after_hashes,
        "before_repository": before_repo,
        "ready_repository": ready_repo,
        "after_repository": after_repo,
        "before_live": before_live,
        "ready_live": ready_live,
        "after_live": after_live,
        "automatic_retry": False,
        "physical_outcome": "unknown",
    }
    WRITE_TEXT(evidence_dir / "evidence.json", json.dumps(evidence, sort_keys=True, separators=(",", ":")) + "\n")
    if result.get("classification") != "ACKNOWLEDGED" or postcondition_error is not None:
        raise RuntimeError("stop_only_probe_not_acknowledged")


if __name__ == "__main__":
    main()
