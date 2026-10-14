# Daily App Idea Card

Goal: produce ONE app idea card — a focused, text-only Markdown one-pager pitching an app concept
anchored in a real, current trend — plus the description of a concept-art cover image.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Category: `{{CATEGORY}}`** — chosen by the runner to keep the backlog balanced. Do not pick a
different one.

{{CATEGORY_GUIDE}}

**Already in the backlog** (date · slug · title — pitch). Your idea must differ in concept, not
just in name:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research.** Use **WebSearch** (and **WebFetch** to read promising pages) to ground the idea in
   a current trend, market gap, regulatory shift, viral pain point, or new platform capability from
   the last 30 days. Bias the searches to the category.
2. **Choose the idea.** It must:
   - reflect a real, current need — not a generic "AI for X";
   - have a plausible monetization model;
   - be buildable as the category's form factor by a solo developer;
   - not repeat anything in the backlog above.
3. **Load the writing skills** (below), then write `card.md` in the OUTPUT FORMAT.
4. **Load `image-prompt-craft`**, then write the cover description (COVER IMAGE below) into the
   final JSON's `cover_prompt`.
5. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write `card.md`, and run `humanizer`'s final pass
on the draft before you save it.** This is a pitch to one reader deciding whether to build the
thing, and pitch language is where AI writing is most obvious and least useful.

Carve-outs, because those skills were written for interactive editing:

- **Ignore their workflow and output instructions** — no audit, no before/after report, no questions.
- **The OUTPUT FORMAT below wins on structure.** The skills apply to the sentences inside it.
- **Unsupported market claims go or get sourced.** "Studies show", "users increasingly demand" —
  cite a Sources entry, or state it as your own judgment. Anything you can't stand behind belongs
  in *Risks & open questions*.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `card.md`

```markdown
---
title: <App Display Name>
date: {{DATE}}
category: {{CATEGORY}}
form_factor: <web app | browser extension | mobile-style PWA | GitHub repo | CLI | AI agent | desktop app>
monetization: <subscription | marketplace fee | freemium | one-time | B2B SaaS | transaction fee | ads | donation/sponsor>
tags: [<tag1>, <tag2>, <tag3>]
status: idea
---

# <App Display Name>

> <one-line pitch — concrete, no fluff>

## Problem

<2–3 sentences: the specific pain a real person hits today. Not "people want X".>

## Target user

<Primary persona and the job to be done: role, context, why today's tools fall short.>

## MVP scope

- <4–6 bullets, each a verifiable capability, not a theme>

## Monetization

<The model and a rough pricing intuition, e.g. "Freemium: 5 free reports a month, $9/mo unlimited".>

## Why now

<2–4 sentences tied to the trends cited in Sources.>

## Risks & open questions

- <3–5 honest bullets, including one demand-side risk and one build-side risk>

## Next step

<One line, e.g. "Build a 1-hour landing page test".>

## Sources

- <URL> — <what it supports>
- <URL> — <what it supports>
```

Rules for the card:

- Text only: no images, code blocks, or UI mockups in `card.md`.
- At least **two** working source URLs from your research. Never invent sources, statistics, or quotes.
- Exact dates only — no "last week".
- Readable in under 60 seconds. Product-marketing tone for pitch/problem/user; engineering tone for
  scope and risks. No hedging adverbs unless the risk really is conditional.

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes a single concept-art illustration that captures the idea **metaphorically**
— e.g. a dark-patterns extension → a magnifying glass revealing hidden traps beneath a glossy
surface. Follow `image-prompt-craft`'s formula, with these job rules winning where they differ:

- Modern editorial-tech illustration: soft gradients, clean vector-influenced shapes, subtle depth.
- A 3–4 colour palette that suits the concept (greens/blues for finance, indigos for privacy…).
- Subject centered or slightly above, with breathing room around it. The scene runs **full-bleed**
  — no inset panel, card, mat or frame around the illustration. The runner renders it at 16:9 — don't put
  the ratio in the prompt.
- **Forbidden:** text of any kind, logos, real brands or product UIs, screenshots, app mockups,
  device frames, charts, recognisable people. Never name an object that carries text ("poster",
  "app icon", "product page").
- End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<App Display Name>",
  "slug": "<kebab-case-slug>",
  "summary": "<the one-line pitch>",
  "category": "{{CATEGORY}}",
  "form_factor": "<as in the frontmatter>",
  "monetization": "<as in the frontmatter>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
