# Weekly Short Story

Goal: write ONE complete, original, publishable short story, plus the description of a cover
illustration.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Genre: `{{GENRE}}`** — chosen by the runner from a rotation. Treat it as the lane, not a
template: subvert it if the story is better for it.

**Premise:** {{IDEA}}

**Stories already written** (date · slug · title — logline). Do not reuse a premise, title,
character, or core twist:

{{EXISTING}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you draft, and run `humanizer`'s final pass on the
finished story before you save it.** Skip their audit/report steps and ask no questions. Fiction is
a protected register: deliberate fragments, repetition and a narrator's tics are craft, not tells —
the skills apply to default-LLM phrasing, not to voice.

--------------------------------------------------
## THE STORY

- **2,000–4,000 words**, complete: a clear premise, characters the reader remembers, and an ending
  that pays off. Not a scene, an outline, or a teaser.
- It stands alone and reads as finished short fiction.
- Specific over generic: named places, concrete objects, dialogue that sounds like a person.
- No epigraph, no author's note, no "The End".

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `story.md`

```markdown
---
title: <Story Title>
date: {{DATE}}
genre: {{GENRE}}
logline: <one sentence>
word_count: <approximate count>
---

# <Story Title>

<the story, as markdown paragraphs; `* * *` for scene breaks; no other headings>
```

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. `cover_prompt` describes one atmospheric illustration of a single
pivotal image from the story — a place, an object, or a figure seen at a distance — not a summary
of the plot. Cinematic digital painting, rich texture, a 3–4 colour palette that matches the
story's mood, the scene running full-bleed with no inset panel or frame, subject placed with room above and below (the runner renders portrait 2:3 — don't put
the ratio in the prompt).

**Forbidden:** the title, author, or any other text; logos; recognisable real people. Never ask for
a "book cover" or "poster" — they carry titles. End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Story Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the logline>",
  "genre": "{{GENRE}}",
  "word_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
