
---

## 2026-06-27 — Repository Authoring Standard

### Discovery

During construction of the repository knowledge framework we identified a repeatable failure mode when AI-generated repository files were emitted in fragmented responses or contained nested Markdown code fences.

Although the content was correct, the format introduced transcription errors and unnecessary cognitive load on the human operator.

### Decision

Repository file generation shall use a single complete shell heredoc:

    cat > filename <<'EOF'
    ...
    EOF

The entire document must be emitted as one uninterrupted block.

Repository files should never be split across multiple responses, require manual reconstruction, or contain nested Markdown code fences that interfere with shell heredocs.

### Rationale

This approach:

- minimizes transcription errors
- reduces operator effort
- makes repository construction deterministic
- improves reproducibility across AI collaborators
- provides a consistent authoring convention for Claude, Gemini, and ChatGPT

### Relationship to Repository Governance

This operational practice reinforces the project's governing principle:

> The repository is the authoritative project memory.

If creating repository memory is difficult or error-prone, important knowledge will remain trapped in transient conversation. Standardizing repository authoring reduces that risk and strengthens the governance process itself.

