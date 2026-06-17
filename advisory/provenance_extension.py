from __future__ import annotations

from advisory.runtime_advisory_inputs import (
    RuntimeAdvisoryInputs,
)


def advisory_provenance(
    advisory_inputs: RuntimeAdvisoryInputs,
):
    """
    Provenance extension only.

    Records advisory evidence contributors.

    Does not alter governance authority.
    """

    return {
        "governance_source": "GovernancePDP",
        "advisory_agents": advisory_inputs.to_list(),
    }
