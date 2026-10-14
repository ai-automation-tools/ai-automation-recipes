#!/usr/bin/env python3
"""Weekend Yearly Collections — advances every long-running image collection by one entry per run.

    python recipes/weekend-yearly-collections/run.py --output-dir ~/ai-output

The collections live in `<output-dir>/collections/collections.json`, seeded on the first run with
three examples (Science Breakthroughs by year, Technology Milestones, Exoplanets). Edit it to add,
pause or reorder collections. Progress is read back from published artifacts, so nothing else
needs tracking; when every collection is finished the run exits 0 without calling the agent.
"""

from __future__ import annotations

import json
import logging
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, NothingToDo, Recipe, RecipeError, RunContext, run  # noqa: E402
from core.images import process  # noqa: E402
from core.artifacts import slugify  # noqa: E402
from core.images import ASPECTS  # noqa: E402

log = logging.getLogger("recipes")
CONFIG = "collections.json"
MAX_PER_RUN = 12


def load_config(collection_dir: Path) -> list[dict]:
    path = collection_dir / CONFIG
    if not path.is_file():
        shutil.copy2(HERE / "collections.default.json", path)
        log.info("seeded %s — edit it to choose your collections", path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RecipeError(f"{path} is not valid JSON: {exc}") from exc
    cols = data.get("collections")
    if not isinstance(cols, list):
        raise RecipeError(f"{path} needs a `collections` list")
    for c in cols:
        if c.get("kind") not in ("years", "list") or c.get("aspect", "3:2") not in ASPECTS or not c.get("id"):
            raise RecipeError(f"{path}: collection {c.get('id')!r} needs an id, kind years|list, aspect in {ASPECTS}")
    return cols


def sequence(c: dict, year: int) -> list[tuple[str, str]]:
    """(key, label) for every entry of a collection, in order."""
    if c["kind"] == "years":
        end = year - 1 if c.get("end", "last-complete") == "last-complete" else int(c["end"])
        return [(str(y), str(y)) for y in range(int(c.get("start", 2000)), end + 1)]
    return [(str(i["key"]), str(i.get("label", i["key"]))) for i in c.get("items", [])]


def prepare(ctx: RunContext) -> dict[str, str]:
    done = {(str(e.get("collection")), str(e.get("key")))
            for a in ctx.existing for e in (a.fields.get("entries") or []) if isinstance(e, dict)}
    plan = []
    for c in load_config(ctx.collection_dir):
        if not c.get("active", True):
            continue
        nxt = next(((k, lab) for k, lab in sequence(c, ctx.day.year) if (c["id"], k) not in done), None)
        if nxt is None:
            log.info("collection %s is complete", c["id"])
            continue
        key, label = nxt
        plan.append({"collection": c["id"], "title": c.get("title", c["id"]), "key": key, "label": label,
                     "file": f"{slugify(c['id'])}-{slugify(key)}.png", "aspect": c.get("aspect", "3:2"),
                     "research": bool(c.get("research")), "lettering": c.get("lettering", "none"),
                     "brief": c.get("brief", "")})
    if not plan:
        raise NothingToDo("every active collection is complete")
    plan = plan[:MAX_PER_RUN]
    ctx.state["plan"] = plan

    blocks = []
    for i, p in enumerate(plan, 1):
        blocks.append(
            f"### {i}. {p['title']} — `{p['label']}`\n\n"
            f"- **Image file:** `{p['file']}` · aspect `{p['aspect']}`\n"
            f"- **Research:** {'yes — use WebSearch, cite sources' if p['research'] else 'no'}\n"
            f"- **Lettering:** {p['lettering']}\n"
            f"- **Collection brief:** {p['brief']}")
    example = [{"collection": p["collection"], "key": p["key"], "title": "<entry title>"} for p in plan]
    images = [{"file": p["file"], "prompt": "<prompt>", "aspect": p["aspect"]} for p in plan]
    return {"PLAN": "\n\n".join(blocks), "ENTRIES_JSON": json.dumps(example, ensure_ascii=False),
            "IMAGES_JSON": json.dumps(images, ensure_ascii=False)}


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    plan = ctx.state["plan"]
    got = [(i.get("file"), i.get("aspect")) for i in manifest.get("images") or [] if isinstance(i, dict)]
    if got != [(p["file"], p["aspect"]) for p in plan]:
        raise RecipeError(f"images must be exactly {[(p['file'], p['aspect']) for p in plan]}, in order")
    entries = manifest.get("entries") or []
    if [(str(e.get("collection")), str(e.get("key"))) for e in entries if isinstance(e, dict)] != \
            [(p["collection"], p["key"]) for p in plan]:
        raise RecipeError("`entries` must echo the planned collection/key pairs, in order")
    md = (staging / "entries.md").read_text(encoding="utf-8")
    missing = [p["file"] for p in plan if f"images/{p['file']}" not in md]
    if missing:
        raise RecipeError(f"entries.md doesn't link {missing}")


def cover_from_first(ctx: RunContext, staging: Path, manifest: dict[str, object]) -> list[str]:
    src = staging / "images" / ctx.state["plan"][0]["file"]
    if not src.is_file():
        return []
    return [process.use_as_cover(staging, f"images/{ctx.state['plan'][0]['file']}")]


RECIPE = Recipe(
    name="weekend-yearly-collections",
    collection="collections",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("entries.md",),
    skills=("image-prompt-craft", "llm-writing", "humanizer"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("entries",),
    cover_aspect=None,
    # text_ok: entries letter their year or title; the runner appends the lettering-only constraint.
    images=ImageSpec(min=1, max=MAX_PER_RUN, aspects=ASPECTS, folder="images", text_ok=True),
    default_model="sonnet",
    timeout_s=3600,
    prepare=prepare,
    validate=validate,
    after_cover=cover_from_first,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
