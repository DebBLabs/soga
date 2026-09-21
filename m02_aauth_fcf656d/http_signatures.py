"""Bounded AAuth HTTP Message Signature profile for in-memory requests.

A later transport adapter must implement RFC 9421 repeated-field combination;
this in-memory model deliberately rejects duplicate normalized header names.
"""

import hashlib
import time
from dataclasses import dataclass

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from . import jose, profile
from .structured_fields import (
    InnerList, Item, StructuredFieldError, Token, parse_dictionary,
    serialize_dictionary, serialize_item, serialize_member,
)


class SignatureProfileError(ValueError):
    def __init__(self, code, message, required_input=()):
        if code not in profile.SIGNATURE_ERROR_CODES:
            raise ValueError("unsupported signature error code")
        super().__init__(message)
        self.code = code
        self.required_input = tuple(required_input)


@dataclass(frozen=True)
class Request:
    method: str
    authority: str
    path: str
    headers: dict
    body: bytes = b""

    def normalized(self):
        if not isinstance(self.method, str) or not self.method:
            raise SignatureProfileError("invalid_input", "method is required")
        if not isinstance(self.authority, str) or not self.authority:
            raise SignatureProfileError("invalid_input", "authority is required")
        if not isinstance(self.path, str) or not self.path.startswith("/"):
            raise SignatureProfileError("invalid_input", "absolute path is required")
        if not isinstance(self.body, bytes) or len(self.body) > profile.MAX_BODY_BYTES:
            raise SignatureProfileError("invalid_input", "body exceeds limit")
        lowered = {}
        for name, value in self.headers.items():
            key = name.lower()
            if key in lowered or not isinstance(value, str):
                raise SignatureProfileError("invalid_input", "duplicate or invalid header")
            lowered[key] = value.strip()
        return Request(self.method.upper(), self.authority.lower(), self.path, lowered, self.body)


class ReplayCache:
    def __init__(self, maximum=1024):
        if maximum < 1:
            raise ValueError("maximum must be positive")
        self.maximum = maximum
        self._entries = {}

    def consume(self, key, now):
        floor = now - profile.FRESHNESS_SECONDS
        self._entries = {item: created for item, created in self._entries.items() if created >= floor}
        if key in self._entries:
            raise SignatureProfileError("invalid_signature", "replayed signature")
        if len(self._entries) >= self.maximum:
            raise SignatureProfileError("invalid_signature", "replay cache is full")
        self._entries[key] = now


def content_digest(body):
    return serialize_dictionary((("sha-256", Item(hashlib.sha256(body).digest())),))


def verify_content_digest(value, body):
    try:
        members = parse_dictionary(value)
    except StructuredFieldError as error:
        raise SignatureProfileError("invalid_input", str(error))
    matches = [member for key, member in members if key == "sha-256"]
    if len(matches) != 1 or not isinstance(matches[0], Item) or not isinstance(matches[0].value, bytes):
        raise SignatureProfileError("invalid_input", "required sha-256 digest missing")
    if matches[0].value != hashlib.sha256(body).digest():
        raise SignatureProfileError("invalid_input", "content digest mismatch")


def signature_key_header(assertion, label=profile.SIGNATURE_LABEL):
    if not isinstance(assertion, str) or not assertion:
        raise SignatureProfileError("invalid_input", "JWT assertion is required")
    return serialize_dictionary(((label, Item(Token("jwt"), (("jwt", assertion),))),))


def _signature_parameters(components, created):
    items = tuple(Item(component) for component in components)
    return InnerList(items, (("created", created),))


def _component_value(request, component):
    if component == "@method":
        return request.method
    if component == "@authority":
        return request.authority
    if component == "@path":
        return request.path
    if component not in request.headers:
        raise SignatureProfileError("required_input", "covered header absent", (component,))
    return request.headers[component]


def _signature_base(request, components, parameters):
    lines = []
    for component in components:
        lines.append(serialize_item(Item(component)) + ": " + _component_value(request, component))
    lines.append('"@signature-params": ' + serialize_member(parameters))
    return "\n".join(lines).encode("utf-8")


def sign_request(request, assertion, private_key, created=None, body_request=False):
    request = request.normalized()
    now = int(time.time()) if created is None else created
    if not isinstance(now, int):
        raise SignatureProfileError("invalid_input", "created must be an integer")
    headers = dict(request.headers)
    headers["signature-key"] = signature_key_header(assertion)
    components = profile.BASE_COMPONENTS
    if body_request:
        if not request.body:
            raise SignatureProfileError("required_input", "body is required")
        headers["content-digest"] = content_digest(request.body)
        if "content-type" not in headers:
            raise SignatureProfileError("required_input", "content-type is required", ("content-type",))
        components += profile.BODY_COMPONENTS
    signed_request = Request(request.method, request.authority, request.path, headers, request.body)
    parameters = _signature_parameters(components, now)
    signature_input = serialize_dictionary(((profile.SIGNATURE_LABEL, parameters),))
    signature = private_key.sign(_signature_base(signed_request, components, parameters))
    headers["signature-input"] = signature_input
    headers["signature"] = serialize_dictionary(((profile.SIGNATURE_LABEL, Item(signature)),))
    return Request(request.method, request.authority, request.path, headers, request.body)


def _single_member(header, label):
    try:
        members = parse_dictionary(header)
    except StructuredFieldError as error:
        raise SignatureProfileError("invalid_input", str(error))
    matches = [member for key, member in members if key == label]
    if len(matches) != 1:
        raise SignatureProfileError("invalid_input", "signature label missing or ambiguous")
    return matches[0]


def _only_labeled_member(header):
    try:
        members = parse_dictionary(header)
    except StructuredFieldError as error:
        raise SignatureProfileError("invalid_input", str(error))
    if len(members) != 1:
        raise SignatureProfileError("invalid_input", "exactly one signature label is required")
    return members[0]


def _signature_key_assertion(value, label):
    member = _single_member(value, label)
    if not isinstance(member, Item) or not isinstance(member.value, Token):
        raise SignatureProfileError("invalid_input", "invalid signature-key member")
    if member.value.value != profile.SIGNATURE_SCHEME:
        raise SignatureProfileError("unsupported_scheme", "unsupported signature scheme")
    parameters = dict(member.parameters)
    if set(parameters) != {"jwt"} or not isinstance(parameters["jwt"], str):
        raise SignatureProfileError("invalid_input", "invalid jwt scheme parameters")
    return parameters["jwt"]


def verify_request(request, issuer_jwks, expected_token_typ, now=None, replay_cache=None,
                   body_request=False):
    request = request.normalized()
    clock = int(time.time()) if now is None else now
    required_headers = ("signature-key", "signature-input", "signature")
    if any(name not in request.headers for name in required_headers):
        raise SignatureProfileError("invalid_signature", "signature headers required")
    label, parameters = _only_labeled_member(request.headers["signature-input"])
    assertion = _signature_key_assertion(request.headers["signature-key"], label)
    try:
        claims = jose.verify_compact(assertion, expected_token_typ, issuer_jwks)
    except jose.JoseError as error:
        raise SignatureProfileError("invalid_signature", str(error))
    confirmation = claims.get("cnf") if isinstance(claims, dict) else None
    signing_jwk = confirmation.get("jwk") if isinstance(confirmation, dict) else None
    try:
        raw_key = jose.validate_public_jwk(signing_jwk)
        thumbprint = jose.jwk_thumbprint(signing_jwk)
    except jose.JoseError as error:
        raise SignatureProfileError("invalid_signature", str(error))

    if not isinstance(parameters, InnerList):
        raise SignatureProfileError("invalid_input", "signature-input must be an inner list")
    components = tuple(item.value for item in parameters.items)
    if any(not isinstance(value, str) for value in components) or len(set(components)) != len(components):
        raise SignatureProfileError("invalid_input", "invalid or duplicate covered component")
    required = profile.BASE_COMPONENTS + (profile.BODY_COMPONENTS if body_request else ())
    missing = tuple(component for component in required if component not in components)
    if missing:
        raise SignatureProfileError("required_input", "required components missing", missing)
    parameters_map = dict(parameters.parameters)
    if any(name not in {"created", "expires", "alg", "keyid"}
           for name in parameters_map):
        raise SignatureProfileError("invalid_input", "unsupported signature parameter")
    created = parameters_map.get("created")
    if not isinstance(created, int):
        raise SignatureProfileError("invalid_signature", "integer created is required")
    if created < clock - profile.FRESHNESS_SECONDS:
        raise SignatureProfileError("invalid_signature", "signature is stale")
    if created > clock + profile.FORWARD_SKEW_SECONDS:
        raise SignatureProfileError("clock_skew", "signature is from the future")
    expires = parameters_map.get("expires")
    if expires is not None and (not isinstance(expires, int) or clock > expires):
        raise SignatureProfileError("invalid_signature", "signature is expired")
    keyid = parameters_map.get("keyid")
    if keyid is not None and keyid != signing_jwk["kid"]:
        raise SignatureProfileError("invalid_signature", "signature keyid mismatch")
    if body_request:
        verify_content_digest(request.headers.get("content-digest", ""), request.body)
        if not request.headers.get("content-type"):
            raise SignatureProfileError("required_input", "content-type is required")

    signature_member = _single_member(request.headers["signature"], label)
    if not isinstance(signature_member, Item) or not isinstance(signature_member.value, bytes):
        raise SignatureProfileError("invalid_signature", "invalid signature value")
    try:
        # Execution holdpoint: D-099 did not exercise from_public_bytes.
        Ed25519PublicKey.from_public_bytes(raw_key).verify(
            signature_member.value, _signature_base(request, components, parameters))
    except InvalidSignature:
        raise SignatureProfileError("invalid_signature", "signature verification failed")
    if replay_cache is not None:
        replay_cache.consume((thumbprint, created, request.method, request.authority, request.path), clock)
    return claims


def signature_error_header(error):
    if not isinstance(error, SignatureProfileError):
        raise TypeError("SignatureProfileError required")
    members = [("error", Item(Token(error.code)))]
    if error.required_input:
        members.append(("required_input", InnerList(tuple(Item(value) for value in error.required_input))))
    return serialize_dictionary(tuple(members))


def parse_signature_error(value):
    try:
        members = dict(parse_dictionary(value))
    except StructuredFieldError as error:
        raise SignatureProfileError("invalid_input", str(error))
    if any(key not in {"error", "required_input"} for key in members):
        raise SignatureProfileError("invalid_input", "unsupported Signature-Error member")
    error_item = members.get("error")
    if (not isinstance(error_item, Item) or not isinstance(error_item.value, Token)
            or error_item.value.value not in profile.SIGNATURE_ERROR_CODES):
        raise SignatureProfileError("invalid_input", "invalid Signature-Error code")
    required = ()
    if "required_input" in members:
        required_member = members["required_input"]
        if (not isinstance(required_member, InnerList) or
                any(not isinstance(item.value, str) for item in required_member.items)):
            raise SignatureProfileError("invalid_input", "invalid required_input")
        required = tuple(item.value for item in required_member.items)
    return error_item.value.value, required
