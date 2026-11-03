from __future__ import annotations

import json
import socket
import time
from collections.abc import Callable, Mapping


HOST = "192.168.8.219"
PORT = 80
SPEAK_PATH = "/api/tts/speak"
STOP_PATH = "/api/tts/stop"
SPEAK_URL = f"http://{HOST}{SPEAK_PATH}"
STOP_URL = f"http://{HOST}{STOP_PATH}"
ALLOWED_URLS = {SPEAK_URL: SPEAK_PATH, STOP_URL: STOP_PATH}


class StrictTransportError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _validate_payload(url: str, payload: Mapping[str, object]) -> dict[str, object]:
    body = dict(payload)
    if url == STOP_URL:
        if body:
            raise StrictTransportError("invalid_stop_payload")
        return body
    if url != SPEAK_URL:
        raise StrictTransportError("target_not_allowlisted")
    if set(body) != {"Text", "Flush", "UtteranceId"}:
        raise StrictTransportError("invalid_speak_fields")
    if body["Text"] != "Would you like to dance?" or body["Flush"] is not True:
        raise StrictTransportError("invalid_speak_payload")
    utterance_id = body["UtteranceId"]
    if not isinstance(utterance_id, str) or len(utterance_id) != 36 or not utterance_id.startswith("pts-"):
        raise StrictTransportError("invalid_utterance_id")
    if any(character not in "0123456789abcdef" for character in utterance_id[4:]):
        raise StrictTransportError("invalid_utterance_id")
    return body


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise StrictTransportError("duplicate_json_key")
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


class StrictJsonPostTransport:
    """Literal-IP HTTP/1.1 POST with one total wall-clock deadline."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 2.0,
        max_response_bytes: int = 65_536,
        socket_factory: Callable[..., socket.socket] = socket.create_connection,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        if not 0 < timeout_seconds <= 2.0:
            raise StrictTransportError("invalid_timeout")
        if not 0 < max_response_bytes <= 65_536:
            raise StrictTransportError("invalid_response_bound")
        self.timeout_seconds = float(timeout_seconds)
        self.max_response_bytes = int(max_response_bytes)
        self._socket_factory = socket_factory
        self._monotonic = monotonic

    def _remaining(self, deadline: float) -> float:
        remaining = deadline - self._monotonic()
        if remaining <= 0:
            raise StrictTransportError("total_timeout")
        return remaining

    def __call__(self, url: str, payload: Mapping[str, object]) -> dict[str, object]:
        path = ALLOWED_URLS.get(url)
        if path is None:
            raise StrictTransportError("target_not_allowlisted")
        body = _validate_payload(url, payload)
        encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if len(encoded) > 512:
            raise StrictTransportError("request_too_large")
        request = (
            f"POST {path} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Accept: application/json\r\n"
            "Content-Type: application/json\r\n"
            "Connection: close\r\n"
            f"Content-Length: {len(encoded)}\r\n\r\n"
        ).encode("ascii") + encoded
        deadline = self._monotonic() + self.timeout_seconds
        connection = None
        raw = bytearray()
        try:
            connection = self._socket_factory((HOST, PORT), timeout=self._remaining(deadline))
            connection.settimeout(self._remaining(deadline))
            connection.sendall(request)
            while True:
                connection.settimeout(self._remaining(deadline))
                chunk = connection.recv(8192)
                if not chunk:
                    break
                raw.extend(chunk)
                if len(raw) > self.max_response_bytes + 8192:
                    raise StrictTransportError("response_too_large")
        except StrictTransportError:
            raise
        except (TimeoutError, socket.timeout) as exc:
            raise StrictTransportError("total_timeout") from exc
        except OSError as exc:
            raise StrictTransportError("transport_failure") from exc
        finally:
            if connection is not None:
                try:
                    connection.close()
                except OSError:
                    pass
        return self._decode_response(bytes(raw))

    def _decode_response(self, raw: bytes) -> dict[str, object]:
        try:
            header_block, body = raw.split(b"\r\n\r\n", 1)
            header_lines = header_block.decode("iso-8859-1").split("\r\n")
            parts = header_lines[0].split(" ", 2)
            status = int(parts[1])
        except (ValueError, UnicodeDecodeError, IndexError) as exc:
            raise StrictTransportError("invalid_http_response") from exc
        if not 200 <= status < 300:
            raise StrictTransportError("http_status")
        headers = {}
        for line in header_lines[1:]:
            if ":" not in line:
                raise StrictTransportError("invalid_http_header")
            name, value = line.split(":", 1)
            lowered = name.strip().lower()
            if lowered in headers:
                raise StrictTransportError("duplicate_http_header")
            headers[lowered] = value.strip()
        if headers.get("transfer-encoding", "").lower() == "chunked":
            body = self._decode_chunked(body)
        elif "content-length" in headers:
            try:
                length = int(headers["content-length"])
            except ValueError as exc:
                raise StrictTransportError("invalid_content_length") from exc
            if length != len(body):
                raise StrictTransportError("content_length_mismatch")
        if len(body) > self.max_response_bytes:
            raise StrictTransportError("response_too_large")
        try:
            decoded = json.loads(body.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
        except StrictTransportError:
            raise
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise StrictTransportError("invalid_json_response") from exc
        if not isinstance(decoded, dict):
            raise StrictTransportError("non_object_response")
        return decoded

    @staticmethod
    def _decode_chunked(body: bytes) -> bytes:
        output = bytearray()
        cursor = 0
        while True:
            line_end = body.find(b"\r\n", cursor)
            if line_end < 0:
                raise StrictTransportError("invalid_chunked_response")
            size_text = body[cursor:line_end].split(b";", 1)[0]
            try:
                size = int(size_text, 16)
            except ValueError as exc:
                raise StrictTransportError("invalid_chunked_response") from exc
            cursor = line_end + 2
            if size == 0:
                return bytes(output)
            end = cursor + size
            if end + 2 > len(body) or body[end:end + 2] != b"\r\n":
                raise StrictTransportError("invalid_chunked_response")
            output.extend(body[cursor:end])
            cursor = end + 2
