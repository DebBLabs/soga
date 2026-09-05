from __future__ import annotations

from copy import deepcopy
from threading import RLock
from typing import Callable, Mapping

from g27_tip_jar.adapter import AdapterError, Invocation

from .mission import ACTION, CATALOG_VERSION


SIGNAL_RGB = {"red": 255, "green": 105, "blue": 180}
NEUTRAL_RGB = {"red": 255, "green": 255, "blue": 0}
LED_PATH = "/led"


class MistySignalLightAdapter:
    """Explicitly configured adapter for the sole M01 signal-light action.

    The caller injects both the target and transport. There is no HTTP client,
    discovery, fallback address, or status query in this module.
    """

    def __init__(
        self,
        *,
        platform_id: str,
        api_base_url: str,
        transport: Callable[[str, Mapping[str, int]], Mapping[str, object]],
        wait: Callable[[float], None],
        duration_seconds: float,
    ) -> None:
        if not platform_id:
            raise AdapterError("adapter_configuration", "missing_platform")
        if not api_base_url.startswith(("http://", "https://")):
            raise AdapterError("adapter_configuration", "explicit_http_target_required")
        api_base_url = api_base_url.rstrip("/")
        if not api_base_url.endswith("/api"):
            raise AdapterError("adapter_configuration", "api_base_must_end_in_api")
        if duration_seconds <= 0 or duration_seconds > 5:
            raise AdapterError("adapter_configuration", "invalid_bounded_duration")
        self.platform_id = platform_id
        self.api_base_url = api_base_url
        self._transport = transport
        self._wait = wait
        self.duration_seconds = duration_seconds
        self._lock = RLock()
        self._receipts: dict[str, dict] = {}
        self._invocations: dict[str, Invocation] = {}

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str) -> dict:
        with self._lock:
            prior = self._receipts.get(invocation.request_id)
            if prior is not None:
                if self._invocations[invocation.request_id] != invocation:
                    raise AdapterError("idempotency", "request_binding_conflict")
                return deepcopy(prior)
            if bound_platform_id != self.platform_id or invocation.platform_id != self.platform_id:
                raise AdapterError("target_binding", "wrong_platform")
            if invocation.action != ACTION or invocation.catalog_version != CATALOG_VERSION:
                raise AdapterError("catalog_binding", "unauthorized_action")
            if any(
                not value
                for value in (
                    invocation.request_id,
                    invocation.decision_reference,
                    invocation.mission_s256,
                    invocation.session_id,
                    invocation.agent_id,
                )
            ):
                raise AdapterError("decision_binding", "missing_binding")

            signal_status = "transport_error"
            wait_status = "completed"
            neutral_status = "transport_error"
            try:
                signal_response = dict(
                    self._transport(self.api_base_url + LED_PATH, SIGNAL_RGB)
                )
                signal_status = (
                    "robot_api_acknowledged"
                    if signal_response.get("status") == "Success"
                    else "robot_api_not_acknowledged"
                )
            except Exception:
                pass
            try:
                self._wait(self.duration_seconds)
            except Exception:
                wait_status = "wait_error"
            try:
                neutral_response = dict(
                    self._transport(self.api_base_url + LED_PATH, NEUTRAL_RGB)
                )
                neutral_status = (
                    "robot_api_acknowledged"
                    if neutral_response.get("status") == "Success"
                    else "robot_api_not_acknowledged"
                )
            except Exception:
                pass
            receipt = {
                "request_id": invocation.request_id,
                "platform_id": invocation.platform_id,
                "adapter_status": (
                    "robot_api_acknowledged"
                    if signal_status == neutral_status == "robot_api_acknowledged"
                    and wait_status == "completed"
                    else "robot_api_incomplete"
                ),
                "signal_adapter_status": signal_status,
                "wait_status": wait_status,
                "physical_outcome": "unknown",
                "neutral_outcome": "unknown",
                "neutral_adapter_status": neutral_status,
                "execution_surface": "misty_api_transport",
            }
            self._receipts[invocation.request_id] = receipt
            self._invocations[invocation.request_id] = invocation
            return deepcopy(receipt)
