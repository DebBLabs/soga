#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
from datetime import datetime

TARGET = sys.argv[1] if len(sys.argv) > 1 else "general"

ROOT = Path(".")
CURRENT = ROOT / "knowledge/working/CURRENT_STATE.md"


def read(path):
    return path.read_text() if path.exists() else f"[MISSING: {path}]"


def required_reading(current_text):
    lines = current_text.splitlines()
    capture = False
    files = []
    for line in lines:
        if line.strip() == "# Required Reading":
            capture = True
            continue
        if capture and line.startswith("# "):
            break
        if capture:
            item = line.strip()
            if item.startswith("- "):
                files.append(item[2:].strip())
    return files


def git_lines(args):
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.rstrip()
    except Exception as exc:
        return f"[GIT UNAVAILABLE: {exc}]"


def repository_head():
    return git_lines(["log", "--oneline", "-3"])


def repository_status():
    return git_lines(["status", "--short"])


current = read(CURRENT)
files = required_reading(current)

print("==========================================")
print("Deb B Labs Session Initialization Package")
print(f"Target: {TARGET}")
print(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
print("==========================================")
print()
print("Repository HEAD:")
print(repository_head())
print()
print("Repository Status:")
status = repository_status()
print(status if status else "clean")
print()
print("Instructions:")
print("Apply the repository operating model.")
print("Treat the included repository artifacts as authoritative.")
print("Do not infer current state from memory or conversation.")
print()
print("===== BEGIN knowledge/working/CURRENT_STATE.md =====")
print(current.rstrip())
print("===== END knowledge/working/CURRENT_STATE.md =====")
print()

for f in files:
    path = ROOT / f
    print(f"===== BEGIN {f} =====")
    print(read(path).rstrip())
    print(f"===== END {f} =====")
    print()

print("Synchronization package complete.")
