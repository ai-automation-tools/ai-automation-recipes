# Song

Goal: write **one completely original `{{SONG_TYPE}}` song** as defined by the CREATIVE BRIEF below:
the lyrics, and the ElevenLabs composition plan that will sing them. The runner renders the plan to
an MP3 and the cover to a square image after you finish.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

> **How this prompt is built.** Everything that makes the song *this type* lives in the CREATIVE
> BRIEF. Where a step says "the brief's **Sound & render**" (or **Cover**, **Frontmatter**,
> **Album**), read that heading in the brief. The brief wins on every creative choice; this
> workflow wins on every mechanical one. Where the brief mentions RECENT SONGS, it means the list
> below.

--------------------------------------------------
## THIS RUN

**Song type: `{{SONG_TYPE}}`**

{{DIRECTION}}

**RECENT SONGS of this type** (newest first) — don't repeat a title, premise, stance, key or tempo
from the last 4:

{{RECENT}}

**Every song already written** (date · slug · title — logline), any type:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Write the song** following the CREATIVE BRIEF. Unless the brief tells you to research (only
   the weekly news type does), this is a *purely original* synthesis: do **not** research, and do
   **not** copy or closely imitate any existing song, artist, lyric, melody, chord progression or
   vocal phrasing. Pick this run's stance / premise from the brief's menus, rotating against
   RECENT SONGS, and an original title.
2. **Build the composition plan** in `composition-plan.json` — the exact JSON the renderer sings:

   ```json
   {
     "chunks": [
       {
         "text": "[Verse 1]\nthe sung lines for this section",
         "duration_ms": 20000,
         "positive_styles": ["genre", "mood", "tempo e.g. 92 BPM", "key", "vocal", "instruments"],
         "negative_styles": ["muddy mix", "off-key vocals", "robotic vocals", "low fidelity"],
         "context_adherence": "high"
       }
     ]
   }
   ```

   - One chunk per section, in order. `text` starts with the `[Section]` label and carries **your
     written lyrics for that section** — the lyrics file must match the plan exactly. Instrumental
     sections have just the label (e.g. `"[Drift]"`).
   - `positive_styles` come from the brief's **Sound & render**: genre, the chosen stance's mood,
     tempo and arrangement, the key, the vocal the brief asks for, the instrumentation. Put the
     full palette on the first chunk; later chunks add what changes (energy, a new instrument).
   - **Curate `negative_styles` toward this record, not a generic one.** Every chunk carries the
     four quality guards above plus the brief's genre and stance exclusions. The negatives are
     where most of the render quality is won or lost.
   - **Instrumental-leaning genres** (the brief says so): keep long instrumental chunks with no
     lyrics, and let the brief's word cap govern; never pad lyrics into a drop or a solo.
   - **Length.** The chunk `duration_ms` values must sum to within 10% of the brief's target
     length (usually 180000 ms; some briefs say otherwise). The runner rejects a plan outside that
     band — a short plan renders a short song.
3. 🔴 **Word-count gate.** Count the words in your finished lyrics, excluding the frontmatter, the
   `#` title, the `>` logline, section headers, `[instrumental]` markers and parenthesised ad-libs.
   The cap is the one in the brief's **Skill rows** (180–260 words unless the brief says
   otherwise). Over cap → **cut a whole section or whole lines, then recount.** Never shorten every
   line instead; that destroys the syllable parallelism between verses. The runner recounts and
   rejects a song over the cap you report, so count honestly. (Every song type has landed 25–97%
   over its cap on early runs. Counting is the only thing that catches it.)
4. **Write `song.md`** using the OUTPUT FORMAT below.
5. **Load `image-prompt-craft`** and write the cover description (the brief's **Cover**) into the
   final JSON's `cover_prompt`. Square; the runner renders it at 1:1 — don't put the ratio in the
   prompt. No text, no logos, no real people's likenesses. End with the skill's constraint block.

--------------------------------------------------
## CREATIVE BRIEF

{{BRIEF}}

{{COMEDY_RULES}}

### Write the lyrics with craft — load the skills

*(If the brief above has its own **Write the lyrics with craft** section, it replaces this one.)*

**Load `songwriting-craft`, `llm-writing`, and `humanizer` before you write a single line, and run
`humanizer`'s final pass over the lyrics before you save them.** `songwriting-craft` is binding on
how the words behave as *sung* lyrics — rhyme scheme, section line caps, syllable budgeting against
each chunk's `duration_ms`, and pronunciation fixes. Read the relevant `references/` file rather
than working from memory. Use the brief's **Skill rows** table, not the skill's defaults.

**Two passes that apply regardless of genre:**

- **Write the chorus first.** Draft it before a single verse, then build the verses to set it up.
- **Run the pronunciation scan before saving.** Take `references/pronunciation.md` over the
  finished lyrics. **Any digit in sung text is a defect** (write *nineteen ninety-nine*, not
  *1999*) — the runner rejects a plan with a digit in a sung line — and so are ambiguous
  initialisms, dialect spellings the model will read literally, and words whose stress flips when
  sung.

Carve-outs, because these skills were written for interactive prose editing:

- **The CREATIVE BRIEF wins.** Where `songwriting-craft` and the brief disagree, the brief is the
  song and the skill is the technique.
- **Lyrics are a protected register.** `humanizer` and `llm-writing` apply to imagery and phrasing,
  not structure. Deliberate repetition, fragments, inverted syntax and rhyme-driven word order are
  craft here, not AI tells.
- **The chorus repeats verbatim** and contains the title.
- **Never touch the mechanical fields** — the frontmatter keys, `length_sec: pending`, and the
  `## [Section]` header form.
- **Ignore the skills' own workflow and reporting instructions** — no audit, no questions.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `song.md`

```markdown
---
title: "<Song Title>"
date: {{DATE}}
song_type: {{SONG_TYPE}}
genre: <the genre line from the brief's Frontmatter section>
mood: <one or two words>
theme: <short phrase: the premise — no dates in it>
tempo_bpm: <tempo>
key: <musical key>
length_sec: pending
engine: ElevenLabs Music
---

# <Song Title>

> <one-line logline: what this song is about (for a comedy song, the joke in one sentence)>

## [Intro]
<lyrics, or nothing for an instrumental section>

## [Verse 1]
<lyrics…>

## [Chorus]
<lyrics…>
```

If the brief gives a full frontmatter template, use it instead (keep `length_sec: pending`). Add
the brief's extra fields (e.g. `stance:`, `era:`). Use the same section names, in the same order,
as the plan's chunks.

--------------------------------------------------
## REQUIREMENTS

- 100% original lyrics — do not reproduce copyrighted lyrics, melodies or phrasing from any artist.
- **No real living people named or defamed** (also a hard ElevenLabs input ban).
- No minors in any sexual or suggestive context, ever.
- Exact dates, not relative ones.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Song Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the logline>",
  "song_type": "{{SONG_TYPE}}",
  "genre": "<genre line>",
  "stance": "<the chosen stance / era / premise, as the brief names it>",
  "mood": "<mood>",
  "key": "<key>",
  "tempo_bpm": 0,
  "target_ms": 180000,
  "word_cap": 260,
  "cover_prompt": "<the full square cover description>",
  "error": null
}
```

`target_ms` is the brief's target length; `word_cap` is the top of the brief's word range (after
any scale-down).
