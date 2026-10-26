"""Held-request-only connection from fictional role-play to accepted seams."""

from __future__ import annotations

import threading
from dataclasses import dataclass

from m02_aauth_fcf656d.approval_pending import ApprovalPendingStore
from m02_aauth_fcf656d.demo_operator import (
    DemoOperatorAdapter, DemoOperatorError,
)
from m02_aauth_fcf656d.other_party_approval import (
    DIRECTED_SCOPE, OtherPartyApprovalPolicy,
)

from .session import (
    ACTION_LABEL, APPROVE, DECLINE, PARTICIPANT, ROLEPLAY, SCENARIO,
    FictionalParentChoice, FictionalParentSession,
)


MISSION_S256 = "mission-sha256"
LEGACY_SCOPE = DIRECTED_SCOPE
APPROVAL_SOURCE = "local-operator-demo-control"
MAX_CLAIMED_PATHS = 1024
_CLAIM_LOCK = threading.Lock()
_CLAIMED_PATHS = set()


class FictionalParentConnectionUnavailable(ValueError):
    pass


@dataclass(frozen=True)
class FictionalParentConnectionEvent:
    state: str
    scenario: str
    action: str
    participant: str
    roleplay: str
    assurance: str
    approval_source: str


class FictionalParentConnection:
    """Own exactly one adapter and pending path for exactly one encounter."""

    def __init__(self, *, store, policy, pending_path, clock,
                 encounter_started_at,
                 receipt_id_factory, scenario=SCENARIO,
                 action=ACTION_LABEL, participant=PARTICIPANT,
                 roleplay=ROLEPLAY, mission_s256=MISSION_S256,
                 scope=LEGACY_SCOPE):
        if (not isinstance(store, ApprovalPendingStore) or
                not isinstance(policy, OtherPartyApprovalPolicy) or
                clock is not store.clock or not callable(receipt_id_factory) or
                scenario != SCENARIO or action != ACTION_LABEL or
                participant != PARTICIPANT or roleplay != ROLEPLAY or
                mission_s256 != MISSION_S256 or scope != LEGACY_SCOPE or
                not isinstance(pending_path, str) or
                type(encounter_started_at) is not int or
                clock() != encounter_started_at):
            raise FictionalParentConnectionUnavailable("session unavailable")
        claim = (store, pending_path)
        with _CLAIM_LOCK:
            if claim in _CLAIMED_PATHS or len(_CLAIMED_PATHS) >= MAX_CLAIMED_PATHS:
                raise FictionalParentConnectionUnavailable("session unavailable")
            _CLAIMED_PATHS.add(claim)
        self._adapter = DemoOperatorAdapter(
            store=store, policy=policy, participant=participant,
            mission_s256=mission_s256, scope=scope, clock=clock,
            receipt_id_factory=receipt_id_factory)
        self._pending_path = pending_path
        self._clock = clock
        self._encounter_started_at = encounter_started_at
        self._lock = threading.Lock()
        self._terminal = False

    def record(self, event):
        with self._lock:
            if (self._terminal or
                    not isinstance(event, FictionalParentChoice) or
                    event.scenario != SCENARIO or
                    event.action != ACTION_LABEL or
                    event.participant != PARTICIPANT or
                    event.roleplay != ROLEPLAY or
                    event.choice not in {APPROVE, DECLINE}):
                raise FictionalParentConnectionUnavailable("session unavailable")
            self._terminal = True
            path, self._pending_path = self._pending_path, None
            state = "APPROVED" if event.choice == APPROVE else "WITHDRAWN"
            try:
                accepted = self._adapter.record_held_input(path, state)
            except DemoOperatorError:
                raise FictionalParentConnectionUnavailable(
                    "session unavailable") from None
            return FictionalParentConnectionEvent(
                state=state, scenario=SCENARIO, action=ACTION_LABEL,
                participant=PARTICIPANT, roleplay=ROLEPLAY,
                assurance=accepted.assurance,
                approval_source=accepted.source)

    @property
    def clock(self):
        return self._clock

    @property
    def encounter_started_at(self):
        return self._encounter_started_at


def create_connection(**values):
    """Composition factory; returns no adapter reference outside the connection."""
    return FictionalParentConnection(**values)


def create_encounter(*, gateway_instance, capability_factory, **values):
    """Create the only session and connection for one same-tick encounter."""
    clock = values.get("clock")
    if not callable(clock):
        raise FictionalParentConnectionUnavailable("session unavailable")
    started = clock()
    values["encounter_started_at"] = started
    connected = create_connection(**values)
    qr_session = FictionalParentSession(
        gateway_instance=gateway_instance, clock=clock,
        encounter_started_at=started,
        capability_factory=capability_factory)
    return qr_session, connected
