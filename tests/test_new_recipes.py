"""Tests for viral-recipe, model-benchmark-watch and news-digest: their checks and prepare hooks,
and news-digest end to end with the feeds and the agent faked."""

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

from core import RecipeError, artifacts, food, runner  # noqa: E402
from core.engines import EngineResult  # noqa: E402


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"recipe_{name}", ROOT / "recipes" / name / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VIRAL = """---
title: "Cottage Cheese Flatbread"
region: "viral"
yield: "2 servings"
active_time_min: 10
total_time_min: 40
tags: [viral, tiktok]
allergens: [dairy, egg]
source: "https://www.tiktok.com/@someone/video/1"
source_platform: "TikTok"
version: "v1"
date: "2026-10-14"
---

# Cottage Cheese Flatbread

## Cultural Context
x

## Why This Went Viral
A two-ingredient high-protein bread.

## Ingredients
- 1 cup cottage cheese
- 2 eggs

## Instructions
1. **Bake:** 35 minutes at 350°F (175°C).

## Sources
- https://www.tiktok.com/@someone/video/1 — the original
"""


class ViralRecipeTests(unittest.TestCase):
    def check(self, text: str, platform: str = "TikTok") -> None:
        mod = load("viral-recipe")
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "recipe.md").write_text(text, encoding="utf-8")
            with mock.patch.object(food, "check_recipe", lambda s, m: None):
                mod.validate(Path(tmp), {"source_platform": platform})

    def test_good_card_passes(self):
        self.check(VIRAL)

    def test_missing_source_platform_or_section_rejected(self):
        with self.assertRaises(RecipeError):
            self.check(VIRAL.replace('source: "https://www.tiktok.com/@someone/video/1"\n', ""))
        with self.assertRaises(RecipeError):
            self.check(VIRAL.replace('source_platform: "TikTok"', 'source_platform: "Blog"'), "Blog")
        with self.assertRaises(RecipeError):
            self.check(VIRAL.replace("## Why This Went Viral\n", "## Why\n"))
        with self.assertRaises(RecipeError):
            self.check(VIRAL, platform="Reddit")  # manifest disagrees with the frontmatter

    def test_platform_flag_and_template_token(self):
        mod = load("viral-recipe")
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace(platform="Reddit"))
        tokens = mod.prepare(ctx)
        self.assertIn("Reddit", tokens["PLATFORM_RULE"])
        self.assertIn("## Ingredients", tokens["RECIPE_TEMPLATE"])


BENCH = """---
title: "Model Benchmark Watch — October 14, 2026"
---
# Model Benchmark Watch

> intro

## Overview
x

## New & Updated Models
### Foo 2
**Who / licence:** Foo Labs; open-weight. **Source:** [page](https://a.example/1).

## Head-to-Head

| Model | Org | Open? | Elo |
|:---|:---|:--:|--:|
| A | X | no | 1400 |
| B | X | no | 1390 |
| C | Y | yes | 1380 |
| D | Y | yes | — |
| E | Z | yes | 1300 |

Reading.

## Benchmark & Leaderboard Movement
- C moved up on 2026-10-12.

## Analysis
x

## Sources
""" + "\n".join(f"- [s{i}](https://s{i}.example/p)" for i in range(10)) + "\n"


class ModelBenchmarkTests(unittest.TestCase):
    def check(self, text: str, compared: int = 5) -> None:
        mod = load("model-benchmark-watch")
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "digest.md").write_text(text, encoding="utf-8")
            mod.validate(Path(tmp), {"compared": compared})

    def test_good_edition_passes(self):
        self.check(BENCH)

    def test_thin_or_hedged_edition_rejected(self):
        with self.assertRaises(RecipeError):
            self.check(BENCH.replace("| E | Z | yes | 1300 |\n", ""), compared=4)
        with self.assertRaises(RecipeError):
            self.check(BENCH, compared=6)
        with self.assertRaises(RecipeError):
            self.check(BENCH.replace("- [s9](https://s9.example/p)", "- [s9](https://s8.example/p)"))
        with self.assertRaises(RecipeError):
            self.check(BENCH.replace("| A | X | no | 1400 |", "| A | X | no | roughly 1400 |"))
        with self.assertRaises(RecipeError):
            self.check(BENCH.replace("## Benchmark & Leaderboard Movement", "## Movement"))

    def test_previous_edition_is_handed_over(self):
        mod = load("model-benchmark-watch")
        with tempfile.TemporaryDirectory() as tmp:
            col = Path(tmp) / "model-benchmark-watch"
            ctx = runner.RunContext(Path(tmp), col, date(2026, 10, 21), [], argparse.Namespace())
            self.assertIn("first edition", mod.prepare(ctx)["PREVIOUS"])
            run_dir = col / "2026-10" / "2026-10-14_model-benchmark-watch"
            run_dir.mkdir(parents=True)
            (run_dir / "digest.md").write_text(BENCH, encoding="utf-8")
            prev = mod.prepare(ctx)["PREVIOUS"]
            self.assertIn("2026-10-14_model-benchmark-watch", prev)
            self.assertIn("| C | Y | yes | 1380 |", prev)
            self.assertIn("C moved up", prev)
            self.assertNotIn("## Analysis", prev)


def feed_items(n: int, source: str, days_ago: int) -> list[dict]:
    when = (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime("%a, %d %b %Y %H:%M:%S +0000")
    return [{"title": f"{source} story {i}", "url": f"https://{source}.example/{days_ago}/{i}", "source": source,
             "description": "d", "published": when, "starsThisWeek": None, "stars": None} for i in range(n)]


def digest_for(topic_sections: list[str], links: int = 9, table: bool = False) -> str:
    urls = [f"https://feed-a.example/1/{i}" for i in range(links)]
    top = "\n\n".join(f"### [Story {i}]({u})\nTwo sentences. *Feed A, 2026-10-13*" for i, u in enumerate(urls[:5]))
    secs = "\n\n".join(f"## {s}\n\n- **[Item]({u})** — one line. *Feed A, 2026-10-13*"
                       for s, u in zip(topic_sections[:3], urls[5:8]))
    extra = f"\n\n## {topic_sections[3]}\n\n- **[Item]({urls[8]})** — one line." if links > 8 else ""
    tbl = "\n\n| a | b |\n|---|---|\n| 1 | 2 |\n" if table else ""
    srcs = "\n".join(f"- [Feed A — {u}]({u})" for u in urls)
    return (f"---\ntitle: T\n---\n# T\n\n> intro\n\n## Top Stories\n\n{top}\n\n{secs}{extra}{tbl}\n\n"
            f"## Watchlist\n\n- next week\n\n## Sources\n\n{srcs}\n")


class NewsDigestTests(unittest.TestCase):
    def test_window_filters_and_caps(self):
        mod = load("news-digest")
        items = feed_items(30, "loud", 1) + feed_items(3, "quiet", 2) + feed_items(5, "old", 30) + [
            {"title": "undated", "url": "https://u.example/x", "source": "u", "description": "", "published": ""}]
        kept = mod.window_items(items, 7)
        by_source = {}
        for it in kept:
            by_source[it["source"]] = by_source.get(it["source"], 0) + 1
        self.assertEqual(by_source, {"loud": mod.PER_SOURCE_CAP, "quiet": 3, "u": 1})
        self.assertEqual(kept[0]["source"], "loud")  # newest first
        self.assertTrue(all(len(it["published"]) == 10 for it in kept))

    def test_prepare_rotates_and_fails_on_empty_window(self):
        mod = load("news-digest")
        payload = {"candidates": feed_items(4, "feed-a", 1), "feeds_ok": ["https://feed-a.example/rss"], "feeds_failed": []}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(mod, "fetch_candidates", return_value=payload):
            ctx = runner.RunContext(Path(tmp), Path(tmp) / "news-digests", date(2026, 10, 14), [],
                                    argparse.Namespace(topic="energy", days=7))
            tokens = mod.prepare(ctx)
            self.assertEqual(tokens["TOPIC"], "energy")
            self.assertEqual(ctx.state["topic"], "energy")
            self.assertIn("feed-a story 0", tokens["CANDIDATES"])
            self.assertIn("Oil & Gas", tokens["SECTIONS"])
            self.assertEqual(tokens["WINDOW"], "2026-10-07 to 2026-10-14")
        # rotation: with `ai` used once, the least-used topic is the first alphabetical unused one
        existing = [artifacts.Existing(title="t", slug="ai", date="2026-10-01", summary="s", fields={"topic": "ai"})]
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(mod, "fetch_candidates", return_value=payload):
            ctx = runner.RunContext(Path(tmp), Path(tmp) / "news-digests", date(2026, 10, 14), existing,
                                    argparse.Namespace(topic=None, days=7))
            self.assertEqual(mod.prepare(ctx)["TOPIC"], "cybersecurity")
        empty = {"candidates": [], "feeds_ok": [], "feeds_failed": ["https://x: URLError"]}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(mod, "fetch_candidates", return_value=empty):
            ctx = runner.RunContext(Path(tmp), Path(tmp) / "news-digests", date(2026, 10, 14), [],
                                    argparse.Namespace(topic="energy", days=7))
            with self.assertRaises(RecipeError):
                mod.prepare(ctx)

    def test_validate_shape(self):
        mod = load("news-digest")
        sections = mod.TOPICS["gaming"]["sections"]
        ctx = runner.RunContext(Path("."), Path("."), date(2026, 10, 14), [], argparse.Namespace())
        ctx.state["topic"] = "gaming"
        good = {"topic": "gaming", "story_count": 9}
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "digest.md").write_text(digest_for(sections), encoding="utf-8")
            mod.validate(p, good, ctx)
            (p / "digest.md").write_text(digest_for(sections, table=True), encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, good, ctx)
            (p / "digest.md").write_text(digest_for(sections, links=6), encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, good, ctx)
            (p / "digest.md").write_text(digest_for(["Nope", "Also nope", "Still nope", "No"]), encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, good, ctx)
            (p / "digest.md").write_text(digest_for(sections), encoding="utf-8")
            with self.assertRaises(RecipeError):
                mod.validate(p, {"topic": "gaming", "story_count": "nine"}, ctx)

    def test_end_to_end_without_an_image_key(self):
        mod = load("news-digest")
        sections = mod.TOPICS["gaming"]["sections"]
        payload = {"candidates": feed_items(9, "feed-a", 1), "feeds_ok": ["f"], "feeds_failed": []}
        reply = "```json\n" + json.dumps({"title": "🎮 Gaming Industry — October 14, 2026", "slug": "gaming",
                                          "summary": "s", "topic": "gaming", "story_count": 9,
                                          "cover_prompt": "blocks", "error": None}) + "\n```"

        class Engine:
            name = "claude"
            skills_dir = ".claude/skills"
            def preflight(self): pass
            def run(self, req):
                assert "feed-a story 3" in req.prompt and "Studios & Deals" in req.prompt
                (req.workdir / "digest.md").write_text(digest_for(sections), encoding="utf-8")
                return EngineResult(text=reply, model="m")

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod, "fetch_candidates", return_value=payload), \
                mock.patch.object(runner, "get_engine", return_value=Engine()), \
                mock.patch.dict("os.environ", {"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""}):
            code = runner.run(mod.RECIPE, ["--output-dir", tmp, "--date", "2026-10-14", "--topic", "gaming"])
            self.assertEqual(code, 0)
            folder = Path(tmp) / "news-digests" / "2026-10" / "2026-10-14_gaming"
            man = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))
            self.assertEqual(man["fields"], {"topic": "gaming", "story_count": 9})
            self.assertTrue((folder / "digest.md").is_file())


if __name__ == "__main__":
    unittest.main()
