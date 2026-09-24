"""Transport-free three-party AAuth fcf656d exchange roles."""

import json
from dataclasses import dataclass

from . import jose
from .http_signatures import Request, sign_request, verify_request
from .identifiers import validate_agent_identifier, validate_server_identifier
from .structured_fields import Item, Token, parse_dictionary
from .tokens import (
    TokenProfileError, issue_auth_token, issue_person_token, issue_resource_token,
    verify_agent_token, verify_auth_token, verify_person_token, verify_resource_token,
)


class ExchangeError(ValueError):
    pass


def _body(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")


def _json_body(request):
    try:
        value = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ExchangeError("invalid JSON request") from error
    if not isinstance(value, dict):
        raise ExchangeError("request body must be an object")
    return value


def signed_post(authority, path, body, assertion, private_key, created):
    request = Request("POST", authority, path, {"content-type": "application/json"}, _body(body))
    return sign_request(request, assertion, private_key, created=created, body_request=True)


@dataclass(frozen=True)
class SupervisionDecision:
    determination: str
    decision_id: str
    reason_code: str


@dataclass(frozen=True)
class Mission:
    s256: str
    agent_id: str
    expires_at: int
    active: bool = True


class PersonServer:
    def __init__(self, *, issuer, agent_provider, resource, directed_subject,
                 missions, supervisor, now):
        self.issuer = issuer
        self.agent_provider = agent_provider
        self.resource = resource
        self.directed_subject = directed_subject
        self.missions = dict(missions)
        self.supervisor = supervisor
        self.now = now

    def _agent(self, request):
        claims = verify_request(request, self.agent_provider.jwks, "aa-agent+jwt",
                                now=self.now, body_request=True)
        return verify_agent_token(
            request_token(request), self.agent_provider.jwks,
            issuer=self.agent_provider.identifier, ps=self.issuer.identifier,
            agent_jwk=claims["cnf"]["jwk"], now=self.now)

    def _mission(self, mission_s256, agent_id):
        mission = self.missions.get(mission_s256)
        if (mission is None or not mission.active or mission.expires_at <= self.now
                or mission.agent_id != agent_id):
            raise ExchangeError("mission is not active for this agent")
        return mission

    def person_token(self, request):
        agent = self._agent(request)
        body = _json_body(request)
        if set(body) != {"resource", "mission_s256"}:
            raise ExchangeError("invalid person-token request")
        if body["resource"] != self.resource.identifier:
            raise ExchangeError("unknown resource")
        mission = self._mission(body["mission_s256"], agent["sub"])
        expires = min(self.now + 3600, agent["exp"], mission.expires_at)
        return issue_person_token(
            self.issuer, resource=self.resource.identifier, subject=self.directed_subject,
            agent_jwk=agent["cnf"]["jwk"], mission_s256=mission.s256,
            now=self.now, expires=expires, jti="person-1",
            agent_expires=agent["exp"], mission_expires=mission.expires_at)

    def auth_token(self, request):
        agent = self._agent(request)
        body = _json_body(request)
        if set(body) != {"resource_token", "presented_token", "justification"}:
            raise ExchangeError("invalid auth-token request")
        resource = verify_resource_token(
            body["resource_token"], self.resource.jwks,
            issuer=self.resource.identifier, ps=self.issuer.identifier,
            agent_jwk=agent["cnf"]["jwk"], now=self.now)
        person = verify_person_token(
            body["presented_token"], self.issuer.jwks,
            issuer=self.issuer.identifier, resource=self.resource.identifier,
            agent_jwk=agent["cnf"]["jwk"], now=self.now)
        bindings = {
            "presented_jti": person["jti"], "ps": person["iss"],
            "sub": person["sub"], "mission_s256": person["mission_s256"],
        }
        if any(resource[name] != value for name, value in bindings.items()):
            raise ExchangeError("resource and presented token binding mismatch")
        mission = self._mission(resource["mission_s256"], agent["sub"])
        supervision_input = {
            "resource_asserted": {
                "resource": resource["iss"], "scope": resource["scope"],
                "resource_jti": resource["jti"], "expires_at": resource["exp"],
            },
            "person_server_verified": {
                "person_server": self.issuer.identifier, "sub": person["sub"],
                "agent_jkt": jose.jwk_thumbprint(agent["cnf"]["jwk"]),
                "mission_s256": mission.s256,
                "mission_active": mission.active, "mission_expires_at": mission.expires_at,
            },
            "agent_asserted": {
                "agent_id": agent["sub"], "justification": body["justification"],
            },
        }
        try:
            decision = self.supervisor(supervision_input)
        except Exception as error:
            raise ExchangeError("supervision failed closed") from error
        if (not isinstance(decision, SupervisionDecision)
                or decision.determination not in {"ALLOW", "DENY"}
                or not decision.decision_id or not decision.reason_code):
            raise ExchangeError("malformed supervision decision")
        if decision.determination != "ALLOW":
            raise ExchangeError("supervision denied authorization")
        expires = min(self.now + 3600, agent["exp"], person["exp"], mission.expires_at)
        return issue_auth_token(
            self.issuer, resource=self.resource.identifier, ps=self.issuer.identifier,
            subject=resource["sub"], agent_jwk=agent["cnf"]["jwk"],
            mission_s256=resource["mission_s256"], scope=resource["scope"],
            now=self.now, expires=expires, jti="auth-1", agent_expires=agent["exp"],
            presented_expires=person["exp"], mission_expires=mission.expires_at)


class Resource:
    def __init__(self, *, issuer, person_server, now):
        self.issuer = issuer
        self.person_server = person_server
        self.now = now

    def authorize(self, request):
        person = verify_request(request, self.person_server.jwks, "aa-person+jwt",
                                now=self.now, body_request=True)
        person = verify_person_token(
            request_token(request), self.person_server.jwks,
            issuer=self.person_server.identifier, resource=self.issuer.identifier,
            agent_jwk=person["cnf"]["jwk"], now=self.now)
        body = _json_body(request)
        if set(body) != {"scope"}:
            raise ExchangeError("invalid authorization request")
        return issue_resource_token(
            self.issuer, ps=self.person_server.identifier, subject=person["sub"],
            presented_jti=person["jti"], agent_jwk=person["cnf"]["jwk"],
            mission_s256=person["mission_s256"], scope=body["scope"],
            now=self.now, expires=self.now + 300, jti="resource-1")

    def enforce(self, request, *, subject, mission_s256, required_scope):
        auth = verify_request(request, self.person_server.jwks, "aa-auth+jwt",
                              now=self.now, body_request=True)
        return verify_auth_token(
            request_token(request), self.person_server.jwks,
            issuer=self.person_server.identifier, resource=self.issuer.identifier,
            ps=self.person_server.identifier, subject=subject,
            agent_jwk=auth["cnf"]["jwk"], mission_s256=mission_s256,
            required_scope=required_scope, now=self.now)


def request_token(request):
    """Return the jwt parameter after signature verification has established it."""
    try:
        members = parse_dictionary(request.headers["signature-key"])
    except (KeyError, ValueError) as error:
        raise ExchangeError("invalid signature-key header") from error
    matches = [member for label, member in members if label == "sig"]
    if len(matches) != 1 or not isinstance(matches[0], Item):
        raise ExchangeError("signature-key label missing or ambiguous")
    member = matches[0]
    if not isinstance(member.value, Token) or member.value.value != "jwt":
        raise ExchangeError("jwt signature-key scheme required")
    parameters = dict(member.parameters)
    if set(parameters) != {"jwt"} or not isinstance(parameters["jwt"], str):
        raise ExchangeError("invalid jwt signature-key parameters")
    return parameters["jwt"]
