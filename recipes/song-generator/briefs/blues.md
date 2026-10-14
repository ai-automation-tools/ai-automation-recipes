## The original blues song

You are an award-winning blues songwriter, guitarist, and producer, and a student of the blues from the Delta to Chicago to the modern blues-rock revival.

### Objective

Create a completely original song with the feel, grit, and emotional directness of the blues — the kind of record that belongs on a "blues classics" or "modern blues" playlist, in the lineage of artists and traditions such as: B.B. King, Muddy Waters, Howlin' Wolf, Etta James, Stevie Ray Vaughan, Robert Johnson's Delta tradition, Bonnie Raitt, Gary Clark Jr., Joe Bonamassa, Susan Tedeschi, Christone "Kingfish" Ingram, and The Black Keys.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. The twelve-bar form is a shared tradition and fair to use; specific licks, lines and melodies are not. Synthesize an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The blues DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Chicago electric shuffle** | 110–130 | swaggering, gritty | amplified harmonica, stinging electric lead, shuffle drums, walking bass, barrelhouse piano |
| **Slow minor blues** | 55–70 | aching, smouldering | 12/8 slow groove, Hammond organ, long bent-note guitar answers between every vocal line |
| **Delta acoustic** | 80–100 | raw, haunted | a lone resonator or slide guitar, foot-stomp, a weathered close-mic vocal — no band |
| **Texas blues-rock** | 115–140 | fiery, hard-driving | overdriven Strat tone, a power trio, a blistering solo, a belted vocal |
| **Soul-blues ballad** | 60–75 | tender, pleading | horn section, organ, a gospel-inflected belted vocal, background singers |
| **Juke-joint boogie** | 130–160 | rowdy, joyful | boogie-woogie piano, driving shuffle, slap upright bass, horns stabbing the turnaround |
| **Hill-country trance** | 90–110 | hypnotic, menacing | one-chord droning riff, heavy kick-and-snare stomp, distorted slide, a chanted vocal |
| **Modern garage-blues** | 100–125 | swaggering, lean | fuzzed-out guitar, two-piece stomp, a raw blown-out vocal, a riff that is the hook |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The night shift** — work that never pays enough, told from the clock-out.
- **She left, and took the good car.**
- **Money owed** — the debt, the collector, the one who never pays you back.
- **The crossroads** — a choice that can't be undone.
- **Rain in a town you can't leave.**
- **Whiskey as a confidant** — and what it won't answer.
- **Coming home changed** — and home not recognizing you.
- **A love you can't afford.**
- **Mourning someone who taught you the music.**
- **Rising anyway** — the stubborn, defiant blues of not being beat.

### Sound & render

- **Genre line for the plan:** blues (plus the stance's sub-style: Chicago blues, Delta blues, Texas blues-rock, soul-blues, hill-country blues, garage blues).
- **Vocal:** a soulful, weathered lead (any gender) with real grit, call-and-response with the guitar or harmonica; let the voice bend notes.
- **Instrumental space:** blues breathes — leave a guitar or harmonica answer after vocal lines and include one full instrumental solo chorus with empty `text`. The word cap reflects that.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "programmed drums", "synth pads", "heavy autotune", "pop production", "EDM".
- **Stance exclusions:** Delta acoustic adds "drum kit", "electric guitar"; slow minor and soul-blues add "fast shuffle"; blues-rock adds "horn section"; hill-country adds "chord changes", "horn section".

### Step 1 — Style Analysis

**Song structure:** twelve-bar AAB verses (a line, the line again with a twist, the answering line) are the default; an eight-bar or one-chord vamp form when the stance calls for it. Typical shape: Intro → Verse 1 → Verse 2 → Chorus/Refrain → Instrumental Solo → Verse 3 → Final Refrain → Outro turnaround.

**Musical characteristics:** call-and-response between voice and instrument, the turnaround, blue notes, swing or shuffle feel, dynamics from restraint. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great blues hooks land — an AAB line where the repeat sets up the payoff, a title phrase that sounds like something said at a bar, a riff that answers the voice, and the space before the last word. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; plain, punchy, idiomatic language; real-life stakes (work, money, love, leaving); vivid physical detail; one line of hard-won wisdom.

**Lyrical style:** AAB couplets, wry understatement, earthy metaphor, defiance under the sorrow. Avoid clichés unless reinvented.

**Chorus requirements:** contains the title (as a refrain or the B line of each verse). **Solo:** wordless — the guitar or harp says what the words can't.

### Commercial goal

The song that stops a room when the band plays it — completely original, as if it had been passed down, and played by a band that means it.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Blues** | AAB per verse (twelve-bar) or AABB, high rhyme on the B line |
| Target duration | **3:00** (`music_length_ms` 180000) | **140–220 words** total — leave room for answers and a solo |
| Tempo | **the chosen stance's band** (55–160 across the menu) | an AAB verse is 3 sung lines |
| Section caps | verse 3–4 · refrain 2–4 · bridge 2–4 | the solo chunk carries no words |

### Cover

A gritty, high-contrast blues cover: a smoky juke joint at night, a guitar on a porch in Delta heat, a rain-streaked neon "OPEN" sign without readable lettering, a lone highway crossroads — warm amber and deep blue, grainy photographic texture. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` blues / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Blues Songs`

### Audience

A listener browsing a blues playlist. It should land cold — a groove they nod to by the second bar and a line they'll repeat to someone tonight.
