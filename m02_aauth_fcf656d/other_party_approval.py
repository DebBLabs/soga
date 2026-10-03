"""Additive resource policy for the bounded other-party approval experiment."""

import json
from dataclasses import dataclass

from . import jose
from .exchange import ExchangeError, Resource, request_token
from .http_signatures import SignatureProfileError
from .localhost import ResourceSurface, _challenge
from .tokens import TokenProfileError


AMBIENT_SCOPE = "misty.acknowledge_tip"
DIRECTED_SCOPE = "misty.address_participant"
POLICY_VERSION = "m02-other-party-approval-v1"
_SCOPES = frozenset({AMBIENT_SCOPE, DIRECTED_SCOPE})


class OtherPartyApprovalError(ValueError):
    pass


@dataclass(frozen=True)
class OtherPartyApprovalReceipt:
    receipt_id: str
    asserted_role: str
    assurance: str
    participant: str
    mission_s256: str
    scope: str
    state: str
    observed_at: int
    expires_at: int
    source: str

    def __post_init__(self):
        text_names = (
            "receipt_id", "asserted_role", "assurance", "participant",
            "mission_s256", "scope", "state", "source",
        )
        if any(not isinstance(getattr(self, name), str) or not getattr(self, name)
               for name in text_names):
            raise OtherPartyApprovalError("approval receipt text is invalid")
        if self.asserted_role != "parent":
            raise OtherPartyApprovalError("asserted role is invalid")
        if self.assurance != "unverified-demo-input":
            raise OtherPartyApprovalError("approval assurance is invalid")
        if self.scope != DIRECTED_SCOPE:
            raise OtherPartyApprovalError("approval scope is invalid")
        if self.state not in {"APPROVED", "WITHDRAWN"}:
            raise OtherPartyApprovalError("approval state is invalid")
        if (type(self.observed_at) is not int or self.observed_at < 0 or
                type(self.expires_at) is not int or self.expires_at < 0 or
                self.expires_at <= self.observed_at):
            raise OtherPartyApprovalError("approval time window is invalid")

    @classmethod
    def create(cls, value):
        names = {
            "receipt_id", "asserted_role", "assurance", "participant",
            "mission_s256", "scope", "state", "observed_at", "expires_at",
            "source",
        }
        if not isinstance(value, dict) or set(value) != names:
            raise OtherPartyApprovalError("exact approval receipt is required")
        return cls(**value)


@dataclass(frozen=True)
class OtherPartyDecisionReceipt:
    policy_version: str
    participant: str
    participant_source: str
    mission_s256: str
    scope: str
    approval_assurance: str
    approval_source: str
    outcome: str
    reason: str

    def as_dict(self):
        return {
            "policy_version": self.policy_version,
            "participant": self.participant,
            "participant_source": self.participant_source,
            "mission_s256": self.mission_s256,
            "scope": self.scope,
            "approval_assurance": self.approval_assurance,
            "approval_source": self.approval_source,
            "outcome": self.outcome,
            "reason": self.reason,
        }


class OtherPartyApprovalPolicy:
    def __init__(self, receipt=None):
        if receipt is not None and not isinstance(receipt, OtherPartyApprovalReceipt):
            raise OtherPartyApprovalError("validated approval receipt is required")
        self.receipt = receipt
        self.calls = 0
        self.decisions = []

    def replace(self, receipt):
        if receipt is not None and not isinstance(receipt, OtherPartyApprovalReceipt):
            raise OtherPartyApprovalError("validated approval receipt is required")
        self.receipt = receipt

    def evaluate(self, *, participant, mission_s256, scope, now):
        self.calls += 1
        if (not isinstance(participant, str) or not participant or
                not isinstance(mission_s256, str) or not mission_s256 or
                scope != DIRECTED_SCOPE or type(now) is not int or now < 0):
            raise OtherPartyApprovalError("exact directed-action inputs are required")
        receipt = self.receipt
        reason = "approval_absent"
        if receipt is not None:
            if receipt.participant != participant:
                reason = "participant_mismatch"
            elif receipt.mission_s256 != mission_s256:
                reason = "mission_mismatch"
            elif receipt.scope != scope:
                reason = "scope_mismatch"
            elif receipt.observed_at > now:
                reason = "approval_not_yet_observed"
            elif receipt.expires_at <= now:
                reason = "approval_expired"
            elif receipt.state != "APPROVED":
                reason = "approval_withdrawn"
            else:
                reason = "approval_active"
        allowed = reason == "approval_active"
        decision = OtherPartyDecisionReceipt(
            policy_version=POLICY_VERSION,
            participant=participant,
            participant_source="agent-asserted-signed-action-body",
            mission_s256=mission_s256,
            scope=scope,
            approval_assurance=(receipt.assurance if receipt is not None
                                else "unverified-demo-input"),
            approval_source=(receipt.source if receipt is not None else "none"),
            outcome="ALLOW" if allowed else "DENY",
            reason=reason,
        )
        self.decisions.append(decision)
        return decision


def _action_candidate(request):
    try:
        value = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if (not isinstance(value, dict) or set(value) != {"participant", "scope"} or
            not isinstance(value["participant"], str) or not value["participant"] or
            not isinstance(value["scope"], str) or not value["scope"]):
        return None
    return value


class ApprovalGovernedResource(Resource):
    def __init__(self, *, issuer, person_server, now, approval_policy):
        super().__init__(issuer=issuer, person_server=person_server, now=now)
        if not isinstance(approval_policy, OtherPartyApprovalPolicy):
            raise OtherPartyApprovalError("valid approval policy is required")
        self.approval_policy = approval_policy
        self.last_decision = None

    def enforce_action(self, request, *, subject, mission_s256):
        self.last_decision = None
        body = _action_candidate(request)
        candidate_scope = (body["scope"] if body is not None
                           else "invalid-action-scope")
        claims = super().enforce(
            request, subject=subject, mission_s256=mission_s256,
            required_scope=candidate_scope)
        if body is None or body["scope"] not in _SCOPES:
            raise OtherPartyApprovalError("exact action body is required")
        if body["scope"] == AMBIENT_SCOPE:
            self.last_decision = None
            return claims
        decision = self.approval_policy.evaluate(
            participant=body["participant"], mission_s256=mission_s256,
            scope=body["scope"], now=self.now)
        self.last_decision = decision
        if decision.outcome != "ALLOW":
            raise OtherPartyApprovalError("other-party approval required")
        return claims


class ApprovalResourceSurface(ResourceSurface):
    def __init__(self, *, resource, subject, mission_s256):
        if not isinstance(resource, ApprovalGovernedResource):
            raise OtherPartyApprovalError("approval-governed resource is required")
        super().__init__(resource=resource, subject=subject,
                         mission_s256=mission_s256,
                         required_scope=DIRECTED_SCOPE)

    def post(self, path, request):
        if path != "/enforce":
            return super().post(path, request)
        try:
            claims = self.resource.enforce_action(
                request, subject=self.subject, mission_s256=self.mission_s256)
        except OtherPartyApprovalError:
            decision = self.resource.last_decision
            return 403, {
                "authorization": "denied",
                "reason": "other_party_approval_required",
                "decision": decision.as_dict() if decision is not None else None,
            }, {}
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
        return 200, {
            "authorization": "allowed", "subject": claims["sub"],
            "mission_s256": claims["mission_s256"], "scope": claims["scope"],
            "decision": (self.resource.last_decision.as_dict()
                         if self.resource.last_decision is not None else None),
        }, {}
