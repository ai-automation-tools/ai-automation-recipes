# AI Stack Radar

[← All recipes](../../README.md)

A monthly radar of **hosted AI products and services** — at least 24, sorted into 7–10 buckets by the job they do, each with what it **replaces** and what it **costs**. Products you sign up for, never bare repos (the repo digests own those). Every URL is fetched before it is published, and nothing an earlier run featured comes back unless it has genuinely changed.

| | |
|:---|:---|
| **Output** | `ai-stack-radar/<YYYY-MM>/<date>_ai-stack-radar/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 11th, 21:30 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only. |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner regenerates `all-bookmarks.html` at the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and hands the agent the full list of what was already featured.

## What the runner checks

The runner logs a warning if any `github.com` link slips in — the scope rule is products, not repos.

## Run it

```bash
python recipes/ai-stack-radar/run.py --output-dir ~/ai-output
```
