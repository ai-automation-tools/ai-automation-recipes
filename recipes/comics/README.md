# Comic

[← All recipes](../../README.md)

One four-panel comic strip a week. Claude picks up the week's topic, writes a script with
dialogue for original, clearly fictional cartoon characters, and describes the full-page strip;
the runner renders it, with short balloon lettering.

| | |
|:---|:---|
| **Output** | `comics/<YYYY-MM>/<date>_<slug>/` → `script.md`, `comic.png`, `artifact.json` |
| **Schedule** | Wednesdays, 10:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) — the strip is the output |

## Topics

Thirty-one, picked least-used first: AI agents in a dysfunctional office, smart homes with
personalities, gig workers getting revenge, a sentient fridge that judges you, and more (see
`run.py`). Force one with `--topic "…"`.

## What the runner checks

`script.md` must have exactly four panels (`## Panel 1`–`## Panel 4`), and the final JSON must
ask for one `comic.png` at 16:9 (a single row) or 1:1 / 3:4 (a 2×2 grid). Lettering is allowed in
this image only; image models still garble long or small text, so balloons are capped at about six
words and the full dialogue lives in `script.md`. No real, recognisable people — the image
engines refuse them anyway.

## Sample

> **Circular Dependency** — Two AI agents are each blocked on the other, so they schedule a meeting about it. Many meetings later they're still blocked on each other.
>
> *First live pilot run, 2026-10-14 · Sonnet · one 2×2 lettered strip*

## Run it

```bash
python recipes/comics/run.py --output-dir ~/ai-output
```
