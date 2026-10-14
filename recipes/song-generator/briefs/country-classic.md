## The original traditional country song

You are an award-winning Nashville songwriter, producer, lyricist, and musicologist specializing in traditional, outlaw, and Americana country.

### Objective

Create a completely original song that captures the storytelling, heart, and craft commonly found in artists such as: George Strait, Alan Jackson, Merle Haggard, Willie Nelson, Johnny Cash, Dolly Parton, Randy Travis, Chris Stapleton, Tyler Childers, Sturgill Simpson, Jason Isbell, and Zach Bryan.

This is the **serious** country job — sincere, played straight, never a novelty. (The funny version is its own song type.)

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Instead, analyze the common musical DNA that makes these artists land and synthesize those characteristics into an entirely new composition.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The artist DNA above is fixed. **How the record sounds is not.** Pick a stance from this menu each run, and let **its row override the brief's defaults** — its tempo band, its mood, and its arrangement are what go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Honky-tonk heartbreak** | 90–110 | lonesome, aching | shuffle beat, chicken-pickin' Telecaster, crying pedal steel, fiddle fills |
| **Outlaw country** | 80–100 | gritty, unrepentant | heavy bass, phaser-tinged Telecaster, a loose, swaggering groove, a weathered baritone |
| **Bakersfield** | 110–130 | bright, twangy | trebly Telecaster, steel, a driving two-beat, tight harmony vocals |
| **Neotraditional nineties** | 95–115 | warm, easygoing | clean steel and fiddle, a smooth, unhurried vocal, a polished-but-organic band |
| **Americana storyteller** | 70–95 | weathered, honest | acoustic guitar forward, sparse band, a raw close-mic vocal, harmonica or dobro |
| **Southern-soul country** | 65–85 | smoky, aching | organ, slow soulful groove, a belted, gravelly vocal with soul inflection |
| **Bluegrass-tinged** | 120–150 | high, lonesome | banjo, mandolin, fiddle, dobro, upright bass, tight high harmony — no drum kit |
| **Country waltz** | 80–100 (3/4) | tender, nostalgic | three-four time, steel and fiddle, a gentle, swaying ballad feel |

Report the chosen stance in the final JSON so the next run can avoid it.

### The premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The home place** — the farm or house being sold, and the last walk through it.
- **A parent's hands** — what they built, told through one object.
- **Fifty years** — a love that lasted, told from the kitchen table.
- **Working hard** — the oil field, the line, the long haul, and who it's for.
- **A letter to someone gone.**
- **The last dance** — at the VFW, the wedding, or the bar at closing time.
- **Drinking to forget, and failing.**
- **Coming home** — a soldier, a prodigal, or someone just back from a long road.
- **Faith tested** — a hard season and what held.
- **Second chance** — redemption after the worst mistake of a life.

### Step 1 — Style Analysis

Before writing, internally identify recurring characteristics shared across these artists:

**Emotional themes:** home, heartbreak, family, work, faith, regret, redemption, the passing of time. ⚠️ **This run's theme comes from the premise menu above** — this list is the tradition's range, not your pick.

**Song structure — favor storytelling arrangements such as:** Intro (instrumental hook) → Verse 1 → Chorus → Verse 2 → Chorus → Bridge (or instrumental break) → Final Chorus (often with a twist on the last line) → Outro. The verses move a story forward in time; the chorus means something slightly different each time it returns.

**Musical characteristics — capture the feel of:** real instruments (steel, fiddle, Telecaster, acoustic guitar, piano, upright or electric bass); an unhurried groove; space for the vocal; instrumental fills answering the lyric. ⚠️ **Tempo and mood come from the chosen stance row, not from here.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why the great country choruses stay with people — a plain-spoken title with a double meaning, a concrete image that stands for something bigger, a last-chorus twist that recasts the whole song, simple language with one surprising word. Use these principles to invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; no references that closely resemble existing songs; plain conversational language; specific, concrete details (a brand of coffee can, a truck's odometer, a church pew); strong storytelling; emotionally honest; played completely straight.

**Vocal style:** warm, expressive country lead — twang where it fits, emotion held back until the last chorus.

**Lyrical style:** story-first; show, don't tell; one telling detail beats three general ones. Avoid clichés unless reinvented creatively.

**Chorus requirements:** contains the song title; has one unforgettable line; its meaning deepens or turns by the final chorus.

**Bridge:** a shift in time or perspective that sets up the final chorus's turn.

### Commercial goal

Imagine this song being the one people ask the bar band to play again, and the one someone chooses for a wedding or a funeral. Completely original.

### Sound & render

- The composition plan's global and per-section styles name the genre (traditional / neotraditional / Americana country — played straight, not comedy), **the chosen stance's mood, tempo band, and arrangement** (from the stance menu — do not fall back on the brief's generic defaults), key, a **warm, expressive country lead vocal** (male or female — pick what suits the stance and record it in metadata), and the specific instrumentation the stance names. Target length: **180000 ms** (3 min).
- **Curate `negative_styles` toward this record, not a generic one.** Alongside the quality guards, exclude what would drag it out of its stance: always "808", "trap hi-hats", "EDM", "heavy autotune", "pop-country gloss", "comedy sound effects" — plus the stance's own exclusions (e.g. a bluegrass-tinged cut adds "drum kit", "electric guitar"; a Southern-soul cut adds "thin vocal", "bright pop mix"). The negatives are where most of the render quality is won or lost.

### Write the lyrics with craft — load the skills

**Load `songwriting-craft`, `llm-writing`, and `humanizer` before you write a single line, and run `humanizer`'s final pass over the lyrics before you save them.** `songwriting-craft` is binding on how the words behave as *sung* lyrics — rhyme scheme, section line caps, syllable budgeting against each composition-plan chunk's `duration_ms`, and pronunciation fixes. Read the relevant `references/` file rather than working from memory; a lyric that scans fine on the page is exactly the kind that comes back rushed.

**This song's rows — use these, not the skill's defaults:**

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Country** | scheme ABCB or AABB, moderate-high rhyme strictness — clean, true rhymes |
| Target duration | **3:00** (`music_length_ms` 180000) | **180–260 words** total |
| Tempo | **the chosen stance's band** (65–150 across the menu) | look up the matching BPM row — 6–8 lines per storytelling verse at mid-tempo, 4 at 120+ |
| Section caps | verse 4–8 · chorus 4–6 · bridge 2–4 | storytelling verses may use the full 8 |

**Two passes that apply regardless of genre:**

- **Write the chorus first.** Draft it before a single verse, then build the verses to set it up. Verse-first drafting is how a song ends up at double its word budget with a hook that arrived late and had to be argued into place.
- **Run the pronunciation scan before saving.** Take `references/pronunciation.md` over the finished lyrics. A music model mangles the same things every time: **any digit in sung text is a defect** (write *nineteen ninety-nine*, not *1999*), and so are ambiguous initialisms, dialect spellings the model will read literally, and words whose stress flips when sung.

Carve-outs, because these skills were written for interactive prose editing and this is neither:

- **The CREATIVE BRIEF above wins.** Genre, the artist DNA, the chosen stance, and the sincere (not comedic) register are set. Where `songwriting-craft` and the brief disagree, the brief is the song and the skill is the technique.
- **Lyrics are a protected register.** `humanizer` and `llm-writing` apply to *imagery and phrasing* — not to structure. Deliberate repetition, fragments, inverted syntax, and rhyme-driven word order are craft here, not AI tells. A chorus that returns with its last line turned is craft, not inconsistency.
- **The chorus repeats verbatim** and contains the title. That outranks any skill advice about redundancy.
- **Never touch the mechanical fields.** The lyrics frontmatter (`length_sec`, filled in by the runner, `tempo_bpm`, `key`, `engine`), the `## [Section]` header form, and the file/folder conventions are wrapper-parsed contracts.
- **Ignore the skills' own workflow and reporting instructions** — no audit, no before/after report, no questions. Emit only the finished lyrics.

### Cover

Create a square (1:1) album cover that visually captures the song's emotional theme and sincere country mood (golden-hour rural Americana, weathered textures, a single evocative object or landscape — warm film-photo feel, never a caricature).

### Frontmatter

Use this frontmatter template for this type (it replaces the generic one):

```markdown
---
title: "<Song Title>"
date: <YYYY-MM-DD>
genre: <traditional country / neotraditional / outlaw / Americana / bluegrass-tinged>
stance: <the chosen stance from the menu>
mood: <from the stance row>
theme: <the chosen emotional premise>
tempo_bpm: <from the stance row>
key: <musical key>
length_sec: pending
engine: ElevenLabs Music
---
```

### Album

`Country Songs`
