<h1 align="center">🧱 Architecture</h1>

<p align="center">
  <em>What happens between a recipe starting and its folder being published, and the contract a viewer can rely on.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/artifact-schema_v1-0078D4?style=for-the-badge" alt="artifact.json schema v1">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Docs home"></a>
</p>

---

## 🗂️ Layout

| Path | Holds |
|:---|:---|
| `recipes/<name>/` | One automation: `prompt.md`, `run.py`, `cronsole.json`, `README.md`, plus any data a user would edit (`themes.md`, `topics.json`) |
| `core/runner.py` | The run loop every recipe shares |
| `core/web.py` | Checks for HTML/JS output: references, `node --check`, Manifest V3, JSON, sources CSV, and a headless-browser smoke test |
| `core/food/` | The recipe-validator safety gate, allergen fix-ups and the Cook's Card |
| `core/digest/` | The research-digest toolkit: feed and GitHub Trending fetchers, digest parser, bookmark/OPML writers, shared rules |
| `core/run-contract.md` | The headless rules spliced into every prompt as `{{RUN_CONTRACT}}` |
| `core/engines/` | Text engines behind one interface: `claude`, `codex` and `gemini` |
| `core/images/` | Image rendering (Gemini, then OpenAI) and `process.py`: crops, ICO, SVG → PNG |
| `core/audio/` | Speech (Gemini or ElevenLabs, preset voices only) and ElevenLabs music |
| `core/video.py` | Optional ffmpeg slideshow for vertical shorts |
| `core/deliver.py` | Optional webhook announcement of each published artifact |
| `core/artifacts.py` | Output layout, `artifact.json`, rotation and do-not-repeat helpers |
| `.claude/skills/` | Skills the recipes load, copied into each run's staging folder |
| `cronsole/` | The two helper templates that aren't recipes: Update Clone and Rebuild Viewer |
| `registry/` | **Generated.** The Cronsole registry, built by `scripts/build_registry.py` |
| `scripts/check_public.py` | Pre-publish scan for keys, personal paths and a private denylist |
| `viewer/index.html` | The viewer page; `scripts/build_viewer.py` copies it into an output folder beside a generated `catalog.js` |
| `tests/` | `unittest` coverage of the run loop, media steps, recipes and the viewer, with every engine faked |

## 🔁 The run loop

1. **Read the collection.** `load_existing()` reads every `artifact.json` under the recipe's
   collection. Recipes use it to rotate categories and genres (`least_used`) and to show the agent
   what already exists (`{{EXISTING}}`).
2. **Fill the prompt.** `{{TOKENS}}` come from the runner (`DATE`, `RUN_CONTRACT`, `EXISTING`,
   `OUTPUT_FILES`, `SKILLS`) and from the recipe's `prepare()` hook. A leftover token fails the run
   before any agent call.
3. **Stage.** A fresh folder under `<collection>/.staging/` gets a copy of the recipe's skills in
   `.claude/skills/`.
4. **Run the engine** with that folder as its working directory and the recipe's tool allowlist.
5. **Check the result.** The agent's last JSON object must have `title`, `summary`, the recipe's
   `fields` and a `cover_prompt`, or an `error`. Every file in `files` must exist and be non-empty
   (subfolder paths like `extension/manifest.json` are allowed; `optional_files` are kept when
   present); any other top-level entry is deleted. The recipe's `validate()` hook runs here (the game
   recipe syntax-checks its script); it may take the run context as a third argument.
6. **Render media.** Any `images` the agent listed (for recipes with an `ImageSpec`; an `optional`
   spec is skipped, not failed, when no image key is set), then the cover
   from `cover_prompt`, each with the no-text constraint (or lettering-only for `text_ok`). Then the
   recipe's `after_cover()` hook adds files that need them: the Cook's Card, wallpaper crops, icon
   PNG/ICO, rendered speech and music, the short video.
7. **Publish.** Move the folder to `<collection>/<YYYY-MM>/<date>_<slug>/`, write `artifact.json`,
   run the `finish()` hook, append to `runs.jsonl`.

Any failure before step 7 publishes nothing. Before step 3, a recipe's `requires` (and any
`ImageSpec`) is checked against the keys that are set, so a missing key fails before the agent runs;
`prepare()` can raise `NothingToDo` to skip the run with exit 0.

## 📄 `artifact.json`

Schema `ai-automation-recipes/artifact@1`, written into every published folder.

```json
{
  "schema": "ai-automation-recipes/artifact@1",
  "recipe": "app-idea-card",
  "recipe_version": "0.1.0",
  "collection": "idea-cards",
  "title": "Receipt Radar",
  "slug": "receipt-radar",
  "date": "2026-10-14",
  "summary": "Finds refunds you are owed.",
  "files": { "main": "card.md", "cover": "cover.png" },
  "fields": { "category": "Browser Extension", "form_factor": "browser extension", "monetization": "freemium" },
  "generator": {
    "engine": "claude", "model": "claude-sonnet-5-5",
    "image_engine": "gemini", "image_model": "gemini-3.1-flash-image",
    "cover_prompt": "…"
  },
  "created_at": "2026-10-14T11:04:12+00:00"
}
```

This is the contract with any viewer. Add fields freely; bump the schema only for a breaking change.

## 🤖 Engines

An engine implements `preflight()` and `run(EngineRequest) -> EngineResult` (see
`core/engines/base.py`) and says where its agent looks for project skills (`skills_dir`). The
request carries the prompt, the staging folder, the tool allowlist, model and timeout; the result
is the agent's final message and the model that produced it. `--engine` picks one; a recipe never
knows which it got.

Every engine is one CLI described by a JSON profile in
[`core/engines/clis/`](../core/engines/clis/README.md), read by `core/engines/cli.py`. The profile
says how to launch the CLI headless, how the prompt gets in, and where the final message, errors and
model sit in what it prints.

| Engine | Runs | Writes are confined by | Tool allowlist | Skills staged to |
|:---|:---|:---|:---|:---|
| `claude` (default) | `claude --print --output-format json` | `--permission-mode dontAsk` plus the recipe's `--allowedTools` | Enforced | `.claude/skills/` |
| `codex` | `codex exec --json -s workspace-write -C <staging>` | the `workspace-write` sandbox | Advisory: Codex has none, the contract in the prompt is the rule | `.agents/skills/` |
| `gemini` | `gemini -p -o json --approval-mode yolo` | nothing but the contract | Advisory | `.gemini/skills/` |
| `opencode` | `opencode run --auto --format json -f <prompt file>` | nothing but the contract | Advisory | `.opencode/skills/` |
| `kimi` | `kimi -p <prompt> --output-format stream-json` | nothing but the contract | Advisory | `.kimi/skills/` |
| `grok` | `grok --prompt-file <file> --output-format plain --always-approve` | nothing but the contract | Advisory | `.grok/skills/` |

A recipe's `default_model` is a Claude alias (`sonnet`, `opus`, `haiku`). Every other CLI treats an
alias as "your own default" and passes a full model id through unchanged. The image, speech and music
steps are the runner's, so they are identical whichever engine wrote the prompts.

Only Claude has run a recipe for real. Codex and Gemini are tested against recorded output; OpenCode
and Kimi answered a smoke prompt; Grok's flags are checked against its `--help`. Each profile's
`verified` block says which. `scripts/check_clis.py` checks every flag a profile passes against the
installed CLI's `--help`, and the weekly upstream routine ([UPSTREAMS.md](UPSTREAMS.md)) keeps the
profiles current.

Adding one means a profile, no code. Recipes don't change: they name their tools the way Claude Code
does; a CLI with no per-tool allowlist gets them through the prompt's contract.

## 📦 The Cronsole edition

`scripts/build_registry.py` turns each recipe in its `NATIVE` list into a second template,
`recipe-<name>-cronsole`: a Cronsole `script` action built from [`cronsole/native-body.py`](../cronsole/native-body.py).
It needs no clone. On its first run it downloads the runtime bundle for `VERSION` from the GitHub
release, checks the sha256 the template pins, unpacks it with a private virtualenv into the user's
cache, and runs the recipe from there. API keys come from optional task secrets
(`${secret.NAME?}`), and the verdict line is printed first because Cronsole keeps only the first
2,000 characters of a run.

`scripts/build_bundle.py` builds that bundle reproducibly: the same tree gives the same bytes on any
OS. Any change under `core/`, `recipes/` or `.claude/skills/` changes it, so it needs a new
`VERSION`. CI refuses a changed bundle under a version that's already released, and the release
workflow publishes `v<VERSION>` only when the rebuilt bundle hashes to what `registry/` pins.

## 🧠 Skills

Recipes name skills; they never paste skill text into a prompt, so the copy in
[`.claude/skills/`](../.claude/skills/README.md) is the only one. A skill that reads like it was written for an interactive session gets
carve-outs in the prompt ("skip the audit, the output format wins"), not edits to the skill.

---

<p align="center">
  <a href="README.md">← Docs home</a> ·
  <a href="../core/README.md">Core</a> ·
  <a href="ADDING-A-RECIPE.md">Next: Adding a recipe →</a>
</p>
