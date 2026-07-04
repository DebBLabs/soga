class CapabilityRegistry:
    """
    Descriptive registry for canonical capabilities.
    The registry stores static metadata and available
    implementation options for a capability.
    It does not:
    - map actions to capabilities
    - inspect standing subject capabilities
    - determine FOUND / MISSING / PROHIBITED
    - analyze capability gaps
    - parse authority scopes
    - evaluate governance conditions
    - select or invoke implementations
    """
    def __init__(self):
        self._capabilities = {}
    def register(
        self,
        canonical_name,
        implementations,
        required_authority_scope,
        governance_dimensions_affected,
    ):
        self._capabilities[canonical_name] = {
            "canonical_name": canonical_name,
            "implementations": implementations,
            "required_authority_scope": required_authority_scope,
            "governance_dimensions_affected":
                governance_dimensions_affected,
        }
    def resolve(self, canonical_name):
        capability = self._capabilities.get(canonical_name)
        if capability is None:
            return {
                "canonical_name": canonical_name,
                "status": "UNREGISTERED",
                "implementations": [],
                "required_authority_scope": None,
                "governance_dimensions_affected": [],
            }
        return {
            "canonical_name": capability["canonical_name"],
            "status": "REGISTERED",
            "implementations": capability["implementations"],
            "required_authority_scope":
                capability["required_authority_scope"],
            "governance_dimensions_affected":
                capability["governance_dimensions_affected"],
        }
    def list_capabilities(self):
        return sorted(self._capabilities.keys())
