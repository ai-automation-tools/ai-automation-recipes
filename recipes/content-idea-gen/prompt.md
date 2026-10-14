# Content Idea

Goal: research what's working on social platforms right now and produce ONE complete,
trend-grounded social-media content idea that could run as a recurring, automatable series — plus
the description of a cover image.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Topic area: `{{TOPIC}}`** — chosen by the runner to keep the backlog varied.

**Ideas already in the backlog** (date · slug · title — pitch). Pick a clearly different concept:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Trend research.** Use **WebSearch** (and **WebFetch** for promising pages) to see what is
   working in the topic area in the last 30 days across TikTok, YouTube Shorts, Instagram, Reddit,
   X and LinkedIn: trending themes, high-performing formats, recurring hooks and storytelling
   patterns. Prefer reporting and platform data over listicles.
2. **Choose one idea** that rides a real current pattern and could become a recurring series an
   automation produces week after week. One sharp idea, not a list.
3. **Load the writing skills**, then write `idea.md` in the format below.
4. **Load `image-prompt-craft`** and write `cover_prompt`.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before writing `idea.md`, and run `humanizer`'s final pass
before you save it.** Skip their audit, report and question steps. The format below wins on
structure. Marketing-speak is the failure mode here: write it like a producer pitching a series to
a sceptical editor. Any engagement claim either cites a source or is stated as your judgment.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `idea.md`

```markdown
---
title: <catchy series name>
date: {{DATE}}
topic: {{TOPIC}}
platforms: [<platform>, <platform>]
formats: [<short video | carousel | thread | audio | post>]
cadence: <e.g. 3x weekly>
---

# <Title>

> <the hook in one line — what stops the scroll>

## Target audience

<who, and what they're already watching>

## The trend it rides

<the pattern, with the evidence from your research>

## Format & treatment

- **Opening hook:** <first 2 seconds / first line>
- **Key talking points:** <3–5 bullets>
- **CTA:** <what the viewer does next>

## Automation potential

<inputs, the generation steps, what a human still reviews, and how the series stays fresh>

## Repurposing

- <one bullet per platform or format>

## Keywords & hashtags

<comma-separated>

## Sources

- <URL> — <what it shows>
```

At least two working source URLs. Never invent sources, statistics or view counts.

--------------------------------------------------
## COVER IMAGE

`cover_prompt` is a modern, attention-grabbing, social-media-friendly illustration of the idea:
one subject, one clear visual gag or metaphor, a named 3–4 colour palette, full-bleed with no inset
panel or frame (the runner renders 16:9 — don't put the ratio in the prompt). Never name an object
that carries text — a phone screen, a feed, a thumbnail, a dashboard — or it renders garbled
lettering. No logos or real brands, no recognisable people. End with the skill's constraint block,
verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<series name>",
  "slug": "<kebab-case-slug>",
  "summary": "<the hook>",
  "topic": "{{TOPIC}}",
  "platforms": ["<platform>"],
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
