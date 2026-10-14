<h1 align="center">🔦 Open-Source Spotlight</h1>

<p align="center">
  <em>An editorial read on open source in six fixed sections, each entry graded by significance.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The sections are Project of the Week, Top 5 Trending, Notable New Releases, Community & Ecosystem
News, Hidden Gems and Developer Tooling Highlights: 20–30 entries, each graded High, Medium or Low.
The agent works from seven news feeds the runner fetches first (GitHub's blogs, GitHub Trending,
TLDR Tech, Hacker News, The Register, LWN).

| | |
|:---|:---|
| **Output** | `oss-spotlight/<YYYY-MM>/<date>_oss-spotlight/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
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
full list of entries already featured.

## What the runner checks

The six section names are fixed. A digest with any other section is rejected.

## Run it

```bash
python recipes/oss-spotlight/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../cool-websites/README.md">Next: Cool Websites →</a>
</p>
