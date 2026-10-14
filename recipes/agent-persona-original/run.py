#!/usr/bin/env python3
"""Original Agent Persona — one invented, debate-ready character card a run.

    python recipes/agent-persona-original/run.py --output-dir ~/ai-output [--concept night-nurse-nia]

The card is a portable second-person prompt any model can adopt. With an image key set, the run
renders the 2:3 cover portrait and a square chat avatar (avatar.png) beside it; without one the
card publishes on its own.
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

GROUPS: dict[str, str] = {
    "Media-Personalities": "broadcast, podcast or streaming voices with an audience, a monetized worldview and a grievance.",
    "Everyday-Archetypes": "grounded working people whose job gives them their lens — an actuary, a foreman, a night nurse, a long-haul driver.",
    "Online-Archetypes": "natives of a specific internet subculture — the forum moderator, the reply guy, the wiki editor.",
    "Workplace-Archetypes": "office and institutional roles — the compliance officer, the middle manager, the founder on a third pivot, the union rep.",
    "Fringe-Archetypes": "true believers at the edges — wellness, doomsday prep, a very specific conspiracy, an economic monomania.",
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--group", choices=sorted(GROUPS), help="Override the archetype-group rotation.")
    p.add_argument("--concept", help="A kebab-case brief to build, e.g. night-nurse-nia.")


def prepare(ctx: RunContext) -> dict[str, str]:
    group = ctx.args.group or least_used(list(GROUPS), ctx.existing, "archetype_group")
    if ctx.args.concept:
        concept = (
            f"**Requested concept: `{ctx.args.concept}`** — read it as a brief (`night-nurse-nia` → an "
            "overnight nurse named Nia) and use it as the slug. Still wholly invented: if it points at a "
            "real person or an existing character, build an original who merely lives in the same world."
        )
    else:
        concept = "No concept was requested: pick a niche in this group that the cast doesn't cover yet."
    return {"GROUP": group, "GROUP_GUIDE": GROUPS[group], "CONCEPT": concept}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    card = (staging / "persona.md").read_text(encoding="utf-8")
    if not card.startswith("---\n") and not card.startswith("---\r\n"):
        raise RecipeError("persona.md must start with its frontmatter (---) at byte 0")
    front = card.split("---", 2)[1]
    if re.search(r"^tags:\s*\[", front, re.M):
        raise RecipeError("persona.md tags must be a YAML block list, not [a, b]")
    if re.search(r"^\s*#", front, re.M):
        raise RecipeError("persona.md frontmatter contains a # comment")
    purpose = re.search(r"^## Purpose\s*\n+(.+?)\s*$", card, re.M)
    if not purpose or len(purpose.group(1)) > 240:
        raise RecipeError("## Purpose must be one sentence under 240 characters")
    if not re.search(r"^## Persona\s*\n+You are ", card, re.M):
        raise RecipeError("## Persona must open in the second person ('You are …')")


RECIPE = Recipe(
    name="agent-persona-original",
    collection="agent-personas",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("persona.md",),
    skills=("character-sim", "llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("archetype_group", "subcategory"),
    cover_aspect="2:3",
    images=ImageSpec(min=1, max=1, aspects=("1:1",), folder="", optional=True),
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
