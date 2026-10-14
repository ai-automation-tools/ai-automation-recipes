<h1 align="center">🗺️ Roadmap</h1>

<p align="center">
  <em>Which recipes have had a real run, and the work left before this repo goes public.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/live--tested-13_of_41-F59E0B?style=for-the-badge" alt="13 of 41 live-tested">
  <img src="https://img.shields.io/badge/visibility-private-6B7280?style=for-the-badge" alt="Private">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Docs home"></a>
</p>

---

The repo stays private until the publish phase below is done and the maintainer says go. Finished
work moves out of this file and into the [changelog](CHANGELOG.md). There's no paid tier planned:
this is the free companion to Cronsole.

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
| [**Browser Game**](../recipes/browser-game/README.md) | Apps & Games | ✅ Plumb Line (played in a browser) |
| [**Mobile Game**](../recipes/mobile-game/README.md) | Apps & Games | ⬜ not yet |
| [**PC Game Concept**](../recipes/pc-game-concept/README.md) | Apps & Games | ⬜ not yet |
| [**3D Print Design**](../recipes/3d-print-design/README.md) | Apps & Games | ⬜ not yet |
| [**Short Story**](../recipes/short-story/README.md) | Writing | ✅ The Blue Words |
| [**Serialized Novella**](../recipes/serialized-novella/README.md) | Writing | ✅ No Speech Detected, ch. 1 (seed run only) · next: a second run, to prove chapter 2 picks up the bible |
| [**Alternate History**](../recipes/alternate-history/README.md) | Writing | ⬜ not yet |
| [**Original Agent Persona**](../recipes/agent-persona-original/README.md) | Writing | ⬜ not yet |
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
| [**News Digest**](../recipes/news-digest/README.md) | Research Digests | ⬜ not yet · added 2026-10-14; nine topics, so one live run per topic before it counts as done |
| [**Comic**](../recipes/comics/README.md) | Images | ✅ Circular Dependency |
| [**AI Meme**](../recipes/ai-meme-generator/README.md) | Images | ⬜ not yet |
| [**Poster**](../recipes/poster/README.md) | Images | ⬜ not yet |
| [**Future Cities 2500**](../recipes/future-cities/README.md) | Images | ⬜ not yet |
| [**Image Prompt Pack**](../recipes/image-prompt-packs/README.md) | Images | ⬜ not yet |
| [**Wallpaper Pack**](../recipes/wallpaper-packs/README.md) | Images | ⬜ not yet · heaviest: three 4K renders per run |
| [**Icon Pack**](../recipes/icon-packs/README.md) | Images | ✅ Browser Actions (re-run after de-branding) |
| [**Image Collections**](../recipes/image-collections/README.md) | Images | ⬜ not yet · needs research; check the seeded collections file |
| [**Song**](../recipes/song-generator/README.md) | Audio | ✅ Every Stone I Set (`folk` only) · other song types untested |
| [**Podcast Script**](../recipes/podcast-script-generator/README.md) | Audio | ✅ Should We Text the Aliens First? |
| [**Podcast Episode**](../recipes/podcast-episode/README.md) | Audio | ✅ Should We Text the Aliens First? (13.5 min) |
| [**Voiceover Script**](../recipes/voiceover-script-generator/README.md) | Audio | ✅ The Spacecraft Lost to a Unit Label |

## 🔨 Build

- [ ] A second `serialized-novella` run writes chapter 2 from the saved story bible, keeping names,
      places and the rolling synopsis consistent
- [ ] A live `alternate-history` run with an image key: the eight scenes read as one illustrated
      piece, and the shared style survives eight separate image calls
- [ ] A live `agent-persona-original` run: the avatar and the cover are recognisably the same person
- [ ] A live run on `--engine codex`, then on `--engine gemini` (the engines are built and
      unit-tested against recorded CLI output; neither has written a real recipe yet). Gemini first
      needs a headless auth that works on the maintainer's machine: the CLI's Google login is on the
      retired free Code Assist tier, so it will be `GEMINI_API_KEY`
- [ ] Decide whether the Cronsole templates expose `engine` as a parameter once Codex and Gemini
      have each shipped a recipe. Until then every template runs Claude

## 🚦 Launch-ready

- [ ] Live runs for every ⬜ recipe in the table above, each sample added to its README
- [ ] The Cronsole test tasks fire on their own and their run history shows a published artifact
      (first runs Thu 2026-10-15 and Fri 2026-10-16)
- [ ] One full pack scheduled through Cronsole for a week with no manual fixes
- [ ] Re-run `check_public.py --history` the day before the flip (clean on 2026-10-14, 604 blobs;
      CI runs it on every push)

## 📣 Publish & promote

Only on the maintainer's go.

- [ ] Repo flipped to public
- [ ] Packs shipped through Cronsole's registry and linked from the Cronsole site
- [ ] A demo viewer of curated output on a subdomain of `ai-automation-tools.dev`, with an "Import
      into Cronsole" link on each recipe
- [ ] Repo added to the org PR sweep, the Dependabot fleet docs and the org landing page
- [ ] Clone moved out of `Custom/` to its permanent folder, with the workspace docs updated

## 🔭 Later

Changes to Cronsole itself, tracked here because these recipes would use them:

- [ ] Multiple registry sources, so this repo can publish its own catalog
- [ ] A crontab compiler for the `linux` target
- [ ] Template-level secret requirements (`requiresSecrets: ["GEMINI_API_KEY"]`)

## 🚫 Not ported

Jobs from the private fleet that stay out, and why.

| Job | Reason |
|:---|:---|
| `agent-persona`, `ai-news-collage`, `weekly-news-montage`, `satirical-news` | Depict real people |
| `weekly-iam-idea` | Employer-domain work |
| `rock-` / `country-` / `psychedelic-` / `weekly-song-generator` | Covered by `song-generator` types |
| `eleven-podcast`, `adhoc-eleven-podcast` | Legacy, replaced by the podcast pair |
| `cosmic-wallpapers` | Sources images instead of generating them; needs a licensing check first |
| `daily-pr-review`, `weekly-tool-enhancement`, `fleet-doctor`, `repo-pull` | Ops jobs on the private fleet itself, not content |
| the finance and rewards newsletters (stock market, trade suggestions, investment insights, card bonuses, portals, transfer bonuses) | Personal finance, and the IAM briefing is employer-domain. The nine general-interest newsletters became `news-digest` topics |

---

<p align="center">
  <a href="README.md">← Docs home</a> ·
  <a href="ADDING-A-RECIPE.md">Adding a recipe</a> ·
  <a href="CHANGELOG.md">Next: Changelog →</a>
</p>
