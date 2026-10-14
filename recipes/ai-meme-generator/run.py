#!/usr/bin/env python3
"""AI Meme — one original square meme, caption baked in, twice a week.

    python recipes/ai-meme-generator/run.py --output-dir ~/ai-output [--theme "AI at work"]

Optional idea queue: put `meme-ideas.md` in <output-dir>/ai-memes/ with lines like
`- [ ] AI replacing everyone except the people who schedule meetings`. The first unchecked idea
becomes the joke, and the run ticks it off with a link to the meme it became.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

THEMES = [
    "AI at work",
    "AI assistants at home",
    "tech culture and startups",
    "internet and social media life",
    "prices, subscriptions and money",
    "streaming and entertainment",
    "gaming",
    "dating and social apps",
    "smart gadgets",
    "office life and meetings",
    "science and the future",
    "everyday relatable chaos",
]

IDEAS_FILE = "meme-ideas.md"
UNCHECKED = re.compile(r"^(\s*[-*]\s*)\[ \]\s*(.+)$", re.M)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--theme", help="Override the theme rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    theme = ctx.args.theme or least_used(THEMES, ctx.existing, "theme")
    ideas = ctx.collection_dir / IDEAS_FILE
    m = UNCHECKED.search(ideas.read_text(encoding="utf-8")) if ideas.is_file() else None
    ctx.state["idea"] = m.group(2).strip() if m else None
    idea = (f"**Joke:** use this idea from the queue — {ctx.state['idea']}. Treat the theme as context."
            if m else "Invent the joke yourself.")
    return {"THEME": theme, "IDEA": idea}


def finish(ctx: RunContext, final: Path, manifest: dict[str, object]) -> None:
    idea = ctx.state.get("idea")
    if not idea:
        return
    path = ctx.collection_dir / IDEAS_FILE
    text = path.read_text(encoding="utf-8")
    m = UNCHECKED.search(text)
    if m and m.group(2).strip() == idea:
        done = f"{m.group(1)}[x] {m.group(2).rstrip()} — meme: {final.relative_to(ctx.collection_dir).as_posix()}"
        path.write_text(text[: m.start()] + done + text[m.end():], encoding="utf-8")


RECIPE = Recipe(
    name="ai-meme-generator",
    collection="ai-memes",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("meme.md",),
    skills=("image-prompt-craft",),
    fields=("theme",),
    cover_aspect=None,
    images=ImageSpec(min=1, max=1, aspects=("1:1",), folder="", text_ok=True),
    default_model="sonnet",
    timeout_s=900,
    add_args=add_args,
    prepare=prepare,
    finish=finish,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
