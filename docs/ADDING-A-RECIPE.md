<h1 align="center">🛠️ Adding a Recipe</h1>

<p align="center">
  <em>Four files in one folder, then a few commands before the pull request.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/files-4-8B5CF6?style=for-the-badge" alt="4 files">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Docs home"></a>
</p>

---

A recipe is four files in `recipes/<name>/`. Copy `app-idea-card` and change what differs. Name it
for what it makes, not how often it runs: `browser-game`, not `weekly-browser-game`. The schedule
belongs to whoever imports the template. A recipe may keep its own data beside the four files when
that data is the thing a user would edit (`poster/themes.md`, `news-digest/topics.json`); read it in
`run.py`, never paste it into the prompt.

## 📝 1. `prompt.md`

The job description the agent reads. Keep these, in roughly this order:

- `{{RUN_CONTRACT}}` near the top: the headless rules every recipe shares.
- What this run is about: the rotation pick from `prepare()`, and `{{EXISTING}}` so the agent
  doesn't repeat itself.
- `{{SKILLS}}` and which skills to load before which step, with the carve-outs the skill can't know.
- `{{OUTPUT_FILES}}` and the exact format of each file.
- A cover section if the recipe has one: what to depict, and what is forbidden.
- **FINAL MESSAGE**: the JSON keys the runner reads. Always `title`, `slug`, `summary`,
  `cover_prompt` and `error`, plus your recipe's `fields` (and `images` with an `ImageSpec`).

Things that belong in code, not the prompt: dates, folder paths, rotation, deduplication lists,
validation the runner can do itself.

## 🐍 2. `run.py`

```python
RECIPE = Recipe(
    name="thing-maker",            # matches the folder
    collection="things",            # output subfolder
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("thing.md",),            # first one is the main file
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill"),   # add WebSearch/WebFetch if it researches
    fields=("genre",),              # extra required keys in the final JSON
    cover_aspect="16:9",            # or None for no cover
    default_model="sonnet",
    optional_files=("notes.md",),   # published when present, never required
    images=ImageSpec(min=1, max=4, aspects=("1:1",)),  # agent lists {file, prompt, aspect}; runner renders
                                    # optional=True: publish text-only when no image key is set
    requires=("speech",),           # "images" / "speech" / "music": fail before the agent if no key
    prepare=prepare,                # (ctx) -> dict of {{TOKENS}}; stash per-run data in ctx.state
    validate=validate,              # (staging, manifest[, ctx]): raise RecipeError to reject
    after_cover=after_cover,        # (ctx, staging, manifest) -> extra files that need the cover
    finish=finish,                  # (ctx, final, manifest): runs after publishing
)
```

Shared helpers live in `core/`: `core.web` for HTML/JS/extension checks, `core.food` for
recipes, `core.digest` for research digests (`digest_recipe()` builds a whole link-list digest;
`fetch_candidates()` on its own reads feeds for a briefing), `core.images.process` for
crops/ICO/SVG, `core.audio` for speech and music, `core.video` for slideshows. Raise `NothingToDo`
from `prepare()` when there is no work this run.

Give the agent the narrowest tool list that works. No `Bash` unless the recipe can't do without it.
Name tools the way Claude Code does; the Codex and Gemini engines treat the list as advisory, so
the prompt's contract has to carry any rule that matters.

## 📅 3. `cronsole.json`

A Registry v1 template. Copy an existing one and change `id` (`recipe-<name>`), `name`,
`description`, `tags`, a sensible default cron (5-field, UTC) and the path in `commandTemplate`. Keep
`recipesPath`, `outputDir`, `model` and `imageEngine` as parameters, and never add a parameter for
an API key.

Then rebuild the registry:

```bash
python scripts/build_registry.py
```

## 📖 4. `README.md`

Use the same shape as the others: a centered emoji title and one-line tagline, a badge row (default
model, any key it needs, a back link to `../README.md`), a facts table (output, model, tools,
skills), the recipe-specific flags, a sample once it has had a live run, and the run command. End
with the footer nav row. Leave the schedule out. Then add the recipe to its group in
[`recipes/README.md`](../recipes/README.md) and to `CATEGORY_PACKS` in `scripts/build_registry.py`.

## ✅ Before you open a PR

```bash
python recipes/<name>/run.py --output-dir ./output --dry-run   # prompt fills, no {{ left
python -m unittest discover -s tests
python scripts/build_registry.py --check
python scripts/check_public.py              # CI runs it with --history too
```

Then run it for real once and read what it made, and add the row to the roadmap's live-test table
(⬜ until that run has been read, played or listened to).

---

<p align="center">
  <a href="README.md">← Docs home</a> ·
  <a href="ARCHITECTURE.md">Architecture</a> ·
  <a href="ROADMAP.md">Next: Roadmap →</a>
</p>
