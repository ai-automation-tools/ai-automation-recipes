# Contributing

Thanks for looking. Two kinds of contribution are welcome, and one kind isn't.

**A new recipe.** Read [docs/ADDING-A-RECIPE.md](docs/ADDING-A-RECIPE.md): four files in one folder,
a dry run, the tests, the registry check and the leak scan. Open a *Recipe request* issue first if
you want to check the idea fits before you build it. A recipe that reads a source it isn't allowed
to won't be merged whatever its quality.

**A fix.** Open a *Bug in a recipe* issue with the log tail, or just send the PR with the failing
case in `tests/`. Prompt changes are code changes here: say what the old prompt got wrong and what
the new one does differently, and dry-run the recipe you touched.

**Not here:** anything about importing, scheduling or running templates. That is
[Cronsole](https://github.com/ai-automation-tools/cronsole/issues).

## Before you open a PR

```bash
python recipes/<name>/run.py --dry-run
python -m unittest discover -s tests
python scripts/build_registry.py --check
python scripts/check_public.py
```

Never commit an API key, a home path, an email address or output folders. `check_public.py` looks
for all of them and CI runs it over the whole history.

## House rules

[AGENTS.md](AGENTS.md) is written for an AI agent editing this repo and holds the rules that aren't
obvious from the code: the registry is generated, skills are named not pasted, recipe names say what
they make and never how often, agents get the narrowest tool list that works. They apply to people
too.

Code is MIT. Bundled skills keep [their own licenses](.claude/skills/README.md).
