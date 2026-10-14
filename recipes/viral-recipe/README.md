<h1 align="center">🔥 Viral Recipe</h1>

<p align="center">
  <em>The dish everyone is making this week, rewritten so it actually cooks, with the creator credited.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude scans TikTok, Instagram, YouTube Shorts, Reddit and Facebook for a recipe with real momentum
right now, pins the quantities down from several posts (creators are vague about them), and writes
it up with the same contract as [Family Recipe](../family-recipe/README.md): Big-9 allergen labels,
food-safety notes, sources, a cover and a Cook's Card. Two things are this recipe's own: the
originating post lives in the frontmatter as `source` and `source_platform`, and a *Why This Went
Viral* section explains the hook and credits the creator by handle.

| | |
|:---|:---|
| **Output** | `viral-recipes/<YYYY-MM>/<date>_<slug>/` → `recipe.md`, `cover.png`, `cooks-card.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `recipe-validator`, `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 📱 Platforms

Any by default. `--platform TikTok` (or Instagram, YouTube, Reddit, Facebook) restricts where the
trend has to come from; the other platforms may still corroborate the recipe.

## 🛡️ Safety gate

Viral food is where unsafe techniques spread fastest. The prompt tells Claude to make the recipe
safe even when the trend as posted isn't, and to say so. Then the runner scans `recipe.md` with the
`recipe-validator` scanner: a critical finding rejects the run, an undeclared allergen gets added.
The runner also rejects a recipe with no `source` URL, no recognised `source_platform`, or no
*Why This Went Viral* section.

## 🏷️ Honest labeling

The recipe is adapted by AI from the cited posts and has not been kitchen-tested. The cover is an
AI illustration of the dish, never a creator's photo or likeness. Creators are named by public
handle only.

## ▶️ Run it

```bash
python recipes/viral-recipe/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../ai-map/README.md">Next: AI Map →</a>
</p>
