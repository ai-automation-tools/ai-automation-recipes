# PC Game Concept

[← All recipes](../../README.md)

One original PC game concept a week, in a rotating genre. Claude researches what's happening in the
genre now, writes a design brief that has to pass a buildability test (what the player presses, how a
run ends, what the difficulty values are), and builds a one-page pitch with key art and copyable
feature bullets.

| | |
|:---|:---|
| **Output** | `pc-game-concepts/<YYYY-MM>/<date>_<slug>/` → `game-design-brief.md`, `pitch.html`, `sources.csv`, `cover.png`, `artifact.json` |
| **Schedule** | Mondays, 14:15 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `game-design`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Genres

Ten, one per ISO week: immersive sim, survival crafting, colony sim, tactical RPG, roguelike
deckbuilder, automation/factory sim, cozy management sim, detective mystery, grand strategy,
extraction shooter. Force one with `--genre "colony sim"`.

## What the runner checks

The run is rejected if `pitch.html` loads an external script or a missing local file (it shows
`cover.png`, which the runner renders after the agent finishes), an inline script fails
`node --check`, or `sources.csv` doesn't have the `title,url,note` header and 3–5 sources. With
`--image-engine none` the pitch's key-art slot stays empty.

## Run it

```bash
python recipes/pc-game-concept/run.py --output-dir ~/ai-output
```
