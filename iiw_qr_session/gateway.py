"""Bounded HTTP codec for the standalone IIW adult-participant fixture."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from typing import Callable

from .package import BindConfiguration, validate_private_ipv4
from .session import (
    ALLOW_DIRECTED_RESPONSE,
    DECLINE_DIRECTED_RESPONSE,
    FIXTURE_ACTION,
    FIXTURE_MISSION,
    FIXTURE_PARTICIPANT,
    ParticipantChoice,
    ParticipantSession,
    SessionUnavailable,
)


MAX_BODY_BYTES = 1024
MAX_HEADER_VALUE_BYTES = 512
PARTICIPANT_PATH = "/participant"
SCRIPT_PATH = "/participant.js"
CHOICE_PATH = "/choice"
SECURITY_HEADERS = {
    "Cache-Control": "no-store",
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; connect-src 'self'; form-action 'none'; frame-ancestors 'none'",
}

_HTML = b"""<!doctype html><html><head><meta charset=utf-8><meta name=viewport content=\"width=device-width,initial-scale=1\"><title>Participant choice</title><style>body{font:18px system-ui;max-width:36rem;margin:3rem auto;padding:1rem}button{display:block;width:100%;margin:1rem 0;padding:1rem}</style></head><body><h1>Participant choice</h1><p>This is an unverified adult demo input. It does not establish identity, consent for another person, parental authority, or legal authority.</p><p>You may choose nothing and leave.</p><button disabled data-choice=\"ALLOW_DIRECTED_RESPONSE\">Allow directed response</button><button disabled data-choice=\"DECLINE_DIRECTED_RESPONSE\">Decline directed response</button><p id=result aria-live=polite></p><script src=\"/participant.js\"></script></body></html>"""

_SCRIPT = b"""'use strict';const cap=location.hash.slice(1);history.replaceState(null,'',location.pathname);const out=document.getElementById('result');const buttons=[...document.querySelectorAll('button')];for(const b of buttons)b.addEventListener('click',async()=>{for(const x of buttons)x.disabled=true;try{const r=await fetch('/choice',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({capability:cap,choice:b.dataset.choice,mission:'iiw-adult-participant-fixture-v1',action:'address_participant',participant:'adult-demo-participant'})});const j=await r.json();out.textContent=j.status}catch(_){out.textContent='session unavailable'}});requestAnimationFrame(()=>requestAnimationFrame(()=>{for(const b of buttons)b.disabled=false}));"""


class GatewayConfigurationError(ValueError):
    pass


class _BoundedThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 4

    def __init__(self, *args, **kwargs):
        self._request_slots = threading.BoundedSemaphore(8)
        super().__init__(*args, **kwargs)

    def process_request(self, request, client_address):
        if not self._request_slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self._request_slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._request_slots.release()


def participant_url(*, literal_ipv4: str, port: int, capability: str) -> str:
    validate_private_ipv4(literal_ipv4)
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise GatewayConfigurationError("port out of range")
    if (not isinstance(capability, str) or len(capability) != 64 or
            any(character not in "0123456789abcdef" for character in capability)):
        raise GatewayConfigurationError("capability format invalid")
    return f"http://{literal_ipv4}:{port}{PARTICIPANT_PATH}#{capability}"


def handler_for(*, session: ParticipantSession,
                gateway_instance: str,
                exact_host: str,
                callback: Callable[[ParticipantChoice], None]):
    """Return a handler class; constructing it does not open a listener."""
    if not callable(callback):
        raise TypeError("synthetic callback required")

    class Handler(BaseHTTPRequestHandler):
        server_version = "IIWParticipantFixture/0"
        protocol_version = "HTTP/1.1"

        def setup(self):
            super().setup()
            self.connection.settimeout(3)

        def log_message(self, _format, *args):
            return

        def do_GET(self):
            if self._has_body_framing() or not self._host_ok():
                self._json(400, "session unavailable", close=True)
            elif self.path == PARTICIPANT_PATH:
                self._write(200, _HTML, "text/html; charset=utf-8",
                            {"Connection": "close"})
                self.close_connection = True
            elif self.path == SCRIPT_PATH:
                self._write(200, _SCRIPT, "text/javascript; charset=utf-8",
                            {"Connection": "close"})
                self.close_connection = True
            else:
                self._json(404, "session unavailable", close=True)

        def do_POST(self):
            if not self._host_ok() or self.path != CHOICE_PATH:
                self._json(404, "session unavailable", close=True)
                return
            content_types = self.headers.get_all("Content-Type", failobj=[])
            lengths = self.headers.get_all("Content-Length", failobj=[])
            transfers = self.headers.get_all("Transfer-Encoding", failobj=[])
            media_type = (content_types[0].split(";", 1)[0].strip().lower()
                          if len(content_types) == 1 else "")
            length = lengths[0] if len(lengths) == 1 else None
            if (transfers or media_type != "application/json" or
                    length is None or not length.isdecimal()):
                self._json(400, "session unavailable", close=True)
                return
            size = int(length)
            if size < 2 or size > MAX_BODY_BYTES:
                self._json(400, "session unavailable", close=True)
                return
            try:
                value = json.loads(self.rfile.read(size).decode("utf-8"))
                if not isinstance(value, dict) or set(value) != {
                    "capability", "choice", "mission", "action", "participant"}:
                    raise ValueError
            except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError):
                self._json(400, "session unavailable", close=True)
                return
            try:
                event = session.submit(
                    capability=value["capability"], choice=value["choice"],
                    mission=value["mission"], action=value["action"],
                    participant=value["participant"],
                    gateway_instance=gateway_instance)
                callback(event)
            except SessionUnavailable:
                self._json(404, "session unavailable", close=True)
                return
            except Exception:
                self._json(500, "session unavailable", close=True)
                return
            self._json(200, "choice recorded", close=True)

        def do_PUT(self):
            self._json(405, "session unavailable", close=True)

        do_DELETE = do_PUT
        do_PATCH = do_PUT
        do_HEAD = do_PUT
        do_OPTIONS = do_PUT
        do_TRACE = do_PUT
        do_CONNECT = do_PUT

        def send_error(self, code, message=None, explain=None):
            self._json(code if 400 <= code < 600 else 400,
                       "session unavailable", close=True)

        def _host_ok(self):
            values = self.headers.get_all("Host", failobj=[])
            return len(values) == 1 and values[0] == exact_host and len(values[0]) <= MAX_HEADER_VALUE_BYTES

        def _has_body_framing(self):
            return bool(self.headers.get_all("Content-Length", failobj=[]) or
                        self.headers.get_all("Transfer-Encoding", failobj=[]))

        def _json(self, status, message, close=False):
            body = json.dumps({"status": message}, separators=(",", ":")).encode("utf-8")
            headers = {"Connection": "close"} if close else {}
            if close:
                self.close_connection = True
            self._write(status, body, "application/json", headers)

        def _write(self, status, body, content_type, headers=None):
            self.send_response(status)
            merged = dict(SECURITY_HEADERS)
            merged.update(headers or {})
            merged["Content-Type"] = content_type
            merged["Content-Length"] = str(len(body))
            for name, value in merged.items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(body)

    return Handler


def server_for(*, configuration: BindConfiguration, port: int, handler_class):
    """Explicit later-execution seam. Caller must complete approved preflight."""
    if not isinstance(configuration, BindConfiguration):
        raise GatewayConfigurationError("validated bind configuration required")
    from .package import validate_bind_configuration
    validate_bind_configuration(
        bind_addresses=[configuration.address],
        interface_addresses=configuration.interface_addresses,
        synthetic_loopback=configuration.synthetic_loopback)
    if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65535:
        raise GatewayConfigurationError("port out of range")
    server = _BoundedThreadingHTTPServer(
        (configuration.address, port), handler_class, bind_and_activate=True)
    return server

