# Weekly Browser Game

Goal: build ONE complete, self-contained, immediately playable browser game as a single
`index.html`, plus a short design brief and the description of a cover image.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Genre: `{{GENRE}}`** — chosen by the runner from a rotation. Build a game in this genre; do not
substitute another.

**Games already built** (date · slug · title — hook). Pick a clearly different title and concept:

{{EXISTING}}

You MAY use **WebSearch** / **WebFetch** if the genre needs grounding (a word game needs a real word
list, a quiz needs real facts). Most arcade and puzzle genres need none.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `game-design` before you choose the concept, and `single-file-game-dev` before you write
`index.html`.** `game-design` decides whether the game is worth playing; `single-file-game-dev`
decides whether it runs correctly in a browser, and it is the one skill that shapes the code.

From `game-design`, the two that matter most:

- **Write the one-sentence core loop before anything else** — verb, pressure, escalation, no genre
  words. If you can't write it, the concept isn't finished.
- **Ramp *kinds* of pressure, not one number.** `speed *= 1.05` is trivial for forty seconds and
  impossible three seconds later.

From `single-file-game-dev`, the failures that are invisible on a desktop:

- **Delta time** on everything time-based, or the game runs twice as fast on a 120Hz phone.
- **`devicePixelRatio`** on the canvas backing store, or it's blurry on every phone.
- **`{ passive: false }`** on touch listeners, or the page scrolls and zooms mid-game.
- **Unlock WebAudio on the first user gesture**, or it's silent on iOS.
- **No allocation inside the frame loop** — pool what you spawn.

**Load `llm-writing` and `humanizer` before writing `game-design-brief.md`** and run `humanizer`'s
final pass on it. They apply to the brief only — never let them touch `index.html`. Skip their
audit/report steps. The tell this format breeds is fun-by-assertion: *What makes it fun* must name
the specific tension, decision, or moment, not "addictive and satisfying".

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `index.html` — hard requirements

- **One file.** All CSS in one `<style>`, all JS inline in `<script>`. **Zero local sibling files.**
- **Dependencies:** prefer vanilla `<canvas>` + JS. The only allowed external script is p5.js from
  `https://cdn.jsdelivr.net/npm/p5@1.11.3/lib/p5.min.js`, and only if the genre genuinely benefits.
  No external images or sounds — draw with canvas/CSS/emoji, synthesize audio with WebAudio.
- **Playable on open** from `file://`: it starts, or shows a clear "press any key / tap to start".
- **No top-level use of late-assigned variables.** One uncaught `TypeError` during initial script
  execution kills the entire inline script — including the `load` listener at the bottom — and
  leaves a title screen that looks fine and responds to nothing. Either assign every element
  reference at the very top of the script (it sits at the end of `<body>`, so the DOM exists), or
  attach every listener inside the same init callback that assigns them. Never mix the two.
- **Controls:** keyboard or mouse, **and** touch-aware (on-screen controls or tap zones where a
  keyboard game needs them).
- A visible live **score** (or level/progress), and a clear **restart** after game over.
- Responsive: scales or letterboxes on desktop and phone viewports; never overflows.
- A comment block at the top naming the game, genre, and controls.

**Before you finish, review the initial execution path:** re-read every top-level statement of the
script (everything outside function bodies and callbacks) and confirm none of it dereferences a
variable assigned later. The runner also syntax-checks the script with `node --check` and rejects
the run if it fails.

### `game-design-brief.md`

No frontmatter. Keep this structure:

```markdown
# <Game Title>

> <one-sentence hook>

**Date**: {{DATE}}
**Genre**: {{GENRE}}
**Core loop**: <the one-sentence loop>

## How to play

<Objective and controls, concrete: what the player does, how they win or lose, what keys/taps do.>

## Core mechanics

- <3–5 bullets>

## Progression & scoring

<How difficulty and score ramp over a session.>

## Look & feel

<Palette, visual style, and how sound and feedback are generated.>

## What makes it fun

- <2–4 bullets, each a specific tension, decision or moment>
```

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. `cover_prompt` describes one piece of **key art** showing the game's
visual style and its central subject — a neon ship weaving through asteroids, a serpent coiling
through a glowing grid. Vibrant game-art style matched to the genre; a 3–4 colour palette; subject
centered with breathing room, the scene running full-bleed — no inset panel or frame (the runner
renders 16:9 — don't put the ratio in the prompt).

**Forbidden:** the title or any other text, logos, real brands or UIs, recognisable people. Never
ask for "box art", a "poster" or a "Steam capsule" — they carry titles. End with the skill's
constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Game Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the one-sentence hook>",
  "genre": "{{GENRE}}",
  "controls": "<one line: keyboard / mouse / touch>",
  "gameplay": "<one sentence on how it plays>",
  "cdn_deps": "<none, or the exact URL>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
