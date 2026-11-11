"""Single internal lifecycle owner; adapters and verifiers are injected."""
from copy import deepcopy
from dataclasses import dataclass
from threading import Condition, RLock

from g27_tip_jar.adapter import Invocation
from .gateway import RobotGatewayError
from .owned_gateway import OwnedRobotGateway
from .unavailable_mbot2 import MBOT2_UNAVAILABLE_PLATFORM_ID, UnavailableMbot2Adapter


@dataclass(frozen=True)
class RobotObservation:
    run_id: str
    platform_id: str
    request_id: str
    session_id: str
    decision_reference: str
    kind: str
    proof: str


class RobotSwitcher:
    def __init__(self, adapters, *, completion_verifiers, neutral_verifiers,
                 authorize, monotonic, run_id):
        if type(run_id) is not str or not run_id or len(run_id) > 256:
            raise ValueError("invalid_run_id")
        if set(adapters) != set(completion_verifiers) or set(adapters) != set(neutral_verifiers):
            raise ValueError("verifier_registry_mismatch")
        callbacks = (*completion_verifiers.values(), *neutral_verifiers.values(), authorize, monotonic)
        if not all(callable(callback) for callback in callbacks):
            raise ValueError("invalid_callback")
        self._token = object()
        self._gateway = OwnedRobotGateway(adapters, access_token=self._token)
        self._completion = dict(completion_verifiers)
        self._neutral = dict(neutral_verifiers)
        self._authorize = authorize
        self._clock = monotonic
        self._run_id = run_id
        self._lock = RLock()
        self._condition = Condition(self._lock)
        self._operations = 0
        self._terminals = {}
        self._placeholder = isinstance(adapters.get(MBOT2_UNAVAILABLE_PLATFORM_ID), UnavailableMbot2Adapter)
        self._phase = "IDLE"
        self._ready = set()
        self._selected = None
        self._invocation = None
        self._deadline = None
        self._requests = set()
        self._decisions = set()
        self._sessions = set()
        self._proofs = set()
        self._record = {}

    @property
    def state(self):
        with self._lock:
            return {"phase": self._phase, "selected_platform_id": self._selected,
                    "record": deepcopy(self._record)}

    def _verify(self, observation, kind, *, startup=False):
        if type(observation) is not RobotObservation or any(
            type(value) is not str or not value or len(value) > 256
            for value in vars(observation).values()
        ):
            raise RobotGatewayError("invalid_observation")
        invocation = None if startup else self._invocation
        expected = ("startup", "startup", "startup") if startup else (
            invocation.request_id, invocation.session_id, invocation.decision_reference
        )
        actual = (observation.request_id, observation.session_id, observation.decision_reference)
        if observation.run_id != self._run_id or observation.kind != kind or actual != expected:
            raise RobotGatewayError("observation_binding_mismatch")
        if observation.platform_id not in self._neutral or (
            not startup and observation.platform_id != invocation.platform_id
        ):
            raise RobotGatewayError("observation_binding_mismatch")
        key = (observation.platform_id, observation.request_id, observation.proof)
        if key in self._proofs:
            raise RobotGatewayError("observation_replay")
        verifier = (self._completion if kind == "completed" else self._neutral)[observation.platform_id]
        try:
            verified = verifier(observation, invocation)
        except Exception as error:
            raise RobotGatewayError("observation_verifier_failed") from error
        if verified is not True:
            raise RobotGatewayError("observation_not_verified")
        self._proofs.add(key)

    def startup_neutral(self, observation):
        with self._lock:
            if self._phase != "IDLE" or self._invocation is not None:
                raise RobotGatewayError("startup_not_expected")
            self._verify(observation, "neutral", startup=True)
            self._ready.add(observation.platform_id)

    def select(self, platform_id):
        with self._lock:
            if self._phase != "IDLE":
                raise RobotGatewayError("neutral_confirmation_required")
            if self._operations:
                raise RobotGatewayError("operation_still_in_flight")
            if platform_id not in self._ready:
                raise RobotGatewayError("startup_neutral_required")
            self._gateway.select_target(platform_id, access_token=self._token)
            self._selected = platform_id

    def allow_open(self, *, session_id, decision_reference):
        with self._condition:
            self._operations += 1
        try:
            return self._allow_open(session_id=session_id, decision_reference=decision_reference)
        finally:
            with self._condition:
                self._operations -= 1
                self._condition.notify_all()

    def _wait_for_stop(self):
        if self._phase == "STOPPING":
            self._condition.wait_for(lambda: self._phase != "STOPPING", timeout=3.0)
        return self.state

    def _allow_open(self, *, session_id, decision_reference):
        with self._lock:
            if self._phase != "IDLE" or self._selected is None:
                raise RobotGatewayError("selected_idle_target_required")
            if session_id in self._sessions or decision_reference in self._decisions:
                raise RobotGatewayError("authorization_consumed")
            invocation = self._authorize(self._selected, session_id, decision_reference)
            if not isinstance(invocation, Invocation) or (
                invocation.platform_id, invocation.session_id, invocation.decision_reference
            ) != (self._selected, session_id, decision_reference):
                raise RobotGatewayError("issued_authorization_mismatch")
            if invocation.request_id in self._requests:
                raise RobotGatewayError("authorization_consumed")
            # Reserve before publishing DISPATCHING so stop cannot precede reservation.
            owner = self._gateway.reserve(invocation, bound_platform_id=self._selected, access_token=self._token)
            if owner is not True:
                raise RobotGatewayError("request_id_not_fresh")
            self._requests.add(invocation.request_id)
            self._sessions.add(session_id)
            self._decisions.add(decision_reference)
            self._invocation = invocation
            self._phase = "DISPATCHING"
            self._deadline = self._clock() + 10.0
            self._record = {
                "request_id": invocation.request_id, "session_id": session_id,
                "decision_reference": decision_reference, "platform_id": self._selected,
                "dispatch_receipt": None, "stop_receipt": None,
                "completion_verified": False, "neutral_verified": False,
                "terminal_event": None, "physical_outcome": "unknown",
            }
        try:
            receipt = self._gateway.dispatch_reserved(
                invocation, bound_platform_id=invocation.platform_id, owner=True, access_token=self._token
            )
        except Exception:
            # Reservation exists; issue the one bounded stop before locking.
            self.finish(event="ERROR", expected_request_id=invocation.request_id)
            with self._lock:
                if self._invocation == invocation:
                    self._lock_for_operator("dispatch_exception")
            raise
        with self._lock:
            if self._invocation != invocation:
                return self.state
            self._record["dispatch_receipt"] = deepcopy(receipt)
            if self._phase != "DISPATCHING":
                return self._wait_for_stop()
            if receipt.get("command_acknowledgement") == "ACKNOWLEDGED":
                self._phase = "WAIT_COMPLETION"
                self._deadline = self._clock() + 10.0
                return self.state
            # Only the accepted zero-I/O placeholder proves no command was sent.
            if (self._placeholder and invocation.platform_id == MBOT2_UNAVAILABLE_PLATFORM_ID
                    and receipt.get("execution_surface") == "unavailable_mbot2_zero_io"
                    and receipt.get("command_acknowledgement") == "NOT_DISPATCHED"
                    and receipt.get("delivery") == "not_dispatched"):
                self._record.update(terminal_event="UNAVAILABLE", neutral_inferred_from_zero_io=True)
                self._release()
                return self.state
        self.finish(event="ERROR", expected_request_id=invocation.request_id)
        with self._lock:
            if self._invocation != invocation:
                return self.state
            self._lock_for_operator("dispatch_unconfirmed")
            return self.state

    def completed(self, observation):
        with self._lock:
            if self._phase != "WAIT_COMPLETION" or self._clock() >= self._deadline:
                raise RobotGatewayError("completion_not_expected")
            self._verify(observation, "completed")
            self._record["completion_verified"] = True
            self._record["completion_observation"] = observation.proof
            self._phase = "RESPONSE_WINDOW"
            self._deadline = self._clock() + 5.0
            return self.state

    def finish(self, *, event="FINISH", expected_request_id=None):
        with self._condition:
            self._operations += 1
        try:
            return self._finish(event=event, expected_request_id=expected_request_id)
        finally:
            with self._condition:
                self._operations -= 1
                self._condition.notify_all()

    def _finish(self, *, event="FINISH", expected_request_id=None):
        if event not in ("FINISH", "LEAVE", "WITHDRAW", "EXPIRE", "ERROR", "SHUTDOWN", "COMPLETION_MISSING", "DISPATCH_TIMEOUT"):
            raise RobotGatewayError("invalid_terminal_event")
        with self._lock:
            if expected_request_id is not None and (
                self._invocation is None or self._invocation.request_id != expected_request_id
            ):
                return self.state
            if self._phase in ("STOPPING", "WAIT_NEUTRAL", "LOCKED"):
                return self._wait_for_stop()
            if self._phase not in ("DISPATCHING", "WAIT_COMPLETION", "RESPONSE_WINDOW"):
                raise RobotGatewayError("no_active_interaction")
            invocation = self._invocation
            raced = self._phase == "DISPATCHING"
            self._phase = "STOPPING"
            self._deadline = self._clock() + 3.0
            self._record["terminal_event"] = event
        try:
            receipt = self._gateway.stop(invocation, access_token=self._token)
        except Exception:
            with self._lock:
                self._lock_for_operator("stop_exception")
            raise
        with self._lock:
            if self._invocation != invocation:
                return self.state
            self._record["stop_receipt"] = deepcopy(receipt)
            if self._phase != "STOPPING":
                self._condition.notify_all()
                return self.state
            if (raced or event in ("ERROR", "COMPLETION_MISSING", "DISPATCH_TIMEOUT")
                    or receipt.get("stop_status") != "ACKNOWLEDGED"
                    or receipt.get("speak_outstanding_at_stop")):
                self._lock_for_operator("stop_or_completion_unconfirmed")
            else:
                self._phase = "WAIT_NEUTRAL"
                self._deadline = self._clock() + 3.0
            self._condition.notify_all()
            return self.state

    def neutral(self, observation):
        with self._lock:
            if self._phase != "WAIT_NEUTRAL" or self._clock() >= self._deadline or self._operations:
                raise RobotGatewayError("neutral_not_expected")
            self._verify(observation, "neutral")
            self._record["neutral_verified"] = True
            self._record["neutral_observation"] = observation.proof
            self._release()
            return self.state

    def recover(self, observation):
        with self._lock:
            if self._phase != "LOCKED":
                raise RobotGatewayError("recovery_not_expected")
            if self._operations or self._gateway.has_inflight:
                raise RobotGatewayError("dispatch_still_in_flight")
            self._verify(observation, "neutral")
            self._record["neutral_verified"] = True
            self._record["recovery_observation"] = observation.proof
            self._release()
            self._gateway.operator_reset(access_token=self._token)
            return self.state

    def terminal_receipt(self, request_id):
        with self._lock:
            return deepcopy(self._terminals.get(request_id))

    def _release(self):
        self._terminals[self._invocation.request_id] = deepcopy(self._record)
        self._gateway.release(self._invocation.request_id, access_token=self._token)
        self._invocation = None
        self._deadline = None
        self._phase = "IDLE"

    def _lock_for_operator(self, reason):
        self._phase = "LOCKED"
        self._record["lock_reason"] = reason
        self._gateway.lock_for_operator_reset(access_token=self._token)
        self._condition.notify_all()

    def tick(self):
        with self._lock:
            if self._deadline is None or self._clock() < self._deadline:
                return self.state
            request_id = None if self._invocation is None else self._invocation.request_id
            phase = self._phase
            if phase in ("WAIT_NEUTRAL", "STOPPING"):
                self._lock_for_operator("neutral_or_stop_deadline")
                return self.state
        event = {"DISPATCHING": "DISPATCH_TIMEOUT", "WAIT_COMPLETION": "COMPLETION_MISSING",
                 "RESPONSE_WINDOW": "EXPIRE"}.get(phase)
        return self.finish(event=event, expected_request_id=request_id) if event else self.state
