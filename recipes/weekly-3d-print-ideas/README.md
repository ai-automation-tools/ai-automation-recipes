# 3D Print Idea

[← All recipes](../../README.md)

One original, FDM-printable product design per run, grounded in what actually sells on maker and
marketplace sites. Each is a build-ready package — dimensions, parts, fits and tolerances, a CAD
modeling guide, print settings, and pricing — plus a machine-readable `design-spec.json` a modeling
agent can consume, and a photoreal product mockup.

| | |
|:---|:---|
| **Output** | `3d-print-designs/<YYYY-MM>/<date>_<slug>/` → `README.md`, `design-spec.json`, `sources.csv`, `cover.png` (1:1), `artifact.json` |
| **Schedule** | Tuesdays, Thursdays and Saturdays, 13:00 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Subcategories

Nine, picked by least-used: Household, Organization and Storage, Desk and Tech, Toys and Fidgets,
Puzzles and Games, Art and Decor, Sports and Fan Gear, Tools and Workshop, Outdoor and Garden. Force
one with `--subcategory Desk-and-Tech`.

## What the runner checks

The run is rejected if `design-spec.json` doesn't parse or has no `parts` array, any part's bounding
box is missing or exceeds 220 mm, a part named in the JSON is missing from the README, or
`sources.csv` doesn't have the `title,url,note` header and 4–8 sources.

## Run it

```bash
python recipes/weekly-3d-print-ideas/run.py --output-dir ~/ai-output
```
