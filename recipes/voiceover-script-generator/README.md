# Voiceover Script

[← All recipes](../../README.md)

A 90–180-second narration about a real-world story — a business collapse, a historical scam, a
survival story — researched from 2–4 sources, with direction notes. The runner narrates it with a
preset voice and, when ffmpeg is installed, cuts a 1080×1920 vertical short from 4–6 generated
scene stills.

| | |
|:---|:---|
| **Output** | `voiceover-scripts/<YYYY-MM>/<date>_<slug>/` → `script.md`, `direction-notes.md`, `voiceover.mp3`, `scenes/scene-*.png`, `short.mp4`, `cover.png`, `artifact.json` |
| **Schedule** | Sundays, 17:00 UTC |
| **Model** | `sonnet` |
| **Needs** | an image key (cover + scenes) and a speech key (`GEMINI_API_KEY` or `ELEVENLABS_API_KEY`) |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

`--voice` fixes the narrator (a preset of the chosen `--speech-engine`); `auto` lets Claude pick by
tone. No image shows a real person's likeness.

## What the runner checks

240–480 words of narration (with a little slack), at least two linked sources, a `## Tone` section
in the direction notes, and a narrator from the active engine's presets.

## Run it

```bash
python recipes/voiceover-script-generator/run.py --output-dir ~/ai-output --speech-engine elevenlabs --voice Adam
```
