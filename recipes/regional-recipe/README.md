<h1 align="center">🗺️ Regional Recipe</h1>

<p align="center">
  <em>A regional recipe library that fills in evenly, one authentic dish at a time.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Each run adds a popular dish to whichever region has the fewest recipes so far, after checking what
that region already holds so nothing repeats. Allergen labeling, the safety gate, the cover and the
Cook's Card all work the same way as in [Family Recipe](../family-recipe/README.md).

| | |
|:---|:---|
| **Output** | `regional-recipes/<YYYY-MM>/<date>_<slug>/` → `recipe.md`, `cover.png`, `cooks-card.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `recipe-validator`, `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🌍 Regions

Twenty-eight, emptiest first: Midwest US, New Orleans, Italian, Thai, Mexican, French, Greek,
Japanese, Mediterranean, American, Southeast Asian, South Asian, East Asian, North African, West
African, South American, Canadian, Australian, Spanish, Korean, Vietnamese, German, Caribbean,
Peruvian, Moroccan, Filipino, Ethiopian, Brazilian. Force one with `--region Georgian`.

## ▶️ Run it

```bash
python recipes/regional-recipe/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../viral-recipe/README.md">Next: Viral Recipe →</a>
</p>
