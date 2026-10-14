<h1 align="center">📰 Signal Sources</h1>

<p align="center">
  <em>A growing reading list of blogs, newsletters, changelogs and channels worth following, with their feeds.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The list covers AI and technology. Each run adds 12+ sources that aren't on it yet, every one active
in the last 90 days and with a verified RSS or Atom feed where one exists.

| | |
|:---|:---|
| **Output** | `signal-sources/<YYYY-MM>/<date>_signal-sources/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only |

## Bookmarks and feeds

Each run writes `bookmarks.html` next to the digest. After every run the runner also rebuilds two
files at the collection root from the whole list: `all-bookmarks.html`, which imports into Chrome,
Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*), and `feeds.opml`, which loads
every feed into a reader in one import.

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and gives the agent the
full list of sources already on it.

## Run it

```bash
python recipes/signal-sources/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../security-toolkit/README.md">Next: Security Toolkit →</a>
</p>
