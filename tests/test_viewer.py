"""Tests for scripts/build_viewer.py: the catalog it writes and what it refuses to let through.

    python -m unittest discover -s tests
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_viewer  # noqa: E402


def artifact(out: Path, collection: str, name: str, data: dict, files: dict[str, bytes | str]) -> Path:
    folder = out / collection / "2026-10" / name
    folder.mkdir(parents=True)
    for rel, body in files.items():
        p = folder / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(body) if isinstance(body, bytes) else p.write_text(body, encoding="utf-8")
    (folder / "artifact.json").write_text(json.dumps({"collection": collection, **data}), encoding="utf-8")
    return folder


def load_catalog(out: Path) -> dict:
    text = (out / "catalog.js").read_text(encoding="utf-8")
    assert text.startswith("window.CATALOG = ") and text.rstrip().endswith(";")
    return json.loads(text[len("window.CATALOG = "):].rstrip().rstrip(";").replace("<\\/", "</"))


class BuildViewerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_catalog_classifies_media(self):
        artifact(self.out, "browser-games", "2026-10-14_g", {"title": "G", "summary": "s", "date": "2026-10-14",
                 "files": {"main": "index.html"}}, {"index.html": "<p>", "game-design-brief.md": "# Brief", "cover.png": b"x"})
        artifact(self.out, "songs", "2026-10-13_s", {"title": "S", "summary": "s", "date": "2026-10-13",
                 "files": {"main": "song.md"}}, {"song.md": "---\ntitle: S\n---\n# S\n\nla", "song.mp3": b"ID3"})
        artifact(self.out, "icon-packs", "2026-10-12_i", {"title": "I", "summary": "s", "date": "2026-10-12",
                 "files": {"main": "pack.md"}}, {"pack.md": "# I", "svg/a.svg": "<svg/>", "png/a.png": b"x"})
        artifact(self.out, "recipes", "2026-10-11_r", {"title": "R", "summary": "s", "date": "2026-10-11",
                 "files": {"main": "recipe.md"}}, {"recipe.md": "# R", "cooks-card.html": "<p>"})
        (self.out / "songs" / ".staging" / "x" / "y").mkdir(parents=True)  # never catalogued

        self.assertEqual(build_viewer.build(self.out, "T"), 4)
        self.assertTrue((self.out / "index.html").is_file())
        items = {i["collection"]: i for i in load_catalog(self.out)["items"]}
        self.assertEqual([i["date"] for i in load_catalog(self.out)["items"]],
                         ["2026-10-14", "2026-10-13", "2026-10-12", "2026-10-11"])  # newest first
        self.assertTrue(items["browser-games"]["html"].endswith("/index.html"))
        self.assertTrue(items["browser-games"]["thumb"].endswith("/cover.png"))
        self.assertEqual(len(items["songs"]["audio"]), 1)
        self.assertNotIn("<p>title: S", items["songs"]["docs"][0]["html"])  # frontmatter stripped
        self.assertEqual([g.split("/")[-2] for g in items["icon-packs"]["gallery"]], ["png"])  # PNG over SVG
        self.assertTrue(items["recipes"]["pages"][0].endswith("/cooks-card.html"))

    def test_model_written_html_is_escaped(self):
        hostile = "# T\n\n<script>alert(1)</script>\n\n<img src=x onerror=alert(1)>\n\nSee <https://example.com>.\n"
        artifact(self.out, "short-stories", "2026-10-14_t", {"title": "</script><script>alert(2)</script>",
                 "summary": "s", "date": "2026-10-14", "files": {"main": "story.md"}}, {"story.md": hostile})
        build_viewer.build(self.out, "T")
        raw = (self.out / "catalog.js").read_text(encoding="utf-8")
        self.assertNotIn("</script>", raw)  # can't close the <script> tag that loads the catalog
        doc = load_catalog(self.out)["items"][0]["docs"][0]["html"]
        self.assertNotIn("<script>", doc)
        self.assertNotIn("<img", doc)
        self.assertIn('href="https://example.com"', doc)  # autolinks still work

    def test_empty_folder(self):
        self.assertEqual(build_viewer.build(self.out, "T"), 0)
        self.assertEqual(load_catalog(self.out)["items"], [])


if __name__ == "__main__":
    unittest.main()
