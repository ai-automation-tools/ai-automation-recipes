# CLAUDE.md — ai-automation-recipes

Public recipes for scheduled Claude Code automations, importable into Cronsole. Read
`docs/ARCHITECTURE.md` before changing `core/`.

- **This repo is meant to be public.** Never add personal names, domains, hostnames, home paths or
  private repo references. Run `python scripts/check_public.py` before every commit.
- **`registry/` is generated.** Edit `recipes/*/cronsole.json` or `cronsole/*.json`, then
  `python scripts/build_registry.py`. Never hand-edit `registry/`: Cronsole verifies sha256 over
  exact bytes, and the files must stay LF.
- **Templates never carry secrets.** No parameter may hold an API key; keys come from the
  environment (`.env` or Cronsole task secrets).
- **Skills are named, not pasted.** `.claude/skills/` is the source of truth; a prompt carries only
  the carve-outs a skill can't know.
- **Recipe names say what they make, never how often** (`browser-game`, not `weekly-browser-game`).
  Schedules belong to whoever imports the template; READMEs and the recipe index don't list them.
- **Docs follow the repo-docs-builder layout:** every folder has a README index with a header,
  catalog table and footer nav. A new recipe also goes into `recipes/README.md` and `CATEGORY_PACKS`.
- **Agents get the narrowest tool list that works.** No `Bash` in a recipe without a reason in its
  README.
- Python 3.10+, stdlib `unittest` (`python -m unittest discover -s tests`), `logging` not `print`
  (the dry-run prompt dump is the one exception).
- Before a PR: dry-run the recipe you touched, run the tests, `build_registry.py --check`,
  `check_public.py`.
