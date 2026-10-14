#!/usr/bin/env python3
"""Comic — one four-panel strip a week: a script and the rendered full-page strip.

    python recipes/comics/run.py --output-dir ~/ai-output [--topic "smart fridges with opinions"]
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

TOPICS = [
    "AI agents stuck in a dysfunctional virtual office",
    "Dating in the age of AI companions",
    "A burnt-out millennial and their sarcastic AI roommate",
    "Robots trying (and failing) to learn human etiquette",
    "Influencer life behind the scenes",
    "Helpdesk tech support in the near future",
    "Self-driving car adventures and mishaps",
    "Gen Z kids vs boomer parents on a video call",
    "Side hustle culture gone wrong",
    "Superheroes whose powers are just apps and algorithms",
    "Cooking disasters with smart kitchen gadgets",
    "Remote workers who never leave their apartments",
    "Therapy-speak taken to ridiculous extremes",
    "The last video-rental store employee",
    "Algorithm addiction support group",
    "Pet influencers running their human's life",
    "Gig economy workers getting revenge",
    "90s kids now failing at adulting",
    "VR addicts who forgot real life",
    "A conspiracy theorist who's occasionally right",
    "Superhero fatigue support group",
    "Smart home devices that developed personalities",
    "Dating app horror stories brought to life",
    "Main character syndrome in everyday situations",
    "True-crime podcast fans solving minor household mysteries",
    "Meal-prep influencers vs chaotic reality",
    "The quiet-quitting office saga",
    "Three rival chatbots as roommates",
    "Airport travel hell with AI agents",
    "The sentient fridge that judges your life choices",
    "A crypto bro who keeps losing everything",
]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--topic", help="Override the topic rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    return {"TOPIC": ctx.args.topic or least_used(TOPICS, ctx.existing, "topic")}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    panels = re.findall(r"(?m)^## Panel (\d)\s*$", (staging / "script.md").read_text(encoding="utf-8"))
    if panels != ["1", "2", "3", "4"]:
        raise RecipeError(f"script.md needs exactly ## Panel 1–4 in order, found {panels}")


RECIPE = Recipe(
    name="comics",
    collection="comics",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("script.md",),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    fields=("series", "topic"),
    cover_aspect=None,
    images=ImageSpec(min=1, max=1, aspects=("16:9", "1:1", "3:4"), folder="", text_ok=True),
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
