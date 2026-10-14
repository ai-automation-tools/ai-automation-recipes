<h1 align="center">🕹️ Browser Game</h1>

<p align="center">
  <em>A complete game in one HTML file, playable from disk on a desktop or a phone.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude writes the core loop in one sentence before anything else, then builds the game against the
things that usually break single-file games: speed tied to frame rate, blurry canvases on high-DPI
screens, missing touch controls. Every game has a score and a restart. A design brief and key-art
cover come with it.

| | |
|:---|:---|
| **Output** | `browser-games/<YYYY-MM>/<date>_<slug>/` → `index.html`, `game-design-brief.md`, `cover.png`, `artifact.json` |
| **Model** | `opus`. A complete game in one pass benefits from it; `sonnet` also works |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `game-design`, `single-file-game-dev`, `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🎲 Genres

Thirteen, and the ISO week number picks which one: endless runner, match-3, top-down arena shooter,
physics stacking, rhythm, snake variant, brick breaker, tower defense, word puzzle, single-screen
platformer, Sokoban-style, Asteroids-style, memory. Pass any string to override it:
`--genre "Tower defense"`.

## 🧪 Sample

> **Plumb Line** — Swing cargo off a dockside crane onto a narrow pier and stack it as high as the
> wind will let you, landing each piece dead level to keep a bonus chain going.
>
> *Physics stacking · 38 KB, no dependencies · mouse, touch and keyboard · first live pilot run,
> 2026-10-14 (Opus, about 11 minutes)*

## ✅ What the runner checks

Nothing is published if `index.html`:

- loads any file or URL other than the p5.js CDN (a `data:` URI is fine);
- has an inline script that fails `node --check`;
- throws a JavaScript error when loaded in a headless browser and poked with clicks and keys.

Whether the game is fun is still your call. Open it and play.

## ▶️ Run it

```bash
python recipes/browser-game/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../mobile-game/README.md">Next: Mobile Game →</a>
</p>
