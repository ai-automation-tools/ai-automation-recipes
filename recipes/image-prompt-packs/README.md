<h1 align="center">🎨 Image Prompt Pack</h1>

<p align="center">
  <em>Five to eight reusable image prompts on one theme, each with a rendered example.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude writes the prompts, each with a negative prompt, aspect ratio, style tags and a use case.
The runner renders one example per prompt, and the first example doubles as the cover.

| | |
|:---|:---|
| **Output** | `image-prompt-packs/<YYYY-MM>/<date>_<slug>/` → `pack.md`, `images/*.png`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill |
| **Skills** | `image-prompt-craft`, `llm-writing`, `humanizer` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). The run stops before calling Claude without one |

## Themes

Ten suggestions, picked by ISO week number (cyberpunk dystopia, vintage travel posters, steampunk
contraptions...). Claude may choose a fresher theme when the suggested one has already been used.
Force one with `--theme "Art Deco Skyscrapers"`.

## Cost

One billed image per prompt, so 5 to 8 per run.

## Run it

```bash
python recipes/image-prompt-packs/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../wallpaper-packs/README.md">Next: Wallpaper Pack →</a>
</p>
