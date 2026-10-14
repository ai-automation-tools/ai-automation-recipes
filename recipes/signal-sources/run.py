#!/usr/bin/env python3
"""Signal Sources — a cumulative reading list; each run adds 12+ sources with verified feeds.

After publishing, the runner regenerates <collection>/all-bookmarks.html and
<collection>/feeds.opml (one-import feed bundle) from every run.

    python recipes/signal-sources/run.py --output-dir ~/ai-output
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.digest import digest_recipe, archive_size  # noqa: E402

from core import run  # noqa: E402


def prepare_extra(ctx) -> dict[str, str]:
    return {"ARCHIVE_SIZE": str(archive_size(ctx.collection_dir))}


RECIPE = digest_recipe(
    name="signal-sources",
    collection="signal-sources",
    archive_title="Signal Sources — Full Archive",
    prepare_extra=prepare_extra,
    opml_title="Signal Sources",
    fields=("site_count", "archive_total"),
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
