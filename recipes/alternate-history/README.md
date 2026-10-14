# Weekly Alternate History

[← All recipes](../../README.md)

One "what if" a week. Claude takes a real, well-documented turning point, changes exactly one
thing, and traces the consequences forward through eight short titled sections — days, then years,
then decades — grounded, plausible and non-graphic. Each section gets a scene illustration prompt,
all written to one shared palette so the set reads as one piece.

| | |
|:---|:---|
| **Output** | `alternate-history/<YYYY-MM>/<date>_<slug>/` → `story.md`, `scene-prompts.md`, `cover.png`, `artifact.json` |
| **Schedule** | Fridays, 15:00 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `writing-principles`, `creative-writing-craft`, `llm-writing`, `humanizer`, `image-prompt-craft` |

The runner rejects a piece unless `story.md` has exactly eight sections and `scene-prompts.md` has
a prompt for each. Only the 2:3 cover is rendered today; rendering the eight scenes waits on the
runner's multi-image step.

## Premise queue (optional)

Create `<output-dir>/alternate-history/alt-history-ideas.md`:

```markdown
- [ ] The Library of Alexandria is never destroyed and survives to the present.
- [ ] The Apollo 13 crew does not make it home.
```

Each run takes the first unchecked premise and ticks it off with the folder it became. With no
queue, Claude invents one, steering away from divergences already written.

## Run it

```bash
python recipes/alternate-history/run.py --output-dir ~/ai-output
```
