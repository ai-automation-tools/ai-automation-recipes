# Weekly Wallpaper Pack

Goal: write the image prompts for THREE wallpapers, one per theme the runner picked, plus a short
pack note. Each prompt renders one **square master**; the runner crops a 16:9 desktop wallpaper
and a 9:16 phone wallpaper from the same master.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

The runner chose these themes and a variation for each (lighting, palette, mood, framing), so
runs stay fresh even when a theme comes back. Use them; don't swap themes.

{{PLAN}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `image-prompt-craft` before writing the prompts** and follow its formula. Ignore its
verify-the-render loop — you never see the renders.

--------------------------------------------------
## THE PROMPTS

For each wallpaper, write one continuous prompt that combines the theme's scene, its variation and
its render style (photorealistic or digital art), and adds:

- **Composition for two crops.** The subject sits at the exact center and the scene extends
  evenly to every edge — the desktop crop keeps the middle band, the phone crop keeps the middle
  column. Nothing important near the corners.
- **Wallpaper quality.** Ultra-detailed, high visual depth, clean areas where desktop icons or a
  phone clock will sit.
- **Never** a device, a frame, a border, a UI, or any lettering. End with the skill's constraint
  block, verbatim.
- Don't write an aspect ratio into the prompt; the runner sets it.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `pack.md`

```markdown
---
title: <Pack title naming the three themes>
date: {{DATE}}
---

# <Pack title>

<One or two sentences on the pack as a set.>

## <Theme 1 label>

![Desktop](desktop/<file-1>) ![Phone](mobile/<file-1>)

<One sentence on the mood and what makes this one work as a wallpaper.>

> <the prompt, exactly as in the final JSON>

## <Theme 2 label>
...
```

The images don't exist yet; link them by the paths above.

--------------------------------------------------
## FINAL MESSAGE

`images` must list exactly the planned files, in plan order, all `1:1`. `themes` echoes the
planned slugs: `{{THEME_SLUGS}}`.

```json
{
  "title": "<Pack title>",
  "slug": "<kebab-case-slug>",
  "summary": "<one sentence>",
  "themes": {{THEME_SLUGS}},
  "images": [
    {"file": "<planned file 1>", "prompt": "<prompt 1>", "aspect": "1:1"},
    {"file": "<planned file 2>", "prompt": "<prompt 2>", "aspect": "1:1"},
    {"file": "<planned file 3>", "prompt": "<prompt 3>", "aspect": "1:1"}
  ],
  "error": null
}
```
