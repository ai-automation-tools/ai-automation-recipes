<h1 align="center">📱 Mobile Game</h1>

<p align="center">
  <em>A portrait, touch-first phone game in one HTML file.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The game sits inside an on-screen phone frame, so it reads as a mobile game even on a desktop. Claude
writes the core loop first, then builds around what breaks phone games: the page scrolling or zooming
mid-drag, games running double speed on 120 Hz screens, blurry canvases, controls hidden under the
notch, and iOS audio that stays silent.

| | |
|:---|:---|
| **Output** | `mobile-games/<YYYY-MM>/<date>_<slug>/` → `index.html`, `game-design-brief.md`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `game-design`, `single-file-game-dev`, `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🎲 Genres

Ten, picked by ISO week number: endless runner, match-3, tap timing, idle incremental, tower defense,
bubble shooter, physics puzzle, merge puzzle, whack-a-mole, rhythm tap. Override with
`--genre "match-3"`.

## ✅ What the runner checks

Nothing is published if `index.html` loads any file or URL other than the p5.js CDN, an inline script
fails `node --check`, or the page throws when loaded in a headless browser and poked. None of that
proves touch feels right. Open it on a phone and play.

## ▶️ Run it

```bash
python recipes/mobile-game/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../pc-game-concept/README.md">Next: PC Game Concept →</a>
</p>
