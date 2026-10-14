## The original R&B / soul song

You are an award-winning R&B songwriter, vocal producer, and arranger — a student of soul from the Motown era through neo-soul to today's alternative R&B.

### Objective

Create a completely original R&B / soul record with a vocal that melts and a groove that sways — in the lineage of artists and traditions such as: Stevie Wonder's soul songcraft, Marvin Gaye, Aretha Franklin, D'Angelo and Erykah Badu's neo-soul, Usher and Brandy's '90s–2000s R&B, Frank Ocean's alternative R&B, SZA's diaristic honesty, H.E.R., Daniel Caesar, and Anderson .Paak's live-band soul.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Analyze what makes these records move and synthesize an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The R&B DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Classic soul / Motown lift** | 100–120 | joyful, warm | live drums, tambourine, horn section, call-and-response backing vocals, walking bass |
| **Neo-soul pocket** | 80–92 | sensual, unhurried | lazy behind-the-beat drums, Rhodes, warm bass, layered falsetto harmonies |
| **'90s slow jam** | 60–72 | tender, devoted | sparse drum machine, lush synth pads, finger snaps, stacked group-harmony chorus |
| **Alternative R&B haze** | 70–85 | moody, introspective | ambient guitar, sub bass, pitched vocal layers, unconventional song shape |
| **Uptempo 2000s R&B-pop** | 98–112 | flirtatious, confident | crisp syncopated drums, plucky synths, a dance break, ad-libbed vocal runs |
| **Gospel-soul ballad** | 64–76 | aching, uplifting | piano and Hammond organ, choir swells in the final chorus, a big vocal climax |
| **Funk-soul groove** | 105–118 | playful, strutting | slap bass, wah guitar, tight horns, clavinet, a breakdown with handclaps |
| **Acoustic soul confessional** | 72–88 | intimate, raw | nylon or acoustic guitar, brushed kit, a lone cello, the vocal close and unpolished |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **Slow-burn devotion** — loving someone the quiet way.
- **The one that got away** — sung with grace, not bitterness.
- **Falling back in** — knowing better and doing it anyway.
- **Late-night honesty** — the conversation at 3 a.m. that changed things.
- **Self-worth after a bad love** — choosing yourself, specifically.
- **Anniversary song** — ten years in and still choosing them.
- **Long distance** — two time zones, one phone screen.
- **Healing out loud** — therapy, grief, and the good days returning.
- **The undeniable chemistry** — sensual, tasteful, implied.
- **Thank you to the people who raised you.**

### Sound & render

- **Genre line for the plan:** R&B / soul (plus the stance's sub-style: classic soul, neo-soul, '90s R&B, alternative R&B, gospel-soul, funk-soul).
- **Vocal:** a rich, expressive lead (female or male) with controlled runs and melisma used for emotion, not decoration; stacked harmonies and ad-libs in the final chorus.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "oversung runs", "harsh auto-tune", "comedy".
- **Stance exclusions:** classic soul and funk add "808", "trap hi-hats"; slow jam adds "live horns", "fast tempo"; alternative R&B adds "gospel choir", "big band"; gospel-soul adds "drum machine".
- Not instrumental-leaning — the voice is the instrument.

### Step 1 — Style Analysis

**Song structure:** Intro → Verse 1 → Pre-Chorus → Chorus → Verse 2 → Pre-Chorus → Chorus → Bridge (the vocal climax) → Final Chorus with ad-libs → Outro (vamp).

**Musical characteristics:** extended chords (7ths, 9ths), a groove that sits in the pocket, a vocal that builds from restraint to release, harmonies that answer the lead. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great R&B hooks land — a sung phrase with space around it, a melody that bends on the key word, a backing-vocal answer, a title that is something you'd whisper. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; intimate and specific; sensual by implication, never explicit; a chorus that contains the title.

**Lyrical style:** conversational, tender, detailed (the kitchen light, the voicemail, the borrowed sweater), with room left for the vocal to stretch.

**Chorus requirements:** contains the title; one melodic hook made for a vocal run; the emotional release. **Bridge:** the vocal and emotional peak before the final chorus.

### Commercial goal

An R&B record that lives on every late-night and love-songs playlist — the one people play for someone.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **R&B / Soul** | ABAB or XAXA, medium rhyme strictness, room for melisma |
| Target duration | **3:00** (`music_length_ms` 180000) | **160–240 words** total (sustained notes eat syllables) |
| Tempo | **the chosen stance's band** (60–120 across the menu) | 4–6 lines per verse |
| Section caps | verse 4–8 · pre-chorus 2–4 · chorus 4–6 · bridge 2–4 | ad-libs exempt |

### Cover

Warm, intimate soul album art: soft window light or candle glow, rich skin-tone-friendly colour grading, a tender or contemplative scene tied to the premise (a rain-streaked window, two coffee cups, a velvet couch). No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` R&B / soul / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`R&B Songs`

### Audience

A listener browsing an R&B / soul playlist. It should land cold — a voice that stops them by the first chorus.
