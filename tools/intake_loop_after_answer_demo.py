from pprint import pprint

from engines.glean_engine import GleanEngine
from engines.observation_extractor import ObservationExtractor
from engines.validator import Validator
from engines.mwr_updater import MWRUpdater

request = (
    "My niece should manage my medical "
    "appointments while I am traveling."
)

observations = ObservationExtractor().extract(request)

mwr = GleanEngine().glean(
    candidate_observations=observations,
    subject_representation={},
    mission_context={"request": request},
    sector_knowledge=[],
)

validator = Validator()

before = validator.evaluate(mwr)

mwr = MWRUpdater().apply(
    mwr,
    {
        "destination": "mission_working_representation",
        "value": "May schedule appointments but may not authorize treatment.",
    },
)

after = validator.evaluate(mwr)

print()
print("INTAKE LOOP AFTER ANSWER DEMO")
print("=============================")
print()

print("BEFORE ANSWER")
print("-------------")
pprint(before)
print()

print("AFTER ANSWER")
print("------------")
pprint(after)
print()
