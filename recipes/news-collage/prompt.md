# News Collage

Goal: research the major U.S. news stories of **{{WINDOW_LABEL}}** and write ONE image prompt for a
cartoon-editorial news image of them, which the runner renders. The stories, their sources and
every caption go in `stories.md`.

Target date: **{{DATE_LONG}}** (`{{DATE}}`). Story window: `{{DATE_FROM}}` to `{{DATE_TO}}`.

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Window: `{{WINDOW}}`** — chosen by the runner. Use the dates above exactly; do not recompute them.

**Layout for this window:** {{LAYOUT}}.

**Title and stamp:** {{TITLE_LINE}} **"{{STAMP}}"**.

**Images already made** (date · slug · title — summary). A new window, not a reworded one:

{{EXISTING}}

--------------------------------------------------
## RESEARCH

Use **WebSearch** and **WebFetch**. Pick **{{COUNT}}** U.S. stories from the window that are
nationally relevant, visually distinct from each other, and together cover the spread (politics,
economy, weather, technology, legal, sports, health, national events, culture). For a week or a
month prefer stories that ran or mattered across the whole window over one-off minor updates.
Every story needs a source URL you actually opened.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `image-prompt-craft` before you write the image prompt.** It owns the prompt formula and the
constraint block. **This file wins wherever the two differ**, and they differ in one place:

- **Ignore the skill's "no panel labels or captions" line.** This image is the skill's text
  exception, like a meme: the embedded in-world captions *are* the deliverable. Write each caption
  into the prompt as an **exact quoted string**, 3–8 words, rendered large and high-contrast. Small
  or long text garbles, and you cannot look at the render here, so short and exact is the only
  defence you have.

--------------------------------------------------
## THE IMAGE

- **Style, stated once and said to cover every panel or the whole scene:** cartoon / editorial comic
  style, bright colours, bold outlines, expressive generic characters, modern polished digital
  illustration, satirical energetic newsroom feel, one illustrator, one light source, one named
  3–4 colour palette.
- State the layout in the prompt text exactly as given above. For the grid, give each panel one
  short clause describing a **single clear action**; six busy panels read as mud. For the scene,
  name the one environment first and put every story *inside* it as an object; a list of stories
  renders as floating vignettes.
- **Embedded text:** each story carries one caption of 3–8 words as in-world text: a document
  headline, protest sign, placard, courtroom exhibit, podium sign, scoreboard, map label, newspaper
  front page, screen, product label, agency seal or building signage. Never a caption strip, never
  a numbered panel, never a vague label ("Breaking News", "Politics") without the story's context.
  Text must not cover the action it labels.
- **Real-person rule (hard):** never ask for a recognisable face, portrait, caricature, lookalike or
  physical likeness of any real living person. Depict a named person's story through symbolic scene
  elements: a labelled podium, a courthouse sketch, a ballot map, a policy document, press
  microphones, a motorcade silhouette, a generic crowd, a headline. Real names may appear **only**
  as in-world text on those objects.
- End the prompt with: "Depict only generic cartoon people and symbolic props; no likeness of any
  real person, no real logos beyond the quoted text, no watermark, no signature."
- Put the aspect in the JSON only: `{{ASPECT}}` for this window.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `stories.md`

```markdown
---
title: <News Collage — {{WINDOW_LABEL}}>
window: {{WINDOW}}
date_from: {{DATE_FROM}}
date_to: {{DATE_TO}}
date: {{DATE}}
---

# <Title>

Window: {{WINDOW_LABEL}} · stamp shown: "{{STAMP}}"

### <Story headline>
<One-line summary of what happened and why it mattered.>
**Source:** https://...
**Caption:** "<the exact 3–8 words in the image>"

### <Story headline>
…
```

One `### ` block per story, in the order they appear in the image (grid: left to right, top to
bottom; scene: foreground first). The `**Caption:**` line is quoted and matches the prompt
word for word.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Title>",
  "slug": "<kebab-case-slug, e.g. news-collage-2026-10-13>",
  "summary": "<one line: the window and the stories it carries>",
  "window": "{{WINDOW}}",
  "story_count": <number of stories>,
  "images": [
    {"file": "collage.png", "aspect": "{{ASPECT}}", "prompt": "<the full image prompt>"}
  ],
  "error": null
}
```
