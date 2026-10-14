#!/usr/bin/env python3
"""Viral Recipe — the dish that is blowing up on social media right now, recreated so it cooks.

    python recipes/viral-recipe/run.py --output-dir ~/ai-output [--platform TikTok]

Same artifacts as family-recipe (recipe.md, cover, Cook's Card, the recipe-validator gate), plus
two things that make it this beat: the originating post is credited in the frontmatter (`source`,
`source_platform`) and the recipe explains why it went viral.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402
from core import food  # noqa: E402

PLATFORMS = ("TikTok", "Instagram", "YouTube", "Reddit", "Facebook")
URL_RE = re.compile(r"^source:\s*[\"']?(https?://\S+?)[\"']?\s*$", re.M)
PLATFORM_RE = re.compile(r"^source_platform:\s*[\"']?([A-Za-z ]+?)[\"']?\s*$", re.M)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--platform", choices=PLATFORMS, help="Only look for a trend on this platform.")


def prepare(ctx: RunContext) -> dict[str, str]:
    where = (
        f"**Platform for this run: {ctx.args.platform}.** Find the trend there; other platforms may only corroborate."
        if ctx.args.platform
        else "Any platform. Scan all of them and take the trend with the most momentum right now."
    )
    return {"PLATFORM_RULE": where, "RECIPE_TEMPLATE": food.TEMPLATE.strip()}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    text = (staging / "recipe.md").read_text(encoding="utf-8")
    front = text.split("---", 2)[1] if text.startswith("---") else ""
    if not URL_RE.search(front):
        raise RecipeError("recipe.md frontmatter needs `source:` with the originating post's https URL")
    m = PLATFORM_RE.search(front)
    if not m or m.group(1).strip() not in PLATFORMS:
        raise RecipeError(f"recipe.md frontmatter needs `source_platform:` as one of {', '.join(PLATFORMS)}")
    if not re.search(r"^## Why This Went Viral\s*$", text, re.M):
        raise RecipeError("recipe.md needs a `## Why This Went Viral` section")
    if manifest.get("source_platform") != m.group(1).strip():
        raise RecipeError("final JSON source_platform must match the frontmatter")
    food.check_recipe(staging, manifest)


RECIPE = Recipe(
    name="viral-recipe",
    collection="viral-recipes",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("recipe.md",),
    skills=("recipe-validator", "llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("source_platform",),
    cover_aspect="3:2",
    default_model="sonnet",
    timeout_s=2400,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
    after_cover=food.cooks_card,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
