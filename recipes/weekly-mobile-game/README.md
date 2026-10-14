# Weekly Mobile Game

[← All recipes](../../README.md)

One phone game a week, as a single `index.html`: portrait, touch-first, shown inside an on-screen
phone frame so it reads as a mobile game even on a desktop. Claude writes the core loop first, then
builds for the things that break phone games — scroll and zoom during drags, 120Hz speed-ups, blurry
canvases, controls under the notch, silent iOS audio.

| | |
|:---|:---|
| **Output** | `mobile-games/<YYYY-MM>/<date>_<slug>/` → `index.html`, `game-design-brief.md`, `cover.png`, `artifact.json` |
| **Schedule** | Thursdays, 16:30 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `game-design`, `single-file-game-dev`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Genres

Ten, one per ISO week: endless runner, match-3, tap timing, idle incremental, tower defense, bubble
shooter, physics puzzle, merge puzzle, whack-a-mole, rhythm tap. Force one with `--genre "match-3"`.

## What the runner checks

The game is rejected if `index.html` loads any file or URL other than the p5.js CDN, or its inline
script fails `node --check`. It can't tell whether the game is fun or whether touch works — open it on
a phone and play.

## Run it

```bash
python recipes/weekly-mobile-game/run.py --output-dir ~/ai-output
```
