<h1 align="center">🎙️ Podcast Script</h1>

<p align="center">
  <em>A debate podcast script with a host and clashing guests, ready to be voiced.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

One episode per run: a host and three or four guests with conflicting views, 1,500 to 3,000 words
of real back-and-forth, written as a speaker-labelled transcript. The
[Podcast Episode](../podcast-episode/README.md) recipe turns it into audio.

| | |
|:---|:---|
| **Output** | `podcast-scripts/<YYYY-MM>/<date>_<slug>/` → `script.md`, `cast.md` (invented casts), `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `image-prompt-craft` |
| **Needs** | Nothing beyond Claude; an image key adds a cover |

## Your own cast and topics (optional)

In `<output-dir>/podcast-scripts/`:

- `podcast-topics.md`: one `- [ ] Title — angle, angle, angle` per line. The first unchecked topic
  is used and ticked off with the episode's path.
- `cast/hosts/*.md` and `cast/groups/<Group>/*.md`: persona cards for a recurring cast. Each run
  picks one host and one group at random and keeps every guest in character.

Without them, Claude picks a fresh topic and invents a fictional cast, written to `cast.md`. No
speaker may be, or be named after, a real living person.

## What the runner checks

At least two guests, each speaking 4 to 7 times; at least ten turns; 1,200 to 3,500 words; a
`## Script` section; and `cast.md` whenever the cast was invented.

## Sample

> **Should We Text the Aliens First?** — A cautious astrophysicist, a backyard radio enthusiast, a contrarian linguist and a cruise-ship crooner argue over whether humanity should beam deliberate messages to the stars, covering the 'dark forest' risk, who gets to decide, whether anyone could understand us, and the century of TV and radar we've already leaked.
>
> *First live pilot run, 2026-10-14 · Opus · 42 turns, about 2,000 words, invented cast*

## Run it

```bash
python recipes/podcast-script-generator/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../podcast-episode/README.md">Next: Podcast Episode →</a>
</p>
