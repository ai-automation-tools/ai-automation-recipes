<h1 align="center">📋 Changelog</h1>

<p align="center">
  <em>Every change to the recipes, the runner and the docs, newest first.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.12.2-2ea44f?style=for-the-badge" alt="Version 0.12.2">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Docs home"></a>
</p>

---

Entries that came off the [roadmap](ROADMAP.md) say which phase in italics. Recipe names before
0.6.0 are the old ones; 0.6.0 lists the renames.

## 0.12.2 — 2026-10-21

**Changed**
- `--output-dir` is optional: with no flag and no `RECIPES_OUTPUT_DIR`, runs land in `output/` inside
  the clone, which git already ignores. `build_viewer.py` uses the same default and reads `.env`, so
  the viewer finds the runs with no arguments.

**Added**
- `build_viewer.py --serve [PORT]`: rebuilds, then serves the output folder as a local site on
  `http://localhost:8000` (loopback only) until Ctrl+C. Served, **Open folder** lists an item's files.

## 0.12.1 — 2026-10-17

**Changed**
- `gemini` profile: the auth note no longer offers a Google login. Google's headless reference says
  the Gemini CLI was replaced by Antigravity for unpaid-tier and Google One users on 2026-06-18,
  and a PONG run on 0.64.0 fails with `IneligibleTierError`. `GEMINI_API_KEY` is the way in.
- Every profile's `verified` block moved to the versions seen on 2026-10-17 (claude 2.1.301, codex
  0.163.0, gemini 0.64.0, opencode 1.19.3); no flag was missing from any `--help`.

## 0.12.0 — 2026-10-15

**Added**
- **Live profiles.** `get_engine` uses the profile on this repo's `main`, fetched at most once a day
  into the user's cache, so a CLI flag fix reaches every clone and Cronsole edition without an
  update. The fetched copy must keep the bundled `binary` and be no older than it; offline or a bad
  fetch falls back to the bundled profile. A `$RECIPES_CLI_DIR` file still wins;
  `RECIPES_CLI_REMOTE=0` turns the fetch off and `RECIPES_CLI_URL` points it elsewhere.
- `scripts/new_cli.py <binary>`: drafts a profile for an unknown CLI from its own `--help` with an
  engine that already works, checks every flag against the help, pings the CLI through the draft,
  and prints the unattended-run flags it chose for review.

**Changed**
- CI runs with `RECIPES_CLI_REMOTE=0`, so it tests the profiles in the commit.
## Unreleased

**Added**
- 2026-10-19: a code-pinned [run diagram](diagrams/README.md) (Archify workflow, source
  `docs/diagrams/recipe-run-flow.json`): template → `core/runner.py` → agent CLI → checks → media →
  published folder, every node linked to the lines it describes. `scripts/build-diagram.mjs` builds it
  and copies it into `homepage/diagram/`, where it replaces the ASCII flow in the homepage's *How it
  works* section, live; `--check` flags drift and CI warns on it. Outside the runtime bundle, so
  `VERSION` is unchanged.
- 2026-10-19: a project homepage in `homepage/` (one static house-style page, no build), published
  to GitHub Pages at `ai-automation-recipes.ai-automation-tools.dev` by `.github/workflows/homepage.yml`.
  The sample viewer stays on the demo site. Outside the runtime bundle, so `VERSION` is unchanged.

**Docs**
- 2026-10-19: the roadmap moved onto the lab roadmap standard: centred header with stage badges,
  the port as a done phase, the public-release gates ticked from 2026-10-14 (a missing `SECURITY.md`
  added as the one open gate), and everything else under `## After public release`. The live-test
  table became one checkbox line per recipe; no items added or dropped otherwise.

**Added**
- README: pointer to the `automated-dev-pipeline` and `task-router` skills in agent-skills, for
  scheduling a whole pipeline rather than one recipe.

## 0.11.1 — 2026-10-14

**Changed**
- `codex` profile: `verified.liveRun` is true after `short-story --engine codex` published a
  2,835-word story; the first real recipe run on a CLI other than Claude *(Build: two-editions pilot)*.
- Cronsole editions: key help text names a task secret instead of the clone's `.env`, which that
  edition doesn't have.

**Verified**
- The three Cronsole editions ran from a local Cronsole on cronsole PR #323: template timeouts
  applied (40, 30 and 60 minutes), optional key secrets reported as optional, short-story published
  without a cover when no key was stored, comics rendered with its key as a task secret, and
  podcast-episode exited cleanly with nothing to render.

## 0.11.0 — 2026-10-14

**Added**
- **Any agent CLI.** Engines are JSON profiles in `core/engines/clis/`, read by one interpreter
  (`core/engines/cli.py`). The three hand-written adapters became `claude`, `codex` and `gemini`
  profiles that parse the same recorded output; `opencode`, `kimi` and `grok` are new. Adding a CLI
  is adding a file, here or in `$RECIPES_CLI_DIR`.
- `scripts/check_clis.py`: checks every profile's flags against the installed CLI's `--help`.
- **Cronsole editions** *(pilot: `short-story`, `comics`, `podcast-episode`)*: `recipe-<name>-cronsole`
  script templates in a new `ai-recipes-cronsole` pack. No clone or `.env`: the first run fetches a
  sha256-pinned runtime bundle into the user's cache, builds a virtualenv, and reads keys from
  optional task secrets. The template's *Agent CLI* parameter picks the engine.
- `scripts/build_bundle.py` (reproducible runtime bundle), a `VERSION` file, and a release workflow
  that publishes `v<VERSION>` only when the rebuilt bundle matches what `registry/` pins. CI fails
  a changed bundle under a version that's already released.
- `docs/UPSTREAMS.md`, the worklist for a new weekly CLI upstream routine that keeps the profiles
  current.

**Changed**
- `--engine` accepts any profile name; the Claude-alias rule (an alias means "your default" on
  any other CLI) moved into the profile as `claudeAliases`.

## 0.10.0 — 2026-10-14

**Released** *(Publish & promote)*
- The repo is public.
- Live samples at [ai-automation-recipes-demo.ai-automation-tools.dev](https://ai-automation-recipes-demo.ai-automation-tools.dev),
  from the separate `ai-automation-recipes-demo` repo: the 13 live runs so far, in the viewer.

**Added**
- `build_viewer.py --repo-url`: a hosted viewer links every item to its recipe and its Cronsole
  template, and drops the "Open folder" button that static hosts can't serve.

**Changed**
- `CONTRIBUTING.md` no longer bars recipes about real people. `agent-persona` and `satirical-news`
  ship as they are, with the guardrails their prompts carry *(Build: the real-people decision)*.
- The viewer and the repo icon moved from fuchsia to indigo (`#818cf8`); fuchsia already belonged
  to another app in the org's icon set.

**Fixed**
- CI's dry-run loop failed on `app-enhancement` and `pr-review`, the two recipes with required
  arguments. It now passes each its arguments, and gives `gh` the workflow token.

## 0.9.0 — 2026-10-14

**Added**
- Every remaining automation in the private fleet, 48 recipes in all. Seven of these were held back
  earlier the same day; the maintainer chose to port everything first and decide what the public
  set keeps later. The roadmap's *Build* list carries that decision.
- `news-collage` (Images): the major U.S. stories of a day, a week or a month, rotating, researched
  by Claude and rendered as one cartoon-editorial image. A day or a month is a six-panel grid, a
  week is one newsroom scene. Captions are 3 to 8 words drawn into the scene, and no real person's
  likeness is drawn. Ports the fleet's daily, weekly and monthly news images.
- `agent-persona` (Writing): the known-figure half of the persona pair. A debate card for a real
  person or an established character, researched from their public record, rotating across ten
  subcategories. It shares the `agent-personas` collection and refuses a figure who already has a
  card.
- `satirical-news` (Writing): *The Overcorrect*. One deadpan article across twelve rotating beats,
  optionally bent from a real story recorded as `inspired_by`, with a sidecar and up to four
  pictures when an image key is set.
- `iam-prototype` (Apps & Games): a runnable identity-and-access tool on synthetic data, rotating
  ten pain areas. Vendor-neutral by rule; standards like SCIM, OIDC and SAML are fair game.
- `finance-digest` (Research Digests): the eight finance and rewards newsletters as one
  topic-driven recipe. The rewards topics write from five points-and-miles feeds; the market topics
  read levels off public pages and cite them. The runner refuses an edition without the closing
  *Not Financial Advice* section, and Trade Ideas also needs its paper-only line and a Risk column.
- `news-digest`: a tenth topic, `iam-security`, from six security newsrooms read through an
  access-management lens.
- A seventh group, **Repo Ops**, with its own pack. `pr-review` reviews every open pull request in
  a repo you name and, only in `comment` or `merge` mode, posts reviews or squash-merges the PRs
  that pass every gate; in `report` mode the runner rejects a run that called a mutating `gh`
  command. `app-enhancement` makes one small additive change to a static app in a folder you name
  and publishes it as a patch; `--apply` writes it back.
- Tests for all of the above: 99 in the suite, all passing.

**Changed**
- The feed-window helper moved from `news-digest` into `core.digest`, so both digests share it.

**Docs**
- Recipe index, registry packs, counts and the footer chain updated for 48 recipes in seven groups.
  The roadmap's *Not ported* table now lists only what has nothing to port.

## 0.8.0 — 2026-10-14

**Added**
- Three recipes, 41 in all. `viral-recipe` (Food & Maps): the dish trending on TikTok, Instagram,
  YouTube, Reddit or Facebook, recreated under the same safety gate and Cook's Card as the other
  food recipes, with the originating post in the frontmatter and a *Why This Went Viral* section.
  `model-benchmark-watch` (Research Digests): the week's model releases and a sourced head-to-head
  table of the current frontier, handed the previous edition so it leads with what moved; the
  runner rejects a hedged number or an under-sourced table. `news-digest` (Research Digests): a
  briefing on one of nine topics written from that topic's own RSS feeds, which the runner fetches,
  windows and caps per source; topics, feeds, sections and palettes live in `topics.json`.
- The private fleet's ten general-interest newsletters are now covered: nine as `news-digest`
  topics (AI, science and space, world, tech policy, energy, gaming, media, emerging technology,
  cybersecurity) and the model watch as its own recipe. The roadmap's *Not ported* table says what
  stays out and why.
- `tests/test_new_recipes.py`: the three recipes' checks and hooks, and news-digest end to end with
  the feeds faked.

**Fixed**
- The feed fetcher now handles what real feeds ship: gzip bodies sent regardless of the request,
  a newline or BOM before the XML declaration, stray control bytes, and a bare `&` in content.
  All 102 `news-digest` feeds were fetched; 8 failed before this, 1 after (PYMNTS, fixed by the
  ampersand rule). Three publishers that refuse non-browser clients (CISA, Fierce Biotech, StreamTV
  Insider) were swapped for Krebs on Security, Endpoints News and Next TV.
- The fetcher's User-Agent is browser-shaped with the project named at the end; VentureBeat
  rate-limited the old "compatible; bot" shape.

**Docs**
- `CONTRIBUTING.md`: what's welcome, the pre-PR commands, and that the house rules apply to people
  too. *(roadmap: Launch-ready)*
- Every page re-read against the repo: counts (41 recipes, 43 templates, 11 digests), the three
  engines and their limits in the README, CLAUDE.md and the recipe guide, recipe-local data files
  and `ImageSpec(optional=True)` in the guide, and a *Where things stand* note plus the open
  live-run and launch items in the roadmap.

## 0.7.0 — 2026-10-14

**Added**
- Two more text engines behind the same interface, picked with `--engine`: `codex` (Codex CLI,
  `codex exec` in the `workspace-write` sandbox) and `gemini` (Gemini CLI, `-o json`). Each stages
  the recipe's skills where its agent looks for them (`.agents/skills/`, `.gemini/skills/`), and the
  run contract names that folder instead of assuming Claude's. A Claude model alias means "that
  CLI's default" on either. Built and tested against recorded CLI output; neither has had a live
  run. *(roadmap: Build)*
- `alternate-history` renders its eight scene prompts into `scenes/` at 16:9 when an image key is
  set, nine images a run with the cover. *(roadmap: Build)*
- `agent-persona-original` renders a square `avatar.png` from the same description as the cover.
  *(roadmap: Build)*
- `ImageSpec(optional=True)`: a recipe whose images are a bonus publishes text-only when no image
  key is set instead of failing before the agent runs. The two recipes above use it.
- `check_public.py --history` scans every blob in every commit on every ref, not just the tree.
  Clean today across 604 blobs; CI runs it on every push. *(roadmap: Launch-ready)*
- Issue templates for a recipe request and a bug in a recipe, with blank issues off and Cronsole's
  own tracker linked. *(roadmap: Launch-ready)*
- `tests/test_engines.py` and a third smoke script for the optional-image recipes (good, bad and
  keyless runs).

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
