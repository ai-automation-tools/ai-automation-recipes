"""Tests for the Cronsole editions: the runtime bundle, the generated script templates, and the
script body itself (setup from a local copy of the bundle, with venv and pip faked)."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_bundle  # noqa: E402
import build_registry  # noqa: E402


def template(recipe: str) -> dict:
    return json.loads((ROOT / "registry" / "templates" / f"recipe-{recipe}-cronsole.json").read_text(encoding="utf-8"))


def fill(body: str, values: dict[str, str]) -> str:
    """What Cronsole's apply does: paste each {{key}} raw."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], body)


def load_body(body: str) -> dict:
    ns: dict = {"__name__": "cronsole_native_under_test"}
    exec(compile(body, "<native-body>", "exec"), ns)
    return ns


class BundleTests(unittest.TestCase):
    def test_reproducible_and_scoped(self):
        a, b = build_bundle.build(), build_bundle.build()
        self.assertEqual(a, b)
        names = tarfile.open(fileobj=io.BytesIO(a)).getnames()
        self.assertIn("core/engines/cli.py", names)
        self.assertIn("core/engines/clis/claude.json", names)
        self.assertIn("recipes/short-story/run.py", names)
        self.assertIn("requirements.txt", names)
        self.assertFalse([n for n in names if n.startswith(("tests/", "registry/", "docs/")) or "__pycache__" in n])
        self.assertFalse([n for n in names if n.endswith((".py", ".md", ".json")) and b"\r\n" in
                          tarfile.open(fileobj=io.BytesIO(a)).extractfile(n).read()], "bundle must be LF")


class TemplateTests(unittest.TestCase):
    def test_every_native_recipe_has_a_valid_template(self):
        for recipe in build_registry.NATIVE:
            t = template(recipe)
            self.assertEqual(t["compatibleTargets"], ["cronsole-native"])
            self.assertEqual(t["action"]["interpreter"], "python")
            self.assertLessEqual(t["execution"]["timeoutSec"], 3600)
            keys = {p["key"] for p in t["parameters"]}
            self.assertNotIn("recipesPath", keys)
            self.assertIn("engine", keys)
            used = set(re.findall(r"\{\{(\w+)\}\}", t["action"]["body"]))
            self.assertEqual(used, keys, recipe)
            self.assertIn(build_bundle.sha256(), t["action"]["body"])
            self.assertLess(len(t["action"]["body"].encode()), 256 * 1024)

    def test_engine_choices_are_the_profiles(self):
        from core.engines import engine_names
        engine = next(p for p in template("short-story")["parameters"] if p["key"] == "engine")
        self.assertEqual(engine["options"], engine_names())

    def test_body_compiles_with_awkward_values(self):
        t = template("short-story")
        body = fill(t["action"]["body"], {"outputDir": "C:\\Users\\you\\AI Output\\", "model": "opus",
                                          "imageEngine": "none", "engine": "codex"})
        ns = load_body(body)
        self.assertEqual(ns["ARGS"][:2], ["--output-dir", "C:\\Users\\you\\AI Output\\"])
        self.assertEqual(ns["ARGS"][-2:], ["--engine", "codex"])
        self.assertEqual(set(ns["KEYS"]), {"GEMINI_API_KEY", "OPENAI_API_KEY"})
        self.assertEqual(ns["RECIPE"], "short-story")


class SetupTests(unittest.TestCase):
    """ensure_runtime() against a file:// copy of the real bundle; venv and pip faked."""

    def run_setup(self, sha: str | None = None):
        data = build_bundle.build()
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        bundle = tmp / "bundle.tar"
        bundle.write_bytes(data)
        body = fill(template("comics")["action"]["body"],
                    {"outputDir": str(tmp / "out"), "model": "sonnet", "imageEngine": "auto", "engine": "claude"})
        ns = load_body(body)
        ns["BUNDLE_URL"] = bundle.as_uri()
        ns["BUNDLE_SHA256"] = sha or hashlib.sha256(data).hexdigest()

        def fake_run(cmd, check=False, **kw):
            if cmd[1:3] == ["-m", "venv"]:
                py = Path(cmd[3]) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
                py.parent.mkdir(parents=True)
                py.write_text("")
            return mock.Mock(returncode=0)

        ns["subprocess"] = mock.Mock(run=fake_run, STDOUT=-2)
        with mock.patch.dict(os.environ, {"LOCALAPPDATA": str(tmp / "cache"), "XDG_CACHE_HOME": ""}):
            return ns, ns["ensure_runtime"]()

    def test_fetches_verifies_and_reuses(self):
        ns, home = self.run_setup()
        self.assertTrue((home / ".ready").is_file())
        self.assertTrue((home / "src" / "recipes" / "comics" / "run.py").is_file())
        self.assertEqual(home.name, build_bundle.version())
        with mock.patch.dict(os.environ, {"LOCALAPPDATA": str(home.parent.parent), "XDG_CACHE_HOME": ""}):
            self.assertEqual(ns["ensure_runtime"](), home)  # second run: no download

    def test_refuses_a_bundle_with_the_wrong_hash(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_setup(sha="0" * 64)
        self.assertIn("sha256", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
