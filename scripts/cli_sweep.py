#!/usr/bin/env python3
"""Run recipes on one agent CLI for real and record the result in the roadmap matrix.

    python scripts/cli_sweep.py --engine codex short-story comics
    python scripts/cli_sweep.py --engine gemini --limit 3      # first three ⬜ cells of its column
    python scripts/cli_sweep.py --engine kimi --no-write short-story   # report only

A recipe passes when `recipes/<name>/run.py --engine <cli>` exits 0, which means it published an
artifact that passed the recipe's own output checks. The cell becomes ✅; otherwise ❌ and the
last error line is printed so it can go into the item that explains the failure. Open the artifact
yourself before trusting a ✅ for a new recipe: the exit code proves the contract, not the taste.

Runs use the profile in this checkout (RECIPES_CLI_REMOTE=0), deliver nowhere (no webhook) and
write under --output-dir, which defaults to a temp folder. `pr-review` and `app-enhancement` need
arguments that touch a repo or an app, so run those by hand (see their READMEs).
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROADMAP = ROOT / "docs" / "ROADMAP.md"
COLUMNS = {"claude": "Claude", "codex": "Codex", "opencode": "OpenCode", "kimi": "Kimi",
           "grok": "Grok", "gemini": "Gemini", "agy": "agy"}
BY_HAND = {"pr-review", "app-enhancement"}
PASS, FAIL, TODO = "✅", "❌", "⬜"
ROW = re.compile(r"^\| \[(?P<name>[^\]]+)\]\([^)]*\) \|")

log = logging.getLogger("cli_sweep")


def _cells(line: str) -> list[str]:
    return line.strip().strip("|").split("|")


def column_index(text: str, engine: str) -> int:
    """Position of the engine's column among the matrix row cells (recipe link is 0)."""
    header = next(l for l in text.splitlines() if l.startswith("| Recipe |"))
    names = [c.strip() for c in _cells(header)]
    return names.index(COLUMNS[engine])


def matrix_cells(text: str, engine: str) -> dict[str, str]:
    """recipe -> current cell for the engine's column."""
    i = column_index(text, engine)
    out = {}
    for line in text.splitlines():
        m = ROW.match(line)
        if m:
            out[m["name"]] = _cells(line)[i].strip()
    return out


def rewrite_matrix(text: str, engine: str, results: dict[str, bool]) -> str:
    """Set the engine's cell for each recipe in `results` (True ✅, False ❌); touch nothing else."""
    i = column_index(text, engine)
    lines = text.split("\n")
    seen = set()
    for n, line in enumerate(lines):
        m = ROW.match(line)
        if m and m["name"] in results:
            cells = _cells(line)
            cells[i] = PASS if results[m["name"]] else FAIL
            lines[n] = "| " + " | ".join(c.strip() for c in cells) + " |"
            seen.add(m["name"])
    missing = set(results) - seen
    if missing:
        raise KeyError(f"not in the matrix: {', '.join(sorted(missing))}")
    return "\n".join(lines)


def error_line(output: str) -> str:
    """The most useful single line from a failed run: the last one that names an error."""
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    hits = [l for l in lines if re.search(r"error|fail|missing|not found|timed out", l, re.I)]
    return (hits or lines or ["no output"])[-1][:300]


def run_recipe(name: str, engine: str, out_dir: Path, extra: list[str]) -> tuple[bool, float, str]:
    env = {**os.environ, "RECIPES_CLI_REMOTE": "0", "RECIPES_WEBHOOK_URL": "", "PYTHONIOENCODING": "utf-8"}
    cmd = [sys.executable, str(ROOT / "recipes" / name / "run.py"), "--engine", engine,
           "--output-dir", str(out_dir), *extra]
    start = time.monotonic()
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    minutes = (time.monotonic() - start) / 60
    return proc.returncode == 0, minutes, "" if proc.returncode == 0 else error_line(proc.stdout + "\n" + proc.stderr)


def main(argv: list[str] | None = None) -> int:
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # ✅/❌ on a cp1252 console
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--engine", required=True, choices=sorted(COLUMNS))
    p.add_argument("recipes", nargs="*", help="Recipes to run; default is the engine's ⬜ cells in matrix order.")
    p.add_argument("--limit", type=int, default=6, help="Most recipes to run when none are named (default 6).")
    p.add_argument("--output-dir", default=str(Path(tempfile.gettempdir()) / "cli-sweep-out"))
    p.add_argument("--no-write", action="store_true", help="Run and report, but leave the matrix alone.")
    args, extra = p.parse_known_args(argv)

    text = ROADMAP.read_text(encoding="utf-8")
    cells = matrix_cells(text, args.engine)
    names = args.recipes or [n for n, c in cells.items() if c == TODO and n not in BY_HAND][: args.limit]
    bad = [n for n in names if n not in cells or n in BY_HAND]
    if bad:
        log.error("not sweepable here (unknown, or run by hand): %s", ", ".join(bad))
        return 2

    results: dict[str, bool] = {}
    for name in names:
        ok, minutes, err = run_recipe(name, args.engine, Path(args.output_dir), extra)
        results[name] = ok
        log.info("%s %-28s %.1f min%s", PASS if ok else FAIL, name, minutes, "" if ok else f"  {err}")
    if results and not args.no_write:
        ROADMAP.write_text(rewrite_matrix(text, args.engine, results), encoding="utf-8", newline="")
        log.info("matrix updated: %s column, %d cells", COLUMNS[args.engine], len(results))
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
