"""M01 governed QR-to-recording-surface prototype.

Its prepared Misty adapter requires an explicitly injected target and transport;
the package itself contains no network client or discovery mechanism.
"""

from .flow import M01Flow, M01FlowError
from .http_transport import StrictJsonPostTransport, TransportError
from .mission import ACTION, AGENT_ID, APPROVER_ID, CATALOG_VERSION, build_mission
from .misty_signal_adapter import MistySignalLightAdapter

__all__ = [
    "ACTION",
    "AGENT_ID",
    "APPROVER_ID",
    "CATALOG_VERSION",
    "M01Flow",
    "M01FlowError",
    "MistySignalLightAdapter",
    "StrictJsonPostTransport",
    "TransportError",
    "build_mission",
]
