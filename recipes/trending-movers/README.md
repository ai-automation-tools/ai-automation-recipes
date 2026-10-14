# Trending Movers

[← All recipes](../../README.md)

A **star-velocity leaderboard across all of open source**: the 12–15 repos that gained the most stars in the past week, plus 5–10 more climbing. The order and every figure are **measured** — the runner scrapes GitHub's weekly trending pages before the agent starts, and the agent writes the why.

| | |
|:---|:---|
| **Output** | `trending-movers/<YYYY-MM>/<date>_trending-movers/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 15th, 12:30 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Fetches its candidate feeds in Python before the agent runs (stdlib only, no key). One dead feed is skipped, never fatal. |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner regenerates `all-bookmarks.html` at the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and hands the agent the full list of what was already featured. Here that list is context for trajectory notes, not exclusions.

## What the runner checks

The runner rejects a digest whose published `+N this week` figures differ from the measurements or whose leaderboard isn't in descending order. A repo that renamed is published under its new URL and logged as unchecked. Repeats are expected here — a repo that keeps surging stays on top.

## Run it

```bash
python recipes/trending-movers/run.py --output-dir ~/ai-output
```
