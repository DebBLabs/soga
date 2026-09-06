"""SQLite persistence for the bounded M02 localhost Person Server."""

from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Mapping


class SQLitePersonServerStore:
    """Own explicit local PS state in one SQLite database.

    A lock protects one shared connection inside a process. SQLite transactions
    provide the database boundary; distributed deployment is outside M02.
    """

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        self._lock = threading.RLock()
        self._connection = sqlite3.connect(
            self.path,
            check_same_thread=False,
            isolation_level=None,
        )
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialize()

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            self._connection.execute("BEGIN IMMEDIATE")
            try:
                yield self._connection
            except BaseException:
                self._connection.execute("ROLLBACK")
                raise
            else:
                self._connection.execute("COMMIT")

    def _initialize(self) -> None:
        # executescript manages its own transaction boundary in sqlite3.
        with self._lock:
            self._connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS signing_keys (
                    key_id TEXT PRIMARY KEY,
                    algorithm TEXT NOT NULL CHECK (algorithm = 'HS256'),
                    secret BLOB NOT NULL,
                    active INTEGER NOT NULL CHECK (active IN (0, 1)),
                    created_at INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS missions (
                    mission_s256 TEXT PRIMARY KEY,
                    document_json TEXT NOT NULL,
                    retained_at INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tokens (
                    token_id TEXT PRIMARY KEY,
                    token_kind TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    audience TEXT NOT NULL,
                    mission_s256 TEXT,
                    issued_at INTEGER NOT NULL,
                    expires_at INTEGER NOT NULL,
                    key_id TEXT NOT NULL,
                    token_digest TEXT NOT NULL UNIQUE,
                    revoked_at INTEGER,
                    revocation_reason TEXT,
                    FOREIGN KEY (mission_s256) REFERENCES missions(mission_s256),
                    FOREIGN KEY (key_id) REFERENCES signing_keys(key_id)
                );

                CREATE TABLE IF NOT EXISTS events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    recorded_at INTEGER NOT NULL,
                    kind TEXT NOT NULL,
                    subject_reference TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS agent_keys (
                    agent_id TEXT PRIMARY KEY,
                    secret BLOB NOT NULL,
                    created_at INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS authenticated_requests (
                    request_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    request_digest TEXT NOT NULL,
                    accepted_at INTEGER NOT NULL,
                    FOREIGN KEY (agent_id) REFERENCES agent_keys(agent_id)
                );

                CREATE TABLE IF NOT EXISTS pending_permissions (
                    pending_id TEXT PRIMARY KEY,
                    request_id TEXT NOT NULL UNIQUE,
                    agent_id TEXT NOT NULL,
                    mission_s256 TEXT NOT NULL,
                    action TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    decision_json TEXT NOT NULL,
                    state TEXT NOT NULL CHECK (state IN ('pending', 'terminal')),
                    created_at INTEGER NOT NULL,
                    expires_at INTEGER NOT NULL,
                    result TEXT,
                    delivered INTEGER NOT NULL DEFAULT 0 CHECK (delivered IN (0, 1)),
                    FOREIGN KEY (mission_s256) REFERENCES missions(mission_s256),
                    FOREIGN KEY (agent_id) REFERENCES agent_keys(agent_id)
                );

                CREATE TABLE IF NOT EXISTS permission_results (
                    request_id TEXT PRIMARY KEY,
                    status INTEGER NOT NULL,
                    response_json TEXT NOT NULL
                );
                """
            )

    def register_agent_key(
        self, *, agent_id: str, secret: bytes, created_at: int
    ) -> None:
        if not agent_id or not secret:
            raise ValueError("agent identifier and secret are required")
        with self.transaction() as connection:
            connection.execute(
                "INSERT INTO agent_keys (agent_id, secret, created_at) VALUES (?, ?, ?)",
                (agent_id, secret, created_at),
            )

    def agent_secret(self, agent_id: str) -> bytes:
        with self._lock:
            row = self._connection.execute(
                "SELECT secret FROM agent_keys WHERE agent_id = ?", (agent_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"unknown agent: {agent_id}")
        return bytes(row["secret"])

    def consume_authenticated_request(
        self,
        *,
        request_id: str,
        agent_id: str,
        request_digest: str,
        accepted_at: int,
    ) -> bool:
        with self.transaction() as connection:
            existing = connection.execute(
                "SELECT agent_id, request_digest FROM authenticated_requests "
                "WHERE request_id = ?", (request_id,)
            ).fetchone()
            if existing is not None:
                if existing["agent_id"] != agent_id or existing["request_digest"] != request_digest:
                    raise ValueError("request_id is bound to different authenticated content")
                return False
            connection.execute(
                "INSERT INTO authenticated_requests "
                "(request_id, agent_id, request_digest, accepted_at) VALUES (?, ?, ?, ?)",
                (request_id, agent_id, request_digest, accepted_at),
            )
            return True

    def retain_permission_result(
        self, *, request_id: str, status: int, response: Mapping[str, Any]
    ) -> None:
        encoded = json.dumps(response, separators=(",", ":"), sort_keys=True)
        with self.transaction() as connection:
            connection.execute(
                "INSERT INTO permission_results (request_id, status, response_json) "
                "VALUES (?, ?, ?) ON CONFLICT(request_id) DO UPDATE SET "
                "status = excluded.status, response_json = excluded.response_json",
                (request_id, status, encoded)
            )

    def permission_result(self, request_id: str) -> tuple[int, dict[str, Any]] | None:
        with self._lock:
            row = self._connection.execute(
                "SELECT status, response_json FROM permission_results WHERE request_id = ?",
                (request_id,),
            ).fetchone()
        return (row["status"], json.loads(row["response_json"])) if row else None

    def add_signing_key(
        self,
        *,
        key_id: str,
        secret: bytes,
        created_at: int,
        active: bool = True,
    ) -> None:
        if not key_id or not secret:
            raise ValueError("key identifier and secret are required")
        with self.transaction() as connection:
            if active:
                connection.execute("UPDATE signing_keys SET active = 0")
            connection.execute(
                "INSERT INTO signing_keys "
                "(key_id, algorithm, secret, active, created_at) VALUES (?, 'HS256', ?, ?, ?)",
                (key_id, secret, int(active), created_at),
            )

    def signing_secret(self, key_id: str) -> bytes:
        with self._lock:
            row = self._connection.execute(
                "SELECT secret FROM signing_keys WHERE key_id = ?",
                (key_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"unknown signing key: {key_id}")
        return bytes(row["secret"])

    def active_signing_key(self) -> tuple[str, bytes]:
        with self._lock:
            row = self._connection.execute(
                "SELECT key_id, secret FROM signing_keys WHERE active = 1 "
                "ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
        if row is None:
            raise KeyError("no active signing key")
        return str(row["key_id"]), bytes(row["secret"])

    def key_descriptors(self) -> tuple[dict[str, Any], ...]:
        with self._lock:
            rows = self._connection.execute(
                "SELECT key_id, algorithm, active, created_at FROM signing_keys "
                "ORDER BY created_at, key_id"
            ).fetchall()
        return tuple(
            {
                "kid": row["key_id"],
                "kty": "oct",
                "alg": row["algorithm"],
                "use": "sig",
                "active": bool(row["active"]),
                "created_at": row["created_at"],
                "test_only": True,
            }
            for row in rows
        )

    def retain_mission(
        self,
        *,
        mission_s256: str,
        document: Mapping[str, Any],
        retained_at: int,
    ) -> None:
        encoded = json.dumps(document, separators=(",", ":"), sort_keys=True)
        with self.transaction() as connection:
            existing = connection.execute(
                "SELECT document_json FROM missions WHERE mission_s256 = ?",
                (mission_s256,),
            ).fetchone()
            if existing is not None:
                if existing["document_json"] != encoded:
                    raise ValueError("mission identifier is already bound to different content")
                return
            connection.execute(
                "INSERT INTO missions (mission_s256, document_json, retained_at) "
                "VALUES (?, ?, ?)",
                (mission_s256, encoded, retained_at),
            )

    def mission(self, mission_s256: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._connection.execute(
                "SELECT document_json FROM missions WHERE mission_s256 = ?",
                (mission_s256,),
            ).fetchone()
        return json.loads(row["document_json"]) if row is not None else None

    def retain_token(self, record: Mapping[str, Any]) -> None:
        with self.transaction() as connection:
            connection.execute(
                """
                INSERT INTO tokens (
                    token_id, token_kind, subject, audience, mission_s256,
                    issued_at, expires_at, key_id, token_digest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["token_id"],
                    record["token_kind"],
                    record["subject"],
                    record["audience"],
                    record.get("mission_s256"),
                    record["issued_at"],
                    record["expires_at"],
                    record["key_id"],
                    record["token_digest"],
                ),
            )

    def token_record(self, token_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._connection.execute(
                "SELECT * FROM tokens WHERE token_id = ?",
                (token_id,),
            ).fetchone()
        return dict(row) if row is not None else None

    def revoke_token(self, *, token_id: str, revoked_at: int, reason: str) -> bool:
        with self.transaction() as connection:
            result = connection.execute(
                "UPDATE tokens SET revoked_at = ?, revocation_reason = ? "
                "WHERE token_id = ? AND revoked_at IS NULL",
                (revoked_at, reason, token_id),
            )
            return result.rowcount == 1

    def append_event(
        self,
        *,
        recorded_at: int,
        kind: str,
        subject_reference: str,
        payload: Mapping[str, Any],
    ) -> None:
        encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        with self.transaction() as connection:
            connection.execute(
                "INSERT INTO events (recorded_at, kind, subject_reference, payload_json) "
                "VALUES (?, ?, ?, ?)",
                (recorded_at, kind, subject_reference, encoded),
            )

    def create_pending(self, record: Mapping[str, Any]) -> None:
        with self.transaction() as connection:
            connection.execute(
                """INSERT INTO pending_permissions
                (pending_id, request_id, agent_id, mission_s256, action,
                 request_json, decision_json, state, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)""",
                (
                    record["pending_id"], record["request_id"], record["agent_id"],
                    record["mission_s256"], record["action"],
                    json.dumps(record["request"], separators=(",", ":"), sort_keys=True),
                    json.dumps(record["decision"], separators=(",", ":"), sort_keys=True),
                    record["created_at"], record["expires_at"],
                ),
            )

    def pending(self, pending_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._connection.execute(
                "SELECT * FROM pending_permissions WHERE pending_id = ?", (pending_id,)
            ).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["request"] = json.loads(result.pop("request_json"))
        result["decision"] = json.loads(result.pop("decision_json"))
        return result

    def finish_pending(self, *, pending_id: str, result: str) -> bool:
        with self.transaction() as connection:
            updated = connection.execute(
                "UPDATE pending_permissions SET state = 'terminal', result = ? "
                "WHERE pending_id = ? AND state = 'pending'",
                (result, pending_id),
            )
            return updated.rowcount == 1

    def deliver_pending_result(
        self, *, pending_id: str, agent_id: str
    ) -> tuple[str, int | None, dict[str, Any] | None]:
        """Atomically deliver one retained terminal result to its bound agent."""

        with self.transaction() as connection:
            row = connection.execute(
                """SELECT p.state, p.delivered, r.status, r.response_json
                FROM pending_permissions AS p
                LEFT JOIN permission_results AS r ON r.request_id = p.request_id
                WHERE p.pending_id = ? AND p.agent_id = ?""",
                (pending_id, agent_id),
            ).fetchone()
            if row is None:
                return "missing", None, None
            if row["state"] == "pending":
                return "pending", None, None
            if row["delivered"]:
                return "gone", None, None
            if row["status"] is None or row["response_json"] is None:
                raise RuntimeError("terminal pending request has no retained result")
            updated = connection.execute(
                "UPDATE pending_permissions SET delivered = 1 "
                "WHERE pending_id = ? AND delivered = 0",
                (pending_id,),
            )
            if updated.rowcount != 1:
                return "gone", None, None
            return "deliver", int(row["status"]), json.loads(row["response_json"])

    def events(self) -> tuple[dict[str, Any], ...]:
        with self._lock:
            rows = self._connection.execute(
                "SELECT * FROM events ORDER BY sequence"
            ).fetchall()
        return tuple(
            {
                **dict(row),
                "payload": json.loads(row["payload_json"]),
            }
            for row in rows
        )
