# Browser Game

[← All recipes](../../README.md)

One playable game a week. Claude designs a game in this week's genre, writes the core loop before
anything else, and builds it as a single `index.html` that runs from `file://` on desktop and phone:
delta-time movement, sharp on high-DPI screens, touch controls, a score and a restart. A design
brief and key-art cover come with it.

| | |
|:---|:---|
| **Output** | `browser-games/<YYYY-MM>/<date>_<slug>/` → `index.html`, `game-design-brief.md`, `cover.png`, `artifact.json` |
| **Schedule** | Saturdays, 14:00 UTC |
| **Model** | `opus` (a complete game in one pass benefits from it; `sonnet` works) |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `game-design`, `single-file-game-dev`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Genres

Thirteen, one per ISO week: endless runner, match-3, top-down arena shooter, physics stacking,
rhythm, snake variant, brick breaker, tower defense, word puzzle, single-screen platformer,
Sokoban-style, Asteroids-style, memory. Force one with `--genre "Tower defense"` (any string works).

## Sample

> **Plumb Line** — Swing cargo off a dockside crane onto a narrow pier and stack it as high as the
> wind will let you, landing each piece dead level to keep a bonus chain going.
>
> *Physics stacking · 38 KB, no dependencies · mouse, touch and keyboard · first live pilot run,
> 2026-10-14 (Opus, about 11 minutes)*

## What the runner checks

The game is rejected, and nothing is published, if `index.html`:

- loads any file or URL other than the p5.js CDN (or a `data:` URI);
- has an inline script that fails `node --check` (skipped with a warning if Node isn't installed).

It can't tell whether the game is fun or whether input works — open it and play.

## Run it

```bash
python recipes/browser-game/run.py --output-dir ~/ai-output
```
