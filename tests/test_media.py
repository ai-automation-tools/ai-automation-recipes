"""Tests for Batch 2 media support: multi-image runs, image post-processing, audio, video.

Every API is faked; nothing here spends a key.

    python -m unittest discover -s tests
"""

from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import ImageSpec, runner, video  # noqa: E402
from core import audio, images  # noqa: E402
from core.engines import EngineResult  # noqa: E402
from core.images import process  # noqa: E402


def png_bytes(size=(64, 48), color=(200, 30, 30)) -> bytes:
    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, format="PNG")
    return buf.getvalue()


class MultiImageRunTests(unittest.TestCase):
    def make_recipe(self, **kw):
        prompt = Path(tempfile.mkdtemp()) / "prompt.md"
        prompt.write_text("{{RUN_CONTRACT}} {{OUTPUT_FILES}}", encoding="utf-8")
        return runner.Recipe(name="t", collection="things", version="0", prompt_path=prompt, files=("comic.md",),
                             cover_aspect=None, images=ImageSpec(min=2, max=3, aspects=("1:1", "2:3")), **kw)

    def run_with(self, recipe, reply, env):
        class Engine:
            name = "claude"
            def preflight(self): pass
            def run(self, req):
                (req.workdir / "comic.md").write_text("# T", encoding="utf-8")
                return EngineResult(text=json.dumps(reply), model="m")

        tmp = tempfile.mkdtemp()
        with mock.patch.object(runner, "get_engine", return_value=Engine()), \
                mock.patch.dict("os.environ", env), \
                mock.patch.dict(images.ENGINES, {"gemini": ("GEMINI_API_KEY", lambda p, a: (png_bytes(), "fake"))}):
            code = runner.run(recipe, ["--output-dir", tmp, "--date", "2026-10-14"])
        return code, Path(tmp)

    def test_renders_each_image_and_lists_them(self):
        reply = {"title": "T", "summary": "s", "images": [
            {"file": "panel-1.png", "prompt": "a cat", "aspect": "1:1"},
            {"file": "panel-2.png", "prompt": "a dog", "aspect": "2:3"}]}
        code, out = self.run_with(self.make_recipe(), reply, {"GEMINI_API_KEY": "k", "OPENAI_API_KEY": ""})
        self.assertEqual(code, 0)
        folder = out / "things" / "2026-10" / "2026-10-14_t"
        self.assertTrue((folder / "images" / "panel-2.png").is_file())
        files = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))["files"]
        self.assertEqual(files["images"], ["images/panel-1.png", "images/panel-2.png"])

    def test_rejects_bad_image_lists(self):
        bad = [
            [{"file": "a.png", "prompt": "x", "aspect": "1:1"}],                                      # too few
            [{"file": "a.png", "prompt": "x", "aspect": "1:1"}, {"file": "a.png", "prompt": "y"}],    # duplicate
            [{"file": "A.PNG", "prompt": "x"}, {"file": "b.png", "prompt": "y"}],                     # bad name
            [{"file": "a.png", "prompt": "x", "aspect": "16:9"}, {"file": "b.png", "prompt": "y"}],  # aspect
            [{"file": "../a.png", "prompt": "x"}, {"file": "b.png", "prompt": "y"}],                  # traversal
        ]
        for images_list in bad:
            code, out = self.run_with(self.make_recipe(), {"title": "T", "summary": "s", "images": images_list},
                                      {"GEMINI_API_KEY": "k", "OPENAI_API_KEY": ""})
            self.assertEqual(code, 1, images_list)
            self.assertFalse(list((out / "things").glob("*/*/artifact.json")))

    def test_preflight_fails_before_the_agent_without_keys(self):
        called = []

        class Engine:
            name = "claude"
            def preflight(self): pass
            def run(self, req):
                called.append(True)

        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(runner, "get_engine", return_value=Engine()), \
                mock.patch.dict("os.environ", {"GEMINI_API_KEY": "", "OPENAI_API_KEY": "", "ELEVENLABS_API_KEY": ""}):
            self.assertEqual(runner.run(self.make_recipe(), ["--output-dir", tmp]), 1)
            recipe = self.make_recipe(requires=("music",))
            self.assertEqual(runner.run(recipe, ["--output-dir", tmp, "--image-engine", "gemini"]), 1)
        self.assertEqual(called, [])


class ProcessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "src.png").write_bytes(png_bytes((1600, 900)))

    def tearDown(self):
        self.tmp.cleanup()

    def test_crop_to_aspect(self):
        from PIL import Image

        out = process.crop_to_aspect(self.d / "src.png", self.d / "phone.png", "9:16", width=540)
        with Image.open(out) as im:
            self.assertEqual(im.size, (540, 960))
        out = process.crop_to_aspect(self.d / "src.png", self.d / "square.png", "1:1")
        with Image.open(out) as im:
            self.assertEqual(im.size, (900, 900))

    def test_make_ico(self):
        from PIL import Image

        (self.d / "icon.png").write_bytes(png_bytes((256, 256)))
        out = process.make_ico(self.d / "icon.png", self.d / "icon.ico")
        with Image.open(out) as im:
            self.assertEqual(im.format, "ICO")
            self.assertIn((32, 32), im.info["sizes"])

    def test_svg_to_png(self):
        if not process.svg_renderer_available():
            self.skipTest("no SVG renderer installed")
        from PIL import Image

        (self.d / "i.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
                                      '<circle cx="12" cy="12" r="10" fill="#0af"/></svg>', encoding="utf-8")
        out = process.svg_to_png(self.d / "i.svg", self.d / "i.png", size=128)
        with Image.open(out) as im:
            self.assertEqual(im.size, (128, 128))


class AudioTests(unittest.TestCase):
    def test_speech_joins_lines_with_distinct_voices(self):
        seen = []

        def fake(text, voice, style=""):
            seen.append(voice)
            return b"\x01\x00" * 2400  # 0.1 s

        lines = [audio.Line("Host", "Hi"), audio.Line("Guest", "Hello"), audio.Line("Host", "Bye")]
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(audio, "_gemini_pcm", fake), \
                mock.patch.dict("os.environ", {"GEMINI_API_KEY": "k", "ELEVENLABS_API_KEY": ""}):
            out, engine, cast = audio.speech(lines, Path(tmp) / "ep.wav")
            with wave.open(str(out)) as wf:
                self.assertEqual(wf.getframerate(), audio.RATE)
                self.assertAlmostEqual(wf.getnframes() / audio.RATE, 3 * (0.1 + 0.35), places=2)
        self.assertEqual(engine, "gemini")
        self.assertEqual(seen[0], seen[2])
        self.assertNotEqual(seen[0], seen[1])
        self.assertEqual(cast, {"Host": seen[0], "Guest": seen[1]})

    def test_gemini_empty_response_is_retried(self):
        # A live podcast run died on line 36 of 42 when Gemini returned a candidate with no content.
        from types import SimpleNamespace as NS

        empty = NS(candidates=[NS(content=None, finish_reason="OTHER")])
        good = NS(candidates=[NS(content=NS(parts=[NS(inline_data=NS(data=b"\x01\x00" * 10))]))])
        calls = iter([empty, good])
        client = NS(models=NS(generate_content=lambda **kw: next(calls)))
        with mock.patch("google.genai.Client", return_value=client), mock.patch.object(audio.time, "sleep"), \
                mock.patch.dict("os.environ", {"GEMINI_API_KEY": "k", "ELEVENLABS_API_KEY": ""}):
            out, _, _ = audio.speech([audio.Line("A", "hi")], Path(tempfile.mkdtemp()) / "a.wav")
        self.assertTrue(out.is_file())

    def test_speech_rejects_non_preset_voices(self):
        with mock.patch.dict("os.environ", {"GEMINI_API_KEY": "k"}):
            with self.assertRaises(audio.AudioError):
                audio.speech([audio.Line("A", "x")], Path(tempfile.mkdtemp()) / "a.wav", engine="gemini",
                             voices={"A": "MyClonedVoice"})

    def test_music_checks_plan_and_posts_it(self):
        sent = {}

        def fake_request(path, body, accept):
            sent.update(path=path, body=body)
            return b"ID3fake-mp3"

        plan = {"positive_global_styles": ["folk"], "negative_global_styles": [],
                "sections": [{"section_name": "Verse", "duration_ms": 20000, "lines": ["la"],
                              "positive_local_styles": [], "negative_local_styles": []}]}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(audio, "_elevenlabs_request", fake_request), \
                mock.patch.dict("os.environ", {"ELEVENLABS_API_KEY": "k"}):
            out = audio.music(plan, Path(tmp) / "song.mp3")
            self.assertEqual(out.read_bytes(), b"ID3fake-mp3")
            self.assertEqual(sent["body"]["model_id"], "music_v1")
            with self.assertRaises(audio.AudioError):
                audio.music({"sections": [{"duration_ms": 100}]}, Path(tmp) / "x.mp3")  # too short


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
class VideoTests(unittest.TestCase):
    def test_slideshow(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.png").write_bytes(png_bytes((400, 300)))
            (d / "b.png").write_bytes(png_bytes((400, 300), (20, 20, 200)))
            with wave.open(str(d / "v.wav"), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(b"\x00\x00" * 24000)
            out = video.slideshow([d / "a.png", d / "b.png"], d / "v.wav", d / "short.mp4", size=(360, 640))
            self.assertIsNotNone(out)
            self.assertGreater(out.stat().st_size, 1000)
            # A live run overshot the audio by 18 s before the length was pinned.
            self.assertAlmostEqual(video.duration_s(out), 1.0, delta=0.15)


if __name__ == "__main__":
    unittest.main()
