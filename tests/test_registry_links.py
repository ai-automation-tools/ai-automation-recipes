"""Pins the "Import into Cronsole" block build_registry.py writes into each recipe README.

    python -m unittest discover -s tests
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

import build_bundle  # noqa: E402
import build_registry as br  # noqa: E402


class RegistryLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = br.build()
        index = br.json.loads(cls.files[br.OUT / "index.json"])
        cls.template_ids = {t["id"] for t in index["templates"]}
        cls.pack_ids = {p["id"] for p in index["packs"]}

    def test_every_recipe_links_only_to_what_the_catalog_has(self):
        readmes = {p: b.decode("utf-8") for p, b in self.files.items() if p.name == "README.md"}
        self.assertEqual(len(readmes), len(list(ROOT.glob("recipes/*/cronsole.json"))))
        for path, text in readmes.items():
            recipe = path.parent.name
            self.assertEqual(text.count(br.LINKS_START), 1, recipe)
            self.assertEqual(text.count(br.LINKS_END), 1, recipe)
            tids = set(re.findall(r"#/t/([\w-]+)\)", text))
            packs = set(re.findall(r"#/collection/([\w-]+)\)", text))
            self.assertIn(f"recipe-{recipe}", tids)
            self.assertLessEqual(tids, self.template_ids, recipe)
            self.assertLessEqual(packs, self.pack_ids, recipe)
            self.assertLess(text.index(br.LINKS_END), text.rindex("\n---\n"), f"{recipe}: block below the footer")

    def test_rebuilding_replaces_the_block_instead_of_adding_one(self):
        text = "# X\n\nBody.\n\n---\n\n<p align=\"center\">nav</p>\n"
        once = br.with_links(text, br.links_block("short-story", "ai-recipes-writing", "AI Recipes: Writing"))
        self.assertEqual(once, br.with_links(once, br.links_block("short-story", "ai-recipes-writing", "AI Recipes: Writing")))

    def test_readmes_stay_out_of_the_runtime_bundle(self):
        self.assertFalse([f for f in build_bundle.files() if f.startswith("recipes/") and f.endswith("README.md")])
        self.assertTrue([f for f in build_bundle.files() if f.endswith("/themes.md")], "recipe data .md must stay in")


if __name__ == "__main__":
    unittest.main()
