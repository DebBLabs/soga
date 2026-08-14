#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import secrets
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc)).strip()
        raise SystemExit(f"Git command failed: git {' '.join(args)}\n{detail}") from exc


def repo_root() -> Path:
    script_path = Path(__file__).resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(script_path.parent), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip()).resolve()
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc)).strip()
        raise SystemExit(f"Unable to locate repository root.\n{detail}") from exc


def load_config(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(
            f"Missing start-session config: {path}\n"
            "Create .agent/reading.json before initializing a session."
        )
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    gate = str(data.get("gate", "")).strip()
    required = data.get("required", [])

    if not gate:
        raise SystemExit(f"{path}: 'gate' must be a non-empty string.")
    if not isinstance(required, list) or not required:
        raise SystemExit(f"{path}: 'required' must be a non-empty list.")

    normalized = []
    for item in required:
        if not isinstance(item, str) or not item.strip():
            raise SystemExit(f"{path}: every required-reading entry must be a path string.")
        normalized.append(item.strip())

    data["gate"] = gate
    data["required"] = normalized
    return data


def require_clean_tree(repo: Path) -> None:
    status = run_git(repo, "status", "--porcelain")
    if status:
        print("STOP — repository is not at a clean committed checkpoint.", file=sys.stderr)
        print(file=sys.stderr)
        print(status, file=sys.stderr)
        print(file=sys.stderr)
        print("Commit or restore these changes, then rerun start_session.py.", file=sys.stderr)
        raise SystemExit(2)


def require_files(repo: Path, paths: list[str]) -> None:
    missing = [p for p in paths if not (repo / p).is_file()]
    if missing:
        message = "\n".join(f"  - {p}" for p in missing)
        raise SystemExit(
            "Required-reading validation failed. Missing files:\n"
            f"{message}\n"
            "No session package was generated."
        )


def read_text(repo: Path, relative_path: str) -> str:
    return (repo / relative_path).read_text().rstrip()


def render_package(
    repo: Path,
    branch: str,
    sha: str,
    gate: str,
    required: list[str],
    proof: str,
) -> str:
    generated = datetime.now().astimezone().isoformat(timespec="seconds")
    parts = [
        "# Deb B Labs Session Initialization Package",
        "",
        "## Checkpoint",
        f"- Review Target: `{branch} @ {sha}`",
        f"- Gate / Task: `{gate}`",
        f"- Generated: `{generated}`",
        f"- Session Proof: `{proof}`",
        "",
        "## Operating Rules",
        "- The Git repository is canonical.",
        "- This file is a generated, non-canonical view of one clean committed checkpoint.",
        "- Never edit this file by hand; regenerate it with `start_session.py`.",
        "- Repository artifacts override conversation history, model memory, and summaries.",
        "- Read every embedded artifact before substantive work.",
        "- Begin the first substantive response by stating the Review Target, Gate / Task, Files Reviewed, and Session Proof.",
        "- If the expected checkpoint in the user's initialization message does not match this file, stop and report the mismatch.",
        "",
        "## Required Reading",
    ]
    parts.extend(f"- `{p}`" for p in required)
    parts.append("")

    for p in required:
        parts.extend([
            f"## BEGIN `{p}`",
            "",
            read_text(repo, p),
            "",
            f"## END `{p}`",
            "",
        ])

    return "\n".join(parts).rstrip() + "\n"


def print_chat_init(branch: str, sha: str, gate: str, package_path: str) -> None:
    print("CHAT INITIALIZATION")
    print("-------------------")
    print(f"Upload/replace: {package_path}")
    print("Then start a fresh chat and send:")
    print()
    print(f"Initialize from `{Path(package_path).name}`.")
    print(f"Expected checkpoint: {branch} @ {sha}")
    print(f"Gate / Task: {gate}")
    print("Read the entire initialization file before responding.")
    print("Echo the Session Proof found inside the file; it is not included in this message.")
    print("If the file is missing, unreadable, or identifies a different checkpoint, stop and tell me.")
    print()


def print_cli_init(branch: str, sha: str, gate: str, required: list[str]) -> None:
    print("REPO-AWARE CLI INITIALIZATION")
    print("-----------------------------")
    print(f"Expected checkpoint: {branch} @ {sha}")
    print(f"Gate / Task: {gate}")
    print("Read these canonical files directly from the repository:")
    for p in required:
        print(f"  - {p}")
    print("Verify HEAD before substantive work and state branch, SHA, gate/task, and files reviewed.")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a clean, SHA-pinned session initialization package."
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the full generated session package to stdout instead of writing it.",
    )
    parser.add_argument(
        "--config",
        default=".agent/reading.json",
        help="Repo-relative structured reading-list config (default: .agent/reading.json).",
    )
    parser.add_argument(
        "--output",
        default=".agent/SESSION_INIT.md",
        help="Repo-relative generated package path (default: .agent/SESSION_INIT.md).",
    )
    args = parser.parse_args()

    repo = repo_root()
    require_clean_tree(repo)

    branch = run_git(repo, "branch", "--show-current") or "(detached HEAD)"
    sha = run_git(repo, "rev-parse", "HEAD")

    config_path = repo / args.config
    config = load_config(config_path)
    gate = config["gate"]
    required = config["required"]

    require_files(repo, required)

    proof = secrets.token_urlsafe(18)
    package = render_package(repo, branch, sha, gate, required, proof)

    if args.stdout:
        print(package, end="")
        return

    output_path = repo / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(package)

    print("==========================================")
    print("Deb B Labs Session Checkpoint")
    print("==========================================")
    print(f"Repository: {repo.name}")
    print(f"Review Target: {branch} @ {sha}")
    print(f"Gate / Task: {gate}")
    print("Repository Status: clean")
    print(f"Required files: {len(required)}/{len(required)} found")
    print(f"Generated: {args.output}")
    print()
    print_chat_init(branch, sha, gate, args.output)
    print_cli_init(branch, sha, gate, required)
    print("IMPORTANT")
    print("---------")
    print("For chat surfaces, replacing SESSION_INIT.md and starting a fresh chat are one action.")
    print("Re-run after every committed working point that must be reviewed.")


if __name__ == "__main__":
    main()
