"""Shared pieces for the food recipes: the recipe template, the safety gate, and the Cook's Card.

* ``check_recipe(staging)`` — runs the bundled ``recipe-validator`` scanner on
  ``recipe.md``. A critical food-safety finding rejects the run; an allergen
  that is in the ingredients but not declared is ADDED to the frontmatter
  (over-labeling is the safe direction, and a scanner false positive shouldn't
  throw away a whole run).
* ``add_cooks_card(final)`` — renders ``recipe.md`` + ``cover.png`` into one
  self-contained ``cooks-card.html`` (cover inlined as a data URI, print
  stylesheet, light/dark aware) and lists it in ``artifact.json``.
"""

from __future__ import annotations

import base64
import html as _html
import io
import json
import logging
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from core import RecipeError  # noqa: E402

log = logging.getLogger("recipes")

TEMPLATE = (HERE / "recipe-template.md").read_text(encoding="utf-8")
SCANNER = ROOT / ".claude" / "skills" / "recipe-validator" / "scripts" / "scan_recipes.py"
CARD = "cooks-card.html"


# --- safety gate -------------------------------------------------------------

def check_recipe(staging: Path, manifest: dict[str, object]) -> None:
    md = staging / "recipe.md"
    if not SCANNER.is_file():
        log.warning("recipe-validator scanner not found at %s — skipping the safety gate", SCANNER)
        return
    proc = subprocess.run([sys.executable, str(SCANNER), str(md)], capture_output=True, text=True, encoding="utf-8")
    try:
        report = json.loads(proc.stdout)
        findings = report["recipes"][0].get("findings", [])
    except (json.JSONDecodeError, KeyError, IndexError):
        log.warning("recipe-validator produced no report (exit %s) — skipping the safety gate", proc.returncode)
        return

    critical = [f for f in findings if f["severity"] == "critical"]
    if critical:
        raise RecipeError("recipe-validator: " + "; ".join(f["message"] for f in critical))

    missing = sorted({m.group(1) for f in findings if f["category"] == "allergen" and f["severity"] == "warning"
                      for m in [re.search(r"contain (\S+) ", f["message"])] if m})
    if missing:
        add_allergens(md, missing)
        log.warning("added undeclared allergens to recipe.md: %s", ", ".join(missing))
    for f in findings:
        if f["severity"] in ("health", "warning") and f["category"] != "allergen":
            log.info("recipe-validator %s: %s", f["severity"], f["message"])


def add_allergens(md: Path, tokens: list[str]) -> None:
    text = md.read_text(encoding="utf-8")
    m = re.search(r"(?m)^allergens:\s*\[(.*?)\]\s*$", text)
    if m:
        have = [a.strip().strip("\"'") for a in m.group(1).split(",") if a.strip()]
        merged = have + [t for t in tokens if t not in have]
        line = "allergens: [" + ", ".join(f'"{a}"' for a in merged) + "]"
        text = text[: m.start()] + line + text[m.end():]
    else:
        text = re.sub(r"\A---\n", "---\nallergens: [" + ", ".join(f'"{t}"' for t in tokens) + "]\n", text, count=1)
    md.write_text(text, encoding="utf-8")


# --- Cook's Card ---------------------------------------------------------------

SWEET = ["#e11d48", "#db2777", "#9333ea", "#c026d3"]
SAVORY = ["#16a34a", "#ea580c", "#0d9488", "#ca8a04"]
REST_SECTIONS = ["Food Safety", "Serving", "Scaling", "Chef", "Nutrition", "Sources", "Credits"]


def add_cooks_card(final: Path) -> None:
    """Render cooks-card.html beside recipe.md and record it in artifact.json."""
    try:
        html = render_card(final / "recipe.md", final / "cover.png")
    except ImportError:
        log.warning("`markdown` not installed — skipping the Cook's Card (pip install -r requirements.txt)")
        return
    (final / CARD).write_text(html, encoding="utf-8")
    manifest_path = final / "artifact.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data.setdefault("files", {})["cooks_card"] = CARD
    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log.info("Cook's Card written: %s", final / CARD)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    m = re.match(r"\A﻿?---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return {}, text
    fields: dict[str, object] = {}
    for line in m.group(1).splitlines():
        kv = re.match(r"^([\w-]+):\s*(.*)$", line)
        if not kv:
            continue
        val = kv.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            fields[kv.group(1).lower()] = [x.strip().strip("\"'") for x in val[1:-1].split(",") if x.strip()]
        else:
            fields[kv.group(1).lower()] = val.strip("\"'")
    return fields, text[m.end():]


def split_sections(body: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^##\s+(.+?)\s*$", body)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def md_inline(text: str) -> str:
    t = _html.escape(text)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", t)


def md_block(text: str) -> str:
    import markdown

    # Bold labels directly above a list need a blank line or the list becomes one paragraph.
    text = re.sub(r"(\*\*[^\n*]+:\*\*)\n(?=[-*+] )", r"\1\n\n", text)
    out = markdown.markdown(text, extensions=["extra"])
    return re.sub(r"<li>\s*<p>(.*?)</p>\s*</li>", r"<li>\1</li>", out, flags=re.S)


def parse_steps(instr: str) -> list[tuple[str | None, str]]:
    """Instructions -> [(phase label or None, step html)]; numbered lines start steps."""
    steps: list[tuple[str | None, str]] = []
    label: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal label
        if buf:
            steps.append((label, md_inline(" ".join(buf))))
            label = None
            buf.clear()

    for line in instr.splitlines():
        sub = re.match(r"^###+\s+(.+?)\s*$", line)
        num = re.match(r"^\d+\.\s+(.*)$", line)
        if sub:
            flush()
            label = re.sub(r"\(.*?\)", "", sub.group(1)).strip()
        elif num:
            flush()
            buf.append(num.group(1).strip())
        elif not line.strip() or re.match(r"^\s*(---+|\*\*\*+)\s*$", line):
            flush()
        else:
            buf.append(line.strip())  # wrapped or continuation line — never drop content
    flush()
    return steps


def image_data_uri(path: Path, max_w: int = 1600) -> str | None:
    if not path.is_file():
        return None
    from PIL import Image

    with Image.open(path) as im:
        im = im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=82, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def minutes(value: object) -> str:
    text = str(value).strip()
    if not text.isdigit():
        return text
    h, m = divmod(int(text), 60)
    return f"{m} min" if not h else (f"{h} hr" if not m else f"{h} hr {m} min")


def shade(hex_color: str, factor: float) -> str:
    r, g, b = (int(hex_color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    if factor <= 1:
        r, g, b = (int(c * factor) for c in (r, g, b))
    else:
        r, g, b = (int(c + (255 - c) * (factor - 1)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def render_card(md_path: Path, hero: Path) -> str:
    fields, body = parse_frontmatter(md_path.read_text(encoding="utf-8"))
    h1 = re.search(r"(?m)^#\s+(.+?)\s*$", body)
    title = str(fields.get("title") or (h1.group(1) if h1 else md_path.stem))
    if h1:
        body = body[: h1.start()] + body[h1.end():]
    sections = split_sections(body)

    def section(name: str) -> tuple[str, str] | None:
        return next(((h, t) for h, t in sections if h.lower().startswith(name.lower())), None)

    tags = fields.get("tags") if isinstance(fields.get("tags"), list) else []
    sweet = any(k in (" ".join(tags) + " " + title).lower()
                for k in ("dessert", "cake", "sweet", "bak", "cookie", "chocolate", "fruit", "pastry", "candy"))
    palette = SWEET if sweet else SAVORY
    accent = palette[sum(ord(c) for c in str(fields.get("date", "")) + title) % len(palette)]
    esc = _html.escape
    region = str(fields.get("region", "")).replace("-", " ").title()

    stats = [(k, v) for k, v in [
        ("Yield", fields.get("yield")),
        ("Active", fields.get("active_time_min") and minutes(fields["active_time_min"])),
        ("Total", fields.get("total_time_min") and minutes(fields["total_time_min"])),
        ("Region", region),
    ] if v]
    allergens = fields.get("allergens") if isinstance(fields.get("allergens"), list) else []

    parts: list[str] = []
    kicker = "  &middot;  ".join(esc(s) for s in (region, str(fields.get("date", ""))) if s)
    if kicker:
        parts.append(f'<p class="kicker">{kicker}</p>')
    parts.append(f"<h1>{esc(title)}</h1>")
    uri = image_data_uri(hero)
    if uri:
        parts.append(f'<img class="hero" src="{uri}" alt="{esc(title)} (AI-generated illustration)" />')
    if stats:
        parts.append('<div class="statbar">' + "".join(
            f'<div class="stat"><div class="stat-l">{esc(k)}</div><div class="stat-v">{esc(str(v))}</div></div>'
            for k, v in stats) + "</div>")
    if tags:
        parts.append('<ul class="tags">' + "".join(f'<li class="tag">{esc(t)}</li>' for t in tags) + "</ul>")
    if allergens:
        parts.append(f'<p class="allergens"><strong>Contains:</strong> {esc(", ".join(allergens))}</p>')

    done = {"cultural context", "ingredients", "equipment", "instructions"}
    ctx = section("Cultural Context")
    if ctx:
        parts.append(f'<p class="intro">{md_inline(ctx[1])}</p>')
    for name in ("Ingredients", "Equipment"):
        s = section(name)
        if s:
            parts.append(f'<h2 class="sec">{name}</h2><div class="panel">{md_block(s[1])}</div>')
    instr = section("Instructions")
    if instr:
        parts.append('<h2 class="sec">Instructions</h2>')
        for i, (label, text) in enumerate(parse_steps(instr[1]), 1):
            if label:
                parts.append(f'<div class="substep">{esc(label)}</div>')
            parts.append(f'<div class="step"><div class="step-num">{i}</div><div class="step-txt">{text}</div></div>')
    ordered = [s for n in REST_SECTIONS if (s := section(n))]
    ordered += [s for s in sections if s not in ordered and not any(s[0].lower().startswith(d) for d in done)]
    for heading, text in ordered:
        if text:
            parts.append(f'<h2 class="sec">{esc(heading)}</h2>{md_block(text)}')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<style>{CSS.replace("ACCENT_DARK", shade(accent, 0.72)).replace("ACCENT_TINT", shade(accent, 1.90)).replace("ACCENT_LIGHT", shade(accent, 1.35)).replace("ACCENT", accent)}</style>
</head>
<body>
<div class="wrap">
{chr(10).join(parts)}
<p class="footer">{esc(title)} &middot; AI Automation Recipes</p>
</div>
</body>
</html>"""


CSS = """
:root { --accent: ACCENT; --accent-dark: ACCENT_DARK; --panel: ACCENT_TINT;
  --ink: #1f2937; --muted: #6b7280; --bg: #ffffff; --border: #e5e7eb; --body: #374151; }
@media (prefers-color-scheme: dark) {
  :root { --ink: #f3f4f6; --muted: #9ca3af; --bg: #0f1115; --panel: #171a21;
    --border: #2a2f3a; --body: #d1d5db; --accent-dark: ACCENT_LIGHT; }
}
* { box-sizing: border-box; }
body { margin: 0; padding: 32px 20px 64px; font: 17px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--body); background: var(--bg); -webkit-text-size-adjust: 100%; }
.wrap { max-width: 760px; margin: 0 auto; }
.kicker { font-size: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: .16em; font-weight: 700; margin: 0 0 8px; }
h1 { font-size: clamp(28px, 6vw, 42px); line-height: 1.15; color: var(--ink); margin: 0 0 18px; letter-spacing: -.02em; }
.hero { width: 100%; height: auto; border-radius: 12px; display: block; margin: 0 0 22px; }
.statbar { display: flex; flex-wrap: wrap; gap: 1px; background: var(--border); border-top: 3px solid var(--accent);
  border-radius: 0 0 10px 10px; overflow: hidden; margin: 0 0 18px; }
.stat { flex: 1 1 120px; background: var(--panel); padding: 12px 10px; text-align: center; }
.stat-l { color: var(--accent); font-size: 10px; text-transform: uppercase; letter-spacing: .12em; font-weight: 700; }
.stat-v { color: var(--accent-dark); font-size: 17px; font-weight: 700; margin-top: 4px; }
.tags { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 14px; padding: 0; list-style: none; }
.tag { background: var(--panel); color: var(--accent-dark); padding: 4px 11px; border-radius: 999px; font-size: 12px; font-weight: 600; }
.allergens { font-size: 14px; margin: 0 0 20px; }
.intro { font-size: 18px; font-style: italic; margin: 0 0 30px; }
h2.sec { font-size: 22px; color: var(--ink); margin: 36px 0 14px; padding-bottom: 7px; border-bottom: 2px solid var(--accent); }
.panel { background: var(--panel); border-radius: 10px; padding: 6px 20px 14px; }
.panel h3 { font-size: 13px; color: var(--accent-dark); text-transform: uppercase; letter-spacing: .08em; margin: 16px 0 6px; }
.step { display: flex; gap: 14px; align-items: flex-start; margin: 0 0 14px; }
.step-num { flex: 0 0 32px; height: 32px; background: var(--accent); color: #fff; border-radius: 50%; font-weight: 700;
  display: flex; align-items: center; justify-content: center; }
.step-txt { flex: 1; padding-top: 4px; }
.substep { font-size: 13px; font-weight: 700; color: var(--accent-dark); text-transform: uppercase; letter-spacing: .08em; margin: 22px 0 10px; }
ul, ol { padding-left: 22px; } li { margin-bottom: 5px; }
strong { color: var(--ink); } a { color: var(--accent-dark); }
table { border-collapse: collapse; width: 100%; display: block; overflow-x: auto; }
td, th { border: 1px solid var(--border); padding: 6px 10px; text-align: left; }
.footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 13px; color: var(--muted); text-align: center; }
@media print {
  :root { --bg: #fff; --ink: #1f2937; --body: #374151; --border: #e5e7eb; }
  body { font-size: 11pt; padding: 0; } .step, .panel { break-inside: avoid; } h2.sec { break-after: avoid; }
  .hero { max-height: 3in; object-fit: cover; }
}
"""
