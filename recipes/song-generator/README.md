<h1 align="center">🎵 Song</h1>

<p align="center">
  <em>An original song in the style you pick: lyrics, a composition plan, and the rendered MP3.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/needs-ELEVENLABS__API__KEY-F59E0B?style=for-the-badge" alt="Needs ELEVENLABS API KEY">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude writes the lyrics and an ElevenLabs composition plan that sings them, section by section.
The runner checks the plan, renders the MP3 with ElevenLabs Music, draws a square cover, and (with
ffmpeg) embeds the cover and tags. Every run spends music credits.

| | |
|:---|:---|
| **Output** | `songs/<YYYY-MM>/<date>_<slug>/` → `song.md`, `composition-plan.json`, `song.mp3`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, plus WebSearch and WebFetch for the `news` type only |
| **Skills** | `songwriting-craft`, `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | `ELEVENLABS_API_KEY` for the music; an image key for the cover (optional) |

## Types

`--type` picks a creative brief from [`briefs/`](briefs/), 37 in all:

- **news**, the default: researches the latest news and picks a modern genre to fit.
- **rock, hard-rock, punk, country-classic, psychedelic, rap, folk, blues, edm, hip-hop, indie,
  jazz, latin, metal, pop, reggae, rnb, ska, synthwave**.
- **Comedy twins** (`rock-comedy`, `folk-comedy` and so on, plus `punk-comedy` and `country`,
  which are comedy-first): adults-only humour under [shared rules](briefs/_comedy-rules.md). No
  minors, no slurs or punching down, no real people.

Add a type by dropping a brief with the same headings into `briefs/`. `--direction "..."` steers
the song toward a topic.

## What the runner checks

The song is rejected before any credits are spent if:

- the plan isn't a `chunks` list with lyrics, durations and style lists per chunk;
- the chunks don't add up to within 10% of the brief's target length (a short plan renders a short song);
- a sung line contains a digit (music models mangle them, so numbers are spelled out);
- the lyrics run over the brief's word cap (the runner recounts them).

## Sample

> **Every Stone I Set** — A dry-stone waller looks back on a life of building walls on the hill, until the first wall he ever built is the one holding him up.
>
> *First live pilot run, 2026-10-14 · `--type folk`, Opus · 3:00 MP3 from ElevenLabs Music*

## Run it

```bash
python recipes/song-generator/run.py --output-dir ~/ai-output --type folk
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../podcast-script-generator/README.md">Next: Podcast Script →</a>
</p>
