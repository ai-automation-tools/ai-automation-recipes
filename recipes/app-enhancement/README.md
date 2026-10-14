<h1 align="center">🔧 App Enhancement</h1>

<p align="center">
  <em>One small additive improvement to one static web app, delivered as a patch you can read first.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-nothing-2ea44f?style=for-the-badge" alt="Needs nothing">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Point it at a folder of static apps (each subfolder with an `index.html`). The runner picks the app
with the fewest enhancements so far, copies it, and the agent edits the copy: a filter, a sort, a
keyboard shortcut, an export, an empty state, an accessibility fix. The runner diffs the copy
against the original into `enhancement.patch`, checks the page still loads clean, and publishes the
patch beside the agent's note. Your app is untouched unless you ask.

| | |
|:---|:---|
| **Output** | `app-enhancements/<YYYY-MM>/<date>_<app>-<title>/` → `enhancement.md`, `enhancement.patch`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill |
| **Skills** | `llm-writing`, `humanizer` |
| **Needs** | Nothing. `node` on PATH and a browser make the checks stronger; both are skipped with a warning when missing |

## 🚩 Flags

| Flag | Does |
|:---|:---|
| `--apps-dir <path>` | The folder of apps. Required |
| `--app <name>` | Force one app instead of the rotation |
| `--apply` | Write the changed files back into the app after the run passes every check. Default off: the patch is the only output |

## 📏 The rules the agent works under

One enhancement, additive only, at most three files, no new files over 50 KB, no deleted files, no
new dependencies or external scripts, the app's own style. Anything the app renders from data has
to survive an entry that lacks the new field. These come from the enhancement job that kept a
fleet of library viewers growing for months without a rollback.

## ✅ What the runner checks

The copy differs from the original, by no more than three text files and no deletions. Then on the
modified copy: no missing local or non-HTTPS reference in `index.html`, `node --check` on every
script touched, and a headless-browser load with no uncaught error. The final JSON's `app` and
`files_changed` must match what the diff found.

The working copy lives in `app-enhancements/.work/` during the run and is removed afterwards. A run
that fails validation leaves it there for inspection; the next run replaces it.

## ▶️ Run it

```bash
python recipes/app-enhancement/run.py --output-dir ~/ai-output --apps-dir ~/sites/tools
python recipes/app-enhancement/run.py --output-dir ~/ai-output --apps-dir ~/sites/tools --app meme-wall --apply
```

---

<p align="center">
  <a href="../README.md">← All recipes</a>
</p>
