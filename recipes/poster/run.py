#!/usr/bin/env python3
"""Poster — one 2:3 poster on a rotating theme, twice a week.

    python recipes/poster/run.py --output-dir ~/ai-output [--theme "Retro NASA Space Travel"]

Themes live in themes.md beside this file; edit it to change the rotation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RecipeError, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402


def themes() -> list[str]:
    found = re.findall(r"(?m)^- (.+?)\s*$", (HERE / "themes.md").read_text(encoding="utf-8"))
    if not found:
        raise RecipeError("themes.md has no `- theme` lines")
    return found


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--theme", help="Override the theme rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    return {"THEME": ctx.args.theme or least_used(themes(), ctx.existing, "theme")}


RECIPE = Recipe(
    name="poster",
    collection="posters",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("poster.md",),
    skills=("llm-writing", "image-prompt-craft"),
    fields=("theme", "style"),
    cover_aspect=None,
    images=ImageSpec(min=1, max=1, aspects=("2:3",), folder="", text_ok=True),
    default_model="sonnet",
    timeout_s=900,
    add_args=add_args,
    prepare=prepare,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
