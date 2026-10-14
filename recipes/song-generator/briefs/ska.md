## The original ska song

You are an award-winning ska songwriter, horn arranger, and producer, and a student of every wave of ska — Jamaican originals, 2 Tone, and '90s third wave.

### Objective

Create a completely original song with the offbeat bounce, horn-driven joy, and sneaky bite of real ska — in the lineage of artists and traditions such as: The Skatalites, Prince Buster, Desmond Dekker, The Specials, Madness, The Selecter, The English Beat, Toots and the Maytals, The Mighty Mighty Bosstones, Reel Big Fish's straighter cuts, Streetlight Manifesto, The Interrupters, Sublime, and No Doubt's early records.

Do **not** copy or closely imitate any existing song, lyrics, melodies, horn lines, chord progressions, or vocal phrasing. Analyze the musical DNA that makes these records skank and synthesize it into an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The ska DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Jamaican first-wave** | 110–130 | joyful, sunlit | upright-feel walking bass, guitar and piano chops on the offbeat, a trombone-and-sax horn section, a warm vintage room |
| **2 Tone protest** | 140–165 | urgent, wry | tight choppy guitar, organ skank, a nervy clipped vocal, social commentary over a danceable beat |
| **Third-wave skate-ska** | 160–190 | manic, cathartic | punk-speed verses that drop into upstroke skank, a big horn riff hook, gang-vocal chorus |
| **Rocksteady slow-burn** | 85–100 | sweet, longing | slowed-down groove, prominent melodic bass, soulful lead with harmony backing vocals |
| **Ska-punk breakdown** | 170–200 | furious, defiant | distorted power chords alternating with clean skank, a half-time horn breakdown |
| **Big-band ska** | 125–145 | swaggering, brassy | a full horn section with trumpet solos, swing-flavoured drums, call-and-response chorus |
| **Dub-ska late night** | 100–115 | hazy, introspective | echo-drenched horn stabs, dub delays on the snare, a laid-back vocal |
| **Pop-ska radio cut** | 130–150 | upbeat, bittersweet | polished production, a catchy sung horn line, a melodic chorus that could cross over |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **Dancing your way through bad news** — the beat as defiance.
- **The working week, and the Friday-night release.**
- **A town that's falling apart, and the people who stay.**
- **Unity on the dance floor** — strangers in step.
- **The one who got away, skanking at someone else's wedding.**
- **Rude-boy pride** — dressed sharp with nowhere to be.
- **A friend who's lost the plot**, and the song that pulls them back.
- **Summer heat in the city** — the hydrant, the block party.
- **Growing up but refusing to grow old.**
- **A letter to the scene that raised you.**

### Sound & render

- **Genre line for the plan:** ska (plus the stance's sub-style: first-wave, 2 Tone, third-wave, rocksteady, ska-punk).
- **Vocal:** an energetic, characterful lead (cheeky or soulful, as the stance asks) with gang vocals and call-and-response from the band.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "drum machine", "synth horns", "trap beat", "autotune".
- **Stance exclusions:** rocksteady/dub add "fast tempo", "distorted guitar"; skate-ska/ska-punk add "slow tempo", "laid-back"; first-wave adds "modern production", "distortion".
- The horn section is a lead voice — give it a real instrumental intro or break chunk.

### Step 1 — Style Analysis

**Song structure:** Horn Intro → Verse 1 → Chorus → Horn Break → Verse 2 → Chorus → Bridge (breakdown or half-time) → Horn Solo → Final Chorus → Outro.

**Musical characteristics:** guitar and keys on the offbeat upstroke, a busy melodic bass, drums with a crisp backbeat (and a one-drop in slower stances), and a horn line as memorable as the vocal hook. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great ska hooks land — a horn riff you can sing, a chorus with a call-and-response, a title that's a phrase people shout, a bounce that makes standing still impossible. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; conversational, specific language; upbeat music carrying lyrics with a little bite; a chorus that contains the title.

**Lyrical style:** witty, street-level specifics, social observation without preaching, and joy as a statement.

**Chorus requirements:** contains the title; a call-and-response or gang-vocal hook; the most danceable part of the song. **Bridge:** a half-time breakdown or a change in perspective before the last chorus.

### Commercial goal

The song that turns a festival field into one bouncing crowd — completely original, horn-led, and impossible not to skank to.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Ska** | ABAB or AABB, medium rhyme strictness |
| Target duration | **3:00** (`music_length_ms` 180000) | **170–250 words** total (horn breaks carry runtime) |
| Tempo | **the chosen stance's band** (85–200 across the menu) | 6 lines per verse at mid-tempo, 4 at 140+ |
| Section caps | verse 4–8 · chorus 4–6 · bridge 2–4 | hard limits |

### Cover

A bold, graphic ska record sleeve: black-and-white checkerboard motifs, sharp-dressed figures mid-skank, a horn section silhouetted against a bright colour block — screen-print texture, high contrast. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` ska / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Ska Songs`

### Audience

A listener browsing a ska, punk, or party playlist. It should land cold — moving their feet by the first horn line.
