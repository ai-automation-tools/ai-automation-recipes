<h1 align="center">🍲 Family Recipe</h1>

<p align="center">
  <em>A well-loved family dish, written as a cookable recipe with full allergen labeling.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude picks a dish people actually cook at home, not viral novelty food, from the cuisine the
rotation hands it. It writes the recipe with Big-9 allergen labels, food-safety notes and sources.
The runner then renders a cover and a **Cook's Card**: one HTML file with the cover inlined, a stat
bar, numbered step cards, a print stylesheet and dark mode.

| | |
|:---|:---|
| **Output** | `recipes/<YYYY-MM>/<date>_<slug>/` → `recipe.md`, `cover.png`, `cooks-card.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `recipe-validator`, `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🌍 Cuisines

Seven, least-used first: Midwest, New Orleans, Italian, Thai, Mexican, Southern US, Chinese. Any
string overrides it: `--cuisine Korean`.

## 🛡️ Safety gate

Once the agent finishes, the runner scans `recipe.md` with the `recipe-validator` scanner.

- A **critical** food-safety finding, such as an unsafe technique or a toxic ingredient handled
  wrong, rejects the run. Nothing is published.
- An allergen that shows up in the ingredients but not in `allergens:` gets **added** to the
  frontmatter. Over-labeling is the safe direction.

## 🏷️ Honest labeling

The recipe is adapted by AI from the cited sources and has not been kitchen-tested. The cover is an
AI illustration, not a photo of the dish. The recipe's Credits section says both.

## 🧪 Sample

> **Minnesota Tater Tot Hotdish** — The classic Upper Midwest casserole: seasoned ground beef and
> vegetables in a creamy mushroom-soup sauce, under rows of crisp tater tots and melted cheddar.
>
> *First live pilot run, 2026-10-14 · Sonnet, under 2 minutes · the scanner added the fish allergen
> that the Worcestershire sauce brings in*

## ▶️ Run it

```bash
python recipes/family-recipe/run.py --output-dir ~/ai-output
```

The Cook's Card needs the `markdown` package (`pip install -r requirements.txt`). Without it the
recipe still publishes, just without the card.

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../regional-recipe/README.md">Next: Regional Recipe →</a>
</p>
