#!/usr/bin/env python3
"""Recipe of the Week — one well-loved family recipe a week, rotating through cuisines.

    python recipes/recipe-of-the-week/run.py --output-dir ~/ai-output [--cuisine Thai]

Publishes recipe.md, an AI-generated cover, and a self-contained Cook's Card
(cooks-card.html). The bundled recipe-validator scanner gates food safety.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402
from core import food  # noqa: E402

CUISINES = ["Midwest", "New Orleans", "Italian", "Thai", "Mexican", "Southern US", "Chinese"]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--cuisine", help="Override the cuisine rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    cuisine = ctx.args.cuisine or least_used(CUISINES, ctx.existing, "cuisine")
    return {"CUISINE": cuisine, "RECIPE_TEMPLATE": food.TEMPLATE.strip()}


RECIPE = Recipe(
    name="recipe-of-the-week",
    collection="recipes",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("recipe.md",),
    skills=("recipe-validator", "llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("cuisine",),
    cover_aspect="3:2",
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=food.check_recipe,
    after_cover=food.cooks_card,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
