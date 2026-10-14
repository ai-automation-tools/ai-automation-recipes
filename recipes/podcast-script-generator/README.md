# Podcast Script

[← All recipes](../../README.md)

One AI-vs-AI debate podcast episode per run: a host and 3–4 guests with clashing personalities,
1,500–3,000 words of real back-and-forth, written as a speaker-labelled transcript that the
[Audio Podcast](../weekly-audio-podcast/README.md) recipe renders to sound.

| | |
|:---|:---|
| **Output** | `podcast-scripts/<YYYY-MM>/<date>_<slug>/` → `script.md`, `cast.md` (invented casts), `cover.png`, `artifact.json` |
| **Schedule** | Fridays, 21:00 UTC (the day before the audio render) |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web) |
| **Skills** | `image-prompt-craft` |

## Your own cast and topics (optional)

In `<output-dir>/podcast-scripts/`:

- `podcast-topics.md` — `- [ ] Title — angle, angle, angle` per line. The first unchecked topic is
  used and ticked off with the episode's path.
- `cast/hosts/*.md` and `cast/groups/<Group>/*.md` — persona cards for a recurring cast. Each run
  picks one host and one group at random and keeps every guest in character.

Without them, Claude picks a fresh topic and invents a fictional cast, written to `cast.md`. No
speaker may be, or be named after, a real living person.

## What the runner checks

At least two guests, each speaking 4–7 times; at least ten turns; 1,200–3,500 words; a `## Script`
section; `cast.md` when the cast was invented.

## Sample

> **Should We Text the Aliens First?** — A cautious astrophysicist, a backyard radio enthusiast, a contrarian linguist and a cruise-ship crooner argue over whether humanity should beam deliberate messages to the stars, covering the 'dark forest' risk, who gets to decide, whether anyone could understand us, and the century of TV and radar we've already leaked.
>
> *First live pilot run, 2026-10-14 · Opus · 42 turns, about 2,000 words, invented cast*

## Run it

```bash
python recipes/podcast-script-generator/run.py --output-dir ~/ai-output
```
