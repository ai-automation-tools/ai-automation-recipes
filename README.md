<h1 align="center">AI Automation Recipes</h1>

<p align="center">
  <em>Scheduled Claude Code automations that research, write, build and illustrate things on their own —<br>packaged so you can import them into Cronsole and run them on your own machine.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-pilot-F97316?style=flat-square" alt="Status: pilot">
  <img src="https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/engine-Claude_Code-8B5CF6?style=flat-square" alt="Engine: Claude Code">
  <img src="https://img.shields.io/badge/schedule_with-Cronsole-0078D4?style=flat-square" alt="Schedule with Cronsole">
  <img src="https://img.shields.io/badge/license-MIT-16A34A?style=flat-square" alt="MIT">
</p>

---

## What this is

Each **recipe** is one automation: a prompt, the skills it loads, and a small Python runner. Run it
once by hand, or schedule it and let it build a collection over weeks — a backlog of researched app
ideas, a shelf of playable browser games, an anthology of short stories.

Every recipe writes into the same folder layout with an `artifact.json` beside each piece, so
anything that can read JSON can display the results.

38 recipes in 6 groups. Each group is also a Cronsole pack, and `ai-recipes` imports them all. Schedules are defaults; change them on import.
**Apps & Games** — pack `ai-recipes-apps-games`

| Recipe | Makes | Schedule |
|:---|:---|:---|
| [`daily-app-card`](recipes/daily-app-card/README.md) | Claude researches a current trend and writes a one-page app pitch (problem, user, MVP, monetization, risks, sources) with a concept-art cover | Daily |
| [`weekly-app-prototype`](recipes/weekly-app-prototype/README.md) | Claude researches a current trend and builds a runnable single-page app prototype — README pitch, requirements, HTML/CSS/JS and sample data — with a concept-art cover | Weekly (Thu) |
| [`weekly-browser-extension`](recipes/weekly-browser-extension/README.md) | Claude researches a current pain point and builds a loadable Manifest V3 extension plus a mock-browser demo that shares the popup's code — README pitch, requirements, permissions table — with a concept-art cover | Weekly (Mon) |
| [`weekly-financial-idea`](recipes/weekly-financial-idea/README.md) | Claude builds a runnable personal-finance app prototype (budgeting, saving, rewards, debt, investing tools…) on synthetic data, rotating themes so the catalogue stays balanced | Monthly (6) |
| [`weekly-browser-game`](recipes/weekly-browser-game/README.md) | Claude designs and builds a complete single-file HTML game in a rotating genre — playable from file://, touch-aware, syntax-checked before it is published — with a design brief and key-art cover | Weekly (Sat) |
| [`weekly-mobile-game`](recipes/weekly-mobile-game/README.md) | Claude designs and builds a portrait, touch-first phone game as one HTML file inside an on-screen phone frame, in a rotating genre — syntax-checked before publishing — with a design brief and key art | Weekly (Thu) |
| [`weekly-pc-game-concept`](recipes/weekly-pc-game-concept/README.md) | Claude researches this week's genre and writes an original PC game concept — a design brief with a buildable core loop and 6-week prototype plan, a one-page pitch, sources and key art | Weekly (Mon) |
| [`weekly-3d-print-ideas`](recipes/weekly-3d-print-ideas/README.md) | Claude researches what sells and writes one original FDM-printable product design — README spec, machine-readable design-spec.json, sources and a product mockup — precise enough to model in CAD | Tue, Thu, Sat |

**Writing** — pack `ai-recipes-writing`

| Recipe | Makes | Schedule |
|:---|:---|:---|
| [`weekly-short-story`](recipes/weekly-short-story/README.md) | Claude writes a complete 2,000–4,000-word short story in a rotating genre, avoiding every premise already written, with a portrait cover illustration | Weekly (Sun) |
| [`serialized-novella`](recipes/serialized-novella/README.md) | Claude writes the next chapter of an ongoing novel against its story bible — inventing the bible on the first run — keeping continuity through a rolling synopsis and the latest chapters, with a chapter illustration | Weekly (Mon) |
| [`alternate-history`](recipes/alternate-history/README.md) | Claude writes an eight-section "what if" timeline from one real historical divergence, with scene-by-scene illustration prompts and a portrait cover | Weekly (Fri) |
| [`agent-persona-original`](recipes/agent-persona-original/README.md) | Claude invents one original, debate-ready character in a rotating archetype group and writes a portable second-person persona card any model can adopt, with an illustrated portrait cover | Weekly (Thu) |
| [`content-idea-gen`](recipes/content-idea-gen/README.md) | Claude researches what is working on social platforms in a rotating topic area and pitches one automatable content series — hook, treatment, automation angle, sources — with a cover | Weekly (Wed) |
| [`weekly-funny-ai-content`](recipes/weekly-funny-ai-content/README.md) | Claude writes one satirical content concept about an absurd AI-agent use case — the bit, script beats, the fake automation angle — with a wordless cover gag | Weekly (Fri) |

**Food & Maps** — pack `ai-recipes-food-maps`

| Recipe | Makes | Schedule |
|:---|:---|:---|
| [`recipe-of-the-week`](recipes/recipe-of-the-week/README.md) | Claude researches a well-loved family dish from a rotating cuisine and writes a cookable recipe with complete allergen labeling, gated by a food-safety scanner, plus a cover and a self-contained Cook's Card page | Weekly (Sat) |
| [`weekly-regional-recipe`](recipes/weekly-regional-recipe/README.md) | Claude adds one authentic dish a week to a regional recipe library, always filling the region with the fewest recipes | Weekly (Fri) |
| [`weekly-ai-map`](recipes/weekly-ai-map/README.md) | Claude researches 8–20 real places on a rotating theme and builds a standalone interactive Leaflet map with categories, popups and directions links, plus a companion guide, sources, and a cover | Weekly (Mon) |

**Research Digests** — pack `ai-recipes-digests`

| Recipe | Makes | Schedule |
|:---|:---|:---|
| [`agent-toolkit`](recipes/agent-toolkit/README.md) | Claude researches 24+ things to install into an LLM or coding agent — skills, commands, MCP servers, plugins, hooks, harnesses — half proven, half new | Monthly (22) |
| [`ai-stack-radar`](recipes/ai-stack-radar/README.md) | Claude researches 24+ hosted AI products, sorted into buckets by the job they do, each with what it replaces and what it costs | Monthly (11) |
| [`oss-spotlight`](recipes/oss-spotlight/README.md) | Pulls seven open-source news feeds, then Claude writes a six-section editorial read on the period — releases, community news, hidden gems — graded by significance | Monthly (8) |
| [`cool-websites`](recipes/cool-websites/README.md) | Claude finds and verifies 28+ genuinely useful, lesser-known websites across 8–12 categories, never repeating an earlier run | Monthly (18) |
| [`top-10-github-repos`](recipes/top-10-github-repos/README.md) | Fetches GitHub Trending's weekly feeds, then Claude ranks the ten strongest AI and developer-tooling repos with what is driving each | Monthly (4) |
| [`trending-movers`](recipes/trending-movers/README.md) | Scrapes GitHub's weekly trending pages for stars gained, then Claude writes a star-velocity leaderboard in the measured order | Monthly (15) |
| [`signal-sources`](recipes/signal-sources/README.md) | Claude adds 12+ blogs, newsletters, changelogs and channels worth following to a cumulative reading list, each with a verified feed | Monthly (1) |
| [`security-toolkit`](recipes/security-toolkit/README.md) | Claude researches 24+ security tools across identity, detection, recon, AppSec, cloud and labs, with licences stated | Monthly (28) |
| [`finance-toolkit`](recipes/finance-toolkit/README.md) | Claude researches 22+ financial tools — market-data APIs, backtesting, broker SDKs, ledgers, finance AI — with verified free-tier caps | Monthly (25) |

**Images** — pack `ai-recipes-images`

| Recipe | Makes | Schedule |
|:---|:---|:---|
| [`comics`](recipes/comics/README.md) | Claude writes a four-panel comic strip in a rotating topic — script with dialogue, original fictional characters only — and the runner renders the full-page strip with short balloon lettering | Weekly (Wed) |
| [`ai-meme-generator`](recipes/ai-meme-generator/README.md) | Claude invents one original AI-and-tech-themed meme in a rotating theme, never a copied template or a real person, and the runner renders it square with the caption baked in | Tue, Fri |
| [`daily-poster`](recipes/daily-poster/README.md) | Claude designs a vertical poster on the next least-used of 200 themes — art movements, nature, science, space, myth, architecture — and the runner renders it at 2:3 | Mon, Thu |
| [`future-cities`](recipes/future-cities/README.md) | Claude imagines a real city 475 years forward — landmarks, climate adaptation, transport, a named colour grade — and the runner renders one cinematic 16:9 cityscape | Weekly (Sat) |
| [`image-prompt-packs`](recipes/image-prompt-packs/README.md) | Claude writes a themed pack of 5–8 reusable, copy-ready image prompts — negative prompts, aspect ratios, style tags, use cases — and every prompt gets a rendered example image | Weekly (Sat) |
| [`wallpaper-packs`](recipes/wallpaper-packs/README.md) | Three themed wallpapers from a rotating pool of twelve, each with a random lighting, palette, mood and framing twist, delivered as a matching 16:9 desktop and 9:16 phone pair cropped from one render | Weekly (Sun) |
| [`icon-packs`](recipes/icon-packs/README.md) | Claude designs a cohesive pack of 12 icons and draws each symbol as SVG; code adds an identical container to all twelve and ships SVG, transparent 1024 px PNG and multi-size ICO | Weekly (Wed) |
| [`weekend-yearly-collections`](recipes/weekend-yearly-collections/README.md) | Advances every long-running image collection by one researched entry — Science Breakthroughs year by year, Technology Milestones, Exoplanets, or your own — configured in an editable collections.json | Tue, Sat |

**Audio** — pack `ai-recipes-audio`

| Recipe | Makes | Schedule |
|:---|:---|:---|
| [`song-generator`](recipes/song-generator/README.md) | Claude writes an original song in the type you choose — weekly news song, rock, country, rap, psychedelic, folk, jazz and more, most with a comedy twin — as lyrics plus an ElevenLabs composition plan, then the runner renders the MP3 and a square cover | Weekly (Wed) |
| [`podcast-script-generator`](recipes/podcast-script-generator/README.md) | Claude writes a 1,500–3,000-word AI-vs-AI debate podcast episode as a speaker-labelled transcript, with a fictional cast (or your own recurring cast cards) and an optional topic queue, plus a square cover | Weekly (Fri) |
| [`weekly-audio-podcast`](recipes/weekly-audio-podcast/README.md) | Renders the oldest unrendered podcast script to an episode: Claude casts a preset voice per speaker and writes show notes, then every line is spoken with Gemini or ElevenLabs text-to-speech | Weekly (Sat) |
| [`voiceover-script-generator`](recipes/voiceover-script-generator/README.md) | Claude researches a real-world story and writes a 90–180-second narration with direction notes; the runner narrates it with a preset voice and, with ffmpeg, cuts a vertical short from generated scene stills | Weekly (Sun) |

## Quick start

You need **Python 3.10+** and **[Claude Code](https://docs.claude.com/claude-code)** signed in (a
Claude subscription or an `ANTHROPIC_API_KEY`). Media needs its own keys:

| Output | Key | Without it |
|:---|:---|:---|
| Covers | `GEMINI_API_KEY` or `OPENAI_API_KEY` | Published without a cover |
| Image recipes (comics, wallpapers, …) | `GEMINI_API_KEY` or `OPENAI_API_KEY` | The run fails before the agent starts |
| Speech (podcast, voiceover) | `GEMINI_API_KEY` or `ELEVENLABS_API_KEY` | The run fails before the agent starts |
| Music (songs) | `ELEVENLABS_API_KEY` | The run fails before the agent starts |

`ffmpeg` is optional: with it, audio is MP3 and voiceovers get a vertical video; without it, WAV and no video.
Voices are always premade presets — these recipes never clone a voice.

```bash
git clone https://github.com/ai-automation-tools/ai-automation-recipes
cd ai-automation-recipes
pip install -r requirements.txt
cp .env.example .env          # add GEMINI_API_KEY or OPENAI_API_KEY, and RECIPES_OUTPUT_DIR

python recipes/daily-app-card/run.py --output-dir ~/ai-output --dry-run   # see the prompt
python recipes/daily-app-card/run.py --output-dir ~/ai-output             # run it
```

Every recipe takes the same flags:

| Flag | Default | Does |
|:---|:---|:---|
| `--output-dir` | `$RECIPES_OUTPUT_DIR` | Root for all output |
| `--model` | per recipe | Claude model alias (`sonnet`, `opus`, `haiku`) |
| `--image-engine` | `auto` | `auto`, `gemini`, `openai`, or `none` |
| `--speech-engine` | `auto` | `auto`, `gemini`, or `elevenlabs` (audio recipes) |
| `--date` | today | Target date, `YYYY-MM-DD` |
| `--dry-run` | — | Print the filled prompt and exit, no agent call |
| `--keep-staging` | — | Keep a failed run's working folder for inspection |

Plus recipe-specific overrides (`--category`, `--genre`, `--cuisine`, `--region`, …) — see each recipe's README.

## Schedule them with Cronsole

[Cronsole](https://cronsole.ai-automation-tools.dev) imports these as templates. Import everything with the
**AI Content Recipes** pack ([`registry/packs/ai-recipes.json`](registry/packs/ai-recipes.json)), one
category pack (`ai-recipes-apps-games`, `-writing`, `-food-maps`, `-digests`, `-images`, `-audio`), or one
template at a
time from [`registry/templates/`](registry/templates/). Each asks for your
clone's path and an output folder. Add **AI Recipes: Update Clone** too, so the clone stays current.

API keys go in Cronsole's task secrets or the clone's `.env` — never in a template parameter.

Not using Cronsole? Each template's `commandTemplate` is a plain command line that cron, Task
Scheduler or launchd can run as-is.

## What a run produces

```text
<output-dir>/
├── runs.jsonl                         # one line per successful run
└── idea-cards/
    └── 2026-10/
        └── 2026-10-14_receipt-radar/
            ├── artifact.json          # title, summary, fields, model, cover prompt
            ├── card.md
            └── cover.png
```

A run either publishes a complete folder or nothing. The agent works in a private staging folder,
the runner checks every promised file, renders the cover, and only then moves it into place.

## Browse what it made

```bash
python scripts/build_viewer.py --output-dir ~/ai-output
```

That writes `index.html` and `catalog.js` into the output folder: a single page that lists every
artifact by collection, with covers, search, rendered Markdown, playable games and apps in a
sandboxed frame, image galleries, and audio and video players. Open it straight from disk, or serve
the folder from any static host. Schedule **AI Recipes: Rebuild Viewer** (in every pack) to keep it
current.

## How it works

```text
run.py ──▶ core/runner.py ──▶ engine (claude --print, in a staging folder)
                │                   │
                │                   └─ writes files + returns JSON (title, summary, cover_prompt…)
                ├─ validates files, removes strays
                ├─ core/images  ──▶ Gemini or OpenAI renders cover.png
                └─ moves the folder into place, writes artifact.json, appends runs.jsonl
```

- **The agent can only write to its staging folder.** Claude runs with `--permission-mode dontAsk`
  and an explicit tool allowlist; anything else is denied.
- **The agent never holds an image key.** It describes the cover; the runner renders it.
- **Skills ship with the repo** in [`.claude/skills/`](.claude/skills/) and are copied into each
  run's staging folder, so a run behaves the same on every machine.

More in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). Adding a recipe:
[`docs/ADDING-A-RECIPE.md`](docs/ADDING-A-RECIPE.md).

## Costs and limits

- Claude usage counts against your subscription or API account. The game recipe on `opus` is the
  heaviest; switch it to `sonnet` if usage matters more than polish.
- Each cover or image is one billed image call; wallpapers render at Gemini's 4K tier.
- A song is one ElevenLabs Music generation; podcasts and voiceovers bill per line of speech.
- Recipes that search the web cite real sources, but check them before you act on a card.

## Project docs

[Roadmap](docs/ROADMAP.md) · [Changelog](docs/CHANGELOG.md) · [Architecture](docs/ARCHITECTURE.md) · [Adding a recipe](docs/ADDING-A-RECIPE.md)

## License

Code: [MIT](LICENSE). Bundled skills keep their own licenses — `humanizer` is MIT © Siqi Chen (see
its folder). What the recipes generate on your machine is yours.
