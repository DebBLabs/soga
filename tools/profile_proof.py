import json
from pathlib import Path
from pprint import pprint

profile = Path("data/subjects/subject-001/profile.json")

print("Subject Representation Proof")
print("============================")
print()

data = json.loads(profile.read_text())

print("Subject ID:")
print(data["subject_id"])
print()

print("Current representation:")
pprint(data)
