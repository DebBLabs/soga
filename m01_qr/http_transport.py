from __future__ import annotations

import json
from typing import Mapping
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class TransportError(RuntimeError):
    pass


class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise TransportError(f"redirect_rejected:{code}")


class StrictJsonPostTransport:
    """Small POST-only transport with no discovery, redirects, or retries."""

    def __init__(self, *, timeout_seconds: float = 2.0, max_response_bytes: int = 65536):
        if timeout_seconds <= 0 or timeout_seconds > 5:
            raise TransportError("invalid_timeout")
        if max_response_bytes <= 0 or max_response_bytes > 65536:
            raise TransportError("invalid_response_bound")
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes
        self._opener = build_opener(_NoRedirects())

    def __call__(self, url: str, payload: Mapping[str, int]) -> Mapping[str, object]:
        if not url.startswith(("http://", "https://")):
            raise TransportError("invalid_url")
        request = Request(
            url,
            data=json.dumps(dict(payload), separators=(",", ":")).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            with self._opener.open(request, timeout=self.timeout_seconds) as response:
                raw = response.read(self.max_response_bytes + 1)
                if len(raw) > self.max_response_bytes:
                    raise TransportError("response_too_large")
                if response.status < 200 or response.status >= 300:
                    raise TransportError(f"http_status:{response.status}")
        except HTTPError as exc:
            raise TransportError(f"http_status:{exc.code}") from exc
        try:
            decoded = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TransportError("invalid_json_response") from exc
        if not isinstance(decoded, dict):
            raise TransportError("non_object_response")
        return decoded
