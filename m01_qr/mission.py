from __future__ import annotations

from aauth_permission.models import Mission


APPROVER_ID = "urn:debblabs:person-server:deb-bucci"
AGENT_ID = "soga-m01-misty-a-qr-agent-v1"
ACTION = "m01.signal_light"
CATALOG_VERSION = "m01-c1-v1"
APPROVED_AT = "2026-09-05T18:26:42Z"


def build_mission() -> Mission:
    """Return the immutable M01 mission authorized by Deb on 2026-09-05."""
    return Mission.approve(
        approver=APPROVER_ID,
        agent=AGENT_ID,
        approved_at=APPROVED_AT,
        approved_tools=[
            {
                "name": ACTION,
                "description": (
                    "Request one catalog-bounded signal-light action on the "
                    "explicitly bound M01 Misty A recording surface."
                ),
            }
        ],
        description=(
            "Permit the M01 mission agent to process a QR-originated request "
            "for one governed signal-light action on the explicitly bound "
            "Misty A platform, subject to current authorization, safety, "
            "cardinality, and truthful-receipt requirements."
        ),
    )
