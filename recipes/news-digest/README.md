<h1 align="center">📰 News Digest</h1>

<p align="center">
  <em>One topic, one week, written from that topic's own feeds: top stories, themed sections, a watchlist, every source.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/topics-9-0078D4?style=for-the-badge" alt="9 topics">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The runner does the fetching: every feed on the topic's list, the last seven days, newest first,
capped at 16 items per publication so one loud feed can't own the week, 150 in all. The agent gets
that list and nothing else to work from. It may fetch an item's page to read it properly; it may not
go looking for stories the feeds didn't carry. What comes back is a briefing a person would
forward, not a feed dump.

| | |
|:---|:---|
| **Output** | `news-digests/<YYYY-MM>/<date>_<topic>/` → `digest.md`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebFetch (no search: the feeds are the beat) |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | The topic's feeds, then article pages |

## 🗞️ Topics

Nine, in [`topics.json`](topics.json), each with its feeds, five sections, a palette and a cover
motif. A run takes the least-covered topic; `--topic energy` forces one. Three runs a week rotates
through all nine every three weeks.

| Topic | Sections | Feeds |
|:---|:---|:-:|
| `ai` | Models & Labs · Agents, MCP & Tooling · Developer Tools · Business & Funding · Research & Policy | 18 |
| `science-space` | Space & Missions · Physics & Astronomy · Life Sciences · Earth & Climate · Methods | 7 |
| `world` | Conflict & Security · Elections · Diplomacy · Economy & Sanctions · Humanitarian & Climate | 10 |
| `tech-policy` | AI Regulation · Antitrust · Privacy & Surveillance · Platforms & Speech · Courts | 10 |
| `energy` | Oil & Gas · Power & Grid · Renewables & Storage · Policy & Markets · Electrification | 10 |
| `gaming` | Studios & Deals · Platforms & Hardware · Releases · Development & Engines · Policy & Labor | 10 |
| `media` | Studios & Streaming · Advertising · Journalism · Music & Audio · Creators | 14 |
| `emerging-tech` | Research Results · In Development · Pilots & Trials · Now Shipping · Coming to the Public | 18 |
| `cybersecurity` | Exploited in the Wild · Patches · Breaches · Threat Actors · Advisories | 11 |

Add a topic by adding an entry; nothing else changes. Feed lists are public RSS and Atom; a dead feed
is skipped and reported in the prompt, never fatal. A window with no items at all fails the run
before the agent starts. Every feed was fetched on 2026-10-14; three publishers that block
non-browser clients outright (CISA's advisories, Fierce Biotech, StreamTV Insider) were swapped for
Krebs on Security, Endpoints News and Next TV. CISA's exploited-vulnerabilities signal still arrives
through the security newsrooms and the vendor blogs.

## What the runner checks

`## Top Stories`, `## Watchlist` and `## Sources` present, at least three of the topic's sections
used, at least eight distinct story links, no markdown tables, and a `story_count` in the final
JSON. The cover is abstract by rule: no faces, flags, logos or lettering, whatever the week's news.

## Run it

```bash
python recipes/news-digest/run.py --output-dir ~/ai-output --topic cybersecurity
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../comics/README.md">Next: Comic →</a>
</p>
