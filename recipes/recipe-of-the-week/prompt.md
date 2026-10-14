# Recipe of the Week

Goal: write ONE popular, family-friendly recipe from this week's cuisine as a clean, cookable
Markdown recipe, plus the description of a cover image.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Cuisine: `{{CUISINE}}`** — chosen by the runner to keep the collection balanced. Do not pick a
different one.

**Recipes already in the collection** (date · slug · title — summary). Do not repeat a dish:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research.** Use **WebSearch** / **WebFetch** to find ONE crowd-pleasing, highly rated dish that
   families actually cook at home from this cuisine — not internet-viral novelty food. Prefer a
   dish with several references from reputable food sites, publications, or well-reviewed
   community recipes.
2. **Load the skills** (below), then write `recipe.md` from the RECIPE TEMPLATE. Stay as close as
   practical to the source recipe — or the consensus of several — while writing it as a clean,
   usable recipe. Say so when you synthesized from more than one source.
3. **Run the `recipe-validator` checks yourself** on the finished draft and fix anything critical
   or high. The runner re-runs the validator's scanner and rejects the recipe on a critical
   food-safety finding.
4. Load `image-prompt-craft` and write the cover description (COVER IMAGE below).
5. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

- **`recipe-validator`** — read its food-safety and nutrition references and apply them to your
  draft: safe cooking temperatures, dangerous ingredient/technique combinations, per-serving
  sodium / saturated fat / added sugar, quantity and ratio sanity, allergen labeling. Its scanner
  script is run by the runner, not by you. If it would flag a genuinely indulgent dish as rich
  rather than unsafe, keep the dish and say so in Chef's Notes.
- **`llm-writing`** + **`humanizer`** apply to the PROSE only — the cultural context, the notes,
  the step wording. Skip their audit/report steps; ask no questions.
- **The template wins on structure.** Never let a prose pass touch a number: a quantity, a
  temperature, a time or a doneness cue is not a style choice.

--------------------------------------------------
## RECIPE REQUIREMENTS

- Genuinely cookable, specific and complete. Preserve the source's distinctive ingredients,
  ratios, techniques, cook times and serving style.
- Frontmatter: realistic `title`, `region` (the cuisine, kebab-case), `yield`, `active_time_min`,
  `total_time_min`, `tags`, `allergens`, `version`, `date`.
- **Allergens — complete and accurate.** List EVERY US Big-9 allergen present, using exactly these
  tokens: `dairy`, `egg`, `fish`, `shellfish`, `tree-nut`, `peanut`, `gluten`, `soy`, `sesame`.
  Check hidden sources: mayonnaise/aioli = egg; fish sauce, Worcestershire, anchovy = fish; soy
  sauce = soy (and gluten unless tamari); batters, béchamel, custard = egg and often gluten;
  butter, cream, any cheese = dairy; peanut is separate from tree-nut; sesame oil, seeds, tahini =
  sesame; shrimp, prawn, crab, lobster = shellfish. Declare an allergen even when the ingredient is
  optional or a garnish, and both sides of an either/or. Under-labeling is a safety defect.
- **Ground-meat safety:** ground beef, pork and lamb to 160°F (71°C); poultry to 165°F (74°C). Never
  serve ground beef rare. The steps and the safety section must agree.
- Food safety and storage guidance appropriate to the dish.
- A `Sources` section with the recipe URLs you used. Never invent a source.
- Keep the template's Credits lines as written: the recipe is AI-adapted and not kitchen-tested,
  and the cover is an AI-generated illustration.
- No image links in `recipe.md` — the runner adds the cover.

### RECIPE TEMPLATE

````markdown
{{RECIPE_TEMPLATE}}
````

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes one appetizing photograph-style image of the FINISHED, plated dish —
exactly as it's served, garnished, filling most of the frame. Natural window light, accurate
color, shallow depth of field, a simple surface and props that suit the cuisine, a 3–4 colour
palette. It must actually look like THIS dish: right protein, sauce, shape and garnish. The runner
renders it at 3:2 — don't put the ratio in the prompt.

**Forbidden:** prep or mid-cook shots, raw ingredients as the subject, text, labels, menus,
packaging, logos, people or hands. End with `image-prompt-craft`'s constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Dish Name>",
  "slug": "<kebab-case-dish-slug>",
  "summary": "<1–2 sentences: what the dish is and why families make it>",
  "cuisine": "{{CUISINE}}",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
