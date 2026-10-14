<h1 align="center">🌐 Cool Websites</h1>

<p align="center">
  <em>28+ useful, lesser-known websites across 8–12 categories, never repeating an earlier run.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Hidden gems over mega-sites. Every run includes a security, privacy and OSINT category and a 3D
modeling and printing category with at least one GitHub repo in it.

| | |
|:---|:---|
| **Output** | `cool-websites/<YYYY-MM>/<date>_cool-websites/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
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
full list of sites already featured. A site is never featured twice.

## Run it

```bash
python recipes/cool-websites/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../top-10-github-repos/README.md">Next: Top 10 GitHub Repos →</a>
</p>
