#!/usr/bin/env python3
"""Weekly Browser Game — one playable single-file HTML game a week, in a rotating genre.

    python recipes/weekly-browser-game/run.py --output-dir ~/ai-output [--genre "Tower defense"]
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

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

    for src in re.findall(r"""<(?:script|link|img|audio|source)[^>]+(?:src|href)\s*=\s*["']([^"']+)""", html, re.I):
        if src.startswith("data:"):
            continue
        if not src.startswith(ALLOWED_CDN):
            raise RecipeError(f"index.html references a disallowed resource: {src}")

    node = shutil.which("node")
    if not node:
        log.warning("node not on PATH — skipping the JS syntax check")
        return
    inline = re.findall(r'''<script(?![^>]*\bsrc\s*=)(?![^>]*\btype\s*=\s*["']?(?!(?:text|application)/javascript\b|module\b)[\w/+.-]+)[^>]*>(.*?)</script>''', html, re.S | re.I)
    with tempfile.TemporaryDirectory() as tmp:
        for i, body in enumerate(inline):
            js = Path(tmp) / f"inline-{i}.js"
            js.write_text(body, encoding="utf-8")
            proc = subprocess.run([node, "--check", str(js)], capture_output=True, text=True)
            if proc.returncode != 0:
                raise RecipeError(f"inline script {i} fails `node --check`:\n{proc.stderr[-1500:]}")
    log.info("index.html: %d inline script(s) pass node --check", len(inline))


RECIPE = Recipe(
    name="weekly-browser-game",
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
