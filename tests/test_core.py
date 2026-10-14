"""Tests for everything in the run loop that doesn't need a live agent.

    python -m unittest discover -s tests
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import artifacts, runner  # noqa: E402
from core.engines import EngineResult  # noqa: E402
from core.images import NO_TEXT, with_constraints  # noqa: E402


def load_recipe(name: str):
    spec = importlib.util.spec_from_file_location(f"recipe_{name}", ROOT / "recipes" / name / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class HelperTests(unittest.TestCase):
    def test_extract_json_prefers_last_fenced_block(self):
        text = 'thinking {"a": 1}\n```json\n{"title": "old"}\n```\nmore\n```json\n{"title": "new"}\n```'
        self.assertEqual(runner.extract_json(text)["title"], "new")

    def test_extract_json_bare_object_fallback(self):
        self.assertEqual(runner.extract_json('Done. {"title": "x", "n": {"k": 1}}')["n"], {"k": 1})

    def test_extract_json_none(self):
        with self.assertRaises(runner.RecipeError):
            runner.extract_json("no json here")

    def test_fill_rejects_unfilled_tokens(self):
        self.assertEqual(runner.fill("a {{X}}", {"X": "b"}), "a b")
        with self.assertRaises(runner.RecipeError):
            runner.fill("a {{X}} {{Y}}", {"X": "b"})

    def test_slugify(self):
        self.assertEqual(artifacts.slugify("Café Déjà Vu: The Game!"), "cafe-deja-vu-the-game")
        self.assertEqual(artifacts.slugify("!!!"), "untitled")

    def test_least_used_counts_then_recency(self):
        ex = [
            artifacts.Existing("t", "s", "2026-01-01", "", {"c": "A"}),
            artifacts.Existing("t", "s", "2026-01-02", "", {"c": "B"}),
            artifacts.Existing("t", "s", "2026-01-03", "", {"c": "A"}),
        ]
        self.assertEqual(artifacts.least_used(["A", "B", "C"], ex, "c"), "C")
        self.assertEqual(artifacts.least_used(["A", "B"], ex, "c"), "B")

    def test_artifact_dir_suffixes_collisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            col = Path(tmp)
            first = artifacts.artifact_dir(col, date(2026, 10, 14), "x")
            first.mkdir(parents=True)
            self.assertEqual(artifacts.artifact_dir(col, date(2026, 10, 14), "x").name, "2026-10-14_x-2")

    def test_constraints_appended_once(self):
        once = with_constraints("a red apple")
        self.assertTrue(once.endswith(NO_TEXT))
        self.assertEqual(with_constraints(once), once)


class BrowserGameValidateTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_recipe("weekly-browser-game")
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, html: str):
        (self.dir / "index.html").write_text(html, encoding="utf-8")

    def test_rejects_local_asset(self):
        self.write('<img src="sprite.png"><script>let a = 1;</script>')
        with self.assertRaises(runner.RecipeError):
            self.mod.validate(self.dir, {})

    def test_allows_p5_cdn(self):
        self.write('<script src="https://cdn.jsdelivr.net/npm/p5@1.11.3/lib/p5.min.js"></script><script>let a=1;</script>')
        self.mod.validate(self.dir, {})

    def test_rejects_syntax_error(self):
        if not self.mod.shutil.which("node"):
            self.skipTest("node not installed")
        self.write("<script>function (</script>")
        with self.assertRaises(runner.RecipeError):
            self.mod.validate(self.dir, {})


class EndToEndTests(unittest.TestCase):
    """The full run loop with the engine and image step faked."""

    def test_app_card_publishes_artifact(self):
        mod = load_recipe("daily-app-card")
        reply = "```json\n" + json.dumps({
            "title": "Receipt Radar", "slug": "receipt-radar", "summary": "Finds refunds you are owed.",
            "category": "Browser Extension", "form_factor": "browser extension",
            "monetization": "freemium", "cover_prompt": "a radar dish over paper receipts", "error": None,
        }) + "\n```"

        class FakeEngine:
            name = "claude"
            def preflight(self): pass
            def run(self, req):
                assert (req.workdir / ".claude" / "skills" / "humanizer" / "SKILL.md").is_file()
                (req.workdir / "card.md").write_text("---\ntitle: Receipt Radar\n---\n# Receipt Radar\n", encoding="utf-8")
                (req.workdir / "scratch.txt").write_text("stray", encoding="utf-8")
                return EngineResult(text=reply, model="claude-test")

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(runner, "get_engine", return_value=FakeEngine()), \
                mock.patch.dict("os.environ", {"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""}):
            code = runner.run(mod.RECIPE, ["--output-dir", tmp, "--date", "2026-10-14"])
            self.assertEqual(code, 0)
            folder = Path(tmp) / "idea-cards" / "2026-10" / "2026-10-14_receipt-radar"
            self.assertTrue((folder / "card.md").is_file())
            self.assertFalse((folder / "scratch.txt").exists())
            self.assertFalse((folder / ".claude").exists())
            manifest = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["fields"]["category"], "Browser Extension")
            self.assertEqual(manifest["generator"]["model"], "claude-test")
            self.assertIsNone(manifest["generator"]["image_engine"])
            self.assertFalse((Path(tmp) / "idea-cards" / ".staging").exists())
            self.assertEqual(len((Path(tmp) / "runs.jsonl").read_text().splitlines()), 1)

            # Second run: the rotation moves off the category just used.
            ctx = runner.RunContext(Path(tmp), Path(tmp) / "idea-cards", date(2026, 10, 15),
                                    artifacts.load_existing(Path(tmp) / "idea-cards"),
                                    argparse.Namespace(category=None))
            self.assertNotEqual(mod.prepare(ctx)["CATEGORY"], "Browser Extension")

    def test_agent_error_publishes_nothing(self):
        mod = load_recipe("weekly-short-story")

        class FailingEngine:
            name = "claude"
            def preflight(self): pass
            def run(self, req):
                return EngineResult(text='```json\n{"error": "could not finish"}\n```', model="m")

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(runner, "get_engine", return_value=FailingEngine()):
            self.assertEqual(runner.run(mod.RECIPE, ["--output-dir", tmp]), 1)
            col = Path(tmp) / "short-stories"
            self.assertEqual(list(col.iterdir()), [])

    def test_story_idea_queue_is_ticked(self):
        mod = load_recipe("weekly-short-story")
        reply = '```json\n{"title": "The Keeper", "slug": "the-keeper", "summary": "s", "genre": "g", "cover_prompt": "c"}\n```'

        class Engine:
            name = "claude"
            def preflight(self): pass
            def run(self, req):
                assert "A lighthouse keeper" in req.prompt
                (req.workdir / "story.md").write_text("# The Keeper\n", encoding="utf-8")
                return EngineResult(text=reply, model="m")

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(runner, "get_engine", return_value=Engine()), \
                mock.patch.dict("os.environ", {"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""}):
            col = Path(tmp) / "short-stories"
            col.mkdir()
            (col / "story-ideas.md").write_text("# Ideas\n- [ ] A lighthouse keeper\n- [ ] Second idea\n", encoding="utf-8")
            self.assertEqual(runner.run(mod.RECIPE, ["--output-dir", tmp, "--date", "2026-10-18"]), 0)
            ideas = (col / "story-ideas.md").read_text(encoding="utf-8")
            self.assertIn("- [x] A lighthouse keeper — story: 2026-10/2026-10-18_the-keeper", ideas)
            self.assertIn("- [ ] Second idea", ideas)


if __name__ == "__main__":
    unittest.main()
