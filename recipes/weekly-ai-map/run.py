#!/usr/bin/env python3
"""Weekly AI Map — one researched, interactive Leaflet map of 8–20 real places a week.

    python recipes/weekly-ai-map/run.py --output-dir ~/ai-output [--idea "coffee crawl in Portland"]

Topic types rotate (least used first); --idea builds a specific map instead.
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

log = logging.getLogger("recipes")

TOPIC_TYPES = [
    "road trips and scenic drives",
    "food trails: restaurant crawls, coffee routes, dessert maps, regional food guides",
    "hiking trails, waterfalls, overlooks, beaches and outdoor recreation",
    "national parks, state parks, monuments and public lands",
    "city visitor guides and weekend getaway itineraries",
    "museum, history, architecture, music, sports or pop-culture tours",
    "seasonal outings: holiday lights, farmers markets, fairs, festivals, family days out",
    "niche practical guides: airport layover walks, EV-charging road trips, rainy-day attractions",
]

ALLOWED = ("https://unpkg.com/leaflet@", "https://cdnjs.cloudflare.com/ajax/libs/leaflet/",
           "https://cdn.jsdelivr.net/npm/leaflet@", "data:")


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--idea", help="Build this specific map instead of a rotating topic.")


def prepare(ctx: RunContext) -> dict[str, str]:
    if ctx.args.idea:
        return {"TOPIC": f"**Map idea (build THIS): {ctx.args.idea}.** Turn it into a clear, specific, "
                         "useful map concept. Set `topic_type` to `custom`."}
    topic = least_used(TOPIC_TYPES, ctx.existing, "topic_type")
    return {"TOPIC": f"**Topic type: `{topic}`** — chosen by the runner so the collection stays varied. "
                     "Pick one specific map within it, and set `topic_type` to exactly that string."}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    html = (staging / "index.html").read_text(encoding="utf-8")
    if not re.search(r"\bstops\s*=\s*\[", html):
        raise RecipeError("index.html has no `stops = [` array")
    for src in re.findall(r"""<(?:script|link|img)[^>]+(?:src|href)\s*=\s*["']([^"']+)""", html, re.I):
        if not src.startswith(ALLOWED):
            raise RecipeError(f"index.html references a disallowed resource: {src}")

    node = shutil.which("node")
    if not node:
        log.warning("node not on PATH — skipping the JS syntax check")
        return
    inline = re.findall(r'''<script(?![^>]*\bsrc\s*=)(?![^>]*\btype\s*=\s*["']?(?!(?:text|application)/javascript\b|module\b)[\w/+.-]+)[^>]*>(.*?)</script>''', html, re.S | re.I)
    with tempfile.TemporaryDirectory() as tmp:
        for i, body in enumerate(inline):
            js = Path(tmp) / f"inline-{i}.js"
            js.write_text(body, encoding="utf-8")
            proc = subprocess.run([node, "--check", str(js)], capture_output=True, text=True)
            if proc.returncode != 0:
                raise RecipeError(f"inline script {i} fails `node --check`:\n{proc.stderr[-1500:]}")


RECIPE = Recipe(
    name="weekly-ai-map",
    collection="maps",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("index.html", "guide.md", "metadata.md"),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("topic_type", "place"),
    cover_aspect="16:9",
    default_model="opus",
    timeout_s=3600,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
