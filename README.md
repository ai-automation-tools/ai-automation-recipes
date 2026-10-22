<a id="readme-top"></a>

<p align="center">
  <a href="recipes/README.md">
    <img src="images/icon.svg" alt="AI Automation Recipes: scheduled Claude Code automations that write, build, draw and compose into a folder you can browse" width="120">
  </a>
</p>

<h1 align="center">AI Automation Recipes</h1>

<p align="center">
  <em>Scheduled Claude Code automations that research, write, build, draw and compose,<br>packaged as templates you can import into Cronsole.</em>
</p>

<p align="center">
  <a href="docs/README.md"><strong>Explore the docs »</strong></a>
</p>

<p align="center">
  <a href="https://ai-automation-recipes-demo.ai-automation-tools.dev">See live samples</a>
  ·
  <a href="recipes/README.md">Browse the recipes</a>
  ·
  <a href="https://github.com/ai-automation-tools/ai-automation-recipes/issues">Report Bug</a>
  ·
  <a href="https://github.com/ai-automation-tools/ai-automation-recipes/issues">Request Feature</a>
</p>

<p align="center">
  <a href="recipes/README.md"><img src="https://img.shields.io/badge/recipes-48-2ea44f?style=for-the-badge" alt="48 recipes"></a>
  <img src="https://img.shields.io/badge/status-experimental-F59E0B?style=for-the-badge" alt="Status: experimental">
  <a href="docs/ROADMAP.md"><img src="https://img.shields.io/badge/plan-ROADMAP-8B5CF6?style=for-the-badge" alt="Roadmap"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Claude_Code-headless-D97757?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code">
  <img src="https://img.shields.io/badge/Cronsole-Registry_v1-A78BFA?style=flat-square" alt="Cronsole Registry v1">
  <img src="https://img.shields.io/badge/Gemini_·_OpenAI-images-4285F4?style=flat-square" alt="Gemini or OpenAI images">
  <img src="https://img.shields.io/badge/ElevenLabs-music_·_speech-000000?style=flat-square" alt="ElevenLabs music and speech">
  <img src="https://img.shields.io/badge/license-MIT-16A34A?style=flat-square" alt="MIT">
</p>

---

## 📦 What's in here

A **recipe** is one automation: a prompt, the skills it loads, a small Python runner and a Cronsole
template. Run one by hand to see what it makes, or schedule it and let a collection build up: app
pitches, playable games, short stories, songs, research digests.

| Folder | What it holds |
|:---|:---|
| [**🍳 recipes/**](recipes/README.md) | The 48 recipes, grouped, each with its own README |
| [**⚙️ core/**](core/README.md) | The shared runner: engines, images, audio, video, checks |
| [**📚 docs/**](docs/README.md) | Architecture, the recipe guide, roadmap and changelog |
| [**🧰 scripts/**](scripts/README.md) | Registry builder, viewer builder, the pre-publish leak scan |
| [**📋 registry/**](registry/README.md) | The generated Cronsole catalog: templates and packs |
| [**🧠 .claude/skills/**](.claude/skills/README.md) | The skills recipes load, with their licenses |
| [**🧪 tests/**](tests/README.md) | Unit tests and faked-engine runs of every recipe |
| [**🖼️ viewer/index.html**](viewer/index.html) | The page `build_viewer.py` copies into an output folder |
| [**🏠 homepage/**](homepage/index.html) | The project homepage, published to GitHub Pages by `.github/workflows/homepage.yml` |

## 🍳 The recipes

| Group | Recipes | For example |
|:---|:---|:---|
| [**🧩 Apps & Games**](recipes/README.md#-apps--games) | 8 | A Manifest V3 extension, a playable HTML game, a 3D-print spec |
| [**📝 Writing**](recipes/README.md#-writing) | 6 | Short stories, a serialized novella, alternate histories |
| [**🍲 Food & Maps**](recipes/README.md#-food--maps) | 4 | Safety-checked recipes with a Cook's Card, this week's viral dish, interactive maps |
| [**🔎 Research Digests**](recipes/README.md#-research-digests) | 11 | Agent tooling, trending repos, a model benchmark watch, a nine-topic news digest |
| [**🎨 Images**](recipes/README.md#-images) | 8 | Comics, posters, 4K wallpapers, SVG icon packs |
| [**🎧 Audio**](recipes/README.md#-audio) | 4 | Songs, a two-step debate podcast, narrated shorts |

When a recipe runs is your call. Templates ship with a default schedule you change on import.

## 🚀 Quick start

You need Python 3.10+ and [Claude Code](https://docs.claude.com/claude-code) signed in, with either a
Claude subscription or an `ANTHROPIC_API_KEY`. The Codex CLI and the Gemini CLI also work as the
agent (`--engine codex`, `--engine gemini`); both are wired and unit-tested but have not written a
real recipe yet, so Claude is the default and the only engine the Cronsole templates expose.

```bash
git clone https://github.com/ai-automation-tools/ai-automation-recipes
cd ai-automation-recipes
pip install -r requirements.txt
cp .env.example .env          # add your image key
python recipes/app-idea-card/run.py --dry-run   # print the prompt, no agent call
python recipes/app-idea-card/run.py             # run it for real: lands in ./output
python scripts/build_viewer.py --serve          # browse everything at http://localhost:8000
```

Output goes to `output/` inside the clone, which git ignores. Set `RECIPES_OUTPUT_DIR` in `.env`
(or pass `--output-dir`) to keep it somewhere else; the viewer follows the same setting.

### Keys

| Output | Key | Without it |
|:---|:---|:---|
| Covers | `GEMINI_API_KEY` or `OPENAI_API_KEY` | Published without a cover |
| Image recipes | `GEMINI_API_KEY` or `OPENAI_API_KEY` | The run stops before the agent starts |
| Speech | `GEMINI_API_KEY` or `ELEVENLABS_API_KEY` | The run stops before the agent starts |
| Music | `ELEVENLABS_API_KEY` | The run stops before the agent starts |

`ffmpeg` is optional. With it, audio is MP3 and voiceovers get a vertical video; without it you get
WAV and no video. Voices are always premade presets. Nothing here clones a voice.

<details>
<summary><b>Flags every recipe takes</b></summary>

| Flag | Default | Does |
|:---|:---|:---|
| `--output-dir` | `$RECIPES_OUTPUT_DIR`, else `./output` | Root for all output (git-ignored by default) |
| `--engine` | `claude` | The agent that writes: `claude`, `codex` or `gemini` (the last two have had no live run yet) |
| `--model` | per recipe | Claude model alias (`sonnet`, `opus`, `haiku`) or a full model id. On `codex` and `gemini` an alias means that CLI's default |
| `--image-engine` | `auto` | `auto`, `gemini`, `openai` or `none` |
| `--speech-engine` | `auto` | `auto`, `gemini` or `elevenlabs` |
| `--date` | today | Target date, `YYYY-MM-DD` |
| `--dry-run` | off | Print the filled prompt and exit |
| `--keep-staging` | off | Keep a failed run's working folder for inspection |

Recipes add their own overrides (`--category`, `--genre`, `--cuisine`, `--type`…). Each recipe's
README lists them.

</details>

## 📅 Schedule them with Cronsole

[Cronsole](https://cronsole.ai-automation-tools.dev) imports the recipes as templates, in two
editions:

| Edition | Template id | Needs | Best for |
|:---|:---|:---|:---|
| **Cronsole edition** *(pilot: short-story, comics, podcast-episode)* | `recipe-<name>-cronsole`, pack `ai-recipes-cronsole` | Python and the agent CLI where Cronsole runs. Nothing else: the first run fetches a pinned, sha256-checked runtime into your cache | Importing and forgetting. Keys are optional task secrets (`${secret.GEMINI_API_KEY?}`) |
| **Clone edition** | `recipe-<name>` | A clone of this repo and a `.env` | Editing prompts, or any scheduler: each command is a plain command line that cron, Task Scheduler or launchd can run as it is |

Take everything with the `ai-recipes` pack, one group pack (`ai-recipes-apps-games`, `-writing`,
`-food-maps`, `-digests`, `-images`, `-audio`), or single templates. The [registry README](registry/README.md)
has the details. Clone-edition packs also carry two helpers: **Update Clone** keeps the clone
current and **Rebuild Viewer** refreshes the browsable page. A template never takes a key as a
parameter.

**Both editions run on any agent CLI.** Pick it with the template's *Agent CLI* parameter or
`--engine`: Claude Code (the default), Codex, Gemini CLI, OpenCode, Kimi Code or Grok Build. Each
CLI is one JSON profile in [`core/engines/clis/`](core/engines/clis/README.md); adding another is
adding a file, and a weekly check keeps the profiles in step with each CLI's releases.

Scheduling a whole pipeline rather than one recipe (ideas to plans, plans to PRs, one sweep to review
them)? The [`automated-dev-pipeline`](https://github.com/ai-automation-tools/agent-skills/tree/main/Skills/Core/Automation/automated-dev-pipeline)
skill in [agent-skills](https://github.com/ai-automation-tools/agent-skills) covers designing and
operating one, and [`task-router`](https://github.com/ai-automation-tools/agent-skills/tree/main/Skills/Core/Automation/task-router)
picks how much machinery a job needs.

## 📂 What a run makes

```text
output/                              # or $RECIPES_OUTPUT_DIR / --output-dir
├── index.html · catalog.js          # the viewer, after build_viewer.py
├── runs.jsonl                       # one line per published run
└── idea-cards/2026-10/2026-10-14_receipt-radar/
    ├── artifact.json                # title, summary, fields, model, cover prompt
    ├── card.md
    └── cover.png
```

A run publishes a complete folder or nothing. The agent works in a private staging folder, the runner
checks every file it promised, renders the media, and only then moves the folder into place.

### 🖥️ Browse what you've made

```bash
python scripts/build_viewer.py            # writes output/index.html + catalog.js
python scripts/build_viewer.py --serve    # same, then serves it at http://localhost:8000 (Ctrl+C stops)
python scripts/build_viewer.py --serve 9000 --title "My AI Library"
```

That gives you one page for everything the recipes made: collections, covers, search, rendered
Markdown, games and apps you can play in place, galleries, and audio and video players. Open
`output/index.html` straight from disk, or use `--serve` for a local site: it listens on
`localhost` only, and served, each item's **Open folder** button lists its files. Re-run the build
after new runs land (the **Rebuild Viewer** template schedules it); a running server picks up the
new catalog on refresh. Set `RECIPES_WEBHOOK_URL` to get a Discord or Slack message, or a JSON
POST, each time something new lands.

## 🧭 How it works

```text
run.py ─▶ core/runner.py ─▶ claude --print, inside a staging folder
               │                └─ writes the files, returns JSON (title, summary, prompts)
               ├─ checks the files, removes strays, runs the recipe's own checks
               ├─ renders images, speech and music from what the agent described
               └─ moves the folder into place, writes artifact.json
```

The [homepage](https://ai-automation-recipes.ai-automation-tools.dev/#how) shows the full run as an
interactive diagram with every step linked to its code; [`docs/diagrams/`](docs/diagrams/README.md)
holds its source and says how it stays current.

- The agent can only write to its staging folder: Claude runs under `--permission-mode dontAsk`
  with an explicit tool allowlist, and anything else is denied. Codex runs in its `workspace-write`
  sandbox; Gemini relies on the contract in the prompt. The recipe never knows which engine it got.
- The agent never holds a media key. It describes the cover or writes the composition plan, and the
  runner does the rendering.
- Skills ship in the repo and are copied into each run, so a run behaves the same on every machine.

## 💸 Costs and limits

- Claude usage counts against your subscription or API account. The game and story recipes default
  to `opus`; switch them to `sonnet` if usage matters more than polish.
- Each cover or image is one billed image call. Wallpapers render at Gemini's 4K tier, so they cost
  the most.
- A song is one ElevenLabs Music generation. Podcasts and voiceovers bill per spoken line.
- Research recipes cite real sources, but check a source before you act on it.
- 13 of the 48 recipes have had a real run so far; the rest have only run with the engines faked.
  The [roadmap](docs/ROADMAP.md#-live-test-status) tracks which.

## 📖 Documentation

| Document | What's in it |
|:---|:---|
| [**📚 Docs home**](docs/README.md) | The map of everything below |
| [**🧱 Architecture**](docs/ARCHITECTURE.md) | The run loop, `artifact.json`, engines and skills |
| [**🛠️ Adding a recipe**](docs/ADDING-A-RECIPE.md) | The four files a recipe needs and the checks before a PR |
| [**🗺️ Roadmap**](docs/ROADMAP.md) | Live-test status and what's left to build |
| [**📋 Changelog**](docs/CHANGELOG.md) | Every change, newest first |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<p align="center">
  Built with <a href="https://docs.claude.com/claude-code">Claude Code</a> ·
  scheduled with <a href="https://cronsole.ai-automation-tools.dev">Cronsole</a> ·
  <a href="LICENSE">MIT</a> code; bundled skills keep <a href=".claude/skills/README.md">their own licenses</a>
</p>
