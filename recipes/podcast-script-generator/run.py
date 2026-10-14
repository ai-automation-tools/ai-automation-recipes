#!/usr/bin/env python3
"""Podcast Script — one AI-vs-AI debate episode as a speaker-labelled transcript.

    python recipes/podcast-script-generator/run.py --output-dir ~/ai-output

Render it to audio with the `weekly-audio-podcast` recipe.

Optional, in <output-dir>/podcast-scripts/:
- `podcast-topics.md` — a topic queue, one `- [ ] Title — angle, angle, angle` per line. The first
  unchecked topic is used and ticked off with the episode path.
- `cast/hosts/*.md` and `cast/groups/<Group>/*.md` — a recurring cast. Each run picks one host and
  one group at random. Without a cast folder, the agent invents a fresh fictional cast and writes
  their cards to `cast.md`.
"""

from __future__ import annotations

import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402

TOPICS_FILE = "podcast-topics.md"
UNCHECKED = re.compile(r"^(\s*[-*]\s*)\[ \]\s*(.+)$", re.M)
SPEAKER_RE = re.compile(r"^###\s+(.+?)\s*$", re.M)


def _next_topic(ctx: RunContext) -> str | None:
    path = ctx.collection_dir / TOPICS_FILE
    if not path.is_file():
        return None
    m = UNCHECKED.search(path.read_text(encoding="utf-8"))
    return m.group(2).strip() if m else None


def _library_cast(ctx: RunContext) -> str | None:
    root = ctx.collection_dir / "cast"
    hosts = sorted((root / "hosts").glob("*.md"))
    groups = [g for g in sorted((root / "groups").glob("*")) if g.is_dir() and any(g.glob("*.md"))]
    if not hosts or not groups:
        return None
    host, group = random.choice(hosts), random.choice(groups)
    ctx.state["cast_source"] = f"{host.stem} + {group.name}"
    cards = [f"### Host card — `{host.name}`\n\n{host.read_text(encoding='utf-8').strip()}"]
    cards += [f"### Guest card — `{g.name}` (group {group.name})\n\n{g.read_text(encoding='utf-8').strip()}"
              for g in sorted(group.glob("*.md"))]
    return "Use exactly this cast — one host and every guest in the group:\n\n" + "\n\n".join(cards)


def prepare(ctx: RunContext) -> dict[str, str]:
    topic = _next_topic(ctx)
    ctx.state["topic"] = topic
    cast = _library_cast(ctx)
    ctx.state["invented_cast"] = cast is None
    return {
        "TOPIC": (f"Use this topic from the queue: **{topic}** (the part after the dash lists its "
                  "discussion angles)." if topic else
                  "Pick an original, debate-worthy topic — science, technology, the future, the strange "
                  "and the unexplained — with at least three distinct angles. Unlike every episode below."),
        "CAST": cast or (
            "Invent the cast for this episode: **one host and 3–4 guests**, all fictional, each a vivid, "
            "contrasting personality with a clear stance on the topic (a skeptic, a true believer, a "
            "contrarian, a comic relief…). Write their cards to `cast.md` (see below) before the script."),
        "CAST_FILE": ("" if cast else
                      "### `cast.md`\n\nOne `## <Display Name>` section per speaker (host first): role, "
                      "personality, voice and speech patterns, beliefs on the topic, catchphrases, and what "
                      "they would never say. 60–120 words each."),
    }


def speakers(script: str) -> list[str]:
    body = script.split("## Script", 1)[1] if "## Script" in script else ""
    return SPEAKER_RE.findall(body)


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    text = (staging / "script.md").read_text(encoding="utf-8")
    if "## Script" not in text:
        raise RecipeError("script.md has no `## Script` section")
    turns = speakers(text)
    if len(turns) < 10:
        raise RecipeError(f"script has {len(turns)} turns; expected a real back-and-forth")
    host, counts = turns[0], {}
    for s in turns:
        counts[s] = counts.get(s, 0) + 1
    guests = {s: n for s, n in counts.items() if s != host}
    if len(guests) < 2:
        raise RecipeError("script needs at least two guests besides the host")
    off = {s: n for s, n in guests.items() if not 4 <= n <= 7}
    if off:
        raise RecipeError(f"each guest speaks 4–7 times; off: {off}")
    words = len(re.findall(r"\w+", text.split("## Script", 1)[1]))
    if not 1200 <= words <= 3500:
        raise RecipeError(f"script is {words} words; expected about 1,500–3,000")
    if ctx.state.get("invented_cast") and not (staging / "cast.md").is_file():
        raise RecipeError("an invented cast must be written to cast.md")
    manifest.update(host=host, cast=sorted(guests), word_count=words)


def finish(ctx: RunContext, final: Path, manifest: dict[str, object]) -> None:
    topic = ctx.state.get("topic")
    if not topic:
        return
    path = ctx.collection_dir / TOPICS_FILE
    text = path.read_text(encoding="utf-8")
    m = UNCHECKED.search(text)
    if m and m.group(2).strip() == topic:
        rel = final.relative_to(ctx.collection_dir).as_posix()
        path.write_text(text[: m.start()] + f"{m.group(1)}[x] {m.group(2).rstrip()} — script: {rel}" + text[m.end():],
                        encoding="utf-8")


RECIPE = Recipe(
    name="podcast-script-generator",
    collection="podcast-scripts",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("script.md",),
    optional_files=("cast.md",),
    skills=("image-prompt-craft",),
    fields=("topic",),
    cover_aspect="1:1",
    default_model="opus",
    timeout_s=2400,
    prepare=prepare,
    validate=validate,
    finish=finish,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
