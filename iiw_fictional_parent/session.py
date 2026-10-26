"""One-use state for the Permission to Speak fictional-parent role-play."""

from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
from dataclasses import dataclass


SCENARIO = "permission-to-speak-fictional-parent-v1"
ACTION_LABEL = "address_fictional_child"
PARTICIPANT = "fictional-child-1"
ROLEPLAY = "fictional-parent-roleplay"
APPROVE = "APPROVE_FICTIONAL_DIRECTED_RESPONSE"
DECLINE = "DECLINE_FICTIONAL_DIRECTED_RESPONSE"
CHOICES = frozenset((APPROVE, DECLINE))
LIFETIME_SECONDS = 30
PRESENTATION_CEILING_SECONDS = 60
CAPABILITY_BYTES = 32


class FictionalParentSessionUnavailable(ValueError):
    """Indistinguishable invalid, terminal, expired or unavailable session."""


@dataclass(frozen=True)
class FictionalParentChoice:
    choice: str
    scenario: str
    action: str
    participant: str
    roleplay: str
    gateway_instance: str


class FictionalParentSession:
    def __init__(self, *, gateway_instance, clock, encounter_started_at,
                 capability_factory=secrets.token_bytes):
        if (not isinstance(gateway_instance, str) or
                not gateway_instance.isascii() or
                not 1 <= len(gateway_instance) <= 64):
            raise ValueError("fixed ASCII gateway instance required")
        if (not callable(clock) or not callable(capability_factory) or
                type(encounter_started_at) is not int or encounter_started_at < 0):
            raise TypeError("clock and capability factory must be callable")
        raw = capability_factory(CAPABILITY_BYTES)
        if not isinstance(raw, bytes) or len(raw) != CAPABILITY_BYTES:
            raise ValueError("capability factory returned invalid entropy")
        now = clock()
        if type(now) is not int or now < 0 or now != encounter_started_at:
            raise ValueError("nonnegative integer clock required")
        capability = raw.hex()
        self._clock = clock
        self._gateway_instance = gateway_instance
        self._encounter_started_at = encounter_started_at
        self._capability = capability
        self._capability_digest = hashlib.sha256(
            capability.encode("ascii")).digest()
        self._expires_at = min(
            now + LIFETIME_SECONDS,
            encounter_started_at + PRESENTATION_CEILING_SECONDS)
        self._terminal = False
        self._lock = threading.Lock()

    @property
    def capability(self):
        with self._lock:
            now = self._clock()
            if type(now) is not int or now >= self._expires_at:
                self._terminal = True
            if self._terminal:
                raise FictionalParentSessionUnavailable("session unavailable")
            return self._capability

    @property
    def expires_at(self):
        return self._expires_at

    @property
    def clock(self):
        return self._clock

    @property
    def encounter_started_at(self):
        return self._encounter_started_at

    def cancel(self):
        with self._lock:
            self._terminal = True

    def submit(self, *, capability, choice, scenario, action, participant,
               roleplay, gateway_instance):
        with self._lock:
            supplied = b""
            if isinstance(capability, str) and capability.isascii():
                supplied = hashlib.sha256(
                    capability.encode("ascii")).digest()
            now = self._clock()
            expired = type(now) is not int or now >= self._expires_at
            if expired:
                self._terminal = True
            valid = (
                not self._terminal and not expired and
                hmac.compare_digest(supplied, self._capability_digest) and
                isinstance(choice, str) and choice in CHOICES and
                scenario == SCENARIO and action == ACTION_LABEL and
                participant == PARTICIPANT and
                roleplay == ROLEPLAY and
                gateway_instance == self._gateway_instance
            )
            if not valid:
                raise FictionalParentSessionUnavailable("session unavailable")
            self._terminal = True
            return FictionalParentChoice(
                choice=choice, scenario=scenario, action=action,
                participant=participant, roleplay=roleplay,
                gateway_instance=gateway_instance)
