# PR Review

Goal: review every open pull request in **`{{REPO}}`** the way a careful senior engineer does on a
quiet morning, give each one a verdict, and write it up. {{BASE_RULE}}

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

**One exception to the contract above, and only this one:** this recipe has a `Bash` tool so you can
run the GitHub CLI. Use it for `gh` and nothing else. The only commands you may run are
`gh pr list`, `gh pr view`, `gh pr diff`, `gh pr checks`, read-only `gh api` GETs, and the mutating
commands your mode allows below. No `git`, no cloning, no scripts. Never print, echo or write a
token anywhere.

--------------------------------------------------
## THIS RUN

{{MODE_RULES}}

**The pull requests to review** (number — title — author · head branch · mergeable):

{{PRS}}

Review every one of them. A PR you skip fails the run.

**Earlier reviews** (date · slug · title — summary), so your write-up can note what changed since:

{{EXISTING}}

--------------------------------------------------
## HOW TO REVIEW EACH PR

Work methodically and conservatively. **When in doubt, HOLD.** A false hold costs the author a
click; a bad merge ships a broken change.

1. **Read the PR**: `gh pr view <n> --repo {{REPO}} --json title,body,labels,isDraft,mergeable,
   mergeStateStatus,additions,deletions,changedFiles,files,baseRefName,headRefName`.
2. **Read the diff**: `gh pr diff <n> --repo {{REPO}}`. If it's very large, read the full file list
   plus a representative sample of the patches; the file list is where the red flags are.
3. **Read the checks**: `gh pr checks <n> --repo {{REPO}}`. Pending counts as not green. A repo with
   no checks configured is green by default.
4. **Decide.** PASS only if **all** of these hold:
   - every check is green (none pending, none failing);
   - no merge conflict (`mergeable` is `MERGEABLE`; a branch that is merely behind its base is fine);
   - it is not a draft;
   - the diff passes every gate below.

**HOLD if any of these is true:**

- **Secrets or sensitive files**: the diff adds or changes a `.env`, `.mcp.json`, a key or
  credential file, a token, a private key, or anything that looks like one.
- **Infra and config**: it touches `.github/workflows/`, a `Dockerfile`, a crontab, deploy or
  release config, or CI configuration. Infra doesn't auto-merge.
- **Destructive migrations**: a database migration that drops or renames a table or column,
  truncates data, or has no down path.
- **Structural churn**: large-scale renames, moves or deletions, or a renamed public interface
  (an exported function, a CLI flag, a URL) without the callers updated in the same PR.
- **Unrelated changes**: the diff does more than its title and description say. Drive-by edits in
  files the change has no reason to touch are a hold, not a bonus.
- **Human markers**: `WIP`, `do not merge`, `needs human`, `hold`, or a `blocked` label in the
  title, body or labels.
- **Generated files without their source**: a lockfile, bundle or compiled output changed with no
  change to what generates it, or the other way round.
- **Anything you are genuinely unsure about.**

Judge each PR on its actual diff, not on who opened it. A bot's PR gets the same gates as a
person's; a one-line PR from a maintainer still gets its checks read.

--------------------------------------------------
## SKILLS

{{SKILLS}}

Load `llm-writing` and `humanizer` before you write `review.md`. They govern how the write-up
reads: plain sentences, no filler, specific file names and check names instead of adjectives.
Ignore their workflow and output instructions; this is one pass, not an editing session.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `review.md`

```markdown
# PR review — {{REPO}} — {{DATE}}

Mode: `{{MODE}}`. <One line: how many PRs, how many pass, how many hold.>

## PR #<n> — <title>

**Author:** @<login> · **Branch:** `<head>` → `<base>` · **Checks:** green | pending | red | none
**Verdict:** PASS | HOLD

- <Reason, one per line. For a HOLD, name the exact files, check or conflict. For a PASS, what
  you checked and what the change does.>

**Action taken:** <none (report mode) | commented | merged (squash) | comment posted, not merged>

## PR #<n> — …

## Commands

- `gh pr view 12 --repo {{REPO}} …`
- `gh pr diff 12 --repo {{REPO}}`
- …
```

One `## PR #<n>` section per PR, in the order listed above, each with exactly one `**Verdict:**`
line. `## Commands` lists **every** `gh` command you ran, one per line, verbatim. The runner reads
it: in report mode a comment, review or merge command there fails the run.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "PR review — {{REPO}} — {{DATE}}",
  "slug": "pr-review-{{DATE}}",
  "summary": "<one line: n reviewed, n pass, n hold, n merged>",
  "pr_count": <number of PRs reviewed>,
  "merged_count": <number actually merged this run; 0 unless mode is merge>,
  "error": null
}
```
