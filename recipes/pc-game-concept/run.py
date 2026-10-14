#!/usr/bin/env python3
"""PC Game Concept — a researched design brief, one-page pitch and key art, rotating genre.

    python recipes/pc-game-concept/run.py --output-dir ~/ai-output [--genre "colony sim"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.web import check_refs, check_sources_csv, node_check  # noqa: E402

# One per ISO week, in order.
GENRES = [
    "immersive sim",
    "survival crafting",
    "colony sim",
    "tactical RPG",
    "roguelike deckbuilder",
    "automation/factory sim",
    "cozy management sim",
    "detective mystery",
    "grand strategy",
    "extraction shooter",
]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--genre", help="Override the weekly genre rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    genre = ctx.args.genre or GENRES[(ctx.day.isocalendar().week - 1) % len(GENRES)]
    return {"GENRE": genre}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    check_refs(staging, "pitch.html", allow_external_scripts=False, pending=("cover.png",))
    node_check(staging, pages=("pitch.html",))
    check_sources_csv(staging, lo=3, hi=5)


RECIPE = Recipe(
    name="pc-game-concept",
    collection="pc-game-concepts",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("game-design-brief.md", "pitch.html", "sources.csv"),
    skills=("game-design", "llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("genre", "differentiators"),
    cover_aspect="16:9",
    default_model="opus",
    timeout_s=2400,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
