from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class CandidateObservation:
    semantic_type: str
    value: str
    asserted_by: str
    source_ref: str
    confidence: float
    status: str
    evidence: str


class ObservationExtractor:
    def extract(self, text: str) -> list[dict[str, Any]]:
        lower = text.lower()
        observations: list[CandidateObservation] = []

        if "niece" in lower:
            observations.append(
                CandidateObservation(
                    semantic_type="delegate",
                    value="niece",
                    asserted_by="subject",
                    source_ref="original_request",
                    confidence=0.72,
                    status="PROPOSED",
                    evidence=text,
                )
            )

        if "medical appointment" in lower or "medical appointments" in lower:
            observations.append(
                CandidateObservation(
                    semantic_type="objective",
                    value="manage medical appointments",
                    asserted_by="subject",
                    source_ref="original_request",
                    confidence=0.95,
                    status="PROPOSED",
                    evidence=text,
                )
            )

        if "traveling" in lower or "travel" in lower:
            observations.append(
                CandidateObservation(
                    semantic_type="context",
                    value="subject traveling",
                    asserted_by="subject",
                    source_ref="original_request",
                    confidence=0.91,
                    status="PROPOSED",
                    evidence=text,
                )
            )

        return [asdict(observation) for observation in observations]
