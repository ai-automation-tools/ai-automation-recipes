## The original metal song

You are an award-winning metal songwriter, riff architect, and producer, and a student of five decades of heavy music — from the first doom records to modern metalcore.

### Objective

Create a completely original song with the weight, precision, and conviction of real metal — heavier and more riff-driven than the house's hard-rock type, built around the riff rather than the radio chorus — in the lineage of artists and traditions such as: Black Sabbath, Metallica, Iron Maiden, Judas Priest, Pantera, Megadeth, Mastodon, Gojira, Opeth, Lamb of God, Trivium, Killswitch Engage, Ghost, Sleep, Blind Guardian, and Dream Theater.

Do **not** copy or closely imitate any existing song, lyrics, riffs, melodies, chord progressions, or vocal phrasing. Analyze the musical DNA that makes these records crush and synthesize it into an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The metal DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Thrash assault** | 170–210 | furious, righteous | tight down-picked E-string riffs, gallop rhythms, a shouted-melodic vocal, a shredding solo over a tempo change |
| **Doom crawl** | 55–75 | crushing, mournful | down-tuned fuzz guitars, enormous slow riffs, cavernous drums, a chanted, haunted clean vocal |
| **Power-metal epic** | 150–180 | heroic, soaring | twin harmonized leads, double-kick, keyboard/orchestral swells, a high operatic clean vocal and a gang-choir chorus |
| **Progressive odyssey** | 90–140 (shifting) | cerebral, vast | odd-meter riffs, clean-to-heavy dynamic shifts, a mellotron or clean-guitar interlude, a long melodic solo |
| **Metalcore anthem** | 130–160 | cathartic, defiant | chugging breakdown riffs, a gritty shouted verse, a huge soaring clean chorus, one half-time breakdown |
| **Groove metal stomp** | 90–110 | menacing, swaggering | syncopated palm-muted grooves locked to the kick, pinch harmonics, a barked rhythmic vocal |
| **Gothic / occult rock-metal** | 100–125 | theatrical, sinister | organ, choir pads, crunchy mid-tempo riffs, a smooth, sly clean vocal — ritual, not rage |
| **Sludge / post-metal swell** | 60–90 | heavy, cathartic | long build from clean arpeggios to a wall of distortion, a sparse, roaring vocal, one massive repeated riff |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **Defiance against a crushing system** — the machine, the grind, the thing that wants you small.
- **A mythic battle** told as allegory — the dragon is the debt, the siege is the depression.
- **Grief turned to iron** — mourning someone by refusing to break.
- **The storm, the sea, the mountain** — nature as an overwhelming, indifferent force.
- **Addiction as a possessing demon** — and the exorcism.
- **The last stand** — outnumbered, holding the line anyway.
- **A cosmic horror** — something vast beneath the ice, told in second person.
- **Betrayal by a brother-in-arms.**
- **Rebirth from ashes** — burned down, rebuilt harder.
- **The ritual** — a gathering in the dark that is half menace, half celebration.

### Sound & render

- **Genre line for the plan:** heavy metal (plus the stance's sub-style: thrash, doom, power metal, progressive metal, metalcore, groove metal, gothic metal, sludge).
- **Vocal:** ⚠️ **harsh/screamed vocals render unreliably** — they often come back garbled or as noise. Prefer a powerful **clean or gritty** lead (belted, operatic, or a raw shouted-melodic grit); allow at most one short screamed line in a breakdown, and write it as a simple phrase that survives being mangled.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "thin guitars", "pop production", "drum machine", "autotune", "unintelligible vocals".
- **Stance exclusions:** doom/sludge add "fast tempo", "blast beats", "bright mix"; thrash/power add "slow tempo", "sludgy"; gothic adds "screaming", "breakdowns"; metalcore adds "orchestral", "operatic".
- Riff-forward — leave real instrumental room (a riff intro, a solo chunk) and keep the word count at the low end of the cap.

### Step 1 — Style Analysis

**Song structure:** Riff Intro → Verse 1 → Pre-Chorus → Chorus → Verse 2 → Pre-Chorus → Chorus → Bridge / Breakdown → Solo → Final Chorus → Riff Outro. Progressive and doom stances may stretch sections and drop the pre-chorus.

**Musical characteristics:** the riff is the hook; down-tuned or standard-tuned high-gain guitars, a locked-in bass, precise powerful drums (double-kick where the stance calls for it), and a vocal that sits on top of the wall rather than fighting it. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great metal hooks land — a riff that's instantly recognizable, a chorus that's a battle cry, a title that sounds like an album name, vowels a stadium can bellow, a tempo shift that makes the last chorus feel earned. Invent an entirely new riff-and-chorus pairing.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; vivid, mythic, or elemental imagery; conviction over cliché; a chorus that contains the title.

**Lyrical style:** strong verbs, concrete imagery (iron, fire, tide, stone) used with intent, allegory over literalism, short shoutable lines in the chorus. Avoid lazy "darkness/pain/fire" filler unless reinvented.

**Chorus requirements:** contains the title; one fist-raising hook; the most singable part of the song. **Bridge:** a breakdown, a tempo change, or a quiet interlude before the solo and final chorus.

### Commercial goal

A track that could open a festival set — completely original, crushing, and with a chorus the whole pit shouts back.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Metal** | ABAB or AABB, medium rhyme strictness — impact outranks rhyme |
| Target duration | **3:00** (`music_length_ms` 180000) | **150–230 words** total (riffs and solos carry runtime) |
| Tempo | **the chosen stance's band** (55–210 across the menu) | 6 lines per verse at mid-tempo, 4 at 140+ |
| Section caps | verse 4–8 · pre-chorus 2–4 · chorus 4–6 · bridge 2–4 | hard limits |

### Cover

Classic metal album art: a painted, epic, high-detail scene tied to the premise — a fortress in a storm, a colossal creature under ice, a ritual circle in a forest — dramatic chiaroscuro lighting, dark palette with one burning accent colour. No text, no band logos, no real people's likenesses.

### Frontmatter

- `genre:` heavy metal / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Metal Songs`

### Audience

A listener browsing a metal or rock playlist. It should land cold — a riff they're headbanging to before the first verse ends.
