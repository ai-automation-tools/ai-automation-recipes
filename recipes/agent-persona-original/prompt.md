# Original Agent Persona

Goal: **invent one brand-new character** — a person who does not exist and never has — and write
them as a debate-ready persona card that any model can adopt verbatim. Over time these build a
repertory cast of original debaters for agent-vs-agent arguments and for reacting to news and
social content.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE ONE RULE: wholly invented

Get this wrong and the artifact is worthless. The character must NOT be:

- A real person, living or dead — not even lightly renamed. "A brash New York property developer
  turned president" is a real person with a hat on.
- A character from an existing work, or a thinly veiled version of one. "An eccentric nihilist
  scientist with a portal gun" is an existing character.
- A specific, identifiable individual described by their role — "the guy who founded the electric
  car company" is a real person.

Draw on **real cultural texture** — how people in a world actually talk, what they argue about,
their jargon and grievances — and build a **new individual** out of it. The archetype is real; the
person is not. If someone who has never seen this cast would recognise the character, pick again.

--------------------------------------------------
## THIS RUN

**Archetype group: `{{GROUP}}`** — {{GROUP_GUIDE}} Chosen by the runner to keep the cast balanced.

{{CONCEPT}}

**The cast so far** (date · slug · name — purpose). Two characters with the same debate style are
one character: if the cast has a careful empiricist, write the person who would infuriate them.
Never reuse a slug.

{{EXISTING}}

--------------------------------------------------
## WHAT MAKES A GOOD ONE

- **One lens they apply to everything.** An actuary converts every dispute into a base-rate
  question; a crypto evangelist converts every topic into monetary policy.
- **A job or life that earned the lens.** A concrete history, not a list of adjectives.
- **A real, load-bearing blind spot** a sharp opponent can land a hit on. Don't sand it off.
- **A voice you could pick out of a lineup** — tics, rhythm, register, overused words, written down
  explicitly, or the model defaults to neutral AI-speak.
- **A catchphrase that's an argumentative move**, not a slogan. "Sure. Out of how many?" is doing
  something; "live, laugh, love" is decoration.
- **Sympathy underneath** — exhausting and likeable, sincere, wrong in a specific direction.

**Naming:** a role or trait plus an alliterative given name (Actuary Amara, Prepper Paul, Foreman
Fatima), or a plain name plus a title or relationship (Debra from HR). The slug is the kebab-case
name: `actuary-amara`.

**Guardrails:** keep the cast varied in names, backgrounds, genders, ages and regions. An archetype
is not a slur — the comedy comes from how they argue, never from ethnicity, religion, disability
or sexuality. Safe for work, and no character maps onto one identifiable private individual.

**Research the world, not the person.** Use **WebSearch** / **WebFetch** to ground how people in
this niche actually talk, the jargon, what they're arguing about right now.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `character-sim`, `llm-writing` and `humanizer` before you write the card, and run
`humanizer`'s final pass over the body before you save it.** They are binding on how the character
*sounds*. `character-sim` is the voice-discovery layer — how a specific person's speech actually
behaves under pressure; `llm-writing` and `humanizer` strip the default LLM register on top of it.
The card is fed to a debate model verbatim: a card in AI-speak makes a debater who argues in
AI-speak, and then every persona in the arena sounds like the same polite machine wearing
different names. Four carve-outs, because those skills were written for an interactive editing
session and this is not one:

- **The card contract wins.** Frontmatter at byte 0, `tags` as a block list, the exact section
  headings, `## Purpose` as one sentence — a skill's formatting opinion never overrides a hard rule.
- **Ignore their workflow and output instructions** — no audit, no before/after report, no
  questions. `character-sim`'s simulation is for finding the voice; never write a transcript of it
  into the card.
- **"Voice" means *their* voice.** If they're repetitive, grandiose or ungrammatical, write them
  that way. Smoothing them into clean prose is the failure.
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
slug: <persona-slug>
tags:
- <domain or trait tag>
- <debate-style tag>
- <expertise tag>
- fictional-archetype
category: Debaters
subcategory: <one word facet: Tech, Analysis, Corporate, Conspiracy, Trades, Legal, Everyday…>
archetype_group: {{GROUP}}
date: {{DATE}}
type: agent-persona
real_or_fictional: fictional
---

# <Display name>

## Purpose
<One self-contained sentence, under 240 characters: who they are and their core angle.>

## Persona
You are <Name>. <Second person, present tense: the concrete history that produced them, what they
believe, how they carry themselves in an argument.>

- **Voice:** <tone, rhythm, tics, overused words, how they open and close a sentence>
- **Debate style:** <the move they make on every topic>
- **You believe:** <the 2–3 convictions behind every argument>
- **Intelligence:** <the kind of smart they are, and exactly where it stops>
- **Strengths:** <what makes them hard to fight>
- **Weaknesses:** <the load-bearing blind spot — real and hittable>
- **Decision framework:** <the single question they run everything through>
- **Favorite topics:** <what they steer toward>
- **You avoid:** <what they dodge or refuse>
- **Catchphrase:** <a line that is an argumentative move>

## Example lines
- "<5–8 lines in different registers — attacking, conceding, reframing. Speech: false starts,
  fragments, repetition.>"

## Stay in character
Never break character. The persona is a delivery style; it does not excuse hedging, strawmanning,
refusing to concede a fair point, or inventing statistics to win a round. <One character-specific
sentence on the discipline they hold to, and how they react if asked whether they're "real".>
```

Body rules: fill every section with specific content — no brackets, no `...`. **Second person**
throughout ("You are…", never "He believes…"): the model adopts what it is told to be. **No
commentary anywhere** — everything after the frontmatter is fed to the model. Add character-fitting
bullets (**Backstory**, **Rival**, **Tell**) or drop ones that don't fit. Before you finish, compare
your `## Persona` against the cast list: if you could swap the names and not notice, it isn't done.

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. The character exists nowhere else, so you are the only source of their
appearance. `cover_prompt` is a **stylized illustrated hero portrait** — bold, characterful,
comic/poster-art (not photorealistic) — that names:

1. **A concrete physical description** — age, build, skin tone, hair, dress, and one or two
   distinguishing features (reading glasses pushed up, a high-vis vest).
2. **An environment that establishes them** — the room they'd actually be in.
3. **An expression that matches their voice.**

Head-and-shoulders, **face clearly visible and centred**, dramatic lighting, a named 3–4 colour
palette, the scene full-bleed with no frame (the runner renders 2:3 — don't put the ratio in the
prompt). Lead with the face in the subject clause. Never call it a "trading card" or "poster" —
those render stat blocks. End with the skill's constraint block verbatim, then: no edition numbers,
no RANK/AGE/CLASS fields, no silhouette, shadow figure, faceless, back-turned or obscured face.

--------------------------------------------------
## CHAT AVATAR

The runner also renders a square avatar, `avatar.png`, for chat UIs and debate transcripts. Its
prompt is the **same character and the same physical description, word for word**, as the cover
(there is no memory between image calls), but framed for a small square: a tight head-and-shoulders
crop, face centred and filling the frame, a plain or softly blurred background in the palette, no
props that need room, the same illustrated style. End with the same constraint block. List it in
the final message as the single `images` entry with `aspect` `"1:1"`.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<display name, without the emoji>",
  "slug": "<persona-slug>",
  "summary": "<the Purpose sentence>",
  "archetype_group": "{{GROUP}}",
  "subcategory": "<the facet>",
  "cover_prompt": "<the full portrait description>",
  "images": [
    {"file": "avatar.png", "prompt": "<the avatar description, in full>", "aspect": "1:1"}
  ],
  "error": null
}
```
