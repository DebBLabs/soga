from pprint import pprint

from engines.glean_engine import GleanEngine
from engines.observation_extractor import (
    ObservationExtractor,
)
from engines.intake_loop import (
    IntakeLoop,
)

request = (
    "My niece should manage my medical "
    "appointments while I am traveling."
)

extractor = ObservationExtractor()

observations = extractor.extract(
    request
)

glean = GleanEngine()

mwr = glean.glean(
    candidate_observations=observations,
    subject_representation={},
    mission_context={
        "request": request,
    },
    sector_knowledge=[],
)

loop = IntakeLoop()

result = loop.step(
    mwr
)

print()
print("INTAKE LOOP DEMO")
print("================")
print()

print("NEXT QUESTION")
print("-------------")
pprint(result["next_question"])
print()

print("VALIDATION")
print("----------")
pprint(result["validation"])
