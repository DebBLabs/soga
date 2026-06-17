import json
from pathlib import Path


class SubjectCapabilityLoader:
    """
    Loads standing capabilities for a Subject.

    These are not preferences or intent.
    They represent available capability/evidence
    inventory that may satisfy mission steps.
    """

    def load(
        self,
        subject_id,
    ):

        path = Path(
            "data/subjects"
        ) / subject_id / "capabilities.json"

        with path.open(
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)

        return data.get(
            "standing_capabilities",
            [],
        )
