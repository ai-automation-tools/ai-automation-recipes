# Recipe of the Week

[← All recipes](../../README.md)

One well-loved family recipe a week. Claude researches a crowd-pleasing dish from this week's
cuisine — the kind families actually cook, not viral novelty food — and writes it as a clean,
cookable recipe with complete Big-9 allergen labeling, food-safety guidance and sources. The
runner renders a cover and a self-contained **Cook's Card**: one HTML file with the cover inlined,
a stat bar, numbered step cards, a print stylesheet and dark mode.

| | |
|:---|:---|
| **Output** | `recipes/<YYYY-MM>/<date>_<slug>/` → `recipe.md`, `cover.png`, `cooks-card.html`, `artifact.json` |
| **Schedule** | Saturdays, 19:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `recipe-validator`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Cuisines

Seven, picked by least-used: Midwest, New Orleans, Italian, Thai, Mexican, Southern US, Chinese.
Force one with `--cuisine Korean` (any string works).

## Safety gate

After the agent finishes, the runner runs the `recipe-validator` scanner on `recipe.md`:

- a **critical** food-safety finding (unsafe technique, toxic ingredient handling) rejects the run —
  nothing is published;
- an allergen found in the ingredients but missing from `allergens:` is **added** to the
  frontmatter, since over-labeling is the safe direction.

## Honest labeling

The recipe is AI-adapted from the cited sources and **not kitchen-tested**, and the cover is an
AI-generated illustration, not a photo of the dish. Both say so in the recipe's Credits.

## Sample

> **Minnesota Tater Tot Hotdish** — The classic Upper Midwest casserole: seasoned ground beef and vegetables in a creamy mushroom-soup sauce, topped with rows of crisp tater tots and melted cheddar. Families make it because it feeds a crowd cheaply, travels to potlucks, and can be assembled ahead.
>
> *First live pilot run, 2026-10-14 · Sonnet, under 2 minutes · the safety scanner added the fish allergen from the Worcestershire sauce*

## Run it

```bash
python recipes/recipe-of-the-week/run.py --output-dir ~/ai-output
```

The Cook's Card needs the `markdown` package (`pip install -r requirements.txt`); without it the
recipe still publishes, minus the card.
