# Regional Recipe

[← All recipes](../../README.md)

A recipe library that grows evenly. Each week Claude adds one authentic, popular dish to the
region with the fewest recipes — checking what that region already holds so nothing repeats —
with the same allergen labeling, safety gate, cover and Cook's Card as
[Family Recipe](../family-recipe/README.md).

| | |
|:---|:---|
| **Output** | `regional-recipes/<YYYY-MM>/<date>_<slug>/` → `recipe.md`, `cover.png`, `cooks-card.html`, `artifact.json` |
| **Schedule** | Fridays, 19:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `recipe-validator`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Regions

Twenty-eight, filled least-first: Midwest US, New Orleans, Italian, Thai, Mexican, French, Greek,
Japanese, Mediterranean, American, Southeast Asian, South Asian, East Asian, North African, West
African, South American, Canadian, Australian, Spanish, Korean, Vietnamese, German, Caribbean,
Peruvian, Moroccan, Filipino, Ethiopian, Brazilian. Force one with `--region Georgian`.

## Run it

```bash
python recipes/regional-recipe/run.py --output-dir ~/ai-output
```
