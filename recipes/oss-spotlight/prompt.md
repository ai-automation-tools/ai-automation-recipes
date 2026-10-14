# Open-Source Spotlight

Goal: write this period's **six-section editorial read on the open-source ecosystem** — 20–30
entries, each graded by significance — grounded in a pre-fetched list of the period's news, plus a
cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## WHAT THIS DIGEST IS — AND IS NOT

The **editorial** repo digest. `top-10-github-repos` picks the ten strongest AI/dev repos;
`trending-movers` orders all of open source by star gain. Neither explains anything. This one does:
six fixed sections, a short framing paragraph per section, one bullet per project, and a
**Significance** grade instead of a rank. A reader should finish knowing what *happened* in open
source — a release that matters, an argument the community had, a tool worth stealing.

It covers **all** of open source, not only AI. A Postgres extension, a kernel change, a Rust build
tool and a font renderer all belong on their merits. If the digest reads like six sections of
AI-agent projects, the selection failed.

--------------------------------------------------
## THE CANDIDATES — THIS PERIOD'S NEWS

Seven sources — GitHub's blog and open-source feed, GitHub Trending, TLDR Tech, the Hacker News
front page, The Register's software desk and LWN — deduped and filtered. `description` is scraped
feed text: a lead, never your sentence.

{{CANDIDATES}}

**Build the digest from this list.** You have real latitude: use **WebSearch** and **WebFetch** freely
to understand a story, find the release notes behind a headline, or follow something the feeds
surfaced obliquely. What you may not do is write a section with no grounding in this period's
candidates — they are what make it *this* period's digest rather than an essay about open source. If
the fetch failed, research the period's news yourself and say so in the Overview.

--------------------------------------------------
## AVOID REPEATS

Projects earlier runs of this recipe featured (date · name — URL). **Prefer ones that haven't
appeared:**

{{FEATURED}}

A project may return if the *story* is new — a major release, a licence change, a governance fight,
a rewrite. Say so ("last covered YYYY-MM-DD; back because …"). "Still popular" is not a story.

--------------------------------------------------
## THE SIX SECTIONS

Use these headings **exactly**, in this order — the runner rejects any other section name.

| Section | What belongs in it | Entries |
|---|---|---|
| `Project of the Week` | The most consequential project. The longest framing paragraph. | exactly 1 |
| `Top 5 Trending Repos` | What actually gained attention — with a reason, not just a count. | 5 |
| `Notable New Releases` | Versioned releases that change what a thing can do. Name version and date. | 3–6 |
| `Community & Ecosystem News` | Governance, licensing, funding, forks, maintainer news, security disclosures. | 3–6 |
| `Hidden Gems` | Small, underexposed, genuinely useful. 40k stars is not a hidden gem. | 3–5 |
| `Developer Tooling Highlights` | Build tools, editors, CLIs, debuggers, CI, package managers. | 3–5 |

Target **20–30 entries**. Fewer, better-explained entries beat a padded list.

**Grade Significance honestly.** `High`: a working developer changes something this month because of
it — adopts, upgrades, migrates off, patches. `Medium`: worth knowing. `Low`: interesting. Most
periods have one or two Highs; a digest where everything is High has graded nothing.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

**Keep this structure exactly** — the runner and the bookmark export parse each entry line.

```markdown
---
title: "Open-Source Spotlight — <Month D, YYYY>"
date: {{DATE}}
type: oss-spotlight
site_count: <number of projects listed>
categories: [<the section names you used>]
tags: [open-source, oss, github, releases, developer-tools, community]
---

# Open-Source Spotlight — <Month D, YYYY>

**As of:** {{DATE}}
**Focus:** Releases, projects, tooling and community news from across open source.

---

## Overview

<3–5 sentences on what the period showed. Name the through-line if there is one, and say plainly when there isn't — a quiet period reported as quiet beats a manufactured theme.>

---

## Project of the Week

<2–3 sentences of framing: why this one, now.>

- **[<Name>](<https URL>)** (<owner>) — <2–3 sentences: what it does, what changed, who should care.> — Significance: High

## Top 5 Trending Repos

<1–2 sentences of framing.>

- **[<Name>](<https URL>)** (<owner>) — <1–2 sentences.> — Significance: <High | Medium | Low>

<...all six sections...>

---

## Sources

<Every URL referenced: `- <Title or descriptor> — <URL>`>
```

Body rules:

- **One entry per line.** It opens `- **[Name](url)** (owner) —` and closes `— Significance:
  High|Medium|Low`. An entry split across lines is lost.
- `(owner)` is the org or person; drop the parentheses for things with no natural owner (a
  foundation announcement, a standards doc).
- **Significance** is the last thing on the line. Don't number entries; don't repeat a project.
- Exact version numbers everywhere. No `**Pricing:**` or `**Replaces:**` clauses.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap is the section framing: six paragraphs introducing six lists is where "In the
ever-evolving landscape of open source…" comes from. Lead with the specific thing that happened.

--------------------------------------------------
## COVER IMAGE

Motif: abstract **"many hands, one structure"** — interlocking woven forms, converging strands, a
lattice assembled from separate pieces. Fixed palette: **deep forest green, emerald, pale sand,
off-white**.

Dangerous nouns for this digest: "GitHub", "octocat", "penguin", "terminal", "code editor", "git branch
diagram", "logo", "app icon".

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Open-Source Spotlight — <Month D, YYYY>",
  "slug": "oss-spotlight",
  "summary": "<one sentence from the Overview>",
  "site_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
