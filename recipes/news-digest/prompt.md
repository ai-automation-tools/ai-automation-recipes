# News Digest — {{TOPIC_NAME}}

Goal: write a **briefing on {{TOPIC_NAME}} for the window {{WINDOW}}**, from the feed items the
runner fetched, plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE BEAT

{{FOCUS}}

Earlier editions on every topic (date · topic · title — summary), so you can notice a story that is
a continuation and say so:

{{EXISTING}}

--------------------------------------------------
## THE CANDIDATES

These are the items the topic's feeds carried in the window, newest first, capped so no single
publication crowds out the rest. **Every story you write comes from this list.** Use **WebFetch** on
an item's URL when its description isn't enough to write two honest sentences; don't search the web
for stories the feeds didn't carry. A story that appears in several feeds is one story: link the
best version and mention the others' angle if it adds something.

{{CANDIDATES}}

--------------------------------------------------
## HOW TO READ IT

- **Consequence over volume.** Pick what changes something for the reader, not what was published
  most. A dozen items on one announcement is one story.
- **Say what is confirmed and what is claimed.** A company's number is "<Company> says"; a
  regulator's is a fact; a report citing unnamed sources is "<Outlet> reports". Keep the difference.
- **Exact dates (`YYYY-MM-DD`)** from the item, never "this week" or "recently".
- **Real people appear in words only** when the news is about them; keep it to what the source says,
  no characterisation. The cover is abstract (below).
- **Thin topics say so.** If the window was quiet, write the shorter edition the material supports
  and say in the intro that it was a quiet week. Never pad, never invent.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "{{EMOJI}} {{TOPIC_NAME}} — <Month D, YYYY>"
date: {{DATE}}
type: news-digest
topic: {{TOPIC}}
window: "{{WINDOW}}"
story_count: <distinct stories linked, across every section>
tags: [news, {{TOPIC}}]
---

# {{EMOJI}} {{TOPIC_NAME}} — <Month D, YYYY>

> <One or two sentences: the shape of the week on this beat.>

## Top Stories

### [<Headline, yours, not the publisher's>](<url>)
<Two or three sentences: what happened, why it matters, what is still open. End with the source and
date in italics: *<Publisher>, YYYY-MM-DD*.>

<…five to eight stories…>

## <section>

- **[<Headline>](<url>)** — <one sentence>. *<Publisher>, YYYY-MM-DD*
<…two to five items per section. Use the sections below, in this order, and drop a section the
week gave nothing for…>

## Watchlist

- <Three to five things to watch next: a date, a decision pending, a trial reporting, a deadline.
  Each tied to a story above.>

## Sources

- [<Publisher — item title>](<url>)
<…every URL you linked anywhere in the file, once…>
```

The topic's sections:

{{SECTIONS}}

Rules the runner checks: `## Top Stories`, `## Watchlist` and `## Sources` present; at least three
of the topic's sections used; at least eight distinct story links; **no markdown tables** (the
digest is lists and prose). Every link is a URL from the candidate list or a page you fetched from
one; nothing from memory.

--------------------------------------------------
## WRITING

{{SKILLS}}

Load `llm-writing` and `humanizer` before you write, and run `humanizer`'s final pass before you
save. Carve-outs: skip their workflow and output steps (no audit, no report, no questions); the
shape above wins on structure; attribution ("<Company> says", "<Outlet> reports") is the beat's
honesty, not hedging to strip. Watch repetition across items: forty bullets that all open with the
subject's name read like a wire feed. Lead with the consequence, the number, the odd detail, the
actor, by turns.

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. Motif for this topic: **{{MOTIF}}**. Fixed palette: **{{PALETTE}}**.
Abstract and editorial: no people, faces, flags, logos, maps with readable names, screens, lettering
or numerals; the nouns that render those conventions will add invented text, so describe the motif
instead. Vary composition and light from edition to edition, never the palette. End with the skill's
constraint block, verbatim. The runner renders it at 16:9; don't put the ratio in the prompt.

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
