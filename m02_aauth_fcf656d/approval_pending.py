"""Additive AAuth approval-pending lifecycle for a resource-held invocation."""

import hashlib
import http.client
import json
import re
import secrets
import threading
from dataclasses import dataclass

from . import jose, profile
from .exchange import ExchangeError, _json_body, request_token
from .http_signatures import (
    Request, SignatureProfileError, sign_request, signature_error_header,
    verify_request,
)
from .localhost import (
    MAX_HTTP_BYTES, LocalhostProfileError, TransportMap, _challenge,
    _handler_for, _role_host,
)
from .other_party_approval import (
    AMBIENT_SCOPE, DIRECTED_SCOPE, ApprovalGovernedResource,
    OtherPartyApprovalError, OtherPartyApprovalPolicy,
    OtherPartyApprovalReceipt, _action_candidate,
)
from .tokens import (
    TokenProfileError, issue_resource_token, verify_auth_token,
    verify_person_token,
)


PENDING_PREFIX = "/pending/"
PENDING_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{32}\Z")
PENDING_LIFETIME_SECONDS = 120
MAX_PENDING_RECORDS = 32
MAX_REPLAY_ENTRIES = 1024
SIGNATURE_HEADER_LIMIT = 16_384
RETRY_AFTER_SECONDS = 0
SIGNATURE_HEADERS = ("signature-key", "signature-input", "signature")
BODY_FRAMING_HEADERS = ("content-length", "content-type", "transfer-encoding")


class ApprovalPendingError(ValueError):
    pass


class _PendingReplayCache:
    def __init__(self, lock):
        self._lock = lock
        self._entries = {}

    def consume(self, key, now):
        with self._lock:
            floor = now - profile.FRESHNESS_SECONDS
            self._entries = {
                item: observed for item, observed in self._entries.items()
                if observed >= floor
            }
            if key in self._entries:
                raise SignatureProfileError("invalid_signature", "replayed signature")
            if len(self._entries) >= MAX_REPLAY_ENTRIES:
                raise SignatureProfileError("invalid_signature", "replay cache is full")
            self._entries[key] = now

    def discard_path(self, path):
        with self._lock:
            self._entries = {
                key: observed for key, observed in self._entries.items()
                if key[-1] != path
            }


@dataclass
class _PendingRecord:
    pending_id: str
    path: str
    token_digest: str
    token_jti: str
    agent_jkt: str
    subject: str
    participant: str
    mission_s256: str
    scope: str
    action_body: bytes
    created_at: int
    expires_at: int
    receipt: object = None
    terminal: bool = False


class ApprovalPendingStore:
    def __init__(self, *, clock, id_factory=None):
        if not callable(clock) or (id_factory is not None and not callable(id_factory)):
            raise ApprovalPendingError("clock and identifier factory must be callable")
        self.clock = clock
        self.id_factory = id_factory or (lambda: secrets.token_urlsafe(24))
        self._lock = threading.RLock()
        self._records = {}
        self._replay = _PendingReplayCache(self._lock)

    @property
    def count(self):
        with self._lock:
            return len([record for record in self._records.values()
                        if not record.terminal and record.expires_at > self.clock()])

    def create(self, *, token, claims, participant, mission_s256, scope, action_body):
        now = self.clock()
        if (type(now) is not int or not isinstance(token, str) or not token or
                not isinstance(claims, dict) or not isinstance(action_body, bytes)):
            raise ApprovalPendingError("exact pending inputs are required")
        auth_expiry = claims.get("exp")
        if type(auth_expiry) is not int or now + PENDING_LIFETIME_SECONDS >= auth_expiry:
            raise ApprovalPendingError("insufficient auth-token lifetime")
        with self._lock:
            live = sum(not item.terminal and item.expires_at > now
                       for item in self._records.values())
            if live >= MAX_PENDING_RECORDS:
                raise OverflowError("pending capacity reached")
            pending_id = self.id_factory()
            if (not isinstance(pending_id, str) or
                    PENDING_ID_PATTERN.fullmatch(pending_id) is None or
                    pending_id in self._records):
                raise ApprovalPendingError("unsafe or duplicate pending identifier")
            path = PENDING_PREFIX + pending_id
            record = _PendingRecord(
                pending_id=pending_id, path=path,
                token_digest=hashlib.sha256(token.encode("ascii")).hexdigest(),
                token_jti=claims["jti"], agent_jkt=jose.jwk_thumbprint(claims["cnf"]["jwk"]),
                subject=claims["sub"], participant=participant,
                mission_s256=mission_s256, scope=scope, action_body=action_body,
                created_at=now, expires_at=now + PENDING_LIFETIME_SECONDS)
            self._records[pending_id] = record
            return record

    def resolve(self, pending_id, receipt):
        if not isinstance(receipt, OtherPartyApprovalReceipt):
            raise ApprovalPendingError("validated other-party receipt required")
        with self._lock:
            record = self._records.get(pending_id)
            if record is None or record.terminal or record.expires_at <= self.clock():
                raise ApprovalPendingError("live pending record required")
            record.receipt = receipt

    def _record(self, path):
        if not isinstance(path, str) or not path.startswith(PENDING_PREFIX):
            return None
        pending_id = path[len(PENDING_PREFIX):]
        if PENDING_ID_PATTERN.fullmatch(pending_id) is None:
            return None
        return self._records.get(pending_id)

    def poll(self, *, path, request, resource, subject, mission_s256):
        now = self.clock()
        if type(now) is not int:
            raise ApprovalPendingError("integer clock required")
        with self._lock:
            record = self._record(path)
            if record is None:
                return 404, {"error": "not_found"}, {}
        try:
            signature_claims = verify_request(
                request, resource.person_server.jwks, "aa-auth+jwt", now=now,
                replay_cache=self._replay, body_request=False)
            raw_token = request_token(request)
            claims = verify_auth_token(
                raw_token, resource.person_server.jwks,
                issuer=resource.person_server.identifier,
                resource=resource.issuer.identifier,
                ps=resource.person_server.identifier, subject=subject,
                agent_jwk=signature_claims["cnf"]["jwk"],
                mission_s256=mission_s256, required_scope=record.scope, now=now)
        except (SignatureProfileError, TokenProfileError, jose.JoseError, ExchangeError):
            return 404, {"error": "not_found"}, {}
        token_digest = hashlib.sha256(raw_token.encode("ascii")).hexdigest()
        if (token_digest != record.token_digest or claims["jti"] != record.token_jti or
                jose.jwk_thumbprint(claims["cnf"]["jwk"]) != record.agent_jkt):
            return 404, {"error": "not_found"}, {}
        with self._lock:
            current = self._records.get(record.pending_id)
            if current is not record:
                return 404, {"error": "not_found"}, {}
            if record.terminal:
                return 410, {"error": "gone"}, {}
            if now >= record.expires_at:
                record.terminal = True
                self._replay.discard_path(record.path)
                return 408, {"error": "expired"}, {}
            if record.receipt is None:
                return 202, {"status": "pending"}, {
                    "AAuth-Requirement": "requirement=approval",
                    "Location": record.path, "Retry-After": str(RETRY_AFTER_SECONDS),
                }
            decision = OtherPartyApprovalPolicy(record.receipt).evaluate(
                participant=record.participant, mission_s256=record.mission_s256,
                scope=record.scope, now=now)
            record.terminal = True
            self._replay.discard_path(record.path)
            if decision.outcome != "ALLOW":
                return 403, {
                    "authorization": "denied",
                    "reason": "other_party_approval_required",
                    "decision": decision.as_dict(),
                }, {}
            return 200, {
                "authorization": "allowed", "subject": record.subject,
                "mission_s256": record.mission_s256, "scope": record.scope,
                "decision": decision.as_dict(),
            }, {}


class ApprovalPendingSurface:
    metadata_path = "/.well-known/aauth-resource.json"

    def __init__(self, *, resource, subject, mission_s256, store):
        if (not isinstance(resource, ApprovalGovernedResource) or
                not isinstance(store, ApprovalPendingStore)):
            raise ApprovalPendingError("approval resource and pending store required")
        self.resource = resource
        self.subject = subject
        self.mission_s256 = mission_s256
        self.store = store
        self.role_identifier = resource.issuer.identifier
        self.authority = _role_host(self.role_identifier)
        self._person_token = None
        self._resource_token = None

    def metadata(self):
        from .metadata import resource_fixture_metadata
        issuer = self.role_identifier
        return resource_fixture_metadata(issuer, issuer + "/jwks", issuer + "/authorize")

    def post(self, path, request):
        now = self.store.clock()
        if type(now) is not int:
            raise ApprovalPendingError("integer clock required")
        if path == "/authorize":
            person = verify_request(
                request, self.resource.person_server.jwks, "aa-person+jwt",
                now=now, body_request=True)
            person = verify_person_token(
                request_token(request), self.resource.person_server.jwks,
                issuer=self.resource.person_server.identifier,
                resource=self.resource.issuer.identifier,
                agent_jwk=person["cnf"]["jwk"], now=now)
            body = _json_body(request)
            if set(body) != {"scope"}:
                raise ExchangeError("invalid authorization request")
            token = issue_resource_token(
                self.resource.issuer, ps=self.resource.person_server.identifier,
                subject=person["sub"], presented_jti=person["jti"],
                agent_jwk=person["cnf"]["jwk"],
                mission_s256=person["mission_s256"], scope=body["scope"],
                now=now, expires=now + 300, jti="resource-1")
            self._person_token = request_token(request)
            self._resource_token = token
            return 200, {"resource_token": token}, {}
        if path != "/enforce":
            raise KeyError(path)
        body = _action_candidate(request)
        candidate_scope = body["scope"] if body is not None else "invalid-action-scope"
        try:
            signature_claims = verify_request(
                request, self.resource.person_server.jwks, "aa-auth+jwt",
                now=now, body_request=True)
            claims = verify_auth_token(
                request_token(request), self.resource.person_server.jwks,
                issuer=self.resource.person_server.identifier,
                resource=self.resource.issuer.identifier,
                ps=self.resource.person_server.identifier, subject=self.subject,
                agent_jwk=signature_claims["cnf"]["jwk"],
                mission_s256=self.mission_s256,
                required_scope=candidate_scope, now=now)
        except (SignatureProfileError, TokenProfileError, jose.JoseError,
                ExchangeError) as error:
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
        if body is None or candidate_scope not in {AMBIENT_SCOPE, DIRECTED_SCOPE}:
            raise OtherPartyApprovalError("exact action body is required")
        if candidate_scope == AMBIENT_SCOPE:
            return 200, {
                "authorization": "allowed", "subject": claims["sub"],
                "mission_s256": claims["mission_s256"], "scope": claims["scope"],
                "decision": None,
            }, {}
        decision = self.resource.approval_policy.evaluate(
            participant=body["participant"], mission_s256=self.mission_s256,
            scope=candidate_scope, now=now)
        if decision.outcome == "ALLOW":
            return 200, {
                "authorization": "allowed", "subject": claims["sub"],
                "mission_s256": claims["mission_s256"], "scope": claims["scope"],
                "decision": decision.as_dict(),
            }, {}
        try:
            record = self.store.create(
                token=request_token(request), claims=claims,
                participant=body["participant"], mission_s256=self.mission_s256,
                scope=candidate_scope, action_body=request.body)
        except OverflowError:
            return 503, {"error": "temporarily_unavailable"}, {"Retry-After": "1"}
        except ApprovalPendingError:
            return 403, {"error": "approval_window_unavailable"}, {}
        return 202, {"status": "pending"}, {
            "AAuth-Requirement": "requirement=approval",
            "Location": record.path, "Retry-After": str(RETRY_AFTER_SECONDS),
        }

    def get_pending(self, path, request):
        return self.store.poll(
            path=path, request=request, resource=self.resource,
            subject=self.subject, mission_s256=self.mission_s256)


def _poll_request(handler, surface):
    for name in BODY_FRAMING_HEADERS:
        if handler.headers.get_all(name):
            raise LocalhostProfileError("GET body framing is prohibited")
    selected = {}
    total = 0
    for name in SIGNATURE_HEADERS:
        values = handler.headers.get_all(name)
        if values is None or len(values) != 1:
            raise SignatureProfileError("invalid_signature", "exact signature headers required")
        encoded = values[0].encode("utf-8")
        if len(encoded) > SIGNATURE_HEADER_LIMIT:
            raise SignatureProfileError("invalid_input", "signature header too large")
        total += len(encoded)
        selected[name] = values[0]
    if total > MAX_HTTP_BYTES:
        raise SignatureProfileError("invalid_input", "signature headers exceed bound")
    return Request("GET", surface.authority, handler.path, selected, b"")


def create_approval_pending_server(surface, *, host="127.0.0.1", port=0):
    if (not isinstance(surface, ApprovalPendingSurface) or host != "127.0.0.1" or
            type(port) is not int or port < 0 or port > 65535):
        raise LocalhostProfileError("bounded approval-pending server required")
    base_handler = _handler_for(surface)

    class Handler(base_handler):
        def do_GET(self):
            if self.path == surface.metadata_path:
                return super().do_GET()
            try:
                request = _poll_request(self, surface)
                status, body, headers = surface.get_pending(self.path, request)
            except SignatureProfileError as error:
                status, body = 401, {"error": "signature_error"}
                headers = {"Signature-Error": signature_error_header(error)}
            except (LocalhostProfileError, TypeError, ValueError):
                status, body, headers = 400, {"error": "invalid_request"}, {}
            except Exception:
                status, body, headers = 500, {"error": "internal_error"}, {}
            if status >= 400:
                self.close_connection = True
                headers = {**headers, "Connection": "close"}
            self._write(status, body, headers)

    from http.server import ThreadingHTTPServer
    return ThreadingHTTPServer((host, port), Handler)


def signed_poll(authority, path, assertion, private_key, created):
    return sign_request(
        Request("GET", authority, path, {}, b""), assertion, private_key,
        created=created, body_request=False)


class ApprovalPendingClient:
    def __init__(self, transport_map, *, timeout=2):
        if not isinstance(transport_map, TransportMap) or timeout != 2:
            raise LocalhostProfileError("bounded transport map and timeout required")
        self.transport_map = transport_map
        self.timeout = timeout

    def poll(self, *, role, path, request):
        if (request.method != "GET" or request.path != path or request.body != b"" or
                request.authority != self.transport_map.authority(role)):
            raise LocalhostProfileError("exact signed GET target required")
        if set(request.headers) != set(SIGNATURE_HEADERS):
            raise LocalhostProfileError("exact signed GET headers required")
        host, port = self.transport_map.destination(role)
        connection = http.client.HTTPConnection(host, port, timeout=self.timeout)
        try:
            connection.request("GET", path, headers={
                "Signature-Key": request.headers["signature-key"],
                "Signature-Input": request.headers["signature-input"],
                "Signature": request.headers["signature"],
            })
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
