"""Strict role-token profile for the bounded AAuth fcf656d exchange."""

from dataclasses import dataclass

from . import jose
from .identifiers import validate_agent_identifier, validate_server_identifier


class TokenProfileError(ValueError):
    pass


PERSON_AUTH_MAX_SECONDS = 3600
RESOURCE_MAX_SECONDS = 300


def _text(value, name):
    if not isinstance(value, str) or not value:
        raise TokenProfileError(name + " is required")
    return value


def _integer(value, name):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TokenProfileError(name + " must be an integer")
    return value


def _common(payload, *, issuer, dwk, now, max_lifetime, audience=None):
    if not isinstance(payload, dict):
        raise TokenProfileError("token payload must be an object")
    required = {"iss", "dwk", "jti", "iat", "exp"}
    if audience is not None:
        required.add("aud")
    missing = required.difference(payload)
    if missing:
        raise TokenProfileError("missing token claims: " + ", ".join(sorted(missing)))
    if payload["iss"] != issuer or payload["dwk"] != dwk:
        raise TokenProfileError("issuer metadata binding mismatch")
    if audience is not None and payload["aud"] != audience:
        raise TokenProfileError("wrong token audience")
    issued = _integer(payload["iat"], "iat")
    expires = _integer(payload["exp"], "exp")
    if issued > now:
        raise TokenProfileError("token issued in the future")
    if expires <= now:
        raise TokenProfileError("token is expired")
    if expires <= issued or expires - issued > max_lifetime:
        raise TokenProfileError("token lifetime exceeds profile")
    _text(payload["jti"], "jti")
    return dict(payload)


def _confirmation(payload, expected_jwk):
    confirmation = payload.get("cnf")
    if not isinstance(confirmation, dict) or set(confirmation) != {"jwk"}:
        raise TokenProfileError("cnf.jwk is required")
    try:
        jose.validate_public_jwk(confirmation["jwk"])
    except jose.JoseError as error:
        raise TokenProfileError(str(error)) from error
    if confirmation["jwk"] != expected_jwk:
        raise TokenProfileError("confirmation key mismatch")


@dataclass(frozen=True)
class Issuer:
    identifier: str
    dwk: str
    kid: str
    private_key: object

    @property
    def jwk(self):
        return jose.public_jwk(self.private_key.public_key(), self.kid)

    @property
    def jwks(self):
        return jose.public_jwks([self.jwk])

    def sign(self, claims, typ):
        return jose.sign_compact(dict(claims), typ, self.kid, self.private_key)


def issue_agent_token(issuer, *, agent_id, ps, agent_jwk, now, expires, jti):
    validate_agent_identifier(agent_id, top_level_only=True)
    validate_server_identifier(issuer.identifier)
    validate_server_identifier(ps)
    claims = {"iss": issuer.identifier, "dwk": "aauth-agent.json", "sub": agent_id,
              "ps": ps, "cnf": {"jwk": dict(agent_jwk)}, "jti": jti,
              "iat": now, "exp": expires}
    return issuer.sign(claims, "aa-agent+jwt")


def verify_agent_token(token, jwks, *, issuer, ps, agent_jwk, now):
    try:
        claims = jose.verify_compact(token, "aa-agent+jwt", jwks)
    except jose.JoseError as error:
        raise TokenProfileError(str(error)) from error
    claims = _common(claims, issuer=issuer, dwk="aauth-agent.json", now=now,
                     max_lifetime=86_400)
    validate_agent_identifier(_text(claims.get("sub"), "sub"), top_level_only=True)
    if claims.get("ps") != ps:
        raise TokenProfileError("wrong person server")
    _confirmation(claims, agent_jwk)
    return claims


def issue_person_token(issuer, *, resource, subject, agent_jwk, mission_s256,
                       now, expires, jti, agent_expires, mission_expires):
    validate_server_identifier(resource)
    if expires > min(agent_expires, mission_expires):
        raise TokenProfileError("person token exceeds governing expiry")
    claims = {"iss": issuer.identifier, "dwk": "aauth-person.json", "aud": resource,
              "sub": _text(subject, "sub"), "cnf": {"jwk": dict(agent_jwk)},
              "mission_s256": _text(mission_s256, "mission_s256"), "jti": jti,
              "iat": now, "exp": expires}
    if expires - now > PERSON_AUTH_MAX_SECONDS:
        raise TokenProfileError("person token lifetime exceeds one hour")
    return issuer.sign(claims, "aa-person+jwt")


def verify_person_token(token, jwks, *, issuer, resource, agent_jwk, now):
    try:
        claims = jose.verify_compact(token, "aa-person+jwt", jwks)
    except jose.JoseError as error:
        raise TokenProfileError(str(error)) from error
    claims = _common(claims, issuer=issuer, dwk="aauth-person.json", now=now,
                     max_lifetime=PERSON_AUTH_MAX_SECONDS, audience=resource)
    if "scope" in claims or "account" in claims:
        raise TokenProfileError("person token carries authorization claims")
    _text(claims.get("sub"), "sub")
    _text(claims.get("mission_s256"), "mission_s256")
    _confirmation(claims, agent_jwk)
    return claims


def issue_resource_token(issuer, *, ps, subject, presented_jti, agent_jwk,
                         mission_s256, scope, now, expires, jti):
    if expires - now > RESOURCE_MAX_SECONDS:
        raise TokenProfileError("resource token lifetime exceeds five minutes")
    claims = {"iss": issuer.identifier, "dwk": "aauth-resource.json", "aud": ps,
              "ps": ps, "sub": _text(subject, "sub"),
              "presented_jti": _text(presented_jti, "presented_jti"),
              "agent_jkt": jose.jwk_thumbprint(agent_jwk),
              "mission_s256": _text(mission_s256, "mission_s256"),
              "scope": _text(scope, "scope"), "jti": jti, "iat": now,
              "exp": expires}
    return issuer.sign(claims, "aa-resource+jwt")


def verify_resource_token(token, jwks, *, issuer, ps, agent_jwk, now):
    try:
        claims = jose.verify_compact(token, "aa-resource+jwt", jwks)
    except jose.JoseError as error:
        raise TokenProfileError(str(error)) from error
    claims = _common(claims, issuer=issuer, dwk="aauth-resource.json", now=now,
                     max_lifetime=RESOURCE_MAX_SECONDS, audience=ps)
    for name in ("ps", "sub", "presented_jti", "agent_jkt", "mission_s256", "scope"):
        _text(claims.get(name), name)
    if claims["ps"] != ps or claims["agent_jkt"] != jose.jwk_thumbprint(agent_jwk):
        raise TokenProfileError("resource token binding mismatch")
    if "cnf" in claims:
        raise TokenProfileError("resource token must not carry cnf")
    return claims


def issue_auth_token(issuer, *, resource, ps, subject, agent_jwk, mission_s256,
                     scope, now, expires, jti, agent_expires, presented_expires,
                     mission_expires):
    if expires > min(agent_expires, presented_expires, mission_expires):
        raise TokenProfileError("auth token exceeds governing expiry")
    if expires - now > PERSON_AUTH_MAX_SECONDS:
        raise TokenProfileError("auth token lifetime exceeds one hour")
    claims = {"iss": issuer.identifier, "dwk": "aauth-person.json", "aud": resource,
              "ps": ps, "sub": _text(subject, "sub"),
              "cnf": {"jwk": dict(agent_jwk)},
              "mission_s256": _text(mission_s256, "mission_s256"),
              "scope": _text(scope, "scope"), "jti": jti, "iat": now,
              "exp": expires}
    return issuer.sign(claims, "aa-auth+jwt")


def verify_auth_token(token, jwks, *, issuer, resource, ps, subject,
                      agent_jwk, mission_s256, required_scope, now):
    try:
        claims = jose.verify_compact(token, "aa-auth+jwt", jwks)
    except jose.JoseError as error:
        raise TokenProfileError(str(error)) from error
    claims = _common(claims, issuer=issuer, dwk="aauth-person.json", now=now,
                     max_lifetime=PERSON_AUTH_MAX_SECONDS, audience=resource)
    expected = {"ps": ps, "sub": subject, "mission_s256": mission_s256}
    if any(claims.get(name) != value for name, value in expected.items()):
        raise TokenProfileError("auth token context mismatch")
    _confirmation(claims, agent_jwk)
    scopes = claims.get("scope", "").split()
    if required_scope not in scopes:
        raise TokenProfileError("required scope absent")
    return claims

