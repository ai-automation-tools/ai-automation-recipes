<h1 align="center">🏆 Top 10 GitHub Repos</h1>

<p align="center">
  <em>The ten strongest trending AI and developer-tooling repos, ranked, with what's driving each.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Each repo is tagged New, Trending or Popular & active. The runner fetches GitHub Trending's weekly
feeds and keyword-filters them before the agent starts, so the agent ranks what is actually trending
instead of what a search happens to turn up.

| | |
|:---|:---|
| **Output** | `top-10-github-repos/<YYYY-MM>/<date>_top-10-github-repos/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Fetches the feeds in Python before the agent starts (stdlib only, no key). A dead feed is skipped, not fatal |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner rebuilds `all-bookmarks.html` at
the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari
(*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and gives the agent the
full list of repos already featured.

## What the runner checks

Categories come from a closed list. A digest with any other category is rejected.

## Run it

```bash
python recipes/top-10-github-repos/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../trending-movers/README.md">Next: Trending Movers →</a>
</p>
