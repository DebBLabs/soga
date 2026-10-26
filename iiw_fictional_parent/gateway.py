"""Bounded HTTP transport for the fictional-parent role-play profile."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading

from iiw_qr_session.package import BindConfiguration, validate_bind_configuration

from .connection import FictionalParentConnectionUnavailable
from .session import (
    ACTION_LABEL, PARTICIPANT, ROLEPLAY, SCENARIO,
    FictionalParentSessionUnavailable,
)


PARTICIPANT_PATH = "/fictional-parent"
SCRIPT_PATH = "/fictional-parent.js"
CHOICE_PATH = "/fictional-parent-choice"
MAX_BODY_BYTES = 1024
MAX_HEADER_VALUE_BYTES = 512
SECURITY_HEADERS = {
    "Cache-Control": "no-store",
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": (
        "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; "
        "connect-src 'self'; form-action 'none'; frame-ancestors 'none'"),
}

DISCLOSURE = (
    "You are an adult participating in a fictional demonstration. You are "
    "role-playing the parent of a fictional child. This does not verify your "
    "identity, establish any real relationship or legal authority, or record "
    "consent for a real person."
)
SOURCE_DISCLOSURE = (
    "The system label local-operator-demo-control names the local software "
    "path carrying your choice. It does not identify or authenticate you and "
    "does not mean that the local operator made your choice."
)
SCOPE_DISCLOSURE = (
    "The internal legacy scope misty.address_participant means only a "
    "simulated directed response by the demo resource. No robot acts."
)

_HTML = ("""<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Permission to Speak — fictional parent role-play</title><style>body{font:18px system-ui;max-width:36rem;margin:3rem auto;padding:1rem}button{display:block;width:100%%;margin:1rem 0;padding:1rem}</style></head><body><h1>Permission to Speak</h1><p>%s</p><p>%s</p><p>%s</p><p>You may choose nothing and leave.</p><button disabled data-choice="APPROVE_FICTIONAL_DIRECTED_RESPONSE">Approve the directed response in this fictional scenario</button><button disabled data-choice="DECLINE_FICTIONAL_DIRECTED_RESPONSE">Decline the directed response in this fictional scenario</button><p id=result aria-live=polite></p><script src="%s"></script></body></html>""" %
         (DISCLOSURE, SOURCE_DISCLOSURE, SCOPE_DISCLOSURE, SCRIPT_PATH)).encode("utf-8")

_SCRIPT = ("""'use strict';const cap=location.hash.slice(1);history.replaceState(null,'',location.pathname);const out=document.getElementById('result');const buttons=[...document.querySelectorAll('button')];for(const b of buttons)b.addEventListener('click',async()=>{for(const x of buttons)x.disabled=true;try{const r=await fetch('%s',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({capability:cap,choice:b.dataset.choice,scenario:'%s',action:'%s',participant:'%s',roleplay:'%s'})});const j=await r.json();out.textContent=j.status}catch(_){out.textContent='session unavailable'}});requestAnimationFrame(()=>requestAnimationFrame(()=>{for(const b of buttons)b.disabled=false}));""" %
           (CHOICE_PATH, SCENARIO, ACTION_LABEL, PARTICIPANT, ROLEPLAY)).encode("utf-8")


class FictionalParentGatewayError(ValueError):
    pass


class _BoundedServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 4

    def __init__(self, *args, **kwargs):
        self._slots = threading.BoundedSemaphore(8)
        super().__init__(*args, **kwargs)

    def process_request(self, request, client_address):
        if not self._slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self._slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._slots.release()


def participant_url(*, literal_ipv4, port, capability):
    from iiw_qr_session.package import validate_private_ipv4
    validate_private_ipv4(literal_ipv4)
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise FictionalParentGatewayError("port out of range")
    if (not isinstance(capability, str) or len(capability) != 64 or
            any(value not in "0123456789abcdef" for value in capability)):
        raise FictionalParentGatewayError("capability format invalid")
    return "http://%s:%d%s#%s" % (
        literal_ipv4, port, PARTICIPANT_PATH, capability)


def handler_for(*, session, gateway_instance, exact_host, connection):
    if (not callable(getattr(connection, "record", None)) or
            session.clock is not connection.clock or
            session.encounter_started_at != connection.encounter_started_at or
            not isinstance(exact_host, str) or not exact_host or
            len(exact_host) > MAX_HEADER_VALUE_BYTES):
        raise TypeError("fictional-parent connection required")

    class Handler(BaseHTTPRequestHandler):
        server_version = "IIWFictionalParent/0"
        protocol_version = "HTTP/1.1"

        def setup(self):
            super().setup()
            self.connection.settimeout(3)

        def log_message(self, _format, *args):
            return

        def do_GET(self):
            if self._has_body() or not self._host_ok():
                return self._json(400, "session unavailable", close=True)
            if self.path == PARTICIPANT_PATH:
                return self._write(200, _HTML, "text/html; charset=utf-8", close=True)
            if self.path == SCRIPT_PATH:
                return self._write(200, _SCRIPT, "text/javascript; charset=utf-8", close=True)
            return self._json(404, "session unavailable", close=True)

        def do_POST(self):
            if not self._host_ok() or self.path != CHOICE_PATH:
                return self._json(404, "session unavailable", close=True)
            content_types = self.headers.get_all("Content-Type", failobj=[])
            lengths = self.headers.get_all("Content-Length", failobj=[])
            transfers = self.headers.get_all("Transfer-Encoding", failobj=[])
            media = (content_types[0].split(";", 1)[0].strip().lower()
                     if len(content_types) == 1 else "")
            length = lengths[0] if len(lengths) == 1 else None
            if transfers or media != "application/json" or length is None or not length.isdecimal():
                return self._json(400, "session unavailable", close=True)
            size = int(length)
            if not 2 <= size <= MAX_BODY_BYTES:
                return self._json(400, "session unavailable", close=True)
            try:
                value = json.loads(self.rfile.read(size).decode("utf-8"))
                if not isinstance(value, dict) or set(value) != {
                        "capability", "choice", "scenario", "action",
                        "participant", "roleplay"}:
                    raise ValueError
                event = session.submit(
                    capability=value["capability"], choice=value["choice"],
                    scenario=value["scenario"], action=value["action"],
                    participant=value["participant"], roleplay=value["roleplay"],
                    gateway_instance=gateway_instance)
                connection.record(event)
            except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError,
                    FictionalParentSessionUnavailable,
                    FictionalParentConnectionUnavailable):
                return self._json(404, "session unavailable", close=True)
            except Exception:
                return self._json(500, "session unavailable", close=True)
            return self._json(200, "fictional choice recorded", close=True)

        def do_PUT(self):
            return self._json(405, "session unavailable", close=True)

        do_DELETE = do_PUT
        do_PATCH = do_PUT
        do_HEAD = do_PUT
        do_OPTIONS = do_PUT
        do_TRACE = do_PUT
        do_CONNECT = do_PUT

        def send_error(self, code, message=None, explain=None):
            return self._json(code if 400 <= code < 600 else 400,
                              "session unavailable", close=True)

        def _host_ok(self):
            values = self.headers.get_all("Host", failobj=[])
            return (len(values) == 1 and values[0] == exact_host and
                    len(values[0]) <= MAX_HEADER_VALUE_BYTES)

        def _has_body(self):
            return bool(self.headers.get_all("Content-Length", failobj=[]) or
                        self.headers.get_all("Transfer-Encoding", failobj=[]))

        def _json(self, status, value, close=False):
            body = json.dumps({"status": value}, separators=(",", ":")).encode("utf-8")
            return self._write(status, body, "application/json", close=close)

        def _write(self, status, body, content_type, close=False):
            self.send_response(status)
            headers = dict(SECURITY_HEADERS)
            headers.update({"Content-Type": content_type,
                            "Content-Length": str(len(body))})
            if close:
                headers["Connection"] = "close"
                self.close_connection = True
            for name, value in headers.items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(body)

    return Handler


def server_for(*, configuration, port, handler_class):
    if not isinstance(configuration, BindConfiguration):
        raise FictionalParentGatewayError("validated bind configuration required")
    validate_bind_configuration(
        bind_addresses=[configuration.address],
        interface_addresses=configuration.interface_addresses,
        synthetic_loopback=configuration.synthetic_loopback)
    if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65535:
        raise FictionalParentGatewayError("port out of range")
    return _BoundedServer((configuration.address, port), handler_class,
                          bind_and_activate=True)
