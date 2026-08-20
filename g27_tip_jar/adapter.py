from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from threading import RLock
from typing import Dict, Mapping


class AdapterError(RuntimeError):
    def __init__(self, stage: str, code: str):
        super().__init__(f"{stage}: {code}")
        self.stage = stage
        self.code = code


@dataclass(frozen=True)
class Invocation:
    request_id: str
    decision_reference: str
    mission_s256: str
    session_id: str
    platform_id: str
    agent_id: str
    action: str
    catalog_version: str


class FakeSurface:
    """Recording-only execution surface; it never reports physical outcome."""

    def __init__(self, platform_id: str) -> None:
        self.platform_id = platform_id
        self._lock = RLock()
        self._received: list[dict] = []

    @property
    def received(self) -> tuple[dict, ...]:
        with self._lock:
            return tuple(deepcopy(self._received))

    def record(self, invocation: Invocation) -> None:
        if invocation.platform_id != self.platform_id:
            raise AdapterError("fake_surface", "wrong_platform")
        with self._lock:
            self._received.append(asdict(invocation))


class TargetBoundAdapter:
    """Immutable platform-to-fake binding. No URL, discovery, or network path."""

    def __init__(self, bindings: Mapping[str, FakeSurface]) -> None:
        if not bindings or any(key != surface.platform_id for key, surface in bindings.items()):
            raise AdapterError("adapter_configuration", "invalid_binding")
        self._bindings: Dict[str, FakeSurface] = dict(bindings)
        self._lock = RLock()
        self._receipts: Dict[str, dict] = {}
        self._invocations: Dict[str, Invocation] = {}

    def dispatch(self, invocation: Invocation, *, bound_platform_id: str) -> dict:
        with self._lock:
            prior = self._receipts.get(invocation.request_id)
            if prior is not None:
                if self._invocations[invocation.request_id] != invocation:
                    raise AdapterError("idempotency", "request_binding_conflict")
                return deepcopy(prior)
            if not invocation.platform_id or invocation.platform_id != bound_platform_id:
                raise AdapterError("target_binding", "wrong_platform")
            surface = self._bindings.get(bound_platform_id)
            if surface is None:
                raise AdapterError("target_resolution", "unavailable_platform")
            required = (
                invocation.request_id,
                invocation.decision_reference,
                invocation.mission_s256,
                invocation.session_id,
                invocation.agent_id,
                invocation.action,
                invocation.catalog_version,
            )
            if any(not value for value in required):
                raise AdapterError("decision_binding", "missing_binding")
            surface.record(invocation)
            receipt = {
                "request_id": invocation.request_id,
                "platform_id": invocation.platform_id,
                "adapter_status": "received_by_recording_surface",
                "physical_outcome": "unknown",
            }
            self._receipts[invocation.request_id] = receipt
            self._invocations[invocation.request_id] = invocation
            return deepcopy(receipt)
