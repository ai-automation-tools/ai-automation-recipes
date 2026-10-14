#!/usr/bin/env python3
"""Alternate History — one illustrated "what if" timeline a week.

    python recipes/alternate-history/run.py --output-dir ~/ai-output

Optional premise queue: put `alt-history-ideas.md` in <output-dir>/alternate-history/ with lines
like `- [ ] The Library of Alexandria is never destroyed.` The first unchecked premise is used,
then ticked off with a link to the piece. With no queue, the agent invents a premise.

With an image key set, the eight scene prompts are rendered to scenes/01-….png … 08-….png at
16:9 alongside the 2:3 cover. Without one, the prompts are still written (scene-prompts.md) and
the piece publishes text-only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RecipeError, RunContext, run  # noqa: E402

IDEAS_FILE = "alt-history-ideas.md"
UNCHECKED = re.compile(r"^(\s*[-*]\s*)\[ \]\s*(.+)$", re.M)
SECTIONS = 8


def _next_idea(ctx: RunContext) -> str | None:
    path = ctx.collection_dir / IDEAS_FILE
    if not path.is_file():
        return None
    m = UNCHECKED.search(path.read_text(encoding="utf-8"))
    return m.group(2).strip() if m else None


def prepare(ctx: RunContext) -> dict[str, str]:
    idea = _next_idea(ctx)
    ctx.args._idea = idea
    premise = (
        f"Use this premise from the queue: **{idea}**"
        if idea
        else "Invent a fresh premise: pick a real, well-documented turning point in history and "
        "change its outcome."
    )
    return {"IDEA": premise}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    story = (staging / "story.md").read_text(encoding="utf-8")
    sections = [h for h in re.findall(r"^## (.+)$", story, re.M) if h.strip().lower() != "synopsis"]
    if len(sections) != SECTIONS:
        raise RecipeError(f"story.md has {len(sections)} sections, expected {SECTIONS}")
    scenes = re.findall(r"^## \d+\.", (staging / "scene-prompts.md").read_text(encoding="utf-8"), re.M)
    if len(scenes) != SECTIONS:
        raise RecipeError(f"scene-prompts.md has {len(scenes)} scenes, expected {SECTIONS}")


def finish(ctx: RunContext, final: Path, manifest: dict[str, object]) -> None:
    idea = getattr(ctx.args, "_idea", None)
    if not idea:
        return
    path = ctx.collection_dir / IDEAS_FILE
    text = path.read_text(encoding="utf-8")
    m = UNCHECKED.search(text)
    if m and m.group(2).strip() == idea:
        rel = final.relative_to(ctx.collection_dir).as_posix()
        done = f"{m.group(1)}[x] {m.group(2).rstrip()} — {rel}"
        path.write_text(text[: m.start()] + done + text[m.end():], encoding="utf-8")


RECIPE = Recipe(
    name="alternate-history",
    collection="alternate-history",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("story.md", "scene-prompts.md"),
    skills=("writing-principles", "creative-writing-craft", "llm-writing", "humanizer", "image-prompt-craft"),
    fields=("era", "divergence_point"),
    cover_aspect="2:3",
    images=ImageSpec(min=SECTIONS, max=SECTIONS, aspects=("16:9",), folder="scenes", optional=True),
    default_model="opus",
    timeout_s=2400,
    prepare=prepare,
    validate=validate,
    finish=finish,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
