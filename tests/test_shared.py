"""Tests for the shared modules in core/: web checks, the food gate and Cook's Card, digests.

    python -m unittest discover -s tests
"""

from __future__ import annotations


import os

# Validators open a real browser when one is available; tests opt in explicitly (BrowserSmokeTests).
os.environ.setdefault("RECIPES_BROWSER_CHECK", "off")

import json
import unittest.mock
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import RecipeError, digest, food, web  # noqa: E402

RECIPE_MD = """---
title: "Test Stew"
yield: "4 servings"
active_time_min: 20
total_time_min: 90
allergens: ["gluten"]
---

# Test Stew

## Ingredients
- 1 lb beef chuck, cubed
- 1 cup milk
- 2 eggs
- 2 cups flour

## Instructions
1. Brown the beef to an internal temperature of 145°F.
2. Simmer for an hour.
"""


class WebTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_check_refs(self):
        (self.d / "a.css").write_text("", encoding="utf-8")
        (self.d / "p.html").write_text(
            '<link href="a.css"><img src="cover.png"><script src="https://x/y.js"></script>', encoding="utf-8")
        web.check_refs(self.d, "p.html", pending=("cover.png",))
        for kwargs in ({"allow_external_scripts": False}, {"https_prefixes": ("https://cdn/",)}):
            with self.assertRaises(RecipeError):
                web.check_refs(self.d, "p.html", pending=("cover.png",), **kwargs)
        (self.d / "q.html").write_text('<img src="missing.png">', encoding="utf-8")
        with self.assertRaises(RecipeError):
            web.check_refs(self.d, "q.html")

    def test_sources_csv(self):
        (self.d / "s.csv").write_text('title,url,note\na,https://a,n\nb,https://b,"x, y"\nc,https://c,n\n',
                                      encoding="utf-8")
        web.check_sources_csv(self.d, "s.csv")
        (self.d / "bad.csv").write_text("name,link\na,b\n", encoding="utf-8")
        with self.assertRaises(RecipeError):
            web.check_sources_csv(self.d, "bad.csv")

    def test_inline_script_regex_skips_data_blocks(self):
        html = ('<script>a()</script><script type="application/json">{"p": 1}</script>'
                "<script type='module'>b()</script><script src=\"x.js\"></script><SCRIPT defer>c()</SCRIPT>")
        self.assertEqual(web.INLINE_SCRIPT_RE.findall(html), ["a()", "b()", "c()"])

    def test_mv3(self):
        ext = self.d / "extension"
        ext.mkdir()
        (ext / "popup.html").write_text("<p>hi</p>", encoding="utf-8")
        (ext / "content.js").write_text("let a = 1;", encoding="utf-8")
        manifest = {"manifest_version": 3, "name": "T", "version": "1.0",
                    "action": {"default_popup": "popup.html"},
                    "content_scripts": [{"matches": ["https://example.com/*"], "js": ["content.js"]}]}
        (ext / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        web.check_mv3(self.d)

        (ext / "content.js").write_text("eval('1')", encoding="utf-8")
        with self.assertRaises(RecipeError):
            web.check_mv3(self.d)
        (ext / "content.js").write_text("let a = 1;", encoding="utf-8")

        manifest["manifest_version"] = 2
        (ext / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(RecipeError):
            web.check_mv3(self.d)


class FoodTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_gate_adds_undeclared_allergens(self):
        (self.d / "recipe.md").write_text(RECIPE_MD, encoding="utf-8")
        food.check_recipe(self.d, {})
        fm, _ = food.parse_frontmatter((self.d / "recipe.md").read_text(encoding="utf-8"))
        self.assertTrue({"dairy", "egg"} <= set(fm["allergens"]), fm["allergens"])

    def test_gate_rejects_critical_safety_issue(self):
        bad = RECIPE_MD.replace("2. Simmer for an hour.", "2. Reuse the marinade as a sauce without boiling it.")
        (self.d / "recipe.md").write_text(bad, encoding="utf-8")
        with self.assertRaises(RecipeError):
            food.check_recipe(self.d, {})

    def test_cooks_card(self):
        try:
            import markdown  # noqa: F401
        except ImportError:
            self.skipTest("markdown not installed")
        (self.d / "recipe.md").write_text(RECIPE_MD, encoding="utf-8")
        self.assertEqual(food.cooks_card(None, self.d, {}), [food.CARD])
        html = (self.d / food.CARD).read_text(encoding="utf-8")
        self.assertIn("Test Stew", html)
        self.assertIn("Ingredients", html)


class DigestTests(unittest.TestCase):
    def test_self_check(self):
        digest._self_check()


@unittest.skipUnless(shutil.which("node"), "node not installed")
class NodeCheckTests(unittest.TestCase):
    def test_node_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "p.html").write_text('<script type="application/json">{"a": 1}</script><script>let x = 1;</script>',
                                      encoding="utf-8")
            web.node_check(d, pages=("p.html",))
            (d / "bad.js").write_text("function (", encoding="utf-8")
            with self.assertRaises(RecipeError):
                web.node_check(d, scripts=("bad.js",))


if __name__ == "__main__":
    unittest.main()


def _browser_available() -> bool:
    try:
        from playwright.sync_api import Error, sync_playwright
    except ImportError:
        return False
    with sync_playwright() as p:
        for channel in (None, "chrome", "msedge"):
            try:
                (p.chromium.launch(channel=channel) if channel else p.chromium.launch()).close()
                return True
            except Error:
                continue
    return False


@unittest.skipUnless(_browser_available(), "no Playwright browser available")
class BrowserSmokeTests(unittest.TestCase):
    def test_catches_dead_pages_and_passes_live_ones(self):
        with tempfile.TemporaryDirectory() as tmp, unittest.mock.patch.dict("os.environ", {"RECIPES_BROWSER_CHECK": "on"}):
            d = Path(tmp)
            (d / "good.html").write_text("<canvas id=c></canvas><script>const c = document.getElementById('c');"
                                         "addEventListener('keydown', () => { c.width = 10; });</script>", encoding="utf-8")
            (d / "dead.html").write_text("<script>let canvas; canvas.addEventListener('click', () => {});"
                                         "addEventListener('load', () => { canvas = document.body; });</script>", encoding="utf-8")
            (d / "on-input.html").write_text("<script>addEventListener('keydown', () => { missing.go(); });</script>",
                                             encoding="utf-8")
            web.browser_smoke(d, "good.html", settle_ms=200)
            for bad in ("dead.html", "on-input.html"):
                with self.assertRaises(RecipeError):
                    web.browser_smoke(d, bad, settle_ms=200)


class DeliverTests(unittest.TestCase):
    ENTRY = {"recipe": "comics", "title": "T", "summary": "S", "date": "2026-10-14", "path": "comics/x", "files": {}}

    def test_payload_shapes(self):
        from core import deliver

        self.assertIn("content", deliver.payload_for("https://discord.com/api/webhooks/1/abc", self.ENTRY))
        self.assertIn("text", deliver.payload_for("https://hooks.slack.com/services/x", self.ENTRY))
        generic = deliver.payload_for("https://example.com/hook", self.ENTRY)
        self.assertEqual(generic["event"], "artifact.published")
        self.assertEqual(generic["title"], "T")

    def test_announce_is_best_effort(self):
        import urllib.error

        from core import deliver

        with unittest.mock.patch.dict("os.environ", {"RECIPES_WEBHOOK_URL": ""}):
            self.assertFalse(deliver.announce(self.ENTRY))
        with unittest.mock.patch.dict("os.environ", {"RECIPES_WEBHOOK_URL": "https://example.com/hook"}), \
                unittest.mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            self.assertFalse(deliver.announce(self.ENTRY))  # logged, never raised
