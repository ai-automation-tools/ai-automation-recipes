#!/usr/bin/env python3
"""3D Print Idea — one researched, build-ready printable product design per run.

    python recipes/weekly-3d-print-ideas/run.py --output-dir ~/ai-output [--subcategory Desk-and-Tech]

The original job made three designs per run; this one makes one, so each design is its own
artifact with its own mockup. Schedule it three times a week for the same volume.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402
from recipes._shared.webcheck import check_json, check_sources_csv  # noqa: E402

BUILD_VOLUME_MM = 220

SUBCATEGORIES: dict[str, str] = {
    "Household": "Useful household gadgets, kitchen helpers (non-food-contact), bathroom, laundry, pet items.",
    "Organization-and-Storage": "Organizers, modular storage systems (Gridfinity-compatible and similar), "
                                "wall mounts, drawer inserts.",
    "Desk-and-Tech": "Computer accessories, cable management, stands, docks, keyboard and mouse accessories, "
                     "AI/tech desk gear.",
    "Toys-and-Fidgets": "Fidget toys, print-in-place toys, original articulated figures, kids' toys.",
    "Puzzles-and-Games": "Mechanical puzzles, puzzle boxes, board-game inserts and accessories, tabletop pieces.",
    "Art-and-Decor": "Sculptures, lamps, planters, wall art, piece-by-piece collectible series.",
    "Sports-and-Fan-Gear": "Generic sports accessories, display stands, training aids, ball and gear holders "
                           "(no team IP).",
    "Tools-and-Workshop": "Jigs, workshop organizers, maker tools, 3D-printer accessories.",
    "Outdoor-and-Garden": "Garden tools, camping and hiking gear, outdoor mounts (note UV/weather material choice).",
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--subcategory", choices=sorted(SUBCATEGORIES), help="Override the subcategory rotation.")


def prepare(ctx: RunContext) -> dict[str, str]:
    sub = ctx.args.subcategory or least_used(list(SUBCATEGORIES), ctx.existing, "subcategory")
    return {"SUBCATEGORY": sub, "SUBCATEGORY_LABEL": sub.replace("-", " "), "SUBCATEGORY_GUIDE": SUBCATEGORIES[sub]}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    spec = check_json(staging, "design-spec.json")
    check_sources_csv(staging, lo=4, hi=8)
    if not isinstance(spec, dict) or not isinstance(spec.get("parts"), list):
        raise RecipeError("design-spec.json needs a `parts` array")
    readme = (staging / "README.md").read_text(encoding="utf-8")
    for part in spec["parts"]:
        box = part.get("bounding_box") or {}
        dims = [box.get(k) for k in ("x", "y", "z")]
        if not all(isinstance(d, (int, float)) and 0 < d <= BUILD_VOLUME_MM for d in dims):
            raise RecipeError(f"part {part.get('id')!r} bounding box {box} is missing or exceeds {BUILD_VOLUME_MM} mm")
        if str(part.get("name", "")) not in readme:
            raise RecipeError(f"part {part.get('name')!r} is in design-spec.json but not in README.md")


RECIPE = Recipe(
    name="weekly-3d-print-ideas",
    collection="3d-print-designs",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("README.md", "design-spec.json", "sources.csv"),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("subcategory", "modeling_difficulty"),
    cover_aspect="1:1",
    default_model="opus",
    timeout_s=2400,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
