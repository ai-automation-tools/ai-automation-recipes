# Signal Sources

Goal: research and write this run's **additions to a cumulative reading list** — at least 12 blogs,
newsletters, changelogs, channels, podcasts and leaderboards on AI and technology worth following,
each with its feed URL — plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## WHAT THIS DIGEST IS — AND IS NOT

Every other digest lists things to **use**. This one lists places to **read**. The question that
decides every judgement call: **does this thing publish on a recurring basis?** A tool's homepage
doesn't belong here; its *changelog* does. A one-off essay doesn't; the blog that published it does.

Two consequences shape the job:

- **It is cumulative.** Each run publishes only its **additions**. The durable output is the archive
  as a whole — the runner regenerates an all-time bookmarks file and an OPML feed bundle from every
  run after yours. That makes deduplication the most important step.
- **Feeds are the point.** A source with an RSS/Atom feed can be subscribed to. Find the feed URL
  for every source you can.

--------------------------------------------------
## THE ARCHIVE — NO SOURCE MAY APPEAR TWICE

The reading list already holds **{{ARCHIVE_SIZE}}** distinct sources. Every one of them (date ·
name — URL):

{{FEATURED}}

**A source already listed must not appear again** — not in a different category, not under a slightly
different name, not as `blog.example.com` when `example.com` is listed. Check three ways: **root
domain**, **feed URL**, and **publication name** (a rebranded blog is the same blog). If the archive is
empty, aim for the high end of the range.

--------------------------------------------------
## RESEARCH

Where to look:

- Blogrolls and "who I read" posts from people working in the field; link sections of established
  newsletters.
- Lab and vendor engineering blogs, research pages and changelogs — the changelog is often the
  higher-signal feed.
- Substack, Buttondown and Ghost discovery pages; domains that recur on Hacker News.
- Conference and workshop sites that publish talks; university lab pages.
- Podcast directories; YouTube channels that publish on a schedule.
- Benchmark and leaderboard pages that update continuously.
- Focused subreddits, forum announcement boards.

**What earns a slot:**

- **Publishes recurrently and is alive** — at least roughly monthly, with something dated in the last
  **90 days**. A blog whose newest post is two years old is an archive, not a source.
- **Primary or genuinely additive** — the lab that did the work, the maintainer who shipped it, a
  person with a specific vantage point. Skip aggregators that restate other people's posts, SEO filler
  and affiliate content.
- **Readable without a hard paywall.** A paid tier is fine if the free tier carries real content.
- **Not already obvious** — assume the reader knows Hacker News, TechCrunch, The Verge and the OpenAI
  blog. Include a major outlet only for a specific high-signal sub-feed, and link that.
- **Has a feed, ideally.** Not required, but prefer the source with one when two are otherwise equal.

**Verify the feed.** WebFetch it and confirm it returns XML starting `<rss`, `<feed` or `<?xml`. A feed
URL guessed from a CMS pattern (`/feed`, `/rss.xml`, `/atom.xml`) is a guess until fetched. If you
can't confirm one, write `none` — honest and harmless.

--------------------------------------------------
## CATEGORIES

**5–8 categories, 2–4 sources each, at least 12 in total** (aim for 12–20). Rotate the mix; add a
sensible new category when one fits.

- **Research & Labs** — lab blogs, paper feeds, research newsletters
- **Engineering Blogs** — how teams actually built and ran the thing
- **Newsletters** — curated regular sends worth the inbox slot
- **Changelogs & Release Feeds** — vendor and project release notes
- **Practitioners & Independents** — individual writers with a specific vantage point
- **Video & Podcasts** — channels and shows on a publishing schedule
- **Benchmarks & Leaderboards** — continuously updated evaluation and tracking pages
- **Docs & Reference Hubs** — living documentation, spec sites, standards trackers
- **Communities & Forums** — focused discussion venues with a readable feed
- **Policy & Industry** — regulation trackers, funding and market analysis

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "Signal Sources — <Month YYYY>"
date: {{DATE}}
type: signal-sources
site_count: <number of sources added this run>
archive_total: <{{ARCHIVE_SIZE}} + site_count>
categories: [<the category names you used>]
tags: [signal-sources, reading, rss, newsletters, blogs]
---

# Signal Sources — <Month YYYY>

> <One sentence: N sources added this run, bringing the reading list to <archive_total>.>

## 🔬 Research & Labs

### [<Source Name>](<https homepage URL>)
<1–2 sentences: what it publishes and whose vantage point it gives you.> **Cadence:** <weekly / ~monthly / on release / daily>. **Feed:** <the RSS or Atom URL, or `none`>.

<...every category, every source in the same shape...>

---

*<total> sources added this run · <archive_total> on the list.*
```

Rules for the body:

- Every source is a `### [Name](URL)` link, the description, then **Cadence:** and **Feed:** in the
  same paragraph. **Feed:** is machine-read for the OPML bundle — a bare URL or the word `none`, never
  prose, never a markdown link.
- The `### [Name](URL)` target is the **homepage**; the feed goes in **Feed:**. Swapping them breaks
  both the bookmarks file and the OPML.
- A leading emoji on each `##` category heading. Don't number sources.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap: descriptions of publications collapse into one sentence with the nouns swapped —
"a weekly newsletter covering the latest in X", twelve times. Answer "why would I read this instead of
the twenty others like it?" — the writer's actual job, the beat nobody else covers, the fact that it
is three paragraphs and always on time.

--------------------------------------------------
## COVER IMAGE

Motif: abstract **"incoming signal"** — concentric broadcast rings, drifting particles, layered
horizon bands. Fixed palette: **deep teal, warm sand, muted coral, off-white**.

Dangerous nouns for this digest: "newspaper", "magazine", "article", "page", "RSS icon", "newsletter",
"inbox".

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Signal Sources — <Month YYYY>",
  "slug": "signal-sources",
  "summary": "<the intro sentence>",
  "site_count": 0,
  "archive_total": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
