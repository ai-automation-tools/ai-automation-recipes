# Yearly Collections

Goal: advance each long-running image collection below by ONE entry — research the entry, write
an entries note, and write one image prompt per entry. The runner renders the images.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

The runner picked the next entry in each active collection. Do exactly these, in this order:

{{PLAN}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `image-prompt-craft` before writing any prompt** and follow its formula. Ignore its
verify-the-render loop — you never see the renders.

**Load `llm-writing` and `humanizer` before writing `entries.md`** and run `humanizer`'s final pass
on its prose. They never touch the image prompts. Skip their audit/report steps.

--------------------------------------------------
## FOR EACH ENTRY

1. **Research** (when the plan says so) with WebSearch and WebFetch. Reliable sources only —
   wire services, major science and history publications, official agency and institution pages.
   Don't rely on memory, and never invent facts or sources.
2. **Choose what to show.** For a year: the 8–12 most significant, visually distinct items, with
   the biggest two or three made prominent. For a list item: what it was, who used it, the era.
3. **Write one prompt** following the collection brief: one unified scene, the brief's style and
   palette, the entry's specifics named concretely.
   - **Lettering:** if the plan gives lettering, quote the exact words in the prompt (for example
     `the year "2003" in bold readable type`) — the runner allows only text quoted in the prompt.
     If the lettering is `none`, ask for no text at all and end with the skill's constraint block.
   - **Never:** real-person likenesses, official logos or brand marks, copyrighted characters,
     graphic injury or casualties.
   - Don't put the aspect ratio in the prompt; the runner sets it.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `entries.md`

```markdown
---
title: Collections — {{DATE}}
date: {{DATE}}
---

# Collections — {{DATE}}

## <Collection title>: <entry label>

![<entry title>](images/<file>)

<2–4 sentences: what this entry shows and why these items were chosen.>

**Featured:**
- <item> — <one line>
- ...

**Sources:**
- <URL> — <what it supports>

**Prompt:**
> <the prompt, exactly as in the final JSON>

## <next collection>…
```

Link each image by its planned file; the images don't exist yet.

--------------------------------------------------
## FINAL MESSAGE

`entries` and `images` both follow the plan order exactly; `file` and `aspect` must match the
plan.

```json
{
  "title": "Collections — {{DATE}}",
  "slug": "collections-{{DATE}}",
  "summary": "<one sentence naming the entries added>",
  "entries": {{ENTRIES_JSON}},
  "images": {{IMAGES_JSON}},
  "error": null
}
```
