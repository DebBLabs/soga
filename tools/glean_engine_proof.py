from pprint import pprint

from engines.glean_engine import GleanEngine

engine = GleanEngine()

mwr = engine.glean(
    candidate_observations=[
        {
            "semantic_type": "delegate",
            "value": "niece",
            "status": "PROPOSED",
        }
    ],
    subject_representation={
        "subject_id": "subject-001",
        "confirmed": [],
    },
    mission_context={
        "request": "My niece should manage my medical appointments while I am traveling."
    },
    sector_knowledge=["healthcare", "calendar", "travel"],
)

print("Glean Engine Proof")
print("==================")
print()

pprint(mwr)
