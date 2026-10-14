#!/usr/bin/env python3
"""App Idea Card — one researched app pitch a day, plus a concept-art cover.

    python recipes/app-idea-card/run.py --output-dir ~/ai-output [--category "Security Tool"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

CATEGORIES: dict[str, str] = {
    "Browser Extension": (
        "A Chrome/Firefox/Edge/Safari extension (Manifest V3 where it applies). Browser-resident and "
        "page-aware, no separate server unless it truly needs one."
    ),
    "GitHub Repo": (
        "A small standalone open-source project: a CLI, library, developer tool, scraper or Docker "
        "image. Buildable in a weekend, explainable in a five-minute README, with a clear license intent."
    ),
    "Web/Mobile App": (
        "A single-page web app or mobile-style PWA for end users, not developers. Auth allowed but minimal."
    ),
    "AI Tool": (
        "An LLM, vision model, embedding model or agent is the headline feature, not a sprinkle: "
        "RAG apps, multi-agent automations, voice tools, AI-driven CLIs."
    ),
    "Security Tool": (
        "Application, cloud or supply-chain security, identity, privacy, threat detection or personal "
        "OPSEC. Defensive only — no offensive tooling."
    ),
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--category", choices=sorted(CATEGORIES), help="Override the category rotation.")


def prepare(ctx: RunContext) -> dict[str, str]:
    category = ctx.args.category or least_used(list(CATEGORIES), ctx.existing, "category")
    return {"CATEGORY": category, "CATEGORY_GUIDE": CATEGORIES[category]}


RECIPE = Recipe(
    name="app-idea-card",
    collection="idea-cards",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("card.md",),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("category", "form_factor", "monetization"),
    cover_aspect="16:9",
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
