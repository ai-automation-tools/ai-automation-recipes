#!/usr/bin/env python3
"""Finance Digest — one of eight money briefings a run, written from feeds and pages the agent fetched.

    python recipes/finance-digest/run.py --output-dir ~/ai-output [--topic transfer-bonuses] [--days 7]

Eight topics live in topics.json beside this file: three market briefings (a stock-market recap,
paper trade ideas, a strategy brief) and five rewards digests (Chase UR, card sign-up bonuses,
transfer bonuses, shopping portals, a cashback-portal leaderboard). A run takes the least-covered
topic unless --topic says otherwise. Topics with feeds get the window's items fetched for them, as
news-digest does; the leaderboard has no feeds and names the store pages to fetch instead. Market
levels come from public pages the agent reads and cites, never from a keyed API. Every edition ends
with the same Not Financial Advice section, and the runner refuses one that doesn't.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402
from core.digest import candidates_block, fetch_candidates, window_items  # noqa: E402

MAIN = "digest.md"
TOPICS: dict[str, dict] = json.loads((HERE / "topics.json").read_text(encoding="utf-8"))
PER_SOURCE_CAP = 20
GLOBAL_CAP = 120
MIN_LINKS = 6
DISCLAIMER = ("For educational purposes only. Not investment, tax or financial advice. Rates, offers and prices "
              "change; verify on the source before acting, and do your own research.")
PAPER_LINE = "Paper only: study ideas, not orders."
IDEA_SECTIONS = ("Dividend Ideas", "Growth Ideas", "ETF Ideas")
LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)")


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--topic", choices=sorted(TOPICS), help="Override the topic rotation.")
    p.add_argument("--days", type=int, default=7, help="How many days back the feed window reaches (default 7).")


def section(text: str, heading: str) -> str:
    """The body of the first `## <heading>…` section, or ''."""
    m = re.search(rf"^##\s+{re.escape(heading)}.*?$\n(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def table_headers(body: str) -> list[str]:
    """The header line of every markdown table in a section body."""
    lines = body.splitlines()
    return [lines[i].strip() for i in range(len(lines) - 1)
            if lines[i].strip().startswith("|") and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1])]


def prepare(ctx: RunContext) -> dict[str, str]:
    topic = ctx.args.topic or least_used(sorted(TOPICS), ctx.existing, "topic")
    spec = TOPICS[topic]
    if spec["feeds"]:
        payload = fetch_candidates({"feeds": spec["feeds"], "limit": 10_000})
        payload["candidates"] = window_items(payload["candidates"], ctx.args.days, PER_SOURCE_CAP, GLOBAL_CAP)
        if not payload["candidates"]:
            raise RecipeError(f"no feed items for {topic!r} in the last {ctx.args.days} days "
                              f"({len(payload['feeds_failed'])} of {len(spec['feeds'])} feeds failed)")
        candidates = candidates_block(payload, desc_chars=360)
    else:
        candidates = "(this topic has no feeds; the pages to fetch are listed under THE BEAT)"
    stores = spec.get("stores", [])
    ctx.state["topic"] = topic
    end = ctx.day
    start = end - timedelta(days=ctx.args.days)
    return {
        "TOPIC": topic,
        "TOPIC_NAME": spec["name"],
        "EMOJI": spec["emoji"],
        "KIND": spec["kind"],
        "FOCUS": spec["focus"],
        "RULES": spec["rules"],
        "SECTIONS": "\n".join(f"- `## {s}`" for s in spec["sections"]),
        "MIN_SECTIONS": str(spec["min_sections"]),
        "WINDOW": f"{start.isoformat()} to {end.isoformat()}",
        "PALETTE": spec["palette"],
        "MOTIF": spec["motif"],
        "CANDIDATES": candidates,
        "STORES": ("Store pages to fetch, in this order:\n"
                   + "\n".join(f"- https://www.cashbackmonitor.com/cashback-store/{s}/" for s in stores)
                   if stores else "(no store pages for this topic)"),
        "DISCLAIMER": DISCLAIMER,
        "PAPER_LINE": PAPER_LINE,
    }


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    text = (staging / MAIN).read_text(encoding="utf-8")
    topic = str(ctx.state.get("topic") or manifest.get("topic"))
    spec = TOPICS[topic]
    headings = re.findall(r"^##\s+(.+?)\s*$", text, re.M)
    if not headings or headings[-1] != "Not Financial Advice":
        raise RecipeError(f"{MAIN} must end with the `## Not Financial Advice` section")
    if DISCLAIMER not in section(text, "Not Financial Advice"):
        raise RecipeError("the Not Financial Advice section must carry the fixed disclaimer sentence verbatim")
    present = [s for s in spec["sections"] if re.search(rf"^##\s+{re.escape(s)}", text, re.M)]
    if len(present) < spec["min_sections"]:
        raise RecipeError(f"{MAIN} uses {len(present)} of the topic's sections; need at least "
                          f"{spec['min_sections']} of {spec['sections']}")
    links = set(LINK_RE.findall(text))
    if len(links) < MIN_LINKS:
        raise RecipeError(f"{MAIN} cites {len(links)} source links; need at least {MIN_LINKS}")
    if topic == "trade-ideas":
        if PAPER_LINE not in text:
            raise RecipeError(f"trade-ideas must carry the line `{PAPER_LINE}`")
        for s in IDEA_SECTIONS:
            heads = table_headers(section(text, s))
            if section(text, s) and (not heads or any("risk" not in h.lower() for h in heads)):
                raise RecipeError(f"every idea table under `## {s}` needs a Risk column")
    if ctx.state.get("topic") and manifest.get("topic") != ctx.state["topic"]:
        raise RecipeError("final JSON `topic` must be this run's topic id")
    count = manifest.get("story_count")
    if not isinstance(count, int) or count < MIN_LINKS:
        raise RecipeError("final JSON `story_count` must be the number of distinct sources linked")


RECIPE = Recipe(
    name="finance-digest",
    collection="finance-digests",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=(MAIN,),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("topic", "story_count"),
    cover_aspect="16:9",
    default_model="sonnet",
    timeout_s=2700,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
