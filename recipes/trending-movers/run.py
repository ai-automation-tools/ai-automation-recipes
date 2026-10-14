#!/usr/bin/env python3
"""Trending Movers — a star-velocity leaderboard across all of open source.

The weekly figures are measured, not researched: prepare() scrapes GitHub's weekly
trending pages, and validate() rejects a digest whose published "+N this week" figures
or order don't match those measurements.

    python recipes/trending-movers/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.digest import MAIN, candidates_block, digest_recipe, fetch_candidates  # noqa: E402

from core import RecipeError, run  # noqa: E402

log = logging.getLogger("recipes")

FEEDS = {
    "trending": [
        "https://github.com/trending?since=weekly",
        "https://github.com/trending/python?since=weekly",
        "https://github.com/trending/typescript?since=weekly",
        "https://github.com/trending/javascript?since=weekly",
        "https://github.com/trending/rust?since=weekly",
        "https://github.com/trending/go?since=weekly",
    ],
    "keywords": [],  # all of open source, ordered by momentum
    "sort": "stars",
    "limit": 40,
}

ENTRY_RE = re.compile(r"^###\s+\d+\.\s+\[([^\]]+)\]\((\S+?)\)\s*$")
GAIN_RE = re.compile(r"^\s*-\s+\*\*Stars this week:\*\*\s*\+?([\d,]+)")
CATEGORIES = {"AI/ML", "Dev Tools", "CLI", "Web", "Data", "Infra/DevOps", "Security", "Other"}
measured: dict[str, int] = {}  # url -> starsThisWeek, filled by prepare() for validate()


def _key(url: str) -> str:
    return url.rstrip("/").lower()


def _leaderboard(text: str) -> list[tuple[str, int | None]]:
    """[(url, weekly gain)] for the `### N. [owner/repo](url)` entries, in order."""
    rows: list[tuple[str, int | None]] = []
    for line in text.splitlines():
        if (m := ENTRY_RE.match(line)):
            rows.append((m.group(2), None))
        elif rows and rows[-1][1] is None and (g := GAIN_RE.match(line)):
            rows[-1] = (rows[-1][0], int(g.group(1).replace(",", "")))
    return rows


def _history(ctx, runs: int = 4) -> str:
    """Last few leaderboards, for trajectory notes ("third week running, gain slowing")."""
    files = sorted(ctx.collection_dir.glob(f"*/*/{MAIN}"))[-runs:]
    lines = []
    for f in files:
        rows = _leaderboard(f.read_text(encoding="utf-8"))
        lines += [f"- {f.parent.name[:10]} · {url} — +{gain:,}" for url, gain in rows if gain is not None]
    return "\n".join(lines) or "(no earlier leaderboards — this is the first run)"


def prepare_extra(ctx) -> dict[str, str]:
    payload = fetch_candidates(FEEDS)
    measured.clear()
    measured.update({_key(c["url"]): c["starsThisWeek"] for c in payload["candidates"] if c.get("starsThisWeek")})
    return {"CANDIDATES": candidates_block(payload, desc_chars=200), "HISTORY": _history(ctx)}


def validate_extra(staging: Path, manifest, cats) -> None:
    unknown = set(cats) - CATEGORIES - {"Repos"}
    if unknown:
        raise RecipeError(f"categories outside the closed list: {sorted(unknown)}")
    rows = _leaderboard((staging / MAIN).read_text(encoding="utf-8"))
    if not rows:
        raise RecipeError("no `### N. [owner/repo](url)` leaderboard entries found")
    for url, gain in rows:
        if gain is None:
            raise RecipeError(f"{url} has no `**Stars this week:**` figure")
        if _key(url) not in measured:
            # A renamed repo is published under its final URL, so it can't be matched here.
            log.warning("trending-movers: %s is not in the measured list (renamed?) — figure unchecked", url)
        elif measured[_key(url)] != gain:
            raise RecipeError(f"{url}: published +{gain:,}, measured +{measured[_key(url)]:,}")
    gains = [g for _, g in rows]
    if gains != sorted(gains, reverse=True):
        raise RecipeError("leaderboard is not in descending order of weekly gain")


RECIPE = digest_recipe(
    name="trending-movers",
    collection="trending-movers",
    archive_title="Trending Movers — Full Archive",
    prepare_extra=prepare_extra,
    validate_extra=validate_extra,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
