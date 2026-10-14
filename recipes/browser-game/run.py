#!/usr/bin/env python3
"""Browser Game — one playable single-file HTML game a week, in a rotating genre.

    python recipes/browser-game/run.py --output-dir ~/ai-output [--genre "Tower defense"]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core.web import browser_smoke, check_refs, node_check  # noqa: E402
from core import Recipe, RecipeError, RunContext, run  # noqa: E402

log = logging.getLogger("recipes")

# One per ISO week, in order. Long enough that a genre comes back about every quarter.
GENRES = [
    "Endless runner",
    "Match-3 puzzle",
    "Top-down arena shooter",
    "Physics stacking",
    "Rhythm / timing",
    "Snake variant",
    "Brick breaker",
    "Tower defense",
    "Word puzzle",
    "Platformer (single screen)",
    "Sokoban-style push puzzle",
    "Asteroids-style space shooter",
    "Memory / pattern recall",
]

ALLOWED_CDN = ("https://cdn.jsdelivr.net/npm/p5@",)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--genre", help="Override the weekly genre rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    genre = ctx.args.genre or GENRES[ctx.day.isocalendar().week % len(GENRES)]
    return {"GENRE": genre}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    html = (staging / "index.html").read_text(encoding="utf-8")
    if "<script" not in html.lower():
        raise RecipeError("index.html has no <script>")
    check_refs(staging, "index.html", https_prefixes=ALLOWED_CDN)
    node_check(staging, pages=("index.html",))
    browser_smoke(staging, "index.html")  # loads it in a real browser; fails on uncaught errors


RECIPE = Recipe(
    name="browser-game",
    collection="browser-games",
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
