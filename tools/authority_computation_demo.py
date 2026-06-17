from datetime import datetime, timedelta, timezone
from pprint import pprint

from engines.authority_computation_engine import (
    AuthorityComputationEngine,
)

authority = {
    "delegation_time":
        datetime.now(timezone.utc)
        - timedelta(days=2),

    "execution_time":
        datetime.now(timezone.utc),

    "delegation_chain": [
        "principal",
        "attorney",
        "agent",
    ],

    "max_elapsed_seconds":
        86400,

    "max_delegation_hops":
        2,
}

print()
print("AUTHORITY COMPUTATION DEMO")
print("==========================")
print()

pprint(
    AuthorityComputationEngine().compute(
        authority
    )
)
