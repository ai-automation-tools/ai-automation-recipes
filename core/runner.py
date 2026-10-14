"""The shared run loop every recipe goes through.

A recipe is data plus a few hooks (see Recipe). The runner owns everything that
should behave the same across recipes:

1. Read what the collection already holds, so the agent can avoid repeats.
2. Fill the recipe's prompt.md and stage an empty folder with its skills.
3. Run the text engine in that folder.
4. Parse the agent's final JSON, check every promised file exists.
5. Render the cover from the agent's `cover_prompt`.
6. Move the folder into place, write artifact.json, append runs.jsonl.

Nothing is published unless every step succeeds; a failed run leaves its
staging folder behind for inspection (or deletes it, without --keep-staging).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Callable

from . import artifacts, images
from .engines import EngineError, EngineRequest, get_engine

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
RUN_CONTRACT = (Path(__file__).parent / "run-contract.md").read_text(encoding="utf-8")
RESERVED_KEYS = ("title", "slug", "summary", "cover_prompt", "error")

log = logging.getLogger("recipes")


class RecipeError(RuntimeError):
    """The run produced something unusable; nothing was published."""


@dataclass
class RunContext:
    output_dir: Path
    collection_dir: Path
    day: date
    existing: list[artifacts.Existing]
    args: argparse.Namespace


@dataclass
class Recipe:
    name: str
    collection: str
    version: str
    prompt_path: Path
    files: tuple[str, ...]  # required; relative paths, subfolders allowed; first is the main file
    optional_files: tuple[str, ...] = ()  # published when present, never required
    skills: tuple[str, ...] = ()
    tools: tuple[str, ...] = ("Read", "Write", "Edit", "Glob", "Grep", "Skill")
    fields: tuple[str, ...] = ()
    cover_aspect: str | None = "16:9"
    default_model: str | None = None
    timeout_s: int = 1800
    add_args: Callable[[argparse.ArgumentParser], None] | None = None
    prepare: Callable[[RunContext], dict[str, str]] | None = None
    validate: Callable[[Path, dict[str, object]], None] | None = None
    finish: Callable[[RunContext, Path, dict[str, object]], None] | None = None
    extra: dict[str, object] = field(default_factory=dict)


# --- helpers ---------------------------------------------------------------

def load_dotenv(path: Path) -> None:
    """Minimal .env loader: KEY=VALUE lines, never overrides the real environment."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def fill(template: str, tokens: dict[str, str]) -> str:
    out = template
    for key, value in tokens.items():
        out = out.replace("{{" + key + "}}", value)
    left = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", out)))
    if left:
        raise RecipeError(f"Unfilled prompt tokens: {', '.join(left)}")
    return out


def extract_json(text: str) -> dict[str, object]:
    """The last JSON object in the agent's reply — fenced block first, bare object as fallback."""
    decoder = json.JSONDecoder()
    for block in reversed(re.findall(r"```json\s*(.*?)```", text, flags=re.S)):
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj

    # No usable fenced block: take the last top-level object, scanning left to right
    # and skipping past each decoded object so a nested one is never returned alone.
    last: dict[str, object] | None = None
    i = text.find("{")
    while i != -1:
        try:
            obj, end = decoder.raw_decode(text, i)
        except json.JSONDecodeError:
            i = text.find("{", i + 1)
            continue
        if isinstance(obj, dict):
            last = obj
        i = text.find("{", end)
    if last is None:
        raise RecipeError("The agent's final message had no JSON object.")
    return last


def stage_skills(staging: Path, names: tuple[str, ...]) -> None:
    for name in names:
        src = SKILLS_DIR / name
        if not (src / "SKILL.md").is_file():
            raise RecipeError(f"Skill {name!r} is missing from {SKILLS_DIR}")
        shutil.copytree(src, staging / ".claude" / "skills" / name)


def parse_args(recipe: Recipe, argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog=recipe.name, description=f"Run the {recipe.name} recipe once.")
    p.add_argument("--output-dir", default=os.environ.get("RECIPES_OUTPUT_DIR"),
                   help="Root folder for all recipe output (or set RECIPES_OUTPUT_DIR).")
    p.add_argument("--date", type=date.fromisoformat, default=date.today(),
                   help="Target date, YYYY-MM-DD (default: today).")
    p.add_argument("--engine", default=os.environ.get("RECIPES_ENGINE", "claude"), help="Text engine.")
    p.add_argument("--model", default=os.environ.get("RECIPES_MODEL", recipe.default_model),
                   help="Model alias or id for the text engine.")
    p.add_argument("--image-engine", default=os.environ.get("RECIPES_IMAGE_ENGINE", "auto"),
                   choices=["auto", "gemini", "openai", "none"],
                   help="auto = first engine with a key set; skips the cover if none is set.")
    p.add_argument("--timeout", type=int, default=recipe.timeout_s, help="Agent timeout in seconds.")
    p.add_argument("--keep-staging", action="store_true", help="Keep the staging folder on failure.")
    p.add_argument("--dry-run", action="store_true", help="Print the filled prompt and exit.")
    if recipe.add_args:
        recipe.add_args(p)
    args = p.parse_args(argv)
    if not args.output_dir:
        p.error("--output-dir is required (or set RECIPES_OUTPUT_DIR)")
    return args


# --- the run ---------------------------------------------------------------

def run(recipe: Recipe, argv: list[str] | None = None) -> int:
    # Windows consoles and schedulers default to cp1252; titles and prompts are UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout)
    load_dotenv(REPO_ROOT / ".env")
    args = parse_args(recipe, argv)

    output_dir = Path(args.output_dir).expanduser().resolve()
    collection_dir = output_dir / recipe.collection
    collection_dir.mkdir(parents=True, exist_ok=True)
    ctx = RunContext(output_dir, collection_dir, args.date, artifacts.load_existing(collection_dir), args)

    tokens = {
        "DATE": ctx.day.isoformat(),
        "DATE_LONG": ctx.day.strftime("%A, %B %d, %Y").replace(" 0", " "),
        "RUN_CONTRACT": RUN_CONTRACT,
        "EXISTING": artifacts.existing_digest(ctx.existing),
        "OUTPUT_FILES": "\n".join(f"- `{f}`" for f in recipe.files),
        "SKILLS": "\n".join(f"- `{s}`" for s in recipe.skills) or "- (none)",
    }
    tokens.update(recipe.prepare(ctx) if recipe.prepare else {})
    prompt = fill(recipe.prompt_path.read_text(encoding="utf-8"), tokens)

    if args.dry_run:
        sys.stdout.write(prompt + "\n")
        return 0

    staging = collection_dir / ".staging" / f"{ctx.day.isoformat()}_{datetime.now():%H%M%S}"
    try:
        final = _run_staged(recipe, ctx, prompt, staging)
    except (RecipeError, EngineError, images.ImageError) as exc:
        log.error("RECIPE_FAILED %s: %s", recipe.name, exc)
        if staging.exists() and not args.keep_staging:
            shutil.rmtree(staging, ignore_errors=True)
            _cleanup_staging_root(collection_dir)
        elif staging.exists():
            log.info("staging kept at %s", staging)
        return 1
    log.info("RECIPE_OK %s", final)
    return 0


def _run_staged(recipe: Recipe, ctx: RunContext, prompt: str, staging: Path) -> Path:
    args = ctx.args
    engine = get_engine(args.engine)
    engine.preflight()

    staging.mkdir(parents=True)
    stage_skills(staging, recipe.skills)

    result = engine.run(EngineRequest(
        prompt=prompt, workdir=staging, tools=recipe.tools, model=args.model, timeout_s=args.timeout,
    ))
    shutil.rmtree(staging / ".claude", ignore_errors=True)

    manifest = extract_json(result.text)
    if manifest.get("error"):
        raise RecipeError(f"agent reported: {manifest['error']}")
    # 0 and False are real values; only absent, null or blank strings count as missing.
    missing = [k for k in ("title", "summary", *recipe.fields) if manifest.get(k) in (None, "") or (isinstance(manifest.get(k), str) and not manifest[k].strip())]
    if recipe.cover_aspect and args.image_engine != "none" and not manifest.get("cover_prompt"):
        missing.append("cover_prompt")
    if missing:
        raise RecipeError(f"final JSON is missing: {', '.join(missing)}")

    for name in recipe.files:
        f = staging / name
        if not f.is_file() or f.stat().st_size == 0:
            raise RecipeError(f"agent did not write {name}")
    # Keep each declared file's top-level entry (a subfolder like extension/ survives whole);
    # anything else at the top level is a sidecar the agent wasn't asked for.
    keep = {Path(f).parts[0] for f in (*recipe.files, *recipe.optional_files)}
    for stray in staging.iterdir():
        if stray.name not in keep:
            log.warning("removing unexpected file from output: %s", stray.name)
            shutil.rmtree(stray) if stray.is_dir() else stray.unlink()

    if recipe.validate:
        recipe.validate(staging, manifest)

    cover = None
    if recipe.cover_aspect and args.image_engine != "none":
        if args.image_engine == "auto" and not images.available_engines():
            log.warning("no image key set (GEMINI_API_KEY / OPENAI_API_KEY) — publishing without a cover")
        else:
            cover = images.render(str(manifest["cover_prompt"]), staging / "cover.png",
                                  recipe.cover_aspect, args.image_engine)

    slug = artifacts.slugify(str(manifest.get("slug") or manifest["title"]))
    final = artifacts.artifact_dir(ctx.collection_dir, ctx.day, slug)
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(staging), str(final))
    _cleanup_staging_root(ctx.collection_dir)

    published = [*recipe.files[1:], *(f for f in recipe.optional_files if (final / f).is_file())]
    files = {"main": recipe.files[0], **{Path(f).with_suffix("").as_posix(): f for f in published}}
    if cover:
        files["cover"] = "cover.png"
    entry = {
        "recipe": recipe.name,
        "recipe_version": recipe.version,
        "collection": recipe.collection,
        "title": manifest["title"],
        "slug": slug,
        "date": ctx.day.isoformat(),
        "summary": manifest["summary"],
        "files": files,
        "fields": {k: v for k, v in manifest.items() if k not in RESERVED_KEYS},
        "generator": {
            "engine": engine.name,
            "model": result.model,
            "image_engine": cover.engine if cover else None,
            "image_model": cover.model if cover else None,
            "cover_prompt": manifest.get("cover_prompt") if cover else None,
        },
    }
    artifacts.write_manifest(final, entry)

    if recipe.finish:
        recipe.finish(ctx, final, manifest)

    artifacts.append_run_log(ctx.output_dir, {
        "date": entry["date"], "recipe": recipe.name, "title": entry["title"],
        "path": final.relative_to(ctx.output_dir).as_posix(),
    })
    return final


def _cleanup_staging_root(collection_dir: Path) -> None:
    root = collection_dir / ".staging"
    if root.is_dir() and not any(root.iterdir()):
        root.rmdir()
