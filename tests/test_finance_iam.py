"""Tests for iam-prototype and finance-digest, and the news-digest iam-security topic: their checks,
rotation and prepare hooks, with the feeds faked."""

from __future__ import annotations

import os

os.environ.setdefault("RECIPES_BROWSER_CHECK", "off")

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import RecipeError, artifacts, digest, runner  # noqa: E402


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"recipe_{name}", ROOT / "recipes" / name / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def feed_items(n: int, source: str, days_old: int) -> list[dict]:
    when = (datetime.now(timezone.utc) - timedelta(days=days_old)).strftime("%a, %d %b %Y %H:%M:%S +0000")
    return [{"title": f"{source} story {i}", "url": f"https://{source}.example/{i}", "source": source,
             "description": "d", "published": when} for i in range(n)]


def links(n: int) -> str:
    return "\n".join(f"- [Source {i}](https://src.example/{i})" for i in range(n))


def finance_digest(sections: list[str], *, disclaimer: bool = True, last: bool = True, n_links: int = 8,
                   paper: bool = False, risk: bool = True) -> str:
    body = "---\ntitle: t\ntopic: x\n---\n\n# Digest\n\n"
    if paper:
        body += "Paper only: study ideas, not orders.\n\n"
    for s in sections:
        if s in ("Dividend Ideas", "Growth Ideas", "ETF Ideas"):
            col = "Risk" if risk else "Note"
            body += f"## {s}\n\n| Ticker | Yield | {col} |\n|---|---|---|\n| AAA | 3% | rate shock |\n\n"
        else:
            body += f"## {s}\n\nSome text.\n\n"
    body += "## Sources\n\n" + links(n_links) + "\n\n"
    if disclaimer:
        nfa = "## Not Financial Advice\n\n" + load("finance-digest").DISCLAIMER + "\n"
        body = (body + nfa) if last else (nfa + "\n" + body)
    return body


class IamPrototypeTests(unittest.TestCase):
    def test_rotation_and_override(self):
        mod = load("iam-prototype")
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace(area=None))
        self.assertEqual(mod.prepare(ctx)["AREA"], "aggregation")  # first option on an empty catalogue
        used = [artifacts.Existing(title="t", slug="s", date="2026-10-01", summary="x", fields={"iam_area": a})
                for a in list(mod.AREAS)[:-1]]
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), used, argparse.Namespace(area=None))
        self.assertEqual(mod.prepare(ctx)["AREA"], "end-user")
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), used, argparse.Namespace(area="roles"))
        self.assertIn("role", mod.prepare(ctx)["AREA_GUIDE"].lower())

    def test_vendor_neutral_and_web_checks(self):
        mod = load("iam-prototype")
        text = (ROOT / "recipes/iam-prototype/prompt.md").read_text(encoding="utf-8").lower()
        for word in ("sailpoint", "identityiq", "okta", "entra"):
            self.assertNotIn(word, text)
        self.assertEqual(mod.RECIPE.fields, ("iam_area",))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "sample-data.json").write_text("{not json", encoding="utf-8")
            (p / "index.html").write_text("<html></html>", encoding="utf-8")
            (p / "script.js").write_text("", encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, {})


class FinanceDigestTests(unittest.TestCase):
    def test_topics_shape(self):
        mod = load("finance-digest")
        self.assertEqual(len(mod.TOPICS), 8)
        for key, spec in mod.TOPICS.items():
            for field in ("name", "emoji", "kind", "focus", "sections", "min_sections", "rules", "palette", "motif", "feeds"):
                self.assertIn(field, spec, f"{key} lacks {field}")
            self.assertLessEqual(spec["min_sections"], len(spec["sections"]))
            self.assertTrue(all(u.startswith("https://") for u in spec["feeds"]), key)
        self.assertTrue(mod.TOPICS["cashback-leaderboard"]["stores"])
        self.assertEqual(mod.TOPICS["cashback-leaderboard"]["feeds"], [])

    def test_prepare_feeds_and_leaderboard(self):
        mod = load("finance-digest")
        payload = {"candidates": feed_items(4, "tpg", 1), "feeds_ok": ["https://tpg.example/feed"], "feeds_failed": []}
        with mock.patch.object(mod, "fetch_candidates", return_value=payload) as fc:
            ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [],
                                    argparse.Namespace(topic="card-bonuses", days=7))
            tokens = mod.prepare(ctx)
            self.assertEqual(fc.call_count, 1)
            self.assertIn("tpg story 0", tokens["CANDIDATES"])
            self.assertIn("Top Picks This Week", tokens["SECTIONS"])
            self.assertEqual(tokens["WINDOW"], "2026-10-07 to 2026-10-14")
            self.assertEqual(ctx.state["topic"], "card-bonuses")
            ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [],
                                    argparse.Namespace(topic="cashback-leaderboard", days=7))
            tokens = mod.prepare(ctx)
            self.assertEqual(fc.call_count, 1)  # no feeds, no fetch
            self.assertIn("cashback-store/walmart/", tokens["STORES"])
        empty = {"candidates": [], "feeds_ok": [], "feeds_failed": ["https://x: URLError"]}
        with mock.patch.object(mod, "fetch_candidates", return_value=empty):
            ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [],
                                    argparse.Namespace(topic="stock-market", days=7))
            with self.assertRaises(RecipeError):
                mod.prepare(ctx)
        existing = [artifacts.Existing(title="t", slug="card-bonuses", date="2026-10-01", summary="s",
                                       fields={"topic": "card-bonuses"})]
        with mock.patch.object(mod, "fetch_candidates", return_value=payload):
            ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), existing,
                                    argparse.Namespace(topic=None, days=7))
            self.assertEqual(mod.prepare(ctx)["TOPIC"], "cashback-leaderboard")  # alphabetical least-used

    def test_validate_shape(self):
        mod = load("finance-digest")
        rewards = mod.TOPICS["chase-rewards"]["sections"][:3]
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace())
        ctx.state["topic"] = "chase-rewards"
        good = {"topic": "chase-rewards", "story_count": 8}
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            d = p / "digest.md"
            d.write_text(finance_digest(rewards), encoding="utf-8")
            mod.validate(p, good, ctx)
            for bad in (finance_digest(rewards, disclaimer=False), finance_digest(rewards, last=False),
                        finance_digest(rewards, n_links=3), finance_digest(rewards[:1])):
                d.write_text(bad, encoding="utf-8")
                with self.assertRaises(RecipeError):
                    mod.validate(p, good, ctx)
            d.write_text(finance_digest(rewards), encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, {"topic": "card-bonuses", "story_count": 8}, ctx)
            with self.assertRaises(RecipeError):
                mod.validate(p, {"topic": "chase-rewards", "story_count": "eight"}, ctx)

    def test_trade_ideas_paper_and_risk(self):
        mod = load("finance-digest")
        ideas = mod.TOPICS["trade-ideas"]["sections"][:5]
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace())
        ctx.state["topic"] = "trade-ideas"
        good = {"topic": "trade-ideas", "story_count": 8}
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            d = p / "digest.md"
            d.write_text(finance_digest(ideas, paper=True), encoding="utf-8")
            mod.validate(p, good, ctx)
            d.write_text(finance_digest(ideas, paper=False), encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, good, ctx)
            d.write_text(finance_digest(ideas, paper=True, risk=False), encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, good, ctx)


class SharedWindowAndIamTopicTests(unittest.TestCase):
    def test_window_items_lives_in_core(self):
        items = feed_items(30, "loud", 1) + feed_items(3, "quiet", 2) + feed_items(5, "old", 30)
        kept = digest.window_items(items, 7, per_source_cap=5, global_cap=100)
        self.assertEqual(sum(1 for i in kept if i["source"] == "loud"), 5)
        self.assertFalse(any(i["source"] == "old" for i in kept))
        self.assertIs(load("news-digest").window_items, digest.window_items)

    def test_iam_security_topic(self):
        topics = json.loads((ROOT / "recipes/news-digest/topics.json").read_text(encoding="utf-8"))
        self.assertEqual(len(topics), 10)
        spec = topics["iam-security"]
        reference = topics["ai"]
        self.assertEqual(set(spec), set(reference))
        self.assertEqual(len(spec["sections"]), 5)
        self.assertEqual(len(spec["feeds"]), 6)
        self.assertTrue(all(u.startswith("https://") for u in spec["feeds"]))


if __name__ == "__main__":
    unittest.main()
