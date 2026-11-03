from __future__ import annotations

import hashlib
import json
import threading
import time
import unittest
from pathlib import Path

from g27_tip_jar.adapter import Invocation
from robot_gateway.coordinator import LIFECYCLE_EVENTS, RESPONSE_WINDOW_SECONDS, SPEECH_COMPLETION_SECONDS, RobotInvitationCoordinator
from robot_gateway.gateway import RobotGateway, RobotGatewayError
from robot_gateway.misty_invitation import ACTION, CATALOG_VERSION, MISTY_B_PLATFORM_ID, MistyInvitationAdapter, utterance_id_for
from robot_gateway.strict_json_post import SPEAK_URL, STOP_URL, StrictJsonPostTransport, StrictTransportError, response_is_acknowledged
from robot_gateway.unavailable_mbot2 import MBOT2_UNAVAILABLE_PLATFORM_ID, UnavailableMbot2Adapter


SUCCESS = {"result": True, "status": "Success"}


class Clock:
    def __init__(self):
        self.value = 100.0

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += seconds


class ScriptedTransport:
    def __init__(self, *, speak=SUCCESS, stop=SUCCESS):
        self.speak = speak
        self.stop = stop
        self.calls = []

    def __call__(self, url, payload):
        self.calls.append((url, dict(payload)))
        outcome = self.speak if url == SPEAK_URL else self.stop
        if isinstance(outcome, BaseException):
            raise outcome
        return dict(outcome)


class BlockingTransport(ScriptedTransport):
    def __init__(self, *, block_url=SPEAK_URL, speak=SUCCESS, stop=SUCCESS):
        super().__init__(speak=speak, stop=stop)
        self.block_url = block_url
        self.entered = threading.Event()
        self.release = threading.Event()

    def __call__(self, url, payload):
        self.calls.append((url, dict(payload)))
        if url == self.block_url:
            self.entered.set()
            self.release.wait(2.5)
        outcome = self.speak if url == SPEAK_URL else self.stop
        if isinstance(outcome, BaseException):
            raise outcome
        return dict(outcome)


class DualBlockingTransport(ScriptedTransport):
    def __init__(self, *, speak=SUCCESS, stop=SUCCESS):
        super().__init__(speak=speak, stop=stop)
        self.speak_entered = threading.Event(); self.stop_entered = threading.Event()
        self.release_speak = threading.Event(); self.release_stop = threading.Event()

    def __call__(self, url, payload):
        self.calls.append((url, dict(payload)))
        if url == SPEAK_URL:
            self.speak_entered.set(); self.release_speak.wait(2.5); outcome = self.speak
        else:
            self.stop_entered.set(); self.release_stop.wait(2.5); outcome = self.stop
        if isinstance(outcome, BaseException):
            raise outcome
        return dict(outcome)


class PausingGateway(RobotGateway):
    def __init__(self, bindings):
        super().__init__(bindings)
        self.dispatch_entered = threading.Event(); self.release_dispatch = threading.Event()

    def dispatch_reserved(self, invocation, *, bound_platform_id, owner):
        self.dispatch_entered.set(); self.release_dispatch.wait(2.5)
        return super().dispatch_reserved(invocation, bound_platform_id=bound_platform_id, owner=owner)


class ObservingMistyAdapter(MistyInvitationAdapter):
    def __init__(self, transport):
        super().__init__(transport); self.stop_calls = 0; self.second_stop_entered = threading.Event()

    def stop_to_neutral(self, invocation, *, bound_platform_id):
        self.stop_calls += 1
        if self.stop_calls == 2:
            self.second_stop_entered.set()
        return super().stop_to_neutral(invocation, bound_platform_id=bound_platform_id)


class RaisingAdapter:
    platform_id = MISTY_B_PLATFORM_ID

    def __init__(self):
        self.dispatch_calls = 0

    def dispatch(self, invocation, *, bound_platform_id):
        self.dispatch_calls += 1
        raise RuntimeError("adapter failure")

    def stop_to_neutral(self, invocation, *, bound_platform_id):
        raise RuntimeError("not used")


class FakeSocket:
    def __init__(self, response, clock=None, advance_per_recv=0.0):
        self.response = bytearray(response)
        self.sent = b""
        self.clock = clock
        self.advance_per_recv = advance_per_recv
        self.closed = False

    def settimeout(self, value):
        self.timeout = value

    def sendall(self, data):
        self.sent += data

    def recv(self, size):
        if self.clock is not None:
            self.clock.advance(self.advance_per_recv)
        if not self.response:
            return b""
        chunk = bytes(self.response[:size])
        del self.response[:size]
        return chunk

    def close(self):
        self.closed = True


def http_response(body=b'{"result":true,"status":"Success"}', status=b"200 OK"):
    return b"HTTP/1.1 " + status + b"\r\nContent-Type: application/json\r\nContent-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body


def invocation(request_id="request-1", decision="decision-1", session="session-1", platform=MISTY_B_PLATFORM_ID, action=ACTION, catalog=CATALOG_VERSION):
    return Invocation(request_id, decision, "a" * 64, session, platform, "aauth:iiw@debblabs.example", action, catalog)


def build_coordinator(transport=None):
    transport = transport or ScriptedTransport()
    gateway = RobotGateway({
        MISTY_B_PLATFORM_ID: MistyInvitationAdapter(transport),
        MBOT2_UNAVAILABLE_PLATFORM_ID: UnavailableMbot2Adapter(),
    })
    clock = Clock()
    identifiers = iter(("request-1", "request-2", "request-3", "request-4"))
    subject = RobotInvitationCoordinator(
        gateway=gateway,
        platform_id=MISTY_B_PLATFORM_ID,
        agent_id="aauth:iiw@debblabs.example",
        mission_s256="a" * 64,
        new_request_id=lambda: next(identifiers),
        monotonic=clock,
    )
    return subject, gateway, clock, transport


class MistyGatewayPhaseTests(unittest.TestCase):
    def test_01_exact_misty_identity_and_platform_binding(self):
        self.assertEqual(MISTY_B_PLATFORM_ID, "urn:debblabs:misty-b:20193802932")
        with self.assertRaises(RobotGatewayError):
            RobotGateway({MISTY_B_PLATFORM_ID: UnavailableMbot2Adapter()})
        gateway = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(ScriptedTransport())})
        with self.assertRaises(RobotGatewayError):
            gateway.dispatch(invocation(platform="urn:debblabs:unknown"), bound_platform_id="urn:debblabs:unknown")

    def test_02_wrong_action_and_catalog_fail_closed(self):
        gateway = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(ScriptedTransport())})
        for candidate in (invocation(action="wrong"), invocation(catalog="wrong"), invocation(decision="")):
            with self.assertRaises(RobotGatewayError):
                gateway.dispatch(candidate, bound_platform_id=MISTY_B_PLATFORM_ID)

    def test_03_exact_speak_wire_bytes(self):
        sock = FakeSocket(http_response())
        transport = StrictJsonPostTransport(socket_factory=lambda address, timeout: sock)
        transport(SPEAK_URL, {"Text": "Would you like to dance?", "Flush": True, "UtteranceId": utterance_id_for("request-1")})
        body = sock.sent.split(b"\r\n\r\n", 1)[1]
        self.assertEqual(body, b'{"Flush":true,"Text":"Would you like to dance?","UtteranceId":"' + utterance_id_for("request-1").encode() + b'"}')
        adapter_transport = ScriptedTransport(); MistyInvitationAdapter(adapter_transport).dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)
        self.assertEqual(adapter_transport.calls, [(SPEAK_URL, {"Text": "Would you like to dance?", "Flush": True, "UtteranceId": utterance_id_for("request-1")})])

    def test_04_exact_stop_wire_bytes(self):
        sock = FakeSocket(http_response())
        StrictJsonPostTransport(socket_factory=lambda address, timeout: sock)(STOP_URL, {})
        self.assertTrue(sock.sent.startswith(b"POST /api/tts/stop HTTP/1.1\r\n"))
        self.assertEqual(sock.sent.split(b"\r\n\r\n", 1)[1], b"{}")
        adapter_transport = ScriptedTransport(); MistyInvitationAdapter(adapter_transport).stop_to_neutral(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)
        self.assertEqual(adapter_transport.calls, [(STOP_URL, {})])

    def test_05_no_caller_controlled_robot_fields(self):
        self.assertEqual(set(invocation().__dict__), {"request_id", "decision_reference", "mission_s256", "session_id", "platform_id", "agent_id", "action", "catalog_version"})

    def test_06_literal_target_no_redirect_retry_dns_proxy_or_fallback(self):
        calls = []
        sock = FakeSocket(http_response(status=b"302 Found"))
        transport = StrictJsonPostTransport(socket_factory=lambda address, timeout: calls.append(address) or sock)
        with self.assertRaises(StrictTransportError):
            transport(SPEAK_URL, {"Text": "Would you like to dance?", "Flush": True, "UtteranceId": utterance_id_for("request-1")})
        self.assertEqual(calls, [("192.168.8.219", 80)])
        with self.assertRaises(StrictTransportError):
            transport("http://example.invalid/api/tts/speak", {})

    def test_07_timeout_size_and_json_shape_are_bounded(self):
        with self.assertRaises(StrictTransportError):
            StrictJsonPostTransport(timeout_seconds=2.1)
        for body in (b"[]", b"not-json", b"x" * 65_537):
            sock = FakeSocket(http_response(body))
            with self.assertRaises(StrictTransportError):
                StrictJsonPostTransport(socket_factory=lambda address, timeout, s=sock: s)(STOP_URL, {})
        clock = Clock()
        sock = FakeSocket(http_response(), clock=clock, advance_per_recv=2.1)
        with self.assertRaises(StrictTransportError):
            StrictJsonPostTransport(socket_factory=lambda address, timeout: sock, monotonic=clock)(STOP_URL, {})

    def test_08_inflight_identical_replay_sends_one_speak(self):
        transport = BlockingTransport()
        gateway = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(transport)})
        results = []
        first = threading.Thread(target=lambda: results.append(gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)))
        second = threading.Thread(target=lambda: results.append(gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)))
        first.start(); transport.entered.wait(1); second.start()
        time.sleep(0.05)  # bounded barrier: second caller has entered the in-flight wait
        transport.release.set(); first.join(); second.join()
        self.assertEqual(([url for url, _ in transport.calls].count(SPEAK_URL), results[0], results[1]), (1, results[0], results[0]))

    def test_09_changed_inflight_and_new_request_for_decision_fail_closed(self):
        transport = BlockingTransport()
        gateway = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(transport)})
        worker = threading.Thread(target=lambda: gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID))
        worker.start(); transport.entered.wait(1)
        with self.assertRaises(RobotGatewayError):
            gateway.dispatch(invocation(decision="changed"), bound_platform_id=MISTY_B_PLATFORM_ID)
        transport.release.set(); worker.join(); gateway.release("request-1")
        with self.assertRaises(RobotGatewayError):
            gateway.dispatch(invocation(request_id="request-2"), bound_platform_id=MISTY_B_PLATFORM_ID)
        self.assertEqual([url for url, _ in transport.calls].count(SPEAK_URL), 1)

    def test_10_dispatch_ack_is_not_physical_outcome(self):
        receipt = MistyInvitationAdapter(ScriptedTransport()).dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)
        self.assertEqual((receipt["command_acknowledgement"], receipt["physical_outcome"]), ("ACKNOWLEDGED", "unknown"))

    def test_11_stop_ack_is_not_physical_outcome(self):
        receipt = MistyInvitationAdapter(ScriptedTransport()).stop_to_neutral(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)
        self.assertEqual((receipt["stop_status"], receipt["physical_outcome"]), ("ACKNOWLEDGED", "unknown"))

    def test_12_failed_lifecycle_stop_blocks_later_dispatch(self):
        subject, gateway, clock, transport = build_coordinator(ScriptedTransport(stop={"result": False, "status": "Failed"}))
        subject.allow_open(decision_reference="decision-1", session_id="session-1")
        receipt = subject.lifecycle("WITHDRAW", session_id="session-1", decision_reference="decision-1")
        self.assertEqual((receipt["stop_status"], receipt["physical_outcome"], gateway.operator_locked), ("FAILED", "unknown", True))
        call_count = len(transport.calls)
        rejected = subject.allow_open(decision_reference="decision-2", session_id="session-2")
        self.assertEqual((rejected["dispatch_status"], rejected["delivery"], len(transport.calls)), ("NOT_DISPATCHED", "not_dispatched", call_count))
        with self.assertRaises(RobotGatewayError):
            gateway.dispatch(invocation(request_id="other", decision="other", session="other"), bound_platform_id=MISTY_B_PLATFORM_ID)

    def test_13_stop_is_single_and_callable_during_dispatch(self):
        transport = BlockingTransport(block_url=SPEAK_URL)
        subject, gateway, clock, transport = build_coordinator(transport)
        results = {}
        dispatch_worker = threading.Thread(target=lambda: results.setdefault("dispatch", subject.allow_open(decision_reference="decision-1", session_id="session-1")))
        dispatch_worker.start(); self.assertTrue(transport.entered.wait(1))
        stop_worker = threading.Thread(target=lambda: results.setdefault("stop", subject.lifecycle("WITHDRAW", session_id="session-1", decision_reference="decision-1")))
        stop_worker.start()
        while [url for url, _ in transport.calls].count(STOP_URL) < 1:
            pass
        transport.release.set(); dispatch_worker.join(); stop_worker.join()
        terminal = subject.terminal_receipt(session_id="session-1", decision_reference="decision-1")
        self.assertEqual([url for url, _ in transport.calls].count(STOP_URL), 1)
        self.assertEqual((terminal["stop_status"], terminal["delivery"], terminal["presentation_outcome"], gateway.operator_locked), ("ACKNOWLEDGED", "acknowledged_after_stop", "STOPPED", True))
        dual = DualBlockingTransport()
        subject2, gateway2, clock2, dual = build_coordinator(dual); results2 = {}
        d = threading.Thread(target=lambda: results2.setdefault("dispatch", subject2.allow_open(decision_reference="decision-1", session_id="session-1")))
        d.start(); self.assertTrue(dual.speak_entered.wait(1))
        s = threading.Thread(target=lambda: results2.setdefault("stop", subject2.lifecycle("WITHDRAW", session_id="session-1", decision_reference="decision-1")))
        s.start(); self.assertTrue(dual.stop_entered.wait(1)); dual.release_speak.set()
        while gateway2._reservations["request-1"].receipt is None:
            time.sleep(0.001)
        time.sleep(0.05)  # gateway has returned Speak while stop remains blocked
        dual.release_stop.set(); d.join(); s.join()
        stored = subject2.terminal_receipt(session_id="session-1", decision_reference="decision-1")
        self.assertEqual((stored["command_acknowledgement"], stored["stop_status"], [url for url, _ in dual.calls].count(STOP_URL)), ("ACKNOWLEDGED", "ACKNOWLEDGED", 1))
        stop_block = BlockingTransport(block_url=STOP_URL)
        adapter = ObservingMistyAdapter(stop_block); candidate = invocation()
        first_result = {}; second_result = {}
        first = threading.Thread(target=lambda: first_result.setdefault("value", adapter.stop_to_neutral(candidate, bound_platform_id=MISTY_B_PLATFORM_ID)))
        second = threading.Thread(target=lambda: second_result.setdefault("value", adapter.stop_to_neutral(candidate, bound_platform_id=MISTY_B_PLATFORM_ID)))
        first.start(); self.assertTrue(stop_block.entered.wait(1)); second.start(); self.assertTrue(adapter.second_stop_entered.wait(1))
        time.sleep(0.05)  # bounded barrier: second stop caller is waiting on the shared receipt
        stop_block.release.set(); first.join(); second.join()
        self.assertEqual(([url for url, _ in stop_block.calls].count(STOP_URL), first_result["value"], second_result["value"]), (1, first_result["value"], first_result["value"]))

    def test_14_all_lifecycle_events_consume_predispatch_binding(self):
        self.assertEqual(LIFECYCLE_EVENTS, frozenset(("LEAVE", "FINISH", "WITHDRAW", "EXPIRE", "ERROR", "SHUTDOWN")))
        for event in LIFECYCLE_EVENTS:
            subject, gateway, clock, transport = build_coordinator()
            decision = None if event == "LEAVE" else "decision-1"
            receipt = subject.lifecycle(event, session_id="session-1", decision_reference=decision)
            self.assertEqual(receipt["dispatch_status"], "NOT_DISPATCHED")
            with self.assertRaises(RobotGatewayError):
                subject.allow_open(decision_reference="decision-1", session_id="session-1")
            with self.assertRaises(RobotGatewayError):
                subject.lifecycle(
                    "FINISH" if event == "LEAVE" else "LEAVE",
                    session_id="session-1",
                    decision_reference="decision-2" if event == "LEAVE" else None,
                )
            self.assertEqual(transport.calls, [])
        for event in LIFECYCLE_EVENTS:
            transport = ScriptedTransport()
            gateway = PausingGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(transport)})
            clock = Clock(); ids = iter(("request-1",))
            subject = RobotInvitationCoordinator(gateway=gateway, platform_id=MISTY_B_PLATFORM_ID, agent_id="aauth:iiw@debblabs.example", mission_s256="a" * 64, new_request_id=lambda: next(ids), monotonic=clock)
            results = {}
            dispatch = threading.Thread(target=lambda: results.setdefault("dispatch", subject.allow_open(decision_reference="decision-1", session_id="session-1")))
            dispatch.start(); self.assertTrue(gateway.dispatch_entered.wait(1))
            stop = threading.Thread(target=lambda: results.setdefault("stop", subject.lifecycle(event, session_id="session-1", decision_reference="decision-1")))
            stop.start()
            while [url for url, _ in transport.calls].count(STOP_URL) < 1:
                pass
            gateway.release_dispatch.set(); dispatch.join(); stop.join()
            terminal = subject.terminal_receipt(session_id="session-1", decision_reference="decision-1")
            self.assertEqual((terminal["dispatch_status"], terminal["command_acknowledgement"], terminal["speak_outstanding_at_stop"], [url for url, _ in transport.calls].count(SPEAK_URL)), ("NOT_DISPATCHED", "NOT_DISPATCHED", False, 0))
        for event in LIFECYCLE_EVENTS:
            subject, gateway, clock, transport = build_coordinator(); subject.allow_open(decision_reference="decision-1", session_id="session-1")
            terminal = subject.lifecycle(event, session_id="session-1", decision_reference="decision-1")
            self.assertEqual((terminal["terminal_event"], [url for url, _ in transport.calls].count(STOP_URL)), (event, 1))

    def test_15_public_mode_cannot_construct_gateway(self):
        root = Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak")
        for name in ("bridge.py", "index.html", "Start IIW Table.command", "IIW_TABLE_OPERATOR_CHECKLIST.md"):
            self.assertNotIn("robot_gateway", (root / name).read_text(encoding="utf-8"))
        producer = Path("/Users/debb/dev/soga-clean/robot_gateway/coordinator.py").read_text(encoding="utf-8")
        self.assertNotIn("/api/", producer); self.assertNotIn("http://", producer); self.assertNotIn("https://", producer)

    def test_16_mbot_placeholder_has_zero_io_no_fallback(self):
        placeholder = UnavailableMbot2Adapter()
        gateway = RobotGateway({MBOT2_UNAVAILABLE_PLATFORM_ID: placeholder, MISTY_B_PLATFORM_ID: MistyInvitationAdapter(ScriptedTransport())})
        candidate = invocation(platform=MBOT2_UNAVAILABLE_PLATFORM_ID)
        receipt = gateway.dispatch(candidate, bound_platform_id=MBOT2_UNAVAILABLE_PLATFORM_ID)
        self.assertEqual((receipt["adapter_status"], receipt["command_acknowledgement"]), ("unavailable", "NOT_DISPATCHED"))
        self.assertEqual(placeholder.stop_to_neutral(candidate, bound_platform_id=MBOT2_UNAVAILABLE_PLATFORM_ID)["stop_status"], "NOT_DISPATCHED")
        with self.assertRaises(TypeError):
            UnavailableMbot2Adapter(transport=object())
        ids = iter(("mbot-request",)); clock = Clock()
        coordinator = RobotInvitationCoordinator(gateway=gateway, platform_id=MBOT2_UNAVAILABLE_PLATFORM_ID, agent_id="aauth:iiw@debblabs.example", mission_s256="a" * 64, new_request_id=lambda: next(ids), monotonic=clock)
        terminal = coordinator.allow_open(decision_reference="mbot-decision", session_id="mbot-session")
        self.assertEqual((terminal["dispatch_status"], terminal["command_acknowledgement"], terminal["delivery"], terminal["stop_status"]), ("NOT_DISPATCHED", "NOT_DISPATCHED", "not_dispatched", "NOT_DISPATCHED"))

    def test_17_cross_target_decision_reuse_fails_closed(self):
        gateway = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(ScriptedTransport()), MBOT2_UNAVAILABLE_PLATFORM_ID: UnavailableMbot2Adapter()})
        gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID); gateway.release("request-1")
        with self.assertRaises(RobotGatewayError):
            gateway.dispatch(invocation(request_id="request-2", platform=MBOT2_UNAVAILABLE_PLATFORM_ID), bound_platform_id=MBOT2_UNAVAILABLE_PLATFORM_ID)
        gateway2 = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(ScriptedTransport()), MBOT2_UNAVAILABLE_PLATFORM_ID: UnavailableMbot2Adapter()})
        gateway2.dispatch(invocation(platform=MBOT2_UNAVAILABLE_PLATFORM_ID), bound_platform_id=MBOT2_UNAVAILABLE_PLATFORM_ID); gateway2.release("request-1")
        with self.assertRaises(RobotGatewayError):
            gateway2.dispatch(invocation(request_id="request-2"), bound_platform_id=MISTY_B_PLATFORM_ID)

    def test_18_concurrent_cross_robot_requests_allow_one(self):
        transport = BlockingTransport()
        gateway = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(transport), MBOT2_UNAVAILABLE_PLATFORM_ID: UnavailableMbot2Adapter()})
        worker = threading.Thread(target=lambda: gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID))
        worker.start(); transport.entered.wait(1)
        with self.assertRaises(RobotGatewayError):
            gateway.dispatch(invocation(request_id="m", decision="m", session="m", platform=MBOT2_UNAVAILABLE_PLATFORM_ID), bound_platform_id=MBOT2_UNAVAILABLE_PLATFORM_ID)
        transport.release.set(); worker.join()

    def test_19_payload_contains_no_participant_material(self):
        transport = ScriptedTransport(); MistyInvitationAdapter(transport).dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)
        self.assertEqual(set(transport.calls[0][1]), {"Text", "Flush", "UtteranceId"})

    def test_20_all_preservation_pins_match(self):
        manifest = json.loads(Path("/Users/debb/dev/soga-clean/tools/robot_gateway/misty-phase-runtime-manifest.json").read_text())
        roots = {
            "preserved_sha256": Path("/Users/debb/dev/soga-clean"),
            "presentation_sha256": Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak"),
            "accepted_evidence_sha256": None,
        }
        for group, root in roots.items():
            for absolute_or_relative, expected in manifest[group].items():
                path = Path(absolute_or_relative) if root is None else root / absolute_or_relative
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)

    def test_21_ack_parser_rejects_null_status_and_duplicate_keys(self):
        self.assertTrue(response_is_acknowledged({"result": True}))
        self.assertFalse(response_is_acknowledged({"result": True, "status": None}))
        body = b'{"result":false,"result":true}'
        with self.assertRaises(StrictTransportError):
            StrictJsonPostTransport(socket_factory=lambda address, timeout: FakeSocket(http_response(body)))(STOP_URL, {})

    def test_22_failure_body_never_acknowledges(self):
        self.assertFalse(response_is_acknowledged({"result": False, "status": "Failed"}))
        self.assertFalse(response_is_acknowledged({"result": True, "error": "failed"}))

    def test_23_speak_timeout_attempts_one_stop_and_locks(self):
        subject, gateway, clock, transport = build_coordinator(ScriptedTransport(speak=StrictTransportError("total_timeout")))
        receipt = subject.allow_open(decision_reference="decision-1", session_id="session-1")
        self.assertEqual((receipt["delivery"], gateway.operator_locked, [url for url, _ in transport.calls].count(STOP_URL)), ("unknown", True, 1))
        raising = RaisingAdapter(); replay_gateway = RobotGateway({MISTY_B_PLATFORM_ID: raising})
        first = replay_gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)
        second = replay_gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID)
        self.assertEqual((first, second, first["adapter_status"], raising.dispatch_calls), (first, first, "adapter_exception", 1))

    def test_24_ack_is_nonterminal_and_reservation_held(self):
        subject, gateway, clock, transport = build_coordinator()
        subject.allow_open(decision_reference="decision-1", session_id="session-1")
        self.assertEqual(gateway.active_request_id, "request-1")
        with self.assertRaises(RobotGatewayError):
            subject.allow_open(decision_reference="decision-2", session_id="session-2")

    def test_25_only_exact_completion_starts_window(self):
        subject, gateway, clock, transport = build_coordinator(); subject.allow_open(decision_reference="decision-1", session_id="session-1")
        with self.assertRaises(RobotGatewayError):
            subject.speech_complete(utterance_id="pts-" + "0" * 32, session_id="session-1", decision_reference="decision-1")
        self.assertEqual(subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id="session-1", decision_reference="decision-1")["phase"], "RESPONSE_WINDOW")

    def test_26_five_second_window_blocks_then_releases(self):
        subject, gateway, clock, transport = build_coordinator(); subject.allow_open(decision_reference="decision-1", session_id="session-1")
        subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id="session-1", decision_reference="decision-1")
        with self.assertRaises(RobotGatewayError):
            subject.allow_open(decision_reference="decision-2", session_id="session-2")
        clock.advance(4.999); self.assertIsNone(subject.tick()); clock.advance(0.001); expired = subject.tick(); self.assertEqual((expired["terminal_event"], expired["command_acknowledgement"], expired["delivery"]), ("EXPIRE", "ACKNOWLEDGED", "acknowledged"))
        self.assertEqual(subject.allow_open(decision_reference="decision-2", session_id="session-2")["command_acknowledgement"], "ACKNOWLEDGED")

    def test_27_missing_stale_duplicate_reordered_and_cross_session_fail_closed(self):
        subject, gateway, clock, transport = build_coordinator(); subject.allow_open(decision_reference="decision-1", session_id="session-1")
        for session, decision in (("other", "decision-1"), ("session-1", "other")):
            with self.assertRaises(RobotGatewayError):
                subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id=session, decision_reference=decision)
        subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id="session-1", decision_reference="decision-1")
        with self.assertRaises(RobotGatewayError):
            subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id="session-1", decision_reference="decision-1")
        with self.assertRaises(RobotGatewayError):
            subject.lifecycle("WITHDRAW", session_id="session-2", decision_reference="decision-2")
        clock.advance(5.0); subject.tick()
        with self.assertRaises(RobotGatewayError):
            subject.allow_open(decision_reference="decision-2", session_id="session-2")
        with self.assertRaises(RobotGatewayError):
            subject.lifecycle("LEAVE", session_id="session-1", decision_reference=None)

    def test_28_operator_reset_cannot_revive_consumed_decision(self):
        gateway = RobotGateway({MISTY_B_PLATFORM_ID: MistyInvitationAdapter(ScriptedTransport())})
        gateway.dispatch(invocation(), bound_platform_id=MISTY_B_PLATFORM_ID); gateway.release("request-1")
        gateway.lock_for_operator_reset(); gateway.operator_reset()
        with self.assertRaises(RobotGatewayError):
            gateway.dispatch(invocation(request_id="request-2"), bound_platform_id=MISTY_B_PLATFORM_ID)
        presentation = Path("/Users/debb/dev/permission-to-speak-work/permission-to-speak")
        for name in ("bridge.py", "index.html", "Start IIW Table.command", "IIW_TABLE_OPERATOR_CHECKLIST.md"):
            content = (presentation / name).read_text(encoding="utf-8")
            self.assertNotIn("robot_gateway.operator_reset", content); self.assertNotIn("/api/robot-reset", content); self.assertNotIn("192.168.8.219", content)

    def test_29_utterance_id_is_exact_bounded_hash(self):
        self.assertEqual(utterance_id_for("private-request"), "pts-" + hashlib.sha256(b"private-request").hexdigest()[:32])

    def test_30_parent_mapping_safety_invariants(self):
        self.assertEqual((SPEECH_COMPLETION_SECONDS, RESPONSE_WINDOW_SECONDS), (10.0, 5.0))
        readme = Path("/Users/debb/dev/soga-clean/robot_gateway/README.md").read_text()
        self.assertNotIn("AAuth token platform", readme)
        self.assertIn("participant devices never share Beryl", readme)
        parent_mapping = {
            1: "test_03_exact_speak_wire_bytes", 2: "DEFERRED:mbot_identity_and_interface_unaccepted",
            3: "test_01_exact_misty_identity_and_platform_binding", 4: "test_17_cross_target_decision_reuse_fails_closed",
            5: "test_17_cross_target_decision_reuse_fails_closed", 6: "test_02_wrong_action_and_catalog_fail_closed",
            7: "test_02_wrong_action_and_catalog_fail_closed", 8: "test_08_inflight_identical_replay_sends_one_speak",
            9: "test_09_changed_inflight_and_new_request_for_decision_fail_closed", 10: "test_16_mbot_placeholder_has_zero_io_no_fallback",
            11: "test_18_concurrent_cross_robot_requests_allow_one", 12: "test_10_dispatch_ack_is_not_physical_outcome",
            13: "test_12_failed_lifecycle_stop_blocks_later_dispatch", 14: "test_19_payload_contains_no_participant_material",
            15: "test_20_all_preservation_pins_match", 16: "test_17_cross_target_decision_reuse_fails_closed",
            17: "test_30_parent_mapping_safety_invariants", 18: "test_15_public_mode_cannot_construct_gateway",
            19: "test_03_exact_speak_wire_bytes", 20: "test_15_public_mode_cannot_construct_gateway",
            21: "test_14_all_lifecycle_events_consume_predispatch_binding", 22: "test_14_all_lifecycle_events_consume_predispatch_binding",
            23: "test_14_all_lifecycle_events_consume_predispatch_binding", 24: "test_32_stop_during_speech_is_terminal_and_idempotent",
            25: "test_27_missing_stale_duplicate_reordered_and_cross_session_fail_closed", 26: "test_23_speak_timeout_attempts_one_stop_and_locks",
            27: "test_09_changed_inflight_and_new_request_for_decision_fail_closed", 28: "test_28_operator_reset_cannot_revive_consumed_decision",
            29: "test_26_five_second_window_blocks_then_releases", 30: "test_34_failed_lifecycle_stop_requires_operator_reset",
        }
        self.assertEqual(set(parent_mapping), set(range(1, 31)))
        methods = {name for name in dir(type(self)) if name.startswith("test_")}
        self.assertTrue(all(value.startswith("DEFERRED:") or value in methods for value in parent_mapping.values()))

    def test_31_completion_deadline_stops_and_locks(self):
        subject, gateway, clock, transport = build_coordinator(BlockingTransport(block_url=STOP_URL)); subject.allow_open(decision_reference="decision-1", session_id="session-1")
        clock.advance(10.0); result = {}
        worker = threading.Thread(target=lambda: result.setdefault("receipt", subject.tick()))
        worker.start(); self.assertTrue(transport.entered.wait(1))
        pending = subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id="session-1", decision_reference="decision-1")
        self.assertEqual(pending["stop_status"], "PENDING")
        transport.release.set(); worker.join(); receipt = result["receipt"]
        self.assertEqual((receipt["completion"], receipt["stop_status"], receipt["command_acknowledgement"], receipt["delivery"], receipt["late_completion_recorded"], receipt["physical_outcome"], gateway.operator_locked), ("missing", "ACKNOWLEDGED", "ACKNOWLEDGED", "acknowledged", True, "unknown", True))

    def test_32_stop_during_speech_is_terminal_and_idempotent(self):
        subject, gateway, clock, transport = build_coordinator(BlockingTransport(block_url=STOP_URL, stop={"result": False, "status": "Failed"})); subject.allow_open(decision_reference="decision-1", session_id="session-1")
        result = {}
        worker = threading.Thread(target=lambda: result.setdefault("first", subject.lifecycle("WITHDRAW", session_id="session-1", decision_reference="decision-1")))
        worker.start(); self.assertTrue(transport.entered.wait(1))
        pending = subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id="session-1", decision_reference="decision-1")
        self.assertEqual(pending["stop_status"], "PENDING")
        clock.advance(11.0); self.assertIsNone(subject.tick())
        transport.release.set(); worker.join(); first = result["first"]
        second = subject.lifecycle("WITHDRAW", session_id="session-1", decision_reference="decision-1")
        self.assertEqual((first, second, first["presentation_outcome"], first["physical_outcome"], first["late_completion_recorded"], gateway.operator_locked), (first, first, "STOPPED", "unknown", True, True))

    def test_33_late_completion_is_recorded_until_deadline_release(self):
        subject, gateway, clock, transport = build_coordinator(); subject.allow_open(decision_reference="decision-1", session_id="session-1")
        subject.lifecycle("FINISH", session_id="session-1", decision_reference="decision-1")
        recorded = subject.speech_complete(utterance_id=utterance_id_for("request-1"), session_id="session-1", decision_reference="decision-1")
        self.assertTrue(recorded["late_completion_recorded"]); self.assertEqual(gateway.active_request_id, "request-1")
        clock.advance(10.0); subject.tick(); self.assertIsNone(gateway.active_request_id)

    def test_34_failed_lifecycle_stop_requires_operator_reset(self):
        subject, gateway, clock, transport = build_coordinator(ScriptedTransport(stop=StrictTransportError("total_timeout")))
        subject.allow_open(decision_reference="decision-1", session_id="session-1")
        receipt = subject.lifecycle("ERROR", session_id="session-1", decision_reference="decision-1")
        self.assertEqual((receipt["stop_status"], gateway.operator_locked), ("TIMED_OUT", True))
        gateway.operator_reset()
        racing = DualBlockingTransport(speak=StrictTransportError("total_timeout"))
        subject2, gateway2, clock2, racing = build_coordinator(racing)
        results = {}
        dispatch_worker = threading.Thread(target=lambda: results.setdefault("dispatch", subject2.allow_open(decision_reference="decision-1", session_id="session-1")))
        dispatch_worker.start(); self.assertTrue(racing.speak_entered.wait(1))
        stop_worker = threading.Thread(target=lambda: results.setdefault("stop", subject2.lifecycle("WITHDRAW", session_id="session-1", decision_reference="decision-1")))
        stop_worker.start()
        self.assertTrue(racing.stop_entered.wait(1)); racing.release_speak.set()
        while gateway2._reservations["request-1"].receipt is None:
            time.sleep(0.001)
        time.sleep(0.05)  # failed Speak is recorded before the blocked stop returns
        racing.release_stop.set(); dispatch_worker.join(); stop_worker.join()
        terminal = subject2.terminal_receipt(session_id="session-1", decision_reference="decision-1")
        self.assertEqual((terminal["command_acknowledgement"], terminal["delivery"], gateway2.operator_locked), ("TIMED_OUT", "unknown", True))


if __name__ == "__main__":
    raise SystemExit("use the reviewed bounded controller")
