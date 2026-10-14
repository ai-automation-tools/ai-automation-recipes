# Finance Toolkit

[← All recipes](../../README.md)

A monthly haul of **22+ financial tools** — market-data APIs, backtesting engines, broker SDKs, ledgers and accounting, finance AI, fintech infrastructure, on-chain tooling and a small personal-finance lane. Builder-first. Free-tier caps are checked on the provider's own pricing page. **Never investment advice.**

| | |
|:---|:---|
| **Output** | `finance-toolkit/<YYYY-MM>/<date>_finance-toolkit/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 25th, 18:30 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only. |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner regenerates `all-bookmarks.html` at the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and hands the agent the full list of what was already featured.

## Run it

```bash
python recipes/finance-toolkit/run.py --output-dir ~/ai-output
```
