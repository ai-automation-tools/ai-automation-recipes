## The original jazz song

You are an award-winning jazz composer, lyricist, and arranger, and a student of vocal jazz from the Great American Songbook era to the modern jazz-soul crossover.

### Objective

Create a completely original **vocal jazz** song with the harmonic sophistication, swing, and wit of the jazz tradition — the kind of record that belongs on a "jazz vocals" or late-night lounge playlist, in the lineage of artists and traditions such as: Ella Fitzgerald, Billie Holiday, Frank Sinatra, Nina Simone, Chet Baker, Sarah Vaughan, Nat King Cole, Diana Krall, Norah Jones, Gregory Porter, Esperanza Spalding, and Samara Joy.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing — no standards, no contrafacts of real tunes. Synthesize an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The jazz DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Swinging big band** | 130–170 | brassy, buoyant | full brass and sax sections, walking bass, ride-cymbal swing, shout chorus |
| **Late-night piano trio ballad** | 55–70 | intimate, smoky | piano, upright bass, brushes, a close, behind-the-beat vocal |
| **Bossa nova** | 120–140 | breezy, wistful | nylon-string guitar, soft bossa groove, flute or muted trumpet, a hushed vocal |
| **Cool jazz** | 90–115 | restrained, wry | muted trumpet, vibraphone, light swing, a dry, conversational vocal |
| **Torch song with strings** | 60–75 | heartbroken, lush | string section, harp, slow rubato verse into a tempo chorus |
| **Bebop-flavoured up-tempo** | 180–220 | dazzling, playful | fast walking bass, crisp ride, tenor sax, scat-friendly lines, quick chord changes |
| **Jazz-soul crossover** | 85–100 | warm, grooving | Rhodes, a soulful backbeat, a horn pad, a rich baritone or alto lead |
| **Gypsy-jazz swing** | 150–190 | sparkling, mischievous | acoustic rhythm guitars with la pompe strum, violin, upright bass — no drums |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The last table at closing time** — two strangers, one candle.
- **A city at night** — told as a love letter.
- **A love affair that only ever happens on weekends.**
- **The one who got away, toasted without regret.**
- **Rain on the window and nowhere to be.**
- **An old lover across a crowded room.**
- **Playing it cool** — while absolutely not being cool.
- **The joy of a Tuesday that went right.**
- **A goodbye said with a joke.**
- **Falling in love with the band, not the singer.**

### Sound & render

- **Genre line for the plan:** vocal jazz (plus the stance's sub-style: swing, big band, bossa nova, cool jazz, jazz ballad, bebop, jazz-soul, gypsy jazz).
- **Vocal:** a supple, characterful jazz vocal (any gender) with phrasing behind or ahead of the beat; scat is welcome in one chorus.
- 🎷 **Instrumental-leaning genre.** A jazz record lives in its solos: build the plan with **one full instrumental solo chunk (or two shorter ones) with empty `text`**, and keep every solo lyric-free. The word cap in Skill rows is lowered to match — never pad lyrics into a solo.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "programmed drums", "synth pads", "distorted guitar", "heavy autotune", "pop production", "EDM".
- **Stance exclusions:** piano trio and torch song add "brass section"; bossa adds "swing ride", "brass section"; gypsy jazz adds "drum kit", "piano"; jazz-soul adds "walking bass".

### Step 1 — Style Analysis

**Song structure:** the classic AABA 32-bar form (or verse-and-chorus for jazz-soul): Intro → A → A → B (bridge) → A → instrumental solo(s) → B → final A with a tag ending.

**Musical characteristics:** extended harmony (sevenths, ninths, ii–V–I movement, a modulating bridge), swing or Latin feel, a melody that rewards a great singer, and an arrangement that leaves the soloist room. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great jazz songs land — a witty title phrase that resolves the A section, internal rhyme, a bridge that changes the angle, a tag ending that repeats the last line twice. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; sophisticated, witty, conversational language; internal rhyme; one image per section; an ending tag.

**Lyrical style:** Songbook wit — clever internal rhyme, understatement, urbane metaphor, warmth under the cool. Avoid clichés unless reinvented.

**Chorus / A-section requirements:** each A section ends on the title. **Bridge (B):** a change of key, angle, or tense.

### Commercial goal

The song a great singer adds to their set and a listener assumes is a lost standard — completely original, timeless, and impossible to play without someone swaying.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Vocal Jazz** | AABA, high internal-rhyme density, the title closes each A |
| Target duration | **3:00** (`music_length_ms` 180000) | **120–200 words** total — solos carry no words |
| Tempo | **the chosen stance's band** (55–220 across the menu) | A sections 4 lines; 2–4 at 180+ |
| Section caps | A section 4 · bridge 4 · tag 1–2 | solo chunks are wordless |

### Cover

A classic jazz-label cover: bold modernist typography-free graphic design or a moody black-and-white photo — a saxophone on a chair under a spotlight, a smoky club booth, a rain-slick city street at night — with one strong accent colour. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` vocal jazz / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Jazz Songs`

### Audience

A listener browsing a jazz vocals or late-night lounge playlist. It should land cold — a melody that sounds like it's been around forever and a line that makes them smile.
