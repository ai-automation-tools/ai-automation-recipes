#!/usr/bin/env python3
"""App Enhancement — one small additive improvement to one static web app in a folder you name.

    python recipes/app-enhancement/run.py --output-dir ~/ai-output --apps-dir ~/sites/tools [--app slug] [--apply]

The runner copies the chosen app (the least-enhanced subfolder with an index.html) into a working
copy, the agent edits the copy, and the runner diffs it against the original into
`enhancement.patch` beside the agent's write-up. Nothing outside the output folder changes unless
`--apply` is set, in which case the changed files are written back to the app after publishing.
"""

from __future__ import annotations

import argparse
import difflib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402
from core.web import browser_smoke, check_refs, node_check  # noqa: E402

MAIN = "enhancement.md"
PATCH = "enhancement.patch"
MAX_FILES = 3
MAX_NEW_BYTES = 50 * 1024
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".cache", "__pycache__"}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--apps-dir", required=True, help="Folder whose subfolders are static apps (each with an index.html).")
    p.add_argument("--app", help="Override the rotation with one app's folder name.")
    p.add_argument("--apply", nargs="?", const="yes", default="no", choices=("yes", "no"),
                   help="yes: write the changed files back to the app after publishing. Default no.")


def list_apps(apps_dir: Path) -> list[str]:
    return sorted(p.name for p in apps_dir.iterdir()
                  if p.is_dir() and p.name not in SKIP_DIRS and (p / "index.html").is_file())


def walk(root: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in root.rglob("*"):
        if p.is_file() and not (set(p.relative_to(root).parts[:-1]) & SKIP_DIRS):
            out[p.relative_to(root).as_posix()] = p
    return out


def prepare(ctx: RunContext) -> dict[str, str]:
    apps_dir = Path(ctx.args.apps_dir).expanduser().resolve()
    if not apps_dir.is_dir():
        raise RecipeError(f"--apps-dir is not a folder: {apps_dir}")
    apps = list_apps(apps_dir)
    if not apps:
        raise RecipeError(f"no subfolder of {apps_dir} has an index.html")
    if ctx.args.app and ctx.args.app not in apps:
        raise RecipeError(f"--app {ctx.args.app!r} is not one of {apps}")
    app = ctx.args.app or least_used(apps, ctx.existing, "app")
    original = apps_dir / app
    work = ctx.collection_dir / ".work" / f"{ctx.day.isoformat()}_{app}"
    if not getattr(ctx.args, "dry_run", False):  # a dry run prints the prompt and never edits
        if work.exists():
            shutil.rmtree(work)
        shutil.copytree(original, work, ignore=shutil.ignore_patterns(*SKIP_DIRS))
    ctx.state.update({"app": app, "original": original, "work": work})
    files = walk(original)
    past = [e for e in ctx.existing if str(e.fields.get("app")) == app]
    return {
        "APP": app,
        "APP_COPY": str(work),
        "APP_FILES": "\n".join(f"- `{rel}` ({files[rel].stat().st_size:,} bytes)" for rel in sorted(files)) or "- (empty)",
        "PAST": "\n".join(f"- {e.date} · {e.title} — {e.summary}" for e in past) or "(none yet — this app's first enhancement)",
        "OTHER_APPS": ", ".join(f"`{a}`" for a in apps if a != app) or "(none)",
    }


def changes_between(original: Path, work: Path) -> tuple[dict[str, str], str]:
    """{relative path: new text} for every added or modified file, and the unified diff."""
    before, after = walk(original), walk(work)
    deleted = sorted(set(before) - set(after))
    if deleted:
        raise RecipeError(f"enhancements are additive: {deleted[0]} was deleted")
    changes: dict[str, str] = {}
    patch: list[str] = []
    for rel in sorted(after):
        new_bytes = after[rel].read_bytes()
        old_bytes = before[rel].read_bytes() if rel in before else None
        if new_bytes == old_bytes:
            continue
        if old_bytes is None and len(new_bytes) > MAX_NEW_BYTES:
            raise RecipeError(f"new file {rel} is {len(new_bytes):,} bytes; the limit is {MAX_NEW_BYTES:,}")
        try:
            new_text = new_bytes.decode("utf-8")
            old_text = old_bytes.decode("utf-8") if old_bytes is not None else ""
        except UnicodeDecodeError as exc:
            raise RecipeError(f"{rel} is not UTF-8 text; only text files may change") from exc
        changes[rel] = new_text
        patch += difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                      fromfile=f"a/{rel}" if old_bytes is not None else "/dev/null",
                                      tofile=f"b/{rel}")
        if patch and not patch[-1].endswith("\n"):
            patch[-1] += "\n"
    return changes, "".join(patch)


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    original, work, app = ctx.state["original"], ctx.state["work"], ctx.state["app"]
    changes, patch = changes_between(original, work)
    if not changes:
        raise RecipeError("the app copy is unchanged; no enhancement was made")
    if len(changes) > MAX_FILES:
        raise RecipeError(f"{len(changes)} files changed; one enhancement touches at most {MAX_FILES}")
    if manifest.get("app") != app:
        raise RecipeError(f"final JSON app must be {app!r}")
    if manifest.get("files_changed") != len(changes):
        raise RecipeError(f"final JSON files_changed must be {len(changes)}")
    check_refs(work, "index.html")
    node_check(work, pages=("index.html",), scripts=tuple(r for r in changes if r.endswith((".js", ".mjs"))))
    browser_smoke(work, "index.html")
    (staging / PATCH).write_text(patch, encoding="utf-8")
    ctx.state["changes"] = changes


def finish(ctx: RunContext, final: Path, manifest: dict[str, object]) -> None:
    if ctx.args.apply == "yes":
        for rel, text in ctx.state["changes"].items():
            target = ctx.state["original"] / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
    shutil.rmtree(ctx.state["work"], ignore_errors=True)
    root = ctx.state["work"].parent
    if root.is_dir() and not any(root.iterdir()):
        root.rmdir()


RECIPE = Recipe(
    name="app-enhancement",
    collection="app-enhancements",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=(MAIN,),
    optional_files=(PATCH,),
    skills=("llm-writing", "humanizer"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill"),
    fields=("app", "files_changed"),
    cover_aspect=None,
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
    finish=finish,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
