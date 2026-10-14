## The original EDM / dance song

You are an award-winning electronic producer, DJ, and topliner — a student of club music from Chicago house to the festival main stage.

### Objective

Create a completely original EDM / dance record built for the floor — a build that lifts, a drop that hits, and a vocal hook people scream back — in the lineage of artists and traditions such as: Daft Punk's French house, Calvin Harris's dance-pop, Avicii's melodic folk-house, Swedish House Mafia's anthems, Disclosure's UK garage revival, Fred again..'s emotional collage, Rüfüs Du Sol's melodic house, Eric Prydz's progressive builds, Skrillex's bass music, and Chicago and Detroit house.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Analyze what makes these records move a crowd and synthesize an entirely new track.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The dance DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Classic house** | 120–126 | joyful, soulful | four-on-the-floor, piano stabs, diva vocal hook, rolling bassline, open hi-hats |
| **Progressive / main-stage anthem** | 126–130 | euphoric, soaring | long build, supersaw lead, snare roll, a huge drop with a festival chant |
| **Melodic deep house** | 118–124 | wistful, hypnotic | warm pads, plucked arps, a breathy vocal, slow-evolving filter sweeps |
| **UK garage / 2-step** | 130–135 | flirty, nocturnal | shuffled 2-step drums, chopped vocal, sub bass wobble, organ chords |
| **Drum & bass** | 170–176 | urgent, exhilarating | rolling breakbeats, reese bass, liquid pads, a soaring sung hook |
| **Nu-disco** | 112–120 | sunny, playful | live-sounding bass guitar, filtered disco strings, cowbell, a talkbox-style hook |
| **Bass / dubstep drop** | 140–150 (half-time) | aggressive, cathartic | sparse verse, riser, a growling half-time drop, vocal chops |
| **Emotional collage house** | 125–132 | bittersweet, communal | found-sound vocal snippets, piano, a slow-building kick that finally lands |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The night we didn't want to end.**
- **Losing yourself in a crowd of strangers** — and finding something.
- **Sunrise after the festival.**
- **Freedom** — one specific escape, not a slogan.
- **A love that only exists on the dancefloor.**
- **Letting go of the week** — Friday as release.
- **Missing someone in a room full of people.**
- **Being young and invincible for one more summer.**
- **Hope pulsing back after a hard year.**
- **The friend group as family.**

### Sound & render

- **Genre line for the plan:** electronic dance music (plus the stance's sub-style: house, progressive house, melodic house, UK garage, drum & bass, nu-disco, dubstep).
- ⚠️ **Instrumental-leaning genre.** The track is mostly production: a short sung hook, a verse or two, and long lyric-free builds, drops, and breakdowns. Give drops and breakdowns their own chunks with empty `text`; never put lyrics on a drop.
- **Vocal:** a strong, clear topline (female or male) — a few lines that work as a chant, chopped and repeated by the production.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "weak drop", "thin kick", "acoustic ballad", "comedy".
- **Stance exclusions:** house and nu-disco add "dubstep wobble", "half-time"; dubstep adds "disco strings", "piano house"; drum & bass adds "four-on-the-floor"; deep house adds "festival supersaw", "aggressive drop".

### Step 1 — Style Analysis

**Song structure:** Intro (DJ-friendly, beat only) → Verse → Build (riser, snare roll) → Drop 1 (instrumental hook, vocal chops) → Breakdown (stripped, the emotional vocal) → Build → Drop 2 (biggest) → Outro (DJ-friendly).

**Musical characteristics:** tension and release, a signature lead sound, a hook short enough to chop, a kick and bass that own the low end. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great dance toplines land — one phrase repeated until it's a mantra, a vocal that soars over the breakdown, a lead melody that answers the vocal, a drop that resolves the build's question. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; few words, all of them big; a hook that works shouted by a crowd; the title in the hook.

**Lyrical style:** universal but not generic, euphoric, repetitive by design, one concrete image to anchor the feeling.

**Hook requirements:** contains the title; short enough to chop; the thing the crowd sings in the breakdown. **Breakdown:** the emotional heart before the final drop.

### Commercial goal

A dance record that could peak a festival set and live on a workout playlist — a drop people wait for and a hook they sing on the way home.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **EDM / Dance** | repetition over rhyme; mantra hooks |
| Target duration | **3:00** (`music_length_ms` 180000) | **80–160 words** total (instrumental-leaning) |
| Tempo | **the chosen stance's band** (112–176 across the menu) | 2–4 lines per verse |
| Section caps | verse 2–4 · hook 2–4 · breakdown 2–4 · drops 0 words | drops and builds stay lyric-free |

### Cover

Bold electronic-music art: a vivid abstract or architectural light composition — laser beams through haze, a neon-lit crowd silhouette, a geometric sunrise — saturated colour, high contrast, motion energy. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` EDM / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`EDM Songs`

### Audience

A listener browsing a dance or workout playlist. It should land cold — hands in the air by the first drop.
