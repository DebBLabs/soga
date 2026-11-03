from __future__ import annotations

from copy import deepcopy
from threading import RLock

from g27_tip_jar.adapter import Invocation


MBOT2_UNAVAILABLE_PLATFORM_ID = "urn:debblabs:mbot2-iiw:unavailable"


class UnavailableMbot2Adapter:
    """Explicit zero-I/O placeholder. It cannot accept a transport or address."""

    platform_id = MBOT2_UNAVAILABLE_PLATFORM_ID

    def __init__(self) -> None:
        self._receipts: dict[str, dict[str, object]] = {}
        self._invocations: dict[str, Invocation] = {}
        self._lock = RLock()

    def _receipt(self, invocation: Invocation, bound_platform_id: str, operation: str) -> dict[str, object]:
        with self._lock:
            prior_invocation = self._invocations.get(invocation.request_id)
            if prior_invocation is not None and prior_invocation != invocation:
                raise ValueError("request_binding_conflict")
            self._invocations.setdefault(invocation.request_id, invocation)
            prior = self._receipts.get(invocation.request_id + ":" + operation)
            if prior is not None:
                return deepcopy(prior)
            status = "unavailable" if invocation.platform_id == bound_platform_id == self.platform_id else "wrong_platform"
            receipt: dict[str, object] = {
                "request_id": invocation.request_id,
                "decision_reference": invocation.decision_reference,
                "platform_id": self.platform_id,
                "action": invocation.action,
                "adapter_status": status,
                "command_acknowledgement": "NOT_DISPATCHED",
                "stop_status": "NOT_DISPATCHED",
                "delivery": "not_dispatched",
                "physical_outcome": "unknown",
                "execution_surface": "unavailable_mbot2_zero_io",
            }
            self._receipts[invocation.request_id + ":" + operation] = receipt
            return deepcopy(receipt)

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, object]:
        return self._receipt(invocation, bound_platform_id, "dispatch")

    def stop_to_neutral(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, object]:
        return self._receipt(invocation, bound_platform_id, "stop")
