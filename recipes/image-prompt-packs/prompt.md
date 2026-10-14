# Weekly Image Prompt Pack

Goal: write ONE themed pack of 5–8 polished, reusable image-generation prompts, each with a
rendered example the runner makes from your prompt.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Suggested theme: `{{THEME}}`.** Use it unless a pack below already covered it, or you have a
more distinct, visually richer idea — then pick a new theme no earlier pack used.

**Packs already published** (date · slug · title — intro). Don't repeat a theme:

{{EXISTING}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `image-prompt-craft` before you write a single prompt.** Every prompt in the pack follows its
formula (subject → style → palette → composition → mood → constraints) and its "name the right
object" rule. Ignore its verify-the-render loop: you never see the renders.

**Load `llm-writing` and `humanizer` before writing the pack's prose** (the intro and each use
case) and run `humanizer`'s final pass on that prose. They never touch the prompts themselves —
prompt language is a register of its own. Skip their audit/report steps.

--------------------------------------------------
## THE PACK

- 5–8 prompts, each exploring a **different facet** of the theme: subject, scale, mood, medium.
- Evocative and specific: sensory detail and concrete style references, not stacked adjectives.
- Style tags that work with current diffusion models.
- Each prompt is a complete, standalone prompt someone can paste into an image tool.
- The `aspect` you give each example must be one of: `1:1`, `16:9`, `9:16`, `3:2`, `2:3`, `4:3`, `3:4`.
- No real people, no brand logos, no copyrighted characters.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `pack.md`

```markdown
---
title: <Pack Title>
date: {{DATE}}
theme: <theme>
prompt_count: <N>
---

# <Pack Title>

<2–3 sentence introduction: what the pack is and who it's for.>

## <Prompt 1 title>

![<Prompt 1 title>](images/<file-1>.png)

> <the primary prompt, exactly as in the final JSON>

- **Negative prompt:** <what to avoid>
- **Aspect ratio:** <aspect>
- **Style tags:** <tag>, <tag>, <tag>
- **Use case:** <one sentence: why someone would use this>

## <Prompt 2 title>
...
```

The images are rendered **after** you finish, from the `images` list in your final JSON. Link
each one by its file name; don't create the files.

--------------------------------------------------
## FINAL MESSAGE

One `images` entry per prompt, in the same order as `pack.md`. `prompt` is the primary prompt
verbatim; `file` is a lowercase kebab-case name ending in `.png`.

```json
{
  "title": "<Pack Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the introduction's first sentence>",
  "theme": "<theme>",
  "images": [
    {"file": "<prompt-1-slug>.png", "prompt": "<primary prompt 1>", "aspect": "16:9"},
    {"file": "<prompt-2-slug>.png", "prompt": "<primary prompt 2>", "aspect": "1:1"}
  ],
  "error": null
}
```
