#!/usr/bin/env python3
"""Finance Toolkit — 22+ financial tools a month: data APIs, backtesting, broker SDKs, ledgers, finance AI.

    python recipes/finance-toolkit/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_digest"))

from digest import digest_recipe  # noqa: E402

from core import run  # noqa: E402


RECIPE = digest_recipe(
    name="finance-toolkit",
    collection="finance-toolkit",
    archive_title="Finance Toolkit — Full Archive",
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
