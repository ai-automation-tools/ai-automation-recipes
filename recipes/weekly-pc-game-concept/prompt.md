# Weekly PC Game Concept

Goal: produce ONE original, substantial **PC game concept** in this week's genre — a game-design brief,
a polished one-page pitch, and key art — the package a small studio or solo dev could take into a
pre-production greenlight discussion.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Genre: `{{GENRE}}`** — chosen by the runner from a weekly rotation. Do not pick a different one.

**Concepts already written** (date · slug · title — hook). Pick a clearly different concept:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research the genre.** Use **WebSearch** (and **WebFetch**) to find **3–5 current reference
   points** in {{GENRE}}: recent or notable releases, genre staples, current design conversations,
   what players praise or criticise right now. Use `after:` / `before:` qualifiers and prefer primary
   sources (developer posts, store pages, reputable outlets). Ground the design in them — don't
   clone any one game.
2. **Design ONE concept** that fits {{GENRE}} unmistakably while carving out its own specific angle,
   realistically scoped as a PC title (keyboard/mouse or controller, Steam-style distribution).
3. **Load the skills** (below), then write `game-design-brief.md`, `pitch.html` and `sources.csv`.
4. **Load `image-prompt-craft`** and write the key-art description into `cover_prompt`.
5. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `game-design` before you choose the concept.** This job ships a design document and no code.
Take three things from it:

- **The one-sentence core loop, written first** — verb, pressure, escalation, no genre words. If the
  sentence would fit another game unchanged, it isn't a loop sentence.
- **`references/pitch-and-brief.md`** — the vagueness traps and the buildability test: what does the
  player press; how does a run end; what's on screen at second 5 / 30 / 90; what number goes up and
  what makes it go up fastest; what does the player see the instant before failure; what are the
  difficulty values at each step. Any "the implementer would decide" is a hole.
- **`references/difficulty-and-progression.md`** for the ramp — distinct *kinds* of pressure, plus
  the fairness guarantees that separate "hard" from "cheap".

**Load `llm-writing` and `humanizer` before you write the brief, and run `humanizer`'s final pass on
it.** This is a design document, not a press release. Carve-outs: ignore their workflow and output
instructions (no audit, no report, no questions); the template below wins on structure; and **a
differentiator that describes a hundred games isn't one** — "a unique blend of exploration and
combat" is the failure mode. The brief is better when it argues with itself: state the loop, then the
specific way it gets boring in hour three.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `game-design-brief.md`

No frontmatter:

```markdown
# <Game Title>

> <one-sentence hook>

**Date**: {{DATE}}
**Genre**: {{GENRE}}
**Platform**: PC (Windows; <controller and/or keyboard & mouse>)
**Core loop**: <the one-sentence loop>
**Status**: Concept

## Target player
<Who it's for, the games they already love, the itch this scratches.>

## Core loop
<The 30-second loop and the 30-minute loop, concretely.>

## Systems
<4–8 bullets, each naming a system and what makes it tick.>

## Progression
<Unlocks, difficulty curve, meta-progression, run structure — with values.>

## World & setting
<Setting, tone, art direction, the fantasy the world sells. 1–2 short paragraphs.>

## Differentiators
- <3–5 bullets, each the specific thing no comparable in Genre references does>

## Monetization notes
<Model (premium / early access / DLC / cosmetic…), a rough price point, an honest read on the market.>

## Accessibility notes
<Remappable controls, colourblind-safe palettes, assist options, scalable UI, subtitles, motion and
photosensitivity options.>

## Risks
- <3–5 design / scope / market risks, each with a one-line mitigation>

## 6-week prototype plan
- **Week 1**: <goal + concrete deliverable>
- … through **Week 6**: <vertical-slice / playtest milestone>

## Genre references
- <Game / source> — <URL> — <what it informs>   (3–5, matching sources.csv)
```

### `pitch.html`

- One self-contained page: **all CSS and JS inline**. No external scripts; one HTTPS web font is the
  only allowed external resource.
- Leads with the title, the hook, the genre/platform line and the key art as
  `<img src="cover.png">` (the runner renders `cover.png` next to the page after you finish).
- Shows the pitch at a glance: target player, core loop, standout systems, differentiators.
- A **"Key features" list with a small "Copy" button per bullet** (inline JS,
  `navigator.clipboard.writeText`, a brief "Copied" confirmation, and a graceful fallback when the
  clipboard API is unavailable).
- Visual design fits the game's tone — a real pitch-deck page, strong in the first screenful.

### `sources.csv`

Strict CSV with a header row, 3–5 references, quoting any field that contains a comma:

```
title,url,note
<reference name>,<https URL>,<what it informed>
```

Rules: real research only — never fabricate sources, statistics, studios, or games; exact dates.

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes a single piece of **key art** for the concept's core fantasy and mood — a lone
diver silhouetted against a bioluminescent trench for a survival-crafting game; a rain-soaked
detective's desk under one lamp for a mystery. It's the card cover and the hero of `pitch.html`.

Follow `image-prompt-craft`; these rules win where they differ:

- Use **"key art"** or **"a cinematic illustration of…"** as the noun. Never write "Steam capsule",
  "box art", "store page" or "game poster" into the prompt — they carry title treatments.
- Name a deliberate 3–4 colour palette and lighting (e.g. "deep teal, sodium orange, bone white,
  near-black").
- 16:9 composition (the runner sets the ratio — don't write it), full-bleed, no inset frame.
- **Forbidden:** any text, logos, real game UIs/HUDs, real company or IP names, screenshots, menu
  mockups, recognisable real people, gore.
- End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Game Title>",
  "slug": "<kebab-case concept slug>",
  "summary": "<the one-sentence hook>",
  "genre": "{{GENRE}}",
  "differentiators": ["<first>", "<second>", "<third>"],
  "cover_prompt": "<the full key-art description>",
  "error": null
}
```
