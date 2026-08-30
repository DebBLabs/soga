from __future__ import annotations

import json
import time
from copy import deepcopy
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import RLock, Thread
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from .adapter import AdapterError, Invocation
from .lifecycle import LifecycleError, SessionGrantService
from .runtime import ActionRequest, Decision, PrototypeRuntime, RuntimeErrorAtStage
from .state_machine import SafetyStateMachine, StateTransitionError


LOOPBACK_HOST = "127.0.0.1"
MAX_JSON_BYTES = 64 * 1024


class LocalhostTransportError(RuntimeError):
    def __init__(self, stage: str, code: str, status: int | None = None):
        super().__init__(f"{stage}: {code}")
        self.stage = stage
        self.code = code
        self.status = status


def _require_loopback_url(url: str) -> str:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "::1"}
        or parsed.port is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise LocalhostTransportError("transport_configuration", "non_loopback_url")
    return url.rstrip("/")


def _read_json(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    try:
        length = int(handler.headers.get("Content-Length", "0"))
    except ValueError as exc:
        raise LocalhostTransportError("transport_request", "invalid_content_length") from exc
    if length <= 0 or length > MAX_JSON_BYTES:
        raise LocalhostTransportError("transport_request", "invalid_body_size")
    try:
        value = json.loads(handler.rfile.read(length))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LocalhostTransportError("transport_request", "invalid_json") from exc
    if not isinstance(value, dict):
        raise LocalhostTransportError("transport_request", "object_required")
    return value


def _write_json(handler: BaseHTTPRequestHandler, status: int, payload: Mapping[str, Any]) -> None:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _error_payload(exc: Exception) -> tuple[int, dict[str, Any]]:
    if isinstance(exc, (LifecycleError, RuntimeErrorAtStage, AdapterError, LocalhostTransportError)):
        return 409, {"error": {"stage": exc.stage, "code": exc.code}}
    if isinstance(exc, StateTransitionError):
        return 409, {"error": {"stage": "state_gate", "code": str(exc)}}
    return 500, {"error": {"stage": "service", "code": "internal_error"}}


class _QuietHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, _format: str, *_args: object) -> None:
        return


class RecordingService:
    """Loopback HTTP surface that records a target-bound invocation and nothing else."""

    def __init__(self, platform_id: str) -> None:
        self.platform_id = platform_id
        self._lock = RLock()
        self._received: list[dict[str, Any]] = []

    @property
    def received(self) -> tuple[dict[str, Any], ...]:
        with self._lock:
            return tuple(deepcopy(self._received))

    def record(self, payload: dict[str, Any]) -> dict[str, Any]:
        required = (
            "request_id",
            "decision_reference",
            "mission_s256",
            "session_id",
            "platform_id",
            "agent_id",
            "action",
            "catalog_version",
        )
        if any(not payload.get(field) for field in required):
            raise AdapterError("decision_binding", "missing_binding")
        if payload["platform_id"] != self.platform_id:
            raise AdapterError("fake_surface", "wrong_platform")
        with self._lock:
            self._received.append(deepcopy(payload))
        return {
            "request_id": payload["request_id"],
            "platform_id": self.platform_id,
            "adapter_status": "received_by_loopback_recording_surface",
            "physical_outcome": "unknown",
        }


def _recording_handler(service: RecordingService) -> type[_QuietHandler]:
    class Handler(_QuietHandler):
        def do_POST(self) -> None:
            try:
                if self.path != "/invoke":
                    raise LocalhostTransportError("transport_route", "unknown_route")
                _write_json(self, 200, service.record(_read_json(self)))
            except Exception as exc:
                status, payload = _error_payload(exc)
                _write_json(self, status, payload)

        def do_GET(self) -> None:
            if self.path == "/status":
                _write_json(
                    self,
                    200,
                    {
                        "service": "recording_surface",
                        "platform_id": service.platform_id,
                        "receipt_count": len(service.received),
                        "physical_outcome_capability": "unknown_only",
                    },
                )
                return
            _write_json(
                self,
                404,
                {"error": {"stage": "transport_route", "code": "unknown_route"}},
            )

    return Handler


class LoopbackRecordingAdapter:
    """Target-bound adapter whose only transport is validated loopback HTTP."""

    def __init__(self, bindings: Mapping[str, str]) -> None:
        if not bindings:
            raise AdapterError("adapter_configuration", "invalid_binding")
        self._bindings = {key: _require_loopback_url(value) for key, value in bindings.items()}
        self._lock = RLock()
        self._receipts: dict[str, dict[str, Any]] = {}
        self._invocations: dict[str, Invocation] = {}

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, Any]:
        with self._lock:
            prior = self._receipts.get(invocation.request_id)
            if prior is not None:
                if self._invocations[invocation.request_id] != invocation:
                    raise AdapterError("idempotency", "request_binding_conflict")
                return deepcopy(prior)
            if invocation.platform_id != bound_platform_id:
                raise AdapterError("target_binding", "wrong_platform")
            base_url = self._bindings.get(bound_platform_id)
            if base_url is None:
                raise AdapterError("target_resolution", "unavailable_platform")
            try:
                receipt = _json_request(base_url, "/invoke", asdict(invocation))
            except LocalhostTransportError as exc:
                raise AdapterError(exc.stage, exc.code) from exc
            if (
                receipt.get("request_id") != invocation.request_id
                or receipt.get("platform_id") != bound_platform_id
                or receipt.get("physical_outcome") != "unknown"
            ):
                raise AdapterError("adapter_response", "invalid_recording_receipt")
            self._receipts[invocation.request_id] = deepcopy(receipt)
            self._invocations[invocation.request_id] = invocation
            return deepcopy(receipt)


class RuntimeService:
    def __init__(self, recording_services: Mapping[str, RecordingService]) -> None:
        self.sessions = SessionGrantService(monotonic=time.monotonic)
        self.machines = {
            platform_id: SafetyStateMachine(platform_id) for platform_id in recording_services
        }
        self.recording_services = dict(recording_services)
        self.runtime: PrototypeRuntime | None = None
        self._lock = RLock()

    def attach_adapter(self, adapter: LoopbackRecordingAdapter) -> None:
        self.runtime = PrototypeRuntime(
            sessions=self.sessions,
            adapter=adapter,
            state_machines=self.machines,
        )

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self.runtime is None:
            raise LocalhostTransportError("service", "runtime_not_ready")
        with self._lock:
            if path == "/offer":
                platform_id = str(payload.get("platform_id", ""))
                if platform_id not in self.machines:
                    raise RuntimeErrorAtStage("target_resolution", "unknown_platform")
                grant = self.sessions.issue_grant(
                    mission_s256=str(payload.get("mission_s256", "mission-sha")),
                    platform_id=platform_id,
                    notice_version=str(payload.get("notice_version", "notice-v1")),
                    policy_version=str(payload.get("policy_version", "policy-v1")),
                    issuer=str(payload.get("issuer", "person-server")),
                )
                return {
                    "grant_id": grant.grant_id,
                    "mission_s256": grant.mission_s256,
                    "platform_id": grant.platform_id,
                    "notice_version": grant.notice_version,
                    "policy_version": grant.policy_version,
                    "state": grant.state.value,
                }
            if path == "/scan":
                session = self.runtime.initiate_session(
                    str(payload.get("grant_id", "")),
                    platform_id=str(payload.get("platform_id", "")),
                    mission_s256=str(payload.get("mission_s256", "")),
                    notice_version=str(payload.get("notice_version", "")),
                    policy_version=str(payload.get("policy_version", "")),
                    channel_key=str(payload.get("channel_key", "")),
                )
                return {
                    "session_id": session.session_id,
                    "mission_s256": session.mission_s256,
                    "platform_id": session.platform_id,
                    "channel_key": session.channel_key,
                    "state": session.state.value,
                }
            if path == "/request":
                request = ActionRequest(
                    request_id=str(payload.get("request_id", "")),
                    mission_s256=str(payload.get("mission_s256", "")),
                    session_id=str(payload.get("session_id", "")),
                    platform_id=str(payload.get("platform_id", "")),
                    agent_id=str(payload.get("agent_id", "")),
                    action=str(payload.get("action", "")),
                    catalog_version=str(payload.get("catalog_version", "")),
                )
                return self.runtime.begin_request(
                    request, channel_key=str(payload.get("channel_key", ""))
                )
            if path == "/decision":
                try:
                    outcome = Decision(str(payload.get("decision", "")))
                except ValueError as exc:
                    raise RuntimeErrorAtStage("decision_validation", "invalid_decision") from exc
                return self.runtime.resolve_request(
                    session_id=str(payload.get("session_id", "")),
                    request_id=str(payload.get("request_id", "")),
                    decision_reference=str(payload.get("decision_reference", "")),
                    outcome=outcome,
                )
            if path == "/stop":
                self.runtime.safety_stop(str(payload.get("platform_id", "")))
                return {"state": "safety_stopped"}
            raise LocalhostTransportError("transport_route", "unknown_route")

    def snapshot(self) -> dict[str, Any]:
        if self.runtime is None:
            raise LocalhostTransportError("service", "runtime_not_ready")
        with self._lock:
            grants = {
                grant_id: {
                    "platform_id": grant.platform_id,
                    "state": grant.state.value,
                    "session_id": grant.session_id,
                }
                for grant_id, grant in self.sessions.grants.items()
            }
            sessions = {
                session_id: {
                    "platform_id": session.platform_id,
                    "state": session.state.value,
                }
                for session_id, session in self.sessions.sessions.items()
            }
            machines = {
                platform_id: {
                    "state": machine.state.value,
                    "phone_status": machine.phone_status,
                    "safety_latched": machine.safety_latched,
                }
                for platform_id, machine in self.machines.items()
            }
            return {
                "transport": "loopback_http_only",
                "grants": grants,
                "sessions": sessions,
                "machines": machines,
                "pending_request_ids": list(self.runtime.pending_request_ids),
                "fake_receipts": {
                    platform_id: len(service.received)
                    for platform_id, service in self.recording_services.items()
                },
                "events": list(self.runtime.events),
            }


def _runtime_handler(service: RuntimeService) -> type[_QuietHandler]:
    class Handler(_QuietHandler):
        def do_POST(self) -> None:
            try:
                _write_json(self, 200, service.post(self.path, _read_json(self)))
            except Exception as exc:
                status, payload = _error_payload(exc)
                _write_json(self, status, payload)

        def do_GET(self) -> None:
            if self.path == "/status":
                try:
                    _write_json(self, 200, service.snapshot())
                except Exception as exc:
                    status, payload = _error_payload(exc)
                    _write_json(self, status, payload)
                return
            _write_json(
                self,
                404,
                {"error": {"stage": "transport_route", "code": "unknown_route"}},
            )

    return Handler


class GovernanceRelay:
    """Separate delivery surface; it evaluates nothing and forwards one decision."""

    def __init__(self, runtime_url: str) -> None:
        self.runtime_url = _require_loopback_url(runtime_url)

    def deliver(self, payload: dict[str, Any]) -> dict[str, Any]:
        required = ("session_id", "request_id", "decision_reference", "decision")
        if any(not payload.get(field) for field in required):
            raise LocalhostTransportError("decision_validation", "missing_binding")
        return _json_request(self.runtime_url, "/decision", payload)


def _governance_handler(service: GovernanceRelay) -> type[_QuietHandler]:
    class Handler(_QuietHandler):
        def do_POST(self) -> None:
            try:
                if self.path != "/deliver":
                    raise LocalhostTransportError("transport_route", "unknown_route")
                _write_json(self, 200, service.deliver(_read_json(self)))
            except Exception as exc:
                status, payload = _error_payload(exc)
                _write_json(self, status, payload)

    return Handler


def _json_request(base_url: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    base_url = _require_loopback_url(base_url)
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        f"{base_url}{path}",
        data=data,
        method="GET" if payload is None else "POST",
        headers={} if data is None else {"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=3) as response:
            result = json.loads(response.read())
    except HTTPError as exc:
        try:
            result = json.loads(exc.read())
            error = result["error"]
            raise LocalhostTransportError(error["stage"], error["code"], exc.code) from exc
        except (KeyError, json.JSONDecodeError):
            raise LocalhostTransportError("transport_response", "invalid_error", exc.code) from exc
    except (URLError, TimeoutError) as exc:
        raise LocalhostTransportError("transport_connection", "loopback_unavailable") from exc
    except json.JSONDecodeError as exc:
        raise LocalhostTransportError("transport_response", "invalid_json") from exc
    if not isinstance(result, dict):
        raise LocalhostTransportError("transport_response", "object_required")
    return result


class LocalhostClient:
    def __init__(self, runtime_url: str, governance_url: str) -> None:
        self.runtime_url = _require_loopback_url(runtime_url)
        self.governance_url = _require_loopback_url(governance_url)

    def runtime_post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return _json_request(self.runtime_url, path, payload)

    def deliver(self, payload: dict[str, Any]) -> dict[str, Any]:
        return _json_request(self.governance_url, "/deliver", payload)

    def status(self) -> dict[str, Any]:
        return _json_request(self.runtime_url, "/status")


class LocalhostStack:
    def __init__(self) -> None:
        self.recording_services = {
            "misty-a": RecordingService("misty-a"),
            "misty-b": RecordingService("misty-b"),
        }
        self._servers: list[ThreadingHTTPServer] = []
        self._threads: list[Thread] = []

        recording_urls: dict[str, str] = {}
        for platform_id, service in self.recording_services.items():
            server, url = self._start(_recording_handler(service))
            self._servers.append(server)
            recording_urls[platform_id] = url

        self.runtime_service = RuntimeService(self.recording_services)
        self.runtime_service.attach_adapter(LoopbackRecordingAdapter(recording_urls))
        runtime_server, self.runtime_url = self._start(_runtime_handler(self.runtime_service))
        self._servers.append(runtime_server)

        self.governance_relay = GovernanceRelay(self.runtime_url)
        governance_server, self.governance_url = self._start(
            _governance_handler(self.governance_relay)
        )
        self._servers.append(governance_server)
        self.recording_urls = recording_urls
        self.client = LocalhostClient(self.runtime_url, self.governance_url)

    def _start(self, handler: type[_QuietHandler]) -> tuple[ThreadingHTTPServer, str]:
        server = ThreadingHTTPServer((LOOPBACK_HOST, 0), handler)
        server.daemon_threads = True
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self._threads.append(thread)
        host, port = server.server_address
        return server, f"http://{host}:{port}"

    def close(self) -> None:
        for server in reversed(self._servers):
            server.shutdown()
            server.server_close()
        for thread in self._threads:
            thread.join(timeout=2)

    def __enter__(self) -> "LocalhostStack":
        return self

    def __exit__(self, _exc_type: object, _exc: object, _traceback: object) -> None:
        self.close()
