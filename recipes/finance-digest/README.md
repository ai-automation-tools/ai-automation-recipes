<h1 align="center">💹 Finance Digest</h1>

<p align="center">
  <em>One of eight money briefings a run: markets, paper trade ideas, strategy, and the points-and-miles beats.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/topics-8-0078D4?style=for-the-badge" alt="8 topics">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The rewards topics work like [News Digest](../news-digest/README.md): the runner fetches the
topic's feeds, keeps the last seven days capped per source, and the agent writes only what the feeds
carried. The three market topics are different. Feeds give them the week's narrative, but the
numbers (index levels, yields, sector moves, an ETF's year-to-date) come from public pages the agent
finds and reads, cited next to the figure. A number it didn't read is `data unavailable`, never an
estimate. There is no keyed market-data API anywhere in this recipe; the private jobs it was ported
from used one, and that is the one thing that didn't come across.

Every edition ends with the same `## Not Financial Advice` section and the runner refuses one that
doesn't. Trade Ideas carries a further rule: the line *Paper only: study ideas, not orders.* under
the title and a `Risk` column in every idea table.

| | |
|:---|:---|
| **Output** | `finance-digests/<YYYY-MM>/<date>_<topic>/` → `digest.md`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | The topic's feeds, then the pages they link and the quote pages the market topics need |

## 🗂️ Topics

Eight, in [`topics.json`](topics.json), each with its sections, a palette, a cover motif and its
own rules. A run takes the least-covered topic; `--topic transfer-bonuses` forces one.

| Topic | Kind | Sections | Feeds |
|:---|:---|:---|:-:|
| `stock-market` | markets | Weekly Recap · Indices, Vol & Yields · Sector Rotation · Top Movers · Earnings Recap · Macro & News Themes · Stock of the Week · Week Ahead · Levels to Watch | 3 |
| `trade-ideas` | markets | Market Pulse · Dividend Ideas · Growth Ideas · ETF Ideas · Tactical Read · Upcoming Catalysts | 3 |
| `strategy-insights` | markets | Executive Summary · Asset Allocation · Top-Performing ETFs · Risk Management Signals · Sector Rotation Strategy · Fixed Income Strategy · Geographic Allocation · Strategic Recommendations · Risk Considerations · Market Environment Assessment | 3 |
| `chase-rewards` | rewards | Transfer Bonuses · Sign-up Bonuses · Earning & Accumulation · Referral Bonuses · Other Program News · Honorable Mentions | 5 |
| `card-bonuses` | rewards | Top Picks This Week · Personal Cards · Business Cards · Newly Elevated & Limited-Time · Application Rules & Other News · Honorable Mentions | 5 |
| `transfer-bonuses` | rewards | At a Glance · Ending Soon · Just Launched · Sweet Spots · Transfer Program News · Honorable Mentions | 5 |
| `shopping-portals` | rewards | Top Portal Bonuses This Week · Cashback Portals · Browser Extensions & Setup · Stacking & Gift Card Plays · Shopping Events & Deadlines · Other Shopping News · Honorable Mentions | 5 |
| `cashback-leaderboard` | leaderboard | This Week's Standouts · Leaderboard by Store · How to Use This · Methodology | 0 |

The market topics share three market-news feeds; the rewards topics share five points-and-miles
blogs. The leaderboard has no feeds at all: the agent fetches twelve retailers' comparison pages on
a cashback-tracking site, listed in `topics.json`, and copies the live rates verbatim. All eight
feeds fetched on 2026-10-14. A rewards section the week gave nothing for is omitted, never explained,
down to a floor of two sections.

## ✅ What the runner checks

`## Not Financial Advice` is the last section and carries the fixed sentence; at least the topic's
minimum number of sections are used; at least six distinct source links; `topic` and `story_count`
in the final JSON; and for `trade-ideas`, the paper-only line and a Risk column in each idea table.
Markdown tables are allowed here; the markets topics are mostly tables.

## ▶️ Run it

```bash
python recipes/finance-digest/run.py --output-dir ~/ai-output --topic card-bonuses
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../comics/README.md">Next: Comic →</a>
</p>
