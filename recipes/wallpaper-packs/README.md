<h1 align="center">🖥️ Wallpaper Pack</h1>

<p align="center">
  <em>Three wallpapers, each as a matching desktop and phone pair.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Each run draws three themes from a pool of twelve (dark abstract flow, deep space, cyberpunk city,
minimal Linux desktop, bioluminescent forest...) and gives each a random twist of lighting,
palette, mood and framing, so a returning theme doesn't come back the same. Claude turns each into
a render prompt. The runner renders one square master per wallpaper and crops the 16:9 desktop and
9:16 phone versions from it, so both share one composition.

| | |
|:---|:---|
| **Output** | `wallpaper-packs/<YYYY-MM>/<date>_<slug>/` → `pack.md`, `masters/`, `desktop/`, `mobile/`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill |
| **Skills** | `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) |

The theme pool and variation axes live in [`themes.json`](themes.json); edit it to change what the
pack draws from. The plan is seeded from the date, so a dry run shows exactly what a real run on
that date will do.

## Resolution

With Gemini, masters render at the 4K tier: about 4096×2304 for the desktop crop and 2304×4096 for
the phone crop. OpenAI has no resolution tier and renders about 1024 px, which is fine on a phone
and soft on a large monitor.

## Cost

Three billed images per run, at Gemini's 4K tier. This is the heaviest image recipe.

## Run it

```bash
python recipes/wallpaper-packs/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../icon-packs/README.md">Next: Icon Pack →</a>
</p>
