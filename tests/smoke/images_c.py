"""Faked-engine checks for the two recipes whose images are optional: alternate-history (eight
scenes) and agent-persona-original (a square avatar). Each runs three ways: with a key and a good
reply (images published), with a key and a bad reply (rejected), and with no key at all (publishes
text-only). Run from the repo root."""
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


STORY = "---\ntitle: T\n---\n\n## Synopsis\n\nx\n\n" + "".join(f"## {i}. Section {i}\n\nx\n\n" for i in range(1, 9))
SCENES = "# Scene prompts — T\n\n**Shared style:** s\n\n" + "".join(f"## {i}. Section {i}\n\nscene {i}\n\n" for i in range(1, 9))
CARD = ("---\ntitle: Nia\ntags:\n  - nurse\n---\n\n## Purpose\n\nA night nurse who argues from triage.\n\n"
        "## Persona\n\nYou are Nia.\n")

AH_GOOD = {"title": "T", "slug": "t", "summary": "s", "era": "1900s", "divergence_point": "d", "cover_prompt": "c",
           "images": [{"file": f"0{i}-s.png", "prompt": f"scene {i}", "aspect": "16:9"} for i in range(1, 9)]}
AP_GOOD = {"title": "Nia", "slug": "nia", "summary": "s", "archetype_group": "Everyday-Archetypes",
           "subcategory": "nurse", "cover_prompt": "c", "images": [{"file": "avatar.png", "prompt": "face", "aspect": "1:1"}]}

CASES = {
    "alternate-history": ({"story.md": STORY, "scene-prompts.md": SCENES}, AH_GOOD,
                          dict(AH_GOOD, images=AH_GOOD["images"][:7]), "scenes/01-s.png"),
    "agent-persona-original": ({"persona.md": CARD}, AP_GOOD,
                               dict(AP_GOOD, images=[dict(AP_GOOD["images"][0], aspect="16:9")]), "avatar.png"),
}


def run_case(mod, files, reply, out, key):
    class Engine:
        name = "claude"
        skills_dir = ".claude/skills"
        def preflight(self): pass
        def run(self, req):
            for name, body in files.items():
                (req.workdir / name).write_text(body, encoding="utf-8")
            return EngineResult(text="```json\n" + json.dumps(reply) + "\n```", model="m")

    with mock.patch.object(runner, "get_engine", return_value=Engine()), \
            mock.patch.dict("os.environ", {"GEMINI_API_KEY": key, "OPENAI_API_KEY": ""}), \
            mock.patch.dict(images.ENGINES, {"gemini": ("GEMINI_API_KEY", lambda p, a, size=None: (png(), "fake"))}):
        return runner.run(mod.RECIPE, ["--output-dir", str(out), "--date", "2026-10-14"])


for name, (files, good, bad, first_image) in CASES.items():
    mod = load(name)
    with tempfile.TemporaryDirectory() as tmp:
        assert run_case(mod, files, good, Path(tmp), "k") == 0, name
        folder = next(Path(tmp).glob("*/*/*/artifact.json")).parent
        man = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))
        assert man["files"]["images"][0] == first_image, man["files"]
        assert all((folder / i).is_file() for i in man["files"]["images"]), name
        assert (folder / "cover.png").is_file(), name
    with tempfile.TemporaryDirectory() as tmp:
        assert run_case(mod, files, bad, Path(tmp), "k") == 1, f"{name} bad case should fail"
        assert not list(Path(tmp).glob("*/*/*/artifact.json")), name
    with tempfile.TemporaryDirectory() as tmp:
        assert run_case(mod, files, good, Path(tmp), "") == 0, f"{name} should publish without a key"
        folder = next(Path(tmp).glob("*/*/*/artifact.json")).parent
        man = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))
        assert not man["files"].get("images") and not (folder / "cover.png").exists(), man["files"]
    print(f"{name}: good publishes {len(good['images'])} image(s), bad rejected, keyless publishes text-only")
print("ALL OK")
