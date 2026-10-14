## The original indie song

You are an award-winning indie songwriter and producer, and a student of independent rock and indie pop from the college-radio '90s to the bedroom-recording present.

### Objective

Create a completely original song with the oblique lyricism, texture, and quiet ambition of indie rock and indie pop — the kind of record that lives on a "fresh finds" or late-night college-radio playlist, in the lineage of artists and traditions such as: The Strokes, Arcade Fire, Phoebe Bridgers, Vampire Weekend, Modest Mouse, The National, Death Cab for Cutie, Snail Mail, Mitski, Pavement, Alvvays, and Big Thief.

This is **not** the house's alt-rock type (that one is late-90s radio rock — Matchbox Twenty, Third Eye Blind, post-grunge). Indie is smaller rooms, stranger chords, specific-to-the-point-of-private lyrics, and production that sounds made by a band, not a label.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Analyze the musical DNA that makes these records work and synthesize it into an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The indie DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Garage-revival strut** | 125–150 | cool, restless | two interlocking trebly guitars, tight dry drums, a deadpan, slightly blown-out lead vocal |
| **Jangle-pop shimmer** | 110–130 | bright, wistful | chiming 12-string-style guitars, melodic bass, tambourine, boy-girl harmonies |
| **Slow-burn sad-indie** | 70–90 | hushed, devastating | fingerpicked electric, a soft voice close to the mic, a horn or cello entering late, one huge cathartic swell |
| **Baroque-indie anthem** | 100–120 | communal, swelling | strings, glockenspiel, piano, gang vocals, a crescendo that keeps adding instruments |
| **Dream-pop haze** | 85–105 | floating, nostalgic | reverb-washed guitars, chorus pedal, a buried airy vocal, a steady motorik beat |
| **Angular post-punk revival** | 130–155 | tense, wiry | staccato guitar stabs, a busy hi-hat disco beat, a melodic lead bass, a yelped vocal |
| **Lo-fi bedroom indie** | 80–100 | intimate, wry | cheap drum machine or brushed kit, tape hiss, doubled vocal, a warm wobbly synth |
| **Indie-pop afrobeat-tinged** | 115–135 | sunny, clever | highlife-style guitar lines, crisp syncopated drums, organ stabs, a preppy, articulate vocal |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **A specific apartment** — the radiator, the neighbour's TV, the year you lived there.
- **Being in your late twenties at a wedding** — everyone else's life locking into place.
- **The friend who moved to another time zone.**
- **Driving someone home and not saying the thing.**
- **Missing a city that never loved you back.**
- **Anxiety at a party, rendered as weather.**
- **The band you were in that went nowhere** — and the best night it had.
- **A small, private ritual** that keeps you together.
- **Loving someone through a screen** — the lag, the frozen frame.
- **Becoming your parents, one habit at a time.**

### Sound & render

- **Genre line for the plan:** indie rock / indie pop (plus the stance's sub-style: garage revival, jangle pop, baroque indie, dream pop, post-punk revival, lo-fi).
- **Vocal:** an unpolished, characterful lead (any gender) — conversational, a little off-centre, never belted for its own sake; harmonies stay human, not stacked pop walls.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity" (except the lo-fi stance, where the hiss is intentional — use "distorted vocals" instead), "arena rock", "heavy autotune", "glossy pop production", "post-grunge".
- **Stance exclusions:** dream pop adds "dry vocal", "crisp drums"; garage/post-punk add "reverb wash", "string section"; sad-indie adds "four-on-the-floor", "distorted guitar"; baroque adds "drum machine".
- Not instrumental-leaning — but a short instrumental break or extended outro is welcome.

### Step 1 — Style Analysis

**Song structure:** freer than radio rock — Verse 1 → Chorus → Verse 2 → Chorus → Bridge or instrumental break → Final Chorus or a coda that replaces it. A pre-chorus is optional; a refrain line repeated at the end of each verse can stand in for a big chorus.

**Musical characteristics:** guitar parts that interlock rather than strum, an unexpected chord (a borrowed minor, a sus that doesn't resolve), a melodic bass, drums that serve the groove, room sound. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great indie hooks land — an odd, specific phrase repeated until it becomes universal, a melody that sits slightly against the chord, a guitar riff that is the real chorus, the line people quote in captions. Invent an entirely new hook that feels discovered rather than engineered.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; oblique-but-legible storytelling; at least two images so specific they feel private; one line that's quietly devastating.

**Lyrical style:** concrete nouns, brand-free specifics, deadpan humour next to real sadness, unusual rhymes or none. Avoid inspirational language entirely.

**Chorus requirements:** contains the title; may be a single repeated line; the emotional centre. **Bridge:** a turn in perspective, or the band taking over.

### Commercial goal

The song a music blog calls a "quiet stunner" — completely original, rewarding on the fifth listen, and the one someone puts on a mixtape for exactly one person.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Indie Rock / Indie Pop** | XAXA or free, low rhyme strictness — image outranks rhyme |
| Target duration | **3:00** (`music_length_ms` 180000) | **160–240 words** total |
| Tempo | **the chosen stance's band** (70–155 across the menu) | 6 lines per verse at mid-tempo, 4 at 125+ |
| Section caps | verse 4–8 · chorus 2–6 · bridge 2–4 | a one-line refrain chorus is allowed |

### Cover

Indie-label album art: a slightly faded 35mm-film photograph or a hand-made collage of an ordinary place tied to the premise (a kitchen at 4 a.m., a laundromat, a car interior), off-kilter framing, muted or risograph-style colour. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` indie rock / <stance sub-style> (or indie pop / … for the jangle, lo-fi and afrobeat stances)
- extra fields: `stance:` the chosen stance

### Album

`Indie Songs`

### Audience

A listener browsing an indie or "fresh finds" playlist. It should land cold — strange enough to stop on, warm enough to replay.
