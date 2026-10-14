# Poster

[← All recipes](../../README.md)

One vertical poster, twice a week, on the next theme from a list of 200 — art movements, nature,
science, space, mythology, architecture, food and lifestyle, abstract. Claude designs the concept,
title and caption and writes the image prompt; the runner renders it at 2:3.

| | |
|:---|:---|
| **Output** | `posters/<YYYY-MM>/<date>_<slug>/` → `poster.md`, `poster.png`, `artifact.json` |
| **Schedule** | Mondays and Thursdays, 15:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) — the poster is the output |

## Themes

[`themes.md`](themes.md) holds the list, grouped under headings. Every `- ` line is a theme; edit
it to change the rotation. Themes are picked least-used first. Force one with `--theme "…"`.

## Lettering

A poster may carry one line of designed lettering — its title or caption, a few words, quoted
exactly. Nothing else: no credits, no stat blocks, no watermark.

## Run it

```bash
python recipes/poster/run.py --output-dir ~/ai-output
```
