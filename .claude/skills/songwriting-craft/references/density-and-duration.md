# Density & Duration

How many words the song gets, how many syllables each chunk gets, and what happens when you overrun.

---

## Why this matters

A generative music model is handed a fixed amount of musical time. Overrun it and you get:

- **Vocal rushing** — words crammed into fixed musical time
- **Loss of clarity** — syllables blur together
- **Section compression** — the music shortens to fit the words
- **Dropped lines** — the model silently skips content

None of these are visible until the render is paid for.

---

## Whole-song word budget

The jobs in this repo request a specific `music_length_ms`. Use the matching row.

| Target duration | `music_length_ms` | Sung genres | Rap / dense flow |
|---|---|---|---|
| 2:00–2:30 | 120000–150000 | 120–180 words | 200–300 |
| 2:30–3:00 | 150000–180000 | 150–220 | 250–350 |
| **3:00** ← most jobs here | **180000** | **180–260** | **300–420** |
| 3:00–3:30 | 180000–210000 | 200–280 | 320–450 |
| 3:30–5:00 | 210000–300000 | 220–400 | 400–600 |
| **4:00** ← psychedelic | **240000** | **260–340** *(far less if slow — see below)* | 450–600 |
| 5:00–7:00 | 300000–420000 | 350–500 | 550–750 |

Subtract roughly **30 words per instrumental break** when estimating — that runtime costs no syllables.

**Slow tempo overrides duration.** A 4:00 track at 60 BPM does *not* want 300 words. Psychedelic,
doom, ambient, and ballad material at sub-80 BPM should land near the **bottom** of its range or
below — often 120–200 words for a four-minute track, with the remaining time carried by instrumental
space and repetition. Long and sparse is a legitimate shape; long and crammed is not.

### Limits

- Over budget → **cut a section**, don't shorten every line. Shortening lines destroys the syllable
  parallelism between verses.
- Under 60% of the low end → likely too sparse unless the genre is deliberately minimal. Add a verse,
  a pre-chorus, or an instrumental break.
- Count words after drafting. Estimating during drafting doesn't work.

---

## Per-chunk syllable budget

**This is the rule that actually governs a render.** The whole-song word count is a planning
estimate; the composition plan's `chunks` are the real constraint, because each carries its own
`duration_ms`.

Approximate sustainable delivery rates:

| Delivery | Syllables / second |
|---|---|
| Slow sung / ballad / doom (< 80 BPM) | 1.5–2.5 |
| Mid-tempo sung (80–120 BPM) | 2.5–3.5 |
| Driving / uptempo sung (120–150 BPM) | 3.5–4.5 |
| Rap, conversational | 4–6 |
| Rap, double-time | 7–9 |
| Ambient / psychedelic (texture vocals) | 0.5–1.5 |

**Budget = `duration_ms` ÷ 1000 × rate.**

Worked example: a 20-second chunk at a mid-tempo sung rate of 3 syl/sec ≈ **60 syllables** ≈ 6–7
lines of 9 syllables. An 8-line verse of 12-syllable lines is 96 syllables — 60% over. That chunk
will rush.

> ⚠️ These rates are engineering estimates for planning, not measured ElevenLabs behaviour. Treat
> them as a first pass and calibrate against real renders: if a track comes back rushed at a budget
> that looked fine, lower the rate for that genre. If it comes back sparse and draggy, raise it.

When a chunk is over budget, in order of preference:
1. Cut lines from that chunk.
2. Split the section across two chunks.
3. Move a line to an adjacent, under-budget chunk.
4. Last resort — shorten lines, accepting that verse parallelism suffers.

---

## Verse length by genre

| Genre family | Default lines/verse | Max safe | Topics/verse | Key rule |
|---|---|---|---|---|
| **Hip-Hop / Rap** | 8 (4 couplets) | 8 | 2–3 | Never exceed 8; half-time trap → treat as 65–75 BPM |
| **Pop** | 4 | 6–8 | 1–2 | Chorus-first; long verses bury the hook |
| **Rock** | 6 | 8 | 2 | 120 BPM sweet spot; riffs need space |
| **Punk** | 4 | 4 | 1 | Every word punches |
| **Hardcore Punk** | 2–3 | 3 | 1 | Shouted, minimal |
| **Metal** | 6–8 | 10 | 2–3 | Vocal delivery compresses syllables; thrash handles most |
| **Doom Metal** | 4 | 6 | 1 | Each word carries weight |
| **Country / Folk** | 6 | 8 | 1–2 | Storytelling pace; ballads drop to 4 |
| **Comedy Country** | 6 | 8 | 1–2 | Setup/payoff needs room to land the joke |
| **Blues** | 3 (AAB) | 3 | 1 | Never break AAB |
| **Electronic / EDM** | 2–4 | 4 | 1 | Production is the star |
| **Psychedelic / Ambient / Shoegaze** | 0–2 | 4 | 1 | Vocals are texture; repetition is content |
| **R&B / Soul** | 6 | 8 | 1–2 | Melisma stretches syllables; groove > density |
| **Jazz** | 6–8 | 8 | 1–2 | Bebop 2–4; ballads 6–8 |
| **Singer-Songwriter** | 6–8 | 8 | 2–3 | Stripped production carries the words |
| **Progressive Rock** | 8–10 | 12 | 3–4 | The exception — handles long verses |

## BPM fallback

When the genre table doesn't settle it, tempo does:

| BPM | Max lines/verse | Topics/verse | Feel |
|---|---|---|---|
| < 80 | 4 | 1–2 | Slow, heavy — fewer lines needed |
| 80–94 | 4–6 | 1–2 | Laid back, mid-tempo |
| 94–110 | 6 | 2–3 | Energetic, driving |
| 110–140 | 6–8 | 2–3 | Standard rock/pop range |
| 140+ | 4 | 1 | Fast — energy over density |

**Default to 4 lines per verse** unless genre and tempo justify more.

## Topic density

- Max **1–2 topics per 4-line verse**, **2–3 per 6–8 line verse**.
- A verse covering 3+ topics in 4 lines should be split.
- **Prefer more short verses over fewer dense ones.**

## Red flags

- An 8-line verse at any BPM under 100
- A verse that reads like a list of names and facts — that's an encyclopedia entry, not a verse
- The brief says "laid back" but the verses are wall-to-wall syllables
- More than three proper nouns introduced in one verse
- Every verse dense, with no breathing room anywhere in the song

## The fix

1. **Prefer adding a verse over cutting content** — spread, don't compress.
2. Give each topic at least a full couplet to land.
3. Re-read at tempo. Can you actually sing or rap this without rushing? If you can't, neither can the model.
