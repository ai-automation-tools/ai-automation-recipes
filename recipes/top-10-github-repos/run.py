#!/usr/bin/env python3
"""Top 10 GitHub Repos — the ten strongest trending AI / developer-tooling repos, ranked.

prepare() pulls GitHub Trending's weekly feeds and keyword-filters them to AI and dev
tooling; the agent picks and ranks ten from that list rather than searching for them.

    python recipes/top-10-github-repos/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.digest import candidates_block, digest_recipe, fetch_candidates  # noqa: E402

from core import RecipeError, run  # noqa: E402

FEEDS = {
    "feeds": [
        f"https://mshibanami.github.io/GitHubTrendingRSS/weekly/{lang}.xml"
        for lang in ("all", "python", "typescript", "javascript", "rust", "go")
    ],
    "keywords": [
        "ai", "llm", "llms", "gpt", "claude", "gemini", "anthropic", "openai",
        "agent", "agents", "agentic", "mcp", "rag", "embedding", "embeddings",
        "inference", "prompt", "prompts", "transformer", "diffusion", "ollama",
        "chatbot", "copilot", "vector", "finetune", "fine-tuning", "multimodal",
        "machine learning", "deep learning", "neural network", "language model",
        "developer tool", "developer tools", "code assistant", "coding agent",
        "model context protocol", "ai-powered", "ai agent", "llm app",
    ],
    "sort": "none",
    "limit": 40,
}
CATEGORIES = {"AI Agents", "AI Tools", "AI/ML", "MCP", "CLI", "Automations", "Integrations",
              "Developer Tools", "Open Source", "Data", "Security"}


def prepare_extra(ctx) -> dict[str, str]:
    return {"CANDIDATES": candidates_block(fetch_candidates(FEEDS))}


def validate_extra(staging: Path, manifest, cats) -> None:
    unknown = set(cats) - CATEGORIES - {"Repos"}
    if unknown:
        raise RecipeError(f"categories outside the closed list: {sorted(unknown)}")


RECIPE = digest_recipe(
    name="top-10-github-repos",
    collection="top-10-github-repos",
    archive_title="Top 10 GitHub Repos — Full Archive",
    prepare_extra=prepare_extra,
    validate_extra=validate_extra,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
