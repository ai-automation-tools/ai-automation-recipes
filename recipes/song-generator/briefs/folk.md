## The original folk song

You are an award-winning folk songwriter and producer, and a student of the folk tradition from the 1960s revival to modern indie-folk.

### Objective

Create a completely original song with the storytelling, plainspoken honesty, and acoustic warmth of folk — the kind of record that belongs on a "folk & acoustic" playlist, in the lineage of artists and traditions such as: Joni Mitchell, Simon & Garfunkel, Nick Drake, Joan Baez, Fleet Foxes, Bon Iver, Iron & Wine, Gregory Alan Isakov, Mumford & Sons, The Lumineers, Brandi Carlile, and Gillian Welch.

This is **not** the house's serious country type (that one covers honky-tonk, outlaw, and the Americana storyteller with steel and fiddle). Folk here means acoustic songcraft without the country signifiers — no pedal steel, no Telecaster twang, no drawl.

Do **not** copy or closely imitate any existing song, lyrics, melodies, chord progressions, or vocal phrasing. Analyze the musical DNA that makes these records work and synthesize it into an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The folk DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Laurel Canyon singer-songwriter** | 80–100 | warm, confessional | open-tuned acoustic, light hand percussion, a melodic upright or fretless bass, a supple lead vocal |
| **Fingerpicked chamber folk** | 65–85 | hushed, autumnal | intricate fingerpicked guitar, a string quartet, a breathy close vocal — no drum kit |
| **Indie-folk stomp** | 110–130 | rousing, communal | kick-drum stomp, banjo and acoustic strumming, gang "hey!" vocals, a big singalong refrain |
| **Cabin-reverb falsetto** | 70–90 | lonely, wintry | layered falsetto harmonies, sparse guitar, a church-hall reverb, a slow-blooming swell |
| **Protest / topical folk** | 95–115 | resolute, plainspoken | one acoustic guitar and harmonica, a clear forward vocal, verses that tell, a chorus that stands |
| **Celtic-tinged folk** | 100–120 | wistful, lilting | fiddle and tin whistle, bodhrán, a 6/8 lilt option, a modal melody |
| **Old-time murder ballad** | 70–90 | dark, spare | a lone banjo or guitar, a stark unaccompanied verse, a cold close harmony — no drums |
| **Duo-harmony coffeehouse** | 85–105 | tender, intimate | two acoustic guitars, two voices in tight close harmony, almost nothing else |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **A river or a road** — the one thing that stayed while the town changed.
- **A letter never sent** — read aloud, verse by verse.
- **The last winter in a family house.**
- **Leaving the city for somewhere quiet** — and what you lost by doing it.
- **A working life** — one trade, one pair of hands, told plainly.
- **A long marriage, in four seasons.**
- **An old-world story, newly told** — a sailor, a lighthouse, a lost child found.
- **Grief that arrives as weather.**
- **A small injustice witnessed and remembered.**
- **The stars over a place you grew up** — the only map you trust.

### Sound & render

- **Genre line for the plan:** folk / acoustic (plus the stance's sub-style: indie folk, chamber folk, Celtic folk, old-time folk).
- **Vocal:** a natural, unprocessed lead (any gender), clear diction so every story line lands; harmonies when the stance asks.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "pedal steel", "country twang", "electric guitar solo", "synth pads", "programmed drums", "heavy autotune".
- **Stance exclusions:** chamber, murder-ballad and duo stances add "drum kit"; the stomp adds "string quartet"; Celtic adds "banjo"; protest folk adds "full band".
- Not instrumental-leaning — the story is the record, though a short instrumental verse is welcome.

### Step 1 — Style Analysis

**Song structure:** Verse 1 → Chorus/Refrain → Verse 2 → Chorus → Verse 3 (or Bridge) → Final Chorus → Outro. Verses carry the story and may run long; the refrain can be a single recurring line.

**Musical characteristics:** acoustic instruments in a real room, melodies singable by anyone, modal or open-tuning colour, dynamics from adding voices rather than volume. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great folk refrains land — a plain phrase that gathers weight each time it returns, a melody that sounds older than it is, a refrain that means something different after verse three. Invent an entirely new refrain.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; a clear story with a beginning, middle, and turn; concrete images from the natural or working world; plain words chosen exactly.

**Lyrical style:** narrative, imagistic, unadorned, occasional archaic or regional colour used lightly. Avoid clichés unless they're the song's deliberate ballad formulas.

**Chorus requirements:** contains the title; simple enough to sing on the second hearing; deepens with each return. **Bridge / Verse 3:** the turn in the story.

### Commercial goal

The song played at a wedding, a funeral, and a campfire in the same year — completely original, and sounding like it has always existed.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Folk / Acoustic** | ABCB or AABB, moderate rhyme strictness — story outranks rhyme |
| Target duration | **3:00** (`music_length_ms` 180000) | **180–260 words** total |
| Tempo | **the chosen stance's band** (65–130 across the menu) | 6–8 lines per verse at slow tempo, 4–6 at 110+ |
| Section caps | verse 4–8 · chorus 2–6 · bridge 2–4 | storytelling verses may use the full 8 |

### Cover

A painterly or woodcut-style folk cover: a landscape, a weathered object, or a lone figure tied to the premise (a river at dusk, a lit window in snow, a boat pulled up on shingle), earthy palette, hand-made texture. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` folk / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Folk Songs`

### Audience

A listener browsing a folk & acoustic playlist. It should land cold — a story they follow to the end and a refrain they find themselves humming.
