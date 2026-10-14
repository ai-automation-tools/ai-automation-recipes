## The weekly news song

A catchy, modern track inspired by **this week's current events**. Unlike every other type, this
one researches before it writes.

### Research the week

- Use **WebSearch** (and **WebFetch** to read promising sources) for news in the 7-day window ending
  on the target date. Constrain queries with `after:` / `before:` date qualifiers and discard
  anything outside the window.
- Run a few angled queries: top world and US news, culture and entertainment, tech and AI, sports,
  viral moments. Prefer credible primary sources. Collect 4–8 candidate stories with their URLs.
- **Pick ONE song-worthy angle** — the single story (or a clear blend) that makes the most
  compelling, *catchy* song. Let the dominant story set the **mood**: bright weeks sound upbeat,
  heavy weeks sound reflective. Avoid anything defamatory or hateful, and anything that targets a
  private individual. **Name no real living person in the lyrics** (also a hard ElevenLabs input
  ban) — sing about the event, not the people in it.
- If research turns up nothing in the window, end with `"error"` set — never invent a theme.

### Choose a modern genre

Pick one from this pool that does **not** appear among the last 4 songs of this type under RECENT
SONGS, suited to the week's mood. A close variant is fine if it fits better.

Pop / dance-pop · Hip-hop / rap · Synth-pop / synthwave · Afrobeats · Hyperpop · Drill ·
Indie-pop / bedroom-pop · R&B / alt-R&B · Electro-pop / future-bass · Pop-punk / rock revival ·
Reggaeton / Latin-pop · House / dance · Country-pop / crossover · Trap / cloud-rap ·
Funk / disco revival

### Write the song

A title and structured lyrics with a sticky hook, in clear sections (Intro, Verse 1, Pre-Chorus,
Chorus, Verse 2, Bridge, Outro). Modern, singable, radio-length — about 140–160 seconds of sung
material in a **3:00** render (the rest is instrumental intro, breaks and outro). The chorus hook is
memorable and repeats.

### Sound & render

- The plan's styles name the genre, mood, tempo feel, vocal style, instrumentation, and the song's
  theme. Target length: **180000 ms** (3 min).
- **Curate `negative_styles` toward the genre you picked**, not a generic song. Alongside the
  quality guards, exclude the adjacent genres the model drifts toward if you don't name them (a
  synth-pop pick excludes "rock band", "acoustic guitar", "organic drums"; an Afrobeats pick
  excludes "EDM drop", "trap hi-hats"; an indie-pop pick excludes "overproduced", "heavy autotune").

### Write the lyrics with craft — load the skills

**Load `songwriting-craft`, `llm-writing`, and `humanizer` before you write, and run `humanizer`'s
final pass over the lyrics before you save them.** This type picks its genre at runtime, so the
craft parameters are not fixed — look up **that genre's own rows** in the skill:

| Look up | In |
|---|---|
| Rhyme scheme + strictness for the chosen genre | `references/rhyme-and-structure.md` → *Schemes by genre* |
| Section line caps for the chosen genre | `references/rhyme-and-structure.md` → *Section line caps by genre* |
| Lines per verse + BPM fallback | `references/density-and-duration.md` → *Verse length by genre* / *BPM fallback* |
| Word budget | `references/density-and-duration.md` → the **3:00** row — **180–260 words** sung, **300–420** for a hip-hop/rap pick |

If the chosen genre is slow (under 80 BPM) or deliberately sparse, apply the skill's **slow-tempo
override** and write well under the budget.

Because the news sets the subject, two rows matter more here than for other types:

- **Pronunciation.** News lyrics carry proper nouns, place names, acronyms and years — exactly what
  a music model mangles. Run the scan in `references/pronunciation.md`. **Any digit in sung text is
  a defect**: write *twenty twenty-six*, not *2026*.
- **Topic density.** At most 1–2 topics per 4-line verse, and no more than three proper nouns
  introduced in one verse. A verse that reads like a list of names is a bulletin, not a song.

**Write the chorus hook first**, then build the verses to set it up.

Carve-outs, because these skills were written for interactive prose editing:

- **This brief wins.** The story, mood, genre and no-repeat rule are set before craft enters.
- **Lyrics are a protected register.** `humanizer` and `llm-writing` apply to imagery and phrasing,
  not structure. Deliberate repetition, fragments and rhyme-driven word order are craft here. The
  hook repeats verbatim.
- **Keep it tasteful.** The rule against anything defamatory, hateful, or targeting a private
  individual outranks any craft advice about specificity.
- **Ignore the skills' own workflow and reporting instructions** — no audit, no questions.

### Cover

A square album cover that captures the week's theme and the genre's mood — symbolic, not a news
photo. No real people's likenesses, no text, no logos.

### Frontmatter

Use this frontmatter template for this type (it replaces the generic one):

```markdown
---
title: "<Song Title>"
date: <YYYY-MM-DD>
song_type: weekly
genre: <chosen modern genre>
mood: <one or two words>
theme: <short phrase describing the current-events theme — no dates in it>
event_date: <YYYY-MM-DD of the news event; omit the line if there isn't one>
key: <musical key>
tempo_bpm: <tempo>
length_sec: pending
engine: ElevenLabs Music
sources:
  - "<source URL 1>"
  - "<source URL 2>"
---
```

### Album

`Weekly News Songs`
