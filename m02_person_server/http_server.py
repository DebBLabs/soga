"""Literal-loopback HTTP surface for the bounded M02 Person Server."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from typing import Any, Mapping, Type

from .service import LocalPersonServer, PersonServerError, TokenRejected


def _require_literal_loopback(host: str) -> None:
    try:
        address = ip_address(host)
    except ValueError as error:
        raise ValueError("server host must be a literal loopback IP") from error
    if not address.is_loopback:
        raise ValueError("server host must be loopback")


def handler_for(service: LocalPersonServer) -> Type[BaseHTTPRequestHandler]:
    class PersonServerHandler(BaseHTTPRequestHandler):
        server_version = "M02LocalPersonServer/0"

        def do_GET(self) -> None:
            if self.path == "/.well-known/aauth-person-server":
                self._json(200, service.metadata())
                return
            if self.path == "/_test/key-metadata":
                try:
                    service.authenticate_operator(self._bearer())
                except TokenRejected as error:
                    self._json(401, {"error": "invalid_token", "detail": str(error)})
                    return
                self._json(200, service.key_document())
                return
            self._json(404, {"error": "not_found"})

        def do_POST(self) -> None:
            try:
                body = self._request_json()
                if self.path == "/permission":
                    status, response = service.permission(
                        request=self._mapping(body, "request"),
                        agent_id=self._text(body, "agent_id"),
                        signature=self._text(body, "signature"),
                        person_token=self._text(body, "person_token"),
                    )
                elif self.path.startswith("/pending/") and self.path.endswith("/poll"):
                    pending_id = self.path.removeprefix("/pending/").removesuffix("/poll")
                    status, response = service.poll_pending(
                        pending_id=pending_id,
                        request=self._mapping(body, "request"),
                        agent_id=self._text(body, "agent_id"),
                        signature=self._text(body, "signature"),
                    )
                else:
                    service.authenticate_operator(self._bearer())
                    status, response = self._operator_post(body)
            except TokenRejected as error:
                self._json(401, {"error": "invalid_token", "detail": str(error)})
                return
            except KeyError as error:
                self._json(404, {"error": "not_found", "detail": str(error)})
                return
            except (PersonServerError, TypeError, ValueError) as error:
                self._json(400, {"error": "invalid_request", "detail": str(error)})
                return
            self._json(status, response)

        def _operator_post(self, body: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
            if self.path == "/_test/agents":
                service.register_test_agent(
                    agent_id=self._text(body, "agent_id"),
                    secret=self._text(body, "secret").encode("utf-8"),
                )
                return 201, {"status": "registered"}
            if self.path == "/_test/missions":
                mission_s256 = self._text(body, "mission_s256")
                service.retain_mission(
                    mission_s256=mission_s256,
                    mission=self._mapping(body, "mission"),
                )
                return 201, {"mission_s256": mission_s256, "status": "retained"}
            if self.path == "/_test/person-token":
                token = service.issue_person_token(
                    subject=self._text(body, "subject"),
                    audience=self._text(body, "audience"),
                    mission_s256=body.get("mission_s256"),
                    confirmation=self._mapping(body, "confirmation"),
                    lifetime_seconds=int(body.get("lifetime_seconds", 300)),
                )
                return 201, {"person_token": token}
            if self.path == "/_test/tokens/revoke":
                changed = service.revoke_person_token(
                    token_id=self._text(body, "token_id"),
                    reason=self._text(body, "reason"),
                )
                return 200, {"status": "revoked", "changed": changed}
            if self.path.startswith("/_test/pending/") and self.path.endswith("/approval"):
                pending_id = self.path.removeprefix("/_test/pending/").removesuffix(
                    "/approval"
                )
                return service.resolve_pending(
                    pending_id=pending_id,
                    result=self._text(body, "result"),
                    approval_evidence=body.get("approval_evidence"),
                )
            raise KeyError(self.path)

        def _request_json(self) -> Mapping[str, Any]:
            content_type = self.headers.get("Content-Type", "")
            if content_type.split(";", 1)[0].strip().lower() != "application/json":
                raise ValueError("Content-Type must be application/json")
            raw_length = self.headers.get("Content-Length")
            if raw_length is None:
                raise ValueError("Content-Length is required")
            length = int(raw_length)
            if length < 0 or length > 1_000_000:
                raise ValueError("request body length is invalid")
            value = json.loads(self.rfile.read(length))
            if not isinstance(value, dict):
                raise ValueError("request body must be a JSON object")
            return value

        def _bearer(self) -> str:
            authorization = self.headers.get("Authorization", "")
            scheme, separator, value = authorization.partition(" ")
            if not separator or scheme.lower() != "bearer" or not value:
                raise TokenRejected("operator bearer credential is required")
            return value

        @staticmethod
        def _text(body: Mapping[str, Any], name: str) -> str:
            value = body.get(name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{name} must be a non-empty string")
            return value

        @staticmethod
        def _mapping(body: Mapping[str, Any], name: str) -> Mapping[str, Any]:
            value = body.get(name)
            if not isinstance(value, dict):
                raise ValueError(f"{name} must be an object")
            return value

        def _json(self, status: int, value: Mapping[str, Any]) -> None:
            body = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return PersonServerHandler


def create_server(
    service: LocalPersonServer,
    *,
    host: str = "127.0.0.1",
    port: int = 0,
) -> ThreadingHTTPServer:
    _require_literal_loopback(host)
    return ThreadingHTTPServer((host, port), handler_for(service))
