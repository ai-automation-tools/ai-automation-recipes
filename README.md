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

| Recipe | Makes | Default schedule |
|:---|:---|:---|
| [`daily-app-card`](recipes/daily-app-card/README.md) | A one-page app pitch grounded in a current trend, with sources and a concept-art cover | Daily |
| [`weekly-browser-game`](recipes/weekly-browser-game/README.md) | A complete single-file HTML game in a rotating genre, plus a design brief and key art | Saturdays |
| [`weekly-short-story`](recipes/weekly-short-story/README.md) | A finished 2,000–4,000-word story in a rotating genre, with a portrait cover | Sundays |

## Quick start

You need **Python 3.10+** and **[Claude Code](https://docs.claude.com/claude-code)** signed in (a
Claude subscription or an `ANTHROPIC_API_KEY`). Cover images need a Gemini or OpenAI key; without
one, recipes publish without a cover.

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
| `--date` | today | Target date, `YYYY-MM-DD` |
| `--dry-run` | — | Print the filled prompt and exit, no agent call |
| `--keep-staging` | — | Keep a failed run's working folder for inspection |

Plus recipe-specific overrides: `--category`, `--genre`.

## Schedule them with Cronsole

[Cronsole](https://cronsole.ai-automation-tools.dev) imports these as templates. Import the
**AI Content Recipes** pack from [`registry/packs/ai-recipes.json`](registry/packs/ai-recipes.json),
or one template at a time from [`registry/templates/`](registry/templates/). Each asks for your
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
- Each cover is one billed image call.
- Recipes that search the web cite real sources, but check them before you act on a card.

## Project docs

[Roadmap](docs/ROADMAP.md) · [Changelog](docs/CHANGELOG.md) · [Architecture](docs/ARCHITECTURE.md) · [Adding a recipe](docs/ADDING-A-RECIPE.md)

## License

Code: [MIT](LICENSE). Bundled skills keep their own licenses — `humanizer` is MIT © Siqi Chen (see
its folder). What the recipes generate on your machine is yours.
