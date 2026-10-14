"""Scratch: faked-engine end-to-end checks for the four audio recipes. No API spend.

    python test_audio_recipes.py <repo-root>
"""

import os

# Validators open a real browser when one is available; tests opt in explicitly (BrowserSmokeTests).
os.environ.setdefault("RECIPES_BROWSER_CHECK", "off")

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core import audio, images, runner  # noqa: E402
from core.engines import EngineResult  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(f"r_{name.replace('-', '_')}", ROOT / "recipes" / name / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def png(size=(64, 64)):
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", size, (40, 90, 160)).save(buf, format="PNG")
    return buf.getvalue()


ENV = {"GEMINI_API_KEY": "k", "ELEVENLABS_API_KEY": "k", "OPENAI_API_KEY": ""}
FAKE_IMG = {"gemini": ("GEMINI_API_KEY", lambda p, a, size=None: (png(), "fake-image"))}
fake_pcm = lambda text, voice, style="": b"\x01\x00" * 2400


class Engine:
    name = "claude"

    def __init__(self, write, reply):
        self.write, self.reply = write, reply

    def preflight(self):
        pass

    def run(self, req):
        self.write(req.workdir)
        return EngineResult(text="```json\n" + json.dumps(self.reply) + "\n```", model="fake")


def go(mod, engine, out, *args):
    with mock.patch.object(runner, "get_engine", return_value=engine), mock.patch.dict("os.environ", ENV), \
            mock.patch.dict(images.ENGINES, FAKE_IMG), mock.patch.object(audio, "_gemini_pcm", fake_pcm), \
            mock.patch.object(audio, "_elevenlabs_request", lambda path, body, accept: b"ID3fake"):
        return runner.run(mod.RECIPE, ["--output-dir", str(out), "--date", "2026-10-14", *args])


# --- song -----------------------------------------------------------------
SONG_MD = """---
title: "Paper Boats"
date: 2026-10-14
song_type: folk
genre: folk / chamber folk
mood: hushed
theme: a letter never sent
tempo_bpm: 72
key: D major
length_sec: pending
engine: ElevenLabs Music
---

# Paper Boats

> A letter read aloud, verse by verse.

## [Verse 1]
I folded every word you never heard
and set them on the river by the mill

## [Chorus]
paper boats paper boats
carry what I could not say
"""


def song_plan(text="[Verse 1]\nI folded every word you never heard", total=180000):
    return {"chunks": [
        {"text": text, "duration_ms": total // 2, "positive_styles": ["folk"], "negative_styles": ["muddy mix"]},
        {"text": "[Chorus]\npaper boats paper boats", "duration_ms": total - total // 2,
         "positive_styles": ["folk"], "negative_styles": ["muddy mix"]}]}


def song_writer(plan, md=SONG_MD):
    def w(d):
        (d / "song.md").write_text(md, encoding="utf-8")
        (d / "composition-plan.json").write_text(json.dumps(plan), encoding="utf-8")
    return w


SONG_REPLY = {"title": "Paper Boats", "slug": "paper-boats", "summary": "A letter read aloud.", "song_type": "folk",
              "genre": "folk", "stance": "Fingerpicked chamber folk", "mood": "hushed", "key": "D major",
              "tempo_bpm": 72, "target_ms": 180000, "word_cap": 260, "cover_prompt": "a paper boat at dusk"}


class SongTests(unittest.TestCase):
    def test_publishes_mp3(self):
        mod, out = load("song-generator"), Path(tempfile.mkdtemp())
        self.assertEqual(go(mod, Engine(song_writer(song_plan()), SONG_REPLY), out, "--type", "folk"), 0)
        art = next(out.glob("songs/*/*/artifact.json"))
        data = json.loads(art.read_text(encoding="utf-8"))
        self.assertEqual(data["files"]["song"], "song.mp3")
        self.assertTrue((art.parent / "song.mp3").is_file())
        self.assertEqual(data["fields"]["plan_ms"], 180000)
        self.assertGreater(data["fields"]["lyric_words"], 10)

    def test_rejects_digit_short_plan_and_over_cap(self):
        mod = load("song-generator")
        for writer, reply in [
            (song_writer(song_plan("[Verse 1]\nback in 1999")), SONG_REPLY),
            (song_writer(song_plan(total=120000)), SONG_REPLY),
            (song_writer(song_plan(), SONG_MD + "\n## [Verse 2]\n" + " ".join(["river"] * 300)), SONG_REPLY),
            (song_writer({"sections": []}), SONG_REPLY),
        ]:
            out = Path(tempfile.mkdtemp())
            self.assertEqual(go(mod, Engine(writer, reply), out, "--type", "folk"), 1)
            self.assertFalse(list(out.glob("songs/*/*/artifact.json")))


# --- podcast pair -----------------------------------------------------------
def script_md():
    lines = ["# Is Time Travel Possible?", "", "**Date**: 2026-10-14", "**Host**: Max Volume",
             "**Cast**: Doc Ruler, Sunny Skye", "", "## Topic Description", "", "Can we go back?", "", "## Script", ""]
    order = ["Max Volume", "Doc Ruler", "Sunny Skye"] * 5 + ["Max Volume"]
    filler = " ".join(["word"] * 110)
    for s in order:
        lines += [f"### {s}", "", f"(laughs) {filler}", ""]
    return "\n".join(lines)


class PodcastPairTests(unittest.TestCase):
    def test_script_then_render_then_nothing(self):
        out = Path(tempfile.mkdtemp())
        script_mod, audio_mod = load("podcast-script-generator"), load("podcast-episode")

        def write_script(d):
            (d / "script.md").write_text(script_md(), encoding="utf-8")
            (d / "cast.md").write_text("## Max Volume\nhost\n", encoding="utf-8")

        reply = {"title": "Is Time Travel Possible?", "slug": "time-travel", "summary": "s", "topic": "Time travel",
                 "host": "Max Volume", "cast": [], "word_count": 0, "cover_prompt": "a clock"}
        self.assertEqual(go(script_mod, Engine(write_script, reply), out), 0)

        # bad cast: a guest who speaks only twice fails
        def bad(d):
            (d / "script.md").write_text(script_md().replace("### Sunny Skye", "### Sunny Sky", 3), encoding="utf-8")
            (d / "cast.md").write_text("x", encoding="utf-8")
        self.assertEqual(go(script_mod, Engine(bad, reply), Path(tempfile.mkdtemp())), 1)

        voices = {"Max Volume": "Puck", "Doc Ruler": "Charon", "Sunny Skye": "Aoede"}
        render_reply = {"title": "Is Time Travel Possible?", "slug": "time-travel", "summary": "s", "voices": voices,
                        "delivery": {"Max Volume": "with gameshow energy"}}
        write_notes = lambda d: (d / "episode.md").write_text("# Episode\n", encoding="utf-8")

        # bad voices: one not a preset
        self.assertEqual(go(audio_mod, Engine(write_notes, {**render_reply, "voices": {**voices, "Doc Ruler": "Clone"}}), out), 1)
        self.assertEqual(go(audio_mod, Engine(write_notes, render_reply), out), 0)
        art = next(out.glob("podcasts/*/*/artifact.json"))
        data = json.loads(art.read_text(encoding="utf-8"))
        self.assertTrue(data["fields"]["script"].startswith("podcast-scripts/"))
        self.assertTrue((art.parent / data["files"]["episode"]).is_file())
        self.assertEqual(data["files"]["cover"], "cover.png")
        self.assertTrue((art.parent / "script.md").is_file())

        # Nothing left to render: the runner skips cleanly (exit 0) and publishes nothing new.
        before = len(list(out.glob("podcasts/*/*/artifact.json")))
        self.assertEqual(go(audio_mod, Engine(write_notes, render_reply), out), 0)
        self.assertEqual(len(list(out.glob("podcasts/*/*/artifact.json"))), before)


# --- voiceover ----------------------------------------------------------------
def vo_writer(words=300):
    body = " ".join(["Lorem"] * (words // 2)) + "\n\n" + " ".join(["ipsum"] * (words - words // 2))
    md = (f"# The Vanishing Ledger\n\n**Category**: Historical Scams\n\n---\n\n{body}\n\n---\n\n## Sources\n\n"
          "- [A](https://a.example/one)\n- [B](https://b.example/two)\n")

    def w(d):
        (d / "script.md").write_text(md, encoding="utf-8")
        (d / "direction-notes.md").write_text("# Direction Notes\n\n## Tone\nlow\n", encoding="utf-8")
    return w


VO_REPLY = {"title": "The Vanishing Ledger", "slug": "vanishing-ledger", "summary": "s", "category": "historical-scams",
            "topic": "A scam", "word_count": 300, "narrator": "Charon", "delivery": "with low urgency",
            "cover_prompt": "a ledger", "images": [{"file": f"scene-{i}.png", "prompt": f"beat {i}", "aspect": "9:16"}
                                                    for i in range(1, 5)]}


class VoiceoverTests(unittest.TestCase):
    def test_publishes_audio_and_short(self):
        mod, out = load("voiceover-script-generator"), Path(tempfile.mkdtemp())
        self.assertEqual(go(mod, Engine(vo_writer(), VO_REPLY), out, "--speech-engine", "gemini"), 0)
        art = next(out.glob("voiceover-scripts/*/*/artifact.json"))
        files = json.loads(art.read_text(encoding="utf-8"))["files"]
        self.assertEqual(len(files["images"]), 4)
        self.assertTrue(any(k.startswith("voiceover") for k in files))
        if shutil.which("ffmpeg"):
            self.assertEqual(files["short"], "short.mp4")

    def test_rejects_wrong_engine_voice_and_short_script(self):
        mod = load("voiceover-script-generator")
        self.assertEqual(go(mod, Engine(vo_writer(), {**VO_REPLY, "narrator": "Rachel"}), Path(tempfile.mkdtemp()),
                            "--speech-engine", "gemini"), 1)
        self.assertEqual(go(mod, Engine(vo_writer(100), VO_REPLY), Path(tempfile.mkdtemp()),
                            "--speech-engine", "gemini"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
