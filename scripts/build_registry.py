#!/usr/bin/env python3
"""Build the Cronsole registry for these recipes.

Collects every `recipes/*/cronsole.json` plus `cronsole/*.json`, checks each
against the Registry v1 rules Cronsole enforces, and writes:

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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "registry"

PACK = {
    "id": "ai-recipes",
    "name": "AI Content Recipes",
    "description": "Scheduled Claude Code automations that research, write, build and illustrate — "
                   "app idea cards, playable browser games, short stories — into a folder you can browse.",
}

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
    used = set(re.findall(r"\{\{(\w+)\}\}", t.get("commandTemplate", "")))
    req(used <= keys, f"placeholders without parameters: {sorted(used - keys)}")
    return errs


def dump(obj: object) -> bytes:
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def build() -> dict[Path, bytes]:
    sources = sorted(ROOT.glob("recipes/*/cronsole.json")) + sorted((ROOT / "cronsole").glob("*.json"))
    templates, errors = [], []
    for src in sources:
        t = json.loads(src.read_text(encoding="utf-8"))
        errors += validate(t, src)
        templates.append(t)
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

    pack_rel = f"packs/{PACK['id']}.json"
    pack_body = dump({"cronsoleCatalogVersion": "1.0", "pack": PACK,
                      "templates": sorted(templates, key=lambda t: t["id"])})
    files[OUT / pack_rel] = pack_body
    index = {
        "registryVersion": "1.0",
        "templates": entries,
        "packs": [{**PACK, "templateIds": [e["id"] for e in entries], "path": pack_rel,
                   "sha256": hashlib.sha256(pack_body).hexdigest()}],
    }
    files[OUT / "index.json"] = dump(index)
    return files


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
    print(f"registry: {len(files) - 2} templates, 1 pack -> {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
