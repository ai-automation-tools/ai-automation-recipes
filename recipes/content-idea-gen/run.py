#!/usr/bin/env python3
"""Content Idea — one trend-grounded, automatable social-media series idea a run, with a cover.

    python recipes/content-idea-gen/run.py --output-dir ~/ai-output [--topic "Gaming"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

TOPICS = [
    "AI and automation",
    "Productivity",
    "Finance and side hustles",
    "Fitness and health",
    "Gaming",
    "Pop culture and entertainment",
    "Cybersecurity",
    "Education",
    "Entrepreneurship",
    "Travel",
    "Food and cooking",
    "DIY and maker culture",
    "Internet culture and memes",
    "Oddly satisfying visuals",
]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--topic", help="Override the topic rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    return {"TOPIC": ctx.args.topic or least_used(TOPICS, ctx.existing, "topic")}


RECIPE = Recipe(
    name="content-idea-gen",
    collection="content-ideas",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("idea.md",),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("topic", "platforms"),
    cover_aspect="16:9",
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
