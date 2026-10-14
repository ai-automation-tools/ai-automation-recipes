#!/usr/bin/env python3
"""AI Stack Radar — a radar of hosted AI products, each with what it replaces and costs.

    python recipes/ai-stack-radar/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.digest import digest_recipe  # noqa: E402

from core import run  # noqa: E402

log = logging.getLogger("recipes")


def validate_extra(staging, manifest, cats) -> None:
    # The scope rule is "no bare repos" — flag drift without failing a good run over one link.
    repos = [e["url"] for es in cats.values() for e in es if "github.com/" in e["url"]]
    if repos:
        log.warning("ai-stack-radar lists %d GitHub link(s) — the prompt bans repos: %s", len(repos), repos)


RECIPE = digest_recipe(
    name="ai-stack-radar",
    collection="ai-stack-radar",
    archive_title="AI Stack Radar — Full Archive",
    validate_extra=validate_extra,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
