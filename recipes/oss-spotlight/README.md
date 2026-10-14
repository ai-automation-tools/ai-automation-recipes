# Open-Source Spotlight

[← All recipes](../../README.md)

An **editorial read on open source** in six fixed sections — Project of the Week, Top 5 Trending, Notable New Releases, Community & Ecosystem News, Hidden Gems, Developer Tooling Highlights — 20–30 entries, each graded High / Medium / Low significance. Grounded in seven fetched news feeds (GitHub's blogs, GitHub Trending, TLDR Tech, Hacker News, The Register, LWN).

| | |
|:---|:---|
| **Output** | `oss-spotlight/<YYYY-MM>/<date>_oss-spotlight/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 8th, 18:30 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Fetches its candidate feeds in Python before the agent runs (stdlib only, no key). One dead feed is skipped, never fatal. |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner regenerates `all-bookmarks.html` at the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and hands the agent the full list of what was already featured.

## What the runner checks

Section names are fixed; a digest using any other section is rejected.

## Run it

```bash
python recipes/oss-spotlight/run.py --output-dir ~/ai-output
```
