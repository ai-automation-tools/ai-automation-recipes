# Daily App Idea Card

[← All recipes](../../README.md)

One researched app pitch a day. Claude searches the last 30 days for a real trend or pain point,
picks an idea nobody in your backlog has covered, and writes a one-page card: problem, target user,
MVP scope, monetization, why now, risks, next step, and at least two sources. Then it describes a
concept-art cover, which the runner renders.

| | |
|:---|:---|
| **Output** | `idea-cards/<YYYY-MM>/<date>_<slug>/` → `card.md`, `cover.png`, `artifact.json` |
| **Schedule** | Daily, 11:00 UTC |
| **Model** | `sonnet` (research + a one-pager doesn't need more) |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Categories

The runner rotates through five categories, always picking the one with the fewest cards (ties go
to the one used least recently): **Browser Extension**, **GitHub Repo**, **Web/Mobile App**,
**AI Tool**, **Security Tool**. Force one with `--category "Security Tool"`.

## Sample

> **ChatWatch** — Shows which of your installed browser extensions can read your ChatGPT, Claude
> and Gemini tabs, and warns you when one gains that access.
>
> *Browser Extension · freemium · first live pilot run, 2026-10-14*

## Run it

```bash
python recipes/daily-app-card/run.py --output-dir ~/ai-output
```
