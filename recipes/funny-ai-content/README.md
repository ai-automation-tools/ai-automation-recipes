<h1 align="center">🤡 Funny AI Content</h1>

<p align="center">
  <em>A ready-to-shoot satirical bit about an absurd use for an AI agent.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Think "using AI to automate your divorce." Each concept comes with the joke, why it lands, an
on-screen treatment, five script beats, the fake automation workflow, and a wordless cover gag.

| | |
|:---|:---|
| **Output** | `funny-ai-content/<YYYY-MM>/<date>_<slug>/` → `concept.md`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

Five premise families, least-used first: emotionally delicate situations, over-automated domestic
life, weird business workflows, petty productivity, socially cursed agents. Force one with
`--family`.

## Run it

```bash
python recipes/funny-ai-content/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../family-recipe/README.md">Next: Family Recipe →</a>
</p>
