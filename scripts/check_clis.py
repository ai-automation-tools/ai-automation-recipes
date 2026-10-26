#!/usr/bin/env python3
"""Check every CLI profile against the CLI installed on this machine.

For each profile in core/engines/clis/ (and $RECIPES_CLI_DIR): is the binary on PATH, what
version does it report, and does every flag the profile passes still appear in the CLI's own
--help? A flag missing from the help text is the usual first sign a CLI changed under us.

    python scripts/check_clis.py              # every profile
    python scripts/check_clis.py codex gemini # just these
    python scripts/check_clis.py --json       # machine-readable, for the upstream routine

Exits 1 if any installed CLI is missing a flag. A CLI that isn't installed is reported and
skipped, not failed: nobody has every CLI.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.engines import load_profiles  # noqa: E402

log = logging.getLogger("check_clis")
VERSION = re.compile(r"\d+\.\d+\.\d+")


def flags(profile: dict) -> list[str]:
    """Every option the profile passes: argv plus the spliced model and tool args (`--x=v` is `--x`)."""
    tokens = [*profile.get("argv", []), *profile.get("modelArgs", []), *profile.get("toolArgs", [])]
    return sorted({t.split("=", 1)[0] for t in tokens if t.startswith("-") and len(t) > 1 and t != "-"})


def run(binary: str, args: list[str]) -> str:
    try:
        proc = subprocess.run([binary, *args], capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"<{exc}>"
    return (proc.stdout or "") + (proc.stderr or "")


def check(profile: dict) -> dict:
    binary = shutil.which(profile["binary"])
    report: dict = {"name": profile["name"], "installed": bool(binary),
                    "verified": profile.get("verified", {}), "flags": flags(profile)}
    if not binary:
        return report
    spec = profile.get("check", {})
    # The first line that looks like a version: wrappers can print banners before it.
    lines = run(binary, spec.get("version", ["--version"])).strip().splitlines()
    report["version"] = next((l.strip() for l in lines if VERSION.search(l)), lines[0] if lines else "")
    help_text = "\n".join(run(binary, args) for args in spec.get("help", [["--help"]]))
    report["missing"] = [f for f in report["flags"] if f not in help_text]
    return report


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    profiles = load_profiles()
    names = args or sorted(profiles)
    unknown = [n for n in names if n not in profiles]
    if unknown:
        log.error("no profile for: %s (have %s)", ", ".join(unknown), ", ".join(sorted(profiles)))
        return 2
    reports = [check(profiles[n]) for n in names]
    if "--json" in sys.argv:
        print(json.dumps(reports, indent=2))
    else:
        for r in reports:
            if not r["installed"]:
                log.info("%-10s not installed - skipped", r["name"])
                continue
            pinned = r["verified"].get("version", "?")
            drift = "" if pinned in r["version"] else f"  (profile verified against {pinned})"
            status = "ok" if not r["missing"] else "MISSING " + " ".join(r["missing"])
            log.info("%-10s %s - %s%s", r["name"], r["version"], status, drift)
    return 1 if any(r.get("missing") for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
