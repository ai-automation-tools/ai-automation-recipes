# Alternate History

Goal: write ONE illustrated "what if" timeline — a real, well-documented turning point in history,
changed at one clear point of divergence, traced forward section by section — plus the image
prompts that illustrate it.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Premise:** {{IDEA}}

**Timelines already written** (date · slug · title — premise). Do not reuse a divergence point,
and don't land in the same era as the last few if you can help it:

{{EXISTING}}

--------------------------------------------------
## WHAT MAKES A GOOD PIECE

- **One clean divergence.** Anchor in real history, then change exactly one thing — a battle, an
  assassination that did or didn't happen, a decision, a near-miss. State the real event clearly
  before you diverge from it.
- **Plausible cascade.** Each section follows believably from the last. Favour second- and
  third-order consequences (politics, technology, ordinary lives) over cartoonish extremes. No
  magic, no aliens.
- **Forward motion.** Sections move forward in time from the divergence: days, then years, then
  decades.
- **Human texture.** Ground some sections in a person's-eye view of living in this timeline, not
  just a chronicle.
- **The history stays real up to the divergence.** Don't soften a documented fact to make the
  alternate timeline tidier.

**Tone.** Serious speculative fiction, the kind of "what if" a good history podcast would explore.
Treat real people and real tragedies with respect. **Non-graphic**: when a premise involves a death
or an atrocity, write the human and geopolitical aftermath, never the act. Even-handed, no
propaganda, no slurs, no conspiracy framing.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `writing-principles`, `creative-writing-craft`, `llm-writing` and `humanizer` before you
write**, and also read `writing-principles`' `resources/failure-modes.md` and
`creative-writing-craft`'s `resources/prose-writing.md`. Those four govern the prose.
`image-prompt-craft` governs the nine image prompts instead — the cover, the shared style and each
section's scene — and the rules under OUTPUT FILES win wherever the two differ.

Four exceptions, because these skills were written for an interactive editing session and this is
not one:

- **Ignore every instruction about your output format, deliverables, workflow, loading other
  skills, spawning agents, or asking anyone anything.** The output files and final message below
  override all of it.
- **You write prompts; you do not render.** The runner renders images after you exit, so
  `image-prompt-craft`'s look-at-it-and-regenerate loop does not apply to you. Its prompt formula,
  constraint block and consistency-across-a-set rules do — they are why it is loaded. Don't call an
  image tool, and don't put an aspect ratio, a filename or an instruction to an agent in any prompt.
- **This is compressed historical narration, not a scene-built story.** Each section is ~100–130
  words covering years or decades, so the craft references' scene-construction and psychic-distance
  advice applies only where it fits. What carries over completely: concrete detail over summary, no
  editorializing, and every AI tell in the antipattern list.
- **The history has to stay real up to the divergence.** Don't soften a documented fact to make the
  alternate timeline tidier, and keep the consequences plausible rather than dramatic.

The tells that hurt this format most are the ones the skills call significance inflation and vague
attribution — "a turning point that would reshape the century", "historians would later argue".
Alternate history reads as real reporting from an unreal world, so state what happened and let it
land.

Run `humanizer`'s final pass on the intro and every section silently before you save — the revised
text only, never the audit.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `story.md`

```markdown
---
title: <evocative title of the timeline>
date: {{DATE}}
era: <short label, e.g. Cold War>
premise: <one sentence: the "what if" in plain language>
divergence_point: <the real event and date, and exactly how it went differently>
---

# <Title>

> **What if…** <premise>

<intro: ~120 words establishing the real history and the point of divergence>

## <Section 1 heading>

<~100–130 words>

… exactly eight sections in all …

## Synopsis

<one paragraph on how the timeline unfolds>
```

### `scene-prompts.md`

The illustration plan: one 16:9 scene per section, written so all eight plus the cover read as one
illustrated piece.

```markdown
# Scene prompts — <Title>

**Shared style:** <one sentence: this timeline's named 3–4 colour palette plus one art-direction clause>

## 1. <Section 1 heading>

<40–80 words: one concrete scene — setting, subjects, composition, light, one clause of mood>

… one per section …
```

Rules for every image prompt, cover included (`image-prompt-craft` applies; these win):

- **The shared style is written once** and repeated verbatim at the end of each scene prompt and the
  cover prompt. Pick colours the timeline earns — a nuclear-winter branch and a jet-age boom branch
  should not look alike.
- **Anchor recurring people and objects** with the identical physical description every time they
  appear. There is no memory between image calls.
- **Never name or describe a real living or recent public figure.** The engines refuse their
  likenesses, and the trigger is the description, not the name. Compose around the moment: the
  room, the crowd, a figure at a distance. Long-dead historical figures are fine when respectful.
- **Atmosphere over violence**: consequence, weather, architecture, faces in the aftermath — never
  the act, a body or a wound.
- Vary the framing across the set: an establishing shot, an interior, a face, an object.
- Cinematic historical concept-art illustration, painterly realism, filmic grade. End each prompt
  with the skill's constraint block, verbatim.

--------------------------------------------------
## COVER IMAGE

`cover_prompt` is one symbolic, striking portrait-orientation scene for the whole timeline,
following the same rules and ending with the shared style and the constraint block. The runner
renders it at 2:3 — don't put the ratio in the prompt.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the premise, one sentence>",
  "era": "<era label>",
  "divergence_point": "<as in the frontmatter>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
