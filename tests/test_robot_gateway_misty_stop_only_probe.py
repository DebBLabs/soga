from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import socket
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / "robot_gateway" / "misty_stop_probe.py"
PHYSICAL_RUNNER = ROOT / "tools" / "robot_gateway" / "run_misty_stop_only_probe.py"
SYNTHETIC_RUNNER = ROOT / "tools" / "robot_gateway" / "run_misty_stop_only_synthetic_tests.py"
ACCEPTED_PARSER = ROOT / "robot_gateway" / "strict_json_post.py"


def load_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


probe = load_path("misty_stop_probe_under_test", PROBE_PATH)
physical_runner = load_path("misty_stop_physical_runner_under_test", PHYSICAL_RUNNER)
synthetic_runner = load_path("misty_stop_synthetic_runner_under_test", SYNTHETIC_RUNNER)


class FakeSocket:
    def __init__(self, chunks=(), *, local=("192.168.8.247", 50000), send_error=None, partial_send=None, recv_error=None):
        self.chunks = list(chunks)
        self.local = local
        self.send_error = send_error
        self.partial_send = partial_send
        self.recv_error = recv_error
        self.sent = []
        self.closed = False
        self.timeouts = []

    def getsockname(self):
        return self.local

    def settimeout(self, value):
        self.timeouts.append(value)

    def send(self, value):
        if self.send_error:
            raise self.send_error
        count = min(len(value), self.partial_send) if self.partial_send else len(value)
        self.sent.append(bytes(value[:count]))
        return count

    def recv(self, _size):
        if self.recv_error:
            raise self.recv_error
        return self.chunks.pop(0) if self.chunks else b""

    def close(self):
        self.closed = True


class Factory:
    def __init__(self, sock):
        self.sock = sock
        self.calls = []

    def __call__(self, target, *, timeout, source_address):
        self.calls.append((target, timeout, source_address))
        return self.sock


def response(body=b'{"result":true}', status=b"200 OK", headers=()):
    lines = [b"HTTP/1.1 " + status, b"Content-Length: " + str(len(body)).encode(), *headers]
    return b"\r\n".join(lines) + b"\r\n\r\n" + body


class MistyStopProbeTests(unittest.TestCase):
    def test_01_exact_request_bytes_and_hash(self):
        self.assertEqual(len(probe.REQUEST_BYTES), 150)
        self.assertEqual(hashlib.sha256(probe.REQUEST_BYTES).hexdigest(), probe.REQUEST_SHA256)

    def test_02_exact_target_and_source(self):
        self.assertEqual(probe.TARGET, ("192.168.8.219", 80))
        self.assertEqual(probe.LOCAL_SOURCE, ("192.168.8.247", 0))

    def test_03_acknowledged_response(self):
        result = probe.classify_response(response(), eof=True)
        self.assertEqual(result["classification"], "ACKNOWLEDGED")

    def test_04_success_status_field(self):
        result = probe.classify_response(response(b'{"result":true,"status":"Success"}'), eof=True)
        self.assertTrue(result["acknowledged"])

    def test_05_result_false_rejected(self):
        self.assertEqual(probe.classify_response(response(b'{"result":false}'), eof=True)["classification"], "REJECTED")

    def test_06_error_member_rejected(self):
        self.assertEqual(probe.classify_response(response(b'{"result":true,"error":"x"}'), eof=True)["classification"], "REJECTED")

    def test_07_non_2xx_precedes_invalid_body(self):
        self.assertEqual(probe.classify_response(response(b"not-json", b"500 Error"), eof=True)["classification"], "REJECTED")

    def test_08_missing_eof_times_out(self):
        self.assertEqual(probe.classify_response(response(), eof=False)["classification"], "TIMED_OUT")

    def test_09_duplicate_json_key_rejected(self):
        with self.assertRaises(probe.ProbeParseError):
            probe.classify_response(response(b'{"result":true,"result":true}'), eof=True)

    def test_10_non_object_rejected(self):
        with self.assertRaises(probe.ProbeParseError):
            probe.classify_response(response(b"[]"), eof=True)

    def test_11_content_length_mismatch(self):
        raw = b"HTTP/1.1 200 OK\r\nContent-Length: 99\r\n\r\n{}"
        with self.assertRaises(probe.ProbeParseError):
            probe.classify_response(raw, eof=True)

    def test_12_raw_overflow(self):
        result = probe.classify_response(b"x" * (probe.MAX_RAW_RESPONSE_BYTES + 1), eof=True)
        self.assertEqual(result["classification"], "OVERFLOW")

    def test_13_one_connection_and_request(self):
        sock = FakeSocket([response()])
        factory = Factory(sock)
        result, _ = probe.run_probe(socket_factory=factory)
        self.assertEqual(len(factory.calls), 1)
        self.assertEqual(factory.calls[0][0], probe.TARGET)
        self.assertEqual(factory.calls[0][2], probe.LOCAL_SOURCE)
        self.assertEqual(b"".join(sock.sent), probe.REQUEST_BYTES)
        self.assertEqual(result["classification"], "ACKNOWLEDGED")
        self.assertTrue(sock.closed)

    def test_14_wrong_local_bind_fails_before_send(self):
        sock = FakeSocket([response()], local=("10.0.0.1", 1))
        result, _ = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["classification"], "TRANSPORT_FAILED")
        self.assertEqual(sock.sent, [])

    def test_15_send_timeout_before_any_byte_is_not_sent(self):
        sock = FakeSocket(send_error=socket.timeout())
        result, _ = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["classification"], "TIMED_OUT")
        self.assertEqual(result["delivery"], "not_sent")

    def test_15a_partial_send_then_failure_is_unknown(self):
        class PartialFailureSocket(FakeSocket):
            def send(self, value):
                if not self.sent:
                    self.sent.append(bytes(value[:7]))
                    return 7
                raise OSError("partial_send_failure")
        sock = PartialFailureSocket()
        result, _ = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["bytes_sent"], 7)
        self.assertEqual(result["delivery"], "unknown")

    def test_16_receive_timeout_unknown(self):
        sock = FakeSocket(recv_error=socket.timeout())
        result, _ = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["classification"], "TIMED_OUT")
        self.assertEqual(result["delivery"], "unknown")

    def test_17_transport_failure(self):
        class Broken:
            def __call__(self, *args, **kwargs):
                raise OSError()
        result, _ = probe.run_probe(socket_factory=Broken())
        self.assertEqual(result["classification"], "TRANSPORT_FAILED")

    def test_18_parser_equivalence_fixtures(self):
        accepted = load_path("accepted_strict_parser", ACCEPTED_PARSER)
        fixtures = [
            {"result": True}, {"result": True, "status": "Success"},
            {"result": False}, {"result": True, "status": "Failure"},
            {"result": True, "error": "x"}, {},
        ]
        for item in fixtures:
            self.assertEqual(probe.response_is_acknowledged(item), accepted.response_is_acknowledged(item))

    def test_19_no_speak_surface_in_probe(self):
        text = PROBE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("/api/tts/speak", text)
        self.assertNotIn("Would you like to dance?", text)

    def test_20_physical_runner_has_no_test_mode(self):
        text = PHYSICAL_RUNNER.read_text(encoding="utf-8")
        self.assertNotIn("unittest", text)
        self.assertNotIn("--test", text)

    def test_21_synthetic_controller_has_no_target(self):
        text = SYNTHETIC_RUNNER.read_text(encoding="utf-8")
        self.assertNotIn("192.168.8.219", text)

    def test_22_fixed_limits(self):
        self.assertEqual(probe.TIMEOUT_SECONDS, 2.0)
        self.assertEqual(probe.MAX_RAW_RESPONSE_BYTES, 73_728)
        self.assertEqual(probe.MAX_BODY_BYTES, 65_536)

    def test_23_request_contains_no_participant_material(self):
        for value in (b"token", b"session", b"parent", b"child", b"decision"):
            self.assertNotIn(value, probe.REQUEST_BYTES.lower())

    def test_24_only_stop_path(self):
        self.assertEqual(probe.REQUEST_BYTES.count(b"/api/tts/stop"), 1)
        self.assertEqual(probe.REQUEST_BYTES.count(b"POST "), 1)

    def test_25_invalid_http_version_is_malformed(self):
        with self.assertRaises(probe.ProbeParseError):
            probe.classify_response(b"GARBAGE 200 OK\r\nContent-Length: 2\r\n\r\n{}", eof=True)

    def test_26_non_2xx_still_requires_valid_framing(self):
        with self.assertRaises(probe.ProbeParseError):
            probe.classify_response(b"HTTP/1.1 500 Error\r\nContent-Length: 9\r\n\r\n{}", eof=True)

    def test_27_negative_chunk_size_is_malformed(self):
        raw = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n1\r\nx\r\n-6\r\n"
        with self.assertRaises(probe.ProbeParseError):
            probe.classify_response(raw, eof=True)

    def test_28_chunked_requires_final_crlf_and_no_trailing_bytes(self):
        for ending in (b"0\r\n", b"0\r\n\r\njunk"):
            raw = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n" + ending
            with self.assertRaises(probe.ProbeParseError):
                probe.classify_response(raw, eof=True)

    def test_29_conflicting_or_unsupported_framing_is_malformed(self):
        fixtures = (
            b"HTTP/1.1 200 OK\r\nTransfer-Encoding: gzip\r\n\r\n{}",
            b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\nContent-Length: 2\r\n\r\n0\r\n\r\n",
            b"HTTP/1.1 200 OK\r\nContent-Length: +2\r\n\r\n{}",
        )
        for raw in fixtures:
            with self.assertRaises(probe.ProbeParseError):
                probe.classify_response(raw, eof=True)

    def test_30_valid_chunked_response(self):
        body = b'{"result":true}'
        raw = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n" + format(len(body), "x").encode() + b"\r\n" + body + b"\r\n0\r\n\r\n"
        self.assertEqual(probe.classify_response(raw, eof=True)["classification"], "ACKNOWLEDGED")

    def test_31_duplicate_http_header_is_malformed(self):
        raw = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nContent-Length: 2\r\n\r\n{}"
        with self.assertRaises(probe.ProbeParseError):
            probe.classify_response(raw, eof=True)

    def test_32_invalid_json_run_probe_is_malformed_and_closes(self):
        sock = FakeSocket([response(b"not-json")])
        result, raw = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["classification"], "MALFORMED")
        self.assertTrue(raw)
        self.assertTrue(sock.closed)

    def test_33_valid_body_without_eof_times_out_with_partial_bytes(self):
        class NeverEof(FakeSocket):
            def recv(self, _size):
                if self.chunks:
                    return self.chunks.pop(0)
                raise socket.timeout()
        wire = response()
        sock = NeverEof([wire])
        result, raw = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["classification"], "TIMED_OUT")
        self.assertEqual(raw, wire)
        self.assertTrue(sock.closed)

    def test_34_injected_clock_deadline_before_connection(self):
        values = iter((0.0, 3.0))
        result, _ = probe.run_probe(socket_factory=Factory(FakeSocket()), monotonic=lambda: next(values))
        self.assertEqual(result["classification"], "TIMED_OUT")
        self.assertEqual(result["delivery"], "not_sent")

    def test_35_route_fixture_accepts_direct_on_link_subnet(self):
        outputs = {
            "/usr/sbin/ipconfig": (0, "192.168.8.247\n"),
            "/sbin/ifconfig": (0, "\tinet 192.168.8.247 netmask 0xffffff00\n"),
            "/sbin/route": (0, "route to: 192.168.8.219\ndestination: 192.168.8.0\nmask: 255.255.255.0\ninterface: en0\nflags: <UP,DONE,CLONING>\n"),
            "/usr/sbin/lsof": (1, ""),
        }
        original = physical_runner.command
        physical_runner.command = lambda argv, allowed=(0,): outputs[argv[0]]
        try:
            observed = physical_runner.live_observations()
        finally:
            physical_runner.command = original
        self.assertEqual(observed["invariant"]["route_interface"], "en0")

    def test_36_route_fixture_rejects_gateway_flag(self):
        outputs = {
            "/usr/sbin/ipconfig": (0, "192.168.8.247\n"),
            "/sbin/ifconfig": (0, "\tinet 192.168.8.247 netmask 0xffffff00\n"),
            "/sbin/route": (0, "route to: 192.168.8.219\ndestination: 192.168.8.219\ninterface: en0\nflags: <UP,GATEWAY>\n"),
            "/usr/sbin/lsof": (1, ""),
        }
        original = physical_runner.command
        physical_runner.command = lambda argv, allowed=(0,): outputs[argv[0]]
        try:
            with self.assertRaises(RuntimeError):
                physical_runner.live_observations()
        finally:
            physical_runner.command = original

    def test_37_controller_audit_and_bounded_process_controls_present(self):
        self.assertIn("os.O_WRONLY", synthetic_runner.CHILD)
        self.assertIn("socket.", synthetic_runner.CHILD)
        self.assertTrue(callable(synthetic_runner.bounded_child))

    def test_38_decoded_body_overflow_is_bounded(self):
        body = b"x" * (probe.MAX_BODY_BYTES + 1)
        sock = FakeSocket([response(body)])
        result, raw = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["classification"], "OVERFLOW")
        self.assertLessEqual(len(raw), probe.MAX_RAW_RESPONSE_BYTES)
        self.assertTrue(sock.closed)

    def test_39_multislice_send_and_multichunk_receive(self):
        wire = response()
        sock = FakeSocket([wire[:11], wire[11:]], partial_send=7)
        result, _ = probe.run_probe(socket_factory=Factory(sock))
        self.assertEqual(result["classification"], "ACKNOWLEDGED")
        self.assertEqual(b"".join(sock.sent), probe.REQUEST_BYTES)
        self.assertGreater(len(sock.sent), 1)

    def test_40_audit_policy_self_check_executes(self):
        result = synthetic_runner.controller_self_check()
        self.assertTrue(all(result.values()))
        with self.assertRaises(RuntimeError):
            synthetic_runner.audit_event("socket.connect", (None,))
        synthetic_runner.audit_event("open", ("x", "r", 0))

    def test_41_readiness_accepts_only_exact_input(self):
        old_ready, old_input = physical_runner.SELECT_READY, physical_runner.READ_INPUT
        old_stdout = sys.stdout
        captured = io.StringIO()
        try:
            sys.stdout = captured
            physical_runner.SELECT_READY = lambda: [object()]
            physical_runner.READ_INPUT = lambda: "PI_READY_AT_POWER_SWITCH\n"
            physical_runner.readiness()
            physical_runner.READ_INPUT = lambda: "STOPPED\n"
            with self.assertRaises(RuntimeError):
                physical_runner.readiness()
            physical_runner.SELECT_READY = lambda: []
            with self.assertRaises(RuntimeError):
                physical_runner.readiness()
        finally:
            sys.stdout = old_stdout
            physical_runner.SELECT_READY, physical_runner.READ_INPUT = old_ready, old_input
        self.assertIn("Type PI_READY_AT_POWER_SWITCH", captured.getvalue())

    def test_42_evidence_paths_are_distinct(self):
        manifest = json.loads((ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json").read_text(encoding="utf-8"))
        self.assertNotEqual(manifest["synthetic_evidence_directory"], manifest["physical_evidence_directory"])

    def test_43_public_demo_has_no_stop_probe_reference(self):
        presentation = Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak")
        for path in (presentation / "bridge.py", presentation / "Start IIW Table.command", ROOT / "robot_gateway/__init__.py"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("misty_stop_probe", text)
            self.assertNotIn("run_misty_stop_only", text)

    def test_44_valid_preflight_time_parser(self):
        value = datetime.now(timezone.utc).isoformat()
        self.assertEqual(physical_runner.parse_time(value).tzinfo, timezone.utc)
        with self.assertRaises(RuntimeError):
            physical_runner.parse_time("2026-11-03T12:00:00")

    def test_45_record_chain_accepts_exact_schema_and_rejects_wrong_type(self):
        manifest = json.loads((ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json").read_text(encoding="utf-8"))
        now = datetime.now(timezone.utc).isoformat()
        package_names = {
            "robot_gateway/misty_stop_probe.py", "robot_gateway/STOP_ONLY_VERIFICATION.md",
            "tests/test_robot_gateway_misty_stop_only_probe.py",
            "tools/robot_gateway/misty-stop-only-runtime-manifest.json",
            "tools/robot_gateway/run_misty_stop_only_probe.py",
            "tools/robot_gateway/run_misty_stop_only_synthetic_tests.py",
        }
        package_hashes = {name: "h-" + name for name in package_names}
        package_hashes["tools/robot_gateway/misty-stop-only-runtime-manifest.json"] = physical_runner.MANIFEST_SHA256
        syn_dir = Path(manifest["synthetic_evidence_directory"])
        syn_hashes = {str(syn_dir / "evidence.json"): "syn-e", str(syn_dir / "stdout.bin"): "syn-o", str(syn_dir / "stderr.bin"): "syn-r"}
        request_hash = "request-hash"
        request = {
            "schema": "iiw-misty-stop-only-physical-request-v1", "soga_head": "head", "presentation_head": manifest["presentation_basis"],
            "package_sha256": package_hashes, "manifest_sha256": physical_runner.MANIFEST_SHA256,
            "physical_request_path": str(physical_runner.REQUEST_PATH), "physical_authority_path": str(physical_runner.AUTHORITY_PATH),
            "physical_preflight_path": str(physical_runner.PREFLIGHT_PATH), "physical_evidence_directory": manifest["physical_evidence_directory"],
            "physical_preflight_schema": manifest["physical_preflight_schema"], "physical_preflight_max_age_seconds": manifest["physical_preflight_max_age_seconds"],
            "accepted_synthetic_evidence_sha256": syn_hashes,
            "command": ["/usr/bin/python3", "-I", "-B", str(physical_runner.Path(physical_runner.__file__).resolve())],
        }
        authority = {"schema": "iiw-misty-stop-only-physical-authority-v1", "request_sha256": request_hash, "authorized_by": "Deb", "authorized_at": now, "automatic_retry": False, "physical_capability": "stop_only"}
        times = {name: now for name in ("serial_config_identity", "complete_beryl_inventory", "misty_idle_state", "power_switch_access", "stable_placement", "router_controls", "local_network_permission", "competing_controllers_closed")}
        preflight = {
            "schema": manifest["physical_preflight_schema"], "observation_times": times, "confirmed_by": "Deb",
            "platform_id": "urn:debblabs:misty-b:20193802932", "serial": "20193802932", "config": "010-000002",
            "misty_mac": "00:D0:CA:00:96:C3", "misty_ip": "192.168.8.219", "laptop_interface": "en0", "laptop_ip": "192.168.8.247",
            "associated_client_count": 2, "sole_powered_misty": True, "misty_idle": True, "misty_not_speaking": True,
            "misty_not_visibly_moving": True, "power_switch_touched_and_reachable": True, "stable_on_dock_or_foam_block": True,
            "beryl_exact_clients": ["00:D0:CA:00:96:C3", "laptop"], "remote_admin_disabled": True, "port_forwarding_disabled": True,
            "local_network_permission_confirmed": True, "public_demo_closed": True, "rehearsal_closed": True,
            "misty_studio_closed": True, "other_robot_controller_closed": True,
        }
        synthetic_record = {"schema": "iiw-misty-stop-only-synthetic-evidence-v1", "returncode": 0, "outcome": "completed", "controller_error": None,
                            "passed_test_count": manifest["synthetic_expected_test_count"], "manifest_sha256": physical_runner.MANIFEST_SHA256,
                            "stdout_sha256": "syn-o", "stderr_sha256": "syn-r", "before": {"x": 1}, "after": {"x": 1},
                            "controller_sha256": package_hashes["tools/robot_gateway/run_misty_stop_only_synthetic_tests.py"]}
        records = {str(physical_runner.REQUEST_PATH): request, str(physical_runner.AUTHORITY_PATH): authority,
                   str(physical_runner.PREFLIGHT_PATH): preflight, str(syn_dir / "evidence.json"): synthetic_record}
        old_read, old_sha = physical_runner.read_json, physical_runner.sha256_path
        def fake_read(path):
            return records[str(path)]
        wrong_path = None
        def fake_sha(path):
            raw = str(path)
            if raw == wrong_path:
                return "wrong-hash"
            if raw == str(physical_runner.REQUEST_PATH): return request_hash
            if raw == str(physical_runner.AUTHORITY_PATH): return "authority-hash"
            if raw == str(physical_runner.PREFLIGHT_PATH): return "preflight-hash"
            if raw == str(physical_runner.MANIFEST_PATH): return physical_runner.MANIFEST_SHA256
            if raw in syn_hashes: return syn_hashes[raw]
            for name, expected in package_hashes.items():
                if raw == str(ROOT / name): return expected
            if raw == str(physical_runner.Path(physical_runner.__file__).resolve()): return package_hashes["tools/robot_gateway/run_misty_stop_only_probe.py"]
            raise AssertionError(raw)
        physical_runner.read_json, physical_runner.sha256_path = fake_read, fake_sha
        try:
            physical_runner.verify_records(manifest)
            base_time = datetime.fromisoformat(now)
            age_limit = manifest["physical_preflight_max_age_seconds"]
            for offset in (-age_limit - 60, 60):
                with self.subTest(offset=offset):
                    times["serial_config_identity"] = (base_time + timedelta(seconds=offset)).isoformat()
                    with self.assertRaisesRegex(RuntimeError, "^preflight_stale$"):
                        physical_runner.verify_records(manifest)
            times["serial_config_identity"] = now
            for record, key, bad, error in (
                (authority, "request_sha256", "wrong", "authority_request_mismatch"),
                (request, "command", ["wrong"], "command_mismatch"),
                (synthetic_record, "after", {"x": 2}, "synthetic_state_changed"),
                (synthetic_record, "controller_sha256", "wrong", "synthetic_controller_pin_mismatch"),
            ):
                with self.subTest(key=key), patch.dict(record, {key: bad}):
                    with self.assertRaisesRegex(RuntimeError, "^" + error + "$"):
                        physical_runner.verify_records(manifest)
            for wrong_path in (str(physical_runner.PROBE_PATH), str(Path(physical_runner.__file__).resolve())):
                with self.subTest(wrong_path=wrong_path):
                    with self.assertRaisesRegex(RuntimeError, "^package_hash_mismatch$"):
                        physical_runner.verify_records(manifest)
            wrong_path = None
            preflight["associated_client_count"] = 2.0
            with self.assertRaises(RuntimeError):
                physical_runner.verify_records(manifest)
        finally:
            physical_runner.read_json, physical_runner.sha256_path = old_read, old_sha

    def test_46_physical_main_writes_truthful_acknowledged_evidence(self):
        manifest = json.loads((ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json").read_text(encoding="utf-8"))
        writes = {}
        record_hashes = {"request": "rq", "authority": "au", "preflight": "pf", "runner": "rn"}
        probe_result = {"classification": "ACKNOWLEDGED", "acknowledged": True, "bytes_sent": 150}
        fake_probe = SimpleNamespace(REQUEST_BYTES=probe.REQUEST_BYTES, REQUEST_SHA256=probe.REQUEST_SHA256, run_probe=lambda: (probe_result, b"response"))
        names = ("sha256_path", "read_json", "verify_manifest", "verify_records", "repository_observations", "live_observations", "load_probe", "readiness",
                 "PATH_EXISTS", "MAKE_DIRECTORY", "WRITE_BYTES", "WRITE_TEXT", "MONOTONIC", "NOW_UTC", "ENVIRONMENT", "ARGUMENTS", "FLAGS", "RECORD_HASHES")
        old = {name: getattr(physical_runner, name) for name in names}
        try:
            physical_runner.sha256_path = lambda path: physical_runner.MANIFEST_SHA256
            physical_runner.read_json = lambda path: manifest
            physical_runner.verify_manifest = lambda value: {"protected": "same"}
            physical_runner.verify_records = lambda value: ({"soga_head": "h"}, {}, {}, record_hashes)
            physical_runner.repository_observations = lambda value, request=None: {"repo": "same"}
            physical_runner.live_observations = lambda: {"invariant": {"live": "same"}, "diagnostic": {}}
            physical_runner.load_probe = lambda: fake_probe
            physical_runner.readiness = lambda: None
            physical_runner.PATH_EXISTS = lambda path: False
            physical_runner.MAKE_DIRECTORY = lambda path: writes.setdefault("mkdir", str(path))
            physical_runner.WRITE_BYTES = lambda path, value: writes.setdefault(path.name, value)
            physical_runner.WRITE_TEXT = lambda path, value: writes.setdefault(path.name, value)
            ticks = iter((0.0, 1.0))
            physical_runner.MONOTONIC = lambda: next(ticks)
            physical_runner.NOW_UTC = lambda: datetime.now(timezone.utc)
            physical_runner.ENVIRONMENT = lambda: {}
            physical_runner.ARGUMENTS = lambda: [str(physical_runner.Path(physical_runner.__file__).resolve())]
            physical_runner.FLAGS = lambda: SimpleNamespace(isolated=1, dont_write_bytecode=1)
            physical_runner.RECORD_HASHES = lambda: record_hashes
            physical_runner.main()
        finally:
            for name, value in old.items(): setattr(physical_runner, name, value)
        evidence = json.loads(writes["evidence.json"])
        self.assertEqual(evidence["classification"], "ACKNOWLEDGED")
        self.assertEqual(evidence["probe_result"], probe_result)
        self.assertEqual(evidence["operator_attestation_status"], "pending")
        self.assertEqual(evidence["physical_outcome"], "unknown")

    def test_47_physical_main_preserves_probe_result_on_postcondition_failure(self):
        manifest = json.loads((ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json").read_text(encoding="utf-8"))
        writes = {}
        record_hashes = {"request": "rq", "authority": "au", "preflight": "pf", "runner": "rn"}
        probe_result = {"classification": "ACKNOWLEDGED", "acknowledged": True}
        fake_probe = SimpleNamespace(REQUEST_BYTES=probe.REQUEST_BYTES, REQUEST_SHA256=probe.REQUEST_SHA256, run_probe=lambda: (probe_result, b"response"))
        names = ("sha256_path", "read_json", "verify_manifest", "verify_records", "repository_observations", "live_observations", "load_probe", "readiness",
                 "PATH_EXISTS", "MAKE_DIRECTORY", "WRITE_BYTES", "WRITE_TEXT", "MONOTONIC", "NOW_UTC", "ENVIRONMENT", "ARGUMENTS", "FLAGS", "RECORD_HASHES")
        old = {name: getattr(physical_runner, name) for name in names}
        calls = {"live": 0}
        def live():
            calls["live"] += 1
            value = "changed" if calls["live"] == 3 else "same"
            return {"invariant": {"live": value}, "diagnostic": {}}
        try:
            physical_runner.sha256_path = lambda path: physical_runner.MANIFEST_SHA256
            physical_runner.read_json = lambda path: manifest
            physical_runner.verify_manifest = lambda value: {"protected": "same"}
            physical_runner.verify_records = lambda value: ({"soga_head": "h"}, {}, {}, record_hashes)
            physical_runner.repository_observations = lambda value, request=None: {"repo": "same"}
            physical_runner.live_observations = live
            physical_runner.load_probe = lambda: fake_probe
            physical_runner.readiness = lambda: None
            physical_runner.PATH_EXISTS = lambda path: False
            physical_runner.MAKE_DIRECTORY = lambda path: None
            physical_runner.WRITE_BYTES = lambda path, value: writes.setdefault(path.name, value)
            physical_runner.WRITE_TEXT = lambda path, value: writes.setdefault(path.name, value)
            ticks = iter((0.0, 1.0))
            physical_runner.MONOTONIC = lambda: next(ticks)
            physical_runner.NOW_UTC = lambda: datetime.now(timezone.utc)
            physical_runner.ENVIRONMENT = lambda: {}
            physical_runner.ARGUMENTS = lambda: [str(physical_runner.Path(physical_runner.__file__).resolve())]
            physical_runner.FLAGS = lambda: SimpleNamespace(isolated=1, dont_write_bytecode=1)
            physical_runner.RECORD_HASHES = lambda: record_hashes
            with self.assertRaises(RuntimeError):
                physical_runner.main()
        finally:
            for name, value in old.items(): setattr(physical_runner, name, value)
        evidence = json.loads(writes["evidence.json"])
        self.assertEqual(evidence["classification"], "INTERNAL_FAILED")
        self.assertEqual(evidence["probe_result"], probe_result)

    def test_48_synthetic_main_records_bounded_success(self):
        manifest = json.loads((ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json").read_text(encoding="utf-8"))
        manifest["synthetic_expected_test_count"] = 49
        stdout = b"".join((f"test_{index:02d} ... ok\n".encode() for index in range(49)))
        writes = {}
        names = ("sha256_path", "LOAD_MANIFEST", "SNAPSHOT", "RUN_CHILD", "PATH_EXISTS", "MAKE_DIRECTORY", "WRITE_BYTES", "WRITE_TEXT",
                 "MONOTONIC", "ENVIRONMENT", "ARGUMENTS", "FLAGS")
        old = {name: getattr(synthetic_runner, name) for name in names}
        try:
            synthetic_runner.sha256_path = lambda path: synthetic_runner.MANIFEST_SHA256
            synthetic_runner.LOAD_MANIFEST = lambda: manifest
            synthetic_runner.SNAPSHOT = lambda value: {"state": "same"}
            synthetic_runner.RUN_CHILD = lambda expected, timeout, limit: (0, stdout, b"", "completed")
            synthetic_runner.PATH_EXISTS = lambda path: False
            synthetic_runner.MAKE_DIRECTORY = lambda path: writes.setdefault("mkdir", str(path))
            synthetic_runner.WRITE_BYTES = lambda path, value: writes.setdefault(path.name, value)
            synthetic_runner.WRITE_TEXT = lambda path, value: writes.setdefault(path.name, value)
            ticks = iter((0.0, 1.0))
            synthetic_runner.MONOTONIC = lambda: next(ticks)
            synthetic_runner.ENVIRONMENT = lambda: {}
            synthetic_runner.ARGUMENTS = lambda: [str(synthetic_runner.Path(synthetic_runner.__file__).resolve())]
            synthetic_runner.FLAGS = lambda: SimpleNamespace(isolated=1, dont_write_bytecode=1)
            synthetic_runner.main()
        finally:
            for name, value in old.items(): setattr(synthetic_runner, name, value)
        evidence = json.loads(writes["evidence.json"])
        self.assertEqual(evidence["returncode"], 0)
        self.assertEqual(evidence["passed_test_count"], 49)
        self.assertTrue(all(evidence["audit_self_check"].values()))

    def test_49_repository_basis_and_status_are_behaviorally_checked(self):
        manifest = {"repository_basis": "basis", "presentation_basis": "presentation-head"}
        request = {"soga_head": "package-head", "presentation_head": "presentation-head"}
        base = physical_runner.PACKAGE_PATHS | {"knowledge/strategy/DECISION_LOG.md"}
        cyberpi = physical_runner.CYBERPI_ADDITION_PATHS
        def observe(*, changed=base, additions=(), status=None, presentation="", head="package-head"):
            def fake_command(argv, allowed=(0,)):
                if "status" in argv and str(physical_runner.ROOT) in argv:
                    return 0, "\n".join(physical_runner.EXCLUDED_STATUS if status is None else status)
                if "status" in argv:
                    return 0, presentation
                if "rev-parse" in argv and str(physical_runner.PRESENTATION) in argv:
                    return 0, "presentation-head\n"
                if "rev-parse" in argv:
                    return 0, head + "\n"
                if "diff" in argv:
                    self.assertIn("--no-renames", argv)
                    values = additions if "--diff-filter=A" in argv else changed
                    return 0, "\n".join(sorted(values))
                if "merge-base" in argv:
                    return 0, ""
                raise AssertionError(argv)
            with patch.object(physical_runner, "command", fake_command):
                return physical_runner.repository_observations(manifest, request)
        self.assertEqual(set(observe()["changed_paths"]), base)
        self.assertEqual(set(observe(changed=base | cyberpi, additions=cyberpi)["changed_paths"]), base | cyberpi)
        for overrides, error in (
            ({"status": [" M unrelated"]}, "repository_status_mismatch"),
            ({"presentation": " M bridge.py"}, "repository_status_mismatch"),
            ({"head": "wrong"}, "execution_head_mismatch"),
            ({"changed": base - {physical_runner.PROBE_PATH.relative_to(ROOT).as_posix()}}, "repository_basis_mismatch"),
            ({"changed": base | {"unrelated"}}, "repository_basis_mismatch"),
            ({"changed": base | cyberpi | {"renamed-away"}, "additions": cyberpi}, "repository_basis_mismatch"),
            ({"changed": base | cyberpi, "additions": ()}, "repository_basis_mismatch"),
        ):
            with self.subTest(overrides=overrides), self.assertRaisesRegex(RuntimeError, "^" + error + "$"):
                observe(**overrides)

    def test_50_manifest_verification_returns_all_observed_maps(self):
        manifest = json.loads((ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json").read_text(encoding="utf-8"))
        expected_by_path = {}
        for section, base in (("source_sha256", ROOT), ("accepted_gateway_sha256", ROOT), ("preserved_sha256", ROOT)):
            for relative, expected in manifest[section].items(): expected_by_path[str(base / relative)] = expected
        for relative, expected in manifest["presentation_sha256"].items(): expected_by_path[str(physical_runner.PRESENTATION / relative)] = expected
        for absolute, expected in manifest["accepted_evidence_sha256"].items(): expected_by_path[absolute] = expected
        old = physical_runner.sha256_path
        physical_runner.sha256_path = lambda path: expected_by_path[str(path)]
        try:
            observed = physical_runner.verify_manifest(manifest)
        finally:
            physical_runner.sha256_path = old
        self.assertEqual(observed["source_sha256"], manifest["source_sha256"])
        self.assertEqual(observed["accepted_evidence_sha256"], manifest["accepted_evidence_sha256"])

    def test_51_synthetic_main_writes_failure_evidence_for_timeout(self):
        manifest = json.loads((ROOT / "tools/robot_gateway/misty-stop-only-runtime-manifest.json").read_text(encoding="utf-8"))
        writes = {}
        names = ("sha256_path", "LOAD_MANIFEST", "SNAPSHOT", "RUN_CHILD", "PATH_EXISTS", "MAKE_DIRECTORY", "WRITE_BYTES", "WRITE_TEXT",
                 "MONOTONIC", "ENVIRONMENT", "ARGUMENTS", "FLAGS")
        old = {name: getattr(synthetic_runner, name) for name in names}
        try:
            synthetic_runner.sha256_path = lambda path: synthetic_runner.MANIFEST_SHA256
            synthetic_runner.LOAD_MANIFEST = lambda: manifest
            synthetic_runner.SNAPSHOT = lambda value: {"state": "same"}
            synthetic_runner.RUN_CHILD = lambda expected, timeout, limit: (None, b"partial", b"", "timeout")
            synthetic_runner.PATH_EXISTS = lambda path: False
            synthetic_runner.MAKE_DIRECTORY = lambda path: None
            synthetic_runner.WRITE_BYTES = lambda path, value: writes.setdefault(path.name, value)
            synthetic_runner.WRITE_TEXT = lambda path, value: writes.setdefault(path.name, value)
            ticks = iter((0.0, 1.0))
            synthetic_runner.MONOTONIC = lambda: next(ticks)
            synthetic_runner.ENVIRONMENT = lambda: {}
            synthetic_runner.ARGUMENTS = lambda: [str(synthetic_runner.Path(synthetic_runner.__file__).resolve())]
            synthetic_runner.FLAGS = lambda: SimpleNamespace(isolated=1, dont_write_bytecode=1)
            with self.assertRaises(RuntimeError):
                synthetic_runner.main()
        finally:
            for name, value in old.items(): setattr(synthetic_runner, name, value)
        evidence = json.loads(writes["evidence.json"])
        self.assertEqual(evidence["outcome"], "timeout")
        self.assertEqual(evidence["returncode"], None)


    def test_52_live_interface_and_listener_refusals(self):
        baseline = {
            "/usr/sbin/ipconfig": (0, "192.168.8.247"),
            "/sbin/ifconfig": (0, "inet 192.168.8.247 netmask 0xffffff00"),
            "/sbin/route": (0, "route to: 192.168.8.219\ndestination: 192.168.8.219\ninterface: en0\nflags: <UP,HOST>"),
            "/usr/sbin/lsof": (1, ""),
        }
        for binary, result, error in (
            ("/usr/sbin/ipconfig", (0, "192.168.8.1"), "interface_mismatch"),
            ("/sbin/ifconfig", (0, "inet 192.168.8.1"), "interface_mismatch"),
            ("/usr/sbin/lsof", (0, ""), "listener_present"),
            ("/usr/sbin/lsof", (1, "listener"), "listener_present"),
        ):
            responses = baseline | {binary: result}
            with self.subTest(binary=binary, result=result):
                with patch.object(physical_runner, "command", lambda argv, allowed=(0,): responses[argv[0]]):
                    with self.assertRaisesRegex(RuntimeError, "^" + error + "$"):
                        physical_runner.live_observations()

    def test_53_readiness_recheck_and_existing_evidence_refuse_before_mkdir(self):
        runner = physical_runner
        manifest = json.loads(runner.MANIFEST_PATH.read_text(encoding="utf-8"))
        good_live = {"invariant": {"value": "same"}}
        for repo_changes, live_changes, exists, error in (
            (True, False, False, "hold_changed_before_consumption"),
            (False, True, False, "hold_changed_before_consumption"),
            (False, False, True, "evidence_directory_must_be_absent"),
        ):
            with self.subTest(repo_changes=repo_changes, live_changes=live_changes, exists=exists):
                repos = iter(({"head": "same"}, {"head": "changed" if repo_changes else "same"}))
                live = iter((good_live, {"invariant": {"value": "changed"}} if live_changes else good_live))
                with patch.multiple(
                    runner, ENVIRONMENT=lambda: {}, ARGUMENTS=lambda: [str(Path(runner.__file__).resolve())],
                    FLAGS=lambda: SimpleNamespace(isolated=1, dont_write_bytecode=1),
                    sha256_path=lambda path: runner.MANIFEST_SHA256, read_json=lambda path: manifest,
                    verify_manifest=lambda value: {}, verify_records=lambda value: ({}, {}, {}, {}),
                    repository_observations=lambda *args: next(repos), live_observations=lambda: next(live),
                    load_probe=lambda: None, readiness=lambda: None, PATH_EXISTS=lambda path: exists,
                ), patch.object(runner, "MAKE_DIRECTORY", side_effect=AssertionError("mkdir reached")) as mkdir:
                    with self.assertRaisesRegex(RuntimeError, "^" + error + "$"):
                        runner.main()
                    mkdir.assert_not_called()

    def test_54_bad_environment_and_invocation_refuse_before_file_read(self):
        for runner, reader in ((physical_runner, "read_json"), (synthetic_runner, "LOAD_MANIFEST")):
            correct_argv = [str(Path(runner.__file__).resolve())]
            for env, argv, isolated, no_bytecode, error in (
                ({"HTTP_PROXY": "fake"}, correct_argv, 1, 1, "ambient_environment_refused"),
                ({"GIT_DIR": "fake"}, correct_argv, 1, 1, "ambient_environment_refused"),
                ({}, correct_argv + ["extra"], 1, 1, "invocation_mismatch"),
                ({}, correct_argv, 0, 1, "invocation_mismatch"),
                ({}, correct_argv, 1, 0, "invocation_mismatch"),
            ):
                with self.subTest(runner=runner.__name__, error=error, argv=argv, env=env):
                    with patch.multiple(runner, ENVIRONMENT=lambda: env, ARGUMENTS=lambda: argv,
                                        FLAGS=lambda: SimpleNamespace(isolated=isolated, dont_write_bytecode=no_bytecode)):
                        with patch.object(runner, reader, side_effect=AssertionError("file read reached")) as read:
                            with self.assertRaisesRegex(RuntimeError, "^" + error + "$"):
                                runner.main()
                            read.assert_not_called()

    def test_55_synthetic_immutability_failure_retains_evidence(self):
        runner = synthetic_runner
        manifest = json.loads(runner.MANIFEST.read_text(encoding="utf-8"))
        manifest["synthetic_expected_test_count"] = 1
        states = iter(({"state": "before"}, {"state": "after"}))
        writes = {}
        ticks = iter((0.0, 1.0))
        with patch.multiple(
            runner, sha256_path=lambda path: runner.MANIFEST_SHA256, LOAD_MANIFEST=lambda: manifest,
            SNAPSHOT=lambda value: next(states), RUN_CHILD=lambda *args: (0, b"test ... ok\n", b"", "completed"),
            PATH_EXISTS=lambda path: False, MAKE_DIRECTORY=lambda path: None,
            WRITE_BYTES=lambda path, value: writes.setdefault(path.name, value),
            WRITE_TEXT=lambda path, value: writes.setdefault(path.name, value),
            MONOTONIC=lambda: next(ticks), ENVIRONMENT=lambda: {},
            ARGUMENTS=lambda: [str(Path(runner.__file__).resolve())],
            FLAGS=lambda: SimpleNamespace(isolated=1, dont_write_bytecode=1),
        ):
            with self.assertRaisesRegex(RuntimeError, "^synthetic_test_failure$"):
                runner.main()
        evidence = json.loads(writes["evidence.json"])
        self.assertEqual(evidence["before"], {"state": "before"})
        self.assertEqual(evidence["after"], {"state": "after"})
        self.assertEqual(evidence["passed_test_count"], 1)
        self.assertEqual(evidence["returncode"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
