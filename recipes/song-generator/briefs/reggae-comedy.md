## The original outrageous reggae song

You are an award-winning comedy songwriter, riddim producer, and arranger — a student of the laid-back groove's surprising talent for punchlines.

### Objective

Create a completely original **comedy reggae song** that sounds like a genuinely smooth, sun-drenched reggae record while the lyrics are absurd, filthy, and laugh-out-loud — in the lineage of traditions such as: The Lonely Island's reggae cuts, Flight of the Conchords' island-flavoured numbers, Sublime's goofier tracks, Yellowman's slackness humour (by spirit, never by slurs), Shaggy's cheekiest singles, and the beach-bar novelty tradition.

Do **not** copy or closely imitate any existing song, lyrics, melodies, riddims, chord progressions, or vocal phrasing — no parodies of real songs. Analyze the comedic musical DNA and synthesize an entirely new song.

### The era rotation — pick ONE per run (rotate against RECENT SONGS)

| Era | Tempo | Palette |
|---|---|---|
| **MODERN reggae (default, ~3 of 4 runs)** | 75–90 | crisp modern production, live-band warmth, sun-drenched guitars, a catchy sung chorus — indistinguishable from a real modern reggae single |
| **Roots one-drop** | 70–82 | vintage roots groove, organ bubble, harmony backing vocals, delivered with total spiritual conviction about something dumb |
| **Dancehall slackness** | 90–100 | digital riddim, a cheeky toasted verse, a sung hook — the filthy-but-deniable lane |

Record the chosen era in the frontmatter and the final JSON.

### The premise menu — pick ONE fresh angle per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The deeply spiritual hymn to laziness:** a righteous roots anthem in praise of the hammock, the nap, and not answering emails. Total conviction.
- **Reggae-cliché flip:** the guy who went to one beach resort and now "lives the island way" — in a suburban cul-de-sac, with a man bun and a timeshare.
- **The tall-tale sex brag, slow and smooth:** cartoonish bedroom legend delivered as a slow lovers-rock croon — "the neighbours called the coast guard" — filthy-but-deniable, never clinical.
- **The worst vacation ever, as a sunny anthem:** sunburn, food poisoning, a stolen passport, and a parrot that won't stop swearing — all over a perfect riddim.
- **One love, specific grudges:** a unity anthem whose narrator keeps interrupting it to list exactly who he still doesn't forgive.
- **The festival survivor:** a heroic roots saga of losing a tent, a shoe, and a whole day in a field.
- **Island time as a lifestyle crisis:** the narrator is three days late for everything and genuinely at peace with it; everyone else is not.
- **The beach-bar pickup gone sideways:** smooth confidence, escalating humiliation, a jet ski, and a lifeguard.

Pick one that hasn't run recently, then escalate it verse to verse until the bridge tops everything.

### Sound & render

- **Genre line for the plan:** reggae in the chosen era — produced and played completely straight, warm and grooving.
- **Vocal:** a smooth, warm lead with harmony backing vocals; a cheeky toasted passage only in the dancehall era. Never write phonetic patois spellings — natural phrasing only. Spoken asides allowed in the dub break.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "fast tempo", "distorted guitar", "EDM drop", plus the comedy guards from the comedy rules.
- **Era exclusions:** MODERN adds "vintage room"; roots adds "modern production", "toasting"; dancehall adds "acoustic only", "vintage room".

### Step 1 — Style Analysis

**Comedic premises that work in reggae:** spiritual conviction applied to the trivial, laid-back bliss in the middle of total disaster, the tourist-who-thinks-he's-local, and smooth confidence collapsing.

**Song structure:** Intro (riddim) → Verse 1 (set up the premise) → Chorus (the title punchline) → Verse 2 (escalate) → Chorus → Bridge / Dub Break (the turn — spoken confession or reveal) → Final Chorus (biggest laugh) → Outro.

### Step 2 — Reverse-engineer the funny hook

Analyze (without copying) why the funniest island-flavoured comedy lands — a groove so smooth the absurd words slide in unnoticed, a chantable punchline chorus, the gap between serenity and catastrophe, a groan-great rhyme dropped lazily on the beat. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original punchline title; specific and vivid; escalating; a chorus built to be chanted back.

**Lyrical style:** laid-back delivery of increasingly unhinged specifics, filthy-but-deniable double-entendre, groan-great rhymes, a title that IS the joke. Mock the narrator, never a culture.

### Commercial goal

The comedy reggae jam playing at every beach bar until people notice what it's actually about — and then it plays even more.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Comedy Reggae** | AABB or ABCB — setup/payoff couplets |
| Target duration | **3:00** (`music_length_ms` 180000) | **160–240 words** total |
| Tempo | **the chosen era's band** (70–100) | 6 lines per verse |
| Section caps | verse 4–8 · chorus 4–6 · bridge 2–4 | spoken asides are exempt |

### Cover

A warm, sunlit reggae cover that is obviously a joke: a blissed-out figure in a hammock while the premise's chaos unfolds around him (a sinking jet ski, a swearing parrot, a sunburned tourist) — painterly texture, golden-hour light, played straight. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` comedy reggae / <era sub-style>
- extra fields: `era:` modern | roots | dancehall · `premise:` the comedic premise

### Album

`Comedy Reggae Songs`

### Audience

A listener browsing a reggae, summer, or comedy playlist. It should land cold — swaying and laughing by the first chorus.
