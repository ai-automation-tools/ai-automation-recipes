#!/usr/bin/env python3
"""Agent Persona (Known Figure) — one debate-ready card a run for a real person or an established
fictional character, researched from their public record or their canon.

    python recipes/agent-persona/run.py --output-dir ~/ai-output [--figure gordon-ramsay]

The card is a portable second-person prompt any model can adopt. With an image key set, the run
renders a 2:3 illustrated cover and a square chat avatar beside it; without one the card publishes
on its own. Shares the `agent-personas` collection with agent-persona-original, so a figure that
already has a card is rejected rather than written twice.
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

SUBCATEGORIES: dict[str, str] = {
    "Comedy": "stand-ups and satirists with a distinct take.",
    "Political": "political figures across the spectrum — provocative, sharply voiced ones.",
    "Celebrity": "actors, hosts and media personalities.",
    "Fictional": "characters from a real, existing film, show, game, cartoon, comic or book, with a strong opinionated voice.",
    "Sports": "athletes and coaches known for big personalities.",
    "Music": "musicians and rappers.",
    "Tech": "tech moguls and founders.",
    "Host": "podcast and talk-show hosts.",
    "Internet": "reality-TV and internet personalities.",
    "Historical": "iconic historical figures.",
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--subcategory", choices=sorted(SUBCATEGORIES), help="Override the subcategory rotation.")
    p.add_argument("--figure", help="A kebab-case figure to build, e.g. gordon-ramsay or rick-sanchez.")


def prepare(ctx: RunContext) -> dict[str, str]:
    sub = ctx.args.subcategory or least_used(list(SUBCATEGORIES), ctx.existing, "subcategory")
    if ctx.args.figure:
        figure = (
            f"**Requested figure: `{ctx.args.figure}`** — build this figure and use it as the slug. Set "
            "`subcategory` to whichever label fits them best; the rotation pick above is only a default."
        )
    else:
        figure = "No figure was requested: pick one in this subcategory that the cast doesn't have yet."
    return {"SUBCATEGORY": sub, "SUBCATEGORY_GUIDE": SUBCATEGORIES[sub], "FIGURE": figure}


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    card = (staging / "persona.md").read_text(encoding="utf-8")
    if not card.startswith("---\n") and not card.startswith("---\r\n"):
        raise RecipeError("persona.md must start with its frontmatter (---) at byte 0")
    front = card.split("---", 2)[1]
    if re.search(r"^tags:\s*\[", front, re.M):
        raise RecipeError("persona.md tags must be a YAML block list, not [a, b]")
    if re.search(r"^\s*#", front, re.M):
        raise RecipeError("persona.md frontmatter contains a # comment")
    if not re.search(r"^real_or_fictional:\s*(real|fictional)\s*$", front, re.M):
        raise RecipeError("persona.md frontmatter needs real_or_fictional: real | fictional")
    if manifest.get("real_or_fictional") not in ("real", "fictional"):
        raise RecipeError("final JSON real_or_fictional must be 'real' or 'fictional'")
    purpose = re.search(r"^## Purpose\s*\n+(.+?)\s*$", card, re.M)
    if not purpose or len(purpose.group(1)) > 240:
        raise RecipeError("## Purpose must be one sentence under 240 characters")
    if not re.search(r"^## Persona\s*\n+You are ", card, re.M):
        raise RecipeError("## Persona must open in the second person ('You are …')")
    if manifest.get("slug") in {e.slug for e in ctx.existing}:
        raise RecipeError(f"{manifest.get('slug')!r} already has a card in this collection")


RECIPE = Recipe(
    name="agent-persona",
    collection="agent-personas",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("persona.md",),
    skills=("character-sim", "llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("subcategory", "real_or_fictional"),
    cover_aspect="2:3",
    images=ImageSpec(min=1, max=1, aspects=("1:1",), folder="", optional=True),
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
