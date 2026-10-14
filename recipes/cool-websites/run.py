#!/usr/bin/env python3
"""Cool Websites — a roundup of 28+ genuinely useful, lesser-known websites by category.

    python recipes/cool-websites/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.digest import digest_recipe  # noqa: E402

from core import run  # noqa: E402


RECIPE = digest_recipe(
    name="cool-websites",
    collection="cool-websites",
    archive_title="Cool Websites — Full Archive",
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
