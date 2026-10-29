<h1 align="center">🗺️ Roadmap</h1>

<p align="center">
  <em>Every recipe on every agent CLI, then better and more recipes.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/stage-public_since_2026--10--14-2ea44f?style=for-the-badge" alt="Stage: public since 2026-10-14">
  <img src="https://img.shields.io/badge/claude-48_of_48-8B5CF6?style=for-the-badge" alt="Claude: 48 of 48">
  <img src="https://img.shields.io/badge/other_CLIs-3_of_288-F59E0B?style=for-the-badge" alt="Other CLIs: 3 of 288">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Back to docs"></a>
</p>

---

The weekly roadmap routine works this file top to bottom every Wednesday. **Every item above
`## After public release` is a go-live gate.** Ticking an item adds its line to the
[changelog](CHANGELOG.md) and updates any doc it made stale, in the same commit. There's no paid
tier planned: this is the free companion to Cronsole, so there is no Revenue group.

Markers: `- [ ]` open, `- [-]` claimed by a run in progress, `- [x]` done, `- [!]` blocked (the
reason follows on the line). `small` marks an item a check verifies; `🔒 Needs Mike` marks one only
the maintainer can do.

> [!NOTE]
> **Where we are, 2026-10-26.** 48 recipes in seven groups. Every one already runs for real on
> Claude in the maintainer's private fleet, so this roadmap no longer tracks a live run per recipe.
> What's left is portability: each recipe has to work on every agent CLI with a profile, not just
> Claude. After that the work is making recipes better and adding new ones.

## 🔨 Phase 1: Port the fleet (done 2026-10-14)

- [x] 48 recipes in seven groups, each with dry-run and faked-engine tests in CI — done 2026-10-14:
      versions 0.1.0 to 0.10.0 in the [changelog](CHANGELOG.md)

## 🚦 Public release

- [x] CI, verified README, clean full-history secret scan, MIT licence, live demo site — done
      2026-10-14; see 0.1.0 to 0.10.0 in the [changelog](CHANGELOG.md)
- [x] `small` `SECURITY.md` with how to report a vulnerability — done 2026-10-28: `SECURITY.md` at the
      root, linked from the README footer. It points at GitHub private vulnerability reporting, which
      is still switched off on the repo (see [open questions](OPEN-QUESTIONS.md))

## After public release

Nothing below blocks go-live.

### 🔌 CLI coverage

A recipe counts as working on a CLI when `run.py --engine <name>` publishes an artifact that passes
the recipe's own output checks, with no change to the recipe. Recipe content is proven on Claude, so
a CLI run only has to show the contract holds: the prompt is followed, the right files land in the
staging folder, staged skills are found, and the tools the recipe needs exist on that CLI.

What a CLI has to provide depends on the **Tools** column: `files` is the default file tools only,
`web` adds web search and fetch, `fetch` adds fetch only, `bash` adds a shell.

Eleven recipes also make billed image, speech or music calls (the **Also needs** column of the
[recipe index](../recipes/README.md)); the keys are in the maintainer's environment, and a routine
run takes at most two of those recipes. `pr-review` runs only in `report` mode and
`app-enhancement` only in patch mode, never `--apply`.

#### Making the sweep cheap

- [ ] A `scripts/cli_sweep.py --engine <name> [--recipe <name>…]` that runs recipes on one CLI,
      records pass or fail with the failing check, and rewrites that CLI's column in the matrix
      below. Done when a sweep of two `files` recipes on `claude` updates their cells and a unit test
      covers the matrix rewrite. Without it, 288 runs is too much to do by hand
- [ ] A `web` recipe on an advisory CLI that has no web tool fails before the agent starts, with a
      message naming the missing tool, instead of publishing an unsourced artifact (unit test with a
      faked profile)
- [ ] Each profile's `verified` block records which recipes passed (`liveRuns: [...]`) instead of a
      single `liveRun` flag, and the [CLI profiles](../core/engines/clis/README.md) table reads it
- [ ] `kimi` passes the prompt as an argument, and Windows caps a command line at 32,767
      characters: `news-digest` (~82k), `finance-digest` (~55k) and `oss-spotlight` (~36k) can't
      start. Move it to `prompt: "file"` with a `-p` that points at the file, as the `agy` profile
      does, and prove it on `news-digest`
- [ ] Map recipe tool names to per-CLI permission rules where a CLI has them (Grok's `--allow`),
      so more profiles can be `allowlist` instead of `advisory`

#### Per CLI

Each item is done when every cell in that CLI's column that needs no key is ✅, or ❌ with its own
item saying why. A run works through one CLI's cells in matrix order and notes its progress here.

- [x] **Claude** (`claude`): every recipe, through the private fleet — done 2026-10-26
- [ ] **Codex** (`codex`): `short-story` ran for real on 2026-10-14 (2,835 words in 4 minutes).
      Next: one recipe per tools class (`web`, `fetch`, `bash`), then the rest
- [ ] **OpenCode** (`opencode`): answers a smoke prompt (1.19.3, 2026-10-17). Next: `short-story`,
      then one recipe per tools class, then the rest
- [ ] **Kimi Code** (`kimi`): answers a smoke prompt (0.18.0, 2026-10-17). Same order as OpenCode
- [ ] **Gemini CLI** (`gemini`): answers on `GEMINI_API_KEY` (0.64.0, 2026-10-26) once
      `~/.gemini/settings.json` has `"security.auth.selectedType": "gemini-api-key"`; a cached Google
      login wins over the key otherwise, and that login is on the retired free tier. `short-story`
      ran for real on 2026-10-26 (3,540 words in 5 minutes). Next: one recipe per tools class
- [ ] **Antigravity** (`agy`): profile added 2026-10-26 (1.4.7), on `GEMINI_API_KEY` with
      `"modelProvider": "gemini"` per the docs. The earlier stall was auth plus the user's MCP
      servers: headless agy sends the message and never starts the turn while they load, so the
      profile runs it from an isolated home. `short-story` ran for real on 2026-10-26 (2,074 words in
      3 minutes). Next: one recipe per tools class
- [ ] **Grok Build** (`grok`): flags checked against `--help` only. Needs an `XAI_API_KEY` (the
      docs' headless path) or `grok login` on the maintainer's machine, then the smoke prompt and
      the same order 🔒 Needs Mike

#### Matrix

✅ publishes on that CLI · ⬜ not run yet · ❌ fails (an item above says why)

| Recipe | Tools | Claude | Codex | OpenCode | Kimi | Grok | Gemini | agy |
|:---|:---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| [app-idea-card](../recipes/app-idea-card/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [app-prototype](../recipes/app-prototype/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [browser-extension](../recipes/browser-extension/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [finance-app-prototype](../recipes/finance-app-prototype/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [iam-prototype](../recipes/iam-prototype/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [browser-game](../recipes/browser-game/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [mobile-game](../recipes/mobile-game/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [pc-game-concept](../recipes/pc-game-concept/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [3d-print-design](../recipes/3d-print-design/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [short-story](../recipes/short-story/README.md) | files | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| [serialized-novella](../recipes/serialized-novella/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [alternate-history](../recipes/alternate-history/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [agent-persona](../recipes/agent-persona/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [agent-persona-original](../recipes/agent-persona-original/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [satirical-news](../recipes/satirical-news/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [content-idea-gen](../recipes/content-idea-gen/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [funny-ai-content](../recipes/funny-ai-content/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [family-recipe](../recipes/family-recipe/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [regional-recipe](../recipes/regional-recipe/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [viral-recipe](../recipes/viral-recipe/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [ai-map](../recipes/ai-map/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [agent-toolkit](../recipes/agent-toolkit/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [ai-stack-radar](../recipes/ai-stack-radar/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [oss-spotlight](../recipes/oss-spotlight/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [cool-websites](../recipes/cool-websites/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [top-10-github-repos](../recipes/top-10-github-repos/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [trending-movers](../recipes/trending-movers/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [signal-sources](../recipes/signal-sources/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [security-toolkit](../recipes/security-toolkit/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [finance-toolkit](../recipes/finance-toolkit/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [model-benchmark-watch](../recipes/model-benchmark-watch/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [news-digest](../recipes/news-digest/README.md) | fetch | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [finance-digest](../recipes/finance-digest/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [comics](../recipes/comics/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [ai-meme-generator](../recipes/ai-meme-generator/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [poster](../recipes/poster/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [news-collage](../recipes/news-collage/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [future-cities](../recipes/future-cities/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [image-prompt-packs](../recipes/image-prompt-packs/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [wallpaper-packs](../recipes/wallpaper-packs/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [icon-packs](../recipes/icon-packs/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [image-collections](../recipes/image-collections/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [song-generator](../recipes/song-generator/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [podcast-script-generator](../recipes/podcast-script-generator/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [podcast-episode](../recipes/podcast-episode/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [voiceover-script-generator](../recipes/voiceover-script-generator/README.md) | web | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [pr-review](../recipes/pr-review/README.md) | bash | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| [app-enhancement](../recipes/app-enhancement/README.md) | files | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

### ✨ Enhance

- [ ] Move the Gemini model defaults off models Google has retired or restricted. Image:
      `gemini-3.1-flash-image` in `core/images/__init__.py` is deprecated; the replacement is
      `gemini-nano-banana-2.1`. Speech: `gemini-2.5-flash-preview-tts` in `core/audio/__init__.py`
      is limited to accounts that already used it; the replacements are `gemini-3.8-flash-tts` and
      `gemini-3.8-flash-lite-tts` (<https://ai.google.dev/gemini-api/docs/changelog>, 2026-09-18 and
      2026-10-06). Also update `.env.example`, `docs/ARCHITECTURE.md` and the `image-prompt-craft`
      engine notes. Done when one real image call and one real speech call succeed on the new defaults
- [ ] Python 3.10 reached end of life on 2026-10-01 (<https://devguide.python.org/versions/>). Raise
      the floor to 3.11 in `AGENTS.md`, the docs, CI and the Cronsole edition's interpreter notes.
      Done when CI runs 3.11 and newer only and the tests pass
- [ ] Cronsole editions for every recipe: add the rest to `NATIVE` in `scripts/build_registry.py`
      (three are there now: `short-story`, `comics`, `podcast-episode`), then decide whether the
      clone edition stays a full set or shrinks to the editing path
- [ ] The Cronsole template's *Agent CLI* parameter lists only CLIs whose matrix column has at least
      one ✅, so nobody schedules a recipe on a CLI nothing has run on
- [ ] Add a sample from each new CLI's first passing run to the
      [demo site](https://ai-automation-recipes-demo.ai-automation-tools.dev), labelled with the CLI
      that made it

### ➕ New recipes

Every private fleet job already has a recipe (see *Not ported*), so new ones are net-new. Each goes
into `recipes/README.md`, `CATEGORY_PACKS` and the matrix above. Candidates the current core already
supports:

- [ ] A release-notes digest that watches a list of GitHub repos the user names
- [ ] A weekly quiz built from the news digests
- [ ] A "year in review" that reads a collection's artifacts and writes a retrospective

### 🔭 Later

Changes to Cronsole itself, tracked here because these recipes would use them:

- [ ] Multiple registry sources, so this repo can publish its own catalog and the packs can be
      linked from the Cronsole site
- [ ] Import a template by URL, for a one-click "Import into Cronsole" on the demo
- [ ] A crontab compiler for the `linux` target
- [ ] Template-level secret requirements (`requiresSecrets: ["GEMINI_API_KEY"]`). Partly covered by
      cronsole PR #323: optional `${secret.NAME?}` references, and the apply response lists the
      secrets a new task still needs
- [ ] `execution.timeoutSec` for command-line (`exec`) native templates; PR #323 covers `script`
      templates only, so the clone edition still gets Cronsole's 5-minute default

### 🚫 Not ported

What's left of the private fleet with nothing to port.

| Job | Reason |
|:---|:---|
| `rock-` / `country-` / `psychedelic-` / `rap-` / `weekly-song` | Consolidated into the fleet's one song job in September; `song-generator` carries every type |
| `weekly-podcast`, `weekly-audio-podcast` | Deprecated on the fleet in July; `podcast-script-generator` + `podcast-episode` replace them |
| `cosmic-wallpapers`, `future-cities` (fleet job) | Retired on the fleet; `wallpaper-packs` and `future-cities` here are the successors |
| `fleet-doctor`, `fleet-status`, `repo-pull`, `watchdog` | Health checks, a status feed and a git pull for one specific box. Nothing a recipe could carry to another machine |
| the three data-sync workflows behind a retired rewards app | Retired with the app they fed |

---

<p align="center">
  <a href="README.md">← Docs home</a> ·
  <a href="ADDING-A-RECIPE.md">Adding a recipe</a> ·
  <a href="CHANGELOG.md">Next: Changelog →</a>
</p>
