"""Public surface for the bounded fictional-parent demonstration profile."""

from .connection import (
    APPROVAL_SOURCE, LEGACY_SCOPE, MISSION_S256,
    FictionalParentConnection, FictionalParentConnectionEvent,
    FictionalParentConnectionUnavailable, create_connection, create_encounter,
)
from .gateway import handler_for, participant_url, server_for
from .session import (
    ACTION_LABEL, APPROVE, DECLINE, LIFETIME_SECONDS, PARTICIPANT, ROLEPLAY,
    SCENARIO, FictionalParentChoice, FictionalParentSession,
    FictionalParentSessionUnavailable,
)

__all__ = (
    "ACTION_LABEL", "APPROVAL_SOURCE", "APPROVE", "DECLINE",
    "FictionalParentChoice", "FictionalParentConnection",
    "FictionalParentConnectionEvent", "FictionalParentConnectionUnavailable",
    "FictionalParentSession", "FictionalParentSessionUnavailable",
    "LEGACY_SCOPE", "LIFETIME_SECONDS", "MISSION_S256", "PARTICIPANT",
    "ROLEPLAY", "SCENARIO", "create_connection", "create_encounter", "handler_for",
    "participant_url", "server_for",
)
