#!/usr/bin/env python3
"""News Collage — the news of a day, a week or a month as one cartoon-editorial image.

    python recipes/news-collage/run.py --output-dir ~/ai-output [--window day|week|month]

day   = yesterday's six U.S. stories, a vertical 2:3 six-panel grid with a date stamp
week  = the previous completed Mon–Sun, one landscape 3:2 scene titled WEEK IN REVIEW
month = the previous calendar month, the 2:3 grid with a month stamp

The agent researches the stories and writes the image prompt with exact short captions; the
runner renders it. No likeness of any real person: names appear only as in-world text.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RecipeError, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

WINDOWS = ["day", "week", "month"]
MAIN = "stories.md"
GRID = (
    "a 6-panel grid, two columns by three rows, each panel a square, clean borders between panels, "
    "the whole canvas vertical 2:3 with no extra height"
)
SCENE = (
    "one continuous landscape 3:2 scene — a chaotic newsroom, command center, map table or city square — "
    "with NO grid, boxes, panel borders, comic strips or numbered sections; stories sit at different "
    "depths (two or three in the foreground, the rest as props, screens and signage further back)"
)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--window", choices=WINDOWS, help="Override the day/week/month rotation.")


def window_for(kind: str, today: date) -> dict[str, str]:
    """Dates, stamp and layout text for one window, computed from `today`."""
    if kind == "day":
        d = today - timedelta(days=1)
        return {
            "WINDOW_LABEL": d.strftime("%A, %B %d, %Y").replace(" 0", " "),
            "DATE_FROM": d.isoformat(), "DATE_TO": d.isoformat(),
            "STAMP": d.strftime("%m/%d/%Y") + " 11:59 PM",
            "COUNT": "exactly six", "MIN": "6", "MAX": "6",
            "LAYOUT": GRID, "ASPECT": "2:3",
            "TITLE_LINE": "No title. A small professional date stamp in the bottom-right corner of the whole image, "
                          "preferably outside the six boxes, reading exactly",
        }
    if kind == "week":
        end = today - timedelta(days=today.weekday() + 1)  # last Sunday
        start = end - timedelta(days=6)
        rng = (f"{start.strftime('%b')} {start.day}-{end.day}, {end.year}" if start.month == end.month
               else f"{start.strftime('%b')} {start.day} - {end.strftime('%b')} {end.day}, {end.year}")
        return {
            "WINDOW_LABEL": f"the week of {rng}",
            "DATE_FROM": start.isoformat(), "DATE_TO": end.isoformat(),
            "STAMP": rng,
            "COUNT": "six to ten", "MIN": "6", "MAX": "10",
            "LAYOUT": SCENE, "ASPECT": "3:2",
            "TITLE_LINE": 'The title "WEEK IN REVIEW" placed naturally in the scene (a newsroom wall, ticker board or '
                          "newspaper masthead), and next to it the date range reading exactly",
        }
    first_this = today.replace(day=1)
    last_prev = first_this - timedelta(days=1)
    return {
        "WINDOW_LABEL": last_prev.strftime("%B %Y"),
        "DATE_FROM": last_prev.replace(day=1).isoformat(), "DATE_TO": last_prev.isoformat(),
        "STAMP": last_prev.strftime("%B %Y"),
        "COUNT": "exactly six", "MIN": "6", "MAX": "6",
        "LAYOUT": GRID, "ASPECT": "2:3",
        "TITLE_LINE": "No title. A small professional month stamp in the bottom-right corner of the whole image, "
                      "preferably outside the six boxes, reading exactly",
    }


def prepare(ctx: RunContext) -> dict[str, str]:
    kind = ctx.args.window or least_used(WINDOWS, ctx.existing, "window")
    ctx.state["window"] = kind
    return {"WINDOW": kind, **window_for(kind, ctx.day)}


STORY_RE = re.compile(r"^### .+$", re.M)
LINK_RE = re.compile(r"https?://\S+")
CAPTION_RE = re.compile(r'^\*\*Caption:\*\*\s*"(.+?)"\s*$', re.M)


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    kind = str(ctx.state.get("window") or manifest.get("window"))
    if manifest.get("window") != kind:
        raise RecipeError("final JSON `window` must be this run's window")
    text = (staging / MAIN).read_text(encoding="utf-8")
    blocks = STORY_RE.split(text)[1:]
    lo, hi = (6, 10) if kind == "week" else (6, 6)
    if not lo <= len(blocks) <= hi:
        raise RecipeError(f"{MAIN} has {len(blocks)} `### ` stories; a {kind} window needs {lo}–{hi}")
    captions = CAPTION_RE.findall(text)
    if len(captions) != len(blocks):
        raise RecipeError(f"{MAIN}: every story needs one `**Caption:** \"...\"` line ({len(captions)} of {len(blocks)})")
    for i, block in enumerate(blocks, 1):
        if not LINK_RE.search(block):
            raise RecipeError(f"{MAIN}: story {i} has no source URL")
    for c in captions:
        n = len(c.split())
        if not 3 <= n <= 8:
            raise RecipeError(f"caption {c!r} is {n} words; keep captions to 3–8")
        if re.match(r"^\s*\d+[.)]", c):
            raise RecipeError(f"caption {c!r} is numbered; panels are never numbered")
    if manifest.get("story_count") != len(blocks):
        raise RecipeError("final JSON `story_count` must equal the number of stories in stories.md")
    imgs = manifest.get("images") or []
    want = "3:2" if kind == "week" else "2:3"
    if not (isinstance(imgs, list) and len(imgs) == 1 and imgs[0].get("aspect") == want):
        raise RecipeError(f"images must be one entry with aspect {want!r} for a {kind} window")


RECIPE = Recipe(
    name="news-collage",
    collection="news-collages",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=(MAIN,),
    skills=("image-prompt-craft",),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("window", "story_count"),
    cover_aspect=None,
    images=ImageSpec(min=1, max=1, aspects=("2:3", "3:2"), folder="", text_ok=True),
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
