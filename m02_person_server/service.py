"""Bounded Person Server semantics for M02 Stage 2.

The core has no sockets and contacts no external component. The separately
bounded HTTP module exposes these operations only on a literal loopback address.
"""

from __future__ import annotations

import secrets
import hashlib
import hmac
import sqlite3
import time
import uuid
from ipaddress import ip_address
from typing import Any, Callable, Mapping
from urllib.parse import urlsplit

from .crypto import (
    canonical_json,
    decode_and_verify_hs256,
    encode_hs256,
    token_digest,
)
from .store import SQLitePersonServerStore
from engines.aauth_execution_runtime_bridge import evaluate_aauth_execution_request


class PersonServerError(RuntimeError):
    """Base error for the bounded local Person Server."""


class TokenRejected(PersonServerError):
    """A token failed integrity, binding, freshness, or revocation checks."""


class LocalPersonServer:
    """Local PS core with explicit persistence and test-only signed tokens."""

    MAX_PERSON_TOKEN_SECONDS = 3600

    def __init__(
        self,
        *,
        store: SQLitePersonServerStore,
        issuer: str = "http://127.0.0.1",
        now: Callable[[], float] = time.time,
        operator_secret: str | None = None,
        max_delegation_hops: int = 0,
        max_authority_age_seconds: int = 3600,
    ) -> None:
        parsed = urlsplit(issuer)
        try:
            literal_host = ip_address(parsed.hostname or "")
        except ValueError as error:
            raise ValueError("M02 Person Server issuer must use a literal loopback IP") from error
        if parsed.scheme != "http" or not literal_host.is_loopback or parsed.username:
            raise ValueError("M02 Person Server issuer must use loopback-only HTTP")
        self.store = store
        self.issuer = issuer.rstrip("/")
        self.now = now
        self.operator_secret = operator_secret or secrets.token_urlsafe(32)
        self.max_delegation_hops = max_delegation_hops
        self.max_authority_age_seconds = max_authority_age_seconds

    @classmethod
    def create_for_local_test(
        cls,
        *,
        store: SQLitePersonServerStore,
        issuer: str = "http://127.0.0.1",
        now: Callable[[], float] = time.time,
        key_id: str = "m02-local-hs256-1",
        secret: bytes | None = None,
        operator_secret: str | None = None,
        max_delegation_hops: int = 0,
        max_authority_age_seconds: int = 3600,
    ) -> "LocalPersonServer":
        service = cls(
            store=store,
            issuer=issuer,
            now=now,
            operator_secret=operator_secret,
            max_delegation_hops=max_delegation_hops,
            max_authority_age_seconds=max_authority_age_seconds,
        )
        try:
            service.store.active_signing_key()
        except KeyError:
            service.store.add_signing_key(
                key_id=key_id,
                secret=secret or secrets.token_bytes(32),
                created_at=int(now()),
            )
        return service

    def authenticate_operator(self, credential: str) -> None:
        if not hmac.compare_digest(credential, self.operator_secret):
            raise TokenRejected("operator credential is invalid")

    def metadata(self) -> dict[str, Any]:
        return {
            "issuer": self.issuer,
            "permission_endpoint": f"{self.issuer}/permission",
            "test_key_metadata_uri": f"{self.issuer}/_test/key-metadata",
            "test_fixture_namespace": f"{self.issuer}/_test/",
            "test_only": True,
            "conformance_claim": None,
        }

    def register_test_agent(self, *, agent_id: str, secret: bytes) -> None:
        self.store.register_agent_key(
            agent_id=agent_id, secret=secret, created_at=int(self.now())
        )

    @staticmethod
    def sign_test_request(*, request: Mapping[str, Any], secret: bytes) -> str:
        return hmac.new(secret, canonical_json(request), hashlib.sha256).hexdigest()

    def authenticate_agent_request(
        self,
        *,
        agent_id: str,
        request: Mapping[str, Any],
        signature: str,
    ) -> bool:
        request_id = request.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            raise TokenRejected("authenticated request_id is required")
        try:
            secret = self.store.agent_secret(agent_id)
        except KeyError as error:
            raise TokenRejected("unknown agent signing identity") from error
        expected = self.sign_test_request(request=request, secret=secret)
        if not hmac.compare_digest(signature, expected):
            raise TokenRejected("agent request signature is invalid")
        try:
            return self.store.consume_authenticated_request(
                request_id=request_id,
                agent_id=agent_id,
                request_digest=hashlib.sha256(canonical_json(request)).hexdigest(),
                accepted_at=int(self.now()),
            )
        except (sqlite3.IntegrityError, ValueError) as error:
            raise TokenRejected(str(error)) from error

    def key_document(self) -> dict[str, Any]:
        # No shared secret is exposed. This is test key metadata, not JWKS.
        return {
            "keys": list(self.store.key_descriptors()),
            "test_only": True,
            "shared_secret_material_exposed": False,
        }

    def retain_mission(
        self,
        *,
        mission_s256: str,
        mission: Mapping[str, Any],
    ) -> None:
        if not mission_s256:
            raise ValueError("mission_s256 is required")
        embedded = mission.get("s256")
        if embedded is not None and embedded != mission_s256:
            raise ValueError("mission content does not match mission_s256")
        self.store.retain_mission(
            mission_s256=mission_s256,
            document=dict(mission),
            retained_at=int(self.now()),
        )
        self.store.append_event(
            recorded_at=int(self.now()),
            kind="mission_retained",
            subject_reference=mission_s256,
            payload={"mission_s256": mission_s256},
        )

    def issue_person_token(
        self,
        *,
        subject: str,
        audience: str,
        mission_s256: str | None = None,
        confirmation: Mapping[str, Any],
        lifetime_seconds: int = 300,
    ) -> str:
        if not subject or not audience:
            raise ValueError("subject and audience are required")
        if lifetime_seconds <= 0 or lifetime_seconds > self.MAX_PERSON_TOKEN_SECONDS:
            raise ValueError("person token lifetime must be between 1 and 3600 seconds")
        if mission_s256 is not None and self.store.mission(mission_s256) is None:
            raise KeyError(f"unknown mission: {mission_s256}")
        issued_at = int(self.now())
        expires_at = issued_at + lifetime_seconds
        token_id = f"pt-{uuid.uuid4().hex}"
        key_id, secret = self.store.active_signing_key()
        claims: dict[str, Any] = {
            "iss": self.issuer,
            "sub": subject,
            "aud": audience,
            "iat": issued_at,
            "exp": expires_at,
            "jti": token_id,
            "token_kind": "person_token",
        }
        if mission_s256 is not None:
            claims["mission_s256"] = mission_s256
        if not confirmation:
            raise ValueError("key confirmation is required")
        claims["cnf"] = dict(confirmation)
        token = encode_hs256(claims, key_id=key_id, secret=secret)
        self.store.retain_token(
            {
                "token_id": token_id,
                "token_kind": "person_token",
                "subject": subject,
                "audience": audience,
                "mission_s256": mission_s256,
                "issued_at": issued_at,
                "expires_at": expires_at,
                "key_id": key_id,
                "token_digest": token_digest(token),
            }
        )
        self.store.append_event(
            recorded_at=issued_at,
            kind="person_token_issued",
            subject_reference=token_id,
            payload={
                "token_id": token_id,
                "subject": subject,
                "audience": audience,
                "mission_s256": mission_s256,
                "expires_at": expires_at,
                "key_id": key_id,
            },
        )
        return token

    def verify_person_token(
        self,
        token: str,
        *,
        audience: str,
        mission_s256: str | None = None,
        expected_confirmation: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            _, claims = decode_and_verify_hs256(
                token,
                secret_for_key_id=self.store.signing_secret,
            )
        except (KeyError, ValueError) as error:
            raise TokenRejected(str(error)) from error
        required = {"iss", "sub", "aud", "iat", "exp", "jti", "token_kind"}
        if required.difference(claims):
            raise TokenRejected("token is missing required claims")
        if claims["token_kind"] != "person_token":
            raise TokenRejected("wrong token kind")
        if claims["iss"] != self.issuer:
            raise TokenRejected("wrong token issuer")
        if claims["aud"] != audience:
            raise TokenRejected("wrong token audience")
        if mission_s256 is not None and claims.get("mission_s256") != mission_s256:
            raise TokenRejected("wrong mission binding")
        if expected_confirmation is not None and claims.get("cnf") != dict(expected_confirmation):
            raise TokenRejected("wrong key confirmation binding")
        current_time = int(self.now())
        if not isinstance(claims["iat"], int) or not isinstance(claims["exp"], int):
            raise TokenRejected("token time claims must be integers")
        if claims["iat"] > current_time:
            raise TokenRejected("token is not yet valid")
        if claims["exp"] <= current_time:
            raise TokenRejected("token is expired")
        record = self.store.token_record(str(claims["jti"]))
        if record is None:
            raise TokenRejected("token is not retained by this Person Server")
        if record["token_digest"] != token_digest(token):
            raise TokenRejected("retained token does not match presented token")
        if record["revoked_at"] is not None:
            raise TokenRejected("token is revoked")
        return claims

    def revoke_person_token(self, *, token_id: str, reason: str) -> bool:
        if not reason.strip():
            raise ValueError("revocation reason is required")
        record = self.store.token_record(token_id)
        if record is None or record["token_kind"] != "person_token":
            raise KeyError(f"unknown person token: {token_id}")
        revoked_at = int(self.now())
        changed = self.store.revoke_token(
            token_id=token_id,
            revoked_at=revoked_at,
            reason=reason,
        )
        if changed:
            self.store.append_event(
                recorded_at=revoked_at,
                kind="person_token_revoked",
                subject_reference=token_id,
                payload={"token_id": token_id, "reason": reason},
            )
        return changed

    def permission(
        self,
        *,
        request: Mapping[str, Any],
        agent_id: str,
        signature: str,
        person_token: str,
        pending_lifetime_seconds: int = 60,
    ) -> tuple[int, dict[str, Any]]:
        """Authenticate and evaluate one action request through SOGA."""

        allowed_request_fields = {
            "request_id", "mission_s256", "action", "description", "subject",
            "reachability",
        }
        unknown_fields = set(request).difference(allowed_request_fields)
        if unknown_fields:
            raise PersonServerError(
                "unsupported permission fields: " + ", ".join(sorted(unknown_fields))
            )
        reserved_security_fields = {
            "representative", "representative_authority", "assent", "refusal",
            "runtime_authority", "authority_state", "policy",
            "max_delegation_hops", "max_elapsed_seconds",
        }
        subject_input = request.get("subject", {})
        if not isinstance(subject_input, dict):
            raise PersonServerError("subject must be an object")
        rejected_security_fields = reserved_security_fields.intersection(subject_input)
        if rejected_security_fields:
            raise PersonServerError(
                "unsupported security claims: "
                + ", ".join(sorted(rejected_security_fields))
            )
        fresh_request = self.authenticate_agent_request(
            agent_id=agent_id, request=request, signature=signature
        )
        if not fresh_request:
            retained_result = self.store.permission_result(str(request["request_id"]))
            if retained_result is None:
                raise PersonServerError("identical request is still being evaluated")
            return retained_result
        mission_s256 = request.get("mission_s256")
        if not isinstance(mission_s256, str) or not mission_s256:
            raise PersonServerError("mission_s256 is required")
        mission = self.store.mission(mission_s256)
        if mission is None:
            raise PersonServerError("mission is not retained")
        claims = self.verify_person_token(
            person_token,
            audience=self.issuer,
            mission_s256=mission_s256,
            expected_confirmation={"kid": agent_id},
        )
        requested_person_id = subject_input.get("person_id")
        if requested_person_id is not None and requested_person_id != claims["sub"]:
            raise TokenRejected("request subject does not match person token subject")
        record = self.store.token_record(claims["jti"])
        assert record is not None
        current_time = int(self.now())
        mission_policy = dict(mission.get("policy", {}))
        unavailable = {"delegation_hops", "attenuated"}
        required_facts = set(mission_policy.get("required_authority_facts", ()))
        unresolved_required = required_facts.intersection(unavailable)
        if unresolved_required:
            raise TokenRejected(
                "required authority facts are unavailable: "
                + ", ".join(sorted(unresolved_required))
            )
        verified_state = {
            "revoked": record["revoked_at"] is not None,
            "expired": record["expires_at"] <= current_time,
            "delegation_hops": 0,
            "max_delegation_hops": self.max_delegation_hops,
            "elapsed_seconds": max(0, current_time - record["issued_at"]),
            "max_elapsed_seconds": self.max_authority_age_seconds,
            "attenuated": False,
            "unavailable": sorted(unavailable),
            "source": "retained-person-token",
            "observed_at": current_time,
        }
        action = request.get("action")
        if not isinstance(action, str) or not action:
            raise PersonServerError("action is required")
        approved_actions = {
            item.get("name")
            for item in mission.get("approved_tools", [])
            if isinstance(item, dict)
        }
        if action not in approved_actions:
            raise TokenRejected("requested action is not approved by the retained mission")
        execution_request = {
            "request_id": request["request_id"],
            "agent_url": agent_id,
            "action": action,
            "message": request.get("description", action),
            "mission": {
                "mission_id": mission_s256,
                "description": mission.get("description", ""),
                "allowed_actions": [
                    item["name"] for item in mission.get("approved_tools", [])
                ],
                "references": {"aauth_mission": mission},
            },
            "authority": {
                "authority_id": claims["jti"],
                "allowed_actions": [action],
            },
            "subject": dict(request.get("subject", {})),
            "reachability": request.get("reachability", "REACHABLE"),
            "policy": {**mission_policy, "mission_s256": mission_s256},
        }
        decision = evaluate_aauth_execution_request(
            execution_request, verified_authority_state=verified_state
        )
        self._record_decision_and_projection(
            request_id=request["request_id"], decision=decision, projection="pending"
        )
        determination = decision["governance_determination"]
        if determination == "ALLOW":
            response = {"permission": "granted"}
            projection = "granted"
            status = 200
        elif determination == "DENY":
            response = {"permission": "denied"}
            projection = "denied"
            status = 200
        else:
            if pending_lifetime_seconds <= 0:
                raise ValueError("pending lifetime must be positive")
            pending_id = f"pending-{uuid.uuid4().hex}"
            self.store.create_pending(
                {
                    "pending_id": pending_id,
                    "request_id": request["request_id"],
                    "agent_id": agent_id,
                    "mission_s256": mission_s256,
                    "action": action,
                    "request": execution_request,
                    "decision": decision,
                    "created_at": current_time,
                    "expires_at": current_time + pending_lifetime_seconds,
                }
            )
            response = {
                "status": "pending",
                "pending_id": pending_id,
                "pending_url": f"/pending/{pending_id}",
                "requirement": "approval",
            }
            self.store.retain_permission_result(
                request_id=request["request_id"], status=202, response=response
            )
            return 202, response
        self._record_projection(request["request_id"], projection, status, response)
        self.store.retain_permission_result(
            request_id=request["request_id"], status=status, response=response
        )
        return status, response

    def resolve_pending(
        self,
        *,
        pending_id: str,
        result: str,
        approval_evidence: Mapping[str, Any] | None = None,
    ) -> tuple[int, dict[str, Any]]:
        pending = self.store.pending(pending_id)
        if pending is None:
            raise KeyError(f"unknown pending request: {pending_id}")
        now = int(self.now())
        if pending["state"] != "pending":
            raise PersonServerError("pending request is terminal")
        if now >= pending["expires_at"]:
            self.store.finish_pending(pending_id=pending_id, result="expired")
            self._record_projection(
                pending["request_id"], "expired", 408, {"error": "expired"}
            )
            self.store.retain_permission_result(
                request_id=pending["request_id"], status=408, response={"error": "expired"}
            )
            return 408, {"error": "expired"}
        if result == "decline":
            self.store.finish_pending(pending_id=pending_id, result="declined")
            response = {"permission": "denied", "reason": "approval declined"}
            self._record_projection(pending["request_id"], "declined", 200, response)
            self.store.retain_permission_result(
                request_id=pending["request_id"], status=200, response=response
            )
            return 200, response
        if result != "approve" or approval_evidence is None:
            raise ValueError("approve requires explicit approval_evidence")
        required_bindings = {
            "pending_id": pending_id,
            "request_id": pending["request_id"],
            "mission_s256": pending["mission_s256"],
            "action": pending["action"],
            "agent_id": pending["agent_id"],
        }
        for name, expected in required_bindings.items():
            if approval_evidence.get(name) != expected:
                raise TokenRejected(f"approval evidence has wrong {name} binding")
        restrict_mode = pending["decision"]["governance_decision"].get("restrict_mode")
        constraint = (
            restrict_mode.get("constraint") if isinstance(restrict_mode, dict) else None
        )
        if isinstance(constraint, dict):
            constraint_bindings = {
                "constraint_reference": constraint.get("gate_id"),
                "required_evidence": constraint.get("required_evidence"),
                "authority_reference": constraint.get("authority_reference"),
            }
            for name, expected in constraint_bindings.items():
                if expected is not None and approval_evidence.get(name) != expected:
                    raise TokenRejected(f"approval evidence has wrong {name} binding")
        execution_request = dict(pending["request"])
        execution_request["request_id"] = f"{pending['request_id']}-reevaluation"
        execution_request["policy"] = {
            **dict(execution_request.get("policy", {})),
            "approval_evidence": dict(approval_evidence),
        }
        # Authority freshness is reconstructed from the retained token reference
        # in the original decision, never accepted from the resolving caller.
        authority_id = execution_request["authority"]["authority_id"]
        record = self.store.token_record(authority_id)
        if record is None:
            raise TokenRejected("retained authority no longer exists")
        if record["revoked_at"] is not None:
            raise TokenRejected("authority was revoked while permission was pending")
        if record["expires_at"] <= now:
            raise TokenRejected("authority expired while permission was pending")
        pending_person_id = pending["request"].get("subject", {}).get("person_id")
        if pending_person_id is not None and record["subject"] != pending_person_id:
            raise TokenRejected("pending subject no longer matches retained authority")
        verified_state = {
            "revoked": record["revoked_at"] is not None,
            "expired": record["expires_at"] <= now,
            "delegation_hops": 0,
            "max_delegation_hops": self.max_delegation_hops,
            "elapsed_seconds": max(0, now - record["issued_at"]),
            "max_elapsed_seconds": self.max_authority_age_seconds,
            "attenuated": False,
            "unavailable": ["delegation_hops", "attenuated"],
            "source": "retained-person-token-reevaluation",
            "observed_at": now,
        }
        decision = evaluate_aauth_execution_request(
            execution_request, verified_authority_state=verified_state
        )
        self.store.finish_pending(pending_id=pending_id, result="reevaluated")
        projection = (
            "granted_after_reevaluation"
            if decision["governance_determination"] == "ALLOW"
            else "denied_after_reevaluation"
        )
        response = {
            "permission": "granted" if projection.startswith("granted") else "denied"
        }
        self._record_decision_and_projection(
            request_id=pending["request_id"], decision=decision, projection=projection
        )
        self._record_projection(pending["request_id"], projection, 200, response)
        self.store.retain_permission_result(
            request_id=pending["request_id"], status=200, response=response
        )
        return 200, response

    def poll_pending(
        self,
        *,
        pending_id: str,
        request: Mapping[str, Any],
        agent_id: str,
        signature: str,
    ) -> tuple[int, dict[str, Any]]:
        self.authenticate_agent_request(
            agent_id=agent_id, request=request, signature=signature
        )
        if set(request) != {"request_id", "pending_id"}:
            raise PersonServerError("pending poll has unsupported fields")
        if request["pending_id"] != pending_id:
            raise PersonServerError("pending poll path and body do not match")
        pending = self.store.pending(pending_id)
        if pending is None or pending["agent_id"] != agent_id:
            raise KeyError("unknown pending request")
        if pending["state"] == "pending" and int(self.now()) >= pending["expires_at"]:
            self.store.finish_pending(pending_id=pending_id, result="expired")
            expired_response = {"error": "expired"}
            self.store.retain_permission_result(
                request_id=pending["request_id"], status=408, response=expired_response
            )
        delivery, status, response = self.store.deliver_pending_result(
            pending_id=pending_id, agent_id=agent_id
        )
        if delivery == "missing":
            raise KeyError("unknown pending request")
        if delivery == "pending":
            return 202, {"status": "pending", "pending_id": pending_id}
        if delivery == "gone":
            return 410, {"error": "gone"}
        assert status is not None and response is not None
        return status, response

    def _record_decision_and_projection(
        self, *, request_id: str, decision: Mapping[str, Any], projection: str
    ) -> None:
        self.store.append_event(
            recorded_at=int(self.now()), kind="soga_decision",
            subject_reference=request_id, payload=dict(decision)
        )

    def _record_projection(
        self, request_id: str, projection: str, status: int, response: Mapping[str, Any]
    ) -> None:
        self.store.append_event(
            recorded_at=int(self.now()), kind="aauth_projection",
            subject_reference=request_id,
            payload={"projection": projection, "status": status, "response": dict(response)},
        )

    @staticmethod
    def canonical_message(value: Mapping[str, Any]) -> bytes:
        """Expose deterministic message bytes for later local transport signing."""

        return canonical_json(value)
