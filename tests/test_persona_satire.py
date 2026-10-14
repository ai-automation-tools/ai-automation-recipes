"""Tests for agent-persona (known figures) and satirical-news: their checks and rotation hooks."""

from __future__ import annotations

import os

os.environ.setdefault("RECIPES_BROWSER_CHECK", "off")

import argparse
import importlib.util
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import RecipeError, artifacts, runner  # noqa: E402


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"recipe_{name}", ROOT / "recipes" / name / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ctx(existing=(), **args) -> runner.RunContext:
    ns = argparse.Namespace(**{"subcategory": None, "figure": None, "beat": None, "topic": None, **args})
    return runner.RunContext(Path("."), Path("."), date(2026, 10, 14), list(existing), ns)


def ex(slug: str, **fields) -> artifacts.Existing:
    return artifacts.Existing(title=slug, slug=slug, date="2026-10-01", summary="", fields=fields)


CARD = """---
title: "Gordon Ramsay"
slug: gordon-ramsay
tags:
- chef
- combative
- food
category: Debaters
subcategory: Celebrity
date: 2026-10-14
type: agent-persona
real_or_fictional: real
---

# Gordon Ramsay

## Purpose
A Michelin-starred chef who treats every argument like a failing kitchen on a Friday night.

## Persona
You are Gordon Ramsay. You have run kitchens for thirty years and nothing you hear in a debate is
worse than what you've seen on a pass.

- **Voice:** clipped, loud, profane.

## Example lines
- "It's RAW."

## Stay in character
Never break character.
"""


class PersonaTests(unittest.TestCase):
    def check(self, text: str, manifest: dict | None = None, existing=()) -> None:
        mod = load("agent-persona")
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "persona.md").write_text(text, encoding="utf-8")
            mod.validate(Path(tmp), manifest or {"slug": "gordon-ramsay", "real_or_fictional": "real"}, ctx(existing))

    def test_good_card_passes(self):
        self.check(CARD)

    def test_contract_breaks_rejected(self):
        with self.assertRaises(RecipeError):
            self.check("\n" + CARD)  # frontmatter not at byte 0
        with self.assertRaises(RecipeError):
            self.check(CARD.replace("real_or_fictional: real\n", ""))
        with self.assertRaises(RecipeError):
            self.check(CARD, {"slug": "gordon-ramsay", "real_or_fictional": "sorta"})
        with self.assertRaises(RecipeError):
            self.check(CARD.replace("You are Gordon Ramsay.", "He is Gordon Ramsay."))

    def test_existing_slug_rejected(self):
        with self.assertRaises(RecipeError):
            self.check(CARD, existing=[ex("gordon-ramsay", subcategory="Celebrity")])
        self.check(CARD, existing=[ex("rick-sanchez", subcategory="Fictional")])

    def test_rotation_and_figure_flag(self):
        mod = load("agent-persona")
        used = [ex(f"p{i}", subcategory=s) for i, s in enumerate(sorted(mod.SUBCATEGORIES)) if s != "Sports"]
        self.assertEqual(mod.prepare(ctx(used))["SUBCATEGORY"], "Sports")
        tokens = mod.prepare(ctx(figure="rick-sanchez", subcategory="Fictional"))
        self.assertIn("rick-sanchez", tokens["FIGURE"])
        self.assertEqual(tokens["SUBCATEGORY"], "Fictional")


ARTICLE_HEAD = """---
title: "Area Man Declares Weather Illegal"
slug: area-man-weather-illegal
date: 2026-10-14
type: satirical-news
publication: The Overcorrect
news_category: "Local / Area Man"
dateline: "DULUTH, MN"
byline: "The Overcorrect Staff"
based_on_true_event: false
tags: [satirical-news, satire, the-overcorrect, local-area-man]
---

# Area Man Declares Weather Illegal

**DULUTH, MN** — Local resident Gary Pelletier announced Tuesday that weather is now against the law.

![Gary at the podium](cover.png)

"""
PARA = "The ordinance, which Pelletier wrote on the back of a receipt, bans precipitation of every kind. " * 4
ARTICLE = ARTICLE_HEAD + "\n\n".join([PARA] * 6) + "\n\n![Sign](images/supporting-1.png)\n\nAt press time, it was raining.\n"
META = """---
title: "Area Man Declares Weather Illegal"
---

# Area Man Declares Weather Illegal

## Key Points

- Weather is illegal now
- The receipt is binding
- It is raining

## Summary

A man bans rain. The rain does not comply.
"""


class SatiricalNewsTests(unittest.TestCase):
    def check(self, article: str, meta: str = META, manifest: dict | None = None) -> None:
        mod = load("satirical-news")
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "article.md").write_text(article, encoding="utf-8")
            (Path(tmp) / "metadata.md").write_text(meta, encoding="utf-8")
            mod.validate(Path(tmp), manifest or {"beat": "Local / Area Man", "based_on_true_event": False})

    def test_good_article_passes(self):
        self.check(ARTICLE)

    def test_word_count_bounds(self):
        mod = load("satirical-news")
        n = mod.body_words(ARTICLE)
        self.assertTrue(350 <= n <= 650, n)
        with self.assertRaises(RecipeError):
            self.check(ARTICLE_HEAD + "Too short.\n")
        with self.assertRaises(RecipeError):
            self.check(ARTICLE_HEAD + "\n\n".join([PARA] * 12))

    def test_frontmatter_rules(self):
        with self.assertRaises(RecipeError):
            self.check(ARTICLE.replace('news_category: "Local / Area Man"', 'news_category: "Gossip"'))
        with self.assertRaises(RecipeError):
            self.check(ARTICLE, manifest={"beat": "Sports", "based_on_true_event": False})
        with self.assertRaises(RecipeError):  # true event without a source URL
            self.check(ARTICLE.replace("based_on_true_event: false", "based_on_true_event: true"))
        self.check(ARTICLE.replace("based_on_true_event: false",
                                   'based_on_true_event: true\ninspired_by: "https://example.com/story"'))
        with self.assertRaises(RecipeError):
            self.check(ARTICLE.replace("**DULUTH, MN** — ", ""))

    def test_metadata_rules(self):
        with self.assertRaises(RecipeError):
            self.check(ARTICLE, META.replace("- It is raining\n", ""))
        with self.assertRaises(RecipeError):
            self.check(ARTICLE, META.replace("## Summary", "## Blurb"))

    def test_rotation_and_topic_flag(self):
        mod = load("satirical-news")
        used = [ex(f"a{i}", beat=b) for i, b in enumerate(mod.BEATS) if b != "Sports"]
        self.assertEqual(mod.prepare(ctx(used))["BEAT"], "Sports")
        self.assertIn("hoa bans weather", mod.prepare(ctx(topic="hoa bans weather"))["TOPIC"])


if __name__ == "__main__":
    unittest.main()
