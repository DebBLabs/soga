#!/usr/bin/env python3
from __future__ import annotations

import argparse
import secrets
import sys
import time
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from m01_qr import M01Flow, MistySignalLightAdapter, StrictJsonPostTransport


PLATFORM_ID = "urn:debblabs:misty-a:20221304273"
EXPECTED_AUTHORIZATION = "D-032"


def authorization_is_recorded(decision_text: str | None = None) -> bool:
    if decision_text is None:
        decision_log = REPOSITORY_ROOT / "knowledge" / "strategy" / "DECISION_LOG.md"
        decision_text = decision_log.read_text(encoding="utf-8")
    return "## D-032 —" in decision_text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the single governed M01 Misty A signal-light action."
    )
    parser.add_argument("--api-base-url", required=True)
    parser.add_argument("--authorization", required=True)
    args = parser.parse_args()
    if args.authorization != EXPECTED_AUTHORIZATION:
        raise SystemExit("Physical execution blocked: D-032 is required")
    if not authorization_is_recorded():
        raise SystemExit("Physical execution blocked: D-032 is not recorded")

    adapter = MistySignalLightAdapter(
        platform_id=PLATFORM_ID,
        api_base_url=args.api_base_url,
        transport=StrictJsonPostTransport(timeout_seconds=2.0),
        wait=time.sleep,
        duration_seconds=1.0,
    )
    flow = M01Flow(
        monotonic=time.monotonic,
        platform_id=PLATFORM_ID,
        execution_adapter=adapter,
    )
    offer = flow.offer(grant_id="m01-physical-" + secrets.token_hex(8))
    print("M01 PHYSICAL EXECUTION — ONE ACTION")
    print("Platform:", PLATFORM_ID)
    print("Target:", args.api_base_url)
    print("QR grant:", offer.qr_payload)
    print("Action: pink (255,105,180) for 1.0 second, then yellow (255,255,0)")
    try:
        confirmation = input('Type EXECUTE m01.signal_light and press Enter: ')
    except EOFError:
        confirmation = ""
    if confirmation != "EXECUTE m01.signal_light":
        raise SystemExit("Physical execution cancelled: confirmation mismatch")

    receipt = flow.scan_and_request(
        offer.qr_payload,
        channel_key="m01-physical-local-terminal",
        request_id="m01-physical-request-" + secrets.token_hex(8),
    )
    print("Governance:", receipt["governance_projection"])
    print("Adapter:", receipt["adapter_status"])
    print("Signal API:", receipt["signal_adapter_status"])
    print("Neutral API:", receipt["neutral_adapter_status"])
    print("Physical outcome:", receipt["physical_outcome"])
    print("Neutral outcome:", receipt["neutral_outcome"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
