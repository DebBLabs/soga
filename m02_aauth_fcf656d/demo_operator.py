"""Sanitized local-operator seam for the bounded AAuth demonstration."""

import re
import threading
from dataclasses import asdict, dataclass

from .approval_pending import (
    PENDING_ID_PATTERN, PENDING_LIFETIME_SECONDS, PENDING_PREFIX,
    ApprovalPendingError, ApprovalPendingStore,
)
from .other_party_approval import (
    DIRECTED_SCOPE, OtherPartyApprovalError, OtherPartyApprovalPolicy,
    OtherPartyApprovalReceipt,
)


RECEIPT_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{32}\Z")
MAX_RECEIPT_IDS = 1024
ASSERTED_ROLE = "parent"
ASSURANCE = "unverified-demo-input"
SOURCE = "local-operator-demo-control"
EVENT_VERSION = "m02-demo-operator-v1"
HELD_EVENT = "held_other_party_input_recorded"
STANDING_EVENT = "standing_other_party_input_recorded"


class DemoOperatorError(ValueError):
    """Fixed, presentation-safe operator error."""

    def __init__(self, code):
        if code not in {
                "invalid_input", "pending_not_live", "operator_capacity",
                "operator_state_unavailable"}:
            code = "operator_state_unavailable"
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class DemoOperatorEvent:
    version: str
    event: str
    receipt_id: object
    asserted_role: str
    assurance: str
    participant: str
    mission_s256: str
    scope: str
    state: str
    observed_at: int
    expires_at: object
    source: str

    def as_dict(self):
        return asdict(self)


class DemoOperatorAdapter:
    """Serialize local operator input into the two accepted resource seams."""

    def __init__(self, *, store, policy, participant, mission_s256, scope,
                 clock, receipt_id_factory):
        if (not isinstance(store, ApprovalPendingStore) or
                not isinstance(policy, OtherPartyApprovalPolicy) or
                not isinstance(participant, str) or not participant or
                not isinstance(mission_s256, str) or not mission_s256 or
                scope != DIRECTED_SCOPE or not callable(clock) or
                clock is not store.clock or not callable(receipt_id_factory)):
            raise DemoOperatorError("invalid_input")
        self._store = store
        self._policy = policy
        self._participant = participant
        self._mission_s256 = mission_s256
        self._scope = scope
        self._clock = clock
        self._receipt_id_factory = receipt_id_factory
        self._receipt_ids = set()
        self._lock = threading.RLock()

    def _sample_time(self):
        try:
            value = self._clock()
        except Exception as error:
            raise DemoOperatorError("operator_state_unavailable") from None
        if type(value) is not int or value < 0:
            raise DemoOperatorError("invalid_input")
        return value

    def _new_receipt(self, state, now):
        if state not in {"APPROVED", "WITHDRAWN"}:
            raise DemoOperatorError("invalid_input")
        try:
            receipt_id = self._receipt_id_factory()
        except Exception:
            raise DemoOperatorError("operator_state_unavailable") from None
        if (not isinstance(receipt_id, str) or
                RECEIPT_ID_PATTERN.fullmatch(receipt_id) is None):
            raise DemoOperatorError("invalid_input")
        if receipt_id in self._receipt_ids:
            raise DemoOperatorError("invalid_input")
        if len(self._receipt_ids) >= MAX_RECEIPT_IDS:
            raise DemoOperatorError("operator_capacity")
        self._receipt_ids.add(receipt_id)
        try:
            receipt = OtherPartyApprovalReceipt.create({
                "receipt_id": receipt_id,
                "asserted_role": ASSERTED_ROLE,
                "assurance": ASSURANCE,
                "participant": self._participant,
                "mission_s256": self._mission_s256,
                "scope": self._scope,
                "state": state,
                "observed_at": now,
                "expires_at": now + PENDING_LIFETIME_SECONDS,
                "source": SOURCE,
            })
        except OtherPartyApprovalError:
            raise DemoOperatorError("operator_state_unavailable") from None
        return receipt

    def _event(self, event, state, now, receipt=None):
        return DemoOperatorEvent(
            version=EVENT_VERSION,
            event=event,
            receipt_id=receipt.receipt_id if receipt is not None else None,
            asserted_role=ASSERTED_ROLE,
            assurance=ASSURANCE,
            participant=self._participant,
            mission_s256=self._mission_s256,
            scope=self._scope,
            state=state,
            observed_at=now,
            expires_at=receipt.expires_at if receipt is not None else None,
            source=SOURCE,
        )

    def record_held_input(self, pending_path, state):
        if (not isinstance(pending_path, str) or
                not pending_path.startswith(PENDING_PREFIX)):
            raise DemoOperatorError("invalid_input")
        pending_id = pending_path[len(PENDING_PREFIX):]
        if PENDING_ID_PATTERN.fullmatch(pending_id) is None:
            raise DemoOperatorError("invalid_input")
        with self._lock:
            now = self._sample_time()
            receipt = self._new_receipt(state, now)
            try:
                self._store.resolve(pending_id, receipt)
            except ApprovalPendingError:
                raise DemoOperatorError("pending_not_live") from None
            return self._event(HELD_EVENT, state, now, receipt)

    def replace_standing_input(self, state):
        if state not in {"APPROVED", "WITHDRAWN", "CLEARED"}:
            raise DemoOperatorError("invalid_input")
        with self._lock:
            now = self._sample_time()
            receipt = None if state == "CLEARED" else self._new_receipt(state, now)
            try:
                self._policy.replace(receipt)
            except OtherPartyApprovalError:
                raise DemoOperatorError("operator_state_unavailable") from None
            return self._event(STANDING_EVENT, state, now, receipt)
