#!/usr/bin/env python3
"""News Digest — a weekly briefing on one topic, written from that topic's own feeds.

    python recipes/news-digest/run.py --output-dir ~/ai-output [--topic energy] [--days 7]

Ten topics live in topics.json beside this file, each with its feed list, sections, palette and
cover motif; a run takes the least-covered one unless --topic says otherwise. The runner fetches the
feeds, keeps the last `--days` of items (capped per source so one loud feed can't crowd the rest),
and hands the agent that candidate list. The agent reads, groups and writes; it never invents a
story the feeds didn't carry.
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
PER_SOURCE_CAP = 16
GLOBAL_CAP = 150
MIN_LINKS = 8
LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)")


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--topic", choices=sorted(TOPICS), help="Override the topic rotation.")
    p.add_argument("--days", type=int, default=7, help="How many days back the feed window reaches (default 7).")


def prepare(ctx: RunContext) -> dict[str, str]:
    topic = ctx.args.topic or least_used(sorted(TOPICS), ctx.existing, "topic")
    spec = TOPICS[topic]
    payload = fetch_candidates({"feeds": spec["feeds"], "limit": 10_000})
    payload["candidates"] = window_items(payload["candidates"], ctx.args.days, PER_SOURCE_CAP, GLOBAL_CAP)
    if not payload["candidates"]:
        raise RecipeError(f"no feed items for {topic!r} in the last {ctx.args.days} days "
                          f"({len(payload['feeds_failed'])} of {len(spec['feeds'])} feeds failed)")
    ctx.state["topic"] = topic
    end = ctx.day
    start = end - timedelta(days=ctx.args.days)
    return {
        "TOPIC": topic,
        "TOPIC_NAME": spec["name"],
        "EMOJI": spec["emoji"],
        "FOCUS": spec["focus"],
        "SECTIONS": "\n".join(f"- `## {s}`" for s in spec["sections"]),
        "WINDOW": f"{start.isoformat()} to {end.isoformat()}",
        "PALETTE": spec["palette"],
        "MOTIF": spec["motif"],
        "CANDIDATES": candidates_block(payload, desc_chars=360),
        "CANDIDATE_URLS": "\n".join(c["url"] for c in payload["candidates"]),
    }


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    text = (staging / MAIN).read_text(encoding="utf-8")
    spec = TOPICS[str(ctx.state.get("topic") or manifest.get("topic"))]
    for h in ("Top Stories", "Watchlist", "Sources"):
        if not re.search(rf"^##\s+{re.escape(h)}", text, re.M):
            raise RecipeError(f"{MAIN} is missing the `## {h}` section")
    present = [s for s in spec["sections"] if re.search(rf"^##\s+{re.escape(s)}", text, re.M)]
    if len(present) < 3:
        raise RecipeError(f"{MAIN} uses {len(present)} of the topic's sections; need at least 3 of {spec['sections']}")
    links = set(LINK_RE.findall(text))
    if len(links) < MIN_LINKS:
        raise RecipeError(f"{MAIN} links {len(links)} stories; need at least {MIN_LINKS}")
    if re.search(r"^\s*\|.*\|\s*$", text, re.M):
        raise RecipeError(f"{MAIN} contains a markdown table; the digest is lists and prose only")
    if ctx.state.get("topic") and manifest.get("topic") != ctx.state["topic"]:
        raise RecipeError("final JSON `topic` must be this run's topic id")
    count = manifest.get("story_count")
    if not isinstance(count, int) or count < MIN_LINKS:
        raise RecipeError("final JSON `story_count` must be the number of distinct stories linked")


RECIPE = Recipe(
    name="news-digest",
    collection="news-digests",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=(MAIN,),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebFetch"),
    fields=("topic", "story_count"),
    cover_aspect="16:9",
    default_model="sonnet",
    timeout_s=2400,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
