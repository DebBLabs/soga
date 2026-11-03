from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from threading import Condition, RLock
from types import MappingProxyType
from typing import Mapping, Protocol

from g27_tip_jar.adapter import Invocation

from .misty_invitation import ACTION, CATALOG_VERSION


class RobotGatewayError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class RobotAdapter(Protocol):
    platform_id: str

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, object]: ...

    def stop_to_neutral(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, object]: ...


@dataclass
class _Reservation:
    invocation: Invocation
    receipt: dict[str, object] | None = None
    in_flight: bool = True


class RobotGateway:
    """Immutable target registry with one global physical invitation slot."""

    def __init__(self, bindings: Mapping[str, RobotAdapter]) -> None:
        if not bindings or any(key != adapter.platform_id for key, adapter in bindings.items()):
            raise RobotGatewayError("invalid_registry")
        self._bindings = MappingProxyType(dict(bindings))
        self._lock = RLock()
        self._condition = Condition(self._lock)
        self._reservations: dict[str, _Reservation] = {}
        self._decision_bindings: dict[str, tuple[str, str, str]] = {}
        self._active_request_id: str | None = None
        self._operator_locked = False

    @property
    def operator_locked(self) -> bool:
        with self._lock:
            return self._operator_locked

    @property
    def active_request_id(self) -> str | None:
        with self._lock:
            return self._active_request_id

    def _validate(self, invocation: Invocation, bound_platform_id: str) -> RobotAdapter:
        if not isinstance(invocation, Invocation):
            raise RobotGatewayError("invalid_invocation_type")
        if invocation.platform_id != bound_platform_id:
            raise RobotGatewayError("wrong_platform")
        if invocation.action != ACTION or invocation.catalog_version != CATALOG_VERSION:
            raise RobotGatewayError("unauthorized_catalog_action")
        values = tuple(vars(invocation).values())
        if any(not isinstance(value, str) or not value or len(value) > 256 for value in values):
            raise RobotGatewayError("invalid_invocation")
        if len(invocation.mission_s256) != 64 or any(character not in "0123456789abcdef" for character in invocation.mission_s256):
            raise RobotGatewayError("invalid_mission_hash")
        adapter = self._bindings.get(bound_platform_id)
        if adapter is None:
            raise RobotGatewayError("unknown_platform")
        return adapter

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str) -> dict[str, object]:
        owner = self.reserve(invocation, bound_platform_id=bound_platform_id)
        return self.dispatch_reserved(invocation, bound_platform_id=bound_platform_id, owner=owner)

    def reserve(self, invocation: Invocation, *, bound_platform_id: str) -> bool:
        self._validate(invocation, bound_platform_id)
        with self._condition:
            prior = self._reservations.get(invocation.request_id)
            if prior is not None:
                if prior.invocation != invocation:
                    raise RobotGatewayError("request_binding_conflict")
                return False
            binding = (invocation.session_id, invocation.platform_id, invocation.request_id)
            existing_binding = self._decision_bindings.get(invocation.decision_reference)
            if existing_binding is not None and existing_binding != binding:
                raise RobotGatewayError("decision_already_consumed")
            if self._operator_locked:
                raise RobotGatewayError("operator_reset_required")
            if self._active_request_id is not None:
                raise RobotGatewayError("invitation_already_active")
            reservation = _Reservation(invocation=invocation)
            self._reservations[invocation.request_id] = reservation
            self._decision_bindings[invocation.decision_reference] = binding
            self._active_request_id = invocation.request_id
            return True

    def dispatch_reserved(
        self, invocation: Invocation, *, bound_platform_id: str, owner: bool
    ) -> dict[str, object]:
        adapter = self._validate(invocation, bound_platform_id)
        with self._condition:
            reservation = self._reservations.get(invocation.request_id)
            if reservation is None or reservation.invocation != invocation:
                raise RobotGatewayError("dispatch_without_exact_reservation")
            if not owner:
                if reservation.in_flight:
                    completed = self._condition.wait_for(lambda: not reservation.in_flight, timeout=3.0)
                    if not completed:
                        return self._inflight_receipt(invocation)
                if reservation.receipt is None:
                    raise RobotGatewayError("missing_stable_receipt")
                return deepcopy(reservation.receipt)

        try:
            receipt = dict(adapter.dispatch(invocation, bound_platform_id=bound_platform_id))
        except Exception:
            receipt = {
                "request_id": invocation.request_id,
                "decision_reference": invocation.decision_reference,
                "platform_id": invocation.platform_id,
                "action": invocation.action,
                "adapter_status": "adapter_exception",
                "command_acknowledgement": "FAILED",
                "delivery": "unknown",
                "physical_outcome": "unknown",
                "execution_surface": "robot_gateway",
            }
        with self._condition:
            reservation.receipt = deepcopy(receipt)
            reservation.in_flight = False
            if receipt.get("command_acknowledgement") != "ACKNOWLEDGED":
                self._active_request_id = None
            self._condition.notify_all()
            return deepcopy(receipt)

    def stop(self, invocation: Invocation) -> dict[str, object]:
        adapter = self._validate(invocation, invocation.platform_id)
        with self._lock:
            reservation = self._reservations.get(invocation.request_id)
            if reservation is None or reservation.invocation != invocation:
                raise RobotGatewayError("stop_without_exact_reservation")
        try:
            return dict(adapter.stop_to_neutral(invocation, bound_platform_id=invocation.platform_id))
        except Exception:
            return {
                "request_id": invocation.request_id,
                "decision_reference": invocation.decision_reference,
                "platform_id": invocation.platform_id,
                "action": invocation.action,
                "adapter_status": "stop_exception",
                "stop_status": "FAILED",
                "delivery": "unknown",
                "physical_outcome": "unknown",
                "execution_surface": "robot_gateway",
            }

    def release(self, request_id: str) -> None:
        with self._condition:
            if self._active_request_id == request_id:
                self._active_request_id = None
            self._condition.notify_all()

    def lock_for_operator_reset(self) -> None:
        with self._condition:
            self._operator_locked = True
            self._condition.notify_all()

    def operator_reset(self) -> None:
        with self._condition:
            if self._active_request_id is not None:
                raise RobotGatewayError("active_invitation_cannot_reset")
            self._operator_locked = False
            self._condition.notify_all()

    @staticmethod
    def _inflight_receipt(invocation: Invocation) -> dict[str, object]:
        return {
            "request_id": invocation.request_id,
            "decision_reference": invocation.decision_reference,
            "platform_id": invocation.platform_id,
            "action": invocation.action,
            "adapter_status": "dispatch_in_flight",
            "command_acknowledgement": "PENDING",
            "delivery": "unknown",
            "physical_outcome": "unknown",
            "execution_surface": "robot_gateway",
        }
