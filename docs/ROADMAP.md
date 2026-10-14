# Roadmap

[← README](../README.md)

Everything left before this repo goes public. The repo stays **private** in its `Custom/` folder
until the publish checklist at the bottom is done and the maintainer says go.

## 1. Pilot ✅

- [x] Shared runner, Claude engine, Gemini/OpenAI cover step, `artifact.json` contract
- [x] Three recipes: `daily-app-card`, `weekly-browser-game`, `weekly-short-story`
- [x] Cronsole Registry v1 templates + `ai-recipes` pack, validated against Cronsole's own schema
- [x] Pre-publish leak scan with an out-of-repo denylist
- [x] One live run of each recipe, output read by a person (the game played in a browser)
- [x] Pack passes Cronsole's import path (schema, normalizer, `{{placeholder}}` substitution) and
      every resolved command runs
- [x] CI: unit tests, `build_registry.py --check`, `check_public.py`, prompt dry runs on every push
- [x] Sample output for each recipe in its README
- [x] Private remote `ai-automation-tools/ai-automation-recipes` with a noreply commit identity

## 2. Batch 1 — recipes that fit the current runner (23) ✅

Each port: read the private job's prompt and wrapper, drop anything personal or fleet-specific,
write `prompt.md` + `run.py` + `cronsole.json` + `README.md`, dry-run it, rebuild the registry.

**Apps & games**

- [x] `weekly-app-prototype` — runnable single-page app prototype + requirements + sample data
- [x] `weekly-browser-extension` — loadable Manifest V3 extension folder
- [x] `weekly-financial-idea` — consumer-finance app prototype
- [x] `weekly-mobile-game` — single-file, portrait, touch-first game
- [x] `weekly-pc-game-concept` — design brief, `pitch.html`, key art, sources
- [x] `weekly-3d-print-ideas` — three printable product specs with `design-spec.json`

**Books & writing**

- [x] `alternate-history` — illustrated "what if" timeline
- [x] `serialized-novella` — one chapter a run against a story bible
- [x] `agent-persona-original` — an invented, debate-ready character card
- [x] `content-idea-gen` — one social-media content idea with a cover
- [x] `weekly-funny-ai-content` — one funny AI-themed content idea

**Food & maps**

- [x] `recipe-of-the-week` — family recipe + Cook's Card HTML; **generated** hero image instead of a
      downloaded photo; `recipe-validator` skill bundled
- [x] `weekly-regional-recipe` — same, cycling through regions
- [x] `weekly-ai-map` — researched interactive Leaflet map + companion markdown

**Research digests**

- [x] `agent-toolkit` — skills, MCP servers, plugins and hooks worth installing
- [x] `ai-stack-radar` — hosted AI products by job, with what they replace and cost
- [x] `oss-spotlight` — editorial read on the open-source ecosystem
- [x] `cool-websites` — lesser-known useful sites by category
- [x] `top-10-github-repos` — weekly ranked AI / dev-tooling repos
- [x] `trending-movers` — star-velocity leaderboard
- [x] `signal-sources` — cumulative reading list with RSS feeds
- [x] `security-toolkit` — monthly security tooling haul
- [x] `finance-toolkit` — monthly financial tooling haul

**Batch 1 wrap-up**

- [x] Bundle any extra skills the ports need, scrubbed and license-checked (`recipe-validator`;
      eight Apache-2.0 writing skills with attribution in `.claude/skills/_vendor/`)
- [x] One live run per category, output reviewed: `weekly-browser-extension`, `serialized-novella`
      (seed run), `recipe-of-the-week`, `trending-movers`
- [x] Split the registry into per-category packs alongside the all-in-one pack (5 packs, 27 templates)
- [x] README recipe table and CHANGELOG updated
- [x] Live samples in the READMEs of the four Batch 1 live runs

## 2b. Consolidate after Batch 1 ✅

- [x] Runner: subfolder paths in `files`, `optional_files`, `0`/`false` no longer read as missing
- [x] Inline JSON data blocks skipped by the JS syntax checks (a live run caught this)
- [x] Move `recipes/_shared/` and `recipes/_digest/` into `core/` and switch `weekly-browser-game`
      to the shared web checks
- [x] Pass the run context to `validate()` (removes the novella's module-level state)
- [x] A post-cover hook, so recipes that embed the cover (Cook's Card) don't patch `artifact.json`
- [x] Unit tests for the shared modules and the new hooks (27 tests)

## 3. Batch 2 — runner additions, then 12 more recipes ✅

**`core/` additions**

- [x] Multi-image output: `ImageSpec` — the agent lists `{file, prompt, aspect}`, the runner renders
- [x] Image post-processing: aspect crops, multi-size ICO, SVG → PNG (`resvg-py`), `use_as_cover`
- [x] Resolution tiers for image renders (`ImageSpec(size="4K")`, Gemini)
- [x] Lettering-only constraint for images that carry words (`text_ok`)
- [x] Audio: Gemini or ElevenLabs speech with **preset voices only** (30 Gemini, 6 ElevenLabs),
      ElevenLabs Music from an agent-written composition plan, MP3 via ffmpeg
- [x] Optional video step (`core.video.slideshow`), skipped when ffmpeg is missing
- [x] `requires=` preflight: a missing key fails the run before the agent starts
- [x] `NothingToDo` skip signal, `prepare()` errors fail cleanly, per-run tool lists via `ctx.state["tools"]`
- [x] Tests for each addition with the engines faked, plus faked-engine smoke runs of every Batch 2 recipe

**Recipes** (12, so 38 in all)

- [x] `comics` — four-panel strip, lettered (live run ✅)
- [x] `ai-meme-generator` — one AI-themed meme, optional idea queue
- [x] `daily-poster` — 2:3 poster from 200 themes
- [x] `future-cities` — speculative cityscapes of 68 real cities
- [x] `image-prompt-packs` — 5–8 prompts with a rendered example each
- [x] `wallpaper-packs` — three 4K masters, each cropped to desktop 16:9 + phone 9:16
- [x] `icon-packs` — 12 icons as SVG + PNG + ICO, plus a contact sheet (live run ✅)
- [x] `weekend-yearly-collections` — user-editable collections that each gain an image per run
- [x] `song-generator` — 37 song types, lyrics + ElevenLabs composition plan → MP3 (live run ✅)
- [x] `podcast-script-generator` — debate script with an invented cast (live run ✅)
- [x] `weekly-audio-podcast` — renders the oldest unrendered script with preset voices (live run ✅,
      13.5-minute episode)
- [x] `voiceover-script-generator` — narrated script → audio → vertical short (live run ✅)

**Batch 2 follow-ups**

- [x] Prune or rework `icon-packs` themes that invite real brand logos (a live "Browsers" run echoed
      real browser marks): 35 branded themes rewritten as generic functional sets; prompt forbids
      naming or echoing any product, company or brand
- [x] Review the other theme lists (posters, comics, memes, wallpapers, prompt packs) for brand,
      artist and real-person risk: clean (art movements only, no named artists or people)
- [x] Live samples in the READMEs of every recipe with a live run (Batches 1 and 2)
- [ ] Live runs, and samples, for the recipes that have only had faked-engine runs

## Not porting

- **Skipped for now (content risk):** `agent-persona` (real public figures), `ai-news-collage`,
  `weekly-news-montage`, `satirical-news` (all depict real people), `weekly-iam-idea` (employer-domain).
- **Superseded or legacy:** `rock-` / `country-` / `psychedelic-` / `weekly-song-generator` (covered
  by `song-generator`), `eleven-podcast`, `adhoc-eleven-podcast`.
- **Needs a licensing check first:** `cosmic-wallpapers` (sources images rather than generating them).

## 4. Viewer

- [x] `viewer/`: a static site that renders any `<output-dir>` from its `artifact.json` files —
      cards, playable games and apps in an iframe, stories, maps, image packs, audio players
      (`scripts/build_viewer.py`; Cronsole template `recipe-viewer-rebuild`)
- [ ] Demo feed of curated output for a future public site on `ai-automation-tools.dev`
- [ ] "Import into Cronsole" link on each recipe in the demo

## 5. Hardening

- [x] Browser smoke test for game and app recipes: loads the page in headless Chrome/Edge/Chromium,
      clicks and presses keys, fails the run on any uncaught error (six recipes)
- [x] Optional delivery step: `RECIPES_WEBHOOK_URL` (Discord, Slack or generic JSON)
- [ ] Drift check that flags when a public prompt falls behind its private original — belongs in the
      private routines repo, since it reads private paths this repo must never contain
- [ ] Import the pack through the Cronsole UI and let templates fire on schedule
- [ ] A week of scheduled runs across every recipe without intervention

## 6. Engines

- [ ] Pluggable text engines beyond Claude (Codex CLI, Gemini CLI) behind `core/engines/`, so every
      recipe has a Claude version and a pluggable version

## 7. Cronsole asks

- [ ] Multiple registry sources, so this repo can publish its own catalog
- [ ] A crontab compiler for the `linux` target
- [ ] Template-level secret requirements (`requiresSecrets: ["GEMINI_API_KEY"]`)

## 8. Publish checklist (only on the maintainer's go)

- [ ] Every batch above done, or explicitly deferred
- [ ] Full-history leak scan (`check_public.py` plus a history scan) clean
- [ ] Flip the repo public
- [ ] Ship the pack through Cronsole's registry and link it from the Cronsole site
- [ ] Add the repo to the org PR sweep, the Dependabot fleet docs and the org landing page
- [ ] Move the clone from `Custom/` to its permanent bucket and update the workspace docs
