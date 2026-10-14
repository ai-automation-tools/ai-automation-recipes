<h1 align="center">🎬 Voiceover Script</h1>

<p align="center">
  <em>A narrated true story with a vertical short cut from generated scene stills.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-speech_and_image_keys-F59E0B?style=for-the-badge" alt="Needs speech and image keys">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude writes a 90 to 180 second narration about a real story (a business collapse, a historical
scam, a survival story) from 2 to 4 sources, plus direction notes. The runner narrates it with a
preset voice and, when ffmpeg is installed, cuts a 1080×1920 short from four to six generated
scene stills.

| | |
|:---|:---|
| **Output** | `voiceover-scripts/<YYYY-MM>/<date>_<slug>/` → `script.md`, `direction-notes.md`, `voiceover.mp3`, `scenes/scene-*.png`, `short.mp4`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | An image key for the cover and scenes, and a speech key (`GEMINI_API_KEY` or `ELEVENLABS_API_KEY`) |

`--voice` fixes the narrator to one preset of the chosen `--speech-engine`; `auto` lets Claude pick
one by tone. No image shows a real person's likeness.

## What the runner checks

240 to 480 words of narration (with a little slack), at least two linked sources, a `## Tone`
section in the direction notes, and a narrator from the active engine's presets.

## Sample

> **The Spacecraft Lost to a Unit Label** — In 1999 NASA's Mars Climate Orbiter burned up at Mars because ground software reported thruster data in pound-seconds instead of newton-seconds.
>
> *First live pilot run, 2026-10-14 · Gemini voice Charon · 2:20 narration and a 1080×1920 short over five scene stills*

## Run it

```bash
python recipes/voiceover-script-generator/run.py --output-dir ~/ai-output --speech-engine elevenlabs --voice Adam
```

---

<p align="center">
  <a href="../README.md">← All recipes</a>
</p>
