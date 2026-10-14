# Signal Sources

[← All recipes](../../README.md)

A **cumulative reading list** of blogs, newsletters, changelogs, channels and leaderboards worth following on AI and technology. Each run adds **12+ sources that aren't already on the list**, each checked alive in the last 90 days and with a verified RSS/Atom feed where one exists.

| | |
|:---|:---|
| **Output** | `signal-sources/<YYYY-MM>/<date>_signal-sources/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 1st, 14:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only. |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner regenerates `all-bookmarks.html` at the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*).

After every run the runner regenerates two cumulative files at the collection root: `all-bookmarks.html` (the whole list as importable bookmarks) and `feeds.opml` (every feed, one import into any reader).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and hands the agent the full list of what was already featured.

## Run it

```bash
python recipes/signal-sources/run.py --output-dir ~/ai-output
```
