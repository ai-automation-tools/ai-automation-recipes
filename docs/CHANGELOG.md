<h1 align="center">📋 Changelog</h1>

<p align="center">
  <em>Every change to the recipes, the runner and the docs, newest first.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.6.0-2ea44f?style=for-the-badge" alt="Version 0.6.0">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Docs home"></a>
</p>

---

Entries that came off the [roadmap](ROADMAP.md) say which phase in italics. Recipe names before
0.6.0 are the old ones; 0.6.0 lists the renames.

## 0.6.0 — 2026-10-14

**Changed**
- Recipe names no longer say how often they run. Sixteen were renamed, with their template IDs and
  display names: `daily-app-card` → `app-idea-card`, `weekly-browser-game` → `browser-game`,
  `weekly-short-story` → `short-story`, `recipe-of-the-week` → `family-recipe`,
  `weekly-audio-podcast` → `podcast-episode`, `weekend-yearly-collections` → `image-collections`,
  `weekly-financial-idea` → `finance-app-prototype`, `weekly-3d-print-ideas` → `3d-print-design`,
  `daily-poster` → `poster`, and the `weekly-` prefix dropped from the other seven. Collections kept
  their names, so earlier output stays where it is.
- The song recipe's `weekly` type is now `news`.
- Prompts and help text no longer assume a cadence ("this week's genre", "one chapter per week").
  Cadence that the code depends on, like GitHub's weekly trending pages, stays.

**Docs**
- Rebuilt the docs as one linked tree: a root README, an index for every folder (`recipes/`,
  `core/`, `scripts/`, `registry/`, `tests/`, `.claude/skills/`, `docs/`), and a header and footer
  on every recipe README that link back up and on to the next recipe.
- The recipe list lost its schedule column. Each Cronsole template still ships a default schedule
  you can change on import.
- The roadmap is now grouped by phase, with finished work moved here.

## 0.5.0 — 2026-10-14

**Added**
- A headless-browser smoke test for the six game and app recipes: the page loads, gets clicked and
  keyed, and the run fails on any uncaught error. It uses Playwright's Chromium or the system Chrome
  or Edge, and skips itself when there's no browser. *(roadmap: Hardening)*
- `RECIPES_WEBHOOK_URL` announces each published artifact to Discord, Slack or any URL as JSON. A
  failed delivery never fails the run. *(roadmap: Hardening)*
- Three templates were imported into a live Cronsole through its import API and scheduled as
  Cronsole-native tasks; the viewer rebuild ran with exit 0.

**Docs**
- A live-test table tracks which recipes have had a real run.

## 0.4.0 — 2026-10-14

**Added**
- `scripts/build_viewer.py` turns any output folder into a browsable page: collections, covers,
  search, rendered Markdown, games and apps in a sandboxed frame, galleries, audio and video. It
  works from disk, and model-written HTML can't run in it. *(roadmap: Viewer)*
- The **Rebuild Viewer** Cronsole template, in every pack.

**Changed**
- `icon-packs` themes no longer name products or brands. A live run on a "Web Browsers" theme drew
  icons that echoed real browser logos, so 35 themes became generic sets and the prompt forbids
  brands. The other image theme lists were checked and are clean.

**Fixed**
- The leak scan stopped reading SVG path data as IP addresses.

**Docs**
- Live samples in nine recipe READMEs.

## 0.3.0 — 2026-10-14

**Added**
- Twelve image and audio recipes, 38 in all: `comics`, `ai-meme-generator`, `daily-poster`,
  `future-cities`, `image-prompt-packs`, `wallpaper-packs`, `icon-packs`,
  `weekend-yearly-collections`, `song-generator`, `podcast-script-generator`, `weekly-audio-podcast`
  and `voiceover-script-generator`. Voices are presets only. *(roadmap: Batch 2)*
- Multi-image runs (`ImageSpec`) with resolution tiers and a lettering-only mode for images that
  carry words.
- `core/images/process.py` for crops, ICO and SVG; `core/audio` for Gemini or ElevenLabs speech and
  ElevenLabs music; `core/video.py` for an ffmpeg slideshow.
- A key preflight (`requires=`), a `NothingToDo` skip signal and per-run tool lists.
- The `songwriting-craft` skill, CC0-derived and attributed.

**Changed**
- Shared helpers moved into `core/web.py`, `core/food/` and `core/digest/`. `validate()` can take
  the run context, and a new `after_cover` hook publishes files that need the cover.
- CI installs the requirements and ffmpeg. Dependabot ignores major versions, and pip version PRs
  are off until publish.

**Fixed**
- A voiceover video ran 18 seconds past its audio.
- An empty Gemini speech response stopped a 42-line podcast at line 36. Empty responses are now
  retried.

## 0.2.0 — 2026-10-14

**Added**
- Twenty-three recipes across apps and games, writing, food and maps, and research digests, 26 in
  all. *(roadmap: Batch 1)*
- The browser extension recipe checks Manifest V3, missing files, remote code and `eval`.
- The serialized novella keeps a story bible in its collection and reseeds a new novel when one
  finishes.
- Food recipes generate their cover instead of downloading a photo, say plainly that the recipe is
  AI-adapted and untested, gate on the recipe-validator scanner and render a Cook's Card.
- Research digests write browser bookmarks and never repeat an earlier entry; `trending-movers`
  rejects figures that don't match what it measured.
- The `recipe-validator` skill and eight Apache-2.0 writing skills, attributed.
- Five registry packs: everything, plus one per group.

**Changed**
- Recipe output may include subfolders and optional files.

**Fixed**
- A field set to `0` or `false` was treated as missing.
- JSON data blocks inside HTML were syntax-checked as JavaScript. A live run caught it.

## 0.1.0 — 2026-10-14

**Added**
- The runner: staged runs that publish all or nothing, a shared headless contract, prompt filling
  that fails on unfilled tokens, and `runs.jsonl`.
- The Claude engine: `claude --print` in the staging folder under `--permission-mode dontAsk`, with a
  tool allowlist per recipe.
- Covers from Gemini, then OpenAI, whichever key is set.
- Three recipes: `daily-app-card`, `weekly-browser-game` and `weekly-short-story`, each with one
  live run. *(roadmap: Pilot)*
- Cronsole Registry v1 templates, a clone-updater template and the `ai-recipes` pack, checked
  against Cronsole's own schema and substitution code.
- `scripts/check_public.py`, and CI running the tests, the registry check, the leak scan and every
  prompt's dry run.

**Changed**
- Covers are requested full-bleed, after the first live cover came out as an inset panel.

---

<p align="center">
  <a href="README.md">← Docs home</a> ·
  <a href="ROADMAP.md">Roadmap</a>
</p>
