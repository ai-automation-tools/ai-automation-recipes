# Finance Digest — {{TOPIC_NAME}}

Goal: write **{{TOPIC_NAME}} for the window {{WINDOW}}**, from the feed items the runner fetched and
the public pages you read, plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE BEAT

{{FOCUS}}

**Rules for this topic.** {{RULES}}

{{STORES}}

Earlier editions on every topic (date · topic · title — summary), so you can notice a story that is
a continuation and say so:

{{EXISTING}}

--------------------------------------------------
## THE CANDIDATES

Feed items from the window, newest first, capped so no single publication crowds out the rest.
Every rewards item and every news theme you write comes from this list; use **WebFetch** on an
item's URL when its description isn't enough to write two honest sentences.

{{CANDIDATES}}

**Market figures are different.** The feeds carry narrative, not numbers. For a `markets` topic,
read the levels off public pages — an index quote page, an exchange's weekly summary, the U.S.
Treasury's daily yield-curve table, an ETF's own fact page — with **WebSearch** to find them and
**WebFetch** to read them, and cite the page next to the number or in the table's source line. A
number you did not read on a page is a number you do not write: put `data unavailable` instead.
This topic's kind is `{{KIND}}`.

--------------------------------------------------
## HOW TO READ IT

- **Money first, prose second.** The rate, the points, the spend, the level, the date. Then one
  sentence on why it matters.
- **Say what is confirmed and what is claimed.** An issuer's terms are a fact; a blogger's
  valuation is "<Outlet> estimates".
- **Exact dates (`YYYY-MM-DD`)** from the item, never "this week" or "soon". An offer with no
  stated end date gets `see source`, never a guess.
- **One item, one section.** If several outlets cover the same offer, link the best version once.
- **Omit, don't explain.** A section the week gave nothing for is left out entirely — no heading,
  no "(none)", no sentence saying it was quiet — as long as at least {{MIN_SECTIONS}} of the
  topic's sections remain. The intro may say it was a thin week.
- **No hype.** "This deal is insane" is a failed line. State the rate and the portal.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "{{EMOJI}} {{TOPIC_NAME}} — <Month D, YYYY>"
date: {{DATE}}
type: finance-digest
topic: {{TOPIC}}
window: "{{WINDOW}}"
story_count: <distinct source links across the whole file>
tags: [finance, {{TOPIC}}]
---

# {{EMOJI}} {{TOPIC_NAME}} — <Month D, YYYY>

> <One or two sentences: the shape of the week on this beat.>

## <the topic's sections, in the order below>

<Rewards topics: one `### <factual headline>` per item, then a short bullet block —
**Source**, **Link** `[<Outlet>](<url>)`, **Ends** (only if stated), **What** (one sentence),
**Why it matters** (one sentence) — plus the per-topic fields its rules name (Issuer and Annual
fee; From / To / Bonus / Effective rate; Portal and Rate). Honorable Mentions is a plain bullet
list: `- [title](url) — one line`.>

<Markets topics: tables where the section is a table (indices, sectors, movers, earnings, ideas,
allocations), each with a source line under it; paragraphs where it is a read. Tables are welcome
here.>

## Not Financial Advice

{{DISCLAIMER}}
```

The topic's sections, in this order:

{{SECTIONS}}

Rules the runner checks: the file **ends** with `## Not Financial Advice` carrying that exact
sentence; at least {{MIN_SECTIONS}} of the sections above are used; at least six distinct source
links across the file; `story_count` matches; and for Trade Ideas, the line
`{{PAPER_LINE}}` sits directly under the H1 and every idea table has a `Risk` column.

--------------------------------------------------
## WRITING

{{SKILLS}}

Load `llm-writing` and `humanizer` before you write, and run `humanizer`'s final pass before you
save. Carve-outs: skip their workflow and output steps (no audit, no report, no questions); the
shape above wins on structure; `see source` and `data unavailable` are the beat's honesty, not
hedging to strip. Watch repetition across items: thirty headlines that all open with the card's
name read like a press-release feed.

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. Motif for this topic: **{{MOTIF}}**. Fixed palette: **{{PALETTE}}**.
Abstract and editorial: no people, faces, logos, card art, tickers, screens, charts, currency
symbols, lettering or numerals; the nouns that render those conventions add invented text and real
brand marks, so describe the motif instead. Vary composition and light from edition to edition,
never the palette. End with the skill's constraint block, verbatim. The runner renders it at 16:9;
don't put the ratio in the prompt.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "{{EMOJI}} {{TOPIC_NAME}} — <Month D, YYYY>",
  "slug": "{{TOPIC}}",
  "summary": "<the intro sentence>",
  "topic": "{{TOPIC}}",
  "story_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
