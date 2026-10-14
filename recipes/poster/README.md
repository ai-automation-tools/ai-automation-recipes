<h1 align="center">🖼️ Poster</h1>

<p align="center">
  <em>A 2:3 poster on the next theme from a list of 200.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The themes cover art movements, nature, science, space, mythology, architecture, food and
abstract work. Claude designs the concept, title and caption and writes the image prompt; the
runner renders it as a vertical 2:3 image.

| | |
|:---|:---|
| **Output** | `posters/<YYYY-MM>/<date>_<slug>/` → `poster.md`, `poster.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). The poster is the output |

## Themes

[`themes.md`](themes.md) holds the list, grouped under headings. Every `- ` line is a theme; edit
the file to change what comes up. Themes are picked least-used first. Force one with
`--theme "..."`.

## Lettering

A poster may carry one line of lettering: its title or caption, a few words, quoted exactly.
Nothing else. No credits, no stat blocks, no watermark.

## Run it

```bash
python recipes/poster/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../future-cities/README.md">Next: Future Cities 2500 →</a>
</p>
