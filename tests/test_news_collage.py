"""news-collage: window math for day/week/month and the stories.md checks."""

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

from core import RecipeError, runner  # noqa: E402

spec = importlib.util.spec_from_file_location("recipe_news_collage", ROOT / "recipes" / "news-collage" / "run.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def story(i: int, caption: str = "Senate passes budget bill") -> str:
    return f"### Story {i}\nSummary {i}.\n**Source:** https://example.com/{i}\n**Caption:** \"{caption}\"\n\n"


def doc(n: int, caption: str = "Senate passes budget bill") -> str:
    return "---\ntitle: x\n---\n# x\n\nWindow: y\n\n" + "".join(story(i, caption) for i in range(1, n + 1))


class WindowTests(unittest.TestCase):
    def test_day(self):
        w = mod.window_for("day", date(2026, 10, 14))
        self.assertEqual((w["DATE_FROM"], w["DATE_TO"], w["STAMP"]), ("2026-10-13", "2026-10-13", "10/13/2026 11:59 PM"))
        self.assertEqual(w["ASPECT"], "2:3")

    def test_week_same_month_and_crossing_months(self):
        w = mod.window_for("week", date(2026, 10, 14))  # Wednesday → Mon 5 to Sun 11
        self.assertEqual((w["DATE_FROM"], w["DATE_TO"], w["STAMP"]), ("2026-10-05", "2026-10-11", "Oct 5-11, 2026"))
        self.assertEqual(w["ASPECT"], "3:2")
        w = mod.window_for("week", date(2026, 10, 5))  # Monday → Sep 28 to Oct 4
        self.assertEqual((w["DATE_FROM"], w["DATE_TO"], w["STAMP"]), ("2026-09-28", "2026-10-04", "Sep 28 - Oct 4, 2026"))

    def test_month_and_january(self):
        w = mod.window_for("month", date(2026, 10, 14))
        self.assertEqual((w["DATE_FROM"], w["DATE_TO"], w["STAMP"]), ("2026-09-01", "2026-09-30", "September 2026"))
        w = mod.window_for("month", date(2026, 1, 3))
        self.assertEqual((w["DATE_FROM"], w["DATE_TO"], w["STAMP"]), ("2025-12-01", "2025-12-31", "December 2025"))

    def test_prepare_flag_and_rotation(self):
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace(window="month"))
        self.assertEqual(mod.prepare(ctx)["WINDOW"], "month")
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace(window=None))
        self.assertEqual(mod.prepare(ctx)["WINDOW"], "day")  # nothing exists yet → first option


class ValidateTests(unittest.TestCase):
    def check(self, text: str, window: str, count: int, aspect: str | None = None) -> None:
        aspect = aspect or ("3:2" if window == "week" else "2:3")
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace(window=window))
        ctx.state["window"] = window
        manifest = {"window": window, "story_count": count, "images": [{"file": "collage.png", "aspect": aspect, "prompt": "p"}]}
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / mod.MAIN).write_text(text, encoding="utf-8")
            mod.validate(Path(tmp), manifest, ctx)

    def test_good(self):
        self.check(doc(6), "day", 6)
        self.check(doc(8), "week", 8)
        self.check(doc(6), "month", 6)

    def test_rejects(self):
        with self.assertRaises(RecipeError):
            self.check(doc(5), "day", 5)  # too few
        with self.assertRaises(RecipeError):
            self.check(doc(11), "week", 11)  # too many
        with self.assertRaises(RecipeError):
            self.check(doc(6, "Tax"), "day", 6)  # caption too short
        with self.assertRaises(RecipeError):
            self.check(doc(6, "1. Senate passes the budget"), "day", 6)  # numbered
        with self.assertRaises(RecipeError):
            self.check(doc(6).replace("https://example.com/3", "no link"), "day", 6)
        with self.assertRaises(RecipeError):
            self.check(doc(6), "day", 5)  # story_count mismatch
        with self.assertRaises(RecipeError):
            self.check(doc(6), "day", 6, aspect="3:2")  # wrong aspect for the window


if __name__ == "__main__":
    unittest.main()
