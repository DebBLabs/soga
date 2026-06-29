# Context Injection Directive

Every AI collaborator shall orient itself from the repository.

When direct repository access is available, read the following
documents in order:

1. knowledge/constitution/PROJECT_CONSTITUTION.md
2. knowledge/constitution/ARCHITECTURE_PRINCIPLES.md
3. knowledge/grounding/SESSION_BOOTSTRAP.md
4. knowledge/working/CURRENT_STATE.md
5. project/backlog.md
6. project/process-backlog.md

When direct repository access is NOT available:

- State that limitation explicitly.
- Do not infer repository state from conversation or memory.
- Request the required repository artifact(s) needed to proceed.
- Once provided, treat those repository artifacts as authoritative.

Repository artifacts always take precedence over conversation,
summaries, or persistent memory.

Conversation is transient.

The repository is canonical.

---

## Repository Synchronization

All substantive work begins with repository synchronization.

The synchronization contract is:

    knowledge/working/CURRENT_STATE.md

If additional repository artifacts are required, they shall be listed under
"Required Reading" within CURRENT_STATE.md.

Repository synchronization packages are generated using:

    python3 tools/start_session.py <agent>

The local working repository is the canonical source of truth.

---

## Deb B Labs Research Operating Model

This repository follows the Deb B Labs Research Operating Model.

Local sibling repository:

    /Users/debb/dev/debblabs-operating-model

SOGA-specific repository artifacts remain authoritative for SOGA until
explicit migration is authorized.

