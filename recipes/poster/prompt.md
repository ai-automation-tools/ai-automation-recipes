# Poster

Goal: design ONE striking vertical poster on a given theme — a concept, a title, a caption — and
write the image prompt the runner renders at 2:3.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Theme: `{{THEME}}`** — chosen by the runner from the theme list, least-used first.

**Posters already made** (date · slug · title — caption). Find a fresh angle on the theme:

{{EXISTING}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `image-prompt-craft` before you write the image prompt.** A poster may carry its title or
caption as designed lettering, so the skill's "no text" rule is relaxed for **that one line only**
— quote it exactly and keep it to a few words. Everything else in the skill applies, including
the constraint against any other text, stat blocks, credits or watermarks.

**Load `llm-writing` before you write `poster.md`.** Skip its audit/report steps.

--------------------------------------------------
## THE POSTER

- A specific, visually striking concept for the theme — not a generic illustration of the word.
- Modern, high-quality, professional design; centered, balanced composition; vertical 2:3.
- Name the style precisely (an era, a medium, a print technique) and a 3–4 colour palette.
- Lettering is optional. If the design uses it, it is the title or the caption — one line, a few
  words, spelled exactly — integrated into the design, not floating on top.
- No real, recognisable people; no real brand logos; no living artist named as a style reference.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `poster.md`

```markdown
---
title: <Poster Title>
date: {{DATE}}
theme: {{THEME}}
style: <the named style>
keywords: [<word>, <word>, <word>]
---

# <Poster Title>

> <the caption or tagline>

<Two or three sentences: the concept, what the eye lands on first, why it suits the theme.>

**Lettering:** <the exact text in the image, or "none">
```

--------------------------------------------------
## THE IMAGE PROMPT

One continuous descriptive prompt, 60–150 words: subject, style, palette, composition and
lighting, textures, mood; then the lettering (quoted exactly, with placement and treatment) if
any; then the skill's constraint block adapted to allow only that lettering. Never write the
aspect ratio into the prompt.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Poster Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the caption or tagline>",
  "theme": "{{THEME}}",
  "style": "<the named style>",
  "images": [
    {"file": "poster.png", "aspect": "2:3", "prompt": "<the full poster prompt>"}
  ],
  "error": null
}
```
