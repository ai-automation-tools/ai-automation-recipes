#!/usr/bin/env python3
"""Song — one original song in a chosen type: lyrics, an ElevenLabs composition plan, the rendered
MP3 and a square cover.

    python recipes/song-generator/run.py --output-dir ~/ai-output [--type rock] [--direction "..."]

Types are the files in briefs/ (37 of them: news songs, rock, country, rap, psychedelic,
folk, jazz, and a comedy twin for most genres). Needs ELEVENLABS_API_KEY — each run spends
ElevenLabs music credits.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402
from core import audio  # noqa: E402

log = logging.getLogger("recipes")

BRIEFS = HERE / "briefs"
TYPES = sorted(p.stem for p in BRIEFS.glob("*.md") if not p.stem.startswith("_"))
SECTION_RE = re.compile(r"^\s*\[[^\]]*\]\s*$", re.M)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--type", dest="song_type", choices=TYPES, default="news", help="Song type (a brief in briefs/).")
    p.add_argument("--direction", default="", help="Optional topic or direction the song should follow.")


def prepare(ctx: RunContext) -> dict[str, str]:
    t = ctx.args.song_type
    if t != "news":  # only the news brief researches; the others forbid web access
        ctx.state["tools"] = tuple(tool for tool in RECIPE.tools if not tool.startswith("Web"))
    recent =[e for e in reversed(ctx.existing) if e.fields.get("song_type") == t][:4]
    rows = "\n".join(
        f"- {e.date} · {e.title} — {e.fields.get('stance', '?')} · {e.fields.get('key', '?')} · "
        f"{e.fields.get('tempo_bpm', '?')} BPM · {e.fields.get('mood', '?')}"
        for e in recent
    ) or "(none yet — the first song of this type)"
    direction = ctx.args.direction.strip()[:2000]
    return {
        "SONG_TYPE": t,
        "BRIEF": (BRIEFS / f"{t}.md").read_text(encoding="utf-8").strip(),
        "COMEDY_RULES": (BRIEFS / "_comedy-rules.md").read_text(encoding="utf-8").strip() if t.endswith("-comedy") else "",
        "RECENT": rows,
        "DIRECTION": (f"**Direction for this run:** {direction}\n\nMake the song about, or clearly steered by, "
                      "this direction. The brief's genre, structure and content rules still apply.") if direction else "",
    }


def lyric_words(md: str) -> int:
    body = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    lines = [l for l in body.splitlines()
             if l.strip() and not l.lstrip().startswith(("#", ">")) and not SECTION_RE.match(l)]
    text = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", " ".join(lines))
    return len(re.findall(r"[A-Za-z0-9'’-]+", text))


def validate(staging: Path, manifest: dict[str, object]) -> None:
    try:
        plan = json.loads((staging / "composition-plan.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RecipeError(f"composition-plan.json is not valid JSON: {exc}") from exc
    chunks = plan.get("chunks") if isinstance(plan, dict) else None
    if not isinstance(chunks, list) or not chunks:
        raise RecipeError("composition-plan.json needs a non-empty `chunks` list")
    total = 0
    for i, c in enumerate(chunks, 1):
        if not isinstance(c, dict) or not isinstance(c.get("text"), str) or not isinstance(c.get("duration_ms"), int):
            raise RecipeError(f"chunk {i} needs `text` (string) and `duration_ms` (integer)")
        if not isinstance(c.get("positive_styles"), list) or not isinstance(c.get("negative_styles"), list):
            raise RecipeError(f"chunk {i} needs `positive_styles` and `negative_styles` lists")
        sung = SECTION_RE.sub("", c["text"])
        if re.search(r"\d", sung):
            raise RecipeError(f"chunk {i} has a digit in a sung line — spell numbers out")
        total += c["duration_ms"]

    target = int(manifest.get("target_ms") or 180000)
    if not 3000 <= total <= 600000 or abs(total - target) > target * 0.10:
        raise RecipeError(f"plan totals {total} ms; must be within 10% of target {target} ms")

    md = (staging / "song.md").read_text(encoding="utf-8")
    if not md.startswith("---"):
        raise RecipeError("song.md must start with its frontmatter")
    words, cap = lyric_words(md), int(manifest.get("word_cap") or 0)
    if not 40 <= cap <= 600:
        raise RecipeError(f"word_cap {cap} is not a plausible cap")
    if words > cap:
        raise RecipeError(f"lyrics are {words} words, over the {cap}-word cap — cut whole lines")
    manifest.update(lyric_words=words, plan_ms=total)


def _ffprobe_seconds(path: Path) -> float | None:
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    try:
        return round(float(out.stdout.strip()), 1)
    except ValueError:
        return None


def _tag(mp3: Path, cover: Path, manifest: dict[str, object], album: str) -> None:
    """ID3 tags + embedded cover, stream copy. Skipped without ffmpeg."""
    if not audio.ffmpeg_available():
        return
    tagged = mp3.with_name("tagged.mp3")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3)]
    cmd += ["-i", str(cover), "-map", "0:a", "-map", "1:v"] if cover.is_file() else []
    cmd += ["-c", "copy", "-id3v2_version", "3", "-metadata", f"title={manifest['title']}",
            "-metadata", "artist=AI Automation Recipes", "-metadata", f"album={album}",
            "-metadata", f"genre={manifest.get('genre', '')}", str(tagged)]
    if subprocess.run(cmd, capture_output=True).returncode == 0:
        tagged.replace(mp3)
    else:
        tagged.unlink(missing_ok=True)
        log.warning("ffmpeg tagging failed; publishing the untagged MP3")


def after_cover(ctx: RunContext, staging: Path, manifest: dict[str, object]) -> list[str]:
    plan = json.loads((staging / "composition-plan.json").read_text(encoding="utf-8"))
    mp3 = audio.music(plan, staging / "song.mp3")
    brief = (BRIEFS / f"{ctx.args.song_type}.md").read_text(encoding="utf-8")
    album = (re.search(r"### Album\s*\n+`([^`]+)`", brief) or [None, "AI Songs"])[1]
    _tag(mp3, staging / "cover.png", manifest, album)
    secs = _ffprobe_seconds(mp3)
    if secs:
        manifest["length_sec"] = secs
        md = staging / "song.md"
        md.write_text(md.read_text(encoding="utf-8").replace("length_sec: pending", f"length_sec: {secs}", 1),
                      encoding="utf-8")
    return ["song.mp3"]


RECIPE = Recipe(
    name="song-generator",
    collection="songs",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("song.md", "composition-plan.json"),
    skills=("songwriting-craft", "llm-writing", "humanizer", "image-prompt-craft"),
    # WebSearch/WebFetch are only used by the news type; the other briefs forbid research.
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("song_type", "genre", "mood", "key"),
    cover_aspect="1:1",
    default_model="opus",
    timeout_s=2400,
    requires=("music",),
    add_args=add_args,
    prepare=prepare,
    validate=validate,
    after_cover=after_cover,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
