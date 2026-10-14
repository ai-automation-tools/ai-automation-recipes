# Serialized Novella

[← All recipes](../../README.md)

A novel, one chapter a week. Every chapter lands a present beat, an earned reveal and a cliffhanger,
written against a story bible whose canon and chapter-by-chapter outline are fixed. Continuity
comes from a rolling synopsis and the three most recent chapters, fed back in every run.

| | |
|:---|:---|
| **Output** | `serialized-novella/<YYYY-MM>/<date>_<novel>-chNN/` → `chapter.md`, `cover.png`, `artifact.json` |
| **State** | `serialized-novella/story-bible.md` |
| **Schedule** | Mondays, 11:30 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `writing-principles`, `creative-writing-craft` (+ its genre reference), `creative-writing-modes`, `story-review` (antipatterns), `llm-writing`, `humanizer`, `image-prompt-craft` |

## The story bible

The first run with no `story-bible.md` invents a novel: it writes the bible (premise, canon, cast,
dramatic question, and an outline of every chapter) **and** chapter 1. Or write your own bible
first; it needs this frontmatter:

```markdown
---
title: Perpetuity
slug: perpetuity
genre: near-future techno-horror
target_chapters: 30
craft_genre: horror
visual_style: Muted painterly realism; slate blue, sodium orange, bone white, deep shadow.
---
```

The chapter number and synopsis come from the chapters already published. When a novel reaches
`target_chapters`, its bible is archived as `story-bible.<slug>.md` and the next run starts a new
novel. `--genre` picks the genre of that next one.

The runner rejects a chapter under 1,200 words, or one whose JSON names the wrong novel or chapter
number, and trims an over-long synopsis to 150 words.

## Run it

```bash
python recipes/serialized-novella/run.py --output-dir ~/ai-output
```
