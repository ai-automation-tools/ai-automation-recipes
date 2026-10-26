"""Pins the links the static homepage in homepage/ must carry.

    python -m unittest discover -s tests
"""

from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent / "homepage"
REPO = "https://github.com/ai-automation-tools/ai-automation-recipes"

# Elements whose end tag is never optional: one opened and not closed (or closed out of order)
# means an edit cut the page. Optional-end tags like <p> and <li> are left to the browser.
STRUCTURAL = {"html", "head", "body", "main", "header", "footer", "nav", "section", "article",
              "aside", "div", "figure", "figcaption", "ul", "ol", "table", "pre", "a", "span",
              "button", "script", "style", "iframe", "details", "summary", "h1", "h2", "h3"}


class _Structure(HTMLParser):
    """Records the problems a botched splice leaves: a mangled tag name, a structural
    element left open, or a close tag with nothing open to match it."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.ids: set[str] = set()
        self.problems: list[str] = []

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", tag):
            self.problems.append(f"line {line}: mangled tag <{tag}")
        if (i := dict(attrs).get("id")):
            self.ids.add(i)
        if tag in STRUCTURAL:
            self.stack.append((tag, line))

    def handle_endtag(self, tag):
        if tag not in STRUCTURAL:
            return
        if not self.stack or self.stack[-1][0] != tag:
            opened = f"<{self.stack[-1][0]}> from line {self.stack[-1][1]}" if self.stack else "nothing"
            self.problems.append(f"line {self.getpos()[0]}: </{tag}> closes {opened}")
            if any(t == tag for t, _ in self.stack):   # resync so one cut reports once
                while self.stack and self.stack.pop()[0] != tag:
                    pass
            return
        self.stack.pop()


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

    def test_markup_is_whole(self):
        """The 2026-10-19 diagram splice cut <section id="how"> to `<s<!--` and left the old
        ASCII flow's tail in the page; nothing failed until the live site checks a week later."""
        html = (HOME / "index.html").read_text(encoding="utf-8")
        p = _Structure()
        p.feed(html)
        p.close()
        problems = p.problems + [f"<{t}> opened on line {n} is never closed" for t, n in p.stack]
        self.assertEqual(problems, [], "homepage/index.html markup is broken")
        for target in sorted(set(re.findall(r'href="#([^"]+)"', html))):
            self.assertIn(target, p.ids, f'href="#{target}" has no element with id="{target}"')

    def test_pages_files(self):
        self.assertEqual((HOME / "CNAME").read_text(encoding="utf-8").strip(),
                         "ai-automation-recipes.ai-automation-tools.dev")
        self.assertTrue((HOME / ".nojekyll").is_file())
        self.assertIn("<svg", (HOME / "favicon.svg").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
