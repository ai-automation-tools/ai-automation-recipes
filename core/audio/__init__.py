"""Speech and music for recipes that publish audio.

Like covers, audio is rendered by the runner after the agent exits: the agent writes the script
or the composition plan, and this module turns it into sound with keys the agent never holds.

* speech() — one or more speakers, one line at a time. Engines: Gemini TTS (GEMINI_API_KEY) or
  ElevenLabs (ELEVENLABS_API_KEY). **Preset voices only** — premade library voices, never clones.
  Both engines are asked for 24 kHz 16-bit mono PCM, so lines join without ffmpeg.
* music()  — ElevenLabs Music from a composition plan the agent wrote.
* to_mp3() — encode a WAV with ffmpeg when it's installed; otherwise the WAV is the deliverable.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
import wave
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)

RATE = 24000  # Hz, 16-bit mono throughout

# Premade voices. Gemini's are prebuilt names; ElevenLabs' are its public library voices.
GEMINI_VOICES = ("Kore", "Puck", "Charon", "Fenrir", "Aoede", "Zephyr", "Leda", "Orus")
ELEVENLABS_VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Josh": "TxGEqnHWrfWFTfGW9XjX",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
}
SPEECH_ENGINES = {"gemini": "GEMINI_API_KEY", "elevenlabs": "ELEVENLABS_API_KEY"}


class AudioError(RuntimeError):
    """Speech or music could not be produced."""


@dataclass(frozen=True)
class Line:
    speaker: str
    text: str
    style: str = ""  # Gemini: "cheerfully", "in a hushed whisper"; ignored by ElevenLabs


def speech_engines() -> list[str]:
    return [e for e, env in SPEECH_ENGINES.items() if os.environ.get(env)]


def music_available() -> bool:
    return bool(os.environ.get("ELEVENLABS_API_KEY"))


def default_voices(speakers: list[str], engine: str) -> dict[str, str]:
    """Assign distinct preset voices to speakers in order of first appearance."""
    pool = list(GEMINI_VOICES) if engine == "gemini" else list(ELEVENLABS_VOICES)
    return {s: pool[i % len(pool)] for i, s in enumerate(speakers)}


def _retry(fn, what: str, attempts: int = 3):
    for i in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - retry transient API errors, surface the last
            msg = str(exc).lower()
            transient = any(t in msg for t in ("429", "rate", "500", "502", "503", "unavailable", "timeout"))
            if i == attempts or not transient:
                raise AudioError(f"{what} failed: {exc}") from exc
            time.sleep(2 ** i)


def _gemini_pcm(text: str, voice: str, style: str) -> bytes:
    from google import genai
    from google.genai import types

    if voice not in GEMINI_VOICES:
        raise AudioError(f"{voice!r} is not a preset Gemini voice ({', '.join(GEMINI_VOICES)})")
    model = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")
    client = genai.Client()  # keep a reference: a collected client closes its HTTP session
    prompt = f"Say {style}: {text}" if style else text
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice))),
        ),
    )
    return resp.candidates[0].content.parts[0].inline_data.data


def _elevenlabs_request(path: str, body: dict, accept: str) -> bytes:
    req = urllib.request.Request(
        f"https://api.elevenlabs.io{path}",
        data=json.dumps(body).encode(),
        method="POST",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json", "Accept": accept},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        raise AudioError(f"ElevenLabs {exc.code}: {exc.read().decode(errors='replace')[:300]}") from exc


def _elevenlabs_pcm(text: str, voice: str) -> bytes:
    voice_id = ELEVENLABS_VOICES.get(voice)
    if not voice_id:
        raise AudioError(f"{voice!r} is not a preset ElevenLabs voice ({', '.join(ELEVENLABS_VOICES)})")
    model = os.environ.get("ELEVENLABS_TTS_MODEL", "eleven_multilingual_v2")
    return _elevenlabs_request(
        f"/v1/text-to-speech/{voice_id}?output_format=pcm_24000",
        {"text": text, "model_id": model, "voice_settings": {"stability": 0.45, "similarity_boost": 0.8}},
        "audio/pcm",
    )


def speech(lines: list[Line], out: Path, engine: str = "auto", voices: dict[str, str] | None = None,
           gap_s: float = 0.35) -> tuple[Path, str, dict[str, str]]:
    """Render lines to a WAV. Returns (path, engine used, speaker->voice map)."""
    if not lines:
        raise AudioError("no lines to speak")
    if engine == "auto":
        available = speech_engines()
        if not available:
            raise AudioError("No speech engine configured: set GEMINI_API_KEY or ELEVENLABS_API_KEY")
        engine = available[0]
    if engine not in SPEECH_ENGINES:
        raise AudioError(f"Unknown speech engine {engine!r}")
    if not os.environ.get(SPEECH_ENGINES[engine]):
        raise AudioError(f"{SPEECH_ENGINES[engine]} is not set")

    speakers = list(dict.fromkeys(line.speaker for line in lines))
    cast = {**default_voices(speakers, engine), **(voices or {})}
    silence = b"\x00\x00" * int(RATE * gap_s)
    pcm = bytearray()
    for i, line in enumerate(lines, 1):
        voice = cast[line.speaker]
        if engine == "gemini":
            chunk = _retry(lambda: _gemini_pcm(line.text, voice, line.style), f"line {i} (gemini/{voice})")
        else:
            chunk = _retry(lambda: _elevenlabs_pcm(line.text, voice), f"line {i} (elevenlabs/{voice})")
        if not chunk:
            raise AudioError(f"line {i} came back empty")
        pcm += chunk + silence
        log.info("speech %d/%d (%s)", i, len(lines), voice)

    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(bytes(pcm))
    log.info("SPEECH_OK %s (%s, %.0fs)", out, engine, len(pcm) / 2 / RATE)
    return out, engine, cast


def music(plan: dict, out: Path) -> Path:
    """Compose a song from an ElevenLabs composition plan (v1 `sections` or v2 `chunks`)."""
    if not music_available():
        raise AudioError("ELEVENLABS_API_KEY is not set")
    parts = plan.get("sections") or plan.get("chunks")
    if not isinstance(parts, list) or not parts:
        raise AudioError("composition plan needs a non-empty `sections` (v1) or `chunks` (v2) list")
    total = sum(int(p.get("duration_ms") or p.get("durationMs") or 0) for p in parts)
    if not 3000 <= total <= 600000:
        raise AudioError(f"composition plan totals {total} ms; ElevenLabs accepts 3,000–600,000")
    model = os.environ.get("ELEVENLABS_MUSIC_MODEL", "music_v1" if "sections" in plan else "music_v2_5")
    audio = _retry(
        lambda: _elevenlabs_request("/v1/music?output_format=mp3_44100_128",
                                    {"composition_plan": plan, "model_id": model}, "audio/mpeg"),
        "music",
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(audio)
    log.info("MUSIC_OK %s (%s, %d KB)", out, model, len(audio) // 1024)
    return out


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def to_mp3(wav: Path, out: Path | None = None) -> Path:
    """Encode to MP3 with ffmpeg and delete the WAV; without ffmpeg, keep the WAV."""
    if not ffmpeg_available():
        log.warning("ffmpeg not found — publishing %s as WAV", wav.name)
        return wav
    out = out or wav.with_suffix(".mp3")
    proc = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(out)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise AudioError(f"ffmpeg failed: {proc.stderr[-500:]}")
    wav.unlink()
    return out


__all__ = ["AudioError", "ELEVENLABS_VOICES", "GEMINI_VOICES", "Line", "default_voices", "ffmpeg_available",
           "music", "music_available", "speech", "speech_engines", "to_mp3"]
