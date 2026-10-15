<h1 align="center">🗺️ Roadmap</h1>

<p align="center">
  <em>Which recipes have had a real run, and the work left to do.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/live--tested-13_of_48-F59E0B?style=for-the-badge" alt="13 of 48 live-tested">
  <img src="https://img.shields.io/badge/visibility-public-2ea44f?style=for-the-badge" alt="Public">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Docs home"></a>
</p>

---

The repo went public on 2026-10-14, with live samples at
[ai-automation-recipes-demo.ai-automation-tools.dev](https://ai-automation-recipes-demo.ai-automation-tools.dev). Finished work moves out of this file
and into the [changelog](CHANGELOG.md). There's no paid tier planned:
this is the free companion to Cronsole.

**Where things stand (2026-10-14).** 48 recipes in seven groups, every one dry-run and faked-engine
tested in CI; 13 have had a real run. Any agent CLI can run them through a JSON profile; six are
bundled (Claude and Codex have run recipes for real; Gemini, OpenCode, Kimi and Grok not yet).
Three recipes have a pilot Cronsole edition, all three run from Cronsole. Every automation in the private fleet now has a recipe, including the seven that
were held back earlier in the day over real-people content and employer-domain work; the maintainer
chose to port everything first and decide what stays in the public set later. What has nothing to
port is listed at the bottom. Everything below is either a live run that hasn't happened yet or the
publish checklist.

## 🧪 Live-test status

Every recipe passes dry runs, unit tests and faked-engine runs in CI. This table tracks **real**
runs, with a real agent and real image, speech or music engines. They're being done over the coming
weeks. Tick a row once a live run has published and someone has read, played or listened to what it
made.

| Recipe | Group | Live run |
|:---|:---|:---|
| [**App Idea Card**](../recipes/app-idea-card/README.md) | Apps & Games | ✅ TapCheck · Cronsole test task from Thu 2026-10-15 |
| [**App Prototype**](../recipes/app-prototype/README.md) | Apps & Games | ⬜ not yet |
| [**Browser Extension**](../recipes/browser-extension/README.md) | Apps & Games | ✅ Exit Ramp |
| [**Finance App Prototype**](../recipes/finance-app-prototype/README.md) | Apps & Games | ⬜ not yet |
| [**IAM App Prototype**](../recipes/iam-prototype/README.md) | Apps & Games | ⬜ not yet · added 2026-10-14 |
| [**Browser Game**](../recipes/browser-game/README.md) | Apps & Games | ✅ Plumb Line (played in a browser) |
| [**Mobile Game**](../recipes/mobile-game/README.md) | Apps & Games | ⬜ not yet |
| [**PC Game Concept**](../recipes/pc-game-concept/README.md) | Apps & Games | ⬜ not yet |
| [**3D Print Design**](../recipes/3d-print-design/README.md) | Apps & Games | ⬜ not yet |
| [**Short Story**](../recipes/short-story/README.md) | Writing | ✅ The Blue Words |
| [**Serialized Novella**](../recipes/serialized-novella/README.md) | Writing | ✅ No Speech Detected, ch. 1 (seed run only) · next: a second run, to prove chapter 2 picks up the bible |
| [**Alternate History**](../recipes/alternate-history/README.md) | Writing | ⬜ not yet |
| [**Agent Persona (Known Figure)**](../recipes/agent-persona/README.md) | Writing | ⬜ not yet · added 2026-10-14 |
| [**Original Agent Persona**](../recipes/agent-persona-original/README.md) | Writing | ⬜ not yet |
| [**Satirical News**](../recipes/satirical-news/README.md) | Writing | ⬜ not yet · added 2026-10-14 |
| [**Content Idea**](../recipes/content-idea-gen/README.md) | Writing | ⬜ not yet |
| [**Funny AI Content**](../recipes/funny-ai-content/README.md) | Writing | ⬜ not yet · Cronsole test task, first run Fri 2026-10-16 |
| [**Family Recipe**](../recipes/family-recipe/README.md) | Food & Maps | ✅ Minnesota Tater Tot Hotdish |
| [**Regional Recipe**](../recipes/regional-recipe/README.md) | Food & Maps | ⬜ not yet |
| [**Viral Recipe**](../recipes/viral-recipe/README.md) | Food & Maps | ⬜ not yet · added 2026-10-14 |
| [**AI Map**](../recipes/ai-map/README.md) | Food & Maps | ⬜ not yet |
| [**Agent Toolkit**](../recipes/agent-toolkit/README.md) | Research Digests | ⬜ not yet |
| [**AI Stack Radar**](../recipes/ai-stack-radar/README.md) | Research Digests | ⬜ not yet |
| [**Open-Source Spotlight**](../recipes/oss-spotlight/README.md) | Research Digests | ⬜ not yet |
| [**Cool Websites**](../recipes/cool-websites/README.md) | Research Digests | ⬜ not yet |
| [**Top 10 GitHub Repos**](../recipes/top-10-github-repos/README.md) | Research Digests | ⬜ not yet |
| [**Trending Movers**](../recipes/trending-movers/README.md) | Research Digests | ✅ Trending Movers 2026-10-14 |
| [**Signal Sources**](../recipes/signal-sources/README.md) | Research Digests | ⬜ not yet |
| [**Security Toolkit**](../recipes/security-toolkit/README.md) | Research Digests | ⬜ not yet |
| [**Finance Toolkit**](../recipes/finance-toolkit/README.md) | Research Digests | ⬜ not yet |
| [**Model Benchmark Watch**](../recipes/model-benchmark-watch/README.md) | Research Digests | ⬜ not yet · added 2026-10-14 |
| [**News Digest**](../recipes/news-digest/README.md) | Research Digests | ⬜ not yet · added 2026-10-14; ten topics, so one live run per topic before it counts as done |
| [**Finance Digest**](../recipes/finance-digest/README.md) | Research Digests | ⬜ not yet · added 2026-10-14; eight topics, one live run each |
| [**Comic**](../recipes/comics/README.md) | Images | ✅ Circular Dependency |
| [**AI Meme**](../recipes/ai-meme-generator/README.md) | Images | ⬜ not yet |
| [**Poster**](../recipes/poster/README.md) | Images | ⬜ not yet |
| [**News Collage**](../recipes/news-collage/README.md) | Images | ⬜ not yet · added 2026-10-14; three windows (day, week, month), one live run each |
| [**Future Cities 2500**](../recipes/future-cities/README.md) | Images | ⬜ not yet |
| [**Image Prompt Pack**](../recipes/image-prompt-packs/README.md) | Images | ⬜ not yet |
| [**Wallpaper Pack**](../recipes/wallpaper-packs/README.md) | Images | ⬜ not yet · heaviest: three 4K renders per run |
| [**Icon Pack**](../recipes/icon-packs/README.md) | Images | ✅ Browser Actions (re-run after de-branding) |
| [**Image Collections**](../recipes/image-collections/README.md) | Images | ⬜ not yet · needs research; check the seeded collections file |
| [**Song**](../recipes/song-generator/README.md) | Audio | ✅ Every Stone I Set (`folk` only) · other song types untested |
| [**Podcast Script**](../recipes/podcast-script-generator/README.md) | Audio | ✅ Should We Text the Aliens First? |
| [**Podcast Episode**](../recipes/podcast-episode/README.md) | Audio | ✅ Should We Text the Aliens First? (13.5 min) |
| [**Voiceover Script**](../recipes/voiceover-script-generator/README.md) | Audio | ✅ The Spacecraft Lost to a Unit Label |
| [**PR Review**](../recipes/pr-review/README.md) | Repo Ops | ⬜ not yet · added 2026-10-14; report mode first, then comment, then merge on a throwaway repo |
| [**App Enhancement**](../recipes/app-enhancement/README.md) | Repo Ops | ⬜ not yet · added 2026-10-14; patch mode first, then `--apply` on a copy |

## 🔨 Build

- [ ] A live `news-collage` run per window: day (the six-panel grid with a readable timestamp),
      week (one scene, title and date range spelled right), month. The captions are the thing to
      check; six garbled captions was the fleet's most common visible defect
- [ ] A live `agent-persona` run and a live `satirical-news` run, read for the guardrails the
      prompts carry (public persona only, no fabricated quotes presented as real, satire labelled)
- [ ] A live `iam-prototype` run: it must stay vendor-neutral and run on synthetic data
- [ ] A live `finance-digest` run per topic; the `trade-ideas` topic must carry its paper-only
      line on every idea and the disclaimer at the end
- [ ] A live `pr-review` run in `report` mode on a repo with open PRs, then `comment`, then `merge`
      on a throwaway repo; a live `app-enhancement` run in patch mode, then `--apply` on a copy

- [ ] A second `serialized-novella` run writes chapter 2 from the saved story bible, keeping names,
      places and the rolling synopsis consistent
- [ ] A live `alternate-history` run with an image key: the eight scenes read as one illustrated
      piece, and the shared style survives eight separate image calls
- [ ] A live `agent-persona-original` run: the avatar and the cover are recognisably the same person
- [ ] **Two-editions pilot** (0.11.0). Every recipe gets a Cronsole edition and runs on any CLI;
      three recipes go first:
  - [x] `short-story`, `comics` and `podcast-episode` imported from `ai-recipes-cronsole` into a
        Cronsole running cronsole PR #323 and run once each (2026-10-14): short-story published
        with no image key (180 s including first-run setup), comics published with its key as a
        task secret (44 s, cached runtime), podcast-episode exited cleanly with nothing to render
  - [x] One pilot recipe run for real on a second CLI: `short-story --engine codex`, 2,835 words
        in 4 minutes (2026-10-14); `codex` profile marked `liveRun`
  - [ ] A real `podcast-episode` render from the Cronsole edition, after a `podcast-script-generator`
        run leaves an unrendered script
  - [ ] Then add every other recipe to `NATIVE` in `scripts/build_registry.py`, and decide whether
        the clone edition stays a full set or shrinks to the editing path
- [ ] A live run on `--engine gemini`. The Gemini CLI first needs a headless auth that works on
      the maintainer's machine: its Google login is on the retired free Code Assist tier, so it
      will be `GEMINI_API_KEY`
- [ ] Antigravity (`agy`) has no profile: `agy --print=<prompt>` hung with no output headless on
      2026-10-14. Retried on 1.3.5 (2026-10-15), which now has `--output-format json|stream-json`
      and `--print-timeout`: still stalls. The `init` event arrives, the model request goes out,
      and no turn ever starts (`num_turns: 0`). It doesn't depend on the model (Gemini 3.8 Flash and
      Claude Sonnet 4.6 both stall), the folder (temp folder or a known workspace),
      `--dangerously-skip-permissions`, or MCP servers (`github` disabled made no difference).
      Next: confirm an interactive `agy` session answers on the same login, then retry with
      `scripts/new_cli.py agy`
- [x] Profiles stay current without an update: runs use the newest profile on `main`, cached a day,
      bundled copy as the fallback (0.12.0)
- [x] `scripts/new_cli.py <binary>` drafts a profile for any other CLI from its `--help`, checks the
      flags and pings it (0.12.0; tried on OpenCode, which drafted and answered)
- [ ] Map recipe tool names to per-CLI permission rules where a CLI has them (Grok's `--allow`),
      so more profiles can be `allowlist` instead of `advisory`
- [ ] A live `news-digest` run on one topic, then one per topic over three weeks of the Mon/Wed/Fri
      default schedule; watch whether the 16-per-source cap keeps the loud feeds (Nature, Podnews,
      Deadline) from owning a week, and whether five sections is the right number for every topic
- [ ] A live `model-benchmark-watch` run, then a second so the previous-edition handover is seen
      working (the second should lead with movement, not restate the table)
- [ ] A live `viral-recipe` run: does Claude find something genuinely current, and does the
      safety gate catch the kind of shortcut viral food carries
- [ ] New automations that aren't ports (every fleet job now has a recipe, see *Not ported*).
      Candidates the current core already supports: a release-notes digest that watches a list of
      GitHub repos the user names, a weekly quiz built from the news digests, a "year in review"
      that reads a collection's artifacts and writes a retrospective

## 🚦 Proving it

- [ ] Live runs for every ⬜ recipe in the table above, each sample added to its README
- [ ] The Cronsole test tasks fire on their own and their run history shows a published artifact
      (first runs Thu 2026-10-15 and Fri 2026-10-16)
- [ ] One full pack scheduled through Cronsole for a week with no manual fixes
- [ ] Re-probe every `news-digest` feed monthly (101 of 102 fetched and parsed on 2026-10-14 after
      the fetcher learned gzip, BOMs, control bytes and bare ampersands; three publishers that 403
      non-browsers were swapped out)
- [ ] Add each new live run's folder to the demo site

## 📣 Publish & promote

- [ ] Packs shipped through Cronsole's registry and linked from the Cronsole site (needs Cronsole's
      multiple-registry-sources work, under *Later*)
- [ ] A one-click "Import into Cronsole" on the demo, once Cronsole can import a template by URL;
      today each sample links to its recipe and its template file

## 🔭 Later

Changes to Cronsole itself, tracked here because these recipes would use them:

- [ ] Multiple registry sources, so this repo can publish its own catalog
- [ ] A crontab compiler for the `linux` target
- [ ] Template-level secret requirements (`requiresSecrets: ["GEMINI_API_KEY"]`). Partly covered by
      cronsole PR #323: optional `${secret.NAME?}` references, and the apply response lists the
      secrets a new task still needs
- [ ] `execution.timeoutSec` for command-line (`exec`) native templates; PR #323 covers `script`
      templates only, so the clone edition still gets Cronsole's 5-minute default

## 🚫 Not ported

What's left of the private fleet with nothing to port. The content jobs that were on this list
until 2026-10-14 (the three news images, both persona kinds, the satirical paper, the IAM prototype,
the eight finance and rewards digests, the IAM briefing, the PR review and the tool-enhancement job)
are recipes now; see the *Build* list for the decision they still owe.

| Job | Reason |
|:---|:---|
| `rock-` / `country-` / `psychedelic-` / `rap-` / `weekly-song` | Consolidated into the fleet's one song job in September; `song-generator` carries every type |
| `weekly-podcast`, `weekly-audio-podcast` | Deprecated on the fleet in July; the podcast pair here is their replacement. The two ElevenLabs form front-ends are the same artifacts from a pasted script or a topic form, which `podcast-script-generator` + `podcast-episode` cover |
| `cosmic-wallpapers`, `future-cities` (fleet job) | Retired on the fleet; `wallpaper-packs` and `future-cities` here are the successors |
| `fleet-doctor`, `fleet-status`, `repo-pull`, `watchdog` | Health checks, a status feed and a git pull for one specific box. Nothing a recipe could carry to another machine |
| the three data-sync workflows behind a retired rewards app | Retired with the app they fed |

---

<p align="center">
  <a href="README.md">← Docs home</a> ·
  <a href="ADDING-A-RECIPE.md">Adding a recipe</a> ·
  <a href="CHANGELOG.md">Next: Changelog →</a>
</p>
