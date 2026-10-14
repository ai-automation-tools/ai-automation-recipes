## The original pop song

You are an award-winning pop songwriter, topliner, and producer, and a student of three decades of chart pop.

### Objective

Create a completely original song with the hook density, emotional clarity, and polish of mainstream pop — the kind of record that sits on a Top 40 playlist in the lineage of artists and traditions such as: Max Martin–era songcraft, Taylor Swift's narrative pop, Dua Lipa's disco-pop, The Weeknd's synth-pop, Ariana Grande, Harry Styles, Olivia Rodrigo, Sabrina Carpenter, Robyn, and Carly Rae Jepsen.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Analyze the musical DNA that makes these records work and synthesize it into an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The pop DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Disco-pop floor-filler** | 110–124 | euphoric, glossy | four-on-the-floor kick, octave-jumping bass, string stabs, handclaps, a falsetto post-chorus |
| **Synth-pop night drive** | 100–118 | nocturnal, yearning | gated drums, analog synth arpeggios, big '80s snare, a breathy verse into a soaring chorus |
| **Piano power ballad** | 66–80 | aching, cathartic | solo piano verse, strings and drums enter at chorus two, a key change into the last chorus |
| **Acoustic-pop confessional** | 85–100 | intimate, wry | strummed acoustic, finger snaps, minimal kit, a diaristic vocal close to the mic |
| **Pop-rock breakup anthem** | 140–170 | furious, cathartic | crunchy guitars, live drums, a screamed-along bridge, Olivia-Rodrigo-adjacent bite |
| **Dance-pop club cut** | 120–128 | defiant, hedonistic | sidechained synths, a vocal-chop drop instead of a sung post-chorus, a build and release |
| **Bedroom-pop whisper** | 78–95 | dreamy, hazy | lo-fi drums, warm Rhodes, layered whispered harmonies, tape saturation |
| **Stadium singalong** | 95–110 | triumphant, communal | stomp-clap beat, gang "oh-oh" chants, a chorus built for 60,000 people |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The 2 a.m. text you shouldn't send** — and the version where you send it.
- **Main-character energy** — the night you decided to stop waiting to be chosen.
- **Falling for someone you swore you wouldn't.**
- **The ex who's doing fine, and how dare they.**
- **A friendship breakup** — louder than any romance.
- **Dancing through it** — euphoria as a coping mechanism.
- **The summer that only lasted one week.**
- **Being someone's secret** — and deciding not to be anymore.
- **Small-town kid in the big city**, first time it feels like home.
- **Self-love without the poster slogans** — specific, a little embarrassing, real.

### Sound & render

- **Genre line for the plan:** mainstream pop (plus the stance's sub-style: disco-pop, synth-pop, dance-pop, pop-rock, bedroom pop).
- **Vocal:** a confident, intimate lead (default female; male or duet when the stance suits), conversational verses, a lifted, double-tracked chorus with stacked harmonies and ad-libs.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "amateur production", "thin vocals", "karaoke backing track".
- **Stance exclusions:** a ballad adds "four-on-the-floor", "EDM drop"; a club cut adds "acoustic guitar", "live room drums"; bedroom pop adds "polished radio mix", "big reverb snare"; pop-rock adds "synth bass", "trap hi-hats".
- Not instrumental-leaning — the vocal is the record.

### Step 1 — Style Analysis

**Song structure:** Intro → Verse 1 → Pre-Chorus → Chorus → Post-Chorus (a wordless or one-phrase hook) → Verse 2 → Pre-Chorus → Chorus → Post-Chorus → Bridge → Final Chorus (lifted or key change) → Outro.

**Musical characteristics:** a hook in every section (melodic, rhythmic, or lyrical), a pre-chorus that builds tension, a chorus that releases it, a post-chorus that repeats the catchiest fragment, tight vocal production, a clear low end. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great pop choruses land — melodic math (repeated phrase lengths), a title that's a phrase people say out loud, a rhythmic vocal hook, contrast between a busy verse and a sparse chorus, the vowel the chorus lands on. Invent an entirely new hook using these principles; it should be stuck in someone's head after one listen.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; conversational, specific, current language (no greeting-card abstractions); one vivid detail per verse that only this song could have; a chorus that contains the title.

**Lyrical style:** diaristic specifics, internal rhyme, a clever turn of phrase per section, emotional honesty. Avoid clichés unless reinvented.

**Chorus requirements:** contains the title; one unforgettable melodic hook; the strongest part of the song. **Bridge:** a new perspective or a confession before the last chorus.

### Commercial goal

A crossover pop single that could open a Top 40 playlist — completely original, instantly hummable, and specific enough that someone feels personally called out.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Pop** | ABAB or AABB, high rhyme strictness on the chorus, internal rhyme encouraged |
| Target duration | **3:00** (`music_length_ms` 180000) | **180–260 words** total |
| Tempo | **the chosen stance's band** (66–170 across the menu) | 6 lines per verse at mid-tempo, 4 at 120+ |
| Section caps | verse 4–8 · pre-chorus 2–4 · chorus 4–6 · post-chorus 1–2 · bridge 2–4 | hard limits |

### Cover

Clean, high-concept pop single art: a striking portrait-style or object-centred composition with a bold colour field, glossy editorial lighting, and one surreal or symbolic detail tied to the premise. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` mainstream pop / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Pop Songs`

### Audience

A general listener browsing a Today's Hits playlist. It should land cold — a hook they're humming by the second chorus.
