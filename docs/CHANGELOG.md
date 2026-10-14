# Changelog

[← README](../README.md)

## 0.1.0 — 2026-10-14

First pilot build.

- **Runner** (`core/runner.py`): staged runs that publish all-or-nothing, a shared headless run
  contract, `{{TOKEN}}` prompt filling that fails on leftovers, JSON extraction from the agent's
  final message, stray-file cleanup, `runs.jsonl`.
- **Claude engine**: `claude --print` in the staging folder under `--permission-mode dontAsk` with a
  per-recipe tool allowlist.
- **Covers**: Gemini then OpenAI, by whichever key is set; PNG re-encoded through Pillow; the
  canonical no-text constraint appended once.
- **Recipes**: `daily-app-card` (five rotating categories), `weekly-browser-game` (thirteen genres
  by ISO week, resource and `node --check` validation), `weekly-short-story` (eleven genres,
  optional `story-ideas.md` queue).
- **Skills**: `humanizer` (MIT, vendored), `llm-writing`, `game-design`, `single-file-game-dev`,
  `image-prompt-craft` (engine references rewritten for public image APIs).
- **Cronsole**: one Registry v1 template per recipe, a clone-updater template, and the
  `ai-recipes` pack; `scripts/build_registry.py` with `--check`.
- **Safety**: `scripts/check_public.py`.
- **CI**: tests, registry check, leak scan and prompt dry runs on every push and PR; Dependabot
  for Actions and pip (majors ignored).
- **Covers** are asked for full-bleed, after the first live run produced an inset panel.
- Verified live: one real run of each recipe, and the pack run through Cronsole's own import and
  substitution code.
