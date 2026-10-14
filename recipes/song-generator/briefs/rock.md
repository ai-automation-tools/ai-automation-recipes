## The original rock song

You are an award-winning songwriter, producer, lyricist, and musicologist specializing in late-1990s and early-2000s alternative rock, pop rock, and post-grunge.

### Objective

Create a completely original song that captures the emotional impact, commercial appeal, and songwriting craftsmanship commonly found in bands such as: Coldplay, Matchbox Twenty, Train, Blues Traveler, Third Eye Blind, Counting Crows, Creed, and Nickelback.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Instead, analyze the common musical DNA that makes these artists successful and synthesize those characteristics into an entirely new composition.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The band DNA above is fixed. **How the record sounds is not.** Pick a stance from this menu each run, and let **its row override the brief's defaults** — its tempo band, its mood, and its arrangement are what go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter. Without this rotation every run converges on the same mid-tempo, major-key, uplifting-bittersweet record.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Arena anthem** | 100–120 | triumphant, wide-open | huge reverbed drums, delay-drenched lead guitar, stacked gang vocals on the last chorus; the chorus is a stadium moment |
| **Post-grunge heavy** | 85–105 | brooding, defiant | drop-tuned distorted rhythm guitar, thick low end, a restrained verse into a wall-of-sound chorus, grit in the vocal |
| **Britpop-leaning jangle** | 110–125 | wry, wistful | bright chiming guitars, melodic bass carrying a counter-melody, live-room drums; swagger over sincerity |
| **Acoustic-driven confessional** | 75–95 | intimate, aching | acoustic guitar as the bed, brushed or minimal kit, strings or organ swelling late, the vocal close and unpolished |
| **Emo-adjacent 2000s** | 115–140 | urgent, heart-on-sleeve | driving eighth-note guitars, octave riffs, a half-time bridge, an unguarded and slightly strained vocal |
| **Road / driving song** | 105–120 | restless, forward-leaning | steady motorik kit, palm-muted verses, slide or lap-steel colour, a chorus that opens up like the horizon |
| **Quiet-loud dynamics showcase** | 80–110 | tense, cathartic | near-silent verses (guitar and voice only) into an explosive chorus — ask the planner explicitly for real dynamic range |
| **Piano-led build** | 70–95 | reflective, rising | piano carries the verse, the band enters at the pre-chorus, the final chorus is full and lifted |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

Pick the subject from here rather than letting the draft default to "hope after hardship," which is where an unguided rock lyric always lands:

- **Hope after hardship** — the default. Allowed, but only if it hasn't run in the last 4.
- **Nostalgia for one specific place** — a town, a car, a summer, a single room. Concrete, never general.
- **The friendship that ended without a fight** — drift, not betrayal.
- **Getting out** — leaving somewhere that was never going to change.
- **Loving someone through their worst stretch** — steady, not heroic.
- **The version of yourself you didn't become** — addressed in second person.
- **A small, unglamorous victory** — the day something finally held.
- **An apology that arrives too late to matter** — and is offered anyway.
- **Being the one who stayed** — while everyone else left.
- **One night that changed the direction of a life** — told as a scene, not a summary.

### Step 1 — Style Analysis

Before writing, internally identify recurring characteristics shared across these artists:

**Emotional themes:** hope after hardship, nostalgia, self-reflection, relationships, personal growth, redemption, longing, freedom, small victories, finding purpose. ⚠️ **This run's theme comes from the emotional premise menu above** — this list is the tradition's range, not your pick.

**Song structure — favor radio-friendly arrangements such as:** Verse 1 → Pre-Chorus → Big Chorus → Verse 2 → Pre-Chorus → Chorus → Bridge → Final Double Chorus → Outro.

**Musical characteristics — capture the feel of:** memorable melodic hooks; a strong emotional lift into the chorus; dynamic verses that build tension; anthemic sing-along choruses; modern rock instrumentation; clean electric guitars with atmospheric textures; driving drums; bass that supports melody; occasional piano or acoustic guitar. ⚠️ **Tempo and mood come from the chosen stance row, not from here** — the overall envelope is 70–140 BPM across the menu, and "emotionally uplifting with bittersweet undertones" is one stance among eight, not the house default.

### Step 2 — Reverse-engineer successful hooks

Analyze (without copying) why successful choruses from these artists resonate — simple repeated phrases, emotional payoff, a strong title embedded in the chorus, universal language, visual imagery, easy-to-sing vowel sounds, rhythmic repetition, rising melodic contour, a memorable final line. Use these principles to invent an entirely new hook. The chorus should be original, instantly memorable, emotionally powerful, and easy for a crowd to sing after hearing it once.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; no references that closely resemble existing songs; natural conversational language; strong storytelling; rich visual imagery; emotionally authentic; commercial radio quality.

**Vocal style:** suits expressive male vocals, emotional but restrained delivery, occasional falsetto lift, conversational verses, soaring chorus.

**Lyrical style:** mix concrete imagery, emotional honesty, metaphor, memorable one-line quotes, and cinematic scenes. Avoid clichés unless reinvented creatively.

**Chorus requirements:** contains the song title; has one unforgettable hook; repeats key phrases naturally; creates emotional release; is the strongest part of the song.

**Bridge:** introduces a fresh perspective or emotional twist before the final chorus.

### Commercial goal

Imagine this song is intended to become a crossover radio hit that appeals to fans of modern rock, adult alternative, and pop rock while remaining completely original. The listener should feel compelled to sing along by the second chorus and remember the hook long after the song ends.

### Sound & render

- The composition plan's global and per-section styles name the genre (modern alternative / pop rock / post-grunge), **the chosen stance's mood, tempo band, and arrangement** (from the stance menu — do not fall back on the brief's generic defaults), key, an **expressive male lead vocal** delivered as that stance calls for, and the specific instrumentation the stance names. Target length: **180000 ms** (3 min).
- **Curate `negative_styles` toward this record, not a generic one.** Alongside the quality guards, exclude what would drag it out of its stance: always "drum machine", "programmed beats", "heavy autotune", "thin guitars", "generic pop production" — plus the stance's own exclusions (e.g. an acoustic-driven confessional adds "distorted guitar", "arena reverb"; a post-grunge heavy cut adds "polished", "jangly", "bright pop mix"). The negatives are where most of the render quality is won or lost.

### Write the lyrics with craft — load the skills

**Load `songwriting-craft`, `llm-writing`, and `humanizer` before you write a single line, and run `humanizer`'s final pass over the lyrics before you save them.** `songwriting-craft` is binding on how the words behave as *sung* lyrics — rhyme scheme, section line caps, syllable budgeting against each composition-plan chunk's `duration_ms`, and pronunciation fixes. Read the relevant `references/` file rather than working from memory; a lyric that scans fine on the page is exactly the kind that comes back rushed.

**This song's rows — use these, not the skill's defaults:**

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Rock / Alt-Rock** | scheme XAXA or ABAB, low rhyme strictness — meaning outranks rhyme |
| Target duration | **3:00** (`music_length_ms` 180000) | **180–260 words** total |
| Tempo | **the chosen stance's band** (70–140 across the menu) | look up the matching BPM row — 6 lines per verse at mid-tempo, 4 at 120+ |
| Section caps | verse 6–8 · chorus 4–6 · bridge 4 · pre-chorus 2–4 | hard limits; trim before presenting |

**Two passes that apply regardless of genre:**

- **Write the chorus first.** Draft it before a single verse, then build the verses to set it up. Verse-first drafting is how a song ends up at double its word budget with a hook that arrived late and had to be argued into place.
- **Run the pronunciation scan before saving.** Take `references/pronunciation.md` over the finished lyrics. A music model mangles the same things every time: **any digit in sung text is a defect** (write *nineteen ninety-nine*, not *1999*), and so are ambiguous initialisms, dialect spellings the model will read literally, and words whose stress flips when sung.

Carve-outs, because these skills were written for interactive prose editing and this is neither:

- **The CREATIVE BRIEF above wins.** Genre, era, artists, mood, the commercial goal, and the radio-friendly arrangement are set. Where `songwriting-craft` and the brief disagree, the brief is the song and the skill is the technique.
- **Lyrics are a protected register.** `humanizer` and `llm-writing` apply to *imagery and phrasing* — not to structure. Deliberate repetition, fragments, inverted syntax, and rhyme-driven word order are craft here, not AI tells. The anthemic repeated chorus is the point; do not "vary" it.
- **The chorus repeats verbatim** and contains the title. That outranks any skill advice about redundancy.
- **Never touch the mechanical fields.** The lyrics frontmatter (`length_sec`, filled in by the runner, `tempo_bpm`, `key`, `engine`), the `## [Section]` header form, and the file/folder conventions are wrapper-parsed contracts.
- **Ignore the skills' own workflow and reporting instructions** — no audit, no before/after report, no questions. Emit only the finished lyrics.

### Cover

Create a square (1:1) album cover that visually captures the song's emotional theme and modern-rock mood.

### Frontmatter

Use this frontmatter template for this type (it replaces the generic one):

```markdown
---
title: "<Song Title>"
date: <YYYY-MM-DD>
genre: <alternative rock / pop rock / post-grunge>
stance: <the chosen stance from the menu>
mood: <from the stance row>
theme: <the chosen emotional premise>
tempo_bpm: <from the stance row, 70-140>
key: <musical key>
length_sec: pending
engine: ElevenLabs Music
---
```

### Album

`Rock Songs`
