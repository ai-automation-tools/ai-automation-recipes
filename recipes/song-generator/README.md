# Song

[← All recipes](../../README.md)

One original song per run, in the type you pick. Claude writes the lyrics and an ElevenLabs
composition plan that sings them, section by section; the runner checks the plan, renders the MP3
with ElevenLabs Music, embeds the cover and tags (with ffmpeg), and draws a square cover.

| | |
|:---|:---|
| **Output** | `songs/<YYYY-MM>/<date>_<slug>/` → `song.md`, `composition-plan.json`, `song.mp3`, `cover.png`, `artifact.json` |
| **Schedule** | Wednesdays, 18:00 UTC (the original was on-demand — each run spends music credits) |
| **Model** | `opus` |
| **Needs** | `ELEVENLABS_API_KEY` (music); an image key for the cover |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch (research is for the weekly type only) |
| **Skills** | `songwriting-craft`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Types

`--type` picks a creative brief from [`briefs/`](briefs/) — 37 of them:

- **weekly** — researches the week's news and picks a modern genre (the default).
- **rock, hard-rock, punk, country-classic, psychedelic, rap, folk, blues, edm, hip-hop, indie,
  jazz, latin, metal, pop, reggae, rnb, ska, synthwave**.
- **Comedy twins** (`rock-comedy`, `folk-comedy`, …, plus `punk-comedy` and `country`, which are
  comedy-first): adults-only, profane-but-deniable humour under [shared rules](briefs/_comedy-rules.md)
  — no minors, no slurs or punching down, no real people.

Add a type by dropping a brief with the same headings into `briefs/`.

## What the runner checks

The song is rejected, and no credits are spent, if:

- the plan isn't a `chunks` list with lyrics, durations and style lists per chunk;
- the chunks don't sum to within 10% of the brief's target length (a short plan renders a short song);
- a sung line contains a digit (music models mangle them — spell numbers out);
- the lyrics are over the brief's word cap (the runner recounts them).

`--direction "..."` steers the song toward a topic.

## Sample

> **Every Stone I Set** — A dry-stone waller looks back on a life of building walls on the hill, until the first wall he ever built is the one holding him up.
>
> *First live pilot run, 2026-10-14 · `--type folk`, Opus · 3:00 MP3 from ElevenLabs Music*

## Run it

```bash
python recipes/song-generator/run.py --output-dir ~/ai-output --type folk
```
