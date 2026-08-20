from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from threading import RLock
from typing import Callable, Dict, Optional
from uuid import uuid4


class GrantState(str, Enum):
    ISSUED = "issued"
    CONSUMED = "consumed"
    EXPIRED = "expired"
    INVALIDATED = "invalidated"


class SessionState(str, Enum):
    LIVE = "live"
    NORMALLY_CLOSED = "normally_closed"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"
    DISTRESS_STOPPED = "distress_stopped"
    SAFETY_STOPPED = "safety_stopped"
    FAILED = "failed"


TERMINAL_SESSION_STATES = frozenset(state for state in SessionState if state != SessionState.LIVE)


class LifecycleError(RuntimeError):
    def __init__(self, stage: str, code: str):
        super().__init__(f"{stage}: {code}")
        self.stage = stage
        self.code = code


@dataclass
class Grant:
    grant_id: str
    mission_s256: str
    platform_id: str
    notice_version: str
    policy_version: str
    issuer: str
    issued_at: float
    expires_at: float
    state: GrantState = GrantState.ISSUED
    consumed_at: Optional[float] = None
    session_id: Optional[str] = None


@dataclass
class Session:
    session_id: str
    grant_id: str
    mission_s256: str
    platform_id: str
    channel_key: str
    created_at: float
    hard_expires_at: float
    idle_expires_at: float
    state: SessionState = SessionState.LIVE
    terminal_cause: Optional[str] = None
    terminal_at: Optional[float] = None
    action_receipts: Dict[str, dict] = field(default_factory=dict)


class SessionGrantService:
    """Process-local G27 lifecycle prototype.

    The single RLock makes grant consumption and the one-live-session policy
    atomic between threads in this process. It intentionally does not claim
    multi-process or distributed atomicity.
    """

    MULTI_PROCESS_ATOMICITY_GAP = (
        "Atomic grant consumption and the one-live-session policy are not "
        "enforced across multiple processes or hosts."
    )

    def __init__(
        self,
        *,
        monotonic: Callable[[], float],
        grant_lifetime_seconds: int = 600,
        idle_timeout_seconds: int = 60,
        hard_session_seconds: int = 300,
    ) -> None:
        self._now = monotonic
        self.grant_lifetime_seconds = grant_lifetime_seconds
        self.idle_timeout_seconds = idle_timeout_seconds
        self.hard_session_seconds = hard_session_seconds
        self._lock = RLock()
        self.grants: Dict[str, Grant] = {}
        self.sessions: Dict[str, Session] = {}
        self.active_session_id: Optional[str] = None
        self.receipts: list[dict] = []

    def issue_grant(
        self,
        *,
        mission_s256: str,
        platform_id: str,
        notice_version: str,
        policy_version: str,
        issuer: str,
        grant_id: Optional[str] = None,
    ) -> Grant:
        required = {
            "mission_s256": mission_s256,
            "platform_id": platform_id,
            "notice_version": notice_version,
            "policy_version": policy_version,
            "issuer": issuer,
        }
        if any(not value for value in required.values()):
            raise LifecycleError("issuance", "missing_binding")
        now = self._now()
        grant = Grant(
            grant_id=grant_id or f"grant-{uuid4().hex}",
            mission_s256=mission_s256,
            platform_id=platform_id,
            notice_version=notice_version,
            policy_version=policy_version,
            issuer=issuer,
            issued_at=now,
            expires_at=now + self.grant_lifetime_seconds,
        )
        with self._lock:
            if grant.grant_id in self.grants:
                raise LifecycleError("issuance", "duplicate_grant_id")
            self.grants[grant.grant_id] = grant
            self.receipts.append(
                {
                    "event": "grant_issued",
                    "grant_digest": self._grant_digest(grant.grant_id),
                    "mission_s256": grant.mission_s256,
                    "platform_id": grant.platform_id,
                    "notice_version": grant.notice_version,
                    "policy_version": grant.policy_version,
                    "issuer": grant.issuer,
                    "issued_at": grant.issued_at,
                    "expires_at": grant.expires_at,
                    "state": grant.state.value,
                }
            )
        return grant

    def inspect(self, grant_id: str) -> dict:
        with self._lock:
            grant = self._grant(grant_id)
            self._expire_grant_if_needed(grant)
            return {
                "grant_id": grant.grant_id,
                "mission_s256": grant.mission_s256,
                "platform_id": grant.platform_id,
                "notice_version": grant.notice_version,
                "policy_version": grant.policy_version,
                "state": grant.state.value,
                "expires_at": grant.expires_at,
            }

    def initiate_and_consume(
        self,
        grant_id: str,
        *,
        platform_id: str,
        mission_s256: str,
        notice_version: str,
        policy_version: str,
        channel_key: str,
    ) -> Session:
        with self._lock:
            grant = self._grant(grant_id)
            self._expire_grant_if_needed(grant)
            if grant.state == GrantState.EXPIRED:
                raise LifecycleError("grant_validation", "expired")
            if grant.state != GrantState.ISSUED:
                raise LifecycleError("grant_consumption", "reused_or_invalid")
            if not channel_key:
                raise LifecycleError("channel_binding", "missing_channel_key")
            supplied = (platform_id, mission_s256, notice_version, policy_version)
            expected = (
                grant.platform_id,
                grant.mission_s256,
                grant.notice_version,
                grant.policy_version,
            )
            if supplied != expected:
                raise LifecycleError("grant_binding", "binding_mismatch")
            self._clear_terminal_active_reference()
            if self.active_session_id is not None:
                raise LifecycleError("session_concurrency", "active_session_exists")

            now = self._now()
            session = Session(
                session_id=f"session-{uuid4().hex}",
                grant_id=grant.grant_id,
                mission_s256=grant.mission_s256,
                platform_id=grant.platform_id,
                channel_key=channel_key,
                created_at=now,
                hard_expires_at=now + self.hard_session_seconds,
                idle_expires_at=now + self.idle_timeout_seconds,
            )
            grant.state = GrantState.CONSUMED
            grant.consumed_at = now
            grant.session_id = session.session_id
            self.sessions[session.session_id] = session
            self.active_session_id = session.session_id
            self.receipts.append(
                {
                    "event": "session_initiated",
                    "session_id": session.session_id,
                    "grant_digest": self._grant_digest(grant.grant_id),
                    "mission_s256": grant.mission_s256,
                    "platform_id": grant.platform_id,
                    "consumption": "atomic_in_process",
                    "created_at": now,
                }
            )
            return session

    def invalidate_grant(self, grant_id: str) -> Grant:
        with self._lock:
            grant = self._grant(grant_id)
            self._expire_grant_if_needed(grant)
            if grant.state != GrantState.ISSUED:
                raise LifecycleError("grant_invalidation", f"terminal_{grant.state.value}")
            grant.state = GrantState.INVALIDATED
            self.receipts.append(
                {
                    "event": "grant_invalidated",
                    "grant_digest": self._grant_digest(grant.grant_id),
                    "mission_s256": grant.mission_s256,
                    "platform_id": grant.platform_id,
                    "invalidated_at": self._now(),
                }
            )
            return grant

    def validate_session(
        self,
        session_id: str,
        *,
        channel_key: str,
        platform_id: str,
        participant_activity: bool = False,
    ) -> Session:
        with self._lock:
            session = self._session(session_id)
            self._expire_session_if_needed(session)
            if session.state != SessionState.LIVE:
                raise LifecycleError("session_validation", f"terminal_{session.state.value}")
            if session.channel_key != channel_key:
                raise LifecycleError("channel_binding", "wrong_channel")
            if session.platform_id != platform_id:
                raise LifecycleError("session_binding", "wrong_platform")
            if participant_activity:
                session.idle_expires_at = min(
                    self._now() + self.idle_timeout_seconds,
                    session.hard_expires_at,
                )
            return session

    def terminate(self, session_id: str, cause: SessionState) -> Session:
        if cause not in TERMINAL_SESSION_STATES:
            raise LifecycleError("session_termination", "nonterminal_cause")
        with self._lock:
            session = self._session(session_id)
            if session.state != SessionState.LIVE:
                if session.state == cause:
                    return session
                raise LifecycleError("session_termination", "already_terminal")
            self._set_terminal(session, cause)
            return session

    def record_action_receipt(self, session_id: str, request_id: str, receipt: dict) -> dict:
        with self._lock:
            session = self._session(session_id)
            prior = session.action_receipts.get(request_id)
            if prior is not None:
                return dict(prior)
            session.action_receipts[request_id] = dict(receipt)
            return dict(receipt)

    def prior_action_receipt(self, session_id: str, request_id: str) -> Optional[dict]:
        with self._lock:
            prior = self._session(session_id).action_receipts.get(request_id)
            return None if prior is None else dict(prior)

    def live_session_for_platform(self, platform_id: str) -> Optional[Session]:
        with self._lock:
            self._clear_terminal_active_reference()
            if self.active_session_id is None:
                return None
            session = self.sessions[self.active_session_id]
            return session if session.platform_id == platform_id else None

    def _grant(self, grant_id: str) -> Grant:
        try:
            return self.grants[grant_id]
        except KeyError as exc:
            raise LifecycleError("grant_lookup", "unknown_grant") from exc

    def _session(self, session_id: str) -> Session:
        try:
            return self.sessions[session_id]
        except KeyError as exc:
            raise LifecycleError("session_lookup", "unknown_session") from exc

    def _expire_grant_if_needed(self, grant: Grant) -> None:
        if grant.state == GrantState.ISSUED and self._now() >= grant.expires_at:
            grant.state = GrantState.EXPIRED

    def _expire_session_if_needed(self, session: Session) -> None:
        if session.state != SessionState.LIVE:
            return
        if self._now() >= session.hard_expires_at or self._now() >= session.idle_expires_at:
            self._set_terminal(session, SessionState.EXPIRED)

    def _set_terminal(self, session: Session, cause: SessionState) -> None:
        session.state = cause
        session.terminal_cause = cause.value
        session.terminal_at = self._now()
        if self.active_session_id == session.session_id:
            self.active_session_id = None
        self.receipts.append(
            {
                "event": "session_terminated",
                "session_id": session.session_id,
                "mission_s256": session.mission_s256,
                "platform_id": session.platform_id,
                "terminal_cause": cause.value,
                "terminal_at": session.terminal_at,
                "pending_action_disposition": "stale",
                "non_reuse": True,
            }
        )

    def _clear_terminal_active_reference(self) -> None:
        if self.active_session_id is None:
            return
        session = self.sessions[self.active_session_id]
        self._expire_session_if_needed(session)
        if session.state in TERMINAL_SESSION_STATES:
            self.active_session_id = None

    @staticmethod
    def _grant_digest(grant_id: str) -> str:
        return sha256(grant_id.encode("utf-8")).hexdigest()
