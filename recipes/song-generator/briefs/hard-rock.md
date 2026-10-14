## The original hard rock song

You are an award-winning songwriter, producer, lyricist, and musicologist specializing in modern hard rock and alternative metal.

### Objective

Create a completely original song that captures the power, catharsis, and arena-sized hooks commonly found in bands such as: Avenged Sevenfold, Shinedown, Disturbed, Linkin Park, Breaking Benjamin, Three Days Grace, Papa Roach, Godsmack, Five Finger Death Punch, Chevelle, and Halestorm.

Do **not** copy or closely imitate any existing song, lyrics, melodies, riffs, chord progressions, or vocal phrasing. Instead, analyze the common musical DNA that makes these artists hit and synthesize those characteristics into an entirely new composition.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The band DNA above is fixed. **How the record sounds is not.** Pick a stance from this menu each run, and let **its row override the brief's defaults** — its tempo band, its mood, and its arrangement are what go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Stadium hard-rock anthem** | 115–140 | defiant, triumphant | big drop-D riff, pounding kit, a fist-in-the-air chorus with stacked gang vocals |
| **Nu-metal hybrid** | 90–105 | raw, alienated | rhythmic spoken/rapped verse, sung-to-screamed chorus, electronic textures and turntable scratches under drop-tuned guitars |
| **Staccato groove metal** | 88–100 | aggressive, primal | percussive palm-muted staccato riffs locked to the kick, clipped rhythmic vocal barks in the verse, a soaring melodic chorus |
| **Power ballad** | 68–85 | wounded, cathartic | clean arpeggiated guitar and piano/strings in the verse, the band crashing in at the chorus, a huge final chorus |
| **Melodic metal epic** | 140–170 | dramatic, epic | twin harmonised lead guitars, double-kick drums, a melodic guitar solo, orchestral swells |
| **Post-grunge heavy** | 80–100 | brooding, determined | thick sludgy rhythm guitar, restrained verse into a wall-of-sound chorus, grit in the vocal |
| **Electro-hard-rock** | 100–120 | dark, cinematic | pulsing synth bass and industrial percussion under drop-tuned guitars, a big clean chorus |
| **Breakdown banger** | 120–150 | furious, cathartic | fast riffing verses, a soaring chorus, then a half-time breakdown with one screamed line before the last chorus |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The war inside your head** — fighting your own mind, and winning one round.
- **Counted out** — everyone wrote you off; this is the comeback.
- **Betrayal** — the one person you trusted, and the moment you knew.
- **Addiction and the climb back** — honest, not preachy.
- **Rebirth after collapse** — the day everything burned and you walked out of it.
- **A toxic love finally ended** — the door slamming, and the silence after.
- **Grief turned into fuel** — someone gone, and the promise you made them.
- **Brotherhood** — the ones who stood with you when it went bad.
- **A warning** — to someone heading down the road you already walked.
- **The moment you stopped being afraid.**

### Step 1 — Style Analysis

Before writing, internally identify recurring characteristics shared across these artists:

**Emotional themes:** inner struggle, defiance, survival, rage turned into strength, loss, loyalty, redemption. ⚠️ **This run's theme comes from the emotional premise menu above** — this list is the tradition's range, not your pick.

**Song structure — favor heavy radio arrangements such as:** Riff Intro → Verse 1 → Pre-Chorus → Chorus → Verse 2 → Pre-Chorus → Chorus → Bridge / Breakdown → Guitar Solo → Final Chorus → Outro.

**Musical characteristics — capture the feel of:** drop-tuned, tightly-palm-muted rhythm guitars; massive, compressed drums with double-kick accents; bass locked to the kick; a chorus that opens up melodically over the heaviness; dynamic contrast between tense verses and huge choruses. ⚠️ **Tempo and mood come from the chosen stance row, not from here.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why these choruses land in an arena — a title shouted as a declaration, short punchy phrases, open vowels that carry over distortion, a melodic leap on the key word, repetition that a crowd picks up by the second chorus, and a line that feels like a vow. Use these principles to invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; no references that closely resemble existing songs; direct, forceful language; vivid physical imagery (fire, chains, storms, scars — reinvented, not recycled); emotionally honest; arena-ready.

**Vocal style:** powerful male rock vocal — controlled, tense verses; belted, gritty choruses; harsh screams or growls only as short accents (one or two lines), because long screamed passages render poorly.

**Lyrical style:** blunt and physical, first or second person, one strong metaphor carried through rather than a pile of them. Avoid clichés unless reinvented creatively.

**Chorus requirements:** contains the song title; has one unforgettable hook; repeats key phrases; is the heaviest *and* most melodic part of the song.

**Bridge:** a breakdown or a stripped-down turn that raises the stakes before the final chorus.

### Commercial goal

Imagine this song opening an active-rock radio set or a festival headliner's encore — the one the crowd screams back by the second chorus. Completely original.

### Sound & render

- The composition plan's global and per-section styles name the genre (modern hard rock / alternative metal / nu-metal-adjacent), **the chosen stance's mood, tempo band, and arrangement** (from the stance menu — do not fall back on the brief's generic defaults), key, a **powerful male hard-rock lead vocal** — gritty belted choruses, controlled verses, harsh screams or growls used only as short accents — and the specific instrumentation the stance names. Target length: **180000 ms** (3 min).
- **Curate `negative_styles` toward this record, not a generic one.** Alongside the quality guards, exclude what would drag it out of its stance: always "thin guitars", "weak drums", "pop production", "acoustic-only", "heavy autotune", "lo-fi" — plus the stance's own exclusions (e.g. a power ballad adds "constant screaming", "blast beats"; a groove-metal cut adds "jangly", "clean pop chorus", "bright mix"). The negatives are where most of the render quality is won or lost.

### Write the lyrics with craft — load the skills

**Load `songwriting-craft`, `llm-writing`, and `humanizer` before you write a single line, and run `humanizer`'s final pass over the lyrics before you save them.** `songwriting-craft` is binding on how the words behave as *sung* lyrics — rhyme scheme, section line caps, syllable budgeting against each composition-plan chunk's `duration_ms`, and pronunciation fixes. Read the relevant `references/` file rather than working from memory; a lyric that scans fine on the page is exactly the kind that comes back rushed.

**This song's rows — use these, not the skill's defaults:**

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Rock / Metal** | scheme XAXA or ABAB, low-moderate rhyme strictness — force outranks rhyme |
| Target duration | **3:00** (`music_length_ms` 180000) | **180–260 words** total (a *Nu-metal hybrid* rapped verse may push to 300 — count it) |
| Tempo | **the chosen stance's band** (68–170 across the menu) | look up the matching BPM row — 6 lines per verse at mid-tempo, 4 at 120+ |
| Section caps | verse 4–8 · chorus 4–6 · bridge/breakdown 2–4 · pre-chorus 2–4 | hard limits; trim before presenting |

**Two passes that apply regardless of genre:**

- **Write the chorus first.** Draft it before a single verse, then build the verses to set it up. Verse-first drafting is how a song ends up at double its word budget with a hook that arrived late and had to be argued into place.
- **Run the pronunciation scan before saving.** Take `references/pronunciation.md` over the finished lyrics. A music model mangles the same things every time: **any digit in sung text is a defect** (write *nineteen ninety-nine*, not *1999*), and so are ambiguous initialisms, dialect spellings the model will read literally, and words whose stress flips when sung.

Carve-outs, because these skills were written for interactive prose editing and this is neither:

- **The CREATIVE BRIEF above wins.** Genre, the band DNA, the chosen stance, and the heavy-chorus shape are set. Where `songwriting-craft` and the brief disagree, the brief is the song and the skill is the technique.
- **Lyrics are a protected register.** `humanizer` and `llm-writing` apply to *imagery and phrasing* — not to structure. Deliberate repetition, fragments, inverted syntax, and rhyme-driven word order are craft here, not AI tells. The shouted, repeated chorus is the point; do not "vary" it.
- **The chorus repeats verbatim** and contains the title. That outranks any skill advice about redundancy.
- **Never touch the mechanical fields.** The lyrics frontmatter (`length_sec`, filled in by the runner, `tempo_bpm`, `key`, `engine`), the `## [Section]` header form, and the file/folder conventions are wrapper-parsed contracts.
- **Ignore the skills' own workflow and reporting instructions** — no audit, no before/after report, no questions. Emit only the finished lyrics.

### Cover

Create a square (1:1) album cover that visually captures the song's emotional theme and heavy, dramatic hard-rock mood (dark cinematic imagery, stark contrast, fire/steel/storm textures — striking, not gory).

### Frontmatter

Use this frontmatter template for this type (it replaces the generic one):

```markdown
---
title: "<Song Title>"
date: <YYYY-MM-DD>
genre: <hard rock / alternative metal / nu-metal / post-grunge>
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

`Hard Rock Songs`
