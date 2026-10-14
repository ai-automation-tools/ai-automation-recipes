#!/usr/bin/env python3
"""Weekly Image Prompt Pack — 5–8 reusable image prompts on one theme, each with a rendered example.

    python recipes/image-prompt-packs/run.py --output-dir ~/ai-output [--theme "Steampunk Contraptions"]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RecipeError, RunContext, run  # noqa: E402
from core.images import process  # noqa: E402

# One suggestion per ISO week; the agent may pick a fresher theme.
THEMES = [
    "Cyberpunk Dystopia", "Retro-Futuristic Technology", "Ethereal Fantasy Landscapes",
    "Office Humor & Corporate Satire", "Vintage Travel Posters", "Gothic Horror Aesthetics",
    "Minimalist Nature", "Cybersecurity Threat Visualizations", "Interstellar Exploration",
    "Steampunk Contraptions",
]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--theme", help="Override the suggested theme (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    return {"THEME": ctx.args.theme or THEMES[ctx.day.isocalendar().week % len(THEMES)]}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    md = (staging / "pack.md").read_text(encoding="utf-8")
    for item in manifest.get("images") or []:
        if isinstance(item, dict) and f"images/{item.get('file')}" not in md:
            raise RecipeError(f"pack.md doesn't link images/{item.get('file')}")
    if len(re.findall(r"(?m)^## ", md)) != len(manifest.get("images") or []):
        raise RecipeError("pack.md needs one `## ` section per image")


def cover_from_first(ctx: RunContext, staging: Path, manifest: dict[str, object]) -> list[str]:
    """The pack's first example doubles as its cover."""
    first = (manifest.get("images") or [{}])[0].get("file")
    src = staging / "images" / str(first)
    if not src.is_file():
        return []
    return [process.use_as_cover(staging, f"images/{first}")]


RECIPE = Recipe(
    name="image-prompt-packs",
    collection="image-prompt-packs",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("pack.md",),
    skills=("image-prompt-craft", "llm-writing", "humanizer"),
    fields=("theme",),
    cover_aspect=None,
    images=ImageSpec(min=5, max=8, aspects=("1:1", "16:9", "9:16", "3:2", "2:3", "4:3", "3:4")),
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
    after_cover=cover_from_first,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
