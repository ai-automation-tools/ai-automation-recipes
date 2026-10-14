"""Scratch: faked-engine runs of the IMAGES B recipes (good run publishes, bad run fails)."""
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from PIL import Image  # noqa: E402

from core import images, runner  # noqa: E402
from core.engines import EngineResult  # noqa: E402

SIZES = {"1:1": (1024, 1024), "3:2": (1536, 1024), "16:9": (1376, 768), "2:3": (1024, 1536)}


def fake_image(prompt, aspect, size=None):
    buf = io.BytesIO()
    Image.new("RGB", SIZES.get(aspect, (800, 800)), (40, 90, 160)).save(buf, format="PNG")
    return buf.getvalue(), "fake-model"


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "recipes" / name / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RECIPE


def go(recipe, write, reply, date="2026-10-17"):
    class Engine:
        name = "claude"
        def preflight(self): pass
        def run(self, req):
            write(req.workdir, req.prompt)
            r = reply(req.prompt) if callable(reply) else reply
            return EngineResult(text="```json\n" + json.dumps(r) + "\n```", model="fake")

    out = Path(tempfile.mkdtemp())
    with mock.patch.object(runner, "get_engine", return_value=Engine()), \
            mock.patch.dict("os.environ", {"GEMINI_API_KEY": "k", "OPENAI_API_KEY": ""}), \
            mock.patch.dict(images.ENGINES, {"gemini": ("GEMINI_API_KEY", fake_image)}):
        code = runner.run(recipe, ["--output-dir", str(out), "--date", date])
    return code, out


def published(out, collection):
    return [p.parent for p in (out / collection).glob("*/*/artifact.json")]


results = {}

# --- image-prompt-packs ---------------------------------------------------
r = load("image-prompt-packs")
imgs = [{"file": f"p{i}.png", "prompt": f"prompt {i}", "aspect": a} for i, a in enumerate(["16:9", "1:1", "2:3", "3:2", "9:16"], 1)]
md = "---\ntitle: T\n---\n# T\n\nIntro.\n" + "".join(f"\n## P{i}\n\n![P{i}](images/p{i}.png)\n> prompt {i}\n" for i in range(1, 6))
code, out = go(r, lambda d, p: (d / "pack.md").write_text(md, encoding="utf-8"),
               {"title": "T", "slug": "t", "summary": "s", "theme": "Steampunk", "images": imgs})
f = published(out, "image-prompt-packs")
assert code == 0 and f and (f[0] / "images" / "p5.png").is_file() and (f[0] / "cover.png").is_file(), code
art = json.loads((f[0] / "artifact.json").read_text(encoding="utf-8"))
assert art["files"]["cover"] == "cover.png" and len(art["files"]["images"]) == 5, art["files"]
code, out = go(r, lambda d, p: (d / "pack.md").write_text(md, encoding="utf-8"),
               {"title": "T", "slug": "t", "summary": "s", "theme": "x", "images": imgs[:3]})
assert code == 1 and not published(out, "image-prompt-packs")
results["image-prompt-packs"] = "ok"

# --- wallpaper-packs ------------------------------------------------------
r = load("wallpaper-packs")


def wall_reply(prompt):
    files = [ln.split("`")[1] for ln in prompt.splitlines() if "— file `" in ln]
    slugs = [x[:-4] for x in files]
    return {"title": "W", "slug": "w", "summary": "s", "themes": slugs,
            "images": [{"file": x, "prompt": "scene", "aspect": "1:1"} for x in files]}


code, out = go(r, lambda d, p: (d / "pack.md").write_text("# W\n", encoding="utf-8"), wall_reply)
f = published(out, "wallpaper-packs")
assert code == 0 and f, code
desk = sorted((f[0] / "desktop").glob("*.png"))
mob = sorted((f[0] / "mobile").glob("*.png"))
assert len(desk) == 3 and len(mob) == 3
with Image.open(desk[0]) as a, Image.open(mob[0]) as b:
    assert a.size == (1024, 576) and b.size == (576, 1024), (a.size, b.size)
assert (f[0] / "cover.png").is_file()


def wall_bad(prompt):
    rep = wall_reply(prompt)
    rep["images"] = list(reversed(rep["images"]))
    return rep


code, out = go(r, lambda d, p: (d / "pack.md").write_text("# W\n", encoding="utf-8"), wall_bad)
assert code == 1 and not published(out, "wallpaper-packs")
results["wallpaper-packs"] = "ok (desktop 1024x576, mobile 576x1024)"

# --- icon-packs ------------------------------------------------------------
r = load("icon-packs")
names = [f"icon-{i}" for i in range(1, 13)]
icons = [{"name": n, "slug": n, "concept": "c", "tile_color": f"#{i * 20:02X}6699"} for i, n in enumerate(names, 1)]
good = "".join(f"=== ICON: {n} ===\n<circle cx=\"50\" cy=\"50\" r=\"{20 + i}\"/>\n<rect x=\"10\" y=\"80\" width=\"80\" height=\"8\" fill-opacity=\"0.5\"/>\n"
               for i, n in enumerate(names))
rep = {"title": "I", "slug": "i", "summary": "s", "theme": "t", "category": "c", "container": "squircle-tile",
       "glyph_color": "#fff", "icons": icons}
code, out = go(r, lambda d, p: ((d / "pack.md").write_text("# I\n", encoding="utf-8"),
                                (d / "glyphs.txt").write_text(good, encoding="utf-8")), rep)
f = published(out, "icon-packs")
assert code == 0 and f, code
assert len(list((f[0] / "svg").glob("*.svg"))) == 12 and len(list((f[0] / "png").glob("*.png"))) == 12
with Image.open(f[0] / "ico" / "icon-1.ico") as ico:
    assert (16, 16) in ico.info["sizes"] and (256, 256) in ico.info["sizes"], ico.info
with Image.open(f[0] / "png" / "icon-1.png") as png:
    assert png.size == (1024, 1024) and png.mode == "RGBA" and png.getpixel((0, 0))[3] == 0  # transparent corner
assert (f[0] / "cover.png").is_file()
bad = good.replace("<circle", "<text>A</text><circle", 3)  # 3 banned -> 9 valid < 10
code, out = go(r, lambda d, p: ((d / "pack.md").write_text("# I\n", encoding="utf-8"),
                                (d / "glyphs.txt").write_text(bad, encoding="utf-8")), rep)
assert code == 1 and not published(out, "icon-packs")
one_bad = good.replace("<circle", "<script/><circle", 1)  # 11 valid -> ships 11
code, out = go(r, lambda d, p: ((d / "pack.md").write_text("# I\n", encoding="utf-8"),
                                (d / "glyphs.txt").write_text(one_bad, encoding="utf-8")), rep)
f = published(out, "icon-packs")
assert code == 0 and len(list((f[0] / "svg").glob("*.svg"))) == 11
results["icon-packs"] = "ok (12 SVG/PNG/ICO, transparent; 11-of-12 ships; 9-of-12 fails)"

# --- weekend-yearly-collections ---------------------------------------------
r = load("weekend-yearly-collections")
plan_files = ["science-breakthroughs-2000.png", "technology-milestones-control-of-fire.png", "exoplanets-lhs-1140-b.png"]
entries = [{"collection": "science-breakthroughs", "key": "2000", "title": "2000"},
           {"collection": "technology-milestones", "key": "control-of-fire", "title": "Fire"},
           {"collection": "exoplanets", "key": "lhs-1140-b", "title": "LHS"}]
md = "# C\n" + "".join(f"![x](images/{x})\n" for x in plan_files)
crep = {"title": "C", "slug": "c", "summary": "s", "entries": entries,
        "images": [{"file": x, "prompt": "p", "aspect": "3:2"} for x in plan_files]}
code, out = go(r, lambda d, p: (d / "entries.md").write_text(md, encoding="utf-8"), crep)
f = published(out, "collections")
assert code == 0 and f and len(list((f[0] / "images").glob("*.png"))) == 3, code
assert (out / "collections" / "collections.json").is_file()

# second run, same output dir: progress moves to 2001 / stone-tools / k2-18-b
seen = {}


def capture(d, p):
    seen["prompt"] = p
    (d / "entries.md").write_text("x", encoding="utf-8")


class E:
    name = "claude"
    def preflight(self): pass
    def run(self, req):
        capture(req.workdir, req.prompt)
        return EngineResult(text='{"error": "stop here"}', model="m")


with mock.patch.object(runner, "get_engine", return_value=E()), \
        mock.patch.dict("os.environ", {"GEMINI_API_KEY": "k"}):
    runner.run(r, ["--output-dir", str(out), "--date", "2026-10-18"])
assert "science-breakthroughs-2001.png" in seen["prompt"] and "stone-tools" in seen["prompt"] and "k2-18-b" in seen["prompt"]

bad = dict(crep, entries=entries[:2])
code, out2 = go(r, lambda d, p: (d / "entries.md").write_text(md, encoding="utf-8"), bad)
assert code == 1 and not published(out2, "collections")

# all done -> exits 0 without calling the agent
cfg = json.loads((out / "collections" / "collections.json").read_text(encoding="utf-8"))
for c in cfg["collections"]:
    c["active"] = False
(out / "collections" / "collections.json").write_text(json.dumps(cfg), encoding="utf-8")
assert runner.run(r, ["--output-dir", str(out)]) == 0  # NothingToDo: skipped, agent never called
results["weekend-yearly-collections"] = "ok (seeds config, advances per collection, exits 0 when done)"

for k, v in results.items():
    print(f"{k}: {v}")
