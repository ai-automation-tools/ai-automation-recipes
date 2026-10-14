#!/usr/bin/env python3
"""Model Benchmark Watch — the week's AI model releases and a sourced head-to-head table.

    python recipes/model-benchmark-watch/run.py --output-dir ~/ai-output

Not a link-list digest: the artifact is a briefing whose centre is a comparison table of the
current frontier, every number traced to a cited source. The previous edition's table and
movement section are handed to the agent so each run leads with what changed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402

MAIN = "digest.md"
PREVIOUS_CHARS = 7000
MIN_TABLE_ROWS = 5
MIN_SOURCES = 10
LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)")


def section(text: str, heading: str) -> str:
    """The body of the first `## <heading>…` section, or ''."""
    m = re.search(rf"^##\s+{re.escape(heading)}.*?$\n(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def table_rows(body: str) -> list[str]:
    rows = [l for l in body.splitlines() if l.strip().startswith("|")]
    return [r for r in rows[2:] if not re.match(r"^\s*\|[\s:|-]+\|\s*$", r)] if len(rows) >= 3 else []


def previous_edition(ctx: RunContext) -> str:
    runs = sorted(ctx.collection_dir.glob(f"*/*/{MAIN}"))
    if not runs:
        return "(none yet — this is the first edition; there is no movement to report, only the current state)"
    text = runs[-1].read_text(encoding="utf-8")
    keep = []
    for h in ("Head-to-Head", "Benchmark & Leaderboard Movement"):
        body = section(text, h)
        if body:
            keep.append(f"### Previous: {h}\n\n{body}")
    out = f"Previous edition: `{runs[-1].parent.name}`\n\n" + "\n\n".join(keep)
    return out[:PREVIOUS_CHARS] + ("\n\n… (trimmed)" if len(out) > PREVIOUS_CHARS else "")


def prepare(ctx: RunContext) -> dict[str, str]:
    return {"PREVIOUS": previous_edition(ctx)}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    text = (staging / MAIN).read_text(encoding="utf-8")
    for h in ("New & Updated Models", "Head-to-Head", "Benchmark & Leaderboard Movement", "Sources"):
        if not re.search(rf"^##\s+{re.escape(h)}", text, re.M):
            raise RecipeError(f"{MAIN} is missing the `## {h}` section")
    rows = table_rows(section(text, "Head-to-Head"))
    if len(rows) < MIN_TABLE_ROWS:
        raise RecipeError(f"the Head-to-Head table has {len(rows)} data rows; need at least {MIN_TABLE_ROWS}")
    sources = LINK_RE.findall(section(text, "Sources"))
    if len(set(sources)) < MIN_SOURCES:
        raise RecipeError(f"Sources lists {len(set(sources))} links; need at least {MIN_SOURCES}")
    if re.search(r"\b(approximately|roughly|around)\s+\d", section(text, "Head-to-Head")):
        raise RecipeError("the Head-to-Head table hedges a number; write the sourced figure or —")
    compared = manifest.get("compared")
    if not isinstance(compared, int) or compared != len(rows):
        raise RecipeError(f"final JSON `compared` must equal the table's row count ({len(rows)})")


RECIPE = Recipe(
    name="model-benchmark-watch",
    collection="model-benchmark-watch",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=(MAIN,),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("new_models", "compared"),
    cover_aspect="16:9",
    default_model="sonnet",
    timeout_s=2700,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
