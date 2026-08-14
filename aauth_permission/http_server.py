from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Type

from .service import PermissionService


def handler_for(service: PermissionService) -> Type[BaseHTTPRequestHandler]:
    class PermissionHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            if self.path != "/permission":
                self._json(404, {"error": "not_found"})
                return
            length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(length) or b"{}")
            try:
                status, response = service.permission(request)
            except (KeyError, TypeError, ValueError) as error:
                self._json(400, {"error": "invalid_request", "detail": str(error)})
                return
            self._json(status, response)

        def do_GET(self) -> None:
            if not self.path.startswith("/pending/"):
                self._json(404, {"error": "not_found"})
                return
            pending_id = self.path.removeprefix("/pending/")
            try:
                status, response = service.poll(pending_id)
            except KeyError:
                self._json(404, {"error": "unknown_pending_request"})
                return
            self._json(status, response)

        def _json(self, status: int, value: dict) -> None:
            body = json.dumps(value).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args) -> None:
            return

    return PermissionHandler


def create_server(
    service: PermissionService, host: str = "127.0.0.1", port: int = 0
) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), handler_for(service))
