#!/usr/bin/env python3
"""Open-Source Spotlight — an editorial read on open source in six fixed sections.

prepare() pulls seven RSS/Atom sources (GitHub's blogs, GitHub Trending, TLDR Tech,
Hacker News, The Register, LWN) so each run is grounded in that period's actual news.

    python recipes/oss-spotlight/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.digest import candidates_block, digest_recipe, fetch_candidates  # noqa: E402

from core import RecipeError, run  # noqa: E402

FEEDS = {
    "feeds": [
        "https://github.blog/feed/",
        "https://github.blog/open-source/feed/",
        "https://mshibanami.github.io/GitHubTrendingRSS/weekly/all.xml",
        "https://tldr.tech/rss/tech.xml",
        "https://hnrss.org/frontpage",
        "https://www.theregister.com/software/headlines.atom",
        "https://lwn.net/headlines/rss",
    ],
    "keywords": [
        "open source", "open-source", "oss", "repo", "repository", "github", "gitlab",
        "release", "released", "releases", "v1.0", "v2.0", "beta", "rc",
        "cli", "library", "framework", "sdk", "toolkit", "package", "plugin",
        "compiler", "runtime", "kernel", "linux", "rust", "python", "typescript", "golang",
        "maintainer", "maintainers", "contributor", "fork", "license", "licence",
        "developer tool", "developer tools", "dev tool", "self-hosted", "self hosted",
        "database", "protocol", "api", "ai", "llm", "agent", "mcp",
    ],
    "match_chars": 500,
    "sort": "none",
    "limit": 50,
}
SECTIONS = ["Project of the Week", "Top 5 Trending Repos", "Notable New Releases",
            "Community & Ecosystem News", "Hidden Gems", "Developer Tooling Highlights"]


def prepare_extra(ctx) -> dict[str, str]:
    return {"CANDIDATES": candidates_block(fetch_candidates(FEEDS))}


def validate_extra(staging: Path, manifest, cats) -> None:
    unknown = set(cats) - set(SECTIONS)
    if unknown:
        raise RecipeError(f"sections outside the fixed six: {sorted(unknown)}")


RECIPE = digest_recipe(
    name="oss-spotlight",
    collection="oss-spotlight",
    archive_title="Open-Source Spotlight — Full Archive",
    prepare_extra=prepare_extra,
    validate_extra=validate_extra,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
