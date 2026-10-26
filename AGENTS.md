# AGENTS.md — ai-automation-recipes

Public recipes for scheduled Claude Code automations, importable into Cronsole. These rules are for
every coding agent (Codex, Gemini CLI, opencode; Claude Code imports this file from `CLAUDE.md`). Read
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
  README. Tool names are Claude Code's; Codex and Gemini treat the list as advisory.
- **Any CLI, one contract.** Every engine is a JSON profile in `core/engines/clis/` read by
  `core/engines/cli.py`; a recipe never knows which it got, and a CLI fact lives only in its
  profile. Add or fix a CLI by editing a profile, then `python scripts/check_clis.py <name>`;
  `scripts/new_cli.py <binary>` drafts a profile for a new one. Runs use the profile on `main` when
  they can fetch it (`RECIPES_CLI_REMOTE=0` turns that off), so a merged profile fix is live for
  everyone within a day. Claude, Codex, Gemini and Antigravity have run recipes for real; each profile's `verified`
  block says how far the others got.
- **Two editions per recipe.** The clone edition is `recipes/<name>/cronsole.json`. The Cronsole
  edition (`recipe-<name>-cronsole`) is generated from it plus `cronsole/native-body.py` for every
  recipe in `NATIVE` in `scripts/build_registry.py`; never hand-write one.
- **The runtime bundle is pinned.** Anything under `core/`, `recipes/` or `.claude/skills/` changes
  the bundle the Cronsole editions download, so it needs a new `VERSION` (patch bump) and a
  `build_registry.py` run in the same change. CI fails a changed bundle under a released version.
- **Recipe-local data lives beside the four files** (`themes.md`, `topics.json`) and is read by
  `run.py`, never pasted into a prompt. `ImageSpec(optional=True)` is for images that are a bonus:
  the run publishes text-only without an image key instead of failing.
- **The run diagram is pinned to code.** `docs/diagrams/recipe-run-flow.json` cites `core/runner.py`
  and friends by line; edit only the JSON, then `node scripts/build-diagram.mjs --pin-head` (it also
  refreshes `homepage/diagram/`). `--check` names cited files that changed; see `docs/diagrams/README.md`.
- Python 3.10+, stdlib `unittest` (`python -m unittest discover -s tests`), `logging` not `print`
  (the dry-run prompt dump is the one exception).
- Before a PR: dry-run the recipe you touched, run the tests, `build_registry.py --check`,
  `check_public.py`.
