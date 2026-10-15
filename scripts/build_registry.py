#!/usr/bin/env python3
"""Build the Cronsole registry for these recipes.

Collects every `recipes/*/cronsole.json` plus `cronsole/*.json`, generates the
Cronsole edition of each recipe in NATIVE (a self-contained script template built
from `cronsole/native-body.py` that fetches the pinned runtime bundle), checks
each against the Registry v1 rules Cronsole enforces, and writes:

    registry/templates/<id>.json   one template per file
    registry/packs/ai-recipes.json the whole set as one importable bundle
    registry/index.json            manifest with a sha256 per file

Files are LF and deterministic (no timestamps), because Cronsole verifies each
file's sha256 over its exact bytes. `--check` rebuilds in memory and exits 1 if
the committed registry is stale — run it in CI.

    python scripts/build_registry.py [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "registry"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_bundle  # noqa: E402
from core.engines import engine_names  # noqa: E402

# Recipes with a Cronsole edition (`recipe-<name>-cronsole`). A pilot set for now; every recipe
# joins once these three have run in Cronsole for real.
NATIVE = ["short-story", "comics", "podcast-episode"]
NATIVE_BODY = ROOT / "cronsole" / "native-body.py"
NATIVE_TIMEOUT_MAX = 3600  # Cronsole caps a native job at 60 minutes
# Keys a parameter can call for; each becomes an optional Cronsole secret on the task.
KEY_ENVS = {"imageEngine": ["GEMINI_API_KEY", "OPENAI_API_KEY"],
            "speechEngine": ["GEMINI_API_KEY", "ELEVENLABS_API_KEY"]}
NATIVE_PACK = {
    "id": "ai-recipes-cronsole",
    "name": "AI Recipes: Cronsole editions",
    "description": "Recipes as self-contained Cronsole script templates: no clone, no .env. Each run fetches "
                   "a pinned, checksummed runtime once and reads its API keys from the task's secrets.",
}

ALL_PACK = {
    "id": "ai-recipes",
    "name": "AI Content Recipes",
    "description": "Every recipe: scheduled Claude Code automations that research, write, build and "
                   "illustrate into a folder you can browse.",
}

# Category packs. Membership is declared, never derived from tags, so a pack only changes when
# this list does. Every pack also carries the support templates: the clone updater the recipes
# depend on and the viewer rebuild.
SUPPORT = ["recipe-recipes-update", "recipe-viewer-rebuild"]
CATEGORY_PACKS = [
    ("ai-recipes-apps-games", "AI Recipes: Apps & Games",
     "Idea cards, runnable app and extension prototypes, playable games, game and 3D-print concepts.",
     ["app-idea-card", "app-prototype", "browser-extension", "finance-app-prototype", "iam-prototype",
      "browser-game", "mobile-game", "pc-game-concept", "3d-print-design"]),
    ("ai-recipes-writing", "AI Recipes: Writing",
     "Short stories, a serialized novella, alternate histories, persona cards for known figures and "
     "original characters, satirical news and content ideas.",
     ["short-story", "serialized-novella", "alternate-history", "agent-persona", "agent-persona-original",
      "satirical-news", "content-idea-gen", "funny-ai-content"]),
    ("ai-recipes-food-maps", "AI Recipes: Food & Maps",
     "Safety-checked recipes with a printable Cook's Card, a viral-recipe recreator, and researched interactive maps.",
     ["family-recipe", "regional-recipe", "viral-recipe", "ai-map"]),
    ("ai-recipes-digests", "AI Recipes: Research Digests",
     "Researched roundups — AI tools, agent tooling, open source, security and finance tooling, "
     "trending repos, useful sites and reading lists, with browser bookmarks — plus a sourced AI "
     "model benchmark briefing, a ten-topic news digest written from RSS feeds and an eight-topic "
     "finance digest.",
     ["agent-toolkit", "ai-stack-radar", "oss-spotlight", "cool-websites", "top-10-github-repos",
      "trending-movers", "signal-sources", "security-toolkit", "finance-toolkit",
      "model-benchmark-watch", "news-digest", "finance-digest"]),
    ("ai-recipes-images", "AI Recipes: Images",
     "Comics, memes, posters, news collages, cityscapes, prompt packs, paired desktop and phone "
     "wallpapers, SVG icon packs and long-running yearly image collections.",
     ["comics", "ai-meme-generator", "poster", "news-collage", "future-cities", "image-prompt-packs",
      "wallpaper-packs", "icon-packs", "image-collections"]),
    ("ai-recipes-audio", "AI Recipes: Audio",
     "Songs composed from AI-written lyrics, a two-step debate podcast, and narrated voiceover shorts — "
     "preset voices only.",
     ["song-generator", "podcast-script-generator", "podcast-episode", "voiceover-script-generator"]),
    ("ai-recipes-repo-ops", "AI Recipes: Repo Ops",
     "Automations that work on a repo you name: a pull-request review pass and one small additive "
     "enhancement to a static app, both report-only unless you turn the side effects on.",
     ["pr-review", "app-enhancement"]),
]


# Mirrors cronsole backend/src/catalog/schema.ts (Registry v1).
RUNTIMES = {"powershell", "batch", "bash", "zsh", "python", "node", "applescript", "vbscript", "executable", "http", "ai-prompt"}
OS_TARGETS = {"windows", "macos", "linux", "cross-platform"}
CATEGORIES = {"backup", "cleanup", "monitoring", "dev-workflow", "data-sync", "ai-agent", "notification", "media", "system", "other"}
TARGETS = {"windows", "cronsole-native", "macos", "linux", "claude-code", "chatgpt", "gemini"}
ID_RE = re.compile(r"^[a-z0-9]+([_-][a-z0-9]+)*$")
KEY_RE = re.compile(r"^\w+$")


def validate(t: dict, src: Path) -> list[str]:
    errs = []
    req = lambda c, msg: None if c else errs.append(f"{src.relative_to(ROOT)}: {msg}")
    req(t.get("schemaVersion") == "1.0", "schemaVersion must be '1.0'")
    req(isinstance(t.get("id"), str) and ID_RE.match(t["id"]), "invalid id")
    req(bool(t.get("name")), "name is required")
    req(t.get("runtime") in RUNTIMES | {None}, f"runtime {t.get('runtime')!r} not allowed")
    req(t.get("os") in OS_TARGETS | {None}, f"os {t.get('os')!r} not allowed")
    req(t.get("category") in CATEGORIES | {None}, f"category {t.get('category')!r} not allowed")
    trig = t.get("trigger") or {}
    req(trig.get("kind") == "schedule" and len(str(trig.get("cron", "")).split()) == 5, "trigger must be a 5-field schedule")
    req(bool(t.get("commandTemplate") or t.get("action")), "needs commandTemplate or action")
    targets = t.get("compatibleTargets") or []
    req(bool(targets) and set(targets) <= TARGETS, f"compatibleTargets invalid: {targets}")
    keys = set()
    for p in t.get("parameters") or []:
        req(KEY_RE.match(str(p.get("key", ""))), f"bad parameter key {p.get('key')!r}")
        keys.add(p.get("key"))
        for fld in ("default",):
            req(fld not in p or isinstance(p[fld], str), f"parameter {p.get('key')}: {fld} must be a string")
    used = set(re.findall(r"\{\{(\w+)\}\}", t.get("commandTemplate", "") + (t.get("action") or {}).get("body", "")))
    req(used <= keys, f"placeholders without parameters: {sorted(used - keys)}")
    return errs


def py_value(token: str) -> str:
    """A command-line token as Python source. A {{param}} is pasted raw by Cronsole, so it goes in a
    raw string with a sentinel: a Windows path ending in a backslash can't end the string early."""
    if "{{" in token:
        return f"r'''{token}|'''[:-1]"
    return repr(token)


def native(t: dict, recipe: str, version: str, digest: str) -> dict:
    """The Cronsole edition of a recipe's clone-based template."""
    tokens = shlex.split(t["commandTemplate"])
    args = tokens[next(i for i, tok in enumerate(tokens) if tok.endswith("/run.py")) + 1:]
    args += ["--engine", "{{engine}}"]
    params = [dict(p) for p in t.get("parameters", []) if p["key"] != "recipesPath"]
    for p in params:
        if p["key"] == "model":
            p.update(type="text", label="Model",
                     help="A Claude alias (sonnet, opus, haiku) or the chosen CLI's own model id. On a CLI other "
                          "than Claude, a Claude alias means that CLI's default model.")
            p.pop("options", None)
    params.append({"key": "engine", "label": "Agent CLI", "type": "select", "default": "claude", "required": True,
                   "options": engine_names(),
                   "help": "Which agent CLI runs the recipe. It must be installed and signed in where Cronsole runs."})
    keys = sorted({k for p in params for k in KEY_ENVS.get(p["key"], [])})
    body = NATIVE_BODY.read_text(encoding="utf-8")
    for marker, value in {"__NAME__": t["name"], "__RECIPE__": recipe, "__VERSION__": version,
                          "__BUNDLE_URL__": build_bundle.bundle_url(version), "__BUNDLE_SHA256__": digest,
                          "__ARGS__": "[" + ", ".join(py_value(a) for a in args) + "]",
                          "__KEYS__": "{" + ", ".join(f"{k!r}: \"${{secret.{k}?}}\"" for k in keys) + "}"}.items():
        body = body.replace(marker, value)
    timeout = min(int((t.get("execution") or {}).get("timeoutSec") or 1800), NATIVE_TIMEOUT_MAX)
    secrets = f" Optional task secrets: {', '.join(keys)}." if keys else ""
    return {
        "schemaVersion": "1.0",
        "id": f"recipe-{recipe}-cronsole",
        "name": f"{t['name']} (Cronsole)",
        "description": f"{t['description']} Cronsole edition: no clone or .env needed. The first run fetches "
                       f"runtime {version} (sha256-pinned) into your cache; the agent CLI is swappable.{secrets}",
        "runtime": "python",
        "os": "cross-platform",
        "category": t.get("category"),
        "tags": sorted(set(t.get("tags", [])) | {"cronsole-native"}),
        "icon": t.get("icon"),
        "trigger": t["trigger"],
        "action": {"kind": "script", "interpreter": "python", "body": body},
        "parameters": params,
        "compatibleTargets": ["cronsole-native"],
        "execution": {"timeoutSec": timeout, "retries": 0},
        "author": t.get("author", "ai-automation-tools"),
        "version": version,
    }


def dump(obj: object) -> bytes:
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def build() -> dict[Path, bytes]:
    sources = sorted(ROOT.glob("recipes/*/cronsole.json")) + sorted((ROOT / "cronsole").glob("*.json"))
    templates, errors = [], []
    for src in sources:
        t = json.loads(src.read_text(encoding="utf-8"))
        errors += validate(t, src)
        templates.append(t)
    version, digest = build_bundle.version(), build_bundle.sha256()
    for recipe in NATIVE:
        src = ROOT / "recipes" / recipe / "cronsole.json"
        n = native(json.loads(src.read_text(encoding="utf-8")), recipe, version, digest)
        n = {k: v for k, v in n.items() if v is not None}
        errors += validate(n, src)
        templates.append(n)
    ids = [t["id"] for t in templates]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append(f"duplicate template ids: {sorted(dupes)}")
    if errors:
        raise SystemExit("Registry validation failed:\n  " + "\n  ".join(errors))

    files: dict[Path, bytes] = {}
    entries = []
    for t in sorted(templates, key=lambda t: t["id"]):
        rel = f"templates/{t['id']}.json"
        body = dump(t)
        files[OUT / rel] = body
        entry = {
            "id": t["id"], "name": t["name"], "description": t.get("description"),
            "category": t.get("category"), "tags": t.get("tags", []),
            "runtime": t.get("runtime"), "os": t.get("os"),
            "compatibleTargets": t["compatibleTargets"],
            "path": rel, "sha256": hashlib.sha256(body).hexdigest(),
        }
        # Registry v1 optionals are absent-or-string; null fails Cronsole's parse.
        entries.append({k: v for k, v in entry.items() if v is not None})

    by_id = {t["id"]: t for t in templates}
    recipe_ids = {p.parent.name for p in ROOT.glob("recipes/*/cronsole.json")}
    grouped = {r for _, _, _, members in CATEGORY_PACKS for r in members}
    if recipe_ids - grouped:
        raise SystemExit(f"Recipes in no category pack: {sorted(recipe_ids - grouped)}")
    if grouped - recipe_ids:
        raise SystemExit(f"Category packs name missing recipes: {sorted(grouped - recipe_ids)}")

    packs = [(ALL_PACK, sorted(by_id)), (NATIVE_PACK, sorted(f"recipe-{r}-cronsole" for r in NATIVE))]
    for pid, name, desc, members in CATEGORY_PACKS:
        packs.append(({"id": pid, "name": name, "description": desc},
                      sorted([f"recipe-{m}" for m in members] + SUPPORT)))

    pack_entries = []
    for meta, ids in packs:
        rel = f"packs/{meta['id']}.json"
        body = dump({"cronsoleCatalogVersion": "1.0", "pack": meta, "templates": [by_id[i] for i in ids]})
        files[OUT / rel] = body
        pack_entries.append({**meta, "templateIds": ids, "path": rel, "sha256": hashlib.sha256(body).hexdigest()})

    index = {"registryVersion": "1.0", "templates": entries, "packs": pack_entries}
    files[OUT / "index.json"] = dump(index)
    return files


def entries_of(files: dict[Path, bytes]) -> list[Path]:
    return [p for p in files if p.parent.name == "templates"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="Exit 1 if registry/ is out of date.")
    args = ap.parse_args()

    files = build()
    existing = {p for p in OUT.rglob("*.json")} if OUT.exists() else set()
    stale = [p for p, b in files.items() if not p.exists() or p.read_bytes() != b]
    orphans = existing - set(files)

    if args.check:
        for p in stale + sorted(orphans):
            print(f"stale: {p.relative_to(ROOT)}")
        return 1 if stale or orphans else 0

    for p in orphans:
        p.unlink()
    for p, body in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(body)
    print(f"registry: {len(entries_of(files))} templates, {len(CATEGORY_PACKS) + 2} packs -> {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
