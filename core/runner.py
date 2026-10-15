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
import inspect
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

from . import artifacts, audio, deliver, images
from .engines import EngineError, EngineRequest, get_engine

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
RUN_CONTRACT = (Path(__file__).parent / "run-contract.md").read_text(encoding="utf-8")
RESERVED_KEYS = ("title", "slug", "summary", "cover_prompt", "images", "error")
IMAGE_FILE_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*\.png$")

log = logging.getLogger("recipes")


class RecipeError(RuntimeError):
    """The run produced something unusable; nothing was published."""


class NothingToDo(Exception):
    """Raised by prepare() when there is no work this run (a finished series). Exits 0."""


@dataclass
class RunContext:
    output_dir: Path
    collection_dir: Path
    day: date
    existing: list[artifacts.Existing]
    args: argparse.Namespace
    state: dict[str, object] = field(default_factory=dict)  # prepare() -> later hooks, one run


@dataclass(frozen=True)
class ImageSpec:
    """A recipe whose agent asks for several images: final JSON carries
    `"images": [{"file": "panel-1.png", "prompt": "...", "aspect": "16:9"}]` and the runner
    renders each into `folder/` after validate()."""

    min: int = 1
    max: int = 12
    aspects: tuple[str, ...] = ("16:9",)
    folder: str = "images"  # "" puts them beside the main file
    text_ok: bool = False  # True swaps the no-text constraint for lettering-only (memes, comics)
    size: str | None = None  # resolution tier where supported: "1K", "2K", "4K"
    optional: bool = False  # True: no image key is not an error; the run publishes without the images


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
    validate: Callable[..., None] | None = None  # (staging, manifest[, ctx]); raise RecipeError to reject
    after_cover: Callable[[RunContext, Path, dict[str, object]], list[str] | None] | None = None  # in staging, cover exists; returns extra files to publish
    finish: Callable[[RunContext, Path, dict[str, object]], None] | None = None
    images: ImageSpec | None = None
    requires: tuple[str, ...] = ()  # "images", "speech", "music": checked before the agent runs
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


def stage_skills(staging: Path, names: tuple[str, ...], skills_dir: str = ".claude/skills") -> None:
    """Copy the recipe's skills to where this engine's agent looks for project skills."""
    for name in names:
        src = SKILLS_DIR / name
        if not (src / "SKILL.md").is_file():
            raise RecipeError(f"Skill {name!r} is missing from {SKILLS_DIR}")
        shutil.copytree(src, staging / Path(skills_dir) / name)


def engine_skills_dir(engine: object) -> str:
    return str(getattr(engine, "skills_dir", ".claude/skills")).strip("/")


def parse_args(recipe: Recipe, argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog=recipe.name, description=f"Run the {recipe.name} recipe once.")
    p.add_argument("--output-dir", default=os.environ.get("RECIPES_OUTPUT_DIR"),
                   help="Root folder for all recipe output (or set RECIPES_OUTPUT_DIR).")
    p.add_argument("--date", type=date.fromisoformat, default=date.today(),
                   help="Target date, YYYY-MM-DD (default: today).")
    p.add_argument("--engine", default=os.environ.get("RECIPES_ENGINE", "claude"),
                   help="Text engine: any CLI with a profile in core/engines/clis/ or $RECIPES_CLI_DIR "
                        "(claude by default; see core/engines/clis/README.md).")
    p.add_argument("--model", default=os.environ.get("RECIPES_MODEL", recipe.default_model),
                   help="Model alias or id for the text engine. A Claude alias (sonnet, opus, haiku) means "
                        "'the engine's default' on codex and gemini.")
    p.add_argument("--image-engine", default=os.environ.get("RECIPES_IMAGE_ENGINE", "auto"),
                   choices=["auto", "gemini", "openai", "none"],
                   help="auto = first engine with a key set; skips the cover if none is set.")
    p.add_argument("--speech-engine", default=os.environ.get("RECIPES_SPEECH_ENGINE", "auto"),
                   choices=["auto", "gemini", "elevenlabs"], help="Text-to-speech engine for audio recipes.")
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
    try:
        engine = get_engine(args.engine)
    except EngineError as exc:
        log.error("RECIPE_FAILED %s: %s", recipe.name, exc)
        return 1

    tokens = {
        "DATE": ctx.day.isoformat(),
        "DATE_LONG": ctx.day.strftime("%A, %B %d, %Y").replace(" 0", " "),
        "RUN_CONTRACT": RUN_CONTRACT,
        "SKILLS_DIR": engine_skills_dir(engine),  # after RUN_CONTRACT, which carries the token
        "EXISTING": artifacts.existing_digest(ctx.existing),
        "OUTPUT_FILES": "\n".join(f"- `{f}`" for f in recipe.files),
        "SKILLS": "\n".join(f"- `{s}`" for s in recipe.skills) or "- (none)",
    }
    try:
        tokens.update(recipe.prepare(ctx) if recipe.prepare else {})
    except NothingToDo as exc:
        log.info("RECIPE_SKIPPED %s: %s", recipe.name, exc)
        return 0
    except (RecipeError, audio.AudioError, images.ImageError) as exc:
        log.error("RECIPE_FAILED %s: %s", recipe.name, exc)
        return 1
    prompt = fill(recipe.prompt_path.read_text(encoding="utf-8"), tokens)

    if args.dry_run:
        sys.stdout.write(prompt + "\n")
        return 0

    staging = collection_dir / ".staging" / f"{ctx.day.isoformat()}_{datetime.now():%H%M%S}"
    try:
        final = _run_staged(recipe, ctx, prompt, staging, engine)
    except (RecipeError, EngineError, images.ImageError, audio.AudioError) as exc:
        log.error("RECIPE_FAILED %s: %s", recipe.name, exc)
        if staging.exists() and not args.keep_staging:
            shutil.rmtree(staging, ignore_errors=True)
            _cleanup_staging_root(collection_dir)
        elif staging.exists():
            log.info("staging kept at %s", staging)
        return 1
    log.info("RECIPE_OK %s", final)
    return 0


def _run_staged(recipe: Recipe, ctx: RunContext, prompt: str, staging: Path, engine: object | None = None) -> Path:
    args = ctx.args
    if engine is None:
        engine = get_engine(args.engine)
    engine.preflight()
    _preflight_media(recipe, args)

    staging.mkdir(parents=True)
    skills_dir = engine_skills_dir(engine)
    stage_skills(staging, recipe.skills, skills_dir)

    result = engine.run(EngineRequest(
        # prepare() may narrow the tool list for this run via ctx.state["tools"]
        prompt=prompt, workdir=staging, tools=tuple(ctx.state.get("tools") or recipe.tools), model=args.model,
        timeout_s=args.timeout,
    ))
    # The skills folder root (.claude, .agents or .gemini) is the engine's, never output.
    shutil.rmtree(staging / Path(skills_dir).parts[0], ignore_errors=True)

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
    if recipe.images and recipe.images.folder:
        keep.add(recipe.images.folder)
    for stray in staging.iterdir():
        if stray.name not in keep:
            log.warning("removing unexpected file from output: %s", stray.name)
            shutil.rmtree(stray) if stray.is_dir() else stray.unlink()

    if recipe.validate:
        # validate(staging, manifest) or validate(staging, manifest, ctx)
        if len(inspect.signature(recipe.validate).parameters) >= 3:
            recipe.validate(staging, manifest, ctx)
        else:
            recipe.validate(staging, manifest)

    rendered = _render_images(recipe, args, staging, manifest) if recipe.images else []

    cover = None
    if recipe.cover_aspect and args.image_engine != "none":
        if args.image_engine == "auto" and not images.available_engines():
            log.warning("no image key set (GEMINI_API_KEY / OPENAI_API_KEY) — publishing without a cover")
        else:
            cover = images.render(str(manifest["cover_prompt"]), staging / "cover.png",
                                  recipe.cover_aspect, args.image_engine)

    extra: list[str] = []
    if recipe.after_cover:
        extra = list(recipe.after_cover(ctx, staging, manifest) or [])
        for name in extra:
            if not (staging / name).is_file():
                raise RecipeError(f"after_cover reported {name}, which does not exist")

    slug = artifacts.slugify(str(manifest.get("slug") or manifest["title"]))
    final = artifacts.artifact_dir(ctx.collection_dir, ctx.day, slug)
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(staging), str(final))
    _cleanup_staging_root(ctx.collection_dir)

    published = [*recipe.files[1:], *(f for f in recipe.optional_files if (final / f).is_file()), *extra]
    files = {"main": recipe.files[0], **{Path(f).with_suffix("").as_posix(): f for f in published}}
    if cover:
        files["cover"] = "cover.png"
    if rendered:
        files["images"] = rendered
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

    path = final.relative_to(ctx.output_dir).as_posix()
    artifacts.append_run_log(ctx.output_dir, {
        "date": entry["date"], "recipe": recipe.name, "title": entry["title"], "path": path,
    })
    deliver.announce({**entry, "path": path})  # no-op unless RECIPES_WEBHOOK_URL is set
    return final


def _preflight_media(recipe: Recipe, args: argparse.Namespace) -> None:
    """Fail before the agent runs when a key the recipe can't do without is missing."""
    needs = set(recipe.requires) | ({"images"} if recipe.images and not recipe.images.optional else set())
    if "images" in needs and (args.image_engine == "none" or
                              (args.image_engine == "auto" and not images.available_engines())):
        raise RecipeError("this recipe makes images: set GEMINI_API_KEY or OPENAI_API_KEY")
    if "speech" in needs and not (audio.speech_engines() if args.speech_engine == "auto"
                                  else [args.speech_engine] if args.speech_engine in audio.speech_engines() else []):
        raise RecipeError("this recipe speaks: set GEMINI_API_KEY or ELEVENLABS_API_KEY")
    if "music" in needs and not audio.music_available():
        raise RecipeError("this recipe makes music: set ELEVENLABS_API_KEY")


def _render_images(recipe: Recipe, args: argparse.Namespace, staging: Path, manifest: dict[str, object]) -> list[str]:
    spec = recipe.images
    assert spec is not None
    wanted = manifest.get("images")
    can_render = args.image_engine != "none" and (args.image_engine != "auto" or bool(images.available_engines()))
    if spec.optional and not can_render:
        if wanted:
            log.warning("no image key set (GEMINI_API_KEY / OPENAI_API_KEY) — publishing without the %d optional image(s)",
                        len(wanted) if isinstance(wanted, list) else 1)
        return []
    if not isinstance(wanted, list) or not spec.min <= len(wanted) <= spec.max:
        raise RecipeError(f"final JSON needs {spec.min}–{spec.max} entries in `images`")
    out, seen = [], set()
    for i, item in enumerate(wanted, 1):
        if not isinstance(item, dict):
            raise RecipeError(f"images[{i}] is not an object")
        name, prompt, aspect = str(item.get("file", "")), str(item.get("prompt", "")).strip(), str(item.get("aspect", spec.aspects[0]))
        if not IMAGE_FILE_RE.match(name) or name in seen:
            raise RecipeError(f"images[{i}].file must be a unique lowercase .png name, got {name!r}")
        if aspect not in spec.aspects:
            raise RecipeError(f"images[{i}].aspect {aspect!r} not in {spec.aspects}")
        if not prompt:
            raise RecipeError(f"images[{i}] has no prompt")
        seen.add(name)
        rel = f"{spec.folder}/{name}" if spec.folder else name
        images.render(prompt, staging / rel, aspect, args.image_engine, text_ok=spec.text_ok, size=spec.size)
        out.append(rel)
    return out


def _cleanup_staging_root(collection_dir: Path) -> None:
    root = collection_dir / ".staging"
    if root.is_dir() and not any(root.iterdir()):
        root.rmdir()
