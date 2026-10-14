# Viral Recipe

Goal: find ONE recipe that is **currently viral on social media**, recreate it as a clean, cookable
Markdown recipe that credits the people who made it blow up, plus the description of a cover image.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

{{PLATFORM_RULE}}

**Viral recipes already in the collection** (date · slug · title — summary). Do not repeat a dish or
a trend that is only a rename of one of these:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Find the trend.** Use **WebSearch** / **WebFetch** where food trends actually break: TikTok
   ("viral recipe", "trending recipe", named trends), Instagram Reels and YouTube Shorts creators,
   Reddit (r/food, r/recipes, r/tonightsdinner, r/GifRecipes), Facebook recipe groups, and the food
   media that tracks trends to corroborate ratios (Delish, Bon Appétit, The Kitchn, Tasty, Today,
   Eater). You want **real momentum in roughly the last few weeks**: a named trend, a creator's dish
   everyone is remixing, an "is this real?" technique. Not an evergreen classic.
2. **Qualify it.** Cookable at home, safe and legal, and corroborated by more than one post so the
   quantities are right. Identify the **original or most-credited creator** and the **platform** it
   is viral on. Note the hook: the surprising technique, the mashup, the look, the dare.
3. **Load the skills** (below), then write `recipe.md` from the RECIPE TEMPLATE with the viral
   additions under RECIPE REQUIREMENTS. Synthesize exact quantities, times and temperatures from the
   posts; creators are vague, the recipe can't be.
4. **Run the `recipe-validator` checks yourself** on the draft and fix anything critical or high.
   The runner re-runs the scanner and rejects the recipe on a critical food-safety finding. Viral
   food is where unsafe techniques spread fastest (undercooked chicken, raw flour, home canning
   shortcuts); if the trend as posted is unsafe, make the recipe safe and say so in Chef's Notes.
5. Load `image-prompt-craft` and write the cover description (COVER IMAGE below).
6. End with the FINAL MESSAGE JSON.

If nothing is genuinely viral right now, take the freshest recently-trending dish you can verify and
say so plainly in *Why This Went Viral*. Never fabricate a trend, a creator, a number or a link.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

- **`recipe-validator`** — read its food-safety and nutrition references and apply them to your
  draft: safe cooking temperatures, dangerous ingredient/technique combinations, per-serving
  sodium / saturated fat / added sugar, quantity and ratio sanity, allergen labeling. Its scanner
  script is run by the runner, not by you. If it would flag an indulgent dish as rich rather than
  unsafe, keep the dish and say so in Chef's Notes.
- **`llm-writing`** + **`humanizer`** apply to the PROSE only: the context, *Why This Went Viral*,
  the notes, the step wording. Skip their audit/report steps; ask no questions.
- **The template wins on structure.** Never let a prose pass touch a number: a quantity, a
  temperature, a time or a doneness cue is not a style choice.

--------------------------------------------------
## RECIPE REQUIREMENTS

- Genuinely cookable, specific and complete. Keep what makes the viral version itself (the
  technique, the ratio, the serving gimmick) while writing it as a real recipe.
- Frontmatter: the template's fields **plus** `source` (the single best originating or most-credited
  post URL, in quotes) and `source_platform` (exactly one of `TikTok`, `Instagram`, `YouTube`,
  `Reddit`, `Facebook`). `region` is the cuisine of origin if clear, else `viral`. `tags` include
  `viral` and the platform in lowercase.
- A **`## Why This Went Viral`** section right after *Cultural Context*: 2–4 sentences on the trend,
  the hook, roughly when and where it took off, and who gets the credit. Name creators by their
  public handle only.
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
- A `Sources` section listing **every** link: the originating post first, labelled with the
  creator's handle and platform, then every corroborating post or article you used. Only URLs you
  actually opened. Never invent a source.
- Keep the template's Credits lines as written: the recipe is AI-adapted and not kitchen-tested,
  and the cover is an AI-generated illustration.
- No image links in `recipe.md`; the runner adds the cover.

### RECIPE TEMPLATE

````markdown
{{RECIPE_TEMPLATE}}
````

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes one appetizing photograph-style image of the FINISHED dish exactly as the
trend serves it, filling most of the frame; if the trend is a look (a cross-section, a pull, a
pour), show that moment. Natural window light, accurate colour, shallow depth of field, a simple
surface, a 3–4 colour palette. It must look like THIS dish. The runner renders it at 3:2; don't put
the ratio in the prompt.

**Forbidden:** prep or mid-cook shots, raw ingredients as the subject, text, labels, phone screens,
watermarks, logos, people, hands or faces (the creator is credited in words, never drawn). End with
`image-prompt-craft`'s constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Dish Name>",
  "slug": "<kebab-case-dish-slug>",
  "summary": "<1–2 sentences: what the dish is and why it took off>",
  "source_platform": "<TikTok | Instagram | YouTube | Reddit | Facebook, exactly as in the frontmatter>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
