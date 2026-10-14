# Trending Movers

Goal: write this period's **star-velocity leaderboard for all of open source** from a measured,
pre-sorted candidate list, plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE ONE THING THIS DIGEST IS FOR

**A repo's position is its stars gained this week.** Not its total, not your judgement of its
importance. `top-10-github-repos` ranks by editorial judgement and `oss-spotlight` explains the week;
this one measures it. Two consequences, and they are absolute:

1. **The order is given to you.** The candidates below arrive sorted by `starsThisWeek`, descending.
   Publish that order. You may drop an entry (which closes the gap); you may never reorder.
2. **Every published entry carries a real weekly figure.** A candidate without `starsThisWeek` does
   not go on the leaderboard. Never estimate one, carry one over, derive one from the total, or round
   a total into a "gain".

The runner checks both: a figure that doesn't match the measurement, or an out-of-order leaderboard,
fails the run.

--------------------------------------------------
## THE CANDIDATES (measured — reproduce the numbers exactly)

Scraped from GitHub's weekly trending pages (all languages, plus Python, TypeScript, JavaScript, Rust
and Go), deduped, sorted by weekly gain. `stars` is the running total; `description` is GitHub's
one-line blurb — a lead, never your sentence.

{{CANDIDATES}}

**If the candidate fetch failed, stop:** end with the FINAL MESSAGE and set `"error"` to "candidate
fetch failed". A leaderboard without measurements is the failure this recipe exists to prevent.

**Don't go looking for more repos.** A repo found by searching has no weekly figure attached. Use
**WebFetch** only to verify the repos you publish and to find what caused a surge.

--------------------------------------------------
## REPEATS ARE EXPECTED — DON'T DEDUP THEM AWAY

The one digest where a repeat is **correct**: a repo that gained 8,000 stars two weeks running belongs
at the top both weeks. What you owe a returning repo is a **different sentence** — say what changed
and note the trajectory ("third week running, gain slowing from 9,100 → 6,400"). Recent leaderboards:

{{HISTORY}}

--------------------------------------------------
## BUILD THE LEADERBOARD

- **The Leaderboard:** the top **12–15** candidates by weekly gain, in the given order.
- **Also Climbing:** a further **5–10** as one-line bullets, same order.
- **All of open source** — no topic filter. A Rust game engine, a font, a kernel tool and an LLM
  framework all belong if the numbers put them there.
- Each leaderboard entry gets 2–3 sentences: what the project is and — where you can establish it —
  **what caused the surge** (a launch post, a release, a talk, a viral thread, an acquisition). If you
  can't find a cause, leave it out rather than inventing one.
- Verify every repo: WebFetch it, drop it if it 404s or is archived, publish the final URL after a
  rename. A dropped entry closes the gap; the next candidate moves up.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

**Keep this structure exactly** — the runner and the bookmark export parse it.

```markdown
---
title: "Trending Movers — {{DATE}}"
date: {{DATE}}
type: trending-movers
site_count: <leaderboard + also-climbing count>
categories: [<the category values you used>]
tags: [github, trending, open-source, stars, momentum]
---

# Trending Movers — {{DATE}}
**As of:** {{DATE}}
**Focus:** The GitHub repos gaining the most stars this week — momentum and breakouts across open source.
**Method:** Ranked by stars gained over the past week, scraped from GitHub's weekly trending pages.

---

## Overview

<3–5 sentences on where the momentum went: the themes the numbers show, anything unusual — one repo running away with the week, a language over-represented, a page that failed to fetch. Not a list of the entries.>

---

## The Leaderboard

### 1. [<owner/repo>](https://github.com/<owner>/<repo>)
- **Stars this week:** +<N,NNN>
- **Category:** <one value from the list below>

<2–3 sentences.>

<...through the last leaderboard entry...>

---

## Also Climbing

- [<owner/repo>](https://github.com/<owner>/<repo>) — +<N,NNN> this week — <one-line note>

---

## Sources

- GitHub Trending (weekly) — https://github.com/trending?since=weekly
- <every other URL referenced>
```

**`Category` is a closed list — use these strings verbatim:**
`AI/ML` · `Dev Tools` · `CLI` · `Web` · `Data` · `Infra/DevOps` · `Security` · `Other`
(`Other` is for the genuinely uncategorisable — a font, a game, a dataset.)

Body rules:

- Headings are `### <N>. [owner/repo](url)` — the slug, linked, not a prettified name.
- The two bullets come first, in that order. An optional `- **Stars:**` total (only if you read it on
  the page) goes after **Stars this week:**.
- Weekly figures as `+12,345` — leading plus, thousands separators, the measured number.
- No `**Pricing:**` or `**Replaces:**` clauses.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap is the surge sentence: fifteen entries that each "have been gaining significant
traction in the developer community" is fifteen copies of nothing. Either you found the cause and can
name it, or you skip the clause.

--------------------------------------------------
## COVER IMAGE

Motif: abstract **"velocity"** — steep rising curves, particle trails, forms accelerating out of frame.
Fixed palette: **deep charcoal, warm amber, burnt orange, off-white**.

Dangerous nouns for this digest: "chart", "graph", "bar chart", "leaderboard", "podium", "GitHub",
"octocat", "star icon", "dashboard", "logo". No invented numbers or axis labels.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Trending Movers — {{DATE}}",
  "slug": "trending-movers",
  "summary": "<one sentence on where the momentum went>",
  "site_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
