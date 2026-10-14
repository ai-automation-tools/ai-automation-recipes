# Future Cities 2500

Goal: imagine ONE real city as it might exist in the **year 2500** and write the prompt for a
single high-definition, cinematic 16:9 cityscape, which the runner renders.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**City: `{{CITY}}`** — chosen by the runner from the city list, least-used first.

**Cities already imagined** (date · slug · title — caption). Keep this one distinct in mood,
palette and big idea:

{{EXISTING}}

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `image-prompt-craft` before you write the image prompt** and end the prompt with its
constraint block, verbatim. **Load `llm-writing` before you write `city.md`**; skip its
audit/report steps.

--------------------------------------------------
## THE VISION

You are a visionary futurist and concept artist. Extrapolate boldly but plausibly from the
city's real geography, landmarks, culture and climate, about 475 years forward:

- radical architecture and megastructures; transport (aerial craft, maglev, arcologies);
- energy, ecology and climate adaptation (sea-level change, green infrastructure);
- how the city's iconic identity survives or transforms.

**Keep it recognisably {{CITY}}.** A viewer who knows the city should be able to name it from
its landmarks and geography, not from the filename. Never a generic sci-fi skyline.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `city.md`

```markdown
---
title: <a title for this vision>
date: {{DATE}}
city: {{CITY}}
year: 2500
style: <e.g. photorealistic cinematic future-city concept art>
signature_landmarks: [<landmark>, <landmark>]
keywords: [<word>, <word>, <word>]
---

# {{CITY}}, 2500: <title>

> <one-sentence caption>

## Vision

<One paragraph, 80–140 words: what the city became and why it is still unmistakably itself.>
```

--------------------------------------------------
## THE IMAGE PROMPT

One extremely detailed prompt for a photorealistic cityscape:

- a **wide cinematic establishing shot** — a sweeping vista or elevated skyline view;
- the city's real, iconic landmarks and geography reinterpreted for 2500, named in the prompt;
- architecture, materials, lighting, atmosphere, weather, time of day, sky, reflections, scale;
- believable future life at scale: transport, energy and ecological systems, crowds;
- dense layered detail from foreground activity to a distant horizon — one continuous scene,
  never a grid of panels;
- **a named colour grade** of three or four colours the city earns (Reykjavik and Marrakech
  should not share one);
- **no text and no signage** anywhere — end with the skill's constraint block, verbatim.

Never write the aspect ratio into the prompt.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<title for this vision>",
  "slug": "<kebab-case-city-name>",
  "summary": "<the caption>",
  "city": "{{CITY}}",
  "style": "<the style>",
  "images": [
    {"file": "cityscape.png", "aspect": "16:9", "prompt": "<the full cityscape prompt>"}
  ],
  "error": null
}
```
