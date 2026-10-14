#!/usr/bin/env python3
"""Satirical News — one deadpan, Onion-style article a run under the masthead The Overcorrect.

    python recipes/satirical-news/run.py --output-dir ~/ai-output [--beat "Space & Aliens"] [--topic "hoa bans weather"]

The beat rotates over twelve categories, least-used first. The agent may anchor the piece on a
real current story found with WebSearch (recorded in the frontmatter as `inspired_by`) or invent it
outright. With an image key set, the run renders the 16:9 cover plus a square thumbnail and two
in-article illustrations; without one the article publishes on its own.
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

BEATS: dict[str, str] = {
    "AI Tool Releases": "new models, agents, \"revolutionary\" launches, feature bloat.",
    "New Technology & Products": "gadgets, apps, hardware, questionable innovation.",
    "Politics": "campaigns, legislation, government, political theater (parody, not endorsement).",
    "Finance & Economy": "markets, crypto, banks, the economy, personal finance.",
    "Space & Aliens": "NASA, private space, UFOs, first contact, cosmic absurdity.",
    "Science & Discovery": "studies, research, \"scientists confirm…\", academia.",
    "Sports": "leagues, athletes, deranged fans, absurd rule changes.",
    "Entertainment & Celebrity": "Hollywood, streaming, music, awards, influencer culture.",
    "Health & Wellness": "wellness fads, biohacking, dubious studies, \"one weird trick\".",
    "Local / Area Man": "the classic human-interest beat (\"Area Man Declares…\"), small-town absurdity, relatable-guy pathos.",
    "Business & Corporate": "startups, CEOs, layoffs-as-vibes, corporate memos, HR.",
    "Environment & Climate": "nature, animals, weather, climate, the planet fighting back.",
}
WORDS = (350, 650)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--beat", choices=sorted(BEATS), help="Override the beat rotation.")
    p.add_argument("--topic", help="Write about this topic instead of picking one (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    beat = ctx.args.beat or least_used(list(BEATS), ctx.existing, "beat")
    if ctx.args.topic:
        topic = (
            f"**Requested topic: `{ctx.args.topic}`** — write that article. Set `news_category` to "
            "whichever beat fits it best; the rotation pick above is only a default."
        )
    else:
        topic = "No topic was requested: find a premise on this beat that the archive doesn't have yet."
    return {"BEAT": beat, "BEAT_GUIDE": BEATS[beat], "TOPIC": topic,
            "BEATS": "\n".join(f"- **{b}** — {g}" for b, g in BEATS.items())}


def body_words(article: str) -> int:
    body = article.split("---", 2)[2] if article.startswith("---") else article
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)  # image lines aren't prose
    return len(body.split())


def validate(staging: Path, manifest: dict[str, object]) -> None:
    article = (staging / "article.md").read_text(encoding="utf-8")
    if not article.startswith("---\n") and not article.startswith("---\r\n"):
        raise RecipeError("article.md must start with its frontmatter (---) at byte 0")
    front = article.split("---", 2)[1]
    cat = re.search(r'^news_category:\s*"?([^"\n]+?)"?\s*$', front, re.M)
    if not cat or cat.group(1) not in BEATS:
        raise RecipeError(f"article.md news_category must be one of {sorted(BEATS)}")
    if manifest.get("beat") != cat.group(1):
        raise RecipeError("final JSON `beat` must match the article's news_category")
    true_event = re.search(r"^based_on_true_event:\s*(true|false)\s*$", front, re.M)
    if not true_event:
        raise RecipeError("article.md frontmatter needs based_on_true_event: true | false")
    if true_event.group(1) == "true" and not re.search(r"^inspired_by:\s*\"?https?://", front, re.M):
        raise RecipeError("a true-event article must record the real story's URL in inspired_by")
    if not re.search(r"^# \S", article, re.M):
        raise RecipeError("article.md needs its headline as an H1")
    if not re.search(r"^\*\*[^*\n]+\*\*\s*[—–-]", article, re.M):
        raise RecipeError("article.md must open with a bold dateline (**CITY, ST** —)")
    n = body_words(article)
    if not WORDS[0] <= n <= WORDS[1]:
        raise RecipeError(f"article.md body is {n} words; the piece runs {WORDS[0]}–{WORDS[1]}")
    meta = (staging / "metadata.md").read_text(encoding="utf-8")
    points = re.search(r"^## Key Points\s*\n((?:\s*- .+\n?)+)", meta, re.M)
    if not points or len(re.findall(r"^\s*- ", points.group(1), re.M)) < 3:
        raise RecipeError("metadata.md needs ## Key Points with at least three bullets")
    if not re.search(r"^## Summary\s*\n+\S", meta, re.M):
        raise RecipeError("metadata.md needs a ## Summary paragraph")


RECIPE = Recipe(
    name="satirical-news",
    collection="satirical-news",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("article.md", "metadata.md"),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("beat", "based_on_true_event"),
    cover_aspect="16:9",
    images=ImageSpec(min=2, max=3, aspects=("1:1", "3:4", "16:9"), folder="images", optional=True),
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
