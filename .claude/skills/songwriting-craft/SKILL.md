---
name: songwriting-craft
version: 1.0.0
description: >-
  Lyric craft for AI-generated songs — rhyme technique, section structure,
  line/syllable budgeting, and pronunciation control for text that will be SUNG
  by a generative music model (ElevenLabs Music `compose_music`), not read.
  Covers rhyme types and per-genre schemes, section length limits, fitting
  lyrics to a composition plan's fixed `duration_ms` chunks so the vocal isn't
  rushed or clipped, homograph/number/acronym phonetic fixes, and a three-pass
  refinement schedule (tighten → strengthen → flow). Use whenever writing,
  revising, or reviewing song lyrics, building or editing an ElevenLabs
  composition plan, or when a rendered track came back with rushed, garbled,
  mispronounced, or dropped words.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Songwriting Craft

Lyrics that read well on the page routinely fall apart when a model sings them. This skill is about
the difference.

> **The core constraint.** A generative music model gets a fixed amount of musical time and must fit
> your words into it. Give it too many syllables and it rushes, slurs, compresses the section, or
> silently drops lines. Give it ambiguous spelling and it picks the wrong pronunciation with total
> confidence. Neither failure shows up until after you've spent the render.

## When to load which reference

| Need | Reference |
|---|---|
| Rhyme types, per-genre schemes, section length caps | [`references/rhyme-and-structure.md`](references/rhyme-and-structure.md) |
| Word counts, syllable budgets, fitting a composition plan's chunks | [`references/density-and-duration.md`](references/density-and-duration.md) |
| Homographs, numbers, acronyms, proper nouns | [`references/pronunciation.md`](references/pronunciation.md) |
| Revising an existing draft | [`references/refinement-passes.md`](references/refinement-passes.md) |

---

## Workflow

1. **Know your budget before you write.** Target duration and BPM come from the job's brief. Convert
   them to a word count and a per-section line cap — see `density-and-duration.md`. Writing first and
   trimming later wastes the best lines.
2. **Pick the rhyme scheme from the genre**, not from habit. There is no universal default; an ABCB
   ballad stanza in a rap track is as wrong as hip-hop couplets in a folk song. See
   `rhyme-and-structure.md`.
3. **Draft to the structure**, respecting per-section line caps.
4. **Run the three refinement passes** — tighten, strengthen, flow. See `refinement-passes.md`.
5. **Scan for pronunciation risk** and apply phonetic respellings. See `pronunciation.md`.
6. **Run the pre-flight checklist** below.
7. **Fit the lyrics to the composition plan.** See the section after the checklist — this is the step
   with no equivalent in ordinary songwriting, and the one that most often ruins a render.

---

## Hard rules

**MUST**
- Match the rhyme scheme and strictness to the genre.
- Keep every section within its genre line cap — count lines after drafting and trim before
  presenting. Don't ask permission to cut; cut.
- Keep corresponding lines within ±2 syllables (±3 for rap). Verse 1's shape must fit Verse 2's melody.
- Repeat the chorus **verbatim**. It's the hook; rewriting it each time destroys recall.
- Put the song title in the chorus unless the brief says otherwise.
- Reach a longer duration by **adding sections, not lengthening them** — a third verse, a pre-chorus,
  an instrumental break.
- Read every line aloud before finalizing. If you stumble, the singer will.

**MUST NOT**
- Force a rhyme by bending grammar, inventing a word, or padding with filler.
- Rhyme a word with itself, or with a near-identical word (mind/mind, time/time).
- Write a wall-of-text verse. Two 4-line verses beat one 8-line verse.
- Introduce more than three proper nouns in a single verse.
- Use clichés straight: *cold as ice, broke my heart, by my side, set me free, learning to fly*, or
  *tonight* as an end-rhyme. Reinvent or cut.
- Tell an emotion the imagery could show. "She was angry" → "Her knuckles white around the glass."
- Switch rhyme scheme mid-section.

---

## Pre-flight checklist

Run all nine before the lyrics are final. Every one of these is cheaper than a re-render.

1. Do the rhyming pairs actually rhyme when read aloud, at the genre's strictness?
2. Any orphan line that sets up a rhyme and never lands it?
3. Corresponding lines within the syllable tolerance?
4. Any filler phrases padding a line to length?
5. Does the rhyme scheme match the genre?
6. Every section within its line cap?
7. Read as plain prose — does it sound natural for this genre's vocal style?
8. Any tongue-twisters, stacked diphthongs, or missing breath points?
9. Every homograph, number, acronym, and unusual proper noun resolved to one pronunciation?

---

## Fitting lyrics to an ElevenLabs composition plan

The jobs in this repo call `create_composition_plan` (free) and then `compose_music` (**paid — once**).
The plan comes back as a `chunks` array; each chunk has `text`, `duration_ms`, `positive_styles`, and
`negative_styles`.

**`duration_ms` is the budget, and it is per chunk.** A whole-song word count is a starting estimate;
the chunk is where the vocal actually rushes. A 20-second chunk holding a 12-line verse will be
rushed no matter how good the song's total word count looks.

Working rules:

- **Your lyrics lead.** Rewrite each chunk's `text` to carry the section you wrote. Light trims to fit
  a chunk are fine; a wholesale rewrite by the planner is not — that's the planner writing the song.
- **Budget each chunk by syllables, not words.** See the syllable-rate table in
  `density-and-duration.md`. If a chunk is over budget, cut lines from that chunk — or ask the plan
  for another chunk and split the section across two.
- **Instrumental chunks are free runtime.** A chunk with no sung text and instrumental
  `positive_styles` buys 20–40 seconds without costing a single syllable. This is the cheapest way to
  hit a duration target.
- **Curate `negative_styles` on every chunk.** Always include the quality guards — *muddy mix,
  off-key vocals, robotic vocals, low fidelity* — alongside any genre exclusions.
- **The saved lyrics file must match the final edited plan.** If you trimmed a line to fit a chunk,
  trim it in the markdown too. A lyrics file that doesn't match the audio is a bug.
- **Plan editing is free; rendering is not.** Do all the fitting before `compose_music`. Get it wrong
  and the fix costs another paid render — or an inpainting pass if `store_for_inpainting` was set.

---

## Scope

This skill owns **craft** — how the words work as sung lyrics. It does **not** own:

- **The creative brief.** Genre, era, artists, mood, emotional theme, and the commercial goal come
  from the job's own prompt. This skill never overrides a brief; where they conflict, the brief wins.
- **Originality and provenance rules.** The job prompt owns those.
- **Prose quality generally** — for that, pair with `llm-writing` and `humanizer`. Note that lyrics
  are a **protected register**: a sung line legitimately breaks rules that prose can't. Deliberate
  repetition, fragments, inverted syntax, and a rhyme-driven word order are craft here, not tells.
  Run the anti-AI pass on the *imagery and phrasing*, never on the structure.
