from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from threading import Condition, RLock
from typing import Callable, Mapping

from g27_tip_jar.adapter import Invocation

from .strict_json_post import SPEAK_URL, STOP_URL, StrictTransportError, response_is_acknowledged


MISTY_B_PLATFORM_ID = "urn:debblabs:misty-b:20193802932"
ACTION = "pts.ask_dance_question.v1"
CATALOG_VERSION = "pts-robot-invitation-v1"
QUESTION = "Would you like to dance?"


class MistyAdapterError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def utterance_id_for(request_id: str) -> str:
    if not request_id or len(request_id) > 256:
        raise MistyAdapterError("invalid_request_id")
    return "pts-" + sha256(request_id.encode("utf-8")).hexdigest()[:32]


class MistyInvitationAdapter:
    platform_id = MISTY_B_PLATFORM_ID

    def __init__(self, transport: Callable[[str, Mapping[str, object]], Mapping[str, object]]) -> None:
        self._transport = transport
        self._lock = RLock()
        self._condition = Condition(self._lock)
        self._invocations: dict[str, Invocation] = {}
        self._dispatch_receipts: dict[str, dict[str, object]] = {}
        self._stop_receipts: dict[str, dict[str, object]] = {}
        self._dispatch_inflight: set[str] = set()
        self._stop_inflight: set[str] = set()
        self._stop_requested: set[str] = set()
        self._stop_while_dispatch: set[str] = set()

    def _validate(self, invocation: Invocation, bound_platform_id: str) -> None:
        if bound_platform_id != self.platform_id or invocation.platform_id != self.platform_id:
            raise MistyAdapterError("wrong_platform")
        if invocation.action != ACTION or invocation.catalog_version != CATALOG_VERSION:
            raise MistyAdapterError("unauthorized_catalog_action")
        values = (
            invocation.request_id,
            invocation.decision_reference,
            invocation.mission_s256,
            invocation.session_id,
            invocation.agent_id,
        )
        if any(not isinstance(value, str) or not value or len(value) > 256 for value in values):
            raise MistyAdapterError("invalid_decision_binding")

    def _bind(self, invocation: Invocation) -> None:
        prior = self._invocations.get(invocation.request_id)
        if prior is not None and prior != invocation:
            raise MistyAdapterError("request_binding_conflict")
        self._invocations.setdefault(invocation.request_id, invocation)

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, object]:
        self._validate(invocation, bound_platform_id)
        with self._condition:
            self._bind(invocation)
            prior = self._dispatch_receipts.get(invocation.request_id)
            if prior is not None:
                return deepcopy(prior)
            if invocation.request_id in self._dispatch_inflight:
                completed = self._condition.wait_for(
                    lambda: invocation.request_id not in self._dispatch_inflight,
                    timeout=3.0,
                )
                if not completed:
                    return self._pending_dispatch_receipt(invocation)
                return deepcopy(self._dispatch_receipts[invocation.request_id])
            if invocation.request_id in self._stop_requested:
                receipt = self._not_dispatched_receipt(invocation)
                self._dispatch_receipts[invocation.request_id] = receipt
                return deepcopy(receipt)
            self._dispatch_inflight.add(invocation.request_id)

        utterance_id = utterance_id_for(invocation.request_id)
        payload = {"Text": QUESTION, "Flush": True, "UtteranceId": utterance_id}
        try:
            response = dict(self._transport(SPEAK_URL, payload))
            acknowledged = response_is_acknowledged(response)
            acknowledgement = "ACKNOWLEDGED" if acknowledged else "FAILED"
            adapter_status = "acknowledged" if acknowledged else "failed"
            delivery = "acknowledged" if acknowledged else "unknown"
        except StrictTransportError as exc:
            acknowledgement = "TIMED_OUT" if exc.code == "total_timeout" else "FAILED"
            adapter_status = "failed"
            delivery = "unknown"
        except Exception:
            acknowledgement = "FAILED"
            adapter_status = "failed"
            delivery = "unknown"

        with self._condition:
            outstanding_at_stop = invocation.request_id in self._stop_while_dispatch
            receipt: dict[str, object] = {
                "request_id": invocation.request_id,
                "decision_reference": invocation.decision_reference,
                "platform_id": self.platform_id,
                "action": ACTION,
                "adapter_status": adapter_status,
                "command_acknowledgement": acknowledgement,
                "delivery": delivery,
                "utterance_id": utterance_id,
                "speak_outstanding_at_stop": outstanding_at_stop,
                "physical_outcome": "unknown",
                "execution_surface": "misty_b_tts_http",
            }
            existing = self._dispatch_receipts.setdefault(invocation.request_id, receipt)
            self._dispatch_inflight.discard(invocation.request_id)
            self._condition.notify_all()
            return deepcopy(existing)

    def stop_to_neutral(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, object]:
        self._validate(invocation, bound_platform_id)
        with self._condition:
            self._bind(invocation)
            self._stop_requested.add(invocation.request_id)
            if invocation.request_id in self._dispatch_inflight:
                self._stop_while_dispatch.add(invocation.request_id)
            prior = self._stop_receipts.get(invocation.request_id)
            if prior is not None:
                return deepcopy(prior)
            if invocation.request_id in self._stop_inflight:
                completed = self._condition.wait_for(
                    lambda: invocation.request_id not in self._stop_inflight,
                    timeout=3.0,
                )
                if not completed:
                    return self._pending_stop_receipt(invocation)
                return deepcopy(self._stop_receipts[invocation.request_id])
            self._stop_inflight.add(invocation.request_id)

        try:
            response = dict(self._transport(STOP_URL, {}))
            status = "ACKNOWLEDGED" if response_is_acknowledged(response) else "FAILED"
        except StrictTransportError as exc:
            status = "TIMED_OUT" if exc.code == "total_timeout" else "FAILED"
        except Exception:
            status = "FAILED"

        with self._condition:
            receipt: dict[str, object] = {
                "request_id": invocation.request_id,
                "decision_reference": invocation.decision_reference,
                "platform_id": self.platform_id,
                "action": ACTION,
                "adapter_status": "stop_recorded",
                "command_acknowledgement": "unknown",
                "stop_status": status,
                "speak_outstanding_at_stop": invocation.request_id in self._stop_while_dispatch,
                "delivery": "unknown",
                "physical_outcome": "unknown",
                "execution_surface": "misty_b_tts_http",
            }
            existing = self._stop_receipts.setdefault(invocation.request_id, receipt)
            self._stop_inflight.discard(invocation.request_id)
            self._condition.notify_all()
            return deepcopy(existing)

    @staticmethod
    def _not_dispatched_receipt(invocation: Invocation) -> dict[str, object]:
        return {
            "request_id": invocation.request_id,
            "decision_reference": invocation.decision_reference,
            "platform_id": invocation.platform_id,
            "action": invocation.action,
            "adapter_status": "stopped_before_dispatch",
            "command_acknowledgement": "NOT_DISPATCHED",
            "delivery": "not_dispatched",
            "utterance_id": utterance_id_for(invocation.request_id),
            "speak_outstanding_at_stop": False,
            "physical_outcome": "unknown",
            "execution_surface": "misty_b_tts_http",
        }

    @staticmethod
    def _pending_dispatch_receipt(invocation: Invocation) -> dict[str, object]:
        return {
            "request_id": invocation.request_id,
            "decision_reference": invocation.decision_reference,
            "platform_id": invocation.platform_id,
            "action": invocation.action,
            "adapter_status": "dispatch_in_flight",
            "command_acknowledgement": "PENDING",
            "delivery": "unknown",
            "physical_outcome": "unknown",
            "execution_surface": "misty_b_tts_http",
        }

    @staticmethod
    def _pending_stop_receipt(invocation: Invocation) -> dict[str, object]:
        return {
            "request_id": invocation.request_id,
            "decision_reference": invocation.decision_reference,
            "platform_id": invocation.platform_id,
            "action": invocation.action,
            "adapter_status": "stop_in_flight",
            "stop_status": "PENDING",
            "delivery": "unknown",
            "physical_outcome": "unknown",
            "execution_surface": "misty_b_tts_http",
        }
