#!/usr/bin/env python3
"""Weekly Browser Extension — a loadable Manifest V3 extension plus a mock-browser demo, weekly.

    python recipes/weekly-browser-extension/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import existing_digest, load_existing  # noqa: E402
from core.web import check_json, check_mv3, check_refs, node_check  # noqa: E402


def prepare(ctx: RunContext) -> dict[str, str]:
    return {"SIBLING_EXISTING": existing_digest(load_existing(ctx.output_dir / "app-prototypes"))}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    check_mv3(staging)
    check_json(staging, "sample-data.json")
    check_refs(staging, "index.html")
    node_check(staging, pages=("index.html",), scripts=("script.js",))


RECIPE = Recipe(
    name="weekly-browser-extension",
    collection="browser-extensions",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=(
        "README.md", "requirements.md", "index.html", "style.css", "script.js", "sample-data.json",
        "extension/manifest.json", "extension/popup.html", "extension/popup.css",
        "extension/popup.js", "extension/content.js",
    ),
    optional_files=("extension/background.js",),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("browser_surface", "monetization"),
    cover_aspect="16:9",
    default_model="opus",
    timeout_s=3600,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
