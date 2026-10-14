"""Faked-engine checks for the Images A recipes. Run from the repo root."""
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from core import images, runner  # noqa: E402
from core.engines import EngineResult  # noqa: E402


def png():
    from PIL import Image
    b = io.BytesIO()
    Image.new("RGB", (64, 64), (9, 9, 9)).save(b, format="PNG")
    return b.getvalue()


def load(name):
    spec = importlib.util.spec_from_file_location(f"r_{name}", ROOT / "recipes" / name / "run.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


SCRIPT = "---\ntitle: T\n---\n# T\n\n## Panel 1\nx\n\n## Panel 2\nx\n\n## Panel 3\nx\n\n## Panel 4\nx\n"
CASES = {
    "comics": ("script.md", SCRIPT, {"title": "T", "summary": "s", "series": "S", "topic": "t", "images": [
        {"file": "comic.png", "aspect": "16:9", "prompt": "four panels"}]},
        ("script.md", SCRIPT.replace("## Panel 4\nx\n", ""))),
    "ai-meme-generator": ("meme.md", "# m", {"title": "M", "summary": "a / b", "theme": "gaming", "images": [
        {"file": "meme.png", "aspect": "1:1", "prompt": "cat"}]}, "badaspect"),
    "poster": ("poster.md", "# p", {"title": "P", "summary": "c", "theme": "Art Nouveau", "style": "s", "images": [
        {"file": "poster.png", "aspect": "2:3", "prompt": "poster"}]}, "badaspect"),
    "future-cities": ("city.md", "# c", {"title": "C", "summary": "c", "city": "Lisbon", "images": [
        {"file": "cityscape.png", "aspect": "16:9", "prompt": "city"}]}, "badaspect"),
}


def run_case(mod, main, body, reply, out):
    class Engine:
        name = "claude"
        def preflight(self): pass
        def run(self, req):
            (req.workdir / main).write_text(body, encoding="utf-8")
            return EngineResult(text="```json\n" + json.dumps(reply) + "\n```", model="m")

    with mock.patch.object(runner, "get_engine", return_value=Engine()), \
            mock.patch.dict("os.environ", {"GEMINI_API_KEY": "k", "OPENAI_API_KEY": ""}), \
            mock.patch.dict(images.ENGINES, {"gemini": ("GEMINI_API_KEY", lambda p, a, size=None: (png(), "fake"))}):
        return runner.run(mod.RECIPE, ["--output-dir", str(out), "--date", "2026-10-14"])


for name, (main, body, good, bad) in CASES.items():
    mod = load(name)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        if name == "ai-meme-generator":
            col = out / "ai-memes"
            col.mkdir()
            (col / "meme-ideas.md").write_text("- [ ] first idea\n- [ ] second\n", encoding="utf-8")
        assert run_case(mod, main, body, good, out) == 0, name
        man = json.loads(next(out.glob("*/*/*/artifact.json")).read_text(encoding="utf-8"))
        img = man["files"]["images"][0]
        assert (next(out.glob("*/*/*/artifact.json")).parent / img).is_file(), (name, img)
        if name == "ai-meme-generator":
            ideas = (out / "ai-memes" / "meme-ideas.md").read_text(encoding="utf-8")
            assert "- [x] first idea — meme: 2026-10/2026-10-14_m" in ideas and "- [ ] second" in ideas, ideas
        # bad: wrong aspect, or for comics a 3-panel script
        if bad == "badaspect":
            b_reply = dict(good, images=[dict(good["images"][0], aspect="4:3")])
            b_main, b_body = main, body
        else:
            b_reply, (b_main, b_body) = good, bad
    with tempfile.TemporaryDirectory() as tmp:
        assert run_case(mod, b_main, b_body, b_reply, Path(tmp)) == 1, f"{name} bad case should fail"
        assert not list(Path(tmp).glob("*/*/*/artifact.json")), name
    print(f"{name}: good publishes ({img}), bad rejected")
print("ALL OK")
