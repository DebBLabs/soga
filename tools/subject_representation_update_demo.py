from pprint import pprint

from engines.subject_representation_updater import (
    SubjectRepresentationUpdater,
)

engine = SubjectRepresentationUpdater()

proposal = engine.propose(
    {
        "question":
            "Preferred pharmacy",
        "answer":
            "CVS",
    }
)

print()
print("SUBJECT REPRESENTATION UPDATE DEMO")
print("==================================")
print()

pprint(proposal)
