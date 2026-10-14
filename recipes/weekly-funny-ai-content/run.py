#!/usr/bin/env python3
"""Weekly Funny AI Content — one satirical AI-use-case content concept a week, with a cover.

    python recipes/weekly-funny-ai-content/run.py --output-dir ~/ai-output [--family "Petty productivity"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

FAMILIES: dict[str, str] = {
    "Emotionally delicate situations": "AI agents handling breakups, apologies, roommate disputes, passive-aggressive office politics, family group chats.",
    "Over-automated domestic life": "chores, dating profiles, baby naming, HOA complaints, wedding planning, birthday texts.",
    "Weird business workflows": "AI performance reviews for pets, automated humblebrags, thought leadership about doing nothing.",
    "Petty productivity": "inbox revenge, meeting-excuse generation, calendar diplomacy, automated small talk with neighbours.",
    "Socially cursed agents": "an agent that optimises your texts until nobody likes you, a bot that ranks friends by cancellation risk, a vibe compliance officer.",
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--family", choices=sorted(FAMILIES), help="Override the premise-family rotation.")


def prepare(ctx: RunContext) -> dict[str, str]:
    family = ctx.args.family or least_used(list(FAMILIES), ctx.existing, "family")
    return {"FAMILY": family, "FAMILY_GUIDE": FAMILIES[family]}


RECIPE = Recipe(
    name="weekly-funny-ai-content",
    collection="funny-ai-content",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("concept.md",),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    fields=("family", "format"),
    cover_aspect="16:9",
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
