# Finance App Prototype

[← All recipes](../../README.md)

One runnable personal-finance tool per run — a budgeting dashboard, a debt payoff planner, a card
rewards optimizer. Claude grounds it in current rates, limits and community pain points, builds it on
synthetic data with integer-cent math, and frames it as an organizer, not advice.

| | |
|:---|:---|
| **Output** | `financial-ideas/<YYYY-MM>/<date>_<slug>/` → `README.md`, `requirements.md`, `index.html`, `style.css`, `script.js`, `sample-data.json`, `cover.png`, `artifact.json` |
| **Schedule** | Monthly, the 6th at 21:30 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Themes

Eight, picked by least-used: **Investing**, **Budgeting**, **Saving**, **Rewards**, **Discounts**,
**Debt**, **Taxes**, **Net-Worth**. Force one with `--theme Debt`.

## What the runner checks

Same as the app prototype: valid `sample-data.json`, no missing local or non-HTTPS references in
`index.html`, and every script passes `node --check`.

## Run it

```bash
python recipes/finance-app-prototype/run.py --output-dir ~/ai-output
```
