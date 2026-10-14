<h1 align="center">💬 Comic</h1>

<p align="center">
  <em>A four-panel comic strip with short lettered balloons, about one rotating topic.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude takes the next topic, writes a script with dialogue for original cartoon characters, and
describes the full strip. The runner renders it as one image with the balloon text drawn in.

| | |
|:---|:---|
| **Output** | `comics/<YYYY-MM>/<date>_<slug>/` → `script.md`, `comic.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). The strip is the output, so the run stops before calling Claude without one |

## Topics

Thirty-one, least-used first: AI agents in a dysfunctional office, smart homes with
personalities, gig workers getting revenge, a fridge that judges you, and more (see `run.py`).
Force one with `--topic "..."`.

## What the runner checks

`script.md` needs exactly four panels, `## Panel 1` to `## Panel 4`. The final JSON asks for one
`comic.png`, either 16:9 (one row) or 1:1 / 3:4 (a 2×2 grid). Image models garble long or small
text, so balloons stay at about six words and the full dialogue lives in `script.md`. No real,
recognisable people; the image engines refuse them anyway.

## Sample

> **Circular Dependency** — Two AI agents are each blocked on the other, so they schedule a meeting about it. Many meetings later they're still blocked on each other.
>
> *First live pilot run, 2026-10-14 · Sonnet · one 2×2 lettered strip*

## Run it

```bash
python recipes/comics/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../ai-meme-generator/README.md">Next: AI Meme →</a>
</p>
