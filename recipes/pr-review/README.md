<h1 align="center">🔀 PR Review</h1>

<p align="center">
  <em>Every open pull request in one repo, read against a fixed set of gates, with a verdict each.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GitHub_CLI-0078D4?style=for-the-badge" alt="Needs the GitHub CLI logged in">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The runner lists the open PRs with `gh` before the agent starts. The agent reads each one's
description, diff and checks, decides PASS or HOLD, and writes the review. What it does beyond
writing depends on the mode you pick. The default does nothing to the repo.

| | |
|:---|:---|
| **Output** | `pr-reviews/<YYYY-MM>/<date>_pr-review-<date>/` → `review.md`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, Bash (for `gh` only) |
| **Skills** | `llm-writing`, `humanizer` |
| **Needs** | The GitHub CLI installed and logged in. Read access for report mode; write access for comment and merge |

## 🚦 Modes

| `--mode` | Does |
|:---|:---|
| `report` (default) | Writes the review. Read-only: the runner rejects the run if a comment, review or merge command appears in the review's command log |
| `comment` | Also posts one comment per PR: what was checked for a PASS, the exact files or check for a HOLD. Never merges |
| `merge` | Also squash-merges every PASS and leaves a hold comment on every HOLD. Squash only, never a rebase, a force-push, a close or a branch delete |

`--base main` narrows the run to PRs into one branch. Without it every open PR is reviewed.

## 🛑 The gates

A PR passes only with green checks, no conflict, not a draft, and a diff that clears all of these:
no secrets or credential files, no workflow, Dockerfile, crontab or deploy config, no destructive
migration, no large-scale rename or delete, no changes the title doesn't account for, no `WIP` or
`do not merge` marker, no generated file changed without its source. When in doubt, hold.

## ✅ What the runner checks

Every listed PR has a `## PR #n` section with one `**Verdict:**` line. The `## Commands` section
lists every `gh` call; report mode fails on a mutating one, comment mode fails on a merge.
`pr_count` must match the list and `merged_count` must be zero outside merge mode. No open PRs
is a clean skip, not a failure.

## ▶️ Run it

```bash
python recipes/pr-review/run.py --output-dir ~/ai-output --repo owner/name
python recipes/pr-review/run.py --output-dir ~/ai-output --repo owner/name --base main --mode merge
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../app-enhancement/README.md">Next: App Enhancement →</a>
</p>
