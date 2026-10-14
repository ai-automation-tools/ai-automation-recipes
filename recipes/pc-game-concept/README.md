<h1 align="center">🖥️ PC Game Concept</h1>

<p align="center">
  <em>An original PC game concept: a design brief, a one-page pitch and key art.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude researches what's happening in the genre right now, then writes a design brief that has to
pass a buildability test: what the player presses, how a run ends, what the difficulty values are.
The pitch page is built from it, with key art and feature bullets you can copy.

| | |
|:---|:---|
| **Output** | `pc-game-concepts/<YYYY-MM>/<date>_<slug>/` → `game-design-brief.md`, `pitch.html`, `sources.csv`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `game-design`, `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🎲 Genres

Ten, picked by ISO week number: immersive sim, survival crafting, colony sim, tactical RPG, roguelike
deckbuilder, automation/factory sim, cozy management sim, detective mystery, grand strategy,
extraction shooter. Override with `--genre "colony sim"`.

## ✅ What the runner checks

Nothing is published if `pitch.html` loads an external script or a missing local file, an inline
script fails `node --check`, or `sources.csv` lacks the `title,url,note` header or has fewer than 3
or more than 5 sources. The pitch shows `cover.png`, which the runner renders after the agent
finishes. With `--image-engine none` that slot stays empty.

## ▶️ Run it

```bash
python recipes/pc-game-concept/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../3d-print-design/README.md">Next: 3D Print Design →</a>
</p>
