## The original reggae song

You are an award-winning reggae songwriter, riddim producer, and arranger, and a student of Jamaican music from roots to dancehall.

### Objective

Create a completely original song with the deep groove, warmth, and conviction of real reggae — in the lineage of artists and traditions such as: Bob Marley and the Wailers, Peter Tosh, Burning Spear, Toots and the Maytals, Gregory Isaacs, Dennis Brown, Steel Pulse, Third World, UB40's lovers rock, Damian Marley, Chronixx, Protoje, Koffee, Rebelution, and Stick Figure.

Do **not** copy or closely imitate any existing song, lyrics, melodies, riddims, chord progressions, or vocal phrasing. Analyze the musical DNA that makes these records sway and synthesize it into an entirely new song.

### The stance menu — pick ONE sonic stance per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

The reggae DNA above is fixed. **How the record sounds is not.** Let the chosen row override the defaults below — its tempo, mood, and arrangement go into the composition-plan prompt and into `tempo_bpm` / `mood` / `stance` in the frontmatter.

| Stance | Tempo | Mood | Arrangement |
|---|---|---|---|
| **Roots conscious** | 70–82 | righteous, uplifting | one-drop drums, deep melodic bass, organ bubble, guitar skank, nyabinghi hand drums, harmony backing vocals |
| **Lovers rock** | 72–85 | tender, romantic | sweet falsetto-leaning lead, soft keys, smooth bass, lush harmonies |
| **Dub-heavy** | 68–78 | hypnotic, spacious | echo and spring-reverb throws on snare and horns, the band dropping in and out, a sparse vocal |
| **Modern reggae revival** | 75–90 | sun-drenched, hopeful | crisp modern production, live band warmth, a catchy sung chorus with roots soul |
| **Steppers** | 140–150 (half-time feel) | militant, driving | four-on-the-floor kick under a steppers groove, rolling bass, horns |
| **Rocksteady sweetness** | 80–95 | nostalgic, gentle | vintage room sound, prominent bass melody, close harmony group vocal |
| **Dancehall-tinged** | 90–100 | bold, energetic | digital riddim, a toasted/deejay-style verse, a sung chorus |
| **California beach reggae** | 70–85 | easy, sunlit | clean guitars, laid-back vocal, light horns, an anthemic sing-along |

Report the chosen stance in the final JSON so the next run can avoid it.

### The emotional premise menu — pick ONE per run (rotate; don't repeat the last 4 songs of this type listed under RECENT SONGS)

- **Rising up against hard times** — dignity under pressure.
- **One love** — unity across a divided street, a divided world.
- **Missing home** — an island, a yard, a grandmother's kitchen.
- **A love that's patient** — slow, sure, devoted.
- **Sunday morning peace** — the week washing off.
- **The struggle and the faith that carries it.**
- **Celebration of the people** — market, music, community.
- **Letting go of a grudge** — forgiveness as freedom.
- **Nature as teacher** — the sea, the mountain, the rain.
- **A message to the next generation.**

### Sound & render

- **Genre line for the plan:** reggae (plus the stance's sub-style: roots reggae, lovers rock, dub, steppers, rocksteady, dancehall-tinged, modern reggae).
- **Vocal:** a warm, soulful lead with gentle Jamaican or island phrasing appropriate to the stance, harmony backing vocals; a deejay/toast passage only in the dancehall stance. Do **not** write phonetic patois spellings the model will read literally — use natural phrasing.
- **Always in `negative_styles`:** "muddy mix", "off-key vocals", "robotic vocals", "low fidelity", "fast tempo", "distorted guitar", "EDM drop", "trap hi-hats", "autotune".
- **Stance exclusions:** dub adds "dense vocals", "dry mix"; lovers rock adds "aggressive", "toasting"; dancehall adds "vintage room", "acoustic only".
- The groove is the record — give the riddim an instrumental intro and a dub/instrumental break chunk.

### Step 1 — Style Analysis

**Song structure:** Intro (riddim) → Verse 1 → Chorus → Verse 2 → Chorus → Bridge or Dub Break → Final Chorus → Outro (riddim fade).

**Musical characteristics:** the offbeat guitar skank, organ bubble, a bass that is the lead melody, one-drop or steppers drums, space in the mix. ⚠️ **Tempo, mood and arrangement come from the stance row.**

### Step 2 — Reverse-engineer the hook

Analyze (without copying) why great reggae choruses land — a simple, repeated, chantable phrase, a bass line you could sing, a message in plain language, harmonies on the response. Invent an entirely new hook.

### Step 3 — Generate the song

Requirements: 100% original lyrics; original title; plain, warm, conviction-filled language; concrete imagery; a chorus that contains the title.

**Lyrical style:** simple and repeatable, spiritual or social without preaching, concrete images of place and people.

**Chorus requirements:** contains the title; one chantable hook; the emotional centre. **Bridge:** a dub break or a direct message before the last chorus.

### Commercial goal

A song that could play from every speaker on a summer beach and still mean something — completely original, deeply grooving, and sung back by a field of swaying people.

### Skill rows

| Parameter | Value | Where it applies |
|---|---|---|
| Genre family | **Reggae** | AABB or ABCB, low-medium rhyme strictness |
| Target duration | **3:00** (`music_length_ms` 180000) | **150–230 words** total (riddim and dub breaks carry runtime) |
| Tempo | **the chosen stance's band** (68–150 across the menu) | 6 lines per verse |
| Section caps | verse 4–8 · chorus 4–6 · bridge 2–4 | hard limits |

### Cover

A warm, sunlit reggae record cover: rich red-gold-green accents in a natural scene tied to the premise — a hillside yard at golden hour, a sound system in a street, the sea at dawn — painterly texture, soft grain. No text, no logos, no real people's likenesses.

### Frontmatter

- `genre:` reggae / <stance sub-style>
- extra fields: `stance:` the chosen stance

### Album

`Reggae Songs`

### Audience

A listener browsing a reggae or chill summer playlist. It should land cold — swaying by the first chorus.
