#!/usr/bin/env python3
"""Weekly Wallpaper Pack — three themed wallpapers, each shipped as a matching desktop + phone pair.

    python recipes/wallpaper-packs/run.py --output-dir ~/ai-output

Each wallpaper renders once as a square master; the runner crops the 16:9 desktop and the
9:16 phone versions from it, so the pair always shares one composition.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RecipeError, RunContext, run  # noqa: E402
from core.images import process  # noqa: E402

DATA = json.loads((HERE / "themes.json").read_text(encoding="utf-8"))
THEMES = {t["slug"]: t for t in DATA["themes"]}
PER_RUN = 3


def prepare(ctx: RunContext) -> dict[str, str]:
    rng = random.Random(ctx.day.toordinal())  # same date, same plan: dry runs match real runs
    last = set(ctx.existing[-1].fields.get("themes") or []) if ctx.existing else set()
    pool = [s for s in THEMES if s not in last] or list(THEMES)
    picks = rng.sample(pool, min(PER_RUN, len(pool)))
    plan = []
    for slug in picks:
        t = THEMES[slug]
        v = {axis: rng.choice(opts) for axis, opts in DATA["variation_axes"].items()}
        plan.append({"slug": slug, "file": f"{slug}.png", "theme": t,
                     "variation": f"{v['light']}, in {v['palette']}. Overall mood {v['mood']}, "
                                  f"composed with {v['framing']}."})
    ctx.state["plan"] = plan
    lines = []
    for i, p in enumerate(plan, 1):
        t = p["theme"]
        lines.append(f"{i}. **{t['label']}** — file `{p['file']}` · {t['style']} · {', '.join(t['categories'])}\n"
                     f"   - Scene: {t['scene']}\n   - Variation: {p['variation']}")
    return {"PLAN": "\n".join(lines), "THEME_SLUGS": json.dumps(picks)}


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    want = [p["file"] for p in ctx.state["plan"]]
    got = [i.get("file") for i in manifest.get("images") or [] if isinstance(i, dict)]
    if got != want:
        raise RecipeError(f"images must be exactly {want}, in that order; got {got}")
    if manifest.get("themes") != [p["slug"] for p in ctx.state["plan"]]:
        raise RecipeError("`themes` must echo the planned theme slugs in order")


def crop_pairs(ctx: RunContext, staging: Path, manifest: dict[str, object]) -> list[str]:
    """Desktop 16:9 and phone 9:16 crops from each square master; the first desktop is the cover."""
    out = []
    for p in ctx.state["plan"]:
        master = staging / "masters" / p["file"]
        for folder, aspect in (("desktop", "16:9"), ("mobile", "9:16")):
            process.crop_to_aspect(master, staging / folder / p["file"], aspect)
            out.append(f"{folder}/{p['file']}")
    return [*out, process.use_as_cover(staging, f"desktop/{ctx.state['plan'][0]['file']}")]


RECIPE = Recipe(
    name="wallpaper-packs",
    collection="wallpaper-packs",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("pack.md",),
    skills=("image-prompt-craft",),
    fields=("themes",),
    cover_aspect=None,
    # 4K square masters (Gemini) crop to ~4096x2304 desktop and ~2304x4096 phone. OpenAI has no
    # size tier and renders ~1024 px, so its crops are preview-grade.
    images=ImageSpec(min=PER_RUN, max=PER_RUN, aspects=("1:1",), folder="masters", size="4K"),
    default_model="sonnet",
    prepare=prepare,
    validate=validate,
    after_cover=crop_pairs,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
