#!/usr/bin/env python3
"""Regional Recipe — one authentic dish a week, adding to a different region each run.

    python recipes/regional-recipe/run.py --output-dir ~/ai-output [--region korean]

The region with the fewest recipes goes next (ties: least recently used), so
every region fills out at the same rate. Same outputs and safety gate as
family-recipe.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import existing_digest, least_used, slugify  # noqa: E402
from core import food  # noqa: E402

REGIONS = [
    "Midwest US", "New Orleans", "Italian", "Thai", "Mexican", "French", "Greek", "Japanese",
    "Mediterranean", "American", "Southeast Asian", "South Asian", "East Asian", "North African",
    "West African", "South American", "Canadian", "Australian", "Spanish", "Korean", "Vietnamese",
    "German", "Caribbean", "Peruvian", "Moroccan", "Filipino", "Ethiopian", "Brazilian",
]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--region", help="Override the region rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    region = ctx.args.region or least_used(REGIONS, ctx.existing, "region")
    in_region = [e for e in ctx.existing if str(e.fields.get("region", "")).lower() == region.lower()]
    return {
        "REGION": region,
        "REGION_SLUG": slugify(region),
        "REGION_EXISTING": existing_digest(in_region),
        "RECIPE_TEMPLATE": food.TEMPLATE.strip(),
    }


RECIPE = Recipe(
    name="regional-recipe",
    collection="regional-recipes",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("recipe.md",),
    skills=("recipe-validator", "llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("region",),
    cover_aspect="3:2",
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=food.check_recipe,
    after_cover=food.cooks_card,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
