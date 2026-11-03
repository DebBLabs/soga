"""Additive, target-bound robot invitation gateway.

This package is not connected to the accepted public Flow A presentation.
"""

from .coordinator import RobotInvitationCoordinator
from .gateway import RobotGateway, RobotGatewayError
from .misty_invitation import MISTY_B_PLATFORM_ID, MistyInvitationAdapter
from .unavailable_mbot2 import MBOT2_UNAVAILABLE_PLATFORM_ID, UnavailableMbot2Adapter

__all__ = (
    "MBOT2_UNAVAILABLE_PLATFORM_ID",
    "MISTY_B_PLATFORM_ID",
    "MistyInvitationAdapter",
    "RobotGateway",
    "RobotGatewayError",
    "RobotInvitationCoordinator",
    "UnavailableMbot2Adapter",
)
