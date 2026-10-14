# AI Meme

Goal: invent ONE original meme — a visual joke plus its caption — and write the image prompt the
runner renders as a square meme with the caption baked in.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Theme: `{{THEME}}`** — chosen by the runner so the collection stays varied.

{{IDEA}}

**Memes already made** (date · slug · title — caption). Don't repeat a joke or a setup:

{{EXISTING}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `image-prompt-craft` and use its MEME pattern.** This recipe is the skill's documented
text exception: the caption baked into the image IS the deliverable, so the skill's general
"no text, letters or numbers" rule does not apply here. Everything else in the skill does —
quote the caption exactly, keep it short, render it large.

--------------------------------------------------
## THE MEME

- **Original.** Inspired by current meme language and internet humour, never a copy of an
  existing meme template.
- **One clear visual joke**, readable at thumbnail size: one subject, one situation, an
  exaggerated reaction or contrast.
- **Caption:** top, bottom or both; together no more than about twelve words, each line short.
  Bold, high-contrast, correctly spelled. No empty caption boxes.
- **No real, identifiable people** — no celebrities, politicians or public figures, by name or by
  description. Use clearly fictional stand-ins. No real brand logos.
- Punch up, not down. No slurs, no jokes about protected groups, nothing sexual.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `meme.md`

```markdown
---
title: <short name for the joke>
date: {{DATE}}
theme: {{THEME}}
caption_top: "<exact top caption, or empty>"
caption_bottom: "<exact bottom caption, or empty>"
---

# <short name for the joke>

<One or two sentences: the joke and why it lands.>

**Alt text:** <a plain description of the image, captions included, for screen readers>
```

--------------------------------------------------
## THE IMAGE PROMPT

One square meme: describe the scene, then the caption placement — quote each caption exactly,
say where it sits and that it is large, bold, white with a black outline (or another high-contrast
treatment that suits the scene). Name a style ("cinematic photo", "glossy 3D render", "flat
cartoon") and end with: "No other text, no watermark, no signature, no border; no real or
recognisable people, no real logos."

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<short name for the joke>",
  "slug": "<kebab-case-slug>",
  "summary": "<the caption, top and bottom joined with ' / '>",
  "theme": "{{THEME}}",
  "images": [
    {"file": "meme.png", "aspect": "1:1", "prompt": "<the full meme prompt with the exact caption>"}
  ],
  "error": null
}
```
