# Adding a recipe

[← README](../README.md)

A recipe is four files in `recipes/<name>/`. Copy `daily-app-card` and change what differs.

## 1. `prompt.md`

The job description the agent reads. Keep these, in roughly this order:

- `{{RUN_CONTRACT}}` near the top — the headless rules every recipe shares.
- What this run is about: the rotation pick from `prepare()`, and `{{EXISTING}}` so the agent
  doesn't repeat itself.
- `{{SKILLS}}` and which skills to load before which step, with the carve-outs the skill can't know.
- `{{OUTPUT_FILES}}` and the exact format of each file.
- A cover section if the recipe has one: what to depict, and what is forbidden.
- **FINAL MESSAGE**: the JSON keys the runner reads — always `title`, `slug`, `summary`,
  `cover_prompt`, `error`, plus your recipe's `fields`.

Things that belong in code, not the prompt: dates, folder paths, rotation, deduplication lists,
validation the runner can do itself.

## 2. `run.py`

```python
RECIPE = Recipe(
    name="weekly-thing",            # matches the folder
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
    prepare=prepare,                # (ctx) -> dict of {{TOKENS}}; stash per-run data in ctx.state
    validate=validate,              # (staging, manifest[, ctx]): raise RecipeError to reject
    after_cover=after_cover,        # (ctx, staging, manifest) -> extra files that need the cover
    finish=finish,                  # (ctx, final, manifest): runs after publishing
)
```

Shared helpers live in `core/`: `core.web` for HTML/JS/extension checks, `core.food` for
recipes, `core.digest` for research digests (`digest_recipe()` builds a whole digest recipe).

Give the agent the narrowest tool list that works. No `Bash` unless the recipe can't do without it.

## 3. `cronsole.json`

A Registry v1 template. Copy an existing one and change `id` (`recipe-<name>`), `name`,
`description`, `tags`, the cron (5-field, UTC) and the path in `commandTemplate`. Keep
`recipesPath`, `outputDir`, `model` and `imageEngine` as parameters, and never add a parameter for
an API key.

Then rebuild the registry:

```bash
python scripts/build_registry.py
```

## 4. `README.md`

What it makes, a sample of the output, the schedule, the cost driver, and any recipe-specific flags.

## Before you open a PR

```bash
python recipes/<name>/run.py --output-dir ./output --dry-run   # prompt fills, no {{ left
python -m unittest discover -s tests
python scripts/build_registry.py --check
python scripts/check_public.py
```

Then run it for real once and read what it made.
