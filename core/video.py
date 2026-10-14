"""Optional video output: a slideshow of images over an audio track, via ffmpeg.

Every function here is a no-op that returns None when ffmpeg isn't installed, so a recipe can
offer video without requiring it.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

log = logging.getLogger(__name__)


def available() -> bool:
    return shutil.which("ffmpeg") is not None


def duration_s(audio: Path) -> float:
    """Length of a WAV (stdlib) or any other file (ffprobe)."""
    if audio.suffix.lower() == ".wav":
        with wave.open(str(audio)) as wf:
            return wf.getnframes() / wf.getframerate()
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)],
                         capture_output=True, text=True)
    return float(out.stdout.strip() or 0)


def slideshow(images: list[Path], audio: Path, out: Path, size: tuple[int, int] = (1080, 1920)) -> Path | None:
    """Show `images` in order for equal shares of `audio`, cropped to fill `size`. Vertical by default."""
    if not available():
        log.warning("ffmpeg not found — skipping %s", out.name)
        return None
    if not images:
        raise ValueError("slideshow needs at least one image")
    per = max(duration_s(audio) / len(images), 0.5)
    w, h = size
    with tempfile.TemporaryDirectory() as tmp:
        listing = Path(tmp) / "images.txt"
        rows = [f"file '{p.resolve().as_posix()}'\nduration {per:.3f}" for p in images]
        rows.append(f"file '{images[-1].resolve().as_posix()}'")  # concat demuxer needs the last frame twice
        listing.write_text("\n".join(rows) + "\n", encoding="utf-8")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-i", str(audio),
               "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},format=yuv420p",
               "-r", "30", "-c:v", "libx264", "-c:a", "aac", "-shortest", str(out)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        log.warning("ffmpeg failed, no video: %s", proc.stderr[-400:])
        return None
    log.info("VIDEO_OK %s", out)
    return out
