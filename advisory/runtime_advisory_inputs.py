from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from advisory.agent_evidence import AgentEvidence


@dataclass
class RuntimeAdvisoryInputs:
    """
    Advisory evidence carried by the Runtime Envelope.

    Zero or more advisory inputs.
    """

    advisory_agents: List[AgentEvidence] = field(
        default_factory=list
    )

    def add(
        self,
        evidence: AgentEvidence,
    ) -> None:
        self.advisory_agents.append(
            evidence
        )

    def to_list(self):
        return [
            agent.to_dict()
            for agent in self.advisory_agents
        ]
