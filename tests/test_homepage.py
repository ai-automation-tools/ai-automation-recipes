"""Pins the links the static homepage in homepage/ must carry.

    python -m unittest discover -s tests
"""

from __future__ import annotations

import unittest
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent / "homepage"
REPO = "https://github.com/ai-automation-tools/ai-automation-recipes"


class HomepageTests(unittest.TestCase):
    def test_required_links(self):
        html = (HOME / "index.html").read_text(encoding="utf-8")
        for needle in (
            'href="https://ai-automation-recipes-demo.ai-automation-tools.dev/"',
            f'href="{REPO}"',
            'href="https://cronsole.ai-automation-tools.dev/"',
            'href="https://ai-automation-tools.dev/"',
            'href="https://ai-automation-tools.dev/cookies.html"',
            'data-ail-consent="manage"',
            'src="https://ai-automation-tools.dev/consent.js"',
            'rel="canonical" href="https://ai-automation-recipes.ai-automation-tools.dev/"',
            f'href="{REPO}/blob/main/docs/ROADMAP.md"',
            f'href="{REPO}/blob/main/docs/CHANGELOG.md"',
            'href="#start"',
        ):
            self.assertIn(needle, html)
        self.assertLess(html.index('class="src-bar"'), html.index('class="topbar"'))

    def test_pages_files(self):
        self.assertEqual((HOME / "CNAME").read_text(encoding="utf-8").strip(),
                         "ai-automation-recipes.ai-automation-tools.dev")
        self.assertTrue((HOME / ".nojekyll").is_file())
        self.assertIn("<svg", (HOME / "favicon.svg").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
