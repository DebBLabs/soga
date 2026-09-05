from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from aauth_permission import PermissionService
from g27_tip_jar.adapter import FakeSurface, TargetBoundAdapter
from g27_tip_jar.lifecycle import SessionGrantService
from g27_tip_jar.runtime import ActionDecision, Decision, PrototypeRuntime
from g27_tip_jar.state_machine import SafetyStateMachine

from .mission import ACTION, AGENT_ID, APPROVER_ID, CATALOG_VERSION, build_mission


PLATFORM_ID = "m01-misty-a-recording-fixture"
NOTICE_VERSION = "m01-notice-v1"
POLICY_VERSION = "m01-policy-v1"
QR_PREFIX = "m01-grant:"


class M01FlowError(RuntimeError):
    def __init__(self, stage: str, code: str):
        super().__init__(f"{stage}: {code}")
        self.stage = stage
        self.code = code


@dataclass(frozen=True)
class QROffer:
    qr_payload: str
    grant_digest: str
    expires_at: float


class M01Flow:
    """Authorized M01 flow over local in-memory and recording-only surfaces.

    QR input contains only an opaque grant reference. SOGA evaluates the
    AAuth-shaped request before the existing G27 runtime records a dispatch.
    No URL, robot endpoint, discovery, or physical transport exists here.
    """

    def __init__(self, *, monotonic: Callable[[], float]) -> None:
        authorized = build_mission()
        self.person_server = PermissionService(
            person_server_id=APPROVER_ID,
            monotonic=monotonic,
        )
        self.mission = self.person_server.approve_mission(
            approver=authorized.approver,
            agent=authorized.agent,
            approved_at=authorized.approved_at,
            approved_tools=[
                {"name": tool.name, "description": tool.description}
                for tool in authorized.approved_tools
            ],
            description=authorized.description,
        )
        if self.mission.s256 != authorized.s256:
            raise M01FlowError("mission", "hash_mismatch")
        self.person_server.authorize_mission_policy(self.mission.s256, {})
        self.sessions = SessionGrantService(monotonic=monotonic)
        self.surface = FakeSurface(PLATFORM_ID)
        self.machine = SafetyStateMachine(PLATFORM_ID)
        self.runtime = PrototypeRuntime(
            sessions=self.sessions,
            adapter=TargetBoundAdapter({PLATFORM_ID: self.surface}),
            state_machines={PLATFORM_ID: self.machine},
        )
        self._action_count: dict[str, int] = {}

    def offer(self, *, grant_id: str | None = None) -> QROffer:
        grant = self.sessions.issue_grant(
            mission_s256=self.mission.s256,
            platform_id=PLATFORM_ID,
            notice_version=NOTICE_VERSION,
            policy_version=POLICY_VERSION,
            issuer=APPROVER_ID,
            grant_id=grant_id,
        )
        return QROffer(
            qr_payload=f"{QR_PREFIX}{grant.grant_id}",
            grant_digest=self.sessions.receipts[-1]["grant_digest"],
            expires_at=grant.expires_at,
        )

    def scan_and_request(
        self,
        qr_payload: str,
        *,
        channel_key: str,
        request_id: str,
        requested_action: str = ACTION,
    ) -> dict:
        grant_id = self._parse_qr(qr_payload)
        if requested_action != ACTION:
            raise M01FlowError("catalog", "action_not_authorized")

        session = self.runtime.initiate_session(
            grant_id,
            platform_id=PLATFORM_ID,
            mission_s256=self.mission.s256,
            notice_version=NOTICE_VERSION,
            policy_version=POLICY_VERSION,
            channel_key=channel_key,
        )
        if self._action_count.get(session.session_id, 0) >= 1:
            raise M01FlowError("cardinality", "session_action_limit")

        status, permission = self.person_server.permission(
            {
                "request_id": request_id,
                "action": requested_action,
                "mission": {"s256": self.mission.s256},
                "agent": AGENT_ID,
                "subject": {
                    "subject_id": "m01-local-test-subject",
                    "subject_agency_state": "INDEPENDENT",
                },
            }
        )
        projection = permission.get("permission")
        if status != 200 or projection != "granted":
            raise M01FlowError("governance", f"permission_{projection or status}")
        soga_entry = self.person_server.mission_log.entries(self.mission.s256)[-2]
        evaluation = soga_entry.payload["soga_decision"]
        if evaluation["governance_determination"] != "ALLOW":
            raise M01FlowError("governance", "projection_mismatch")
        decision_reference = evaluation["canonical_decision_package"][
            "execution_receipt"
        ]

        receipt = self.runtime.submit(
            ActionDecision(
                request_id=request_id,
                decision_reference=decision_reference,
                decision=Decision.ALLOW,
                mission_s256=self.mission.s256,
                session_id=session.session_id,
                platform_id=PLATFORM_ID,
                agent_id=AGENT_ID,
                action=requested_action,
                catalog_version=CATALOG_VERSION,
            ),
            channel_key=channel_key,
        )
        self._action_count[session.session_id] = 1
        return {
            **receipt,
            "mission_s256": self.mission.s256,
            "governance_projection": projection,
            "execution_surface": "recording_only",
            "physical_outcome": "unknown",
        }

    @staticmethod
    def _parse_qr(qr_payload: str) -> str:
        if not qr_payload.startswith(QR_PREFIX):
            raise M01FlowError("qr", "invalid_format")
        grant_id = qr_payload[len(QR_PREFIX) :]
        if not grant_id or ":" in grant_id or "/" in grant_id:
            raise M01FlowError("qr", "invalid_grant_reference")
        return grant_id
