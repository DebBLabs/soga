from __future__ import annotations

import argparse
import threading
from dataclasses import dataclass
from typing import Callable

from .adapter import AdapterError, FakeSurface, TargetBoundAdapter
from .lifecycle import Grant, GrantState, LifecycleError, SessionGrantService
from .runtime import ActionDecision, ActionRequest, Decision, PrototypeRuntime, RuntimeErrorAtStage
from .state_machine import OperatingState, SafetyStateMachine, StateTransitionError


class DemoFailure(RuntimeError):
    pass


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


@dataclass
class Harness:
    clock: Clock
    sessions: SessionGrantService
    fake_a: FakeSurface
    fake_b: FakeSurface
    state_a: SafetyStateMachine
    state_b: SafetyStateMachine
    runtime: PrototypeRuntime


def check(label: str, condition: bool, detail: str) -> None:
    result = "PASS" if condition else "FAIL"
    print(f"  [{result}] {label}: {detail}")
    if not condition:
        raise DemoFailure(label)


def heading(number: int, title: str) -> None:
    print(f"\n=== {number}. {title} ===")


def build_harness() -> Harness:
    clock = Clock()
    sessions = SessionGrantService(monotonic=clock)
    fake_a = FakeSurface("misty-a")
    fake_b = FakeSurface("misty-b")
    state_a = SafetyStateMachine("misty-a")
    state_b = SafetyStateMachine("misty-b")
    adapter = TargetBoundAdapter({"misty-a": fake_a, "misty-b": fake_b})
    runtime = PrototypeRuntime(
        sessions=sessions,
        adapter=adapter,
        state_machines={"misty-a": state_a, "misty-b": state_b},
    )
    return Harness(clock, sessions, fake_a, fake_b, state_a, state_b, runtime)


def issue(harness: Harness, platform_id: str, grant_id: str) -> Grant:
    return harness.sessions.issue_grant(
        mission_s256="walkthrough-mission",
        platform_id=platform_id,
        notice_version="notice-v1",
        policy_version="policy-v1",
        issuer="walkthrough-person-server",
        grant_id=grant_id,
    )


def consume(harness: Harness, grant: Grant, channel: str):
    return harness.runtime.initiate_session(
        grant.grant_id,
        platform_id=grant.platform_id,
        mission_s256=grant.mission_s256,
        notice_version=grant.notice_version,
        policy_version=grant.policy_version,
        channel_key=channel,
    )


def decision(session, request_id: str, outcome: Decision = Decision.ALLOW) -> ActionDecision:
    return ActionDecision(
        request_id=request_id,
        decision_reference=f"decision-{request_id}",
        decision=outcome,
        mission_s256=session.mission_s256,
        session_id=session.session_id,
        platform_id=session.platform_id,
        agent_id="tip-jar-agent",
        action="greet_participant",
        catalog_version="catalog-test-fixture",
    )


def positive() -> None:
    heading(1, "Valid scan and permitted request")
    harness = build_harness()
    grant = issue(harness, "misty-a", "positive-grant")
    print(f"  grant before scan: {grant.state.value}")
    session = consume(harness, grant, "temporary-channel-a")
    print(f"  grant after scan:  {grant.state.value}")
    print(f"  session:           {session.state.value} on {session.platform_id}")
    receipt = harness.runtime.submit(
        decision(session, "positive-request"), channel_key=session.channel_key
    )
    check("single-use consumption", grant.state == GrantState.CONSUMED, grant.state.value)
    check("correct target", len(harness.fake_a.received) == 1, "fake A received once")
    check("other target unchanged", len(harness.fake_b.received) == 0, "fake B received zero")
    check("receipt only", receipt["adapter_status"] == "received_by_recording_surface", receipt["adapter_status"])
    check("no invented physical success", receipt["physical_outcome"] == "unknown", receipt["physical_outcome"])
    check("participant sees uncertainty", receipt["phone_status"] == "unknown", receipt["phone_status"])


def same_grant_race() -> None:
    heading(2, "Two scans race for the same grant")
    harness = build_harness()
    grant = issue(harness, "misty-a", "same-grant-race")
    barrier = threading.Barrier(3)
    results: list[tuple[str, str]] = []

    def scan(channel: str) -> None:
        barrier.wait()
        try:
            consume(harness, grant, channel)
            results.append((channel, "session_created"))
        except (LifecycleError, RuntimeErrorAtStage) as exc:
            results.append((channel, f"rejected_at_{exc.stage}:{exc.code}"))

    threads = [threading.Thread(target=scan, args=(f"scanner-{index}",)) for index in range(2)]
    for thread in threads:
        thread.start()
    barrier.wait()
    for thread in threads:
        thread.join()
    for channel, result in sorted(results):
        print(f"  {channel}: {result}")
    check("one winner", sum(result == "session_created" for _, result in results) == 1, "exactly one session")
    check("one replay rejection", sum("grant_consumption:reused_or_invalid" in result for _, result in results) == 1, "exact stage recorded")
    check("one session total", len(harness.sessions.sessions) == 1, str(len(harness.sessions.sessions)))


def different_grant_race() -> None:
    heading(3, "Two valid grants race for one live-session slot")
    harness = build_harness()
    grants = [
        issue(harness, "misty-a", "slot-grant-a"),
        issue(harness, "misty-b", "slot-grant-b"),
    ]
    barrier = threading.Barrier(3)
    results: list[tuple[str, str]] = []

    def scan(grant: Grant) -> None:
        barrier.wait()
        try:
            consume(harness, grant, f"channel-{grant.platform_id}")
            results.append((grant.grant_id, "session_created"))
        except (LifecycleError, RuntimeErrorAtStage) as exc:
            results.append((grant.grant_id, f"rejected_at_{exc.stage}:{exc.code}"))

    threads = [threading.Thread(target=scan, args=(grant,)) for grant in grants]
    for thread in threads:
        thread.start()
    barrier.wait()
    for thread in threads:
        thread.join()
    for grant_id, result in sorted(results):
        state = next(grant.state.value for grant in grants if grant.grant_id == grant_id)
        print(f"  {grant_id}: {result}; grant={state}")
    consumed = [grant for grant in grants if grant.state == GrantState.CONSUMED]
    unused = [grant for grant in grants if grant.state == GrantState.ISSUED]
    check("one session winner", len(consumed) == 1, consumed[0].grant_id)
    check("loser remains unused", len(unused) == 1, unused[0].grant_id)


def rejection_paths() -> None:
    heading(4, "Governance, target, replay, and terminal rejection")
    denied = build_harness()
    session = consume(denied, issue(denied, "misty-a", "deny-grant"), "deny-channel")
    receipt = denied.runtime.submit(
        decision(session, "denied-request", Decision.DENY), channel_key=session.channel_key
    )
    check("DENY does not dispatch", len(denied.fake_a.received) == 0, receipt["adapter_status"])
    check("degraded remains readable", receipt["phone_status"] == "degraded", receipt["phone_status"])

    wrong = build_harness()
    session = consume(wrong, issue(wrong, "misty-a", "wrong-target-grant"), "wrong-channel")
    invocation = decision(session, "wrong-target-request")
    try:
        wrong.runtime.submit(
            ActionDecision(**{**invocation.__dict__, "platform_id": "misty-b"}),
            channel_key=session.channel_key,
        )
    except RuntimeErrorAtStage as exc:
        print(f"  wrong target rejected at: {exc.stage}:{exc.code}")
        check("wrong target exact stage", exc.stage == "session_binding", f"{exc.stage}:{exc.code}")
    else:
        raise DemoFailure("wrong target was accepted")
    check("wrong target reached neither fake", not wrong.fake_a.received and not wrong.fake_b.received, "A=0 B=0")

    replay = build_harness()
    session = consume(replay, issue(replay, "misty-a", "replay-grant"), "replay-channel")
    first = decision(session, "stable-request", Decision.DENY)
    replay.runtime.submit(first, channel_key=session.channel_key)
    try:
        replay.runtime.submit(
            ActionDecision(**{**first.__dict__, "decision": Decision.ALLOW}),
            channel_key=session.channel_key,
        )
    except RuntimeErrorAtStage as exc:
        print(f"  changed replay rejected at: {exc.stage}:{exc.code}")
        check("changed replay exact stage", exc.stage == "idempotency", f"{exc.stage}:{exc.code}")
    else:
        raise DemoFailure("changed replay was accepted")


def safety() -> None:
    heading(5, "Safety stop wins and remains latched")
    harness = build_harness()
    session = consume(harness, issue(harness, "misty-a", "safety-grant"), "safety-channel")
    harness.runtime.safety_stop("misty-a")
    print(f"  state after halt: {harness.state_a.state.value}")
    print(f"  session after halt: {session.state.value}")
    try:
        harness.runtime.submit(decision(session, "late-allow"), channel_key=session.channel_key)
    except RuntimeErrorAtStage as exc:
        print(f"  late ALLOW rejected at: {exc.stage}:{exc.code}")
        check("halt defeats late ALLOW", exc.code == "terminal_safety_stopped", exc.code)
    else:
        raise DemoFailure("late ALLOW was accepted")
    for cause in (
        "network_restoration",
        "late_allow",
        "adapter_process_restart",
        "participant_retry",
        "release_of_misty_b",
    ):
        cleared = harness.state_a.attempt_automatic_release(cause)
        print(f"  {cause}: cleared={cleared}")
        check(cause, not cleared and harness.state_a.safety_latched, "still latched")
    check(
        "wrong robot cannot release",
        not harness.state_a.operator_release(
            platform_id="misty-b", conditions_verified=True, neutral_established=True
        ),
        "refused",
    )
    released = harness.state_a.operator_release(
        platform_id="misty-a", conditions_verified=True, neutral_established=True
    )
    check("verified operator release", released, harness.state_a.state.value)
    check("old session remains terminal", session.state.value == "safety_stopped", session.state.value)


SCENARIOS: dict[str, Callable[[], None]] = {
    "positive": positive,
    "same-grant-race": same_grant_race,
    "session-slot-race": different_grant_race,
    "rejections": rejection_paths,
    "safety": safety,
}


def interactive() -> int:
    harness = build_harness()
    current_grant = None
    current_session = None
    pending_request_id = None
    request_number = 0

    print("G27 TIP JAR — INTERACTIVE TWO-STAGE TERMINAL")
    print("One process. No HTTP, network, robot connection, or actuation.")
    print("Type help to see commands. Nothing happens until you enter a command.")

    def show_status() -> None:
        print("  grant:", "none" if current_grant is None else current_grant.state.value)
        print("  session:", "none" if current_session is None else current_session.state.value)
        if current_session is not None:
            machine = harness.runtime.state_machines[current_session.platform_id]
            print("  platform:", current_session.platform_id)
            print("  operating state:", machine.state.value)
            print("  phone status:", machine.phone_status)
        print("  pending request:", pending_request_id or "none")
        print("  fake A receipts:", len(harness.fake_a.received))
        print("  fake B receipts:", len(harness.fake_b.received))

    def show_events() -> None:
        if not harness.runtime.events:
            print("  no runtime events")
            return
        for event in harness.runtime.events:
            details = ", ".join(
                f"{key}={value}"
                for key, value in event.items()
                if key not in {"sequence", "kind"}
            )
            print(f"  {event['sequence']:02d} {event['kind']}: {details}")

    while True:
        try:
            raw = input("g27> ").strip()
        except EOFError:
            print()
            return 0
        if not raw:
            continue
        parts = raw.split()
        command = parts[0].lower()
        try:
            if command in {"quit", "exit"}:
                return 0
            if command == "help":
                print("  offer a|b    issue a fresh single-use grant")
                print("  scan         consume the offered grant and open a session")
                print("  request [action]  submit a request; it remains Pending")
                print("  allow|deny   deliver governance as a separate event")
                print("  stop         latch safety stop before a decision")
                print("  release      verified operator release for this platform")
                print("  status       inspect current states and fake receipts")
                print("  events       inspect ordered request/decision/dispatch/outcome history")
                print("  quit         end the in-memory process")
            elif command == "offer":
                if len(parts) != 2 or parts[1].lower() not in {"a", "b"}:
                    print("  usage: offer a|b")
                    continue
                platform = f"misty-{parts[1].lower()}"
                current_grant = issue(
                    harness, platform, f"interactive-grant-{len(harness.sessions.grants) + 1}"
                )
                current_session = None
                pending_request_id = None
                print(f"  issued grant for {platform}; state={current_grant.state.value}")
            elif command == "scan":
                if current_grant is None:
                    print("  rejected: issue a grant first")
                    continue
                current_session = consume(
                    harness, current_grant, f"channel-{current_grant.platform_id}"
                )
                print(
                    f"  scan accepted; grant={current_grant.state.value}; "
                    f"session={current_session.state.value}"
                )
            elif command == "request":
                if current_session is None:
                    print("  rejected: scan a grant first")
                    continue
                if pending_request_id is not None:
                    print("  rejected: resolve or stop the current Pending request first")
                    continue
                request_number += 1
                pending_request_id = f"interactive-request-{request_number}"
                action = parts[1] if len(parts) > 1 else "greet_participant"
                result = harness.runtime.begin_request(
                    ActionRequest(
                        request_id=pending_request_id,
                        mission_s256=current_session.mission_s256,
                        session_id=current_session.session_id,
                        platform_id=current_session.platform_id,
                        agent_id="tip-jar-agent",
                        action=action,
                        catalog_version="catalog-test-fixture",
                    ),
                    channel_key=current_session.channel_key,
                )
                print(f"  request received; state={result['state']}")
                print("  no governance decision, dispatch, or physical outcome exists yet")
            elif command in {"allow", "deny"}:
                if current_session is None or pending_request_id is None:
                    print("  rejected: there is no Pending request")
                    continue
                outcome = Decision.ALLOW if command == "allow" else Decision.DENY
                request_id = pending_request_id
                try:
                    receipt = harness.runtime.resolve_request(
                        session_id=current_session.session_id,
                        request_id=request_id,
                        decision_reference=f"interactive-{command}-{request_id}",
                        outcome=outcome,
                    )
                    pending_request_id = None
                    print(
                        f"  governance={outcome.value}; adapter={receipt['adapter_status']}; "
                        f"physical={receipt['physical_outcome']}; phone={receipt['phone_status']}"
                    )
                except RuntimeErrorAtStage as exc:
                    pending_request_id = None
                    print(f"  governance arrived but was rejected at {exc.stage}:{exc.code}")
            elif command == "stop":
                if current_session is None:
                    print("  rejected: there is no session")
                    continue
                harness.runtime.safety_stop(current_session.platform_id)
                print("  safety stop latched; session is terminal; Pending work cannot execute")
            elif command == "release":
                if current_session is None:
                    print("  rejected: there is no platform to release")
                    continue
                machine = harness.runtime.state_machines[current_session.platform_id]
                released = machine.operator_release(
                    platform_id=current_session.platform_id,
                    conditions_verified=True,
                    neutral_established=True,
                )
                print(f"  verified operator release={released}; old session={current_session.state.value}")
            elif command == "status":
                show_status()
            elif command == "events":
                show_events()
            else:
                print("  unknown command; type help")
        except (LifecycleError, RuntimeErrorAtStage, AdapterError, StateTransitionError) as exc:
            stage = getattr(exc, "stage", "state")
            code = getattr(exc, "code", str(exc))
            print(f"  rejected at {stage}:{code}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the recording-only G27 Tip Jar terminal demonstration."
    )
    parser.add_argument(
        "scenario",
        nargs="?",
        choices=["all", "interactive", "localhost", *SCENARIOS],
        default="all",
        help="scenario to run (default: all)",
    )
    args = parser.parse_args(argv)
    if args.scenario == "interactive":
        return interactive()
    if args.scenario == "localhost":
        from .localhost_demo import interactive_localhost

        return interactive_localhost()
    print("G27 TIP JAR — FAKE-SURFACE TERMINAL DEMONSTRATION")
    print("No network, robot connection, actuation, or physical outcome is used.")
    selected = SCENARIOS.values() if args.scenario == "all" else (SCENARIOS[args.scenario],)
    try:
        for scenario in selected:
            scenario()
    except DemoFailure as exc:
        print(f"\nDEMONSTRATION FAILED: {exc}")
        return 1
    print("\nDEMONSTRATION PASSED")
    return 0
