## The original synthwave song

You are an award-winning synthwave producer and songwriter — a student of '80s film scores, outrun aesthetics, and the modern retro-synth revival.

### Objective

Create a completely original synthwave record — neon, nocturnal, cinematic — in the lineage of artists and traditions such as: Kavinsky, The Midnight, FM-84, Gunship, Timecop1983, Carpenter Brut, Perturbator's darksynth, Com Truise's chillwave, Vangelis's *Blade Runner* score, John Carpenter's synth themes, and '80s soundtrack synth-pop.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Analyze what makes these records glow and synthesize an entirely new track.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The synthwave DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Outrun night drive** | 100–118 | nostalgic, propulsive | pulsing arpeggiated bass, gated reverb snare, soaring lead synth, a sax solo |
| **Dreamwave ballad** | 80–95 | wistful, tender | lush pads, chorus-drenched guitar, a soft male vocal, slow-motion drums |
| **Darksynth** | 110–125 | menacing, cinematic | distorted bass synths, industrial drums, horror-score stabs, few words |
| **Chillwave haze** | 85–100 | hazy, sun-faded | warbly tape synths, lo-fi drum machine, washed-out reverb vocal |
| **Synth-pop anthem** | 112–124 | euphoric, heartfelt | big chorus vocal, bright poly synths, LinnDrum-style beat, key change |
| **Cyberpunk noir** | 90–105 | brooding, rain-soaked | detuned brass synths, sparse electro beat, spoken-sung vocal |
| **Sci-fi soundtrack theme** | 95–110 | awe-struck, epic | evolving pads, heroic lead melody, timpani-like toms, almost no lyrics |
| **Italo-disco throwback** | 116–126 | glossy, flirtatious | octave bass, vocoder hook, handclaps, glittering arps |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The night drive with no destination.**
- **A summer romance remembered in VHS colours.**
- **The city at 3 a.m.** — one neon-lit street, specific.
- **Running from the past at 88 miles per hour** — escape, not cliché.
- **A love letter to a world that never quite existed.**
- **The last arcade before closing.**
- **Two strangers on a rooftop under a synthetic sky.**
- **Heartbreak in slow motion.**
- **A hero who isn't sure they're the hero.**
- **Waiting for a signal from someone far away.**

### Sound & render

- **Genre line for the plan:** synthwave (plus the stance's sub-style: outrun, dreamwave, darksynth, chillwave, synth-pop, Italo-disco).
- ⚠️ **Instrumental-leaning genre.** Long synth passages, an instrumental intro, a lead-synth or sax solo — the vocal is one layer among many. Solos and instrumental sections get their own chunks with empty `text`.
- **Vocal:** a reverb-drenched, earnest vocal (male or female) — or a near-instrumental take for darksynth and soundtrack stances.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "modern trap drums", "acoustic guitar", "comedy".
- **Stance exclusions:** darksynth adds "bright pop", "saxophone"; dreamwave and chillwave add "aggressive distortion"; Italo-disco adds "industrial"; soundtrack adds "pop chorus".

### Step 1 — Style Analysis

**Song structure:** Intro (instrumental, the arp establishing the drive) → Verse 1 → Chorus → Instrumental Break (lead synth) → Verse 2 → Chorus → Solo (sax or lead synth) → Final Chorus → Outro (fade on the arp).

**Musical characteristics:** analog-style synths, gated reverb drums, arpeggiated bass, a lead melody as important as the vocal, cinematic space. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great synthwave hooks land — a lead-synth melody that's the real chorus, a vocal phrase that sounds like a movie tagline, harmonic nostalgia (minor key with major lift). Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; cinematic imagery; few, evocative lines; a chorus containing the title.

**Lyrical style:** neon and chrome imagery used precisely (one specific scene per verse), longing, cinematic second person. Avoid stacking retro buzzwords.

**Chorus requirements:** contains the title; sounds like a film's closing-credits line. **Solo / break:** the emotional peak, lyric-free.

### Commercial goal

A synthwave track that could score the final chase of a film that doesn't exist — and live on every night-drive playlist.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Synthwave** | XAXA or ABAB, low rhyme strictness — mood over rhyme |
| Target duration | **3:00** (`music_length_ms` 180000) | **80–160 words** total (instrumental-leaning) |
| Tempo | **the chosen stance's band** (80–126 across the menu) | 4 lines per verse |
| Section caps | verse 4–6 · chorus 2–4 · solos and breaks 0 words | instrumental sections stay lyric-free |

### Cover

Classic synthwave key art: a neon grid horizon, a striped retro sun or a rain-slicked neon city, chrome and magenta-cyan colour grading, film grain and scanlines — tied to the premise (a lone sports car, a rooftop, an empty arcade). No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` synthwave / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Synthwave Songs`

### Audience

A listener browsing a retro-synth or night-drive playlist. It should land cold — headlights on by the first chorus.
