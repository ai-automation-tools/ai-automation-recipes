# Audio Podcast

[← All recipes](../../README.md)

Turns the oldest unrendered [podcast script](../podcast-script-generator/README.md) into an episode.
Claude casts a **preset** voice for every speaker (distinct voices while they last) with a short
delivery note, and writes show notes; the runner speaks every line with text-to-speech and joins
them into one track.

| | |
|:---|:---|
| **Output** | `podcasts/<YYYY-MM>/<date>_<slug>/` → `episode.md`, `episode.mp3` (WAV without ffmpeg), `script.md`, `cover.png` (the script's), `artifact.json` |
| **Schedule** | Saturdays, 18:00 UTC |
| **Model** | `sonnet` |
| **Needs** | `GEMINI_API_KEY` (Gemini TTS, default) or `ELEVENLABS_API_KEY` (`--speech-engine elevenlabs`, premade voices) |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web) |
| **Skills** | `llm-writing`, `humanizer` |

Preset voices only — Gemini: Kore, Puck, Charon, Fenrir, Aoede, Zephyr, Leda, Orus; ElevenLabs:
Rachel, Adam, Antoni, Bella, Josh, Domi. No cloned or custom voices.

A script counts as rendered once an episode's `artifact.json` names it. With nothing left to
render, the run logs `NOTHING_TO_RENDER` and exits 0.

## Sample

> **Should We Text the Aliens First?** — A risk analyst, an allotment radio ham, a contrarian linguist and a cruise-ship crooner argue over whether humanity should transmit a hello to the stars or keep listening.
>
> *First live pilot run, 2026-10-14 · Gemini preset voices · 13.5-minute MP3 rendered from the script above*

## Run it

```bash
python recipes/weekly-audio-podcast/run.py --output-dir ~/ai-output
```
