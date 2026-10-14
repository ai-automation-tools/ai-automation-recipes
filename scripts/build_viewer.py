#!/usr/bin/env python3
"""Build a browsable viewer for a recipes output folder.

Reads every `artifact.json` under the folder and writes two files into it:

    index.html   the viewer page (copied from viewer/index.html)
    catalog.js   window.CATALOG = {...}: every artifact, its media and its markdown pre-rendered

Open index.html straight from disk, or serve the folder from any static host. Re-run after new
artifacts land (or schedule it after your recipes).

    python scripts/build_viewer.py --output-dir ~/ai-output [--title "My AI Library"]

Markdown is rendered with the `markdown` package. Raw HTML inside it is escaped first, because the
documents are model-written: a stray <script> in a story should show as text, not run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from core.artifacts import MANIFEST  # noqa: E402

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".ogg"}
VIDEO_EXT = {".mp4", ".webm"}
GALLERY_MAX = 60
DOC_MAX_CHARS = 200_000
FRONTMATTER = re.compile(r"\A﻿?---\r?\n.*?\r?\n---\r?\n", re.S)
RAW_TAG = re.compile(r"<(?!https?://|mailto:)(?=[A-Za-z/!?])")


def groups() -> list[dict]:
    """Sidebar groups from the registry's category packs, keyed by collection."""
    try:
        import build_registry as b
    except ImportError:
        return []
    out = []
    for _, name, _, members in b.CATEGORY_PACKS:
        cols = []
        for recipe in members:
            col = _collection_of(recipe)
            if col and col not in {c["id"] for c in cols}:
                cols.append({"id": col, "label": col.replace("-", " ").title()})
        out.append({"name": name.split(": ", 1)[-1], "collections": cols})
    return out


def _collection_of(recipe: str) -> str | None:
    text = (ROOT / "recipes" / recipe / "run.py").read_text(encoding="utf-8") if (ROOT / "recipes" / recipe / "run.py").is_file() else ""
    m = re.search(r'collection\s*=\s*"([^"]+)"', text)
    return m.group(1) if m else None


def render_markdown(text: str) -> str:
    import markdown

    text = FRONTMATTER.sub("", text, count=1)
    text = RAW_TAG.sub("&lt;", text)
    return markdown.markdown(text[:DOC_MAX_CHARS], extensions=["tables", "fenced_code", "sane_lists"])


def item(folder: Path, out_dir: Path) -> dict | None:
    try:
        a = json.loads((folder / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    rel = folder.relative_to(out_dir).as_posix()
    files = sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*")
                   if p.is_file() and p.name != MANIFEST and not any(part.startswith(".") for part in p.parts))
    declared = a.get("files") or {}
    main = declared.get("main") if isinstance(declared.get("main"), str) else None
    cover = "cover.png" if "cover.png" in files else None

    html = None
    if main and main.endswith(".html"):
        html = main
    elif "index.html" in files:
        html = "index.html"
    elif "pitch.html" in files:
        html = "pitch.html"

    gallery = [f for f in files if Path(f).suffix.lower() in IMAGE_EXT and f != cover]
    # Prefer the rendered PNGs over their SVG sources when a pack ships both.
    if any(f.startswith("png/") for f in gallery):
        gallery = [f for f in gallery if not f.startswith("svg/")]
    gallery = gallery[:GALLERY_MAX]

    docs = []
    md_files = [main] if main and main.endswith(".md") else []
    md_files += [f for f in files if f.endswith(".md") and f not in md_files and "/" not in f]
    for name in md_files[:4]:
        try:
            docs.append({"name": name, "html": render_markdown((folder / name).read_text(encoding="utf-8"))})
        except (OSError, UnicodeDecodeError, ImportError):
            continue

    def link(f: str) -> str:
        return f"{rel}/{f}"

    thumb = cover or (gallery[0] if gallery else None)
    return {
        "id": rel,
        "folder": rel,
        "collection": a.get("collection") or folder.parts[-3],
        "recipe": a.get("recipe", ""),
        "title": a.get("title") or folder.name,
        "summary": a.get("summary", ""),
        "date": a.get("date", ""),
        "fields": a.get("fields") or {},
        "thumb": link(thumb) if thumb else None,
        "cover": link(cover) if cover else None,
        "html": link(html) if html else None,
        "gallery": [link(g) for g in gallery],
        # Other top-level pages (a Cook's Card, an extension demo) get their own button.
        "pages": [link(f) for f in files if f.endswith(".html") and "/" not in f and f != html],
        "audio": [link(f) for f in files if Path(f).suffix.lower() in AUDIO_EXT],
        "video": [link(f) for f in files if Path(f).suffix.lower() in VIDEO_EXT],
        "docs": docs,
        "files": [link(f) for f in files],
    }


def build(out_dir: Path, title: str) -> int:
    items = []
    for manifest in out_dir.glob(f"*/*/*/{MANIFEST}"):
        if any(part.startswith(".") for part in manifest.relative_to(out_dir).parts):
            continue  # staging folders
        it = item(manifest.parent, out_dir)
        if it:
            items.append(it)
    items.sort(key=lambda i: (i["date"], i["id"]), reverse=True)

    known = groups()
    seen = {c["id"] for g in known for c in g["collections"]}
    extra = sorted({i["collection"] for i in items} - seen)
    if extra:
        known.append({"name": "Other", "collections": [{"id": c, "label": c.replace("-", " ").title()} for c in extra]})

    catalog = {"title": title, "generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "groups": known, "items": items}
    # </script>-safe: catalog.js is loaded as a script, so never let a string close the tag.
    payload = json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/")
    (out_dir / "catalog.js").write_text(f"window.CATALOG = {payload};\n", encoding="utf-8")
    shutil.copyfile(ROOT / "viewer" / "index.html", out_dir / "index.html")
    return len(items)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--output-dir", default=os.environ.get("RECIPES_OUTPUT_DIR"), help="The recipes output folder.")
    ap.add_argument("--title", default="AI Recipes", help="Shown in the viewer's header and tab.")
    args = ap.parse_args()
    if not args.output_dir:
        ap.error("--output-dir is required (or set RECIPES_OUTPUT_DIR)")
    out_dir = Path(args.output_dir).expanduser().resolve()
    n = build(out_dir, args.title)
    print(f"viewer: {n} artifacts -> {out_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
