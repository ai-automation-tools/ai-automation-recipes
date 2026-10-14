# Comic

Goal: write ONE four-panel comic strip — a script with dialogue — and the image prompt for the
finished full-page strip, which the runner renders.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Topic: `{{TOPIC}}`** — chosen by the runner from a rotation. Build the strip around it.

**Strips already made** (date · slug · title — logline). Find a different joke, not a reworded one:

{{EXISTING}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write `script.md`** and run `humanizer`'s final
pass on it. Skip their audit/report steps. Comic dialogue is a protected register: fragments,
interruptions and deliberate repetition are timing, not tells.

**Load `image-prompt-craft` before you write the image prompt.** This strip is the skill's text
exception — it carries speech balloons — so its general "no text" rule does not apply to the
balloons. Everything else in the skill does.

--------------------------------------------------
## THE STRIP

- Four panels, read left to right: setup, development, turn, punchline. The last panel has to
  land on its own.
- Humorous, satirical or dry — pick one register and hold it.
- **Original, clearly fictional cartoon characters only.** Never name, describe or caricature a
  real, recognisable or famous person, and no real brand logos or trademarks — stand-ins only.
  Image models refuse real people, and this collection doesn't depict them.
- Give the strip a recurring-sounding series name, as if it ran every week.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `script.md`

```markdown
---
title: <Strip Title>
series: <Series Name>
date: {{DATE}}
topic: <the topic>
humor_type: <satire | dry | slapstick | absurdist>
characters: [<Name 1>, <Name 2>]
---

# <Strip Title>

*<Series Name>* · <one-line setting>

## Panel 1
**Scene:** <what we see>
**<NAME>:** <dialogue>

## Panel 2
…

## Panel 3
…

## Panel 4
…
```

Every panel heading must be exactly `## Panel 1` … `## Panel 4`.

--------------------------------------------------
## THE IMAGE

One full-page image of the whole strip: four panels in a single row or a 2×2 grid, clean gutters,
a consistent newspaper-comic art style, the same character designs in every panel.

- **Balloon text:** quote each balloon exactly as in the script, at most about six words per
  balloon — long or small lettering garbles. If a line is longer, shorten it in the balloon and
  keep the full line in `script.md`.
- Describe each panel's composition in order, then the shared style and a 3–4 colour palette.
- End with: "Depict only original, fictional cartoon characters; no real or recognisable people,
  no real logos or trademarks, no watermark, no signature."
- Pick the aspect that fits the layout: `16:9` for a single row, `1:1` or `3:4` for a 2×2 grid.
  Put it in the JSON, never in the prompt.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Strip Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<one-line logline of the joke>",
  "series": "<Series Name>",
  "topic": "{{TOPIC}}",
  "humor_type": "<as in the frontmatter>",
  "images": [
    {"file": "comic.png", "aspect": "<16:9 | 1:1 | 3:4>", "prompt": "<the full-page strip prompt>"}
  ],
  "error": null
}
```
