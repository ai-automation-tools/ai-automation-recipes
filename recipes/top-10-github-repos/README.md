# Top 10 GitHub Repos

[← All recipes](../../README.md)

The **ten strongest trending AI and developer-tooling repositories**, ranked, each tagged New / Trending / Popular & active with what is driving it. The runner fetches GitHub Trending's weekly feeds and keyword-filters them first, so the agent picks from what is actually trending rather than what it can find by searching.

| | |
|:---|:---|
| **Output** | `top-10-github-repos/<YYYY-MM>/<date>_top-10-github-repos/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 4th, 12:30 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Fetches its candidate feeds in Python before the agent runs (stdlib only, no key). One dead feed is skipped, never fatal. |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner regenerates `all-bookmarks.html` at the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and hands the agent the full list of what was already featured.

## What the runner checks

Categories are a closed list; a digest using any other category is rejected.

## Run it

```bash
python recipes/top-10-github-repos/run.py --output-dir ~/ai-output
```
