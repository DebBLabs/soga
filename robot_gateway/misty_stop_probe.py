from __future__ import annotations

import json
import socket
import time
from typing import Callable, Mapping


HOST = "192.168.8.219"
PORT = 80
LOCAL_HOST = "192.168.8.247"
TARGET = (HOST, PORT)
LOCAL_SOURCE = (LOCAL_HOST, 0)
TIMEOUT_SECONDS = 2.0
MAX_RAW_RESPONSE_BYTES = 73_728
MAX_BODY_BYTES = 65_536
REQUEST_BYTES = (
    b"POST /api/tts/stop HTTP/1.1\r\n"
    b"Host: 192.168.8.219\r\n"
    b"Accept: application/json\r\n"
    b"Content-Type: application/json\r\n"
    b"Connection: close\r\n"
    b"Content-Length: 2\r\n\r\n{}"
)
REQUEST_SHA256 = "863897eae5c306229ffaed3ebfd943fe1c99a03a8753ef8922df174c2d8f13ab"


class ProbeParseError(ValueError):
    pass


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProbeParseError("duplicate_json_key")
        result[key] = value
    return result


def response_is_acknowledged(response: Mapping[str, object]) -> bool:
    if "error" in response or "Error" in response:
        return False
    if response.get("result") is not True:
        return False
    if "status" in response and response["status"] != "Success":
        return False
    return True


def _decode_chunked(body: bytes) -> bytes:
    output = bytearray()
    cursor = 0
    while True:
        line_end = body.find(b"\r\n", cursor)
        if line_end < 0:
            raise ProbeParseError("invalid_chunked_response")
        size_text = body[cursor:line_end].split(b";", 1)[0]
        if not size_text or any(byte not in b"0123456789abcdefABCDEF" for byte in size_text):
            raise ProbeParseError("invalid_chunked_response")
        try:
            size = int(size_text, 16)
        except ValueError as exc:
            raise ProbeParseError("invalid_chunked_response") from exc
        cursor = line_end + 2
        if size == 0:
            if body[cursor:] != b"\r\n":
                raise ProbeParseError("invalid_chunked_response")
            if len(output) > MAX_BODY_BYTES:
                raise OverflowError("body_overflow")
            return bytes(output)
        end = cursor + size
        if end + 2 > len(body) or body[end:end + 2] != b"\r\n":
            raise ProbeParseError("invalid_chunked_response")
        output.extend(body[cursor:end])
        if len(output) > MAX_BODY_BYTES:
            raise OverflowError("body_overflow")
        cursor = end + 2


def classify_response(raw: bytes, *, eof: bool) -> dict[str, object]:
    if len(raw) > MAX_RAW_RESPONSE_BYTES:
        return {"classification": "OVERFLOW", "http_status": None, "acknowledged": False}
    if not eof:
        return {"classification": "TIMED_OUT", "http_status": None, "acknowledged": False}
    try:
        header_block, body = raw.split(b"\r\n\r\n", 1)
        lines = header_block.decode("iso-8859-1").split("\r\n")
        parts = lines[0].split(" ", 2)
        if len(parts) < 2 or parts[0] not in ("HTTP/1.0", "HTTP/1.1"):
            raise ProbeParseError("invalid_http_status_line")
        if len(parts[1]) != 3 or not parts[1].isascii() or not parts[1].isdigit():
            raise ProbeParseError("invalid_http_status_line")
        status = int(parts[1])
    except (ValueError, UnicodeDecodeError, IndexError) as exc:
        raise ProbeParseError("invalid_http_response") from exc

    if not 100 <= status <= 599:
        raise ProbeParseError("invalid_http_status")

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            raise ProbeParseError("invalid_http_header")
        name, value = line.split(":", 1)
        if not name or name != name.strip() or any(ch.isspace() for ch in name):
            raise ProbeParseError("invalid_http_header")
        lowered = name.lower()
        if lowered in headers:
            raise ProbeParseError("duplicate_http_header")
        headers[lowered] = value.strip()
    transfer_encoding = headers.get("transfer-encoding")
    if transfer_encoding is not None and transfer_encoding.lower() != "chunked":
        raise ProbeParseError("unsupported_transfer_encoding")
    if transfer_encoding is not None and "content-length" in headers:
        raise ProbeParseError("conflicting_http_framing")
    if transfer_encoding is not None:
        body = _decode_chunked(body)
    elif "content-length" in headers:
        try:
            length_text = headers["content-length"]
            if not length_text or not length_text.isascii() or not length_text.isdigit():
                raise ValueError
            length = int(length_text)
        except ValueError as exc:
            raise ProbeParseError("invalid_content_length") from exc
        if length != len(body):
            raise ProbeParseError("content_length_mismatch")
    if len(body) > MAX_BODY_BYTES:
        raise OverflowError("body_overflow")
    parser_facts: dict[str, object] = {
        "http_version": parts[0],
        "http_status": status,
        "framed_body_bytes": len(body),
        "chunked": headers.get("transfer-encoding", "").lower() == "chunked",
    }
    if not 200 <= status < 300:
        return {**parser_facts, "classification": "REJECTED", "acknowledged": False}
    try:
        decoded = json.loads(body.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except ProbeParseError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ProbeParseError("invalid_json_response") from exc
    if not isinstance(decoded, dict):
        raise ProbeParseError("non_object_response")
    acknowledged = response_is_acknowledged(decoded)
    return {
        **parser_facts,
        "classification": "ACKNOWLEDGED" if acknowledged else "REJECTED",
        "acknowledged": acknowledged,
        "json_keys": sorted(decoded),
        "result_is_true": decoded.get("result") is True,
        "status_value": decoded.get("status") if isinstance(decoded.get("status"), str) else None,
        "has_error_key": "error" in decoded or "Error" in decoded,
    }


def run_probe(
    *,
    socket_factory: Callable[..., socket.socket] = socket.create_connection,
    monotonic: Callable[[], float] = time.monotonic,
) -> tuple[dict[str, object], bytes]:
    started = monotonic()
    deadline = started + TIMEOUT_SECONDS
    progress: dict[str, object] = {
        "connection_created": False,
        "local_bound": False,
        "connected": False,
        "bytes_sent": 0,
        "eof_received": False,
    }
    raw = bytearray()
    connection = None

    def remaining() -> float:
        value = deadline - monotonic()
        if value <= 0:
            raise TimeoutError("deadline")
        return value

    try:
        connection = socket_factory(TARGET, timeout=remaining(), source_address=LOCAL_SOURCE)
        progress["connection_created"] = True
        progress["connected"] = True
        local = connection.getsockname()
        progress["local_bound"] = bool(local and local[0] == LOCAL_HOST)
        if not progress["local_bound"]:
            return ({**progress, "classification": "TRANSPORT_FAILED", "delivery": "not_sent"}, bytes(raw))
        connection.settimeout(remaining())
        view = memoryview(REQUEST_BYTES)
        while progress["bytes_sent"] < len(REQUEST_BYTES):
            connection.settimeout(remaining())
            sent = connection.send(view[progress["bytes_sent"]:])
            if not isinstance(sent, int) or sent <= 0:
                raise OSError("send_failed")
            progress["bytes_sent"] += sent
        while True:
            connection.settimeout(remaining())
            chunk = connection.recv(8192)
            if not chunk:
                progress["eof_received"] = True
                break
            raw.extend(chunk)
            if len(raw) > MAX_RAW_RESPONSE_BYTES:
                return ({**progress, "classification": "OVERFLOW", "delivery": "unknown"}, bytes(raw[:MAX_RAW_RESPONSE_BYTES]))
        try:
            parsed = classify_response(bytes(raw), eof=True)
        except OverflowError:
            parsed = {"classification": "OVERFLOW", "http_status": None, "acknowledged": False}
        except ProbeParseError:
            parsed = {"classification": "MALFORMED", "http_status": None, "acknowledged": False}
        return ({**progress, **parsed, "delivery": "unknown"}, bytes(raw))
    except (TimeoutError, socket.timeout):
        return ({**progress, "classification": "TIMED_OUT", "delivery": "unknown" if progress["bytes_sent"] else "not_sent"}, bytes(raw))
    except OSError:
        return ({**progress, "classification": "TRANSPORT_FAILED", "delivery": "unknown" if progress["bytes_sent"] else "not_sent"}, bytes(raw))
    finally:
        if connection is not None:
            try:
                connection.close()
            except OSError:
                pass
