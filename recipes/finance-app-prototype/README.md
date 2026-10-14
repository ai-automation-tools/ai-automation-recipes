<h1 align="center">💵 Finance App Prototype</h1>

<p align="center">
  <em>A runnable personal-finance tool built on synthetic data.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Think budgeting dashboard, debt payoff planner, card rewards optimizer. Claude checks current rates,
limits and the complaints people post about the problem, then builds the tool on made-up data with
all money math done in integer cents. It's framed as an organizer. It never gives financial advice.

| | |
|:---|:---|
| **Output** | `financial-ideas/<YYYY-MM>/<date>_<slug>/` → `README.md`, `requirements.md`, `index.html`, `style.css`, `script.js`, `sample-data.json`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🗂️ Themes

Eight: **Investing**, **Budgeting**, **Saving**, **Rewards**, **Discounts**, **Debt**, **Taxes**,
**Net-Worth**. Each run takes the least-used one. Force one with `--theme Debt`.

## ✅ What the runner checks

The same checks as [App Prototype](../app-prototype/README.md): valid `sample-data.json`, no missing
local or non-HTTPS references in `index.html`, every script passes `node --check`, and the page
loads in a headless browser without throwing.

## ▶️ Run it

```bash
python recipes/finance-app-prototype/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../iam-prototype/README.md">Next: IAM App Prototype →</a>
</p>
