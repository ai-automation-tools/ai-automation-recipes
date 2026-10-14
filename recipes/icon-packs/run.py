#!/usr/bin/env python3
"""Icon Packs — twelve cohesive icons drawn as SVG, shipped as SVG + transparent PNG + multi-size ICO.

    python recipes/icon-packs/run.py --output-dir ~/ai-output [--theme "Databases — Postgres, …"]

The agent draws only each icon's *symbol*, as an SVG fragment in a 0–100 box. Code owns the rest:
the container shape (identical on all twelve by construction), the tile gradient, the final SVG
document, and rasterizing every PNG and ICO size from the vector. No image model is involved.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RecipeError, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402
from core.images import ImageError, process  # noqa: E402

log = logging.getLogger("recipes")

# (theme, category). Each names twelve similar, nameable things plus the container they share.
THEMES = [
    ("Web Browsers — Chrome, Firefox, Edge, Safari, Brave, Opera, Vivaldi — squircle tiles", "Apps-and-Services"),
    ("AI Chat Assistants — Claude, ChatGPT, Gemini, Copilot, Perplexity, Grok — squircle tiles", "AI-Tools"),
    ("Cloud Storage Services — Dropbox, Drive, OneDrive, iCloud, Box, Mega — drive blocks", "Cloud-and-Data"),
    ("AI Coding Tools — Claude Code, Cursor, Copilot, Codex, Windsurf, Zed — squircle tiles", "AI-Tools"),
    ("Windows Library Folders — Documents, Downloads, Pictures, Music, Videos, Desktop — folder tabs", "Folders"),
    ("Code Editors and IDEs — VS Code, JetBrains, Vim, Sublime, Xcode, Android Studio — rounded squares", "Developer-Tools"),
    ("Messaging Apps — WhatsApp, Signal, Telegram, Discord, Slack, Messenger — circle badges", "Apps-and-Services"),
    ("Developer Folder Icons — Repos, Branches, Builds, Releases, Tests, Docs — folder tabs", "Folders"),
    ("Password Managers and Security Apps — 1Password, Bitwarden, KeePass, Authy, YubiKey — rounded squares", "System-and-Security"),
    ("Note-Taking Apps — Notion, Obsidian, Evernote, OneNote, Bear, Logseq — squircle tiles", "Apps-and-Services"),
    ("Website Page Icons — Home, About, Contact, Services, Pricing, FAQ — bare glyphs", "Web-Page-Icons"),
    ("Cloud Providers — AWS, Azure, GCP, Cloudflare, DigitalOcean, Linode — rounded squares", "Cloud-and-Data"),
    ("Media Library Folders — Movies, TV Shows, Anime, Audiobooks, Podcasts, Photos — folder tabs", "Folders"),
    ("Version Control and CI — Git, GitHub, GitLab, Jenkins, Actions, Docker Hub — rounded squares", "Developer-Tools"),
    ("Video Conferencing Apps — Zoom, Teams, Meet, Webex, FaceTime, Jitsi — circle badges", "Apps-and-Services"),
    ("AI Image Generators — Midjourney, DALL·E, Stable Diffusion, Flux, Ideogram — squircle tiles", "AI-Tools"),
    ("E-Commerce Page Icons — Cart, Checkout, Orders, Wishlist, Returns, Tracking — bare glyphs", "Web-Page-Icons"),
    ("Programming Language Marks — Python, JavaScript, Rust, Go, TypeScript, C++ — rounded squares", "Developer-Tools"),
    ("Project Workspace Folders — Active, Archive, Client Work, Drafts, Assets, Exports — folder tabs", "Folders"),
    ("Terminal and Shell Tools — PowerShell, Bash, Zsh, Windows Terminal, tmux, SSH — rounded squares", "Developer-Tools"),
    ("Game Launchers — Steam, Epic, GOG, Battle.net, Xbox, Ubisoft — squircle tiles", "Apps-and-Services"),
    ("Productivity Suite Apps — Docs, Sheets, Slides, Word, Excel, PowerPoint — squircle tiles", "Apps-and-Services"),
    ("Backup and Archive Folders — Backups, Snapshots, Old Versions, Cold Storage, Restore — folder tabs", "Folders"),
    ("Media Players — VLC, MPV, Plex, Jellyfin, Kodi, Foobar — rounded squares", "Apps-and-Services"),
    ("Login and Account Page Icons — Sign In, Sign Up, Reset Password, Two Factor, Profile, Logout — bare glyphs", "Web-Page-Icons"),
    ("Databases — Postgres, MySQL, SQLite, MongoDB, Redis, DuckDB — drive blocks", "Cloud-and-Data"),
    ("Automation Platforms — n8n, Zapier, Make, Node RED, IFTTT, Power Automate — squircle tiles", "Developer-Tools"),
    ("Antivirus and System Security Apps — Defender, Malwarebytes, Bitdefender, Firewall, VPN, Sandbox — rounded squares", "System-and-Security"),
    ("Web Framework Marks — React, Vue, Svelte, Next, Astro, Angular — circle badges", "Developer-Tools"),
    ("Cloud Sync Folders — Synced, Pending, Offline, Shared, Conflicts, Trash — folder tabs", "Folders"),
    ("AI Model Families — Claude, GPT, Gemini, Llama, Mistral, DeepSeek — circle badges", "AI-Tools"),
    ("Blog and Content Page Icons — Blog, Archive, Categories, Tags, Author, RSS — bare glyphs", "Web-Page-Icons"),
    ("Virtualization and Containers — Docker, Kubernetes, Proxmox, VirtualBox, WSL, Podman — rounded squares", "Developer-Tools"),
    ("Email Clients — Gmail, Outlook, Thunderbird, Proton Mail, Spark, Fastmail — squircle tiles", "Apps-and-Services"),
    ("Windows System Icons — This PC, Recycle Bin, Control Panel, Network, Devices, Settings — rounded squares", "System-and-Security"),
    ("Documentation Page Icons — Docs, Getting Started, API Reference, Changelog, Support, Search — bare glyphs", "Web-Page-Icons"),
    ("Finance and Banking Apps — Bank, Wallet, Budget, Invest, Crypto, Taxes — squircle tiles", "Apps-and-Services"),
    ("Package Managers — npm, pip, cargo, apt, winget, Homebrew — rounded squares", "Developer-Tools"),
    ("Linux Distribution Marks — Ubuntu, Debian, Arch, Fedora, Mint, Alpine — circle badges", "System-and-Security"),
    ("Self-Hosted Apps — Nextcloud, Home Assistant, Immich, Paperless, Vaultwarden, Uptime Kuma — squircle tiles", "Apps-and-Services"),
    ("Monitoring and Observability Tools — Grafana, Prometheus, Sentry, Datadog, Loki, Uptime — rounded squares", "Developer-Tools"),
    ("Tagged Category Folders — Red, Orange, Yellow, Green, Blue, Purple — folder tabs", "Folders"),
    ("Dashboard and Analytics Page Icons — Overview, Reports, Metrics, Trends, Exports, Alerts — bare glyphs", "Web-Page-Icons"),
    ("Smart Home and IoT Devices — Hub, Lights, Thermostat, Camera, Lock, Sensor — circle badges", "Apps-and-Services"),
    ("Networking and NAS Tools — Router, Switch, NAS, VPN, DNS, Firewall — drive blocks", "Cloud-and-Data"),
    ("Vector Databases and RAG Tools — Pinecone, Weaviate, Chroma, Qdrant, pgvector, FAISS — drive blocks", "Cloud-and-Data"),
    ("Project Management Apps — Jira, Linear, Trello, Asana, ClickUp, Monday — rounded squares", "Apps-and-Services"),
    ("Error and Status Page Icons — 404, 500, Maintenance, Coming Soon, Offline, Rate Limited — bare glyphs", "Web-Page-Icons"),
    ("ML Framework Marks — PyTorch, TensorFlow, JAX, scikit learn, Keras, ONNX — circle badges", "AI-Tools"),
    ("3D and CAD Tools — Blender, Fusion 360, SketchUp, Rhino, Cinema 4D, Unreal — squircle tiles", "Apps-and-Services"),
    ("Retro-Futuristic Synthwave Icon Set", "Design-Styles"),
    ("Soft Claymorphism Colorful Icons", "Design-Styles"),
    ("Retro Windows 95 System Icons", "Design-Styles"),
    ("Electric Neon Glow Web Elements", "Design-Styles"),
]

# Containers, in a 512x512 user space. The agent picks a key; code draws the shape.
CONTAINERS = {
    "squircle-tile": ("a rounded-square (squircle) app tile with a large corner radius",
                      '<rect x="32" y="32" width="448" height="448" rx="104" ry="104" fill="{fill}"/>', (136, 136, 240)),
    "rounded-square": ("a rounded square with a small, tight corner radius",
                       '<rect x="32" y="32" width="448" height="448" rx="48" ry="48" fill="{fill}"/>', (136, 136, 240)),
    "circle-badge": ("a perfect circle badge", '<circle cx="256" cy="256" r="224" fill="{fill}"/>', (141, 141, 230)),
    "folder-tab": ("a front-facing folder with a tab on its upper-left, drawn flat and straight-on",
                   '<path d="M64 96 h132 a28 28 0 0 1 22 11 l26 35 h212 a36 36 0 0 1 36 36 v250 a36 36 0 0 1 -36 36 '
                   'H64 a36 36 0 0 1 -36 -36 V132 a36 36 0 0 1 36 -36 z" fill="{fill}"/>', (171, 215, 170)),
    "drive-block": ("a front-facing hard-drive / device block with a consistent silhouette",
                    '<rect x="48" y="112" width="416" height="288" rx="40" ry="40" fill="{fill}"/>', (161, 161, 190)),
    "bare-glyph": ("no container at all — the bare symbol, drawn at a consistent optical weight", "", (48, 48, 416)),
}
VIEWBOX = 512
CANVAS = 1024
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)
MIN_ICONS = 10  # a pack ships if at least this many of twelve glyphs pass validation

SVG_NS = "http://www.w3.org/2000/svg"
HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
GLYPH_DELIM_RE = re.compile(r"^===\s*ICON:\s*(.+?)\s*===\s*$", re.M)
BANNED = ("text", "tspan", "image", "script", "foreignObject", "style", "textPath")
DRAWING = ("path", "circle", "rect", "ellipse", "polygon", "polyline", "line", "g")
EXTERNAL_REF_RE = re.compile(r'(?:href|src)\s*=\s*["\']\s*(?!#)(?:[a-zA-Z]+:|//)', re.I)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-") or "icon"


def norm_hex(value: object, fallback: str) -> str:
    v = str(value or "").strip()
    if not HEX_RE.match(v):
        return fallback
    if len(v) == 4:
        v = "#" + "".join(c * 2 for c in v[1:])
    return v.upper()


def lighten(hex_color: str, amount: float) -> str:
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: int(round(c + (255 - c) * amount))  # noqa: E731
    return f"#{mix(r):02X}{mix(g):02X}{mix(b):02X}"


def parse_glyphs(text: str) -> dict[str, str]:
    parts = GLYPH_DELIM_RE.split(text or "")
    out = {}
    for i in range(1, len(parts) - 1, 2):
        body = re.sub(r"^```(?:svg|xml|html)?\s*|\s*```\s*$", "", parts[i + 1].strip()).strip()
        if body:
            out[slugify(parts[i])] = body
    return out


def unwrap(fragment: str) -> tuple[str, float]:
    """(inner markup, drawing-box size). Accepts a full <svg> document and uses its viewBox."""
    text = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", fragment.strip()).strip()
    m = re.search(r"<svg\b([^>]*)>(.*)</svg\s*>", text, re.S | re.I)
    if not m:
        return text, 100.0
    vb = re.search(r'viewBox\s*=\s*["\']\s*([-\d.]+)[,\s]+([-\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)', m.group(1))
    return m.group(2).strip(), (max(float(vb.group(3)), float(vb.group(4))) or 100.0) if vb else 100.0


def check_glyph(fragment: str) -> str | None:
    """None if the fragment is drawable offline, else the reason it isn't."""
    inner, _ = unwrap(fragment)
    try:
        root = ET.fromstring(f'<svg xmlns="{SVG_NS}">{inner}</svg>')
    except ET.ParseError as exc:
        return f"not well-formed XML ({exc})"
    tags = [el.tag.split("}")[-1] for el in root.iter()]
    banned = sorted({t for t in tags if t in BANNED})
    if banned:
        return "banned element(s): " + ", ".join(f"<{t}>" for t in banned)
    if not any(t in DRAWING for t in tags):
        return "no drawing elements"
    if EXTERNAL_REF_RE.search(inner):
        return "external reference in href/src"
    return None


def compose(glyph: str, container: str, tile: str, glyph_color: str, grad_id: str) -> str:
    """Wrap a validated glyph in the pack's code-owned container document."""
    _, shape, (gx, gy, gsize) = CONTAINERS[container]
    inner, box = unwrap(glyph)
    defs = body = ""
    if shape:
        defs = (f'<defs><linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0" stop-color="{lighten(tile, 0.18)}"/><stop offset="1" stop-color="{tile}"/>'
                f'</linearGradient></defs>')
        body = shape.format(fill=f"url(#{grad_id})")
    return (f'<svg xmlns="{SVG_NS}" viewBox="0 0 {VIEWBOX} {VIEWBOX}" width="{VIEWBOX}" height="{VIEWBOX}">'
            f'{defs}{body}<g transform="translate({gx:.3f} {gy:.3f}) scale({gsize / box:.6f})" '
            f'fill="{glyph_color}" stroke="none">{inner}</g></svg>')


# --- hooks -----------------------------------------------------------------

def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--theme", help="Use this theme instead of the rotation (any string).")


def prepare(ctx: RunContext) -> dict[str, str]:
    if ctx.args.theme:
        theme, category = ctx.args.theme, "Custom"
    else:
        theme = least_used([t for t, _ in THEMES], ctx.existing, "theme")
        category = dict(THEMES)[theme]
    table = "\n".join(f"| `{k}` | {desc} |" for k, (desc, _, _) in CONTAINERS.items())
    return {"THEME": theme, "CATEGORY": category, "CONTAINERS": table}


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    container = str(manifest.get("container", "")).strip().lower()
    if container not in CONTAINERS:
        raise RecipeError(f"container must be one of {list(CONTAINERS)}, got {container!r}")
    icons = manifest.get("icons")
    if not isinstance(icons, list) or len(icons) != 12:
        raise RecipeError("`icons` must list exactly 12 icons")
    glyphs = parse_glyphs((staging / "glyphs.txt").read_text(encoding="utf-8"))
    glyph_color = norm_hex(manifest.get("glyph_color"), "#FFFFFF")
    good, seen = [], set()
    for icon in icons:
        slug = slugify(str(icon.get("slug") or icon.get("name")))
        if slug in seen:
            raise RecipeError(f"duplicate icon slug {slug!r}")
        seen.add(slug)
        frag = glyphs.get(slug)
        reason = check_glyph(frag) if frag else "missing from glyphs.txt"
        if reason:
            log.warning("icon %s dropped: %s", slug, reason)
            continue
        tile = norm_hex(icon.get("tile_color"), "#3B82F6")
        good.append({"slug": slug, "name": icon.get("name", slug), "tile": tile,
                     "glyph": tile if container == "bare-glyph" else glyph_color, "fragment": frag})
    if len(good) < MIN_ICONS:
        raise RecipeError(f"only {len(good)} of 12 glyphs are drawable; need {MIN_ICONS}")
    ctx.state.update(container=container, icons=good)


def _rasterize(svg: str, size: int, tmp: Path):
    from PIL import Image

    src, out = tmp / "in.svg", tmp / f"out-{size}.png"
    src.write_text(svg, encoding="utf-8")
    process.svg_to_png(src, out, size=size)
    with Image.open(out) as im:
        return im.convert("RGBA")


def build_assets(ctx: RunContext, staging: Path, manifest: dict[str, object]) -> list[str]:
    """svg/ always; png/ (1024 px), ico/ (each size from the vector) and a contact-sheet cover
    when an SVG renderer is installed."""
    from PIL import Image

    container, icons = ctx.state["container"], ctx.state["icons"]
    (staging / "svg").mkdir()
    svgs = {}
    for ic in icons:
        svgs[ic["slug"]] = compose(ic["fragment"], container, ic["tile"], ic["glyph"], f"g-{ic['slug']}")
        (staging / "svg" / f"{ic['slug']}.svg").write_text(svgs[ic["slug"]], encoding="utf-8")
    out = [f"svg/{s}.svg" for s in svgs]

    if not process.svg_renderer_available():
        log.warning("no SVG renderer installed (pip install resvg-py) — shipping SVG only")
        return out
    (staging / "png").mkdir()
    (staging / "ico").mkdir()
    rendered = []
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for slug, svg in svgs.items():
            try:
                big = _rasterize(svg, CANVAS, tmp)
                small = [_rasterize(svg, s, tmp) for s in ICO_SIZES]
            except ImageError as exc:
                log.warning("icon %s not rasterized: %s", slug, exc)
                continue
            big.save(staging / "png" / f"{slug}.png", format="PNG")
            # Each ICO entry comes from the vector at its own size, so 16 px stays legible.
            small[-1].save(staging / "ico" / f"{slug}.ico", format="ICO",
                           sizes=[(s, s) for s in ICO_SIZES], append_images=small[:-1])
            out += [f"png/{slug}.png", f"ico/{slug}.ico"]
            rendered.append(big)

    if rendered:  # 4-column contact sheet: the set's cohesion at a glance
        cell, cols = 256, 4
        rows = (len(rendered) + cols - 1) // cols
        sheet = Image.new("RGBA", (cols * cell, rows * cell), (24, 24, 28, 255))
        for i, im in enumerate(rendered):
            tile = im.copy()
            tile.thumbnail((cell - 32, cell - 32), Image.LANCZOS)
            sheet.paste(tile, ((i % cols) * cell + (cell - tile.width) // 2,
                               (i // cols) * cell + (cell - tile.height) // 2), tile)
        sheet.convert("RGB").save(staging / "cover.png")
        out.append("cover.png")
    return out


RECIPE = Recipe(
    name="icon-packs",
    collection="icon-packs",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("pack.md", "glyphs.txt"),
    skills=("llm-writing", "humanizer"),
    fields=("theme", "category", "container", "icons"),
    cover_aspect=None,
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
    after_cover=build_assets,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
