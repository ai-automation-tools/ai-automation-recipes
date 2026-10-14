<h1 align="center">📈 Trending Movers</h1>

<p align="center">
  <em>A star-velocity leaderboard: the repos across open source that gained the most stars in the past week.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The 12–15 biggest gainers, plus 5–10 more that are climbing. The order and every figure are
measured, not written: the runner scrapes GitHub's weekly trending pages before the agent starts,
and the agent only writes the why.

| | |
|:---|:---|
| **Output** | `trending-movers/<YYYY-MM>/<date>_trending-movers/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Scrapes the trending pages in Python before the agent starts (stdlib only, no key). A dead page is skipped, not fatal |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner rebuilds `all-bookmarks.html` at
the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari
(*Import bookmarks from HTML file*).

## Earlier runs

The runner hands the agent the last few leaderboards as context for trajectory notes. Repeats are
expected here: a repo that keeps surging stays on top.

## What the runner checks

It rejects a digest whose `+N this week` figures differ from the measured ones, or whose
leaderboard isn't in descending order. A repo that was renamed is published under its new URL and
logged as unchecked.

## Sample

> **Trending Movers — 2026-10-14** — One reverse-engineering agent repo, morluto/rea, gained
> +183,758 stars, more than the other fourteen leaderboard entries combined, while the rest of the
> momentum went to agent skill packs, memory layers, browsers and test tooling.
>
> *First live pilot run, 2026-10-14 · Sonnet, under 2 minutes · 22 entries from live GitHub data, figures checked*

## Run it

```bash
python recipes/trending-movers/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../signal-sources/README.md">Next: Signal Sources →</a>
</p>
