"""Literal-loopback HTTP transport for the bounded AAuth fcf656d profile."""

import http.client
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import MappingProxyType
from urllib.parse import urlsplit

from . import jose
from .exchange import ExchangeError, request_token
from .http_signatures import Request, SignatureProfileError, signature_error_header
from .metadata import person_server_fixture_metadata, resource_fixture_metadata
from .structured_fields import Item, Token, serialize_dictionary
from .tokens import TokenProfileError


MAX_HTTP_BYTES = 64 * 1024
_LOOPBACK = re.compile(r"http://127\.0\.0\.1:([1-9][0-9]{0,4})\Z")


class LocalhostProfileError(ValueError):
    pass


def _role_host(identifier):
    parsed = urlsplit(identifier)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.port is not None or
            parsed.username is not None or parsed.password is not None or
            parsed.path or parsed.query or parsed.fragment or
            identifier != "https://" + parsed.hostname.lower()):
        raise LocalhostProfileError("canonical HTTPS role identifier required")
    return parsed.hostname.lower()


def _transport(value):
    if not isinstance(value, str):
        raise LocalhostProfileError("transport address must be a string")
    match = _LOOPBACK.fullmatch(value)
    if match is None or (len(match.group(1)) > 1 and match.group(1).startswith("0")):
        raise LocalhostProfileError("exact literal-loopback transport address required")
    port = int(match.group(1))
    if not 1 <= port <= 65535:
        raise LocalhostProfileError("transport port is out of range")
    return "127.0.0.1", port


class TransportMap:
    def __init__(self, *, person_server, resource, mappings):
        roles = (person_server, resource)
        if person_server == resource or not isinstance(mappings, dict) or set(mappings) != set(roles):
            raise LocalhostProfileError("exact Person Server and resource mappings required")
        self._hosts = MappingProxyType({role: _transport(mappings[role]) for role in roles})
        self._authorities = MappingProxyType({role: _role_host(role) for role in roles})

    def destination(self, role):
        try:
            return self._hosts[role]
        except KeyError as error:
            raise LocalhostProfileError("unknown transport role") from error

    def authority(self, role):
        try:
            return self._authorities[role]
        except KeyError as error:
            raise LocalhostProfileError("unknown authority role") from error


def _body_json(request):
    try:
        value = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LocalhostProfileError("signed body must be JSON") from error
    if not isinstance(value, dict):
        raise LocalhostProfileError("signed body must be an object")
    return value


def _envelope(request):
    request = request.normalized()
    return {"headers": dict(request.headers), "body": request.body.decode("utf-8")}


def _challenge(resource_token):
    return serialize_dictionary((
        ("requirement", Item(Token("auth-token"), (("resource-token", resource_token),))),
    ))


class _Surface:
    def __init__(self, *, role_identifier):
        self.role_identifier = role_identifier
        self.authority = _role_host(role_identifier)

    def metadata(self):
        raise NotImplementedError

    def post(self, path, request):
        raise NotImplementedError


class PersonServerSurface(_Surface):
    metadata_path = "/.well-known/aauth-person.json"

    def __init__(self, *, person_server):
        super().__init__(role_identifier=person_server.issuer.identifier)
        self.person_server = person_server

    def metadata(self):
        issuer = self.role_identifier
        return person_server_fixture_metadata(
            issuer, issuer + "/jwks", issuer + "/person-token", issuer + "/auth-token")

    def post(self, path, request):
        if path == "/person-token":
            return 200, {"person_token": self.person_server.person_token(request)}, {}
        if path == "/auth-token":
            return 200, {"auth_token": self.person_server.auth_token(request)}, {}
        raise KeyError(path)


class ResourceSurface(_Surface):
    metadata_path = "/.well-known/aauth-resource.json"

    def __init__(self, *, resource, subject, mission_s256, required_scope):
        super().__init__(role_identifier=resource.issuer.identifier)
        self.resource = resource
        self.subject = subject
        self.mission_s256 = mission_s256
        self.required_scope = required_scope
        self._person_token = None
        self._resource_token = None

    def metadata(self):
        issuer = self.role_identifier
        return resource_fixture_metadata(
            issuer, issuer + "/jwks", issuer + "/authorize")

    def post(self, path, request):
        if path == "/authorize":
            token = self.resource.authorize(request)
            self._person_token = request_token(request)
            self._resource_token = token
            return 200, {"resource_token": token}, {}
        if path != "/enforce":
            raise KeyError(path)
        try:
            claims = self.resource.enforce(
                request, subject=self.subject, mission_s256=self.mission_s256,
                required_scope=self.required_scope)
        except (SignatureProfileError, TokenProfileError, jose.JoseError, ExchangeError) as error:
            presented = None
            try:
                presented = request_token(request)
            except Exception:
                pass
            if (self._resource_token is not None and self._person_token is not None and
                    presented == self._person_token):
                return 401, {"error": "auth_token_required"}, {
                    "AAuth-Requirement": _challenge(self._resource_token)}
            raise error
        return 200, {
            "authorization": "allowed", "subject": claims["sub"],
            "mission_s256": claims["mission_s256"], "scope": self.required_scope,
        }, {}


def _handler_for(surface):
    class Handler(BaseHTTPRequestHandler):
        server_version = "M02AAuthLocalhost/0"
        protocol_version = "HTTP/1.1"

        def do_GET(self):
            if self.path == surface.metadata_path:
                self._write(200, surface.metadata(), {})
            else:
                self._write(404, {"error": "not_found"}, {})

        def do_POST(self):
            try:
                request = self._signed_request()
                status, body, headers = surface.post(self.path, request)
            except SignatureProfileError as error:
                status, body = 401, {"error": "signature_error"}
                headers = {"Signature-Error": signature_error_header(error)}
            except TokenProfileError as error:
                status = 403 if str(error) in {
                    "required scope absent", "auth token context mismatch"} else 401
                body, headers = {"error": "not_authorized"}, {}
            except jose.JoseError:
                status, body, headers = 401, {"error": "invalid_token"}, {}
            except ExchangeError:
                status, body, headers = 403, {"error": "not_authorized"}, {}
            except (LocalhostProfileError, TypeError, ValueError, UnicodeDecodeError,
                    json.JSONDecodeError):
                status, body, headers = 400, {"error": "invalid_request"}, {}
            except KeyError:
                status, body, headers = 404, {"error": "not_found"}, {}
            except Exception:
                status, body, headers = 500, {"error": "internal_error"}, {}
            self._write(status, body, headers)

        def do_PUT(self):
            self._write(405, {"error": "method_not_allowed"}, {})

        do_DELETE = do_PUT
        do_PATCH = do_PUT

        def _signed_request(self):
            if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
                raise LocalhostProfileError("application/json required")
            raw_length = self.headers.get("Content-Length")
            if raw_length is None or not raw_length.isdecimal() or raw_length.startswith("+"):
                raise LocalhostProfileError("exact Content-Length required")
            length = int(raw_length)
            if length <= 0 or length > MAX_HTTP_BYTES:
                raise LocalhostProfileError("invalid body length")
            envelope = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(envelope, dict) or set(envelope) != {"headers", "body"}:
                raise LocalhostProfileError("exact signed-request envelope required")
            headers = envelope["headers"]
            body = envelope["body"]
            if (not isinstance(headers, dict) or
                    any(not isinstance(key, str) or not isinstance(value, str)
                        for key, value in headers.items()) or
                    not isinstance(body, str)):
                raise LocalhostProfileError("invalid signed-request envelope")
            encoded = body.encode("utf-8")
            if len(encoded) > MAX_HTTP_BYTES:
                raise LocalhostProfileError("signed body too large")
            return Request(self.command, surface.authority, self.path, headers, encoded)

        def _write(self, status, payload, headers):
            body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            for name, value in headers.items():
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format, *_args):
            return

    return Handler


def create_server(surface, *, host="127.0.0.1", port=0):
    if host != "127.0.0.1" or type(port) is not int or port < 0 or port > 65535:
        raise LocalhostProfileError("literal IPv4 loopback and valid port required")
    return ThreadingHTTPServer((host, port), _handler_for(surface))


class LocalAgentClient:
    def __init__(self, transport_map, *, timeout=2):
        if not isinstance(transport_map, TransportMap) or timeout != 2:
            raise LocalhostProfileError("bounded transport map and timeout required")
        self.transport_map = transport_map
        self.timeout = timeout

    def send(self, *, role, path, request):
        if request.method != "POST" or request.path != path:
            raise LocalhostProfileError("signed request target mismatch")
        if request.authority != self.transport_map.authority(role):
            raise LocalhostProfileError("signed request authority mismatch")
        host, port = self.transport_map.destination(role)
        body = json.dumps(_envelope(request), sort_keys=True,
                          separators=(",", ":")).encode("utf-8")
        if len(body) > MAX_HTTP_BYTES:
            raise LocalhostProfileError("transport body too large")
        connection = http.client.HTTPConnection(host, port, timeout=self.timeout)
        try:
            connection.request("POST", path, body=body,
                               headers={"Content-Type": "application/json",
                                        "Content-Length": str(len(body))})
            response = connection.getresponse()
            raw_length = response.getheader("Content-Length")
            if raw_length is None or not raw_length.isdecimal():
                raise LocalhostProfileError("bounded response length required")
            length = int(raw_length)
            if length < 0 or length > MAX_HTTP_BYTES:
                raise LocalhostProfileError("response too large")
            raw = response.read(length)
            if len(raw) != length:
                raise LocalhostProfileError("truncated response")
            value = json.loads(raw.decode("utf-8"))
            if not isinstance(value, dict):
                raise LocalhostProfileError("response object required")
            return response.status, dict(response.getheaders()), value
        finally:
            connection.close()
