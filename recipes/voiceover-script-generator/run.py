#!/usr/bin/env python3
"""Voiceover Script — a researched 90–180 s narration about a real story, narrated with a preset
voice, plus 9:16 scene stills and (with ffmpeg) a vertical short.

    python recipes/voiceover-script-generator/run.py --output-dir ~/ai-output [--voice Adam] [--speech-engine elevenlabs]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import ImageSpec, Recipe, RecipeError, RunContext, run, video  # noqa: E402
from core import audio  # noqa: E402

PRESETS = {**{v: "gemini" for v in audio.GEMINI_VOICES}, **{v: "elevenlabs" for v in audio.ELEVENLABS_VOICES}}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--voice", choices=["auto", *PRESETS], default="auto",
                   help="Narrator preset (must belong to the speech engine). auto lets the agent pick by tone.")


def _engine(args) -> str:
    if args.speech_engine != "auto":
        return args.speech_engine
    if args.voice != "auto":
        return PRESETS[args.voice]
    available = audio.speech_engines()
    return available[0] if available else "gemini"


def prepare(ctx: RunContext) -> dict[str, str]:
    engine = _engine(ctx.args)
    ctx.state["engine"] = engine
    counts = Counter(str(e.fields.get("category")) for e in ctx.existing)
    if ctx.args.voice != "auto":
        if PRESETS[ctx.args.voice] != engine:
            raise RecipeError(f"--voice {ctx.args.voice} is an {PRESETS[ctx.args.voice]} voice, not {engine}")
        voice = f"The narrator is fixed for this run: set `narrator` to `{ctx.args.voice}`."
    else:
        voice = ("Pick the preset that fits the story's tone and set it as `narrator` "
                 f"({engine} voices only):\n\n" +
                 "\n".join(f"   - `{v}` — {audio.voice_notes(engine)[v]}" for v, e in PRESETS.items() if e == engine))
    return {
        "CATEGORIES": "\n".join(f"- `{c}`: {n}" for c, n in counts.most_common()) or "(none yet)",
        "VOICE": voice,
    }


def narration(md: str) -> str:
    parts = re.split(r"^---\s*$", md, flags=re.M)
    return parts[1].strip() if len(parts) >= 3 else ""


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    md = (staging / "script.md").read_text(encoding="utf-8")
    body = narration(md)
    words = len(re.findall(r"[\w'’-]+", body))
    if not 220 <= words <= 500:
        raise RecipeError(f"narration is {words} words; expected 240–480")
    if len(re.findall(r"\]\(https?://", md.split("## Sources", 1)[-1])) < 2:
        raise RecipeError("script.md needs at least two linked sources under ## Sources")
    if "## Tone" not in (staging / "direction-notes.md").read_text(encoding="utf-8"):
        raise RecipeError("direction-notes.md is missing its ## Tone section")
    narrator = str(manifest.get("narrator", ""))
    if PRESETS.get(narrator) != ctx.state["engine"]:
        raise RecipeError(f"narrator {narrator!r} is not a preset {ctx.state['engine']} voice")
    manifest["word_count"] = words


def after_cover(ctx: RunContext, staging: Path, manifest: dict[str, object]) -> list[str]:
    body = narration((staging / "script.md").read_text(encoding="utf-8"))
    paragraphs = [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", body) if p.strip()]
    delivery = str(manifest.get("delivery") or "")
    lines = [audio.Line("Narrator", p, delivery) for p in paragraphs]
    wav, engine, _ = audio.speech(lines, staging / "voiceover.wav", ctx.state["engine"],
                                  {"Narrator": str(manifest["narrator"])}, gap_s=0.3)
    track = audio.to_mp3(wav)
    manifest["speech_engine"] = engine
    out = [track.name]
    scenes = sorted((staging / "scenes").glob("scene-*.png"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    if scenes and video.slideshow(scenes, track, staging / "short.mp4"):
        out.append("short.mp4")
    return out


RECIPE = Recipe(
    name="voiceover-script-generator",
    collection="voiceover-scripts",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("script.md", "direction-notes.md"),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("category", "topic", "narrator"),
    cover_aspect="16:9",
    images=ImageSpec(min=4, max=6, aspects=("9:16",), folder="scenes"),
    default_model="sonnet",
    timeout_s=2400,
    requires=("speech",),
    add_args=add_args,
    prepare=prepare,
    validate=validate,
    after_cover=after_cover,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
