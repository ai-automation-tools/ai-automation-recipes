# Top 10 GitHub Repos

Goal: rank and write this period's **top 10 AI and developer-tooling repositories** from a
pre-fetched trending candidate list, plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE CANDIDATES — PICK FROM THESE, DON'T GO LOOKING

GitHub Trending's weekly feeds (all languages, plus Python, TypeScript, JavaScript, Rust and Go),
deduped and filtered to AI and developer tooling. `description` is the head of each README, scraped
from the feed — a lead, never your sentence; half of it is badges and boilerplate.

{{CANDIDATES}}

**Pick your ten from this list.** This digest's claim is "what is actually trending on GitHub right
now" — a repo found by searching is evidence of searching, not of trending. Two narrow exceptions:

- If fewer than 15 candidates arrived (or the fetch failed), top the shortlist up with **WebSearch**
  and say so in the Overview.
- Always **WebFetch** the repos you shortlist — that is verification, not discovery.

--------------------------------------------------
## AVOID REPEATS

Repos earlier runs of this recipe featured (date · name — URL). **Prefer repos that haven't appeared:**

{{FEATURED}}

A dominant repo can sit on Trending for months. It may return **at least 6 weeks** after it was last
covered if something real changed — a major release, a rewrite, a licence change, a surge with a
cause. Say so ("last covered YYYY-MM-DD; returns because …"). "Still trending" is not a reason. Dedup
against this recipe only; overlap with `oss-spotlight`, `trending-movers` or `agent-toolkit` is fine.

--------------------------------------------------
## PICK THE TEN

Shortlist ~15, then cut to 10 on:

- **Relevance** — AI tools, agents, automations, integrations, MCP, CLIs, developer tooling. A
  trending game engine is not this list.
- **Momentum with a cause** — a release, a launch post, a rewrite, a spec landing.
- **Substance** — a README that says what it does, non-trivial scope. Awesome-lists, tutorials,
  interview-prep collections and course dumps are drops, however high they trend.
- **Freshness** — prefer repos not featured before.

**Order matters:** #1 is the strongest pick, #10 the weakest; make it defensible. **Mix new and
established:** tag each `New`, `Trending` or `Popular & active`, with at least 3 `New` and 3 `Trending`.

**Star counts are optional and must be read on the page.** If WebFetch shows a current count, include
`- **Stars:**` with thousands separators; otherwise omit the bullet. Never estimate one, and never
take the candidate list's `stars` unless you saw it on the page.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

**Keep this structure exactly** — the numbered `##` heading, the `- **Repo:**` bullet and the
`- **Category:**` bullet are parsed by the runner and the bookmark export.

```markdown
---
title: "Top 10 GitHub Repos — <Month D, YYYY>"
date: {{DATE}}
type: top-10-github-repos
site_count: 10
categories: [<the category values you used>]
tags: [github, repos, ai, agents, mcp, developer-tools, trending]
---

# Top 10 GitHub Repos — {{DATE}}
**As of:** {{DATE}}
**Focus:** AI tools, automations, agents, integrations, MCP, CLIs and developer tooling.
**Snapshot:** Current trending picks at the moment of generation — not a historical recap.

---

## Overview

<3–5 sentences on what this set shows: the dominant themes, anything unusual — a major release, a category suddenly crowded, a feed that failed. A read on the ten, not a list of them.>

---

## 1. <Repo Name>

- **Repo:** https://github.com/<owner>/<repo>
- **Category:** <one value from the list below>
- **Status:** <New | Trending | Popular & active>

<2–4 sentences: what it does, who it is for, and what is driving it right now.>

**Why it's on the list:** <one line — the takeaway, not a summary of the paragraph>

---

<...same shape through #10...>

## Honorable Mentions

<0–5 bullets: `- [<owner>/<repo>](https://github.com/<owner>/<repo>) — <one-line note>`>

---

## Sources

<Every URL referenced: `- <Title or descriptor> — <URL>`>
```

**`Category` is a closed list — use these strings verbatim (the runner rejects anything else):**
`AI Agents` · `AI Tools` · `AI/ML` · `MCP` · `CLI` · `Automations` · `Integrations` ·
`Developer Tools` · `Open Source` · `Data` · `Security`

Body rules:

- `## <N>. <Repo Name>` uses a readable project name; the `owner/repo` slug lives in the **Repo:** URL.
- The bullets come first, in order (**Repo**, optional **Stars**, **Category**, **Status**), before
  any prose. **Why it's on the list:** is the last line of each entry.
- No `**Pricing:**` or `**Replaces:**` clauses.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap: every README opens "A powerful, extensible framework that empowers developers
to…". Ten paraphrases of that is ten copies of one sentence.

--------------------------------------------------
## COVER IMAGE

Motif: abstract **"ranked ascent"** — stepped strata, stacked planes, rising layered forms. Fixed
palette: **deep navy, sky blue, pale gold, off-white**.

Dangerous nouns for this digest: "GitHub", "octocat", "repository", "code editor", "terminal",
"leaderboard", "podium", "logo", "app icon".

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Top 10 GitHub Repos — <Month D, YYYY>",
  "slug": "top-10-github-repos",
  "summary": "<one sentence from the Overview>",
  "site_count": 10,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
