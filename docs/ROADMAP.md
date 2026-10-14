# Roadmap

[← README](../README.md)

## Pilot (now)

- [x] Shared runner, Claude engine, Gemini/OpenAI cover step, `artifact.json` contract
- [x] Three recipes: `daily-app-card`, `weekly-browser-game`, `weekly-short-story`
- [x] Cronsole Registry v1 templates + `ai-recipes` pack, validated against Cronsole's own schema
- [x] Pre-publish leak scan with an out-of-repo denylist
- [x] One live run of each recipe, output read by a person (the game played in a browser)
- [x] Pack passes Cronsole's import path (schema, normalizer, `{{placeholder}}` substitution) and
      every resolved command runs
- [ ] Import the pack through a Cronsole UI and let one template fire on schedule
- [ ] A week of scheduled runs without intervention

## Before going public

- [ ] Create `ai-automation-tools/ai-automation-recipes` with a fresh history and a noreply commit identity
- [x] CI: unit tests, `build_registry.py --check`, `check_public.py`, prompt dry runs on every PR
- [x] Sample output for each recipe in its README
- [ ] Ship the AI Content Recipes pack through Cronsole's registry, and link it from the Cronsole site

## Viewer

- [ ] `viewer/`: a static site that renders any `<output-dir>` from its `artifact.json` files —
      cards, playable games in an iframe, stories
- [ ] Public demo at a subdomain of `ai-automation-tools.dev`, fed by curated output
- [ ] "Import into Cronsole" link on each recipe in the demo

## More recipes

- [ ] Port the next tier: browser-extension ideas, 3D-print ideas, OSS spotlight, AI stack radar,
      cool websites, recipes with `recipe-validator`, songs
- [ ] A drift check that flags when a public prompt falls behind the private original

## Engines

- [ ] Pluggable text engines beyond Claude (Codex CLI, Gemini CLI) behind `core/engines/`
- [ ] Optional browser smoke test for the game recipe (Playwright: load, tap, check the score moves)
- [ ] Optional delivery step: email or webhook with the new artifact

## Cronsole asks

- [ ] Multiple registry sources, so this repo can publish its own catalog
- [ ] A crontab compiler for the `linux` target
- [ ] Template-level secret requirements (`requiresSecrets: ["GEMINI_API_KEY"]`)
