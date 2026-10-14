"""Tests for pr-review and app-enhancement: prepare hooks with gh and the filesystem faked,
and the validate gates."""

from __future__ import annotations

import os

os.environ.setdefault("RECIPES_BROWSER_CHECK", "off")

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import NothingToDo, RecipeError, artifacts, runner  # noqa: E402


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"recipe_{name}", ROOT / "recipes" / name / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ctx_for(tmp: Path, existing=(), **args) -> runner.RunContext:
    col = tmp / "col"
    col.mkdir(exist_ok=True)
    return runner.RunContext(tmp, col, date(2026, 10, 14), list(existing), argparse.Namespace(**args))


# --- pr-review -------------------------------------------------------------

PRS = [{"number": 12, "title": "Fix login", "author": {"login": "ada"}, "headRefName": "fix/login",
        "isDraft": False, "mergeable": "MERGEABLE", "url": "https://github.com/o/r/pull/12"},
       {"number": 15, "title": "Bump deps", "author": {"login": "app/dependabot"}, "headRefName": "dependabot/npm",
        "isDraft": True, "mergeable": "CONFLICTING", "url": "https://github.com/o/r/pull/15"}]


def fake_gh(prs, auth_rc=0):
    def run_(cmd, **kw):
        if cmd[:2] == ["gh", "auth"]:
            return subprocess.CompletedProcess(cmd, auth_rc, "", "not logged in" if auth_rc else "")
        return subprocess.CompletedProcess(cmd, 0, json.dumps(prs), "")
    return run_


REVIEW = """# PR review — o/r — 2026-10-14

Mode: `report`. 2 PRs, 1 pass, 1 hold.

## PR #12 — Fix login

**Author:** @ada · **Checks:** green
**Verdict:** PASS

- one-file fix, checks green

**Action taken:** none

## PR #15 — Bump deps

**Verdict:** HOLD

- draft, conflicting

## Commands

- `gh pr view 12 --repo o/r --json title`
- `gh pr diff 12 --repo o/r`
- `gh pr checks 15 --repo o/r`
"""


class PrReviewTests(unittest.TestCase):
    def test_prepare_lists_prs_and_skips_when_none(self):
        mod = load("pr-review")
        with tempfile.TemporaryDirectory() as tmp:
            ctx = ctx_for(Path(tmp), repo="o/r", base=None, mode="report")
            with mock.patch.object(subprocess, "run", fake_gh(PRS)):
                tokens = mod.prepare(ctx)
            self.assertIn("#12 — Fix login — @ada", tokens["PRS"])
            self.assertIn("DRAFT", tokens["PRS"])
            self.assertEqual(ctx.state["numbers"], [12, 15])
            self.assertIn("Read-only", tokens["MODE_RULES"])
            with mock.patch.object(subprocess, "run", fake_gh([])), self.assertRaises(NothingToDo):
                mod.prepare(ctx)
            with mock.patch.object(subprocess, "run", fake_gh(PRS, auth_rc=1)), self.assertRaises(RecipeError):
                mod.prepare(ctx)

    def check(self, text: str, mode: str = "report", numbers=(12, 15), **manifest) -> None:
        mod = load("pr-review")
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "review.md").write_text(text, encoding="utf-8")
            ctx = ctx_for(Path(tmp), repo="o/r", base=None, mode=mode)
            ctx.state["numbers"] = list(numbers)
            mod.validate(Path(tmp), {"pr_count": len(numbers), "merged_count": 0, **manifest}, ctx)

    def test_good_report_passes(self):
        self.check(REVIEW)

    def test_gates(self):
        with self.assertRaises(RecipeError):  # a PR without a section
            self.check(REVIEW, numbers=(12, 15, 16))
        with self.assertRaises(RecipeError):  # a section without a verdict
            self.check(REVIEW.replace("**Verdict:** HOLD", "Verdict: hold"))
        with self.assertRaises(RecipeError):  # no command log
            self.check(REVIEW.split("## Commands")[0])
        with self.assertRaises(RecipeError):  # report mode ran a mutating command
            self.check(REVIEW + "- `gh pr comment 15 --repo o/r --body-file b.md`\n")
        with self.assertRaises(RecipeError):  # report mode ran a mutating gh api call
            self.check(REVIEW + "- `gh api -X PUT repos/o/r/pulls/12/merge`\n")
        with self.assertRaises(RecipeError):  # comment mode merged
            self.check(REVIEW + "- `gh pr merge 12 --repo o/r --squash`\n", mode="comment")
        with self.assertRaises(RecipeError):  # merged_count outside merge mode
            self.check(REVIEW, merged_count=1)
        with self.assertRaises(RecipeError):  # wrong pr_count
            self.check(REVIEW, pr_count=3)
        # merge mode may merge
        self.check(REVIEW + "- `gh pr merge 12 --repo o/r --squash`\n", mode="merge", merged_count=1)
        # comment mode may comment
        self.check(REVIEW + "- `gh pr comment 15 --repo o/r --body-file b.md`\n", mode="comment")


# --- app-enhancement -------------------------------------------------------

INDEX = "<!doctype html><html><head><link rel=stylesheet href=style.css></head><body><script src=script.js></script></body></html>"


def make_apps(root: Path) -> Path:
    apps = root / "apps"
    for name in ("alpha", "beta"):
        d = apps / name
        d.mkdir(parents=True)
        (d / "index.html").write_text(INDEX, encoding="utf-8")
        (d / "style.css").write_text("body{margin:0}\n", encoding="utf-8")
        (d / "script.js").write_text("const x = 1;\n", encoding="utf-8")
    (apps / "notes").mkdir()  # no index.html: not an app
    return apps


def existing(app: str, day: str) -> artifacts.Existing:
    return artifacts.Existing(title=f"{app} x", slug=f"{app}-x", date=day, summary="s", fields={"app": app})


class AppEnhancementTests(unittest.TestCase):
    def setup(self, tmp: Path, **args):
        mod = load("app-enhancement")
        apps = make_apps(tmp)
        ctx = ctx_for(tmp, [existing("alpha", "2026-10-01")], apps_dir=str(apps), app=None, apply="no", **args)
        tokens = mod.prepare(ctx)
        return mod, ctx, apps, tokens

    def test_rotation_and_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod, ctx, apps, tokens = self.setup(Path(tmp))
            self.assertEqual(ctx.state["app"], "beta")  # alpha was enhanced already
            self.assertTrue((ctx.state["work"] / "index.html").is_file())
            self.assertIn("`script.js`", tokens["APP_FILES"])
            self.assertIn("`alpha`", tokens["OTHER_APPS"])
            self.assertEqual(mod.list_apps(apps), ["alpha", "beta"])
            ctx.args.app = "nope"
            with self.assertRaises(RecipeError):
                mod.prepare(ctx)

    def test_patch_apply_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod, ctx, apps, _ = self.setup(Path(tmp))
            work, staging = ctx.state["work"], Path(tmp) / "staging"
            staging.mkdir()
            (work / "script.js").write_text("const x = 1;\nconst y = 2;\n", encoding="utf-8")
            (work / "help.md").write_text("# Help\n", encoding="utf-8")
            manifest = {"app": "beta", "files_changed": 2}
            mod.validate(staging, manifest, ctx)
            patch = (staging / "enhancement.patch").read_text(encoding="utf-8")
            self.assertIn("+++ b/script.js", patch)
            self.assertIn("+const y = 2;", patch)
            self.assertIn("--- /dev/null\n+++ b/help.md", patch)
            # apply=no leaves the original alone and removes the copy
            mod.finish(ctx, staging, manifest)
            self.assertEqual((apps / "beta" / "script.js").read_text(encoding="utf-8"), "const x = 1;\n")
            self.assertFalse(work.exists())
            # apply=yes writes the changes back
            mod, ctx, apps, _ = self.setup(Path(tmp) / "again")
            ctx.args.apply = "yes"
            (ctx.state["work"] / "style.css").write_text("body{margin:0}\nh1{color:red}\n", encoding="utf-8")
            mod.validate(staging, {"app": "beta", "files_changed": 1}, ctx)
            mod.finish(ctx, staging, {"app": "beta", "files_changed": 1})
            self.assertIn("h1{color:red}", (apps / "beta" / "style.css").read_text(encoding="utf-8"))

    def test_validate_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod, ctx, apps, _ = self.setup(Path(tmp))
            work, staging = ctx.state["work"], Path(tmp) / "staging"
            staging.mkdir()
            with self.assertRaises(RecipeError):  # nothing changed
                mod.validate(staging, {"app": "beta", "files_changed": 0}, ctx)
            (work / "script.js").write_text("const x = 2;\n", encoding="utf-8")
            with self.assertRaises(RecipeError):  # wrong count
                mod.validate(staging, {"app": "beta", "files_changed": 2}, ctx)
            with self.assertRaises(RecipeError):  # wrong app
                mod.validate(staging, {"app": "alpha", "files_changed": 1}, ctx)
            for i in range(3):
                (work / f"extra{i}.txt").write_text("x", encoding="utf-8")
            with self.assertRaises(RecipeError):  # four files
                mod.validate(staging, {"app": "beta", "files_changed": 4}, ctx)
            for i in range(3):
                (work / f"extra{i}.txt").unlink()
            (work / "style.css").unlink()
            with self.assertRaises(RecipeError):  # a deletion
                mod.validate(staging, {"app": "beta", "files_changed": 1}, ctx)


if __name__ == "__main__":
    unittest.main()
