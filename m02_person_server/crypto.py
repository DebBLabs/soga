"""Test-only compact token signing for the bounded localhost Person Server.

This module deliberately uses a shared-secret HMAC key from Python's standard
library.  It is suitable for exercising signed-message verification between
local test components; it is not an AAuth-conformant or production key system.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from typing import Any, Mapping


def canonical_json(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.b64decode(
            value + padding,
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, base64.binascii.Error) as error:
        raise ValueError("invalid base64url value") from error


def encode_hs256(
    claims: Mapping[str, Any],
    *,
    key_id: str,
    secret: bytes,
) -> str:
    header = {"alg": "HS256", "kid": key_id, "typ": "JWT"}
    encoded_header = b64url_encode(canonical_json(header))
    encoded_claims = b64url_encode(canonical_json(claims))
    signing_input = f"{encoded_header}.{encoded_claims}".encode("ascii")
    signature = hmac.new(secret, signing_input, hashlib.sha256).digest()
    return f"{encoded_header}.{encoded_claims}.{b64url_encode(signature)}"


def decode_and_verify_hs256(
    token: str,
    *,
    secret_for_key_id,
) -> tuple[dict[str, Any], dict[str, Any]]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("token must contain three compact parts")
    encoded_header, encoded_claims, encoded_signature = parts
    try:
        header = json.loads(b64url_decode(encoded_header))
        claims = json.loads(b64url_decode(encoded_claims))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("token contains invalid JSON") from error
    if not isinstance(header, dict) or not isinstance(claims, dict):
        raise ValueError("token header and claims must be objects")
    if header.get("alg") != "HS256" or header.get("typ") != "JWT":
        raise ValueError("unsupported token header")
    key_id = header.get("kid")
    if not isinstance(key_id, str) or not key_id:
        raise ValueError("token has no key identifier")
    secret = secret_for_key_id(key_id)
    signing_input = f"{encoded_header}.{encoded_claims}".encode("ascii")
    expected = hmac.new(secret, signing_input, hashlib.sha256).digest()
    supplied = b64url_decode(encoded_signature)
    if not hmac.compare_digest(supplied, expected):
        raise ValueError("token signature is invalid")
    return header, claims


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("ascii")).hexdigest()
