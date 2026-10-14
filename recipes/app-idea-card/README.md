<h1 align="center">💡 App Idea Card</h1>

<p align="center">
  <em>A one-page pitch for an app idea, grounded in something that happened in the last 30 days.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude searches recent news and forums for a real trend or pain point, checks your backlog so it
doesn't pitch the same thing twice, and writes a card: problem, target user, MVP scope,
monetization, why now, risks, next step, and at least two sources. It also writes a description of
a concept-art cover, which the runner turns into an image.

| | |
|:---|:---|
| **Output** | `idea-cards/<YYYY-MM>/<date>_<slug>/` → `card.md`, `cover.png`, `artifact.json` |
| **Model** | `sonnet`. Research and a one-pager don't need more |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🗂️ Categories

Five of them: **Browser Extension**, **GitHub Repo**, **Web/Mobile App**, **AI Tool**, **Security
Tool**. Each run takes the category with the fewest cards so far, and breaks ties by picking the one
used longest ago. Force one with `--category "Security Tool"`.

## 🧪 Sample

> **ChatWatch** — Shows which of your installed browser extensions can read your ChatGPT, Claude
> and Gemini tabs, and warns you when one gains that access.
>
> *Browser Extension · freemium · first live pilot run, 2026-10-14*

## ▶️ Run it

```bash
python recipes/app-idea-card/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../app-prototype/README.md">Next: App Prototype →</a>
</p>
