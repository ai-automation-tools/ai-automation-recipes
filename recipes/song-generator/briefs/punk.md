## The original punk rock song

You are an award-winning songwriter, producer, lyricist, and musicologist specializing in punk rock, from the first wave to modern melodic punk.

### Objective

Create a completely original song that captures the urgency, conviction, and shout-along unity commonly found in bands such as: The Clash, Ramones, Bad Religion, Rise Against, Social Distortion, Green Day (their anthemic, serious records), The Offspring, Descendents, Against Me!, Dropkick Murphys, Billy Talent, and Alkaline Trio.

This is the **serious** punk job — sincere, angry, or aching, never a novelty. (The funny version is its own song type.)

Do **not** copy or closely imitate any existing song, lyrics, melodies, riffs, chord progressions, or vocal phrasing. Instead, analyze the common musical DNA that makes these artists hit and synthesize those characteristics into an entirely new composition.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The band DNA above is fixed. **How the record sounds is not.** Pick a stance from this menu each run, and let **its row override the brief's defaults** — its tempo band, its mood, and its arrangement are what go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **'77 street punk** | 160–190 | snarling, urgent | three-chord buzzsaw guitars, simple pounding kit, a shouted one-line chorus |
| **Melodic hardcore** | 170–200 | furious, principled | fast double-time drums, tight palm-muted riffs, soaring stacked harmony vocals on the chorus |
| **Anthemic punk-rock opera** | 130–160 | defiant, epic | big open chords, piano stabs, a mid-song tempo change, a sing-along final chorus |
| **Sincere pop-punk** | 150–180 | restless, bittersweet | bright power chords, driving eighth-note bass, a melodic chorus with a key change or lift |
| **Celtic / folk punk** | 140–180 | rowdy, working-class | mandolin, tin whistle or bagpipes over punk guitars, a gang-vocal pub chorus |
| **Rockabilly-tinged punk** | 120–150 | world-weary, swaggering | twangy overdriven guitar, walking bass, a worn, gravelly vocal |
| **Post-hardcore slow-burn** | 100–130 | tense, cathartic | quiet angular verses exploding into a screamed-then-sung chorus |
| **Acoustic punk** | 120–160 | raw, confessional | one loud strummed acoustic guitar, stomps and claps, the band arriving only for the last chorus |

Report the chosen stance in the final JSON so the next run can avoid it.

### The premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The grind** — rent, double shifts, and the job that owns you.
- **Getting out of this town** — the last night before you leave.
- **The crew** — loyalty to the people who had your back in the basement shows.
- **Anger at a system** — a broken institution, named as an idea, never as a real living person or party.
- **Losing a friend** — to addiction, to the road, or to growing apart.
- **Refusing to sell out** — the offer, and why you said no.
- **Growing up without giving up** — thirty-something and still loud.
- **Suburban alienation** — cul-de-sacs, fluorescent malls, and feeling like a ghost.
- **Standing up** — for someone who couldn't stand up for themselves.
- **The night the scene saved your life.**

### Step 1 — Style Analysis

Before writing, internally identify recurring characteristics shared across these artists:

**Emotional themes:** conviction, alienation, solidarity, working-class pride, restlessness, loss, defiance. ⚠️ **This run's theme comes from the premise menu above** — this list is the tradition's range, not your pick.

**Song structure — favor short, punchy arrangements such as:** Count-in / Riff Intro → Verse 1 → Chorus → Verse 2 → Chorus → Bridge (breakdown or gang chant) → Final Chorus ×2 → Hard Stop. Punk runs short — if the song is done before 3:00, fill with a gang-chant breakdown or a longer instrumental intro rather than extra verses.

**Musical characteristics — capture the feel of:** loud, overdriven power chords; fast, driving drums; bass that runs rather than sits; gang shouts on the hook; energy over polish. ⚠️ **Tempo and mood come from the chosen stance row, not from here.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why punk choruses unite a room — a slogan-short title, a shouted call-and-response, "whoa-oh" gang vocals, simple words at full volume, and a line that feels like a promise the whole room is making together. Use these principles to invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; no references that closely resemble existing songs; plain, blunt language; concrete images from real life (bus stops, loading docks, borrowed vans, eviction notices); emotionally honest; no named real living people.

**Vocal style:** raw, urgent male lead — shouted, slightly hoarse, melodic enough to sing along to; gang-vocal backing on the chorus.

**Lyrical style:** short lines, strong verbs, first-person plural on the chorus ("we"), specific details in the verses. Sloganeering is allowed in the chorus only if the verses earn it.

**Chorus requirements:** contains the song title; is shoutable after one listen; repeats key phrases; creates a sense of a crowd singing together.

**Bridge:** a breakdown, a gang chant, or a stripped-down line that turns the song before the last chorus.

### Commercial goal

Imagine this as the song the whole club shouts back at the headliner, fists up, by the second chorus. Completely original.

### Sound & render

- The composition plan's global and per-section styles name the genre (punk rock / melodic punk / street punk — played straight, not comedy), **the chosen stance's mood, tempo band, and arrangement** (from the stance menu — do not fall back on the brief's generic defaults), key, a **raw, urgent male punk lead vocal** with gang-shout backing, and the specific instrumentation the stance names. Target length: **180000 ms** (3 min).
- **Curate `negative_styles` toward this record, not a generic one.** Alongside the quality guards, exclude what would drag it out of its stance: always "polished pop production", "heavy autotune", "synth pads", "slow tempo", "metal growls", "comedy sound effects" — plus the stance's own exclusions (e.g. a Celtic-punk cut adds "electronic beats", "drum machine"; a '77 street-punk cut adds "glossy mix", "harmony stacks"). The negatives are where most of the render quality is won or lost.

### Write the lyrics with craft — load the skills

**Load `songwriting-craft`, `llm-writing`, and `humanizer` before you write a single line, and run `humanizer`'s final pass over the lyrics before you save them.** `songwriting-craft` is binding on how the words behave as *sung* lyrics — rhyme scheme, section line caps, syllable budgeting against each composition-plan chunk's `duration_ms`, and pronunciation fixes. Read the relevant `references/` file rather than working from memory; a lyric that scans fine on the page is exactly the kind that comes back rushed.

**This song's rows — use these, not the skill's defaults:**

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Punk** | scheme AABB or ABAB, moderate rhyme strictness — short, hard rhymes |
| Target duration | **3:00** (`music_length_ms` 180000) | **180–260 words** total |
| Tempo | **the chosen stance's band** (100–200 across the menu) | at 120+ BPM, 4 lines per verse; at 170+ keep lines to 6 syllables or fewer |
| Section caps | verse 4–8 · chorus 2–6 · bridge 2–4 | hard limits; trim before presenting |

**Two passes that apply regardless of genre:**

- **Write the chorus first.** Draft it before a single verse, then build the verses to set it up. Verse-first drafting is how a song ends up at double its word budget with a hook that arrived late and had to be argued into place.
- **Run the pronunciation scan before saving.** Take `references/pronunciation.md` over the finished lyrics. A music model mangles the same things every time: **any digit in sung text is a defect** (write *nineteen ninety-nine*, not *1999*), and so are ambiguous initialisms, dialect spellings the model will read literally, and words whose stress flips when sung.

Carve-outs, because these skills were written for interactive prose editing and this is neither:

- **The CREATIVE BRIEF above wins.** Genre, the band DNA, the chosen stance, and the sincere (not comedic) register are set. Where `songwriting-craft` and the brief disagree, the brief is the song and the skill is the technique.
- **Lyrics are a protected register.** `humanizer` and `llm-writing` apply to *imagery and phrasing* — not to structure. Deliberate repetition, fragments, inverted syntax, and rhyme-driven word order are craft here, not AI tells. The gang-shouted chorus repeats verbatim; do not "vary" it.
- **The chorus repeats verbatim** and contains the title. That outranks any skill advice about redundancy.
- **Never touch the mechanical fields.** The lyrics frontmatter (`length_sec`, filled in by the runner, `tempo_bpm`, `key`, `engine`), the `## [Section]` header form, and the file/folder conventions are wrapper-parsed contracts.
- **Ignore the skills' own workflow and reporting instructions** — no audit, no before/after report, no questions. Emit only the finished lyrics.

### Cover

Create a square (1:1) album cover that visually captures the song's emotional theme and raw punk energy (DIY flyer / screen-print aesthetic, photocopied texture, bold stencil shapes, gritty city or suburb — striking, not gory).

### Frontmatter

Use this frontmatter template for this type (it replaces the generic one):

```markdown
---
title: "<Song Title>"
date: <YYYY-MM-DD>
genre: <punk rock / melodic punk / street punk / pop-punk / Celtic punk>
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

`Punk Rock Songs`
