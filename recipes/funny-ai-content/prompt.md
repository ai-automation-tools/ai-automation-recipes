# Funny AI Content

Goal: one content concept about a funny, weird, off-putting or questionably useful AI / AI-agent use
case — the kind of thing that becomes a TikTok, a Short, a Reel, an X thread or a LinkedIn parody
post — plus the description of a cover image.

Tone reference (not a concept to repeat): *"using AI to automate your divorce."*

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Premise family: {{FAMILY}}** — {{FAMILY_GUIDE}} Chosen by the runner so the weeks don't repeat.

**Concepts already done** (date · slug · title — hook). Don't reuse a premise, punchline, setting or
automation target:

{{EXISTING}}

**Tone.** Funny, slightly uncomfortable, internet-native. Absurd enough to entertain, grounded enough
that a viewer can imagine someone actually pitching it. Satire is welcome. No cruelty toward
protected classes, no targeted harassment, no self-harm instructions, no real legal, medical or
financial advice — and the artifact makes clear it's a content concept, not a recommendation. One
sharp idea beats a list of jokes.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write, and run `humanizer`'s final pass on your
draft.** A joke explained in AI-speak isn't a weaker joke — it isn't a joke. Carve-outs:

- **Ignore their workflow and output instructions** — no audit, report or questions.
- **The template below wins on structure.**
- **Keep the deliberate comic devices.** An escalating triad is joke architecture, not padding.
- **Corporate-speak is allowed inside the fake product** — the feature names, the fake CEO quote.
  That's the gag. The writing around it is a person's.

Never explain the joke: analysis belongs in *Why It Works* and nowhere else.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `concept.md`

```markdown
---
title: "<catchy content title>"
date: {{DATE}}
type: funny-ai-content
premise: "<one-sentence premise>"
format: "<primary format>"
platforms: [TikTok, YouTube Shorts, Instagram Reels]
tags: [funny-ai-content, ai-automation, ai-agents, satire]
---

# <Title>

> <one-sentence hook that would stop someone scrolling>

## The Bit

<the core joke in 2–4 short paragraphs>

## Why It Works

- <why it's funny and shareable>
- <the anxiety, behaviour or tech culture it pokes at>
- <why the audience recognises the situation>

## Content Treatment

- **Primary format:** <short vertical video / carousel / skit / mock product demo / thread>
- **Opening shot:** <what the viewer sees first>
- **On-screen hook:** <short text hook>
- **Escalation:** <how it gets worse or stranger>
- **Button:** <final punchline or CTA>

## Sample Script Beats

1. <beat>
2. <beat>
3. <beat>
4. <beat>
5. <beat>

## Automation Angle

<the fake-or-plausible agent workflow: inputs, tools, outputs, and the overly serious product
language that makes it land>

## Repurposing

- <short video>
- <carousel / thread>
- <fake product demo>

## Guardrails

- Satirical concept; not advice.
- Real-world sensitive domains stay framed as parody.
- No private personal data, real names, or instructions that would harm someone.
```

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft` (this section wins where they differ). `cover_prompt` is a polished,
cinematic, surreal-but-clean editorial illustration: a person reacting to an absurd machine.

- **The comedy is about software, and software nouns render as garbled text.** "Dashboard",
  "chat bubble", "notification", "browser window", "spreadsheet" — the model draws the whole
  convention and no "no text" beats it. **Change the noun.** Get the joke from the human and the
  physical absurdity: the expression, an impossible tangle of cables, a machine that has clearly
  won. Glowing abstract panels with no glyphs are fine; a screen "showing" something is not.
- **Name three or four colours** that suit the week's joke.
- **One subject, one gag** — it has to read at thumbnail size.
- No title or lettering, no real logos, no face that reads as a real person. Full-bleed, no frame;
  the runner renders 16:9. End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the hook>",
  "family": "{{FAMILY}}",
  "format": "<primary format>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
