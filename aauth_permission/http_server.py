from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Type

from .service import PermissionService


def handler_for(service: PermissionService) -> Type[BaseHTTPRequestHandler]:
    class PermissionHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(length) or b"{}")
            try:
                if self.path == "/permission":
                    status, response = service.permission(request)
                elif self.path.startswith("/pending/") and self.path.endswith("/approval"):
                    pending_id = self.path.removeprefix("/pending/").removesuffix("/approval")
                    status, response = service.record_approval(
                        pending_id,
                        result=request["result"],
                        asserted_by=request["asserted_by"],
                        person_server_authenticated_assertion=(
                            self.headers.get("G26-PS-Assertion") == "authenticated"
                        ),
                        authority_reference=request["authority_reference"],
                        required_evidence=request["required_evidence"],
                        constraint_reference=request["constraint_reference"],
                        holder_attribution_asserted=request["holder_attribution_asserted"],
                        human_attribution=request.get("human_attribution"),
                    )
                else:
                    self._json(404, {"error": "not_found"})
                    return
            except PermissionError as error:
                self._json(403, {"error": "denied", "detail": str(error)}, problem=True)
                return
            except (KeyError, TypeError, ValueError) as error:
                self._json(400, {"error": "invalid_request", "detail": str(error)}, problem=True)
                return
            self._json(status, response)

        def do_GET(self) -> None:
            if not self.path.startswith("/pending/"):
                self._json(404, {"error": "not_found"})
                return
            pending_id = self.path.removeprefix("/pending/")
            try:
                status, response = service.poll(
                    pending_id, agent=self.headers.get("AAuth-Agent", "")
                )
            except PermissionError:
                self._json(404, {"error": "invalid_code"}, problem=True)
                return
            except KeyError:
                self._json(404, {"error": "unknown_pending_request"}, problem=True)
                return
            self._json(status, response, problem=status >= 400)

        def _json(self, status: int, value: dict, *, problem: bool = False) -> None:
            body = json.dumps(value).encode("utf-8")
            self.send_response(status)
            self.send_header(
                "Content-Type",
                "application/problem+json" if problem else "application/json",
            )
            if status == 202:
                self.send_header("AAuth-Requirement", "requirement=approval")
                self.send_header("Location", value["pending_url"])
                self.send_header("Retry-After", str(service.retry_after_seconds))
                self.send_header("Cache-Control", "no-store")
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
