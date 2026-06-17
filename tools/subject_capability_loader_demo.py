from pprint import pprint

from engines.subject_capability_loader import (
    SubjectCapabilityLoader,
)

capabilities = (
    SubjectCapabilityLoader()
    .load("subject-001")
)

print()
print("SUBJECT CAPABILITY LOADER DEMO")
print("==============================")
print()

pprint(capabilities)
