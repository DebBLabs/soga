from __future__ import annotations

from .localhost import LocalhostStack, LocalhostTransportError


def interactive_localhost() -> int:
    current_grant: dict | None = None
    current_session: dict | None = None
    pending_request_id: str | None = None
    request_number = 0

    with LocalhostStack() as stack:
        client = stack.client
        print("G27 TIP JAR — LOCALHOST SPLIT-SERVICE TERMINAL")
        print("Real loopback HTTP between local services; fake recording surfaces only.")
        print("No external network, robot connection, discovery, query, or actuation.")
        print(f"runtime service: {stack.runtime_url}")
        print(f"governance delivery service: {stack.governance_url}")
        print(f"fake A service: {stack.recording_urls['misty-a']}")
        print(f"fake B service: {stack.recording_urls['misty-b']}")
        print("Type help to see commands. Nothing happens until you enter a command.")

        def show_status() -> None:
            status = client.status()
            grant = None if current_grant is None else status["grants"].get(current_grant["grant_id"])
            session = (
                None
                if current_session is None
                else status["sessions"].get(current_session["session_id"])
            )
            print("  transport:", status["transport"])
            print("  grant:", "none" if grant is None else grant["state"])
            print("  session:", "none" if session is None else session["state"])
            if current_session is not None:
                platform = current_session["platform_id"]
                machine = status["machines"][platform]
                print("  platform:", platform)
                print("  operating state:", machine["state"])
                print("  phone status:", machine["phone_status"])
            pending = status["pending_request_ids"]
            print("  pending request:", "none" if not pending else pending[0])
            print("  fake A receipts:", status["fake_receipts"]["misty-a"])
            print("  fake B receipts:", status["fake_receipts"]["misty-b"])

        def show_events() -> None:
            events = client.status()["events"]
            if not events:
                print("  no runtime events")
                return
            for event in events:
                details = ", ".join(
                    f"{key}={value}"
                    for key, value in event.items()
                    if key not in {"sequence", "kind"}
                )
                print(f"  {event['sequence']:02d} {event['kind']}: {details}")

        while True:
            try:
                raw = input("g27-local> ").strip()
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
                    print("  offer a|b    issue a fresh single-use grant over localhost")
                    print("  scan         consume the offered grant and open a session")
                    print("  request [action]  submit a request; it remains Pending")
                    print("  allow|deny   deliver governance through its separate service")
                    print("  stop         latch safety stop before a decision")
                    print("  status       inspect service, session, and fake-receipt state")
                    print("  events       inspect ordered cross-service event history")
                    print("  quit         stop all four loopback services")
                elif command == "offer":
                    if len(parts) != 2 or parts[1].lower() not in {"a", "b"}:
                        print("  usage: offer a|b")
                        continue
                    platform_id = f"misty-{parts[1].lower()}"
                    current_grant = client.runtime_post("/offer", {"platform_id": platform_id})
                    current_session = None
                    pending_request_id = None
                    print(
                        f"  localhost runtime issued grant for {platform_id}; "
                        f"state={current_grant['state']}"
                    )
                elif command == "scan":
                    if current_grant is None:
                        print("  rejected: issue a grant first")
                        continue
                    current_session = client.runtime_post(
                        "/scan",
                        {
                            **current_grant,
                            "channel_key": f"channel-{current_grant['platform_id']}",
                        },
                    )
                    print("  localhost scan accepted; grant=consumed; session=live")
                elif command == "request":
                    if current_session is None:
                        print("  rejected: scan a grant first")
                        continue
                    if pending_request_id is not None:
                        print("  rejected: resolve or stop the current Pending request first")
                        continue
                    request_number += 1
                    pending_request_id = f"localhost-request-{request_number}"
                    action = parts[1] if len(parts) > 1 else "greet_participant"
                    result = client.runtime_post(
                        "/request",
                        {
                            "request_id": pending_request_id,
                            "mission_s256": current_session["mission_s256"],
                            "session_id": current_session["session_id"],
                            "platform_id": current_session["platform_id"],
                            "channel_key": current_session["channel_key"],
                            "agent_id": "tip-jar-agent",
                            "action": action,
                            "catalog_version": "catalog-test-fixture",
                        },
                    )
                    print(f"  request crossed localhost; state={result['state']}")
                    print("  no governance decision, fake receipt, or physical outcome exists yet")
                elif command in {"allow", "deny"}:
                    if current_session is None or pending_request_id is None:
                        print("  rejected: there is no Pending request")
                        continue
                    request_id = pending_request_id
                    try:
                        receipt = client.deliver(
                            {
                                "session_id": current_session["session_id"],
                                "request_id": request_id,
                                "decision_reference": f"localhost-{command}-{request_id}",
                                "decision": command.upper(),
                            }
                        )
                        pending_request_id = None
                        print(
                            f"  governance crossed separate service={command.upper()}; "
                            f"adapter={receipt['adapter_status']}; "
                            f"physical={receipt['physical_outcome']}; "
                            f"phone={receipt['phone_status']}"
                        )
                    except LocalhostTransportError as exc:
                        pending_request_id = None
                        print(f"  governance arrived but was rejected at {exc.stage}:{exc.code}")
                elif command == "stop":
                    if current_session is None:
                        print("  rejected: there is no session")
                        continue
                    client.runtime_post("/stop", {"platform_id": current_session["platform_id"]})
                    print("  safety stop crossed localhost; session terminal; Pending cannot execute")
                elif command == "status":
                    show_status()
                elif command == "events":
                    show_events()
                else:
                    print("  unknown command; type help")
            except LocalhostTransportError as exc:
                print(f"  rejected at {exc.stage}:{exc.code}")
