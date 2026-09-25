"""Fail-closed SOGA supervision adapter for the bounded localhost profile."""

from dataclasses import dataclass
from types import MappingProxyType

from engines.aauth_execution_runtime_bridge import evaluate_aauth_execution_request

from .exchange import SupervisionDecision


class SupervisionAdapterError(ValueError):
    pass


_BOOL_FIELDS = frozenset({"revoked", "expired", "attenuated"})
_INT_FIELDS = frozenset({
    "delegation_hops", "max_delegation_hops", "elapsed_seconds",
    "max_elapsed_seconds",
})
_REQUIRED_FIELDS = _BOOL_FIELDS | _INT_FIELDS
_KNOWN_FIELDS = _REQUIRED_FIELDS | frozenset({"source", "observed_at", "unavailable"})


def validated_authority_state(value):
    if not isinstance(value, dict) or set(value) != _KNOWN_FIELDS:
        raise SupervisionAdapterError("exact verified authority state is required")
    if any(type(value[name]) is not bool for name in _BOOL_FIELDS):
        raise SupervisionAdapterError("authority flags must be booleans")
    if any(type(value[name]) is not int or value[name] < 0 for name in _INT_FIELDS):
        raise SupervisionAdapterError("authority counts must be non-negative integers")
    if value["delegation_hops"] > value["max_delegation_hops"]:
        raise SupervisionAdapterError("delegation policy limit exceeded")
    if value["elapsed_seconds"] > value["max_elapsed_seconds"]:
        raise SupervisionAdapterError("elapsed policy limit exceeded")
    if not isinstance(value["source"], str) or not value["source"]:
        raise SupervisionAdapterError("authority source is required")
    if type(value["observed_at"]) is not int or value["observed_at"] < 0:
        raise SupervisionAdapterError("authority observation time is invalid")
    unavailable = value["unavailable"]
    if (not isinstance(unavailable, (list, tuple)) or
            any(item not in _REQUIRED_FIELDS for item in unavailable) or
            len(set(unavailable)) != len(unavailable)):
        raise SupervisionAdapterError("unavailable authority facts are invalid")
    result = dict(value)
    result["unavailable"] = tuple(unavailable)
    return MappingProxyType(result)


@dataclass(frozen=True)
class SogaSupervisionProfile:
    verified_authority_state: object
    required_authority_facts: tuple
    subject_governance_state: str
    reachability: str
    subject_state_source: str
    reachability_source: str

    @classmethod
    def create(cls, *, verified_authority_state, required_authority_facts,
               subject_governance_state, reachability, subject_state_source,
               reachability_source):
        state = validated_authority_state(verified_authority_state)
        required = tuple(required_authority_facts)
        if (len(set(required)) != len(required) or
                any(item not in _REQUIRED_FIELDS for item in required)):
            raise SupervisionAdapterError("required authority facts are invalid")
        if subject_governance_state not in {
                "INDEPENDENT", "SUPERVISED", "MANAGED", "DELEGATED", "LAPSED"}:
            raise SupervisionAdapterError("subject governance state is invalid")
        if reachability not in {"REACHABLE", "UNREACHABLE", "UNKNOWN"}:
            raise SupervisionAdapterError("subject reachability is invalid")
        if (not isinstance(subject_state_source, str) or not subject_state_source or
                not isinstance(reachability_source, str) or not reachability_source):
            raise SupervisionAdapterError("subject state sources are required")
        return cls(state, required, subject_governance_state, reachability,
                   subject_state_source, reachability_source)


class SogaSupervisor:
    """Translate separated supervision input into one SOGA governance call."""

    def __init__(self, profile, evaluator=evaluate_aauth_execution_request):
        if not isinstance(profile, SogaSupervisionProfile) or not callable(evaluator):
            raise SupervisionAdapterError("valid profile and evaluator are required")
        self.profile = profile
        self.evaluator = evaluator
        self.calls = 0

    def __call__(self, value):
        self.calls += 1
        try:
            request = self._request(value)
            result = self.evaluator(
                request,
                verified_authority_state=dict(self.profile.verified_authority_state),
            )
            if not isinstance(result, dict):
                raise SupervisionAdapterError("malformed governance result")
            determination = result.get("governance_determination")
            decision = result.get("governance_decision")
            cdp = result.get("canonical_decision_package")
            if (determination not in {"ALLOW", "RESTRICT", "DENY"} or
                    not isinstance(decision, dict) or not isinstance(cdp, dict)):
                raise SupervisionAdapterError("incomplete governance result")
            step_id = decision.get("step_id")
            if not isinstance(step_id, str) or not step_id:
                raise SupervisionAdapterError("governance decision lacks identifier")
            if determination == "ALLOW":
                return SupervisionDecision("ALLOW", step_id, "soga-allow")
            return SupervisionDecision("DENY", step_id, "soga-" + determination.lower())
        except Exception:
            return SupervisionDecision("DENY", "soga-fail-closed", "soga-error")

    def _request(self, value):
        if not isinstance(value, dict) or set(value) != {
                "resource_asserted", "person_server_verified", "agent_asserted"}:
            raise SupervisionAdapterError("separated supervision input is required")
        resource = value["resource_asserted"]
        verified = value["person_server_verified"]
        agent = value["agent_asserted"]
        if not all(isinstance(item, dict) for item in (resource, verified, agent)):
            raise SupervisionAdapterError("supervision origins must be objects")
        scope = resource.get("scope")
        if not isinstance(scope, str) or not scope:
            raise SupervisionAdapterError("resource scope is required")
        mission_s256 = verified.get("mission_s256")
        subject = verified.get("sub")
        if not all(isinstance(item, str) and item for item in (mission_s256, subject)):
            raise SupervisionAdapterError("verified mission and subject are required")
        return {
            "request_id": "soga-" + str(resource.get("resource_jti", "missing")),
            "user_id": subject,
            "message": str(agent.get("justification", "")),
            "action": scope,
            "mission": {
                "mission_id": mission_s256,
                "subject_id": subject,
                "objective": str(agent.get("justification", "")),
                "allowed_actions": [scope],
                "references": {
                    "resource_asserted": dict(resource),
                    "person_server_verified": dict(verified),
                    "agent_asserted": dict(agent),
                },
            },
            "authority": {
                "authority_id": str(resource.get("resource_jti", "")),
                "authority_type": "aauth-resource-token-chain",
                "allowed_actions": [scope],
                "references": {"assertion_origins_separated": True},
            },
            "subject": {
                "subject_id": subject,
                "governance_state": self.profile.subject_governance_state,
                "reachability": self.profile.reachability,
                "context": {
                    "governance_state_source": self.profile.subject_state_source,
                    "reachability_source": self.profile.reachability_source,
                },
            },
            "runtime": {"requested_action": scope},
            "policy": {
                "profile": "m02-aauth-localhost-v1",
                "mission_s256": mission_s256,
                "required_authority_facts": list(self.profile.required_authority_facts),
            },
        }
