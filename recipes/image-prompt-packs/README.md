# Weekly Image Prompt Pack

[← All recipes](../../README.md)

A themed pack of 5–8 polished, reusable image-generation prompts, each with a rendered example.
Claude writes the prompts (with negative prompts, aspect ratios, style tags and a use case for
each); the runner renders one example per prompt, and the first example becomes the cover.

| | |
|:---|:---|
| **Output** | `image-prompt-packs/<YYYY-MM>/<date>_<slug>/` → `pack.md`, `images/*.png`, `cover.png`, `artifact.json` |
| **Schedule** | Saturdays, 16:00 UTC |
| **Model** | `sonnet` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) — the run fails before calling Claude without one |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill |
| **Skills** | `image-prompt-craft`, `llm-writing`, `humanizer` |

## Themes

Ten suggestions, one per ISO week (cyberpunk dystopia, vintage travel posters, steampunk
contraptions…). Claude may pick a fresher theme when the suggestion was already used. Force one
with `--theme "Art Deco Skyscrapers"`.

## Cost

One billed image per prompt: 5–8 per run.

## Run it

```bash
python recipes/image-prompt-packs/run.py --output-dir ~/ai-output
```
