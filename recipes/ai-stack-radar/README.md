<h1 align="center">📡 AI Stack Radar</h1>

<p align="center">
  <em>24+ hosted AI products sorted by the job they do, each with what it replaces and what it costs.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Products you sign up for, grouped into 7–10 buckets. Bare repos belong to the repo digests, not this
one. Every URL is fetched before it's published.

| | |
|:---|:---|
| **Output** | `ai-stack-radar/<YYYY-MM>/<date>_ai-stack-radar/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
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
full list of products already featured. A product can come back after at least 8 weeks, and only if
it has changed in a way worth reporting.

## What the runner checks

It logs a warning when a `github.com` link slips in. The scope is products, not repos.

## Run it

```bash
python recipes/ai-stack-radar/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../oss-spotlight/README.md">Next: Open-Source Spotlight →</a>
</p>
