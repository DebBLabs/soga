# Start Session Process

## Purpose

`start_session.py` creates a SHA-pinned initialization checkpoint for both chat-only and repo-aware agent surfaces without making conversation history authoritative.

The Git repository remains canonical. `.agent/SESSION_INIT.md` is a generated, non-canonical view for chat surfaces only. It must never be edited by hand.

## One-time setup

1. Put `.agent/reading.json` under version control.
2. Add this line to `.gitignore`:

   `.agent/SESSION_INIT.md`

3. Replace the old `start_session.py` with the new version.

## Normal start

From anywhere inside the repository:

```bash
python tools/start_session.py
```

The script will:

1. locate the Git repository root;
2. refuse to run if the working tree is dirty;
3. capture branch and exact HEAD SHA;
4. load the structured gate/reading list from `.agent/reading.json`;
5. fail if the reading list is empty or any required file is missing;
6. regenerate `.agent/SESSION_INIT.md`;
7. place a random Session Proof inside the file only;
8. print small initialization instructions for chat and CLI surfaces.

## Chat surfaces

For ChatGPT, Gemini chat, or Claude chat:

1. Run `start_session.py`.
2. Replace the Project/chat copy of `.agent/SESSION_INIT.md`.
3. Start a fresh chat immediately.
4. Paste the small initialization message printed by the script.
5. Confirm the agent echoes the Session Proof from the file.

If it cannot echo the Session Proof, treat the session as not initialized.

Replacing the file and starting a fresh chat are a single workflow action. Existing open chats are stale after a replacement.

## Repo-aware CLI surfaces

For Codex, Claude Code, Gemini CLI, or another verified repo-aware CLI:

- Do not upload `SESSION_INIT.md` as a source of truth.
- Have the CLI read the canonical files listed by the script directly from the repository.
- Require the agent to report branch, SHA, gate/task, and files reviewed.

## Mid-sprint

After any committed working point that needs review:

```bash
python tools/start_session.py
```

The new HEAD becomes the review checkpoint. Review conclusions from different SHAs are not directly comparable.

## Fallback

To preserve the old pasteable behavior:

```bash
python tools/start_session.py --stdout
```

This prints the complete package instead of writing `.agent/SESSION_INIT.md`.

## Scope boundary

The script does not:

- auto-commit;
- upload to ChatGPT, Claude, or Gemini;
- create a Drive bridge;
- maintain a second canonical state;
- synchronize model memory.

Git synchronizes artifacts. `start_session.py` synchronizes the reference checkpoint.
