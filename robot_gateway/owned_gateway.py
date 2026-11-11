from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from threading import Condition, RLock
from types import MappingProxyType
from typing import Mapping, Protocol

from g27_tip_jar.adapter import Invocation

from .misty_invitation import ACTION, CATALOG_VERSION


from .gateway import RobotGatewayError, RobotAdapter


@dataclass
class _Reservation:
    invocation: Invocation
    receipt: dict[str, object] | None = None
    in_flight: bool = True


class OwnedRobotGateway:
    """Immutable target registry with one global physical invitation slot."""

    def __init__(self, bindings: Mapping[str, RobotAdapter], *, access_token: object) -> None:
        if access_token is None:
            raise RobotGatewayError("owner_required")
        self._access_token = access_token
        if not bindings or any(key != adapter.platform_id for key, adapter in bindings.items()):
            raise RobotGatewayError("invalid_registry")
        self._bindings = MappingProxyType(dict(bindings))
        self._lock = RLock()
        self._condition = Condition(self._lock)
        self._reservations: dict[str, _Reservation] = {}
        self._decision_bindings: dict[str, tuple[str, str, str]] = {}
        self._active_request_id: str | None = None
        self._operator_locked = False
        self._selected_platform_id: str | None = None

    def _require_owner(self, access_token):
        if access_token is not self._access_token:
            raise RobotGatewayError("exclusive_owner_required")

    @property
    def has_inflight(self):
        with self._lock:
            return any(reservation.in_flight for reservation in self._reservations.values())

    @property
    def selected_platform_id(self) -> str | None:
        with self._lock:
            return self._selected_platform_id

    def select_target(self, platform_id: str, *, access_token=None) -> None:
        """Select an idle target before a new authorization is bound.

        The operator service must route every coordinator through this same
        gateway. Selection never sends a command or releases an interaction.
        A terminal interaction and any required neutral confirmation belong
        to the lifecycle owner before this method is called.
        """
        self._require_owner(access_token)
        with self._condition:
            if type(platform_id) is not str or platform_id not in self._bindings:
                raise RobotGatewayError("unknown_platform")
            if self._operator_locked:
                raise RobotGatewayError("operator_reset_required")
            if self._active_request_id is not None:
                raise RobotGatewayError("invitation_already_active")
            if any(reservation.in_flight for reservation in self._reservations.values()):
                raise RobotGatewayError("dispatch_still_in_flight")
            self._selected_platform_id = platform_id
            self._condition.notify_all()

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

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str, access_token=None) -> dict[str, object]:
        self._require_owner(access_token)
        owner = self.reserve(invocation, bound_platform_id=bound_platform_id, access_token=access_token)
        return self.dispatch_reserved(invocation, bound_platform_id=bound_platform_id, owner=owner, access_token=access_token)

    def reserve(self, invocation: Invocation, *, bound_platform_id: str, access_token=None) -> bool:
        self._require_owner(access_token)
        self._validate(invocation, bound_platform_id)
        with self._condition:
            if self._selected_platform_id is None or invocation.platform_id != self._selected_platform_id:
                raise RobotGatewayError("target_not_selected")
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
        self, invocation: Invocation, *, bound_platform_id: str, owner: bool, access_token=None
    ) -> dict[str, object]:
        self._require_owner(access_token)
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

        receipt = None
        try:
            receipt = deepcopy(dict(adapter.dispatch(invocation, bound_platform_id=bound_platform_id)))
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
                "execution_surface": "owned_robot_gateway",
            }
        finally:
            with self._condition:
                reservation.receipt = receipt
                reservation.in_flight = False
                self._condition.notify_all()
        return deepcopy(receipt)

    def stop(self, invocation: Invocation, *, access_token=None) -> dict[str, object]:
        self._require_owner(access_token)
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

    def release(self, request_id: str, *, access_token=None) -> None:
        self._require_owner(access_token)
        with self._condition:
            if self._active_request_id == request_id:
                self._active_request_id = None
            self._condition.notify_all()

    def lock_for_operator_reset(self, *, access_token=None) -> None:
        self._require_owner(access_token)
        with self._condition:
            self._operator_locked = True
            self._condition.notify_all()

    def operator_reset(self, *, access_token=None) -> None:
        self._require_owner(access_token)
        with self._condition:
            if self._active_request_id is not None or self.has_inflight:
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
