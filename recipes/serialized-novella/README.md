<h1 align="center">📚 Serialized Novella</h1>

<p align="center">
  <em>A novel written one chapter per run, held together by a story bible.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Every chapter lands a present beat, an earned reveal and a cliffhanger, written against a bible
whose canon and chapter outline don't move. Continuity comes from a rolling synopsis plus the three
most recent chapters, which the runner feeds back in each time.

| | |
|:---|:---|
| **Output** | `serialized-novella/<YYYY-MM>/<date>_<novel>-chNN/` → `chapter.md`, `cover.png`, `artifact.json` |
| **State** | `serialized-novella/story-bible.md` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `writing-principles`, `creative-writing-craft` (+ its genre reference), `creative-writing-modes`, `story-review` (antipatterns), `llm-writing`, `humanizer`, `image-prompt-craft` |

## The story bible

With no `story-bible.md` in the collection, the first run invents a novel: it writes the bible
(premise, canon, cast, dramatic question, and an outline of every chapter) **and** chapter 1. You can
also write your own bible first. It needs this frontmatter:

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
`target_chapters`, its bible is archived as `story-bible.<slug>.md` and the next run starts a new one.
`--genre` sets the genre of that next novel.

The runner rejects a chapter under 1,200 words or one whose JSON names the wrong novel or chapter
number, and it trims an over-long synopsis to 150 words.

## Sample

> ***No Speech Detected*, chapter 1: "False Wake"** — On the night shift, a half-deaf annotator who
> labels accidental smart-speaker recordings gets a clip from her own locked kitchen in which her dead
> brother's voice says her name.
>
> *First live pilot run, 2026-10-14 · Opus, about 6 minutes · seed run: story bible plus chapter 1, 2,344 words*

## Run it

```bash
python recipes/serialized-novella/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../alternate-history/README.md">Next: Alternate History →</a>
</p>
