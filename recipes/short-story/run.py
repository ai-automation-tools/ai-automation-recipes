#!/usr/bin/env python3
"""Short Story — one complete 2,000–4,000-word story a week, plus a cover.

    python recipes/short-story/run.py --output-dir ~/ai-output [--genre "cozy mystery"]

Optional idea queue: put `story-ideas.md` in <output-dir>/short-stories/ with lines like
`- [ ] A lighthouse keeper who…`. The first unchecked idea becomes the premise, and the
run ticks it off with a link to the story it became.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

GENRES = [
    "near-future AI fiction",
    "cozy mystery",
    "cyberpunk",
    "office absurdism",
    "magical realism",
    "quiet horror",
    "tech satire",
    "fantasy",
    "identity / security thriller",
    "comedy",
    "hard sci-fi",
]

IDEAS_FILE = "story-ideas.md"
UNCHECKED = re.compile(r"^(\s*[-*]\s*)\[ \]\s*(.+)$", re.M)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--genre", help="Override the genre rotation (any string).")


def _next_idea(ctx: RunContext) -> str | None:
    path = ctx.collection_dir / IDEAS_FILE
    if not path.is_file():
        return None
    m = UNCHECKED.search(path.read_text(encoding="utf-8"))
    return m.group(2).strip() if m else None


def prepare(ctx: RunContext) -> dict[str, str]:
    genre = ctx.args.genre or least_used(GENRES, ctx.existing, "genre")
    idea = _next_idea(ctx)
    ctx.args._idea = idea
    premise = (
        f"Use this idea from the queue: **{idea}**"
        if idea
        else "Invent an original premise that fits the genre and is unlike every story listed below."
    )
    return {"GENRE": genre, "IDEA": premise}


def finish(ctx: RunContext, final: Path, manifest: dict[str, object]) -> None:
    idea = getattr(ctx.args, "_idea", None)
    if not idea:
        return
    path = ctx.collection_dir / IDEAS_FILE
    text = path.read_text(encoding="utf-8")
    rel = final.relative_to(ctx.collection_dir).as_posix()
    m = UNCHECKED.search(text)
    if m and m.group(2).strip() == idea:
        done = f"{m.group(1)}[x] {m.group(2).rstrip()} — story: {rel}"
        path.write_text(text[: m.start()] + done + text[m.end():], encoding="utf-8")


RECIPE = Recipe(
    name="short-story",
    collection="short-stories",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("story.md",),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    fields=("genre",),
    cover_aspect="2:3",
    default_model="opus",
    timeout_s=2400,
    add_args=add_args,
    prepare=prepare,
    finish=finish,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
