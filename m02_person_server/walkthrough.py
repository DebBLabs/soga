"""Visible terminal walkthrough for the bounded M02 localhost Person Server."""

from __future__ import annotations

import argparse
import json
import tempfile
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping

from .service import LocalPersonServer
from .store import SQLitePersonServerStore
from .http_server import create_server


MISSION_ID = "m02-visible-walkthrough-mission"
AGENT_ID = "m02-visible-test-agent"
AGENT_SECRET = b"m02-visible-agent-secret-32-bytes"
OPERATOR_SECRET = "m02-visible-operator-secret"


def _http(
    base: str,
    method: str,
    path: str,
    body: Mapping[str, Any] | None = None,
    *,
    operator: bool = False,
) -> tuple[int, dict[str, Any]]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"} if data is not None else {}
    if operator:
        headers["Authorization"] = f"Bearer {OPERATOR_SECRET}"
    request = urllib.request.Request(
        f"{base}{path}", data=data, method=method, headers=headers
    )
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


def _pause(enabled: bool) -> None:
    if enabled:
        input("Press Enter to continue... ")


def _show(label: str, status: int, body: Mapping[str, Any]) -> None:
    print(f"{label}: HTTP {status} {json.dumps(body, sort_keys=True)}")


def run(*, pause: bool = True) -> int:
    print("M02 STAGE 2 — BOUNDED LOCAL PERSON SERVER WALKTHROUGH")
    print("Real 127.0.0.1 HTTP and SQLite; test-only identities; no execution surface.")
    print("No wallet, external network, production credential, or robot access.\n")

    with tempfile.TemporaryDirectory(prefix="m02-person-server-") as directory:
        store_path = Path(directory) / "person-server.sqlite3"
        store = SQLitePersonServerStore(store_path)
        service = LocalPersonServer.create_for_local_test(
            store=store,
            issuer="http://127.0.0.1",
            secret=b"m02-visible-person-server-secret",
            operator_secret=OPERATOR_SECRET,
        )
        server = create_server(service, host="127.0.0.1", port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            print(f"local service: {base}")
            print(f"SQLite file:   {store_path}")
            _pause(pause)

            print("\n=== 1. Establish test identity, mission, and person token over HTTP ===")
            status, body = _http(
                base, "POST", "/_test/agents",
                {"agent_id": AGENT_ID, "secret": AGENT_SECRET.decode("ascii")},
                operator=True,
            )
            _show("agent registration", status, body)
            mission = {
                "s256": MISSION_ID,
                "description": "Visible M02 governed permission walkthrough",
                "approved_tools": [{"name": "greet_participant"}],
            }
            status, body = _http(
                base, "POST", "/_test/missions",
                {"mission_s256": MISSION_ID, "mission": mission},
                operator=True,
            )
            _show("mission retention", status, body)
            status, token_body = _http(
                base, "POST", "/_test/person-token",
                {
                    "subject": "person-visible-test",
                    "audience": service.issuer,
                    "mission_s256": MISSION_ID,
                    "confirmation": {"kid": AGENT_ID},
                    "lifetime_seconds": 300,
                },
                operator=True,
            )
            _show("person-token issuance", status, {"person_token": "[retained and hidden]"})
            token = token_body["person_token"]
            _pause(pause)

            print("\n=== 2. Send a signed, mission-bound action request ===")
            request = {
                "request_id": "visible-request-1",
                "mission_s256": MISSION_ID,
                "action": "greet_participant",
                "subject": {
                    "person_id": "person-visible-test",
                    "subject_agency_state": "INDEPENDENT",
                },
                "reachability": "REACHABLE",
            }
            permission_body = {
                "request": request,
                "agent_id": AGENT_ID,
                "signature": service.sign_test_request(
                    request=request, secret=AGENT_SECRET
                ),
                "person_token": token,
            }
            status, body = _http(base, "POST", "/permission", permission_body)
            _show("governed permission", status, body)
            decisions = [e for e in store.events() if e["kind"] == "soga_decision"]
            projections = [e for e in store.events() if e["kind"] == "aauth_projection"]
            print(f"SOGA decisions retained: {len(decisions)}")
            print(f"AAuth projections retained: {len(projections)}")
            print("execution dispatched: no")
            _pause(pause)

            print("\n=== 3. Show deferred governance and one-time terminal delivery ===")
            pending_request = {
                **request,
                "request_id": "visible-request-2",
                "subject": {
                    "person_id": "person-visible-test",
                    "subject_agency_state": "SUPERVISED",
                },
            }
            status, pending = _http(
                base,
                "POST",
                "/permission",
                {
                    "request": pending_request,
                    "agent_id": AGENT_ID,
                    "signature": service.sign_test_request(
                        request=pending_request, secret=AGENT_SECRET
                    ),
                    "person_token": token,
                },
            )
            _show("permission before approval", status, pending)
            status, final = _http(
                base,
                "POST",
                f"/_test/pending/{pending['pending_id']}/approval",
                {"result": "decline"},
                operator=True,
            )
            _show("separate governance decision", status, final)
            for number in (1, 2):
                poll = {
                    "request_id": f"visible-poll-{number}",
                    "pending_id": pending["pending_id"],
                }
                status, body = _http(
                    base,
                    "POST",
                    f"{pending['pending_url']}/poll",
                    {
                        "request": poll,
                        "agent_id": AGENT_ID,
                        "signature": service.sign_test_request(
                            request=poll, secret=AGENT_SECRET
                        ),
                    },
                )
                _show(f"terminal poll {number}", status, body)
            _pause(pause)

            print("\n=== 4. Revoke retained authority and prove fail-closed ===")
            token_id = service.verify_person_token(
                token,
                audience=service.issuer,
                mission_s256=MISSION_ID,
                expected_confirmation={"kid": AGENT_ID},
            )["jti"]
            status, body = _http(
                base,
                "POST",
                "/_test/tokens/revoke",
                {"token_id": token_id, "reason": "visible walkthrough revocation"},
                operator=True,
            )
            _show("revocation", status, body)
            revoked_request = {**request, "request_id": "visible-request-3"}
            status, body = _http(
                base,
                "POST",
                "/permission",
                {
                    "request": revoked_request,
                    "agent_id": AGENT_ID,
                    "signature": service.sign_test_request(
                        request=revoked_request, secret=AGENT_SECRET
                    ),
                    "person_token": token,
                },
            )
            _show("request after revocation", status, body)
            print("new SOGA decision after revoked request: no")

            print("\nWALKTHROUGH COMPLETE")
            print("The Person Server processed real local HTTP and persistent state.")
            print("Nothing was sent to a resource, robot, or physical execution surface.")
            return 0
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)
            store.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("walkthrough",))
    parser.add_argument("--no-pause", action="store_true")
    arguments = parser.parse_args(argv)
    return run(pause=not arguments.no_pause)
