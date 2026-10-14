<h1 align="center">💹 Finance Toolkit</h1>

<p align="center">
  <em>22+ financial tools for builders, from market-data APIs to ledgers, with free-tier caps checked.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Market-data APIs, backtesting engines, broker SDKs, ledgers and accounting, finance AI, fintech
infrastructure, on-chain tooling, and a small personal-finance lane. Free-tier caps come from the
provider's own pricing page. Nothing in it is investment advice.

| | |
|:---|:---|
| **Output** | `finance-toolkit/<YYYY-MM>/<date>_finance-toolkit/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner rebuilds `all-bookmarks.html` at
the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari
(*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and gives the agent the
full list of tools already featured. A tool can come back after at least 6 months, and only if it
has shipped something worth a second look.

## Run it

```bash
python recipes/finance-toolkit/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../model-benchmark-watch/README.md">Next: Model Benchmark Watch →</a>
</p>
