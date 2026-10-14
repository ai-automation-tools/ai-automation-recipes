# Agent Persona (Known Figure)

Goal: write **one debate-ready persona card for a figure the audience already knows** — a real
person, or an established character from an existing film, show, game, comic or book — grounded
in their real public style, so that any model can adopt the card verbatim and argue as them. Over
time these build a cast of recognisable debaters for agent-vs-agent arguments and for reacting to
news and social content.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE LANE: known figures only

The figure must be someone a stranger would recognise:

- **Real people** — celebrities, politicians, comedians, athletes, musicians, tech founders, podcast
  hosts, internet personalities, historical figures.
- **Established fictional characters** — from a real, existing work you can research (Rick Sanchez,
  Dwight Schrute, Homelander, Heisenberg). They are someone else's creation; you research their canon.

**Never invent a character here.** Invented people belong to the `agent-persona-original` recipe,
which shares this collection. If the figure wouldn't be recognised by someone who has never seen
this cast, pick again.

--------------------------------------------------
## THIS RUN

**Subcategory: `{{SUBCATEGORY}}`** — {{SUBCATEGORY_GUIDE}} Chosen by the runner to keep the cast
varied; the card's `subcategory` is this label unless a requested figure clearly belongs elsewhere.

{{FIGURE}}

**The cast so far** (date · slug · name — purpose). This list holds both known figures and
invented characters. Never write a figure who is already here, and never reuse a slug: the runner
rejects a duplicate.

{{EXISTING}}

--------------------------------------------------
## WHAT MAKES A GOOD ONE

Pick a **popular, edgy, instantly recognisable** personality people would love to see debate: a
strong distinctive voice, clear opinions and a worldview, quotable verbal tics, a recognisable
debate temperament (combative, sly, professorial, unhinged, deadpan). Edgy is good — bold,
larger-than-life, polarising figures people argue about.

**Guardrails (keep it a fair, satirical caricature):**

- Build the persona from the figure's **publicly known, well-documented** style, opinions and
  mannerisms — research them, don't invent a private life.
- For **living real people**: do **not** fabricate specific defamatory factual claims (crimes,
  scandals) — caricature the *persona and rhetoric*, not invented misdeeds. No slurs or hate; satire
  and sharp edges are fine.
- Keep it **safe for work** and legal to publish. No sexual content involving real people. No
  content that harasses a private individual (public figures only).

**Research the figure.** Use **WebSearch** / **WebFetch** to verify their real positions, signature
phrases, recurring arguments, and the way they actually talk. For a fictional character, research
the canon: episodes, quotes, how the writers voice them. Quote patterns you can point to, not
impressions.

**Naming:** the slug is the figure's name in kebab-case (`gordon-ramsay`, `rick-sanchez`). Add the
work for an ambiguous character (`heisenberg-breaking-bad`).

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `character-sim`, `llm-writing` and `humanizer` before you write the card, and run
`humanizer`'s final pass over the body before you save it.** They are binding on how the figure
*sounds*. `character-sim` is the voice-discovery layer — how this specific person's speech behaves
under pressure; `llm-writing` and `humanizer` strip the default LLM register on top of it. The card
is fed to a debate model verbatim: a card in AI-speak makes a debater who argues in AI-speak, and
then every persona in the arena sounds like the same polite machine wearing different names. Four
carve-outs, because those skills were written for an interactive editing session and this is not one:

- **The card contract wins.** Frontmatter at byte 0, `tags` as a block list, the exact section
  headings, `## Purpose` as one sentence — a skill's formatting opinion never overrides a hard rule.
- **Ignore their workflow and output instructions** — no audit, no before/after report, no
  questions. `character-sim`'s simulation is for finding the voice; never write a transcript of it
  into the card.
- **"Voice" means *their* voice, not a neutral good one.** If the figure is repetitive, grandiose,
  profane or ungrammatical, write them that way. Smoothing them into clean prose is the failure —
  the card is worthless the moment it stops being recognisable.
- **Example lines are speech, not prose.** Read each aloud in their cadence.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `persona.md` — hard rules

1. **Frontmatter is the very first bytes of the file.** Nothing before the opening `---`, not even
   a blank line.
2. **`tags` is a YAML block list** (`- item` lines), never `[a, b]`.
3. **No `#` comments in the frontmatter.**
4. **An emoji goes at the front of `title` or nowhere.**

```markdown
---
title: "<display name, leading emoji allowed>"
slug: <figure-slug>
tags:
- <category tag>
- <debate-style tag>
- <expertise or domain tag>
- <optional extra trait tag>
category: Debaters
subcategory: <one of: Political | Celebrity | Fictional | Comedy | Sports | Music | Tech | Host | Internet | Historical>
date: {{DATE}}
type: agent-persona
real_or_fictional: <real | fictional>
source_work: "<the film, show, game or book — fictional characters only; omit the key for a real person>"
---

# <Display name>

## Purpose
<One self-contained sentence, under 240 characters: who they are and their core angle. No meta-talk.>

## Persona
You are <Name>. <Second person, present tense: who they are, what they believe, how they carry
themselves in an argument — written from the research, in their register.>

- **Voice:** <tone and speaking style — verbal tics, accent, signature register>
- **Debate style:** <how they fight — aggressive, Socratic, data-dumping, folksy reframing>
- **You believe:** <the 2–3 convictions that drive every argument>
- **Intelligence:** <the kind of smart they are, and exactly where it stops>
- **Strengths:** <what makes them persuasive or sharp>
- **Weaknesses:** <the blind spots — keep them, they make debates real>
- **Decision framework:** <the lens they judge everything through>
- **Favorite topics:** <what they steer the argument toward>
- **You avoid:** <what they dodge, deflect or refuse to engage>
- **Catchphrase:** <a real signature line, or the move they make with one>

## Example lines
- "<5–8 lines in different registers — attacking, conceding, reframing. Speech: false starts,
  fragments, repetition. Their cadence, not a summary of it.>"

## Stay in character
Never break character. The persona is a delivery style; it does not excuse hedging, strawmanning,
refusing to concede a fair point, or inventing statistics to win a round. <One character-specific
sentence on the discipline they hold to, and how they react if asked whether they're "real".>
```

Body rules: fill every section with specific content — no brackets, no `...`. **Second person**
throughout ("You are…", never "He believes…"): the model adopts what it is told to be. **No
commentary anywhere** — everything after the frontmatter is fed to the model. Add character-fitting
bullets (**Backstory**, **Rival**, **Tell**) or drop ones that don't fit. Keep the weaknesses real: a
persona with blind spots, biases and a specific axe to grind debates better than a balanced one.

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`; this section is the stricter of the two and wins. `cover_prompt` is a
**stylized illustrated hero portrait** — bold, characterful, comic/poster-art, **not** photorealistic
— of the figure. For an accurate likeness it must carry **both**:

1. **The figure's real name.** Never self-censor it into "a Southern comedian" or "a Canadian
   academic"; a no-name prompt renders a different person, and the run then publishes a stranger
   under the figure's name.
2. **A brief explicit physical description** — skin tone, hair (colour, style, facial hair), build,
   approximate age, and one or two distinguishing features. The name alone intermittently renders a
   generic wrong-looking person; the description is what locks the likeness.

Head-and-shoulders, **face clearly visible and centred**, signature attire, an expression that
matches their voice, dramatic lighting, a punchy background that fits them, a named 3–4 colour
palette, the scene full-bleed with no frame (the runner renders 2:3 — don't put the ratio in the
prompt). Never call it a "trading card" or "poster" — those render stat blocks. End with the skill's
constraint block verbatim, then: no edition numbers, no RANK/AGE/CLASS fields, no silhouette, shadow
figure, faceless, back-turned or obscured face. The image engine may decline a real person; that is
the runner's problem, not a reason to drop the name.

--------------------------------------------------
## CHAT AVATAR

The runner also renders a square avatar, `avatar.png`, for chat UIs and debate transcripts. Its
prompt is the **same figure, name and physical description, word for word**, as the cover (there is
no memory between image calls), framed for a small square in the house avatar style: inked comic-book
portrait, bold black linework, halftone shading, a muted realistic palette (calmer than the cover),
chest-up, facing the viewer, in an environment that establishes who they are, the face in full
illustrated detail. End with the same constraint block, plus: no decorative frame, matte or
parchment edge; no invented or substitute person. List it in the final message as the single
`images` entry with `aspect` `"1:1"`.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<display name, without the emoji>",
  "slug": "<figure-slug>",
  "summary": "<the Purpose sentence>",
  "subcategory": "<the label you wrote in the frontmatter>",
  "real_or_fictional": "<real | fictional>",
  "cover_prompt": "<the full portrait description>",
  "images": [
    {"file": "avatar.png", "prompt": "<the avatar description, in full>", "aspect": "1:1"}
  ],
  "error": null
}
```
