# Wallpaper Pack

[← All recipes](../../README.md)

Three wallpapers a week, each as a matching pair: a 16:9 desktop wallpaper and a 9:16 phone
wallpaper. The runner draws three themes from a pool of twelve (dark abstract flow, deep space,
cyberpunk city, Linux-ricing minimal, bioluminescent forest…) and gives each a random twist of
lighting, palette, mood and framing, so a theme that comes back doesn't come back the same. Claude
turns each into a render prompt; the runner renders one square master per wallpaper and crops both
versions from it, so the pair always shares one composition.

| | |
|:---|:---|
| **Output** | `wallpaper-packs/<YYYY-MM>/<date>_<slug>/` → `pack.md`, `masters/`, `desktop/`, `mobile/`, `cover.png`, `artifact.json` |
| **Schedule** | Sundays, 15:30 UTC |
| **Model** | `sonnet` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill |
| **Skills** | `image-prompt-craft` |

The theme pool and variation axes live in [`themes.json`](themes.json) — edit them to change what
the pack draws from. The same date always produces the same plan, so a dry run shows exactly what a
real run will do.

## Resolution

With Gemini, masters render at the 4K tier, so the desktop crop is about 4096×2304 and the phone
crop about 2304×4096. OpenAI has no resolution tier and renders about 1024 px, so its crops are
fine for previews and small screens but soft on a large monitor.

## Cost

Three billed images per run.

## Run it

```bash
python recipes/wallpaper-packs/run.py --output-dir ~/ai-output
```
