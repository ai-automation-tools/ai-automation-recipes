# Architecture

[← README](../README.md)

## Layout

| Path | Holds |
|:---|:---|
| `recipes/<name>/` | One automation: `prompt.md`, `run.py`, `cronsole.json`, `README.md` |
| `core/runner.py` | The run loop every recipe shares |
| `core/web.py` | Checks for HTML/JS output: references, `node --check`, Manifest V3, JSON, sources CSV, and a headless-browser smoke test |
| `core/food/` | The recipe-validator safety gate, allergen fix-ups and the Cook's Card |
| `core/digest/` | The research-digest toolkit: feed and GitHub Trending fetchers, digest parser, bookmark/OPML writers, shared rules |
| `core/run-contract.md` | The headless rules spliced into every prompt as `{{RUN_CONTRACT}}` |
| `core/engines/` | Text engines behind one interface (`claude` today) |
| `core/images/` | Image rendering (Gemini, then OpenAI) and `process.py`: crops, ICO, SVG → PNG |
| `core/audio/` | Speech (Gemini or ElevenLabs, preset voices only) and ElevenLabs music |
| `core/video.py` | Optional ffmpeg slideshow for vertical shorts |
| `core/deliver.py` | Optional webhook announcement of each published artifact |
| `core/artifacts.py` | Output layout, `artifact.json`, rotation and do-not-repeat helpers |
| `.claude/skills/` | Skills the recipes load, copied into each run's staging folder |
| `cronsole/` | Templates that aren't recipes (the clone updater) |
| `registry/` | **Generated.** The Cronsole registry, built by `scripts/build_registry.py` |
| `scripts/check_public.py` | Pre-publish scan for keys, personal paths and a private denylist |
| `viewer/index.html` | The viewer page; `scripts/build_viewer.py` copies it into an output folder beside a generated `catalog.js` |
| `tests/` | `unittest` coverage of the run loop with the engine faked |

## The run loop

1. **Read the collection.** `load_existing()` reads every `artifact.json` under the recipe's
   collection. Recipes use it to rotate categories and genres (`least_used`) and to show the agent
   what already exists (`{{EXISTING}}`).
2. **Fill the prompt.** `{{TOKENS}}` come from the runner (`DATE`, `RUN_CONTRACT`, `EXISTING`,
   `OUTPUT_FILES`, `SKILLS`) and from the recipe's `prepare()` hook. A leftover token fails the run
   before any agent call.
3. **Stage.** A fresh folder under `<collection>/.staging/` gets a copy of the recipe's skills in
   `.claude/skills/`.
4. **Run the engine** with that folder as its working directory and the recipe's tool allowlist.
5. **Check the result.** The agent's last JSON object must have `title`, `summary`, the recipe's
   `fields` and a `cover_prompt`, or an `error`. Every file in `files` must exist and be non-empty
   (subfolder paths like `extension/manifest.json` are allowed; `optional_files` are kept when
   present); any other top-level entry is deleted. The recipe's `validate()` hook runs here (the game
   recipe syntax-checks its script); it may take the run context as a third argument.
6. **Render media.** Any `images` the agent listed (for recipes with an `ImageSpec`), then the cover
   from `cover_prompt`, each with the no-text constraint (or lettering-only for `text_ok`). Then the
   recipe's `after_cover()` hook adds files that need them: the Cook's Card, wallpaper crops, icon
   PNG/ICO, rendered speech and music, the short video.
7. **Publish.** Move the folder to `<collection>/<YYYY-MM>/<date>_<slug>/`, write `artifact.json`,
   run the `finish()` hook, append to `runs.jsonl`.

Any failure before step 7 publishes nothing. Before step 3, a recipe's `requires` (and any
`ImageSpec`) is checked against the keys that are set, so a missing key fails before the agent runs;
`prepare()` can raise `NothingToDo` to skip the run with exit 0.

## `artifact.json` (schema `ai-automation-recipes/artifact@1`)

```json
{
  "schema": "ai-automation-recipes/artifact@1",
  "recipe": "app-idea-card",
  "recipe_version": "0.1.0",
  "collection": "idea-cards",
  "title": "Receipt Radar",
  "slug": "receipt-radar",
  "date": "2026-10-14",
  "summary": "Finds refunds you are owed.",
  "files": { "main": "card.md", "cover": "cover.png" },
  "fields": { "category": "Browser Extension", "form_factor": "browser extension", "monetization": "freemium" },
  "generator": {
    "engine": "claude", "model": "claude-sonnet-5-5",
    "image_engine": "gemini", "image_model": "gemini-3.1-flash-image",
    "cover_prompt": "…"
  },
  "created_at": "2026-10-14T11:04:12+00:00"
}
```

This is the contract with any viewer. Add fields freely; bump the schema only for a breaking change.

## Engines

An engine implements `preflight()` and `run(EngineRequest) -> EngineResult` (see
`core/engines/base.py`). The request carries the prompt, the staging folder, the tool allowlist,
model and timeout; the result is the agent's final message and the model that produced it.

Adding one means a module in `core/engines/` and a line in `ENGINES`. Recipes don't change — they
already describe their tools by Claude Code's names, which an engine maps to its own.

## Skills

Recipes name skills; they never paste skill text into a prompt. The copy in `.claude/skills/` is
the single source of truth. A skill that reads like it was written for an interactive session gets
carve-outs in the prompt ("skip the audit, the output format wins"), not edits to the skill.
