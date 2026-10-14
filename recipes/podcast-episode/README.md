<h1 align="center">🎧 Podcast Episode</h1>

<p align="center">
  <em>The oldest unrendered podcast script, voiced with preset voices into one MP3.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_ELEVENLABS_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or ELEVENLABS key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

It picks up the oldest [podcast script](../podcast-script-generator/README.md) that has no episode
yet. Claude casts a preset voice for every speaker, distinct while there are enough to go round,
adds a short delivery note for each, and writes show notes. The runner speaks every line with
text-to-speech and joins them into one track.

| | |
|:---|:---|
| **Output** | `podcasts/<YYYY-MM>/<date>_<slug>/` → `episode.md`, `episode.mp3` (WAV without ffmpeg), `script.md`, `cover.png` (the script's), `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `humanizer` |
| **Needs** | `GEMINI_API_KEY` for Gemini TTS (the default), or `ELEVENLABS_API_KEY` with `--speech-engine elevenlabs` |

Preset voices only: Gemini's 30 prebuilt voices (Kore, Puck, Charon and the rest) or ElevenLabs'
premade Rachel, Adam, Antoni, Bella, Josh and Domi. No cloned or custom voices.

A script counts as rendered once an episode's `artifact.json` names it. When there's nothing left
to render, the run logs `RECIPE_SKIPPED` and exits 0 without calling Claude.

## Sample

> **Should We Text the Aliens First?** — A risk analyst, an allotment radio ham, a contrarian linguist and a cruise-ship crooner argue over whether humanity should transmit a hello to the stars or keep listening.
>
> *First live pilot run, 2026-10-14 · Gemini preset voices · 13.5-minute MP3 rendered from the script above*

## Run it

```bash
python recipes/podcast-episode/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../voiceover-script-generator/README.md">Next: Voiceover Script →</a>
</p>
