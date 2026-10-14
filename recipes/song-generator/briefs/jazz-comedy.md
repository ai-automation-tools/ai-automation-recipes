## The original outrageous jazz song

You are an award-winning comedy songwriter and jazz arranger — a student of the witty, risqué side of jazz, from novelty swing to the lounge-lizard act.

### Objective

Create a completely original **comedy vocal-jazz song** that sounds exactly like a polished jazz record — swinging band, sophisticated changes, a velvet vocal — while the lyrics are absurd, risqué, and laugh-out-loud. Lineage: Cab Calloway's jive, Louis Prima, Fats Waller's comic asides, Slim Gaillard's nonsense jazz, Dave Frishberg's wry songs, Bill Murray's lounge-singer sketch, Tom Lehrer at the piano, and the risqué "party record" tradition of the 1950s.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing — no standards, no contrafacts, no parodies of real songs. Synthesize an entirely new song.

### The era rotation — pick ONE per run (rotate against RECENT SONGS)

| Era | Tempo | Palette |
|---|---|---|
| **MODERN lounge swing (default, ~3 of 4 runs)** | 110–160 | a slick contemporary big-band or septet, walking bass, crisp ride swing, brass punctuating every punchline — a polished modern jazz record |
| **1940s jump & jive** | 160–200 | jumping horns, boogie piano, a call-and-response band chorus, a hepcat lead |
| **Velvet torch ballad** | 55–70 | piano trio with strings, a breathy rubato vocal — mock-heartbreak at its most sincere |

Record the chosen era in the frontmatter and the final JSON.

### The premise menu — pick ONE fresh angle per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **The lounge lizard's seduction that keeps failing:** a smooth crooner's pickup lines get worse, more specific, and more desperate every A section.
- **Jazz-cliché flip:** the smoky club, the martini, the cool cat — taken literally: the smoke is the kitchen on fire, the martini is warm, the cat is an actual cat who owns the band now.
- **The risqué swing number:** a strutting party record where every line is a filthy-but-deniable double-entendre about a trumpet player's embouchure, a slide trombone, or "keeping time."
- **The torch song for a lost object:** a devastating ballad of longing for a left-behind umbrella, a phone charger, or the last slice of pizza.
- **The jive explanation of modern life:** a hepcat narrator tries to explain cryptocurrency, smart fridges, or a QR-code menu in 1940s slang and gets it all wrong.
- **The bebop speed-ramble:** an impossibly fast patter song about a cascade of minor social disasters at a dinner party.
- **The pianist who hates the request:** a bitter, gorgeous ballad sung by the lounge pianist asked for the same song for the ninth time tonight.
- **The midlife jazz convert:** a man who discovered jazz last month and now explains it to everyone, at length, wrongly.

Pick one that hasn't run recently, then escalate it verse to verse until the bridge tops everything.

### Sound & render

- **Genre line for the plan:** vocal jazz in the chosen era — arranged and played completely straight, sophisticated harmony, real swing.
- **Vocal:** a velvet crooner or a sly jazz vocalist (any gender) delivering every absurdity with total suavity; a scat chorus can "comment" on the joke.
- 🎷 **Instrumental-leaning genre.** Keep **one full instrumental solo chunk (or two shorter ones) with empty `text`** — the band can answer a punchline with a horn stab, never with a sound effect. The word cap is lowered to match; never pad lyrics into a solo.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "programmed drums", "synth pads", "pop production", plus the comedy guards ("novelty kazoo", "comedy sound effects", "cartoon sound effects", "slide whistle").
- **Era exclusions:** modern adds "lo-fi", "thin mix"; jump & jive adds "strings", "bossa"; torch ballad adds "brass section", "fast swing".

### Step 1 — Style Analysis

**Comedic premises that work in jazz:** suavity applied to failure, Songbook wit pushed past decency, the jive narrator out of his era, and the gorgeous ballad about something absurd.

**Song structure:** Intro → A (set up the premise) → A (escalate) → B / bridge (the twist or a spoken aside) → A (the title punchline lands hardest) → instrumental solo → final A with a tag ending that repeats the punchline twice.

### Step 2 — Reverse-engineer the funny hook

Analyze (without copying) why witty jazz songs land — a title phrase that closes each A section and means something worse each time, dense internal rhyme, a bridge that pulls the rug, and a band that never cracks a smile. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original punchline title; escalating A sections; vivid modern specifics in a classic form; a tag ending that gets the last laugh.

**Lyrical style:** Songbook-clever internal rhyme, risqué filthy-but-deniable double-entendre, suave understatement, groan-great rhymes, a title that IS the joke.

### Commercial goal

The jazz number the whole room laughs at by the second A section and requests again by the encore — a real, swinging record that's also a perfect joke.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Comedy Vocal Jazz** | AABA, dense internal rhyme — the title closes each A as a punchline |
| Target duration | **3:00** (`music_length_ms` 180000) | **120–200 words** total — solos carry no words |
| Tempo | **the chosen era's band** (55–200) | A sections 4 lines; 2–4 at 180+ |
| Section caps | A section 4 · bridge 4 · tag 1–2 | spoken asides are exempt; solo chunks are wordless |

### Cover

A classic jazz-label cover played completely straight, of something absurd: a tuxedoed crooner serenading an empty room except for a cat, a martini glass on fire in a spotlight, a grand piano buried in request slips. Moody black-and-white with one bold accent colour. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` comedy vocal jazz / <era sub-style>
- extra fields: `era:` modern | jive | torch · `premise:` the comedic premise

### Album

`Comedy Jazz Songs`

### Audience

A listener browsing a jazz or comedy playlist. It should land cold — a swinging record that sounds like a classic and a punchline that makes them choke on their drink.
