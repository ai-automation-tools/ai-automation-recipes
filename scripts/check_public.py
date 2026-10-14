#!/usr/bin/env python3
"""Fail if anything in the repo looks private before it is pushed.

Two layers:

* Built-in patterns — API-key shapes, private keys, personal home paths,
  email addresses, raw IPv4 addresses.
* A personal denylist kept OUTSIDE the repo (names, domains, hostnames, server
  IPs you never want published), one regex per line, `#` for comments:
      $RECIPES_DENYLIST, or ~/.config/ai-automation-recipes/denylist.txt
  It lives outside the repo because the list itself is the private data.

Scans every tracked file (`git ls-files`), or every file under the repo when
it is not a git repo yet.

    python scripts/check_public.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".pdf"}

BUILTIN = {
    "anthropic key": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "openai key": r"sk-(?:proj-)?[A-Za-z0-9]{32,}",
    "google api key": r"AIza[0-9A-Za-z_-]{35}",
    "github token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "windows home path": r"[A-Za-z]:[\\/]+Users[\\/]+(?!<|\{|Public|you|USER)[A-Za-z0-9._-]+",
    "unix home path": r"/(?:home|Users)/(?!<|\{|you\b|user\b|runner\b|ubuntu\b)[a-z][a-z0-9._-]+/",
    "email": r"[A-Za-z0-9._%+-]+@(?!example\.|users\.noreply\.github\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "ipv4": r"\b(?!127\.0\.0\.1\b|0\.0\.0\.0\b)(?:\d{1,3}\.){3}\d{1,3}\b",
}
# Lines that legitimately match a built-in pattern.
ALLOW = [
    re.compile(r"noreply@anthropic\.com"),
    re.compile(r"\bp5@\d"),  # jsdelivr version pins look like emails
]


def denylist() -> dict[str, str]:
    path = Path(os.environ.get("RECIPES_DENYLIST", Path.home() / ".config" / "ai-automation-recipes" / "denylist.txt"))
    if not path.is_file():
        print(f"note: no personal denylist at {path} — built-in patterns only", file=sys.stderr)
        return {}
    rules = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            rules[f"denylist: {line}"] = line
    return rules


def files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        return [ROOT / f for f in out.splitlines()]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob("*") if p.is_file() and not SKIP_DIRS & set(p.parts)]


def main() -> int:
    rules = {name: re.compile(rx, re.I) for name, rx in {**BUILTIN, **denylist()}.items()}
    hits = 0
    for path in files():
        if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file() or path.name == ".env":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if any(a.search(line) for a in ALLOW):
                continue
            for name, rx in rules.items():
                m = rx.search(line)
                if m:
                    hits += 1
                    print(f"{path.relative_to(ROOT).as_posix()}:{n}: [{name}] {m.group(0)}")
    if hits:
        print(f"\n{hits} finding(s). Fix them, or narrow the rule, before publishing.", file=sys.stderr)
        return 1
    print("check_public: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
