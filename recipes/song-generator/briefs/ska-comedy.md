## The original outrageous ska song

You are an award-winning comedy songwriter, horn arranger, and producer — a student of ska's long, proud history of not taking itself seriously.

### Objective

Create a completely original **comedy ska song** that sounds like a genuinely great horn-driven record while the lyrics are absurd, filthy, and laugh-out-loud — in the lineage of traditions such as: Reel Big Fish, Less Than Jake, Mustard Plug, Madness's daftest singles, The Aquabats, Goldfinger's sillier cuts, Save Ferris, and the novelty side of '90s third wave.

Do **not** copy or closely imitate any existing song, lyrics, melodies, horn lines, chord progressions, or vocal phrasing — no parodies of real songs. Analyze the comedic musical DNA and synthesize an entirely new song.

### The era rotation — pick ONE per run (rotate against RECENT SONGS)

| Era | Tempo | Palette |
|---|---|---|
| **MODERN third-wave (default, ~3 of 4 runs)** | 150–190 | punk-speed verses into upstroke skank, a tight horn section blasting the hook, gang-vocal chorus, a half-time breakdown — indistinguishable from a real third-wave single |
| **2 Tone throwback** | 140–160 | choppy guitar, organ skank, nervy clipped vocal, a sharp-suited British bounce |
| **Rocksteady croon** | 85–100 | slow, sweet, soulful — a love-song groove applied with total sincerity to something ridiculous |

Record the chosen era in the frontmatter and the final JSON.

### The premise menu — pick ONE fresh angle per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The upbeat bop about a total catastrophe:** sunny horns, cheerful skank, lyrics about a flooded basement, a repo man, or the worst first date in history.
- **Ska-cliché flip:** the checkered Vans, the pork-pie hat, the trombone player nobody invited — the scene's own costumes taken literally.
- **The tall-tale sex brag as a horn-section brag:** cartoonish bravado where every line is about "my brass," "my slide," "my rhythm section" — filthy-but-deniable, never clinical.
- **The aging ska kid:** still skanking at forty with a bad knee, a mortgage, and a pork-pie hat that no longer fits.
- **The petty kiss-off party anthem:** she left, so he's throwing a horn-driven celebration with oddly specific grievances.
- **Day-job disaster:** the most mundane job in the world told as a high-energy skank — the DMV, the deli counter, the inventory audit.
- **The rude-boy who isn't:** swagger anthem from a narrator who is plainly not cool at all.
- **Party gone sideways:** a "hold my beer" house-party escalation ending in the fire department, a raccoon, and a trombone in the pool.

Pick one that hasn't run recently, then escalate it verse to verse until the bridge tops everything.

### Sound & render

- **Genre line for the plan:** ska in the chosen era — produced and played completely straight, tight and brassy.
- **Vocal:** a cheeky, energetic lead with gang vocals and call-and-response; spoken asides allowed in the breakdown.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "drum machine", "synth horns", plus the comedy guards from the comedy rules.
- **Era exclusions:** MODERN adds "slow tempo", "vintage room"; 2 Tone adds "distorted guitar", "modern pop production"; rocksteady adds "fast tempo", "distortion".

### Step 1 — Style Analysis

**Comedic premises that work in ska:** sunny music under disastrous lyrics, the scene's own clichés, the brag that collapses, and the party that escalates into chaos.

**Song structure:** Horn Intro → Verse 1 (set up the premise) → Chorus (the title punchline) → Horn Break → Verse 2 (escalate) → Chorus → Bridge / Breakdown (the turn — spoken confession or reveal) → Horn Solo → Final Chorus (biggest laugh) → Outro.

### Step 2 — Reverse-engineer the funny hook

Analyze (without copying) why the funniest ska songs land — a horn riff so catchy it makes a stupid chorus irresistible, a gang-shout punchline, the gap between joyful music and disastrous words, a groan-great rhyme on the upbeat. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original punchline title; specific and vivid; escalating; a chorus built to be shouted back.

**Lyrical style:** fast, wordy, cheeky specifics, filthy-but-deniable double-entendre, groan-great rhymes, a title that IS the joke.

### Commercial goal

The comedy ska anthem that turns every pit into a skank circle and every crowd into a choir of people shouting something deeply stupid.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Comedy Ska** | AABB or ABAB — setup/payoff couplets |
| Target duration | **3:00** (`music_length_ms` 180000) | **170–250 words** total |
| Tempo | **the chosen era's band** (85–190) | 6 lines per verse at mid-tempo, 4 at 140+ |
| Section caps | verse 4–8 · chorus 4–6 · bridge 2–4 | gang shouts and spoken asides are exempt |

### Cover

A bold checkerboard ska sleeve that is obviously a joke: a sharp-dressed figure mid-skank in front of the premise's disaster (a burning barbecue, a raccoon holding a trombone) — screen-print texture, high-contrast colour blocks, played straight. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` comedy ska / <era sub-style>
- extra fields: `era:` modern | 2tone | rocksteady · `premise:` the comedic premise

### Album

`Comedy Ska Songs`

### Audience

A listener browsing a ska, punk, or comedy playlist. It should land cold — skanking and laughing by the first chorus.
