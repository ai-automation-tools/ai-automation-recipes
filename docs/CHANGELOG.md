# Changelog

[← README](../README.md)

## 0.5.0 — 2026-10-14

- **Browser smoke test** (`core.web.browser_smoke`): game and app recipes load their page in a
  headless browser (Playwright with Chromium, or the system Chrome or Edge), click and press keys,
  and reject the run on any uncaught error. Catches the dead-title-screen class `node --check`
  can't. Skipped when no browser is available or `RECIPES_BROWSER_CHECK=off`.
- **Webhook delivery** (`core/deliver.py`): `RECIPES_WEBHOOK_URL` announces each published
  artifact; Discord and Slack get native messages, anything else JSON. Best-effort.
- 49 tests.

## 0.4.0 — 2026-10-14

- **Viewer**: `scripts/build_viewer.py` turns any output folder into a browsable page
  (`index.html` + `catalog.js`): collections in a sidebar, cover grid, search, rendered Markdown,
  games and apps in a sandboxed iframe, galleries, audio and video. Works from `file://`. House
  style (fuchsia accent, light/dark, phone drawer). Model-written HTML in documents is escaped and
  the catalog can't close its own `<script>` tag.
- **Cronsole**: new `AI Recipes: Rebuild Viewer` template, shipped in every pack.
- **icon-packs**: 35 brand-named themes rewritten as generic functional sets, and the prompt now
  forbids naming or echoing any product, company or brand — a live run had echoed real browser
  logos. Other theme lists reviewed: clean.
- **Docs**: live samples in nine recipe READMEs.
- 46 tests.

## 0.3.0 — 2026-10-14

Batch 2: media support and 12 image and audio recipes, 38 in all.

- **Images**: `comics`, `ai-meme-generator`, `daily-poster`, `future-cities`, `image-prompt-packs`,
  `wallpaper-packs` (4K masters cropped to desktop and phone), `icon-packs` (SVG + PNG + ICO from
  agent-written glyphs), `weekend-yearly-collections` (user-editable collections). Theme lists were
  cleaned of real people and named artists.
- **Audio**: `song-generator` (37 song types, ElevenLabs composition plans), `podcast-script-generator`
  and `weekly-audio-podcast` (script, then a rendered episode), `voiceover-script-generator`
  (narration and a vertical short). Preset voices only.
- **Runner**: `ImageSpec` multi-image output with resolution tiers and a lettering-only mode;
  `requires=` preflight; `NothingToDo` skip signal; `prepare()` errors fail cleanly; per-run tool
  lists via `ctx.state["tools"]`.
- **core**: `core/images/process.py` (crops, ICO, SVG rasterizing), `core/audio` (Gemini and
  ElevenLabs speech, ElevenLabs music), `core/video.py` (ffmpeg slideshow).
- **Consolidation**: shared helpers moved into `core/web.py`, `core/food/`, `core/digest/`;
  `validate()` can take the run context; new `after_cover` hook.
- **Fixed from live runs**: a slideshow ran 18 s past its audio; an empty Gemini TTS response killed
  a 42-line episode at line 36 (now retried).
- **Skills**: `songwriting-craft` (CC0-derived, attributed).
- **Registry**: 39 templates in seven packs. **Tests**: 43, plus faked-engine smoke runs of every
  Batch 2 recipe. CI installs requirements and ffmpeg. Dependabot ignores majors and pip version
  PRs until publish.

## 0.2.0 — 2026-10-14

Batch 1: 23 more recipes, 26 in all.

- **Apps & games**: `weekly-app-prototype`, `weekly-browser-extension` (loadable Manifest V3 folder,
  checked for MV3, missing files, remote code and `eval`), `weekly-financial-idea`,
  `weekly-mobile-game`, `weekly-pc-game-concept`, `weekly-3d-print-ideas` (one design per run,
  three runs a week).
- **Writing**: `serialized-novella` (story bible kept in the collection, chapter number and rolling
  synopsis derived from published chapters, archived and reseeded at the target length),
  `alternate-history` (optional premise queue), `agent-persona-original`, `content-idea-gen`,
  `weekly-funny-ai-content`.
- **Food & maps**: `recipe-of-the-week` and `weekly-regional-recipe` (generated covers instead of
  downloaded photos, credits that say the recipe is AI-adapted and untested, the recipe-validator
  scanner as a hard safety gate, a self-contained Cook's Card page), `weekly-ai-map` (Leaflet,
  per-stop photo downloads dropped).
- **Research digests** (monthly): `agent-toolkit`, `ai-stack-radar`, `oss-spotlight`,
  `cool-websites`, `top-10-github-repos`, `trending-movers` (published figures must match the
  measured ones), `signal-sources` (cumulative, with OPML), `security-toolkit`, `finance-toolkit`.
  Each writes browser bookmarks and never repeats an earlier entry.
- **Shared helpers**: `recipes/_shared/` (web and MV3 checks, Cook's Card) and `recipes/_digest/`
  (fetchers, parser, bookmark and OPML writers).
- **Runner**: subfolder paths and `optional_files`; `0` and `false` are no longer treated as
  missing fields; inline JSON data blocks are skipped by the JS syntax checks.
- **Skills**: `recipe-validator`; eight Apache-2.0 writing skills from creative-writing-skills,
  attributed in `.claude/skills/_vendor/` (which now also covers `llm-writing`).
- **Registry**: 27 templates in five packs — everything, plus one per category.
- `markdown` added to `requirements.txt` for the Cook's Card.

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
