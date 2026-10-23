"""Pure state machine for one bounded adult-participant QR session."""

from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
from dataclasses import dataclass
from typing import Callable, Optional


ALLOW_DIRECTED_RESPONSE = "ALLOW_DIRECTED_RESPONSE"
DECLINE_DIRECTED_RESPONSE = "DECLINE_DIRECTED_RESPONSE"
CHOICES = frozenset((ALLOW_DIRECTED_RESPONSE, DECLINE_DIRECTED_RESPONSE))
FIXTURE_MISSION = "iiw-adult-participant-fixture-v1"
FIXTURE_ACTION = "address_participant"
FIXTURE_PARTICIPANT = "adult-demo-participant"
MAX_LIFETIME_SECONDS = 120
CAPABILITY_BYTES = 32


class SessionUnavailable(ValueError):
    """Publicly indistinguishable terminal or invalid session outcome."""


@dataclass(frozen=True)
class ParticipantChoice:
    choice: str
    mission: str
    action: str
    participant: str
    gateway_instance: str


class ParticipantSession:
    """At most one choice, bound to one fixture context and monotonic expiry."""

    def __init__(self, *, gateway_instance: str, clock: Callable[[], float],
                 lifetime_seconds: int = MAX_LIFETIME_SECONDS,
                 capability_factory: Callable[[int], bytes] = secrets.token_bytes):
        if not isinstance(gateway_instance, str) or not gateway_instance.isascii():
            raise ValueError("fixed ASCII gateway instance required")
        if not 1 <= len(gateway_instance) <= 64:
            raise ValueError("gateway instance length out of range")
        if not callable(clock) or not callable(capability_factory):
            raise TypeError("clock and capability factory must be callable")
        if (isinstance(lifetime_seconds, bool) or
                not isinstance(lifetime_seconds, int) or
                not 1 <= lifetime_seconds <= MAX_LIFETIME_SECONDS):
            raise ValueError("session lifetime out of range")
        raw = capability_factory(CAPABILITY_BYTES)
        if not isinstance(raw, bytes) or len(raw) != CAPABILITY_BYTES:
            raise ValueError("capability factory returned invalid entropy")
        now = float(clock())
        self._clock = clock
        self._expires_at = now + lifetime_seconds
        self._gateway_instance = gateway_instance
        self._capability = raw.hex()
        self._capability_digest = hashlib.sha256(self._capability.encode("ascii")).digest()
        self._terminal = False
        self._lock = threading.Lock()

    @property
    def capability(self) -> str:
        with self._lock:
            if float(self._clock()) >= self._expires_at:
                self._terminal = True
            if self._terminal:
                raise SessionUnavailable("session unavailable")
            return self._capability

    @property
    def expires_at(self) -> float:
        return self._expires_at

    def cancel(self) -> None:
        with self._lock:
            self._terminal = True

    def submit(self, *, capability: str, choice: str, mission: str,
               action: str, participant: str,
               gateway_instance: str) -> ParticipantChoice:
        with self._lock:
            supplied = b""
            if isinstance(capability, str) and capability.isascii():
                supplied = hashlib.sha256(capability.encode("ascii")).digest()
            bindings_match = (
                mission == FIXTURE_MISSION and action == FIXTURE_ACTION and
                participant == FIXTURE_PARTICIPANT and
                gateway_instance == self._gateway_instance
            )
            expired = float(self._clock()) >= self._expires_at
            if expired:
                self._terminal = True
            valid = (
                not self._terminal and not expired and
                hmac.compare_digest(supplied, self._capability_digest) and
                isinstance(choice, str) and choice in CHOICES and bindings_match
            )
            if not valid:
                raise SessionUnavailable("session unavailable")
            self._terminal = True
            return ParticipantChoice(
                choice=choice, mission=mission, action=action,
                participant=participant, gateway_instance=gateway_instance)

