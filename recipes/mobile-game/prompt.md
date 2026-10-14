# Mobile Game

Goal: build ONE complete, self-contained, immediately playable **phone game** as a single
`index.html` — portrait-first, touch-first, rendered inside an on-screen phone frame — plus a short
design brief and the description of a cover.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Genre: `{{GENRE}}`** — chosen by the runner from a weekly rotation. Build a game in this genre; do
not substitute another.

**Games already built** (date · slug · title — hook). Pick a clearly different title and concept —
and compare on the **core loop**, not the theme:

{{EXISTING}}

You MAY use **WebSearch** / **WebFetch** if the genre needs grounding (a word game needs a real word
list). Most casual and arcade genres need none.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `game-design` before you choose the concept, and `single-file-game-dev` before you write
`index.html`.** `game-design` decides whether the game is worth playing; `single-file-game-dev`
decides whether it runs correctly on a phone, and it is the one skill that shapes the code. This job
is touch-first and phone-first, so every mobile failure mode in it applies directly.

From `game-design`:

- **Write the one-sentence core loop before anything else** — verb, pressure, escalation, no genre
  words. A theme swap ("match-3, but space") is not a new game; variety comes from changing the
  *decision*, not the skin.
- **One verb, deep.** A single action with a variable outcome (how long you hold, when you release,
  where you tap) is what works under a thumb. Four shallow buttons do not.
- **Ramp *kinds* of pressure, not one number.**

From `single-file-game-dev`, in the order these actually break a phone game:

- **`{ passive: false }` on touch listeners plus `touch-action: none` in CSS.** Both, not either —
  otherwise `preventDefault()` is a silent no-op and the page scrolls, zooms and rubber-bands
  mid-drag. This is the single most common reason a mobile web game feels broken.
- **Delta time** on everything time-based, or the game runs twice as fast on a 120Hz phone.
- **`devicePixelRatio`** on the canvas backing store, capped at 2, or it's blurry on every phone.
- **Safe areas and thumb reach.** Nothing interactive or readable within ~44 CSS px of an edge;
  controls in the bottom third, never the top corners.
- **Unlock WebAudio on the first tap**, or it's silent on iOS.
- **No allocation in the frame loop**; pool what you spawn.

**Load `llm-writing` and `humanizer` before writing `game-design-brief.md`** and run `humanizer`'s
final pass on it. Brief only — never `index.html`. Skip their audit/report steps. *What makes it
fun* must name the specific tension, decision, or moment — not "addictive and satisfying".

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `index.html` — hard requirements

- **One file.** All CSS in one `<style>`, all JS inline in `<script>`. **Zero local sibling files.**
- **Phone form factor.** The game sits inside a centered **portrait phone frame** (a simple bezel /
  rounded "screen") on a muted backdrop, so it reads as a phone game even in a landscape iframe. The
  play area is portrait (about 9:16 or 3:4) and scales to the viewport height without overflowing.
- **Touch-first controls** — tap / swipe / drag / hold, with on-screen controls where the genre needs
  them — **and** keyboard/mouse equivalents so it's testable on desktop. Detect touch and adapt the
  hint ("Tap to start" vs "Click to start").
- **Dependencies:** prefer vanilla `<canvas>` + JS. The only allowed external script is p5.js from
  `https://cdn.jsdelivr.net/npm/p5@1.11.3/lib/p5.min.js`, and only if the genre genuinely benefits.
  No external images or sounds — draw with canvas/CSS/emoji, synthesize audio with WebAudio.
- **Playable on open** from `file://`, or a clear "Tap to start" screen.
- **No top-level use of late-assigned variables.** One uncaught `TypeError` during initial script
  execution kills the whole inline script — including the `load` listener at the bottom — and leaves
  a title screen that looks fine and responds to nothing. Either assign every element reference at
  the very top of the script, or attach every listener inside the same init callback that assigns
  them. Never mix the two.
- A visible live **score** (or level) inside the phone screen, and an on-screen **restart** button
  after game over (plus `R` on desktop).
- A comment block at the top naming the game, genre, and controls.

**Before you finish, review the initial execution path**: re-read every top-level statement of the
script and confirm none dereferences a variable assigned later. The runner also runs `node --check`
on the script and rejects the run if it fails.

### `game-design-brief.md`

No frontmatter:

```markdown
# <Game Title>

> <one-sentence hook>

**Date**: {{DATE}}
**Genre**: {{GENRE}}
**Platform**: Mobile (portrait, touch-first)
**Core loop**: <the one-sentence loop>

## How to play
<Objective, what the player taps/swipes, how they win or lose, the desktop key equivalents.>

## Core mechanics
- <3–5 bullets>

## Progression & scoring
<How difficulty and score ramp over a session.>

## Look & feel
<Palette, visual style, how sound and feedback are generated, the phone-frame presentation.>

## What makes it fun
- <2–4 bullets, each a specific tension, decision or moment>
```

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. `cover_prompt` describes one piece of **key art** showing the game's
visual style and central subject — a runner leaping between neon rooftops, a cascade of glowing gems
mid-match. Vibrant casual-game art matched to the genre; a 3–4 colour palette; the scene full-bleed
with no inset panel or frame (the runner renders 16:9 — don't put the ratio in the prompt). A
stylised handheld motif is optional.

**Forbidden:** the title or any other text, logos, real brands, real iOS/Android or app-store UI,
recognisable people. Never ask for "box art", a "poster" or an "app icon" — they carry text. End with
the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Game Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the one-sentence hook>",
  "genre": "{{GENRE}}",
  "controls": "<one line: touch + desktop keys>",
  "gameplay": "<one sentence on how it plays>",
  "cdn_deps": "<none, or the exact URL>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
