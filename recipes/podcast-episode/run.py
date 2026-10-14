#!/usr/bin/env python3
"""Podcast Episode — render the oldest unrendered podcast script to an episode.

    python recipes/podcast-episode/run.py --output-dir ~/ai-output [--speech-engine gemini]

Reads the scripts the `podcast-script-generator` recipe wrote to <output-dir>/podcast-scripts/.
The agent casts a preset voice per speaker and writes show notes; the runner renders every line
with text-to-speech (Gemini by default; ElevenLabs premade voices with --speech-engine elevenlabs)
and encodes MP3 when ffmpeg is installed. With no unrendered script, it logs that and exits 0.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import NothingToDo, Recipe, RecipeError, RunContext, run  # noqa: E402
from core import audio  # noqa: E402
from core.artifacts import MANIFEST  # noqa: E402

log = logging.getLogger("recipes")

SCRIPTS = "podcast-scripts"
TURN_RE = re.compile(r"^###\s+(.+?)\s*$", re.M)


def turns(script: str) -> list[tuple[str, str]]:
    """(speaker, text) per `### Speaker` block after `## Script`."""
    body = script.split("## Script", 1)[1] if "## Script" in script else ""
    parts = TURN_RE.split(body)
    out = []
    for i in range(1, len(parts), 2):
        text = " ".join(line.strip() for line in parts[i + 1].splitlines() if line.strip())
        if text:
            out.append((parts[i].strip(), text))
    return out


def _engine(args) -> str:
    if args.speech_engine != "auto":
        return args.speech_engine
    available = audio.speech_engines()
    return available[0] if available else "gemini"


def _presets(engine: str) -> tuple[str, ...]:
    return audio.GEMINI_VOICES if engine == "gemini" else tuple(audio.ELEVENLABS_VOICES)


def prepare(ctx: RunContext) -> dict[str, str]:
    scripts_dir = ctx.output_dir / SCRIPTS
    rendered = {e.fields.get("script") for e in ctx.existing}
    candidates = []
    for manifest in scripts_dir.glob(f"*/*/{MANIFEST}"):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        rel = manifest.parent.relative_to(ctx.output_dir).as_posix()
        if rel not in rendered and (manifest.parent / "script.md").is_file():
            candidates.append((str(data.get("date", "")), rel))
    if not candidates:
        raise NothingToDo(f"no unrendered scripts in {scripts_dir} — nothing to do")
    _, rel = min(candidates)  # oldest first
    folder = ctx.output_dir / rel
    script = (folder / "script.md").read_text(encoding="utf-8")
    cast = list(dict.fromkeys(s for s, _ in turns(script)))
    engine = _engine(ctx.args)
    ctx.state.update(script_rel=rel, script_dir=folder, speakers=cast, engine=engine)
    cast_md = folder / "cast.md"
    return {
        "SCRIPT_PATH": rel,
        "SCRIPT": script.strip(),
        "SPEAKERS": ", ".join(f"`{s}`" for s in cast),
        "CAST_NOTES": f"Cast cards:\n\n{cast_md.read_text(encoding='utf-8').strip()}" if cast_md.is_file() else "",
        "ENGINE": engine,
        "VOICES": "\n".join(f"- `{v}` — {audio.voice_notes(engine).get(v, '')}" for v in _presets(engine)),
    }


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    voices, presets = manifest.get("voices"), _presets(ctx.state["engine"])
    if not isinstance(voices, dict):
        raise RecipeError("final JSON needs a `voices` map")
    missing = [s for s in ctx.state["speakers"] if s not in voices]
    if missing:
        raise RecipeError(f"no voice for: {', '.join(missing)}")
    bad = {s: v for s, v in voices.items() if v not in presets}
    if bad:
        raise RecipeError(f"not preset {ctx.state['engine']} voices: {bad}")
    if len(set(voices.values())) < min(len(ctx.state["speakers"]), len(presets)):
        raise RecipeError("speakers share a voice while unused presets remain")


def after_cover(ctx: RunContext, staging: Path, manifest: dict[str, object]) -> list[str]:
    src = ctx.state["script_dir"]
    script = (src / "script.md").read_text(encoding="utf-8")
    shutil.copy2(src / "script.md", staging / "script.md")
    extra = ["script.md"]
    if (src / "cover.png").is_file():  # reuse the script's cover instead of drawing a new one
        shutil.copy2(src / "cover.png", staging / "cover.png")
        extra.append("cover.png")

    delivery = manifest.get("delivery") if isinstance(manifest.get("delivery"), dict) else {}
    lines = [audio.Line(s, t, str(delivery.get(s, ""))) for s, t in turns(script)]
    wav, engine, cast = audio.speech(lines, staging / "episode.wav", ctx.state["engine"], manifest["voices"])
    out = audio.to_mp3(wav)
    manifest.update(script=ctx.state["script_rel"], speech_engine=engine, voices=cast)
    return [out.name, *extra]


RECIPE = Recipe(
    name="podcast-episode",
    collection="podcasts",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("episode.md",),
    skills=("llm-writing", "humanizer"),
    cover_aspect=None,  # the script's own cover is reused
    default_model="sonnet",
    timeout_s=3600,
    requires=("speech",),
    prepare=prepare,
    validate=validate,
    after_cover=after_cover,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
