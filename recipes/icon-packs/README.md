# Icon Pack

[← All recipes](../../README.md)

Twelve cohesive icons in one shared visual system, shipped as SVG, transparent 1024 px PNG and a
multi-size Windows `.ico`. No image model is involved: Claude designs the pack (twelve real,
nameable members of one family — browsers, databases, page icons — with an original mark for each,
never a copied logo) and draws each icon's **symbol** as an SVG fragment. Code owns everything
else: the container (squircle tile, circle badge, folder, drive block…), identical on all twelve by
construction; the tile gradient; and every PNG and ICO size, each rasterized from the vector at its
own size so the 16 px entry stays crisp.

| | |
|:---|:---|
| **Output** | `icon-packs/<YYYY-MM>/<date>_<slug>/` → `pack.md`, `glyphs.txt`, `svg/`, `png/`, `ico/`, `cover.png` (contact sheet), `artifact.json` |
| **Schedule** | Wednesdays, 10:00 UTC |
| **Model** | `sonnet` |
| **Needs** | Nothing beyond Claude. PNG/ICO need `resvg-py` (in `requirements.txt`); without it the pack ships SVG only |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill |
| **Skills** | `llm-writing`, `humanizer` |

## What the runner checks

Every glyph is parsed and rejected if it uses `<text>`, `<image>`, `<script>`, `<style>`,
`<foreignObject>` or an external `href`/`src`, or draws nothing. A rejected glyph is dropped; a
pack with fewer than 10 drawable glyphs is rejected outright.

## Themes

About fifty, rotated least-used first, each with a category (AI-Tools, Developer-Tools,
Folders, Web-Page-Icons…). Force one with `--theme "Databases — Postgres, MySQL, SQLite — drive blocks"`.

## Run it

```bash
python recipes/icon-packs/run.py --output-dir ~/ai-output
```
