from __future__ import annotations

import uuid
from dataclasses import asdict
from typing import Any, Mapping

from engines.aauth_execution_runtime_bridge import evaluate_aauth_execution_request

from .models import Mission, MissionLog


class PermissionService:
    """Mock AAuth Person Server permission surface for G26."""

    def __init__(
        self,
        *,
        deferred_response_supported: bool = True,
        internally_dischargeable_modes: frozenset[str] = frozenset(),
    ) -> None:
        self.deferred_response_supported = deferred_response_supported
        self.internally_dischargeable_modes = internally_dischargeable_modes
        self.missions: dict[str, Mission] = {}
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

    def permission(self, request: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
        mission = self._mission_for(request.get("mission"))
        agent = str(request.get("agent") or (mission.agent if mission else "agent"))
        evaluation = evaluate_aauth_execution_request(
            self._execution_request(request, mission, agent)
        )
        soga = evaluation["governance_determination"]

        if soga == "ALLOW":
            status, response, projection = 200, {"permission": "granted"}, "granted"
        elif soga == "DENY":
            status, response, projection = 200, {"permission": "denied"}, "denied"
        elif self._restriction_mode(evaluation) in self.internally_dischargeable_modes:
            status, response, projection = 200, {"permission": "granted"}, "granted_after_internal_discharge"
        elif self.deferred_response_supported:
            pending_id = f"pending-{uuid.uuid4().hex[:12]}"
            response = {
                "status": "pending",
                "pending_id": pending_id,
                "pending_url": f"/pending/{pending_id}",
                "requirement": "interaction",
            }
            self.pending[pending_id] = {
                "state": "pending",
                "soga_decision": evaluation,
                "request": dict(request),
            }
            status, projection = 202, "deferred"
        else:
            # Authorized August fallback. AAuth has no structured carrier for
            # the residual SOGA restriction; do not export an unenforced duty.
            status = 200
            response = {
                "permission": "denied",
                "reason": "SOGA requires pre-grant agent participation that this implementation cannot safely represent.",
            }
            projection = "denied_with_reason_fallback"

        if mission:
            self.mission_log.append(
                mission.s256,
                kind="permission_decision",
                actor="soga-governance-engine",
                attribution="delegate_acting_for_person-server",
                payload={
                    "action": request["action"],
                    "soga_decision": evaluation,
                    "aauth_projection": projection,
                    "aauth_response": response,
                },
            )
        return status, response

    @staticmethod
    def _restriction_mode(evaluation: Mapping[str, Any]) -> str | None:
        restrict_mode = evaluation["governance_decision"].get("restrict_mode")
        return restrict_mode.get("mode") if isinstance(restrict_mode, dict) else restrict_mode

    def poll(self, pending_id: str) -> tuple[int, dict[str, Any]]:
        # G26 intentionally defines no timeout or implicit termination.
        pending = self.pending[pending_id]
        if pending["state"] == "pending":
            return 202, {
                "status": "pending",
                "pending_id": pending_id,
                "pending_url": f"/pending/{pending_id}",
                "requirement": "interaction",
            }
        return 200, dict(pending["response"])

    def _mission_for(self, reference: Any) -> Mission | None:
        if reference is None:
            return None
        s256 = reference if isinstance(reference, str) else reference.get("s256")
        if s256 not in self.missions:
            raise KeyError(f"unknown mission: {s256}")
        return self.missions[s256]

    @staticmethod
    def _execution_request(
        request: Mapping[str, Any], mission: Mission | None, agent: str
    ) -> dict[str, Any]:
        subject = dict(request.get("subject", {}))
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
            "policy": dict(request.get("policy", {})),
        }
