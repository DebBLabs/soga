from __future__ import annotations
from typing import Any, Dict
def invoke_mcp_style_capability(
    decision_package: Dict[str, Any],
    capability: str,
) -> Dict[str, Any]:
    """
    Representative MCP-style capability invocation stub.
    Stub boundary:
    - no MCP transport
    - no MCP SDK
    - no external libraries
    - no execution side effects
    The stub consumes a Canonical Decision Package-shaped dictionary
    and returns what an MCP/tool boundary would need to know.
    """
    determination = decision_package.get("governance_determination")
    if isinstance(determination, dict):
        determination = determination.get("value")
    if determination is None:
        determination = decision_package.get("decision")
    return {
        "capability": capability,
        "transport": "mcp-style-stub",
        "governance_determination": determination,
        "would_invoke": determination == "ALLOW",
        "decision_package_received": True,
        "governance_reasoning_token": decision_package.get(
            "governance_reasoning_token"
        ),
    }
