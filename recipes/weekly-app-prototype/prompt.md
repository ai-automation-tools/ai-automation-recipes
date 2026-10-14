# Weekly App Prototype

Goal: build ONE substantial, runnable app prototype — a timely idea that could realistically make
money — as a single-page demo with requirements, sample data, and the description of a cover.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

Concepts may come from any field (productivity, finance, health, creator tools, dev tools, civic
tech, e-commerce, education, real estate, climate…) and any form factor that runs as a single page:
web app, mobile-style PWA, desktop-style web tool, or a demo of a small GitHub repo or CLI.

🚫 **Browser extensions are out of scope.** If the best idea needs to read, change, or react to
pages the user is already on, or live in the toolbar / context menu / side panel / omnibox, set it
aside and pick another. Don't file it here as a "web app version" of an extension.

**Prototypes already built** (date · slug · title — pitch). Pick a clearly different concept:

{{EXISTING}}

**Browser extensions already built** (don't rebuild one of these as a web app):

{{SIBLING_EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research.** Use **WebSearch** (and **WebFetch** to read promising pages) to ground the idea in
   the last 30 days: recent launches, market gaps, regulatory shifts, viral pain points, new platform
   capabilities, rising consumer behaviour.
2. **Choose ONE idea.** It must be timely, have a plausible monetization model (subscription,
   marketplace fee, freemium, one-time, B2B SaaS, transaction fee, ads…), not be a browser extension,
   be demonstrable as a single page with HTML/CSS/JS plus a sample-data JSON file, and not repeat
   anything listed above.
3. **Load the writing skills** (below) and write `README.md` and `requirements.md`.
4. **Build the prototype**: `index.html`, `style.css`, `script.js`, `sample-data.json`.
5. **Load `image-prompt-craft`** and write the cover description into `cover_prompt`.
6. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write `README.md` / `requirements.md`, and run
`humanizer`'s final pass over both before you save them.** A pitch is where AI writing is worst —
unearned superlatives, *revolutionary / seamless / game-changing / empowers*, padded three-item
lists, confident demand claims with nothing behind them. A reader should finish the README believing
a person thought this through.

Carve-outs, because those skills were written for interactive editing:

- **Ignore their workflow and output instructions** — no audit, no report, no questions.
- **The OUTPUT FORMAT below wins on structure.** The skills apply to the sentences inside it.
- **Prose only** — `README.md` and the prose of `requirements.md`. Never the code, the JSON, code
  comments, or the terse spec lines and user stories, which should read like a spec.
- 🚨 **Keep the honest hedges.** The section is "Why it could be **profitable**", not "why it will
  be". A calibrated claim about an unbuilt product is accuracy, not padding. Cite the trend, name the
  model, say plainly where the demand rationale is thin. Overclaiming is the failure mode here.
- **Product register yes, marketing copy no.** Describe what the app does in plain product language;
  don't sell it.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `README.md`

```markdown
# <App Display Name>

> <one-line pitch>

**Date**: {{DATE}}
**Form factor**: <web app | mobile-style PWA | desktop-style web tool | GitHub repo | CLI>
**Status**: Prototype

## What it is

<2–3 sentence elevator description.>

## Who it serves

<Primary persona and the specific pain point.>

## Why it could be profitable

<Monetization model and an honest demand rationale, citing the timely trend(s) with at least one URL.>

## Form factor & scope

<Which surface this lives on and the minimum scope this prototype demonstrates.>

## How to run it

1. Open `index.html` in any modern browser.
2. <Anything else needed to see the core flow.>

## What's in this prototype

<Bullets: which screens, which interactions, what data is loaded.>

## Roadmap

- <3–5 next features>

## Sources

- <URL> — <what it supports>
- <URL> — <what it supports>
```

### `requirements.md`

```markdown
# <App Display Name> — Requirements

## Goals
<bullets>

## Primary user
<persona, context of use, job to be done>

## Functional requirements
- FR1: <…>   (8–15 entries)

## User stories
- As a <role>, I want to <action>, so that <outcome>.   (5–10 stories)

## Non-functional requirements
- <performance / accessibility / privacy / data handling>

## Out of scope (for the prototype)
- <…>

## Open questions
- <…>
```

### `index.html` · `style.css` · `script.js` · `sample-data.json`

- `index.html`: semantic HTML5; a `<header>` with the app name, a primary view, and the controls the
  core flow needs. Links `style.css` and `script.js` by relative path.
- **It must run from `file://`.** Browsers block `fetch()` of a local file there, so put the sample
  data in an inline `<script type="application/json" id="sample-data">` block that `script.js`
  reads, and ship the same data as `sample-data.json`. Say so in "How to run it".
- `style.css`: modern and readable, mobile-friendly with flex/grid and media queries. No CSS
  framework unless the prototype genuinely benefits (HTTPS CDN only).
- `script.js`: vanilla JS (or one HTTPS-CDN library if the concept needs it, e.g. Chart.js). Renders
  the core view and wires at least one interactive control that meaningfully demonstrates the idea.
- `sample-data.json`: realistic, plausible, strictly valid JSON; 8–25 records.
- No server code, no API keys, no network calls that need auth. Every local file the page references
  must exist. The prototype should look intentional, not generic — pick colour, layout and
  typography that fit the concept.

Rules: real research only — never fabricate sources, statistics, or quotes; at least two sources;
exact dates, never "last week". Product tone in the README, engineering tone in the requirements,
short readable code.

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes a single concept-art illustration that captures the app's core idea
**metaphorically** — a property-tax-appeal app as a stylised house under a magnifying glass; a
tariff-refund app as stacked shipping containers with a green refund tag. Follow
`image-prompt-craft`'s formula; these job rules win where they differ:

- Modern editorial-tech illustration: soft gradients, clean vector-influenced shapes, subtle depth.
- A 3–4 colour palette that suits the concept, named.
- Subject centered or slightly above, with breathing room; the scene runs **full-bleed** — no inset
  panel, card or frame. The runner renders 16:9 — don't put the ratio in the prompt.
- **Forbidden:** any text, logos, real brands or product UIs, screenshots, app mockups, charts,
  device frames, recognisable people.
- End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<App Display Name>",
  "slug": "<kebab-case-slug>",
  "summary": "<the one-line pitch>",
  "form_factor": "<as in the README>",
  "monetization": "<the model, in a few words>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
