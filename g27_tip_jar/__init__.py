"""G27 bounded Tip Jar prototype. Contains no real-robot transport."""

from .adapter import AdapterError, FakeSurface, TargetBoundAdapter
from .lifecycle import LifecycleError, SessionGrantService
from .runtime import ActionDecision, ActionRequest, Decision, PrototypeRuntime
from .state_machine import OperatingState, SafetyStateMachine

__all__ = [
    "AdapterError",
    "FakeSurface",
    "LifecycleError",
    "ActionDecision",
    "ActionRequest",
    "Decision",
    "OperatingState",
    "SafetyStateMachine",
    "SessionGrantService",
    "TargetBoundAdapter",
    "PrototypeRuntime",
]
