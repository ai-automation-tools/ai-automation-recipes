#!/usr/bin/env python3
"""Future Cities 2500 — one real city imagined 475 years forward, as a 16:9 cinematic cityscape.

    python recipes/future-cities/run.py --output-dir ~/ai-output [--city "Lisbon"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402

CITIES = [
    "San Francisco", "New York City", "Tokyo", "London", "Paris", "Dubai", "Singapore", "Shanghai",
    "Hong Kong", "Sydney", "Los Angeles", "Chicago", "Toronto", "Mexico City", "Rio de Janeiro",
    "São Paulo", "Buenos Aires", "Lagos", "Cairo", "Nairobi", "Cape Town", "Istanbul", "Moscow",
    "Berlin", "Amsterdam", "Barcelona", "Rome", "Venice", "Athens", "Stockholm", "Reykjavik",
    "Mumbai", "Delhi", "Bangkok", "Jakarta", "Seoul", "Beijing", "Kyoto", "Manila", "Kuala Lumpur",
    "Tehran", "Riyadh", "Tel Aviv", "Marrakech", "Vancouver", "Seattle", "Miami", "Las Vegas",
    "Boston", "Washington DC", "Havana", "Lima", "Bogotá", "Santiago", "Lisbon", "Vienna", "Prague",
    "Copenhagen", "Oslo", "Helsinki", "Warsaw", "Kyiv", "Dublin", "Edinburgh", "Zurich", "Auckland",
    "Honolulu", "Anchorage",
]


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--city", help="Override the city rotation (any real city).")


def prepare(ctx: RunContext) -> dict[str, str]:
    return {"CITY": ctx.args.city or least_used(CITIES, ctx.existing, "city")}


RECIPE = Recipe(
    name="future-cities",
    collection="future-cities",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("city.md",),
    skills=("llm-writing", "image-prompt-craft"),
    fields=("city",),
    cover_aspect=None,
    images=ImageSpec(min=1, max=1, aspects=("16:9",), folder=""),
    default_model="sonnet",
    timeout_s=900,
    add_args=add_args,
    prepare=prepare,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
