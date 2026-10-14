<h1 align="center">🧩 Icon Pack</h1>

<p align="center">
  <em>Twelve matching icons shipped as SVG, transparent PNG and a multi-size Windows .ico.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

No image model is involved. Claude designs the pack, twelve members of one family (browser
actions, database objects, page icons), and draws each icon's symbol as an SVG fragment. Code does
the rest: the container (squircle tile, circle badge, folder, drive block...), identical on all
twelve; the tile gradient; and every PNG and ICO size, each rasterized from the vector at its own
size so the 16 px icon stays crisp.

| | |
|:---|:---|
| **Output** | `icon-packs/<YYYY-MM>/<date>_<slug>/` → `pack.md`, `glyphs.txt`, `svg/`, `png/`, `ico/`, `cover.png` (contact sheet), `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill |
| **Skills** | `llm-writing`, `humanizer` |
| **Needs** | Nothing beyond Claude. PNG and ICO need `resvg-py` (in `requirements.txt`); without it the pack ships SVG only |

## No brands

Themes name a family of functions, never a product. Naming one invites a copy of its logo: an early
run on a "Web Browsers" theme drew icons that echoed real browser marks. The prompt also forbids
naming or echoing any product, company or brand.

## What the runner checks

Every glyph is parsed and dropped if it uses `<text>`, `<image>`, `<script>`, `<style>`,
`<foreignObject>` or an external `href`/`src`, or draws nothing. A pack with fewer than 10 drawable
glyphs is rejected.

## Themes

Fifty-four, least-used first, each with a category (AI-Tools, Developer-Tools, Folders,
Web-Page-Icons...). Force one with
`--theme "Database Objects — table, index, query, schema, backup, replica — drive blocks"`.

## Sample

> **Browser Actions** — Twelve solid white browser-control glyphs on cool-toned squircle tiles: back, forward, reload, new tab, bookmarks, history and more.
>
> *Live pilot run, 2026-10-14 · Sonnet · first run after the themes were de-branded*

## Run it

```bash
python recipes/icon-packs/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../image-collections/README.md">Next: Image Collections →</a>
</p>
