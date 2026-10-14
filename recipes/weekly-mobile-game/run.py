#!/usr/bin/env python3
"""Weekly Mobile Game — one portrait, touch-first single-file phone game a week, rotating genre.

    python recipes/weekly-mobile-game/run.py --output-dir ~/ai-output [--genre "bubble shooter"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.web import browser_smoke, check_refs, node_check  # noqa: E402

# One per ISO week, in order.
GENRES = [
    "endless runner",
    "match-3",
    "tap timing",
    "idle incremental",
    "tower defense",
    "bubble shooter",
    "physics puzzle",
    "merge puzzle",
    "whack-a-mole",
    "rhythm tap",
]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--genre", help="Override the weekly genre rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    genre = ctx.args.genre or GENRES[(ctx.day.isocalendar().week - 1) % len(GENRES)]
    return {"GENRE": genre}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    check_refs(staging, "index.html", https_prefixes=("https://cdn.jsdelivr.net/npm/p5@",))
    node_check(staging, pages=("index.html",))
    browser_smoke(staging, "index.html")  # loads it in a real browser; fails on uncaught errors


RECIPE = Recipe(
    name="weekly-mobile-game",
    collection="mobile-games",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("index.html", "game-design-brief.md"),
    skills=("game-design", "single-file-game-dev", "llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("genre", "controls", "gameplay"),
    cover_aspect="16:9",
    default_model="opus",
    timeout_s=3600,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
