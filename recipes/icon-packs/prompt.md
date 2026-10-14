# Icon Pack

Goal: design ONE cohesive pack of 12 icons and draw each icon's **symbol** as an SVG fragment.
The runner owns everything else: the container shape, the tile gradient, the final SVG documents,
and the transparent PNG and multi-size ICO files rendered from them. No image model is involved.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Theme: `{{THEME}}`** (category `{{CATEGORY}}`) — chosen by the runner. If the theme names its
members, use those (add more of the same family to reach twelve); if it names a style, choose
twelve concrete, nameable members that suit it.

**Packs already published** (date · slug · title — description):

{{EXISTING}}

--------------------------------------------------
## WHAT A PACK IS

**One category of similar, nameable things, in one shared visual system.** "Chrome, Firefox, Edge,
Safari…" — twelve members of one family, each instantly identifiable, all cut from the same cloth.

- **Name the real things**, plainly ("Firefox", "Google Drive", "Checkout").
- **Draw an original mark for each.** Never reproduce a trademarked logo. Take the product's idea —
  what it does, its colour, its silhouette — and design a fresh symbol in the pack's style.
- If the theme has no real-world members (page icons, a style study), the members are the concrete
  pages or functions themselves.

**One container for the whole pack.** The runner draws it, identically on all twelve:

| `container` | What it is |
|---|---|
{{CONTAINERS}}

Pick by subject: `squircle-tile` for apps and AI tools, `folder-tab` for folder packs,
`circle-badge` for social/profile/round-dock sets, `rounded-square` for system and utility icons,
`drive-block` for storage and devices, `bare-glyph` for inline web page/UI icons.

**Two-tone colour.** Each icon gets its own saturated `tile_color` (a 6-digit hex like `#3B82F6`;
no two near-identical, all one palette family). The pack shares ONE `glyph_color` — almost always
`#FFFFFF`, a very dark neutral only if every tile is pale. For `bare-glyph`, `tile_color` is the
symbol's own colour and `glyph_color` is ignored.

--------------------------------------------------
## DRAWING THE SYMBOLS — `glyphs.txt`

Draw all twelve in one pass, with the other eleven in view: one optical weight across the set is
the single most important property of the pack.

1. Each symbol lives in a plain **0–100 square box**. Use the whole box; the runner scales and
   centers it into the container.
2. Output **bare SVG shape elements only**: `<path>`, `<circle>`, `<rect>`, `<ellipse>`,
   `<polygon>`, `<polyline>`, `<line>`, `<g>`. No `<svg>` wrapper, no XML declaration, no comments.
3. **No `<text>` or `<tspan>`, ever** — the renderer has no fonts. Draw a letterform as filled
   geometry if a member needs one.
4. No `<image>`, `<script>`, `<style>`, `<foreignObject>`, and no `href`/`src` pointing anywhere.
5. Colour: the symbol's fill is already set to the pack's `glyph_color`. Plain shapes need no fill.
   You may use `fill-opacity` between 0.35 and 0.75 for a secondary shade. No other colours.
6. Prefer solid filled shapes. If you stroke, use the glyph colour, `stroke-width` 6–9, round caps
   and joins — and the same width on every icon.
7. Same density, corner treatment and level of detail on all twelve.

Format — one delimiter line, then that icon's markup, for all twelve in pack order:

```text
=== ICON: <slug> ===
<path d="..."/>
<circle cx="50" cy="50" r="12"/>
```

Before you finish, re-read `glyphs.txt` against rules 2–4: a glyph that breaks them is dropped,
and a pack with fewer than 10 drawable glyphs is rejected.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before writing `pack.md`** and run `humanizer`'s final pass on
its prose. They never touch `glyphs.txt`. Skip their audit/report steps.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `pack.md`

```markdown
---
title: <Pack title>
date: {{DATE}}
theme: {{THEME}}
container: <container key>
---

# <Pack title>

<Short intro: the pack's style and what it's for.>

**Formats:** every icon ships as vector source in `svg/`, a transparent 1024 px PNG in `png/`, and
a multi-size Windows `.ico` (16–256 px) in `ico/`.

**Using them:** drop an `.ico` onto a folder via Properties → Customize → Change Icon, or onto a
shortcut via Properties → Shortcut → Change Icon. The SVGs are the source art for web and app UI.

## Icons

- **<Name>** (`<slug>`) — <one line on what the symbol shows and why it reads as that thing>
- ...
```

--------------------------------------------------
## FINAL MESSAGE

`icons` lists all twelve in the same order as `glyphs.txt`; each `slug` matches its
`=== ICON: <slug> ===` line exactly.

```json
{
  "title": "<Pack title>",
  "slug": "<kebab-case-slug>",
  "summary": "<one sentence: the pack's style and use>",
  "theme": "{{THEME}}",
  "category": "{{CATEGORY}}",
  "container": "<container key>",
  "glyph_color": "#FFFFFF",
  "icons": [
    {"name": "<Name>", "slug": "<slug>", "concept": "<one line>", "tile_color": "#RRGGBB"}
  ],
  "error": null
}
```
