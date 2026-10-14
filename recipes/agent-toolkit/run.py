#!/usr/bin/env python3
"""Agent Toolkit — 24+ skills, commands, MCP servers, plugins and harnesses to install into an agent.

    python recipes/agent-toolkit/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.digest import digest_recipe  # noqa: E402

from core import run  # noqa: E402


RECIPE = digest_recipe(
    name="agent-toolkit",
    collection="agent-toolkit",
    archive_title="Agent Toolkit — Full Archive",
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
