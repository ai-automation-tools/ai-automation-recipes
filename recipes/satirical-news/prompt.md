# Satirical News — The Overcorrect

Goal: publish **one satirical, Onion-style news article** under the masthead **The Overcorrect**: a
deadpan newswire report of an absurd premise, with a metadata sidecar and, when the runner can
render them, a cover, a square thumbnail and two in-article illustrations.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Beat: `{{BEAT}}`** — {{BEAT_GUIDE}} Chosen by the runner so the archive rotates through all
twelve beats; the article's `news_category` is this label unless a requested topic clearly belongs
elsewhere. The twelve, for reference:

{{BEATS}}

{{TOPIC}}

**The archive so far** (date · slug · headline — summary). Do not reuse a headline, premise, joke or
angle that is already here.

{{EXISTING}}

--------------------------------------------------
## OPTIONALLY ANCHOR TO A TRUE EVENT

Some articles should be **inspired by a real, current event**. If you choose to, use **WebSearch**
to find a genuine recent story on the beat, then **satirize** it — exaggerate it to absurdity,
invert it, or follow its logic to a ridiculous conclusion. Set `based_on_true_event: true` and put
the real story's URL in `inspired_by`. Others can be pure invention (`false`, no `inspired_by`).
Either way the finished piece is **clearly satire**, never presented as a real report.

--------------------------------------------------
## VOICE & TONE (write like The Onion)

- **Deadpan.** Report the absurd in a completely straight, authoritative newswire voice. The comedy
  comes from treating a ridiculous premise with total journalistic seriousness.
- **Headline first.** The headline is the joke's delivery mechanism — punchy, specific, often a
  complete gag on its own ("Area Man Passionate Defender Of What He Imagines Constitution To Be").
- **Escalate.** Each paragraph raises the stakes or adds a stranger detail.
- **Fake quotes and experts.** Invent sources — "at press time", a spokesperson, a bewildered
  bystander, a study, a wildly overconfident expert — with absurd but human-sounding quotes.
- **Funny, ridiculous and sometimes mean is fine** — sharp, cutting satire is the point. Punch at
  power, institutions, trends and human folly.

### Hard guardrails (do not cross)

- **No slurs, no hate**, and no jokes whose punchline is a **protected class** (race, religion,
  ethnicity, gender, sexual orientation, disability). Satire targets behaviour, power and ideas —
  not identity.
- **No private individuals.** Real named targets may only be **public figures** (politicians, CEOs,
  celebrities) and only as **obvious parody**. Do not invent a real, defamatory factual claim about
  a real person (accusing a real living person of an actual crime). Absurd, clearly fictional quotes
  and situations are the parody register — keep it plainly unbelievable.
- **No real-world harm:** no instructions for violence, weapons or self-harm, no sexual content, no
  doxxing, no real personal data.
- The artifact must read as **satire/comedy**, not as a genuine news report or a hoax intended to
  deceive.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write anything, and run `humanizer`'s final pass
on your own draft before you save it.** Deadpan satire dies the second it sounds like a language
model wrote it. Three carve-outs, because those skills were written for an interactive session:

- **Ignore their workflow and output instructions** — no audit, no diff, no before/after table, no
  questions. The files below are the only output.
- **"Personality and soul" means *The Overcorrect's* voice** — straight-faced and institutional. The
  personality lives in the specific detail and the invented sources' quotes, never in the reporter.
- **Keep the deliberate comic devices.** An escalating triad or a repeated construction is joke
  architecture here, not rule-of-three padding.

The pass applies to **everything a reader sees** — the headline, the body, and the `Key Points` and
`Summary` in the sidecar. A humanized article under a "This piece highlights the growing tension
between…" summary gives the whole thing away.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `article.md`

Frontmatter is the **very first bytes of the file**. Exact shape:

```markdown
---
title: "<THE HEADLINE — no quotes inside the value>"
slug: <headline-slug>
date: {{DATE}}
type: satirical-news
publication: The Overcorrect
news_category: "<one of the twelve beats, exact label>"
dateline: "<CITY, ST>"
byline: "The Overcorrect Staff"
based_on_true_event: <true | false>
inspired_by: "<the real story's URL — only when based_on_true_event is true; omit the key otherwise>"
tags: [satirical-news, satire, the-overcorrect, "<beat as a kebab tag>"]
---

# <THE HEADLINE>

**<CITY, ST>** — <Opening paragraph in deadpan newswire voice that states the absurd premise as
established fact.>

![<cover caption>](cover.png)

<2–4 body paragraphs that escalate the premise, with at least two invented quotes from
named-but-fictional sources or clearly-parody public figures.>

![<supporting caption 1>](images/supporting-1.png)

<More body — a fake study, statistic, spokesperson or bystander reaction.>

![<supporting caption 2>](images/supporting-2.png)

<A final beat. Close on the signature kicker, often beginning "At press time, …".>
```

The body runs a tight **350–650 words** (the runner counts; image lines don't count). Satire is
sharper short. Keep the image lines even if the runner may not render the pictures: a missing file
is a broken image, a missing line is a different article.

### `metadata.md`

```markdown
---
title: "<same headline>"
date: {{DATE}}
type: satirical-news
publication: The Overcorrect
news_category: "<same beat>"
dateline: "<CITY, ST>"
based_on_true_event: <true | false>
---

# <Headline>

**Category:** <beat> · **Dateline:** <CITY, ST> · **Based on a true event:** <Yes | No>

## Key Points

- <one-line satirical takeaway>
- <one-line satirical takeaway>
- <one-line satirical takeaway>

## Summary

<2–3 sentence plain summary of the article's joke and its target, for a card or an email.>
```

--------------------------------------------------
## THE PICTURES

Load `image-prompt-craft` before writing any prompt; this section wins where they differ. All four
are illustrations for a satirical article, styled as **polished editorial / mock-photojournalism**:
cinematic, believable-looking news imagery of an absurd scene, tasteful visual comedy, **no real
logos, no readable body text, no real identifiable people**. A newspaper-masthead *feel* is fine; the
moment a prompt names a literal object that carries text (a front page, a lower-third, a protest
sign) the model renders garbled lettering, so describe the scene and let the newsroom feel come
from lighting and framing.

- **One publication shot all four.** There is no memory between image calls. Compose the style and
  palette clauses once and paste them **verbatim** into every prompt; vary only the scene, framing
  and light.
- **Play it straight.** The comedy is in the absurd content rendered soberly. Single-focus scenes;
  crowded satirical scenes read as noise.
- End every prompt with the skill's constraint block verbatim.

| File | Aspect | What |
|:---|:---|:---|
| `cover_prompt` → `cover.png` | 16:9 (runner) | The lead hero — the article's main editorial image. |
| `images/thumbnail.png` | `1:1` | A tighter, simpler crop of the same subject for a square feed card. |
| `images/supporting-1.png` | `3:4` | First in-article illustration — a different beat of the story. |
| `images/supporting-2.png` | `16:9` | Second in-article illustration — another scene. |

List the three `images` entries in the final message in that order.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<the headline>",
  "slug": "<headline-slug>",
  "summary": "<the Summary paragraph>",
  "beat": "<the news_category label>",
  "based_on_true_event": <true | false>,
  "cover_prompt": "<the full cover description>",
  "images": [
    {"file": "thumbnail.png", "prompt": "<…>", "aspect": "1:1"},
    {"file": "supporting-1.png", "prompt": "<…>", "aspect": "3:4"},
    {"file": "supporting-2.png", "prompt": "<…>", "aspect": "16:9"}
  ],
  "error": null
}
```
