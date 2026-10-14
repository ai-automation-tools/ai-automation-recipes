#!/usr/bin/env python3
"""Serialized Novella — one chapter a run of an ongoing novel, written against a story bible.

    python recipes/serialized-novella/run.py --output-dir ~/ai-output [--genre "techno-horror"]

State lives in <output-dir>/serialized-novella/:

* `story-bible.md` — the novel's canon and chapter outline, with frontmatter
  (`title`, `slug`, `genre`, `target_chapters`, `visual_style`, optional `craft_genre`: fantasy,
  horror, litfic, mystery, romance or thriller). Write your own, or let the
  first run invent one: with no bible, the run writes chapter 1 *and* the bible.
* The chapter number and rolling synopsis come from the chapters already published.

When the novel passes `target_chapters`, its bible is archived as `story-bible.<slug>.md` and the
next run starts a new novel.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402

BIBLE = "story-bible.md"
MIN_WORDS = 1200  # well under the 1,800–2,200 target; catches a truncated chapter
SYNOPSIS_MAX_WORDS = 150
# Genre for a newly seeded novel -> its creative-writing-craft genre reference.
GENRES: dict[str, str] = {
    "near-future techno-horror": "horror",
    "sci-fi first contact": "thriller",
    "near-future literary science fiction": "litfic",
    "dark-futurism / AI takeover": "thriller",
    "cozy speculative mystery": "mystery",
}
CRAFT_GENRES = ("fantasy", "horror", "litfic", "mystery", "romance", "thriller")

SEED_TASK = """**There is no story bible yet — this run starts a new novel.** Invent it, in **{genre}**,
and write two files: the bible and chapter 1.

`story-bible.md` must open with this frontmatter, exactly these keys:

```markdown
---
title: <the novel's title>
slug: <kebab-case slug>
genre: {genre}
target_chapters: {target}
craft_genre: {craft_genre}
visual_style: <one sentence: the book's illustration style and 3–4 named colours, reused on every chapter's art>
---
```

Then, 2,500–4,000 words: the premise in one breath; the canon and world rules (what is fixed and
true); the cast, including who is secretly what; the central dramatic question and stakes; the
per-chapter formula; and a **chapter-by-chapter outline of all {target} chapters**, grouped into
acts, one or two sentences each. Foreshadow the ending you pick.

Chapter 1 is the bible's cold opening: setting, protagonist and inciting incident, ending on a hook."""


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--genre", help="Genre for the next NEW novel (ignored while a novel is in progress).")
    p.add_argument("--target-chapters", type=int, default=30, help="Length of a newly seeded novel.")


def _frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    if not m:
        return {}
    return {k.strip(): v.strip().strip('"') for k, v in re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M)}


def _chapters(collection: Path, slug: str) -> list[tuple[int, Path, dict]]:
    """Published chapters of one novel, in order: (number, folder, artifact fields)."""
    out = []
    for manifest in collection.glob("*/*/artifact.json"):
        fields = json.loads(manifest.read_text(encoding="utf-8")).get("fields") or {}
        if fields.get("novel_slug") == slug:
            out.append((int(fields.get("chapter", 0)), manifest.parent, fields))
    return sorted(out, key=lambda c: c[0])


def _genre_reference(craft_genre: str) -> str:
    if craft_genre not in CRAFT_GENRES:
        return ""
    return (f"\nAlso read `creative-writing-craft`'s genre reference for this novel: "
            f"`resources/genre/{craft_genre}.md`.\n")


def prepare(ctx: RunContext) -> dict[str, str]:
    col, args = ctx.collection_dir, ctx.args
    bible_path = col / BIBLE
    bible = _frontmatter(bible_path.read_text(encoding="utf-8")) if bible_path.is_file() else {}

    if bible:
        done = _chapters(col, bible.get("slug", ""))
        target = int(bible.get("target_chapters") or 30)
        if len(done) >= target:
            bible_path.rename(col / f"story-bible.{bible.get('slug', 'finished')}.md")
            bible = {}

    if not bible:
        archived = len(list(col.glob("story-bible.*.md")))
        genre = args.genre or list(GENRES)[archived % len(GENRES)]
        craft_genre = GENRES.get(genre, "litfic")
        ctx.state.update(seed=True, expect={"chapter": 1})
        return {
            "NOVEL_TITLE": "<the title you invent>",
            "NOVEL_SLUG": "<your-novel-slug>",
            "CHAPTER": "1",
            "CHAPTER_PADDED": "01",
            "TARGET_CHAPTERS": str(args.target_chapters),
            "GENRE": genre,
            "BIBLE_TASK": SEED_TASK.format(genre=genre, target=args.target_chapters, craft_genre=craft_genre),
            "CONTINUITY": "",
            "OUTPUT_FILES": f"- `chapter.md`\n- `{BIBLE}`",
            "GENRE_REFERENCE": _genre_reference(craft_genre),
        }

    slug, chapters = bible["slug"], _chapters(col, bible["slug"])
    n = len(chapters) + 1
    ctx.state.update(seed=False, expect={"chapter": n, "novel_slug": slug})

    continuity = ""
    if chapters:
        recent = []
        for num, folder, _ in chapters[-3:]:
            text = (folder / "chapter.md").read_text(encoding="utf-8")
            text = re.sub(r"^---\n.*?\n---\n", "", text.replace("\r\n", "\n"), count=1, flags=re.S).strip()
            recent.append(f"### Chapter {num}\n\n{text[:9000]}")
        continuity = (
            "**Rolling synopsis so far:**\n\n" + str(chapters[-1][2].get("synopsis", "")) +
            "\n\n**The most recent chapters** — match voice and tense, honour every planted thread, "
            "never contradict or repeat:\n\n" + "\n\n".join(recent)
        )

    return {
        "NOVEL_TITLE": bible.get("title", slug),
        "NOVEL_SLUG": slug,
        "CHAPTER": str(n),
        "CHAPTER_PADDED": f"{n:02d}",
        "TARGET_CHAPTERS": bible.get("target_chapters", "30"),
        "GENRE": bible.get("genre", ""),
        "BIBLE_TASK": f"The story bible (fixed canon) is below.\n\n----- STORY BIBLE -----\n"
                      f"{bible_path.read_text(encoding='utf-8')}\n----- END STORY BIBLE -----",
        "CONTINUITY": continuity,
        "OUTPUT_FILES": "- `chapter.md`",
        "GENRE_REFERENCE": _genre_reference(bible.get("craft_genre", "")),
    }


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    for key, want in ctx.state["expect"].items():
        if str(manifest.get(key)) != str(want):
            raise RecipeError(f"final JSON has {key}={manifest.get(key)!r}, expected {want!r}")
    words = len((staging / "chapter.md").read_text(encoding="utf-8").split())
    if words < MIN_WORDS:
        raise RecipeError(f"chapter.md is {words} words, under the {MIN_WORDS}-word floor")
    synopsis = str(manifest.get("synopsis", "")).split()
    if len(synopsis) > SYNOPSIS_MAX_WORDS:
        # ponytail: hard word cut; the prompt asks the agent to condense, this is only a guard
        manifest["synopsis"] = " ".join(synopsis[:SYNOPSIS_MAX_WORDS])
    if ctx.state["seed"]:
        if not (staging / BIBLE).is_file():
            raise RecipeError(f"the seed run did not write {BIBLE}")
        bible = _frontmatter((staging / BIBLE).read_text(encoding="utf-8"))
        missing = [k for k in ("title", "slug", "genre", "target_chapters", "visual_style") if not bible.get(k)]
        if missing:
            raise RecipeError(f"story-bible.md frontmatter is missing: {', '.join(missing)}")
        if bible["slug"] != manifest.get("novel_slug"):
            raise RecipeError("story-bible.md slug and the final JSON's novel_slug differ")


def finish(ctx: RunContext, final: Path, manifest: dict[str, object]) -> None:
    if ctx.state.get("seed"):
        # The chapter-1 folder keeps its copy as a snapshot; the live bible sits at the collection root.
        shutil.copy2(final / BIBLE, ctx.collection_dir / BIBLE)


RECIPE = Recipe(
    name="serialized-novella",
    collection="serialized-novella",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("chapter.md",),
    optional_files=(BIBLE,),  # written only by the seed run; validate() requires it then
    skills=("writing-principles", "creative-writing-craft", "creative-writing-modes", "story-review",
            "llm-writing", "humanizer", "image-prompt-craft"),
    fields=("novel_title", "novel_slug", "chapter", "synopsis"),
    cover_aspect="16:9",
    default_model="opus",
    timeout_s=2400,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
    finish=finish,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
