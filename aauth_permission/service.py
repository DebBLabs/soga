from __future__ import annotations

import time
import uuid
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from engines.aauth_execution_runtime_bridge import evaluate_aauth_execution_request

from .models import Mission, MissionLog, ProvisionalG26ApprovalEvidence


class PermissionService:
    """Mock AAuth Person Server permission surface for G26."""

    def __init__(
        self,
        *,
        deferred_response_supported: bool = True,
        internally_dischargeable_modes: frozenset[str] = frozenset(),
        pending_expiry_seconds: float | None = None,
        retry_after_seconds: int = 30,
        person_server_id: str = "https://person.example",
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self.deferred_response_supported = deferred_response_supported
        self.internally_dischargeable_modes = internally_dischargeable_modes
        self.pending_expiry_seconds = pending_expiry_seconds
        self.retry_after_seconds = retry_after_seconds
        self.person_server_id = person_server_id
        self.monotonic = monotonic
        self.missions: dict[str, Mission] = {}
        self.mission_policies: dict[str, dict[str, Any]] = {}
        self.mission_log = MissionLog()
        self.pending: dict[str, dict[str, Any]] = {}

    def approve_mission(self, **values: Any) -> Mission:
        mission = Mission.approve(**values)
        self.missions[mission.s256] = mission
        self.mission_log.append(
            mission.s256,
            kind="mission_approved",
            actor=mission.approver,
            attribution="person",
            payload={"mission": mission.to_dict()},
        )
        return mission

    def authorize_mission_policy(
        self, mission_s256: str, policy: Mapping[str, Any]
    ) -> None:
        if mission_s256 not in self.missions:
            raise KeyError(f"unknown mission: {mission_s256}")
        self.mission_policies[mission_s256] = dict(policy)

    def permission(self, request: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
        mission = self._mission_for(request.get("mission"))
        agent = str(request.get("agent") or (mission.agent if mission else "agent"))
        execution_request = self._execution_request(request, mission, agent)
        evaluation = evaluate_aauth_execution_request(execution_request)
        soga = evaluation["governance_determination"]
        mode = self._restriction_mode(evaluation)

        if soga == "ALLOW":
            status, response, projection = 200, {"permission": "granted"}, "granted"
        elif soga == "DENY":
            status, response, projection = 200, {"permission": "denied"}, "denied"
        elif mode in self.internally_dischargeable_modes and mode != "fail_closed":
            status, response, projection = 200, {"permission": "granted"}, "granted_after_internal_discharge"
        elif mode == "HOLDING" and self._can_defer_approval():
            pending_id = f"pending-{uuid.uuid4().hex}"
            pending_url = f"/pending/{pending_id}"
            response = self._pending_body(pending_id, pending_url)
            constraint = evaluation["governance_decision"]["restrict_mode"]["constraint"]
            self.pending[pending_id] = {
                "state": "pending",
                "created_monotonic": self.monotonic(),
                "expires_after_seconds": self.pending_expiry_seconds,
                "agent": agent,
                "mission_s256": mission.s256 if mission else None,
                "action": request["action"],
                "constraint": dict(constraint),
                "originating_soga_decision": evaluation,
                "request": dict(request),
                "terminal": None,
                "delivered": False,
                "approval_evidence": None,
            }
            status, projection = 202, "deferred_approval"
        else:
            status = 200
            response = {
                "permission": "denied",
                "reason": self._fail_closed_reason(mode),
            }
            projection = "denied_with_reason_fallback"

        if mission:
            self._log_soga_and_projection(
                mission.s256, request["action"], evaluation, projection, status, response
            )
        return status, response

    def record_approval(
        self,
        pending_id: str,
        *,
        result: str,
        asserted_by: str,
        person_server_authenticated_assertion: bool,
        authority_reference: str,
        required_evidence: str,
        constraint_reference: str,
        holder_attribution_asserted: bool,
        human_attribution: str | None = None,
    ) -> tuple[int, dict[str, Any]]:
        pending = self.pending[pending_id]
        if pending["state"] != "pending":
            raise ValueError("pending request is already terminal")
        if result not in {"approve", "decline"}:
            raise ValueError("result must be approve or decline")
        if asserted_by != self.person_server_id or not person_server_authenticated_assertion:
            raise PermissionError("approval assertion is not authenticated by this Person Server")

        constraint = pending["constraint"]
        evidence = ProvisionalG26ApprovalEvidence(
            pending_id=pending_id,
            evaluation_reference=pending["originating_soga_decision"]["canonical_decision_package"]["execution_receipt"],
            mission_s256=pending["mission_s256"],
            action=pending["action"],
            originating_soga_decision="RESTRICT",
            constraint_reference=constraint_reference,
            restrict_path="HOLDING",
            required_evidence=required_evidence,
            authority_reference=authority_reference,
            asserted_by=asserted_by,
            person_server_authenticated_assertion=person_server_authenticated_assertion,
            holder_attribution_asserted=holder_attribution_asserted,
            human_attribution=human_attribution,
            result=result,
            recorded_at=datetime.now(timezone.utc).isoformat(),
            provenance="Person Server authenticated approval assertion",
        )

        if result == "decline":
            pending["approval_evidence"] = evidence.to_dict()
            pending["terminal"] = (
                403,
                {"error": "denied", "detail": "The approver declined the request."},
            )
            pending["state"] = "terminal"
            self._log_approval(pending, evidence)
            self._log_final_projection(pending, "approval_declined", *pending["terminal"])
            return 200, {"status": "recorded", "result": "decline"}

        reeval_request = dict(pending["request"])
        reeval_request["request_id"] = f"{reeval_request.get('request_id') or pending_id}-reevaluation"
        mission = self._mission_for(reeval_request.get("mission"))
        execution_request = self._execution_request(
            reeval_request,
            mission,
            pending["agent"],
            trusted_approval_evidence=evidence.to_dict(),
        )
        reevaluation = evaluate_aauth_execution_request(execution_request)
        evidence = replace(
            evidence,
            reevaluation_reference=reevaluation["canonical_decision_package"]["execution_receipt"],
            reevaluation_result=reevaluation["governance_determination"],
        )
        pending["approval_evidence"] = evidence.to_dict()
        pending["reevaluation"] = reevaluation
        self._log_approval(pending, evidence)
        self.mission_log.append(
            pending["mission_s256"],
            kind="soga_reevaluation_decision",
            actor="soga-governance-engine",
            attribution="delegate_acting_for_person-server",
            payload={
                "pending_id": pending_id,
                "same_mission_s256": pending["mission_s256"],
                "same_action": pending["action"],
                "same_subject": reeval_request.get("subject"),
                "soga_decision": reevaluation,
            },
        )

        if reevaluation["governance_determination"] == "ALLOW":
            terminal = (200, {"permission": "granted"})
            projection = "granted_after_approval_reevaluation"
        elif reevaluation["governance_determination"] == "DENY":
            terminal = (200, {"permission": "denied"})
            projection = "denied_after_approval_reevaluation"
        else:
            terminal = (
                200,
                {
                    "permission": "denied",
                    "reason": "Approval evidence did not satisfy the authorized HOLDING constraint.",
                },
            )
            projection = "denied_after_unsatisfied_approval_evidence"
        pending["terminal"] = terminal
        pending["state"] = "terminal"
        self._log_final_projection(pending, projection, *terminal)
        return 200, {"status": "recorded", "result": "approve"}

    def poll(self, pending_id: str, *, agent: str) -> tuple[int, dict[str, Any]]:
        pending = self.pending[pending_id]
        if agent != pending["agent"]:
            raise PermissionError("pending request does not belong to this agent")
        self._expire_if_needed(pending_id, pending)
        if pending["state"] == "pending":
            return 202, self._pending_body(pending_id, f"/pending/{pending_id}")
        if pending["delivered"]:
            return 410, {"error": "invalid_code", "detail": "Pending response already consumed."}
        pending["delivered"] = True
        return pending["terminal"]

    def _can_defer_approval(self) -> bool:
        return self.deferred_response_supported and self.pending_expiry_seconds is not None

    def _expire_if_needed(self, pending_id: str, pending: dict[str, Any]) -> None:
        if pending["state"] != "pending":
            return
        if self.monotonic() - pending["created_monotonic"] < pending["expires_after_seconds"]:
            return
        pending["state"] = "terminal"
        pending["terminal"] = (408, {"error": "expired", "detail": "The approval request expired."})
        self._log_final_projection(pending, "approval_expired", *pending["terminal"])

    def _log_soga_and_projection(self, mission_s256, action, evaluation, projection, status, response):
        self.mission_log.append(
            mission_s256,
            kind="soga_decision",
            actor="soga-governance-engine",
            attribution="delegate_acting_for_person-server",
            payload={"action": action, "soga_decision": evaluation},
        )
        self.mission_log.append(
            mission_s256,
            kind="aauth_projection",
            actor=self.person_server_id,
            attribution="person-server",
            payload={"action": action, "aauth_projection": projection, "status": status, "aauth_response": response},
        )

    def _log_approval(self, pending, evidence):
        self.mission_log.append(
            pending["mission_s256"],
            kind="provisional_g26_approval_evidence",
            actor=self.person_server_id,
            attribution="person-server-authenticated-assertion",
            payload=evidence.to_dict(),
        )

    def _log_final_projection(self, pending, projection, status, response):
        self.mission_log.append(
            pending["mission_s256"],
            kind="aauth_final_projection",
            actor=self.person_server_id,
            attribution="person-server",
            payload={"pending_id": pending["approval_evidence"]["pending_id"] if pending.get("approval_evidence") else None, "aauth_projection": projection, "status": status, "aauth_response": response},
        )

    def _pending_body(self, pending_id: str, pending_url: str) -> dict[str, Any]:
        return {"status": "pending", "pending_id": pending_id, "pending_url": pending_url, "requirement": "approval"}

    @staticmethod
    def _restriction_mode(evaluation: Mapping[str, Any]) -> str | None:
        restrict_mode = evaluation["governance_decision"].get("restrict_mode")
        return restrict_mode.get("mode") if isinstance(restrict_mode, dict) else restrict_mode

    def _fail_closed_reason(self, mode: str | None) -> str:
        if mode == "fail_closed":
            return "SOGA RESTRICT has no authorized operational path; no path was inferred."
        if mode == "HOLDING" and self.pending_expiry_seconds is None:
            return "HOLDING approval cannot be deferred without configured expiry policy."
        return "SOGA restriction cannot be safely represented by this implementation."

    def _mission_for(self, reference: Any) -> Mission | None:
        if reference is None:
            return None
        s256 = reference if isinstance(reference, str) else reference.get("s256")
        if s256 not in self.missions:
            raise KeyError(f"unknown mission: {s256}")
        return self.missions[s256]

    def _execution_request(
        self,
        request: Mapping[str, Any],
        mission: Mission | None,
        agent: str,
        *,
        trusted_approval_evidence: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        subject = dict(request.get("subject", {}))
        policy = (
            dict(self.mission_policies.get(mission.s256, {}))
            if mission
            else dict(request.get("policy", {}))
        )
        policy.pop("approval_evidence", None)
        if mission:
            policy["mission_s256"] = mission.s256
        if trusted_approval_evidence is not None:
            policy["approval_evidence"] = dict(trusted_approval_evidence)
        return {
            "request_id": request.get("request_id"),
            "agent_url": agent,
            "action": request["action"],
            "message": request.get("description") or request["action"],
            "mission": {
                "mission_id": mission.s256,
                "description": mission.description,
                "allowed_actions": [tool.name for tool in mission.approved_tools],
                "references": {"aauth_mission": mission.to_dict()},
            } if mission else {},
            "authority": {
                "authority_id": mission.s256 if mission else "permission-without-mission",
                "allowed_actions": [request["action"]],
            },
            "subject": subject,
            "reachability": request.get("reachability", "REACHABLE"),
            "policy": policy,
        }
