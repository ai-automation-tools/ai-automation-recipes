"""Checks for recipes that ship runnable HTML/JS: every local reference exists, external
references are HTTPS (optionally from an allowlist), and every script parses under
`node --check` when Node is installed.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .runner import RecipeError

log = logging.getLogger("recipes")

REF_RE = re.compile(r"""<(script|link|img|audio|source|iframe)\b[^>]*?\b(?:src|href)\s*=\s*["']([^"']+)""", re.I)
INLINE_SCRIPT_RE = re.compile(r'''<script(?![^>]*\bsrc\s*=)(?![^>]*\btype\s*=\s*["']?(?!(?:text|application)/javascript\b|module\b)[\w/+.-]+)[^>]*>(.*?)</script>''', re.S | re.I)


def check_refs(
    staging: Path,
    page: str,
    *,
    https_prefixes: tuple[str, ...] | None = None,
    allow_external_scripts: bool = True,
    pending: tuple[str, ...] = (),
) -> None:
    """Reject a page that loads a missing local file or a disallowed URL.

    https_prefixes — if set, external URLs must start with one of these.
    pending        — local names the runner writes later (e.g. "cover.png").
    """
    html = (staging / page).read_text(encoding="utf-8")
    for tag, ref in REF_RE.findall(html):
        if ref.startswith(("data:", "#", "mailto:")):
            continue
        if ref.startswith(("http://", "https://", "//")):
            if not ref.startswith("https://"):
                raise RecipeError(f"{page} loads a non-HTTPS resource: {ref}")
            if tag.lower() == "script" and not allow_external_scripts:
                raise RecipeError(f"{page} must inline its scripts, but loads {ref}")
            if https_prefixes and not ref.startswith(https_prefixes):
                raise RecipeError(f"{page} references a disallowed resource: {ref}")
            continue
        local = ref.split("#")[0].split("?")[0]
        if local not in pending and not ((staging / page).parent / local).is_file():
            raise RecipeError(f"{page} references a missing local file: {local}")


REMOTE_CODE_RE = re.compile(r"\beval\s*\(|\bnew\s+Function\s*\(|importScripts\s*\(\s*['\"]https?:")


def check_mv3(staging: Path, ext_dir: str = "extension") -> dict:
    """A loadable Manifest V3 extension: manifest parses, every file it names exists, no remote
    code (no external <script src>, eval, new Function, remote importScripts, or unsafe-eval CSP),
    and every .js file passes node --check. Returns the parsed manifest."""
    root = staging / ext_dir
    manifest = check_json(staging, f"{ext_dir}/manifest.json")
    if not isinstance(manifest, dict) or manifest.get("manifest_version") != 3:
        raise RecipeError(f"{ext_dir}/manifest.json must declare \"manifest_version\": 3")
    for key in ("name", "version"):
        if not manifest.get(key):
            raise RecipeError(f"{ext_dir}/manifest.json is missing `{key}`")

    named: list[str] = []
    action = manifest.get("action") or {}
    named += [action.get("default_popup")]
    named += [(manifest.get("background") or {}).get("service_worker")]
    named += [manifest.get("options_page"), (manifest.get("options_ui") or {}).get("page")]
    named += [(manifest.get("side_panel") or {}).get("default_path")]
    for cs in manifest.get("content_scripts") or []:
        named += list(cs.get("js") or []) + list(cs.get("css") or [])
    named += list((manifest.get("icons") or {}).values())
    for f in filter(None, named):
        if not (root / f).is_file():
            raise RecipeError(f"{ext_dir}/manifest.json names {f}, which isn't in {ext_dir}/")

    csp = json.dumps(manifest.get("content_security_policy") or "")
    if "unsafe-eval" in csp or re.search(r"script-src[^;\"]*https?:", csp):
        raise RecipeError(f"{ext_dir}/manifest.json relaxes the content security policy")

    pages = sorted(p.relative_to(staging).as_posix() for p in root.rglob("*.html"))
    scripts = sorted(p.relative_to(staging).as_posix() for p in root.rglob("*.js"))
    for page in pages:
        check_refs(staging, page, allow_external_scripts=False)
    for s in scripts:
        if REMOTE_CODE_RE.search((staging / s).read_text(encoding="utf-8")):
            raise RecipeError(f"{s} uses eval / new Function / remote importScripts — MV3 forbids remote code")
    node_check(staging, pages=tuple(pages), scripts=tuple(scripts))
    return manifest


def node_check(staging: Path, pages: tuple[str, ...] = (), scripts: tuple[str, ...] = ()) -> None:
    """`node --check` every inline script in `pages` and every file in `scripts`."""
    node = shutil.which("node")
    if not node:
        log.warning("node not on PATH — skipping the JS syntax check")
        return
    bodies = [(f"{p} inline #{i}", b)
              for p in pages
              for i, b in enumerate(INLINE_SCRIPT_RE.findall((staging / p).read_text(encoding="utf-8")))]
    bodies += [(s, (staging / s).read_text(encoding="utf-8")) for s in scripts]
    with tempfile.TemporaryDirectory() as tmp:
        for i, (label, body) in enumerate(bodies):
            js = Path(tmp) / f"check-{i}.js"
            js.write_text(body, encoding="utf-8")
            proc = subprocess.run([node, "--check", str(js)], capture_output=True, text=True)
            if proc.returncode != 0:
                raise RecipeError(f"{label} fails `node --check`:\n{proc.stderr[-1500:]}")
    log.info("%d script(s) pass node --check", len(bodies))


def check_json(staging: Path, name: str) -> object:
    try:
        return json.loads((staging / name).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RecipeError(f"{name} is not valid JSON: {exc}") from exc


def check_sources_csv(staging: Path, name: str = "sources.csv", lo: int = 3, hi: int = 8) -> None:
    import csv
    with (staging / name).open(encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows or [c.strip().lower() for c in rows[0]] != ["title", "url", "note"]:
        raise RecipeError(f"{name} must start with the header title,url,note")
    body = [r for r in rows[1:] if any(c.strip() for c in r)]
    if not lo <= len(body) <= hi:
        raise RecipeError(f"{name} has {len(body)} sources; expected {lo}–{hi}")
    for r in body:
        if len(r) != 3 or not r[1].startswith("http"):
            raise RecipeError(f"{name} has a malformed row: {r}")


