"""Strict Ed25519 compact JWS and public JWKS helpers for AAuth fcf656d."""

import base64
import binascii
import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from . import profile


class JoseError(ValueError):
    pass


_B64U = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")


def _b64u_encode(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64u_decode(value):
    if (not isinstance(value, str) or not value or
            any(character not in _B64U for character in value)):
        raise JoseError("invalid base64url")
    try:
        return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except (ValueError, binascii.Error):
        raise JoseError("invalid base64url")


def _json_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def public_jwk(public_key, kid):
    if not isinstance(kid, str) or not kid:
        raise JoseError("kid is required")
    return {"alg": profile.JOSE_ALGORITHM, "crv": "Ed25519", "kid": kid,
            "kty": "OKP", "x": _b64u_encode(public_key.public_bytes_raw())}


def validate_public_jwk(jwk):
    if not isinstance(jwk, dict):
        raise JoseError("JWK must be an object")
    if "d" in jwk:
        raise JoseError("private JWK material prohibited")
    if set(jwk) != {"alg", "crv", "kid", "kty", "x"}:
        raise JoseError("unexpected JWK members")
    if jwk["alg"] != profile.JOSE_ALGORITHM or jwk["kty"] != "OKP" or jwk["crv"] != "Ed25519":
        raise JoseError("JWK algorithm or key type mismatch")
    if not isinstance(jwk["kid"], str) or not jwk["kid"]:
        raise JoseError("invalid JWK kid")
    raw = _b64u_decode(jwk["x"])
    if len(raw) != 32:
        raise JoseError("invalid Ed25519 public key length")
    return raw


def public_jwks(jwks):
    validated = sorted((dict(jwk) for jwk in jwks), key=lambda item: item.get("kid", ""))
    seen = set()
    for jwk in validated:
        validate_public_jwk(jwk)
        if jwk["kid"] in seen:
            raise JoseError("duplicate kid")
        seen.add(jwk["kid"])
    return {"keys": validated}


def jwk_thumbprint(jwk):
    validate_public_jwk(jwk)
    canonical = _json_bytes({"crv": jwk["crv"], "kty": jwk["kty"], "x": jwk["x"]})
    return _b64u_encode(hashlib.sha256(canonical).digest())


def sign_compact(payload, typ, kid, private_key):
    if typ not in profile.TOKEN_TYPES:
        raise JoseError("unsupported AAuth token type")
    if not isinstance(kid, str) or not kid:
        raise JoseError("kid is required")
    if not isinstance(payload, dict):
        raise JoseError("payload must be an object")
    header = {"alg": profile.JOSE_ALGORITHM, "kid": kid, "typ": typ}
    protected = _b64u_encode(_json_bytes(header))
    encoded_payload = _b64u_encode(_json_bytes(payload))
    signing_input = (protected + "." + encoded_payload).encode("ascii")
    signature = private_key.sign(signing_input)
    return protected + "." + encoded_payload + "." + _b64u_encode(signature)


def verify_compact(token, expected_typ, jwks):
    if expected_typ not in profile.TOKEN_TYPES:
        raise JoseError("unsupported expected token type")
    if not isinstance(token, str) or len(token) > profile.MAX_BODY_BYTES:
        raise JoseError("invalid compact token")
    parts = token.split(".")
    if len(parts) != 3:
        raise JoseError("invalid compact token")
    try:
        header = json.loads(_b64u_decode(parts[0]).decode("utf-8"))
        payload = json.loads(_b64u_decode(parts[1]).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise JoseError("invalid token JSON")
    if not isinstance(header, dict) or set(header) != {"alg", "kid", "typ"}:
        raise JoseError("invalid protected header")
    if header["alg"] != profile.JOSE_ALGORITHM:
        raise JoseError("unsupported token algorithm")
    if header["typ"] != expected_typ:
        raise JoseError("wrong AAuth token type")
    if not isinstance(payload, dict):
        raise JoseError("token payload must be an object")
    keys = jwks.get("keys") if isinstance(jwks, dict) else None
    if not isinstance(keys, list):
        raise JoseError("invalid JWKS")
    matches = [key for key in keys if isinstance(key, dict) and key.get("kid") == header["kid"]]
    if len(matches) != 1:
        raise JoseError("unknown or ambiguous kid")
    raw_key = validate_public_jwk(matches[0])
    # Execution holdpoint: D-099 did not exercise from_public_bytes.
    public_key = Ed25519PublicKey.from_public_bytes(raw_key)
    signature = _b64u_decode(parts[2])
    try:
        public_key.verify(signature, (parts[0] + "." + parts[1]).encode("ascii"))
    except InvalidSignature:
        raise JoseError("invalid token signature")
    return payload
