# Weekly Short Story

[← All recipes](../../README.md)

One finished story a week, 2,000–4,000 words, in a rotating genre. Claude sees the title and
logline of every story already written and has to avoid their premises, characters and twists.
The cover is a portrait illustration of one pivotal image from the story.

| | |
|:---|:---|
| **Output** | `short-stories/<YYYY-MM>/<date>_<slug>/` → `story.md`, `cover.png`, `artifact.json` |
| **Schedule** | Sundays, 13:00 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Genres

Eleven, picked by least-used: near-future AI fiction, cozy mystery, cyberpunk, office absurdism,
magical realism, quiet horror, tech satire, fantasy, identity/security thriller, comedy, hard
sci-fi. Force one with `--genre "cozy mystery"`.

## Sample

> **The Blue Words** — When a firmware update shows a retired Duluth dock worker which words his
> hearing aids have been quietly guessing, he learns that the one sentence that carried him through
> his wife's death was never said.
>
> *Near-future AI fiction · 3,165 words · first live pilot run, 2026-10-14 (Opus, about 3 minutes)*

## Idea queue (optional)

Create `<output-dir>/short-stories/story-ideas.md`:

```markdown
- [ ] A lighthouse keeper who starts receiving letters from the ships she failed to warn
- [ ] An HR chatbot that unionizes
```

Each run takes the first unchecked idea as its premise and ticks it off with a link to the story:
`- [x] A lighthouse keeper… — story: 2026-10/2026-10-18_the-keeper`.

## Run it

```bash
python recipes/weekly-short-story/run.py --output-dir ~/ai-output
```
