"""scripts/cli_sweep.py: the matrix rewrite and the sweep loop, with the recipe runs faked."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import cli_sweep  # noqa: E402

MATRIX = """intro
| Recipe | Tools | Claude | Codex | OpenCode | Kimi | Grok | Gemini | agy |
|:---|:---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| [short-story](../recipes/short-story/README.md) | files | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| [comics](../recipes/comics/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [pr-review](../recipes/pr-review/README.md) | bash | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [poster](../recipes/poster/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
outro
"""


class MatrixTests(unittest.TestCase):
    def test_cells_read_the_engine_column(self):
        self.assertEqual(cli_sweep.matrix_cells(MATRIX, "codex"),
                         {"short-story": "✅", "comics": "⬜", "pr-review": "⬜", "poster": "⬜"})
        self.assertEqual(cli_sweep.matrix_cells(MATRIX, "opencode")["short-story"], "⬜")

    def test_rewrite_touches_only_named_cells_in_that_column(self):
        out = cli_sweep.rewrite_matrix(MATRIX, "codex", {"comics": True, "poster": False})
        self.assertIn("| [comics](../recipes/comics/README.md) | files | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |", out)
        self.assertIn("| [poster](../recipes/poster/README.md) | files | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |", out)
        want = MATRIX.replace("comics](../recipes/comics/README.md) | files | ✅ | ⬜", "comics](../recipes/comics/README.md) | files | ✅ | ✅") \
                     .replace("poster](../recipes/poster/README.md) | files | ✅ | ⬜", "poster](../recipes/poster/README.md) | files | ✅ | ❌")
        self.assertEqual(out, want)

    def test_unknown_recipe_is_an_error(self):
        with self.assertRaises(KeyError):
            cli_sweep.rewrite_matrix(MATRIX, "codex", {"nope": True})

    def test_error_line_prefers_the_last_error(self):
        self.assertEqual(cli_sweep.error_line("starting\nERROR: skill not found\nbye\n"), "ERROR: skill not found")
        self.assertEqual(cli_sweep.error_line("one\ntwo\n"), "two")
        self.assertEqual(cli_sweep.error_line(""), "no output")


class SweepTests(unittest.TestCase):
    def sweep(self, argv, outcomes):
        tmp = Path(tempfile.mkdtemp()) / "ROADMAP.md"
        tmp.write_text(MATRIX, encoding="utf-8")
        calls = []

        def fake(name, engine, out, extra):
            calls.append((name, engine))
            return outcomes[name]

        with mock.patch.object(cli_sweep, "ROADMAP", tmp), mock.patch.object(cli_sweep, "run_recipe", fake):
            code = cli_sweep.main(argv)
        return code, calls, tmp.read_text(encoding="utf-8")

    def test_default_takes_todo_cells_and_skips_by_hand_recipes(self):
        code, calls, text = self.sweep(["--engine", "codex"], {"comics": (True, 1.0, ""), "poster": (False, 2.0, "boom")})
        self.assertEqual(calls, [("comics", "codex"), ("poster", "codex")])
        self.assertEqual(code, 1)
        self.assertEqual(cli_sweep.matrix_cells(text, "codex"),
                         {"short-story": "✅", "comics": "✅", "pr-review": "⬜", "poster": "❌"})

    def test_limit_and_no_write(self):
        code, calls, text = self.sweep(["--engine", "kimi", "--limit", "1", "--no-write"], {"short-story": (True, 1.0, "")})
        self.assertEqual(calls, [("short-story", "kimi")])
        self.assertEqual(code, 0)
        self.assertEqual(text, MATRIX)

    def test_by_hand_recipe_is_refused(self):
        code, calls, text = self.sweep(["--engine", "codex", "pr-review"], {})
        self.assertEqual((code, calls, text), (2, [], MATRIX))


if __name__ == "__main__":
    unittest.main()
