#!/usr/bin/env python3
"""Security Toolkit — 24+ security tools a month across identity, detection, recon, AppSec and labs.

    python recipes/security-toolkit/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_digest"))

from digest import digest_recipe  # noqa: E402

from core import run  # noqa: E402


RECIPE = digest_recipe(
    name="security-toolkit",
    collection="security-toolkit",
    archive_title="Security Toolkit — Full Archive",
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
